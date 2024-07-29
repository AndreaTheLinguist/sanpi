# `ALL`: Collect bigrams corresponding to top adverbs


```python
import pandas as pd
from am_notebooks import (load_bigram_dfs, locate_bigram_am_paths,
                          nb_show_table, show_adv_bigrams)

from source.utils.associate import TOP_AM_DIR, adjust_assoc_columns
from source.utils.general import confirm_dir, print_iter, timestamp_today

ADV_FLOOR = 5000
K = 8

DATA_DATE = '2024-07-28'
TAG = 'ALL'
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
confirm_dir(TOP_AM_TAG_DIR)

data_top = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / data_top
confirm_dir(OUT_DIR)

# for loading `polar/*/bigram/*` tables
bigram_floor = 25 
mirror_floor = 5 
if TAG=='ALL':
    bigram_floor, mirror_floor = [x*2 for x in (bigram_floor, mirror_floor)]
```

## Set columns and diplay settings


```python
FOCUS = ['f',
         'am_p1_given2', 'am_p1_given2_simple', 
         'conservative_log_ratio',
         'am_log_likelihood',
          'mutual_information',
         'am_odds_ratio_disc', 't_score',
         'N', 'f1', 'f2', 'E11', 'unexpected_f',
         'l1', 'l2', 
         'adv', 'adv_total', 'adj', 'adj_total']
pd.set_option('display.max_colwidth', 30)
pd.set_option('display.max_columns', 9)
pd.set_option('display.width', 120)
pd.set_option("display.precision", 2)
pd.set_option("styler.format.precision", 2)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.2f}'.format)
```

(MOVED the following to `./am_notebooks.py`)


```python
# def force_ints(_df):
#     count_cols = _df.filter(regex=r'total|^[fN]').columns
#     _df[count_cols] = _df[count_cols].astype('int')
#     # _df[count_cols] = _df[:, count_cols].astype('int64')
#     # print(_df.dtypes.to_frame('dtypes'))
#     return _df


# def nb_show_table(df, n_dec: int = 2,
#                   adjust_columns: bool = True,
#                   outpath: Path = None,
#                   return_df: bool = False) -> None:
#     _df = df.copy()
#     try:
#         start_0 = _df.index.start == 0
#     except AttributeError:
#         pass
#     else:
#         _df.index.name = 'rank'
#         if start_0:
#             _df.index = _df.index + 1
#     if adjust_columns:
#         _df = adjust_assoc_columns(_df)
#     _df.columns = [f'`{c}`' for c in _df.columns]
#     _df.index = [f'**{r}**' for r in _df.index]
#     table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
#     if outpath:
#         outpath.write_text(table)

#     print(f'\n{table}\n')
#     return (_df if return_df else None)
# from pprint import pprint
# from source.utils.dataframes import catify_hit_table as catify


# bigram_am_paths = {d.name:
              
#                   tuple(d.joinpath('bigram/extra').glob(
#                       f'*{TAG}*min{mirror_floor if d.name.endswith("mirror") else bigram_floor}x*extra.parq'))[0]
                  
#               for d in POLAR_DIR.iterdir()}

# pprint(bigram_am_paths)
# bigram_dfs = {n: catify(update_index(pd.read_parquet(p)), 
#                         reverse=True) 
#               for n, p in bigram_am_paths.items()}

# def show_adv_bigrams(sample_size, C, 
#                      bigram_dfs, 
#                      selector: str = 'dP1', 
#                      column_list: list = None) -> dict:
#     def _force_ints(_df):
#         count_cols = _df.filter(regex=r'total$|^[fN]').columns
#         _df.loc[:, count_cols] = _df.loc[:, count_cols].apply(
#             pd.to_numeric, downcast='unsigned')
#         return _df

#     def get_top_bigrams(bdf, adv, bigram_k):
#         bdf = _force_ints(bdf.loc[bdf.adv == adv, :])
#         top_by_metric = [bdf.nlargest(bigram_k * 2, m) for m in ['dP1', 'LRC']]
#         half_k = bigram_k // 2
#         adv_pat_bigrams = pd.concat(
#             [top_bigrams.head(half_k) for top_bigrams in top_by_metric]).drop_duplicates()
#         x = 0
#         while len(adv_pat_bigrams) < min(bigram_k, len(bdf)):
#             x += 1
#             next_ix = half_k + x
            
#             try:
#                 next_entries = [top_by_metric[0].iloc[[next_ix], :], 
#                             top_by_metric[1].iloc[[next_ix], :]]
#             except IndexError:
#                 print(f'All bigrams for {adv} retrieved.')
#                 break
#             else:
#                 adv_pat_bigrams = pd.concat((adv_pat_bigrams, 
#                                          *next_entries)).drop_duplicates()
#         return adv_pat_bigrams.head(bigram_k)

#     bigram_k = max(sample_size + 2, 10)
#     print(
#         f'## Top {bigram_k} "most negative" bigrams corresponding to top {sample_size} adverbs\n')
#     print(timestamp_today())
#     patterns = list(bigram_dfs.keys())
#     top_adverbs = C.index
#     bigram_samples = {adv: dict.fromkeys(
#         patterns + ['both', 'adj']) for adv in top_adverbs}
#     bigrams, adj = [], []

#     for rank, adv in enumerate(top_adverbs, start=1):
#         print(f'\n### {rank}. _{adv}_\n')
#         adj_for_adv = []
#         adv_top = None

#         for pat, bdf in bigram_dfs.items():
#             bdf = adjust_assoc_columns(
#                 bdf[[c for c in FOCUS + ['adj', 'adj_total', 'adv', 'adv_total'] if c in bdf.columns]])
#             bdf = bdf.loc[bdf.LRC >= 1, :]
#             adv_pat_bigrams = get_top_bigrams(bdf, adv, bigram_k)

#             if adv_pat_bigrams.empty:
#                 print(f'No bigrams found in loaded `{pat}` AM table.')
#             else:
#                 print(
#                     f'\n#### Top {len(adv_pat_bigrams)} `{pat}` "{adv}_*" bigrams (sorted by `{selector}`; `LRC > 1`)\n')
#                 column_list = column_list if column_list is not None else bdf.columns
#                 nb_show_table(adv_pat_bigrams.filter(column_list), n_dec=2)

#             adj_for_adv.extend(adv_pat_bigrams.adj.drop_duplicates().to_list())
#             bigram_samples[adv][pat] = adv_pat_bigrams
#             if adv_top is None: 
#                 adv_top = adv_pat_bigrams 
#             else:
#                 adv_top = pd.concat([df.fillna('') for df in (adv_top, adv_pat_bigrams)])

#         bigram_samples[adv]['adj'] = set(adj_for_adv)
#         bigrams.extend(adv_top.l2.drop_duplicates().to_list())
#         adj.extend(adj_for_adv)
#         bigram_samples[adv]['both'] = adv_top

#     bigram_samples['bigrams'] = set(bigrams)
#     bigram_samples['adj'] = set(adj)
#     return bigram_samples, bigram_k
```

## Load data


```python
bigram_dfs = load_bigram_dfs(locate_bigram_am_paths(TAG, mirror_floor, bigram_floor))

try:
    combined_am_csv = tuple(OUT_DIR.glob(
                   f'{TAG}-Top{K}_NEG-ADV_combined-{ADV_FLOOR}*.{DATA_DATE or timestamp_today()}.csv'))[0]
except IndexError:
    combined_am_csv = tuple(TOP_AM_TAG_DIR.rglob(
        f'{TAG}-Top{K}_NEG-ADV_combined*.csv'))[0]
print(f'Loaded from: "{combined_am_csv}"')

C = adjust_assoc_columns(pd.read_csv(combined_am_csv, index_col='adv'))

main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in ('LRC', 'P1', 'G2')],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2']])
                              ).to_list()
C
```

    {'RBdirect': PosixPath('/share/compling/projects/sanpi/results/assoc_df/polar/RBdirect/bigram/extra/polarized-bigram_ALL-direct_min50x_extra.parq'),
     'mirror': PosixPath('/share/compling/projects/sanpi/results/assoc_df/polar/mirror/bigram/extra/polarized-bigram_ALL-mirror_min10x_extra.parq')}
    Loaded from: "/share/compling/projects/sanpi/results/top_AM/ALL/ALL-Top8/ALL-Top8_NEG-ADV_combined-5000.2024-07-28.csv"





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
      <th>...</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>necessarily</th>
      <td>NEGany~necessarily</td>
      <td>42595</td>
      <td>0.83</td>
      <td>0.87</td>
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
samples_dict, bigram_k = show_adv_bigrams(
    K, C, bigram_dfs,
    column_list=[
        *pd.Series(main_cols_ordered).str.replace(
            r'mean_|_SET|_MIR', '', regex=True)
        .drop_duplicates().to_list(),
        'adv_total', 'adj_total',
        # 't', 'MI'
    ]
)
```

    ## Top 10 "most negative" bigrams corresponding to top 8 adverbs
    
    2024-07-28
    
    ### 1. _necessarily_
    
    
    #### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                       |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~necessarily_useful**         |    6.75 |    0.96 |   1.00 |   651.75 |   104 | 3,173,660 |    104 |        48,947 |       227,709 |
    | **NEGany~necessarily_fun**            |    6.62 |    0.96 |   1.00 |   601.61 |    96 | 3,173,660 |     96 |        48,947 |       190,026 |
    | **NEGany~necessarily_essential**      |    6.57 |    0.96 |   1.00 |   582.81 |    93 | 3,173,660 |     93 |        48,947 |        69,845 |
    | **NEGany~necessarily_reliable**       |    6.35 |    0.96 |   1.00 |   507.61 |    81 | 3,173,660 |     81 |        48,947 |        90,598 |
    | **NEGany~necessarily_proud**          |    6.14 |    0.96 |   1.00 |   444.94 |    71 | 3,173,660 |     71 |        48,947 |       207,536 |
    | **NEGany~necessarily_indicative**     |    9.43 |    0.95 |   0.99 | 8,577.54 | 1,389 | 3,173,660 |  1,400 |        48,947 |         8,148 |
    | **NEGany~necessarily_easy**           |    9.01 |    0.95 |   0.99 | 5,605.64 |   909 | 3,173,660 |    917 |        48,947 |       579,827 |
    | **NEGany~necessarily_representative** |    8.34 |    0.95 |   0.99 | 2,996.58 |   487 | 3,173,660 |    492 |        48,947 |        18,355 |
    | **NEGany~necessarily_surprising**     |    8.33 |    0.95 |   1.00 | 2,117.16 |   340 | 3,173,660 |    341 |        48,947 |        70,540 |
    | **NEGany~necessarily_new**            |    7.94 |    0.94 |   0.98 | 2,923.82 |   482 | 3,173,660 |    492 |        48,947 |       253,862 |
    
    
    #### Top 7 `mirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~necessarily_right**   |    2.15 |    0.83 |   1.00 |  81.13 |    23 | 291,732 |     23 |         1,107 |         5,576 |
    | **NEGmir~necessarily_illegal** |    1.20 |    0.83 |   1.00 |  52.91 |    15 | 291,732 |     15 |         1,107 |           937 |
    | **NEGmir~necessarily_wrong**   |    5.04 |    0.81 |   0.98 | 698.74 |   211 | 291,732 |    216 |         1,107 |        20,880 |
    | **NEGmir~necessarily_new**     |    1.84 |    0.79 |   0.96 |  73.19 |    23 | 291,732 |     24 |         1,107 |        12,836 |
    | **NEGmir~necessarily_bad**     |    2.95 |    0.77 |   0.94 | 154.45 |    50 | 291,732 |     53 |         1,107 |        10,261 |
    | **NEGmir~necessarily_true**    |    2.69 |    0.73 |   0.90 | 150.42 |    53 | 291,732 |     59 |         1,107 |         6,191 |
    | **NEGmir~necessarily_better**  |    1.63 |    0.70 |   0.87 |  72.90 |    27 | 291,732 |     31 |         1,107 |        14,013 |
    
    
    ### 2. _that_
    
    
    #### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                             |   `LRC` |   `dP1` |   `P1` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------|--------:|--------:|-------:|----------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~that_far-fetched** |    5.83 |    0.96 |   1.00 |    369.74 |    59 | 3,173,660 |     59 |       208,262 |         5,185 |
    | **NEGany~that_thrilled**    |    5.83 |    0.96 |   1.00 |    369.74 |    59 | 3,173,660 |     59 |       208,262 |        24,182 |
    | **NEGany~that_uncommon**    |    9.43 |    0.95 |   1.00 |  4,998.32 |   802 | 3,173,660 |    804 |       208,262 |        11,312 |
    | **NEGany~that_surprising**  |    9.20 |    0.95 |   0.99 |  6,986.81 | 1,133 | 3,173,660 |  1,143 |       208,262 |        70,540 |
    | **NEGany~that_dissimilar**  |    7.86 |    0.95 |   0.99 |  1,871.65 |   304 | 3,173,660 |    307 |       208,262 |         4,605 |
    | **NEGany~that_unusual**     |    8.92 |    0.95 |   0.99 |  6,003.05 |   977 | 3,173,660 |    988 |       208,262 |        71,234 |
    | **NEGany~that_complicated** |    8.68 |    0.94 |   0.98 |  7,337.84 | 1,207 | 3,173,660 |  1,230 |       208,262 |       159,822 |
    | **NEGany~that_hard**        |    8.59 |    0.91 |   0.96 | 58,817.24 | 9,948 | 3,173,660 | 10,380 |       208,262 |       348,463 |
    | **NEGany~that_familiar**    |    8.35 |    0.93 |   0.97 |  6,781.11 | 1,126 | 3,173,660 |  1,156 |       208,262 |       156,296 |
    | **NEGany~that_noticeable**  |    7.65 |    0.95 |   0.99 |  1,621.81 |   264 | 3,173,660 |    267 |       208,262 |        31,467 |
    
    
    #### Top 10 `mirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                             |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~that_keen**        |    2.73 |    0.83 |   1.00 |   109.35 |    31 | 291,732 |     31 |         5,494 |         1,360 |
    | **NEGmir~that_impressive**  |    2.15 |    0.83 |   1.00 |    81.13 |    23 | 291,732 |     23 |         5,494 |         5,007 |
    | **NEGmir~that_fond**        |    1.84 |    0.79 |   0.96 |    73.19 |    23 | 291,732 |     24 |         5,494 |         1,115 |
    | **NEGmir~that_comfortable** |    1.84 |    0.79 |   0.96 |    73.19 |    23 | 291,732 |     24 |         5,494 |         4,642 |
    | **NEGmir~that_clear**       |    1.30 |    0.78 |   0.95 |    56.03 |    18 | 291,732 |     19 |         5,494 |         6,722 |
    | **NEGmir~that_simple**      |    4.36 |    0.72 |   0.90 | 1,340.19 |   474 | 291,732 |    529 |         5,494 |        25,408 |
    | **NEGmir~that_easy**        |    4.23 |    0.71 |   0.89 | 1,248.84 |   450 | 291,732 |    508 |         5,494 |        18,610 |
    | **NEGmir~that_great**       |    3.57 |    0.66 |   0.84 |   725.16 |   286 | 291,732 |    342 |         5,494 |         5,568 |
    | **NEGmir~that_big**         |    3.17 |    0.69 |   0.86 |   300.54 |   113 | 291,732 |    131 |         5,494 |         8,177 |
    | **NEGmir~that_popular**     |    3.15 |    0.76 |   0.93 |   195.15 |    65 | 291,732 |     70 |         5,494 |         5,668 |
    
    
    ### 3. _exactly_
    
    
    #### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                               |   `LRC` |   `dP1` |   `P1` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------|--------:|--------:|-------:|----------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~exactly_conducive**  |    7.82 |    0.96 |   1.00 |  1,303.50 |   208 | 3,173,660 |    208 |        58,643 |         9,110 |
    | **NEGany~exactly_shocking**   |    7.33 |    0.96 |   1.00 |    946.29 |   151 | 3,173,660 |    151 |        58,643 |        35,115 |
    | **NEGany~exactly_pleasant**   |    7.24 |    0.96 |   1.00 |    889.88 |   142 | 3,173,660 |    142 |        58,643 |        52,223 |
    | **NEGany~exactly_famous**     |    7.10 |    0.96 |   1.00 |    814.68 |   130 | 3,173,660 |    130 |        58,643 |       223,813 |
    | **NEGany~exactly_difficult**  |    7.05 |    0.96 |   1.00 |    789.62 |   126 | 3,173,660 |    126 |        58,643 |       732,106 |
    | **NEGany~exactly_easy**       |    9.32 |    0.95 |   0.99 |  6,596.91 | 1,066 | 3,173,660 |  1,073 |        58,643 |       579,827 |
    | **NEGany~exactly_new**        |    9.10 |    0.94 |   0.99 |  8,410.32 | 1,371 | 3,173,660 |  1,388 |        58,643 |       253,862 |
    | **NEGany~exactly_cheap**      |    8.96 |    0.95 |   0.99 |  4,281.59 |   691 | 3,173,660 |    695 |        58,643 |        60,531 |
    | **NEGany~exactly_clear**      |    8.78 |    0.94 |   0.98 | 10,578.33 | 1,746 | 3,173,660 |  1,784 |        58,643 |       349,214 |
    | **NEGany~exactly_surprising** |    8.71 |    0.95 |   1.00 |  2,743.34 |   440 | 3,173,660 |    441 |        58,643 |        70,540 |
    
    
    #### Top 4 `mirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~exactly_sure**  |    5.31 |    0.83 |   1.00 | 522.11 |   148 | 291,732 |    148 |         1,041 |         6,761 |
    | **NEGmir~exactly_easy**  |    1.86 |    0.83 |   1.00 |  70.55 |    20 | 291,732 |     20 |         1,041 |        18,610 |
    | **NEGmir~exactly_clear** |    3.38 |    0.81 |   0.98 | 173.89 |    52 | 291,732 |     53 |         1,041 |         6,722 |
    | **NEGmir~exactly_new**   |    2.31 |    0.80 |   0.97 |  93.90 |    29 | 291,732 |     30 |         1,041 |        12,836 |
    
    
    ### 4. _any_
    
    
    #### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                         |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~any_happier**  |    6.34 |    0.82 |   0.86 | 4,420.49 |   828 | 3,173,660 |    963 |        34,382 |        16,606 |
    | **NEGany~any_younger**  |    5.57 |    0.79 |   0.83 | 1,323.36 |   255 | 3,173,660 |    307 |        34,382 |        26,216 |
    | **NEGany~any_nicer**    |    4.75 |    0.76 |   0.81 |   486.82 |    96 | 3,173,660 |    119 |        34,382 |         9,955 |
    | **NEGany~any_simpler**  |    5.00 |    0.71 |   0.75 | 1,087.71 |   226 | 3,173,660 |    300 |        34,382 |        23,480 |
    | **NEGany~any_brighter** |    3.91 |    0.67 |   0.72 |   292.00 |    63 | 3,173,660 |     88 |        34,382 |         9,280 |
    | **NEGany~any_easier**   |    5.08 |    0.62 |   0.66 | 6,987.78 | 1,594 | 3,173,660 |  2,405 |        34,382 |       209,940 |
    | **NEGany~any_cheaper**  |    4.01 |    0.58 |   0.63 |   542.97 |   129 | 3,173,660 |    206 |        34,382 |        46,055 |
    | **NEGany~any_smarter**  |    4.00 |    0.63 |   0.67 |   394.95 |    89 | 3,173,660 |    132 |        34,382 |         8,501 |
    | **NEGany~any_clearer**  |    4.26 |    0.54 |   0.58 | 1,421.60 |   355 | 3,173,660 |    608 |        34,382 |        11,680 |
    | **NEGany~any_worse**    |    3.94 |    0.42 |   0.46 | 5,676.37 | 1,686 | 3,173,660 |  3,673 |        34,382 |       179,012 |
    
    
    #### Top 10 `mirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~any_younger**   |    1.86 |    0.83 |   1.00 |    70.55 |    20 | 291,732 |     20 |         1,197 |           939 |
    | **NEGmir~any_clearer**   |    1.50 |    0.83 |   1.00 |    59.97 |    17 | 291,732 |     17 |         1,197 |           130 |
    | **NEGmir~any_different** |    3.24 |    0.81 |   0.98 |   159.93 |    48 | 291,732 |     49 |         1,197 |        36,166 |
    | **NEGmir~any_bigger**    |    2.73 |    0.80 |   0.97 |   118.17 |    36 | 291,732 |     37 |         1,197 |         3,923 |
    | **NEGmir~any_easier**    |    3.04 |    0.75 |   0.92 |   181.65 |    61 | 291,732 |     66 |         1,197 |         2,386 |
    | **NEGmir~any_better**    |    4.38 |    0.74 |   0.91 | 1,096.01 |   380 | 291,732 |    419 |         1,197 |        14,013 |
    | **NEGmir~any_worse**     |    2.73 |    0.66 |   0.83 |   217.46 |    87 | 291,732 |    105 |         1,197 |         8,790 |
    | **NEGmir~any_higher**    |    1.42 |    0.74 |   0.91 |    61.24 |    21 | 291,732 |     23 |         1,197 |         2,893 |
    | **NEGmir~any_closer**    |    2.33 |    0.65 |   0.83 |   141.82 |    57 | 291,732 |     69 |         1,197 |           993 |
    | **NEGmir~any_good**      |    2.12 |    0.74 |   0.91 |    93.53 |    32 | 291,732 |     35 |         1,197 |        31,585 |
    
    
    ### 5. _remotely_
    
    
    #### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~remotely_surprising** |    5.07 |    0.85 |   0.89 |   413.61 |    75 | 3,173,660 |     84 |        16,426 |        70,540 |
    | **NEGany~remotely_ready**      |    4.16 |    0.74 |   0.78 |   287.63 |    58 | 3,173,660 |     74 |        16,426 |       141,590 |
    | **NEGany~remotely_true**       |    4.61 |    0.63 |   0.68 | 1,111.13 |   250 | 3,173,660 |    370 |        16,426 |       231,639 |
    | **NEGany~remotely_funny**      |    4.15 |    0.60 |   0.65 |   589.74 |   137 | 3,173,660 |    212 |        16,426 |       122,927 |
    | **NEGany~remotely_qualified**  |    3.13 |    0.52 |   0.56 |   222.79 |    57 | 3,173,660 |    101 |        16,426 |        74,643 |
    | **NEGany~remotely_close**      |    3.65 |    0.39 |   0.43 | 2,243.22 |   694 | 3,173,660 |  1,597 |        16,426 |       411,329 |
    | **NEGany~remotely_comparable** |    2.98 |    0.38 |   0.43 |   375.73 |   118 | 3,173,660 |    277 |        16,426 |        12,252 |
    | **NEGany~remotely_accurate**   |    2.10 |    0.33 |   0.37 |   143.78 |    50 | 3,173,660 |    134 |        16,426 |       152,299 |
    | **NEGany~remotely_interested** |    2.74 |    0.27 |   0.31 |   817.06 |   330 | 3,173,660 |  1,062 |        16,426 |       264,528 |
    | **NEGany~remotely_similar**    |    2.20 |    0.23 |   0.27 |   334.61 |   152 | 3,173,660 |    559 |        16,426 |       203,453 |
    
    
    #### Top 10 `mirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~remotely_believable**  |    1.96 |    0.83 |   1.00 |  74.08 |    21 | 291,732 |     21 |         2,341 |           600 |
    | **NEGmir~remotely_surprising**  |    1.50 |    0.83 |   1.00 |  59.97 |    17 | 291,732 |     17 |         2,341 |         2,662 |
    | **NEGmir~remotely_comparable**  |    2.72 |    0.76 |   0.94 | 134.02 |    44 | 291,732 |     47 |         2,341 |           283 |
    | **NEGmir~remotely_true**        |    3.04 |    0.75 |   0.92 | 181.65 |    61 | 291,732 |     66 |         2,341 |         6,191 |
    | **NEGmir~remotely_new**         |    1.00 |    0.69 |   0.86 |  50.62 |    19 | 291,732 |     22 |         2,341 |        12,836 |
    | **NEGmir~remotely_close**       |    3.28 |    0.65 |   0.82 | 532.96 |   218 | 291,732 |    267 |         2,341 |        13,874 |
    | **NEGmir~remotely_funny**       |    1.85 |    0.63 |   0.80 |  97.91 |    41 | 291,732 |     51 |         2,341 |         5,365 |
    | **NEGmir~remotely_similar**     |    1.70 |    0.49 |   0.66 | 127.32 |    71 | 291,732 |    107 |         2,341 |         7,011 |
    | **NEGmir~remotely_possible**    |    1.42 |    0.56 |   0.73 |  78.73 |    38 | 291,732 |     52 |         2,341 |         3,160 |
    | **NEGmir~remotely_interesting** |    1.80 |    0.56 |   0.73 | 115.20 |    56 | 291,732 |     77 |         2,341 |        12,447 |
    
    
    ### 6. _ever_
    
    
    #### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                           |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |       `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------|--------:|--------:|-------:|---------:|------:|-----------:|-------:|--------------:|--------------:|
    | **NEGany~ever_simple**    |    5.56 |    0.80 |   0.84 | 1,109.28 |   211 |  3,173,660 |    250 |       114,075 |       396,749 |
    | **NEGany~ever_boring**    |    4.46 |    0.76 |   0.80 |   362.74 |    72 |  3,173,660 |     90 |       114,075 |        45,891 |
    | **NEGany~ever_easy**      |    5.41 |    0.73 |   0.77 | 2,105.13 |   429 |  3,173,660 |    555 |       114,075 |       579,827 |
    | **NEGany~ever_certain**   |    4.80 |    0.72 |   0.76 |   713.34 |   147 |  3,173,660 |    193 |       114,075 |        74,952 |
    | **NEGany~ever_sure**      |    3.34 |    0.49 |   0.54 |   328.20 |    87 |  3,173,660 |    162 |       114,075 |       262,825 |
    | **NEGany~ever_good**      |    3.81 |    0.46 |   0.50 | 1,188.69 |   331 |  3,173,660 |    660 |       114,075 |     1,681,795 |
    | **COM~ever_closer**       |    3.51 |    0.04 |   1.00 |   538.66 | 6,305 | 69,662,736 |  6,307 |       114,075 |        61,475 |
    | **NEGany~ever_enough**    |    3.54 |    0.45 |   0.50 |   618.62 |   173 |  3,173,660 |    347 |       114,075 |       152,020 |
    | **NEGany~ever_perfect**   |    3.34 |    0.40 |   0.44 |   706.71 |   216 |  3,173,660 |    489 |       114,075 |       104,659 |
    | **NEGany~ever_satisfied** |    2.57 |    0.38 |   0.42 |   203.01 |    64 |  3,173,660 |    151 |       114,075 |        62,862 |
    
    
    #### Top 10 `mirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                         |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~ever_simple**  |    5.82 |    0.83 |   1.00 |   726.76 |   206 | 291,732 |    206 |         5,060 |        25,408 |
    | **NEGmir~ever_enough**  |    5.30 |    0.83 |   1.00 |   518.58 |   147 | 291,732 |    147 |         5,060 |         2,596 |
    | **NEGmir~ever_certain** |    5.26 |    0.83 |   1.00 |   504.47 |   143 | 291,732 |    143 |         5,060 |         1,800 |
    | **NEGmir~ever_boring**  |    3.80 |    0.83 |   1.00 |   201.07 |    57 | 291,732 |     57 |         5,060 |         1,961 |
    | **NEGmir~ever_black**   |    3.77 |    0.83 |   1.00 |   197.54 |    56 | 291,732 |     56 |         5,060 |         1,412 |
    | **NEGmir~ever_easy**    |    6.44 |    0.83 |   1.00 | 1,285.01 |   368 | 291,732 |    369 |         5,060 |        18,610 |
    | **NEGmir~ever_good**    |    5.68 |    0.82 |   0.99 | 1,013.87 |   299 | 291,732 |    303 |         5,060 |        31,585 |
    | **NEGmir~ever_perfect** |    5.57 |    0.82 |   1.00 |   714.47 |   206 | 291,732 |    207 |         5,060 |         3,134 |
    | **NEGmir~ever_sick**    |    3.15 |    0.83 |   1.00 |   137.57 |    39 | 291,732 |     39 |         5,060 |         1,895 |
    | **NEGmir~ever_able**    |    4.17 |    0.78 |   0.95 |   426.52 |   136 | 291,732 |    143 |         5,060 |         3,704 |
    
    
    ### 7. _yet_
    
    
    #### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                           |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~yet_eligible**   |    8.96 |    0.96 |   1.00 |  2,807.56 |    448 | 3,173,660 |    448 |        95,763 |        23,252 |
    | **NEGany~yet_official**   |    8.61 |    0.96 |   1.00 |  2,205.93 |    352 | 3,173,660 |    352 |        95,763 |         6,853 |
    | **NEGany~yet_convinced**  |    7.50 |    0.96 |   1.00 |  1,059.09 |    169 | 3,173,660 |    169 |        95,763 |        12,132 |
    | **NEGany~yet_online**     |    6.66 |    0.96 |   1.00 |    614.14 |     98 | 3,173,660 |     98 |        95,763 |        15,650 |
    | **NEGany~yet_mainstream** |    6.11 |    0.96 |   1.00 |    438.67 |     70 | 3,173,660 |     70 |        95,763 |        17,792 |
    | **NEGany~yet_clear**      |   10.77 |    0.95 |   0.99 | 64,409.97 | 10,406 | 3,173,660 | 10,476 |        95,763 |       349,214 |
    | **NEGany~yet_ready**      |    9.93 |    0.94 |   0.99 | 45,985.07 |  7,501 | 3,173,660 |  7,599 |        95,763 |       141,590 |
    | **NEGany~yet_complete**   |    9.20 |    0.94 |   0.98 | 13,277.09 |  2,174 | 3,173,660 |  2,208 |        95,763 |        86,361 |
    | **NEGany~yet_final**      |    8.97 |    0.95 |   1.00 |  3,972.92 |    640 | 3,173,660 |    643 |        95,763 |         5,860 |
    | **NEGany~yet_over**       |    7.21 |    0.95 |   0.99 |  1,003.13 |    162 | 3,173,660 |    163 |        95,763 |         3,983 |
    
    
    #### Top 5 `mirror` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~yet_available** |    2.54 |    0.83 |   1.00 |  98.77 |    28 | 291,732 |     28 |           815 |        10,284 |
    | **NEGmir~yet_certain**   |    1.96 |    0.83 |   1.00 |  74.08 |    21 | 291,732 |     21 |           815 |         1,800 |
    | **NEGmir~yet_sure**      |    1.75 |    0.83 |   1.00 |  67.02 |    19 | 291,732 |     19 |           815 |         6,761 |
    | **NEGmir~yet_clear**     |    1.75 |    0.83 |   1.00 |  67.02 |    19 | 291,732 |     19 |           815 |         6,722 |
    | **NEGmir~yet_ready**     |    1.63 |    0.83 |   1.00 |  63.49 |    18 | 291,732 |     18 |           815 |         3,034 |
    
    
    ### 8. _immediately_
    
    
    #### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                    |   `LRC` |   `dP1` |   `P1` |       `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------------------|--------:|--------:|-------:|-----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~immediately_possible**    |    7.62 |    0.91 |   0.95 |   5,845.77 |  1,000 | 3,173,660 |  1,054 |        96,973 |       245,272 |
    | **NEGany~immediately_clear**       |    8.16 |    0.89 |   0.94 | 141,186.69 | 24,416 | 3,173,660 | 26,038 |        96,973 |       349,214 |
    | **NEGany~immediately_reachable**   |    5.56 |    0.86 |   0.91 |     610.53 |    109 | 3,173,660 |    120 |        96,973 |         2,672 |
    | **NEGany~immediately_sure**        |    5.40 |    0.82 |   0.86 |     738.65 |    138 | 3,173,660 |    160 |        96,973 |       262,825 |
    | **NEGany~immediately_certain**     |    4.19 |    0.71 |   0.75 |     336.68 |     70 | 3,173,660 |     93 |        96,973 |        74,952 |
    | **NEGany~immediately_available**   |    5.70 |    0.67 |   0.72 |  98,046.67 | 21,078 | 3,173,660 | 29,351 |        96,973 |       666,909 |
    | **NEGany~immediately_able**        |    4.70 |    0.59 |   0.63 |   2,655.18 |    626 | 3,173,660 |    989 |        96,973 |       223,196 |
    | **NEGany~immediately_obvious**     |    4.55 |    0.52 |   0.56 |   8,712.07 |  2,238 | 3,173,660 |  3,989 |        96,973 |       165,439 |
    | **NEGany~immediately_forthcoming** |    3.89 |    0.55 |   0.60 |     540.70 |    133 | 3,173,660 |    223 |        96,973 |         7,473 |
    | **NEGany~immediately_intuitive**   |    3.21 |    0.55 |   0.59 |     218.74 |     54 | 3,173,660 |     91 |        96,973 |        20,664 |
    
    
    #### Top 2 `mirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                  |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~immediately_clear**     |    1.13 |    0.55 |   0.72 |  62.95 |    31 | 291,732 |     43 |         1,195 |         6,722 |
    | **NEGmir~immediately_available** |    1.85 |    0.42 |   0.59 | 241.53 |   162 | 291,732 |    275 |         1,195 |        10,284 |
    
    
    ### 9. _particularly_
    
    
    #### Top 10 `RBdirect` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                       |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~particularly_likable**       |    5.53 |    0.85 |   0.89 |   657.49 |   119 | 3,173,660 |    133 |       513,668 |         8,160 |
    | **NEGany~particularly_likeable**      |    5.34 |    0.84 |   0.88 |   579.07 |   106 | 3,173,660 |    120 |       513,668 |         5,902 |
    | **NEGany~particularly_forthcoming**   |    4.85 |    0.82 |   0.87 |   387.25 |    72 | 3,173,660 |     83 |       513,668 |         7,473 |
    | **NEGany~particularly_religious**     |    6.12 |    0.81 |   0.86 | 2,585.71 |   485 | 3,173,660 |    565 |       513,668 |        28,028 |
    | **NEGany~particularly_original**      |    5.86 |    0.80 |   0.85 | 1,894.60 |   360 | 3,173,660 |    426 |       513,668 |        37,594 |
    | **NEGany~particularly_new**           |    6.04 |    0.79 |   0.83 | 3,874.46 |   747 | 3,173,660 |    900 |       513,668 |       253,862 |
    | **NEGany~particularly_athletic**      |    4.77 |    0.75 |   0.79 |   541.01 |   108 | 3,173,660 |    136 |       513,668 |        17,142 |
    | **NEGany~particularly_revolutionary** |    4.49 |    0.75 |   0.79 |   385.60 |    77 | 3,173,660 |     97 |       513,668 |        10,338 |
    | **NEGany~particularly_flashy**        |    4.08 |    0.73 |   0.77 |   278.96 |    57 | 3,173,660 |     74 |       513,668 |         4,494 |
    | **NEGany~particularly_surprising**    |    4.71 |    0.57 |   0.61 | 4,433.52 | 1,069 | 3,173,660 |  1,743 |       513,668 |        70,540 |
    
    
    #### Top 10 `mirror` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                       |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~particularly_novel**         |    3.71 |    0.83 |   1.00 |   190.49 |    54 | 291,732 |     54 |        13,003 |           320 |
    | **NEGmir~particularly_comfortable**   |    3.36 |    0.83 |   1.00 |   155.21 |    44 | 291,732 |     44 |        13,003 |         4,642 |
    | **NEGmir~particularly_revolutionary** |    3.15 |    0.83 |   1.00 |   137.57 |    39 | 291,732 |     39 |        13,003 |           485 |
    | **NEGmir~particularly_radical**       |    2.73 |    0.83 |   1.00 |   109.35 |    31 | 291,732 |     31 |        13,003 |         1,072 |
    | **NEGmir~particularly_fast**          |    2.39 |    0.83 |   1.00 |    91.71 |    26 | 291,732 |     26 |        13,003 |         1,259 |
    | **NEGmir~particularly_new**           |    5.92 |    0.81 |   0.99 | 1,365.17 |   404 | 291,732 |    410 |        13,003 |        12,836 |
    | **NEGmir~particularly_surprising**    |    5.06 |    0.82 |   0.99 |   564.67 |   166 | 291,732 |    168 |        13,003 |         2,662 |
    | **NEGmir~particularly_wrong**         |    5.05 |    0.81 |   0.98 |   702.22 |   212 | 291,732 |    217 |        13,003 |        20,880 |
    | **NEGmir~particularly_remarkable**    |    4.24 |    0.80 |   0.97 |   354.53 |   108 | 291,732 |    111 |        13,003 |         3,238 |
    | **NEGmir~particularly_close**         |    4.01 |    0.77 |   0.94 |   415.70 |   136 | 291,732 |    145 |        13,003 |        13,874 |
    
    
    ### 10. _inherently_
    
    All bigrams for inherently retrieved.
    
    #### Top 7 `RBdirect` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                   |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~inherently_wrong**       |    5.36 |    0.66 |   0.71 | 7,535.97 | 1,639 | 3,173,660 |  2,315 |        47,803 |       149,064 |
    | **NEGany~inherently_illegal**     |    3.51 |    0.60 |   0.64 |   252.59 |    59 | 3,173,660 |     92 |        47,803 |        30,194 |
    | **NEGany~inherently_bad**         |    4.62 |    0.56 |   0.61 | 3,270.68 |   794 | 3,173,660 |  1,307 |        47,803 |       429,537 |
    | **NEGany~inherently_negative**    |    2.50 |    0.35 |   0.39 |   222.63 |    75 | 3,173,660 |    193 |        47,803 |        53,385 |
    | **NEGany~inherently_evil**        |    2.81 |    0.28 |   0.32 |   905.80 |   358 | 3,173,660 |  1,123 |        47,803 |        22,706 |
    | **NEGany~inherently_good**        |    2.21 |    0.20 |   0.24 |   554.72 |   283 | 3,173,660 |  1,177 |        47,803 |     1,681,795 |
    | **NEGany~inherently_problematic** |    1.17 |    0.17 |   0.21 |    98.70 |    58 | 3,173,660 |    277 |        47,803 |        33,408 |
    
    All bigrams for inherently retrieved.
    
    #### Top 6 `mirror` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~inherently_improper** |    1.63 |    0.83 |   1.00 |    63.49 |    18 | 291,732 |     18 |         5,133 |           142 |
    | **NEGmir~inherently_illegal**  |    2.10 |    0.79 |   0.96 |    83.54 |    26 | 291,732 |     27 |         5,133 |           937 |
    | **NEGmir~inherently_wrong**    |    4.08 |    0.66 |   0.83 | 3,787.53 | 1,513 | 291,732 |  1,826 |         5,133 |        20,880 |
    | **NEGmir~inherently_bad**      |    2.86 |    0.62 |   0.79 |   342.53 |   148 | 291,732 |    188 |         5,133 |        10,261 |
    | **NEGmir~inherently_better**   |    1.65 |    0.57 |   0.75 |    93.95 |    44 | 291,732 |     59 |         5,133 |        14,013 |
    | **NEGmir~inherently_evil**     |    1.18 |    0.41 |   0.59 |    85.70 |    58 | 291,732 |     99 |         5,133 |         1,271 |
    
    
    ### 11. _terribly_
    
    
    #### Top 10 `RBdirect` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~terribly_surprising** |    8.66 |    0.94 |   0.98 | 5,794.10 |   949 | 3,173,660 |    964 |        58,964 |        70,540 |
    | **NEGany~terribly_uncommon**   |    6.33 |    0.94 |   0.98 |   625.85 |   103 | 3,173,660 |    105 |        58,964 |        11,312 |
    | **NEGany~terribly_likely**     |    6.26 |    0.93 |   0.97 |   649.50 |   108 | 3,173,660 |    111 |        58,964 |       890,421 |
    | **NEGany~terribly_productive** |    5.39 |    0.91 |   0.96 |   376.84 |    64 | 3,173,660 |     67 |        58,964 |       102,361 |
    | **NEGany~terribly_reliable**   |    4.99 |    0.90 |   0.94 |   296.70 |    51 | 3,173,660 |     54 |        58,964 |        90,598 |
    | **NEGany~terribly_original**   |    6.41 |    0.90 |   0.94 | 1,150.48 |   199 | 3,173,660 |    212 |        58,964 |        37,594 |
    | **NEGany~terribly_different**  |    6.33 |    0.85 |   0.89 | 2,022.47 |   366 | 3,173,660 |    409 |        58,964 |       825,838 |
    | **NEGany~terribly_unusual**    |    6.17 |    0.90 |   0.94 |   847.05 |   146 | 3,173,660 |    155 |        58,964 |        71,234 |
    | **NEGany~terribly_sure**       |    5.08 |    0.86 |   0.91 |   386.31 |    69 | 3,173,660 |     76 |        58,964 |       262,825 |
    | **NEGany~terribly_impressive** |    5.97 |    0.86 |   0.90 | 1,087.64 |   196 | 3,173,660 |    218 |        58,964 |       178,051 |
    
    
    #### Top 10 `mirror` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~terribly_surprising**  |    4.07 |    0.83 |   1.00 | 236.35 |    67 | 291,732 |     67 |         4,610 |         2,662 |
    | **NEGmir~terribly_original**    |    3.40 |    0.83 |   1.00 | 158.74 |    45 | 291,732 |     45 |         4,610 |         1,555 |
    | **NEGmir~terribly_special**     |    2.23 |    0.83 |   1.00 |  84.66 |    24 | 291,732 |     24 |         4,610 |        15,541 |
    | **NEGmir~terribly_unusual**     |    2.23 |    0.83 |   1.00 |  84.66 |    24 | 291,732 |     24 |         4,610 |         2,302 |
    | **NEGmir~terribly_popular**     |    1.75 |    0.83 |   1.00 |  67.02 |    19 | 291,732 |     19 |         4,610 |         5,668 |
    | **NEGmir~terribly_new**         |    3.66 |    0.80 |   0.97 | 225.93 |    69 | 291,732 |     71 |         4,610 |        12,836 |
    | **NEGmir~terribly_interesting** |    2.44 |    0.68 |   0.85 | 145.16 |    56 | 291,732 |     66 |         4,610 |        12,447 |
    | **NEGmir~terribly_interested**  |    2.36 |    0.74 |   0.91 | 112.46 |    39 | 291,732 |     43 |         4,610 |         8,255 |
    | **NEGmir~terribly_clear**       |    1.20 |    0.83 |   1.00 |  52.91 |    15 | 291,732 |     15 |         4,610 |         6,722 |
    | **NEGmir~terribly_remarkable**  |    1.03 |    0.83 |   1.00 |  49.38 |    14 | 291,732 |     14 |         4,610 |         3,238 |
    


## Top 10 "most negative" bigrams corresponding to top 8 adverbs

2024-07-28

### 1. _necessarily_


#### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                       |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~necessarily_useful**         |    6.75 |    0.96 |   1.00 |   651.75 |   104 | 3,173,660 |    104 |        48,947 |       227,709 |
| **NEGany~necessarily_fun**            |    6.62 |    0.96 |   1.00 |   601.61 |    96 | 3,173,660 |     96 |        48,947 |       190,026 |
| **NEGany~necessarily_essential**      |    6.57 |    0.96 |   1.00 |   582.81 |    93 | 3,173,660 |     93 |        48,947 |        69,845 |
| **NEGany~necessarily_reliable**       |    6.35 |    0.96 |   1.00 |   507.61 |    81 | 3,173,660 |     81 |        48,947 |        90,598 |
| **NEGany~necessarily_proud**          |    6.14 |    0.96 |   1.00 |   444.94 |    71 | 3,173,660 |     71 |        48,947 |       207,536 |
| **NEGany~necessarily_indicative**     |    9.43 |    0.95 |   0.99 | 8,577.54 | 1,389 | 3,173,660 |  1,400 |        48,947 |         8,148 |
| **NEGany~necessarily_easy**           |    9.01 |    0.95 |   0.99 | 5,605.64 |   909 | 3,173,660 |    917 |        48,947 |       579,827 |
| **NEGany~necessarily_representative** |    8.34 |    0.95 |   0.99 | 2,996.58 |   487 | 3,173,660 |    492 |        48,947 |        18,355 |
| **NEGany~necessarily_surprising**     |    8.33 |    0.95 |   1.00 | 2,117.16 |   340 | 3,173,660 |    341 |        48,947 |        70,540 |
| **NEGany~necessarily_new**            |    7.94 |    0.94 |   0.98 | 2,923.82 |   482 | 3,173,660 |    492 |        48,947 |       253,862 |


#### Top 7 `mirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~necessarily_right**   |    2.15 |    0.83 |   1.00 |  81.13 |    23 | 291,732 |     23 |         1,107 |         5,576 |
| **NEGmir~necessarily_illegal** |    1.20 |    0.83 |   1.00 |  52.91 |    15 | 291,732 |     15 |         1,107 |           937 |
| **NEGmir~necessarily_wrong**   |    5.04 |    0.81 |   0.98 | 698.74 |   211 | 291,732 |    216 |         1,107 |        20,880 |
| **NEGmir~necessarily_new**     |    1.84 |    0.79 |   0.96 |  73.19 |    23 | 291,732 |     24 |         1,107 |        12,836 |
| **NEGmir~necessarily_bad**     |    2.95 |    0.77 |   0.94 | 154.45 |    50 | 291,732 |     53 |         1,107 |        10,261 |
| **NEGmir~necessarily_true**    |    2.69 |    0.73 |   0.90 | 150.42 |    53 | 291,732 |     59 |         1,107 |         6,191 |
| **NEGmir~necessarily_better**  |    1.63 |    0.70 |   0.87 |  72.90 |    27 | 291,732 |     31 |         1,107 |        14,013 |


### 2. _that_


#### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                             |   `LRC` |   `dP1` |   `P1` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------|--------:|--------:|-------:|----------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~that_far-fetched** |    5.83 |    0.96 |   1.00 |    369.74 |    59 | 3,173,660 |     59 |       208,262 |         5,185 |
| **NEGany~that_thrilled**    |    5.83 |    0.96 |   1.00 |    369.74 |    59 | 3,173,660 |     59 |       208,262 |        24,182 |
| **NEGany~that_uncommon**    |    9.43 |    0.95 |   1.00 |  4,998.32 |   802 | 3,173,660 |    804 |       208,262 |        11,312 |
| **NEGany~that_surprising**  |    9.20 |    0.95 |   0.99 |  6,986.81 | 1,133 | 3,173,660 |  1,143 |       208,262 |        70,540 |
| **NEGany~that_dissimilar**  |    7.86 |    0.95 |   0.99 |  1,871.65 |   304 | 3,173,660 |    307 |       208,262 |         4,605 |
| **NEGany~that_unusual**     |    8.92 |    0.95 |   0.99 |  6,003.05 |   977 | 3,173,660 |    988 |       208,262 |        71,234 |
| **NEGany~that_complicated** |    8.68 |    0.94 |   0.98 |  7,337.84 | 1,207 | 3,173,660 |  1,230 |       208,262 |       159,822 |
| **NEGany~that_hard**        |    8.59 |    0.91 |   0.96 | 58,817.24 | 9,948 | 3,173,660 | 10,380 |       208,262 |       348,463 |
| **NEGany~that_familiar**    |    8.35 |    0.93 |   0.97 |  6,781.11 | 1,126 | 3,173,660 |  1,156 |       208,262 |       156,296 |
| **NEGany~that_noticeable**  |    7.65 |    0.95 |   0.99 |  1,621.81 |   264 | 3,173,660 |    267 |       208,262 |        31,467 |


#### Top 10 `mirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                             |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~that_keen**        |    2.73 |    0.83 |   1.00 |   109.35 |    31 | 291,732 |     31 |         5,494 |         1,360 |
| **NEGmir~that_impressive**  |    2.15 |    0.83 |   1.00 |    81.13 |    23 | 291,732 |     23 |         5,494 |         5,007 |
| **NEGmir~that_fond**        |    1.84 |    0.79 |   0.96 |    73.19 |    23 | 291,732 |     24 |         5,494 |         1,115 |
| **NEGmir~that_comfortable** |    1.84 |    0.79 |   0.96 |    73.19 |    23 | 291,732 |     24 |         5,494 |         4,642 |
| **NEGmir~that_clear**       |    1.30 |    0.78 |   0.95 |    56.03 |    18 | 291,732 |     19 |         5,494 |         6,722 |
| **NEGmir~that_simple**      |    4.36 |    0.72 |   0.90 | 1,340.19 |   474 | 291,732 |    529 |         5,494 |        25,408 |
| **NEGmir~that_easy**        |    4.23 |    0.71 |   0.89 | 1,248.84 |   450 | 291,732 |    508 |         5,494 |        18,610 |
| **NEGmir~that_great**       |    3.57 |    0.66 |   0.84 |   725.16 |   286 | 291,732 |    342 |         5,494 |         5,568 |
| **NEGmir~that_big**         |    3.17 |    0.69 |   0.86 |   300.54 |   113 | 291,732 |    131 |         5,494 |         8,177 |
| **NEGmir~that_popular**     |    3.15 |    0.76 |   0.93 |   195.15 |    65 | 291,732 |     70 |         5,494 |         5,668 |


### 3. _exactly_


#### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                               |   `LRC` |   `dP1` |   `P1` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------|--------:|--------:|-------:|----------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~exactly_conducive**  |    7.82 |    0.96 |   1.00 |  1,303.50 |   208 | 3,173,660 |    208 |        58,643 |         9,110 |
| **NEGany~exactly_shocking**   |    7.33 |    0.96 |   1.00 |    946.29 |   151 | 3,173,660 |    151 |        58,643 |        35,115 |
| **NEGany~exactly_pleasant**   |    7.24 |    0.96 |   1.00 |    889.88 |   142 | 3,173,660 |    142 |        58,643 |        52,223 |
| **NEGany~exactly_famous**     |    7.10 |    0.96 |   1.00 |    814.68 |   130 | 3,173,660 |    130 |        58,643 |       223,813 |
| **NEGany~exactly_difficult**  |    7.05 |    0.96 |   1.00 |    789.62 |   126 | 3,173,660 |    126 |        58,643 |       732,106 |
| **NEGany~exactly_easy**       |    9.32 |    0.95 |   0.99 |  6,596.91 | 1,066 | 3,173,660 |  1,073 |        58,643 |       579,827 |
| **NEGany~exactly_new**        |    9.10 |    0.94 |   0.99 |  8,410.32 | 1,371 | 3,173,660 |  1,388 |        58,643 |       253,862 |
| **NEGany~exactly_cheap**      |    8.96 |    0.95 |   0.99 |  4,281.59 |   691 | 3,173,660 |    695 |        58,643 |        60,531 |
| **NEGany~exactly_clear**      |    8.78 |    0.94 |   0.98 | 10,578.33 | 1,746 | 3,173,660 |  1,784 |        58,643 |       349,214 |
| **NEGany~exactly_surprising** |    8.71 |    0.95 |   1.00 |  2,743.34 |   440 | 3,173,660 |    441 |        58,643 |        70,540 |


#### Top 4 `mirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~exactly_sure**  |    5.31 |    0.83 |   1.00 | 522.11 |   148 | 291,732 |    148 |         1,041 |         6,761 |
| **NEGmir~exactly_easy**  |    1.86 |    0.83 |   1.00 |  70.55 |    20 | 291,732 |     20 |         1,041 |        18,610 |
| **NEGmir~exactly_clear** |    3.38 |    0.81 |   0.98 | 173.89 |    52 | 291,732 |     53 |         1,041 |         6,722 |
| **NEGmir~exactly_new**   |    2.31 |    0.80 |   0.97 |  93.90 |    29 | 291,732 |     30 |         1,041 |        12,836 |


### 4. _any_


#### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                         |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~any_happier**  |    6.34 |    0.82 |   0.86 | 4,420.49 |   828 | 3,173,660 |    963 |        34,382 |        16,606 |
| **NEGany~any_younger**  |    5.57 |    0.79 |   0.83 | 1,323.36 |   255 | 3,173,660 |    307 |        34,382 |        26,216 |
| **NEGany~any_nicer**    |    4.75 |    0.76 |   0.81 |   486.82 |    96 | 3,173,660 |    119 |        34,382 |         9,955 |
| **NEGany~any_simpler**  |    5.00 |    0.71 |   0.75 | 1,087.71 |   226 | 3,173,660 |    300 |        34,382 |        23,480 |
| **NEGany~any_brighter** |    3.91 |    0.67 |   0.72 |   292.00 |    63 | 3,173,660 |     88 |        34,382 |         9,280 |
| **NEGany~any_easier**   |    5.08 |    0.62 |   0.66 | 6,987.78 | 1,594 | 3,173,660 |  2,405 |        34,382 |       209,940 |
| **NEGany~any_cheaper**  |    4.01 |    0.58 |   0.63 |   542.97 |   129 | 3,173,660 |    206 |        34,382 |        46,055 |
| **NEGany~any_smarter**  |    4.00 |    0.63 |   0.67 |   394.95 |    89 | 3,173,660 |    132 |        34,382 |         8,501 |
| **NEGany~any_clearer**  |    4.26 |    0.54 |   0.58 | 1,421.60 |   355 | 3,173,660 |    608 |        34,382 |        11,680 |
| **NEGany~any_worse**    |    3.94 |    0.42 |   0.46 | 5,676.37 | 1,686 | 3,173,660 |  3,673 |        34,382 |       179,012 |


#### Top 10 `mirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~any_younger**   |    1.86 |    0.83 |   1.00 |    70.55 |    20 | 291,732 |     20 |         1,197 |           939 |
| **NEGmir~any_clearer**   |    1.50 |    0.83 |   1.00 |    59.97 |    17 | 291,732 |     17 |         1,197 |           130 |
| **NEGmir~any_different** |    3.24 |    0.81 |   0.98 |   159.93 |    48 | 291,732 |     49 |         1,197 |        36,166 |
| **NEGmir~any_bigger**    |    2.73 |    0.80 |   0.97 |   118.17 |    36 | 291,732 |     37 |         1,197 |         3,923 |
| **NEGmir~any_easier**    |    3.04 |    0.75 |   0.92 |   181.65 |    61 | 291,732 |     66 |         1,197 |         2,386 |
| **NEGmir~any_better**    |    4.38 |    0.74 |   0.91 | 1,096.01 |   380 | 291,732 |    419 |         1,197 |        14,013 |
| **NEGmir~any_worse**     |    2.73 |    0.66 |   0.83 |   217.46 |    87 | 291,732 |    105 |         1,197 |         8,790 |
| **NEGmir~any_higher**    |    1.42 |    0.74 |   0.91 |    61.24 |    21 | 291,732 |     23 |         1,197 |         2,893 |
| **NEGmir~any_closer**    |    2.33 |    0.65 |   0.83 |   141.82 |    57 | 291,732 |     69 |         1,197 |           993 |
| **NEGmir~any_good**      |    2.12 |    0.74 |   0.91 |    93.53 |    32 | 291,732 |     35 |         1,197 |        31,585 |


### 5. _remotely_


#### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~remotely_surprising** |    5.07 |    0.85 |   0.89 |   413.61 |    75 | 3,173,660 |     84 |        16,426 |        70,540 |
| **NEGany~remotely_ready**      |    4.16 |    0.74 |   0.78 |   287.63 |    58 | 3,173,660 |     74 |        16,426 |       141,590 |
| **NEGany~remotely_true**       |    4.61 |    0.63 |   0.68 | 1,111.13 |   250 | 3,173,660 |    370 |        16,426 |       231,639 |
| **NEGany~remotely_funny**      |    4.15 |    0.60 |   0.65 |   589.74 |   137 | 3,173,660 |    212 |        16,426 |       122,927 |
| **NEGany~remotely_qualified**  |    3.13 |    0.52 |   0.56 |   222.79 |    57 | 3,173,660 |    101 |        16,426 |        74,643 |
| **NEGany~remotely_close**      |    3.65 |    0.39 |   0.43 | 2,243.22 |   694 | 3,173,660 |  1,597 |        16,426 |       411,329 |
| **NEGany~remotely_comparable** |    2.98 |    0.38 |   0.43 |   375.73 |   118 | 3,173,660 |    277 |        16,426 |        12,252 |
| **NEGany~remotely_accurate**   |    2.10 |    0.33 |   0.37 |   143.78 |    50 | 3,173,660 |    134 |        16,426 |       152,299 |
| **NEGany~remotely_interested** |    2.74 |    0.27 |   0.31 |   817.06 |   330 | 3,173,660 |  1,062 |        16,426 |       264,528 |
| **NEGany~remotely_similar**    |    2.20 |    0.23 |   0.27 |   334.61 |   152 | 3,173,660 |    559 |        16,426 |       203,453 |


#### Top 10 `mirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                 |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~remotely_believable**  |    1.96 |    0.83 |   1.00 |  74.08 |    21 | 291,732 |     21 |         2,341 |           600 |
| **NEGmir~remotely_surprising**  |    1.50 |    0.83 |   1.00 |  59.97 |    17 | 291,732 |     17 |         2,341 |         2,662 |
| **NEGmir~remotely_comparable**  |    2.72 |    0.76 |   0.94 | 134.02 |    44 | 291,732 |     47 |         2,341 |           283 |
| **NEGmir~remotely_true**        |    3.04 |    0.75 |   0.92 | 181.65 |    61 | 291,732 |     66 |         2,341 |         6,191 |
| **NEGmir~remotely_new**         |    1.00 |    0.69 |   0.86 |  50.62 |    19 | 291,732 |     22 |         2,341 |        12,836 |
| **NEGmir~remotely_close**       |    3.28 |    0.65 |   0.82 | 532.96 |   218 | 291,732 |    267 |         2,341 |        13,874 |
| **NEGmir~remotely_funny**       |    1.85 |    0.63 |   0.80 |  97.91 |    41 | 291,732 |     51 |         2,341 |         5,365 |
| **NEGmir~remotely_similar**     |    1.70 |    0.49 |   0.66 | 127.32 |    71 | 291,732 |    107 |         2,341 |         7,011 |
| **NEGmir~remotely_possible**    |    1.42 |    0.56 |   0.73 |  78.73 |    38 | 291,732 |     52 |         2,341 |         3,160 |
| **NEGmir~remotely_interesting** |    1.80 |    0.56 |   0.73 | 115.20 |    56 | 291,732 |     77 |         2,341 |        12,447 |


### 6. _ever_


#### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                           |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |       `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------|--------:|--------:|-------:|---------:|------:|-----------:|-------:|--------------:|--------------:|
| **NEGany~ever_simple**    |    5.56 |    0.80 |   0.84 | 1,109.28 |   211 |  3,173,660 |    250 |       114,075 |       396,749 |
| **NEGany~ever_boring**    |    4.46 |    0.76 |   0.80 |   362.74 |    72 |  3,173,660 |     90 |       114,075 |        45,891 |
| **NEGany~ever_easy**      |    5.41 |    0.73 |   0.77 | 2,105.13 |   429 |  3,173,660 |    555 |       114,075 |       579,827 |
| **NEGany~ever_certain**   |    4.80 |    0.72 |   0.76 |   713.34 |   147 |  3,173,660 |    193 |       114,075 |        74,952 |
| **NEGany~ever_sure**      |    3.34 |    0.49 |   0.54 |   328.20 |    87 |  3,173,660 |    162 |       114,075 |       262,825 |
| **NEGany~ever_good**      |    3.81 |    0.46 |   0.50 | 1,188.69 |   331 |  3,173,660 |    660 |       114,075 |     1,681,795 |
| **COM~ever_closer**       |    3.51 |    0.04 |   1.00 |   538.66 | 6,305 | 69,662,736 |  6,307 |       114,075 |        61,475 |
| **NEGany~ever_enough**    |    3.54 |    0.45 |   0.50 |   618.62 |   173 |  3,173,660 |    347 |       114,075 |       152,020 |
| **NEGany~ever_perfect**   |    3.34 |    0.40 |   0.44 |   706.71 |   216 |  3,173,660 |    489 |       114,075 |       104,659 |
| **NEGany~ever_satisfied** |    2.57 |    0.38 |   0.42 |   203.01 |    64 |  3,173,660 |    151 |       114,075 |        62,862 |


#### Top 10 `mirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                         |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~ever_simple**  |    5.82 |    0.83 |   1.00 |   726.76 |   206 | 291,732 |    206 |         5,060 |        25,408 |
| **NEGmir~ever_enough**  |    5.30 |    0.83 |   1.00 |   518.58 |   147 | 291,732 |    147 |         5,060 |         2,596 |
| **NEGmir~ever_certain** |    5.26 |    0.83 |   1.00 |   504.47 |   143 | 291,732 |    143 |         5,060 |         1,800 |
| **NEGmir~ever_boring**  |    3.80 |    0.83 |   1.00 |   201.07 |    57 | 291,732 |     57 |         5,060 |         1,961 |
| **NEGmir~ever_black**   |    3.77 |    0.83 |   1.00 |   197.54 |    56 | 291,732 |     56 |         5,060 |         1,412 |
| **NEGmir~ever_easy**    |    6.44 |    0.83 |   1.00 | 1,285.01 |   368 | 291,732 |    369 |         5,060 |        18,610 |
| **NEGmir~ever_good**    |    5.68 |    0.82 |   0.99 | 1,013.87 |   299 | 291,732 |    303 |         5,060 |        31,585 |
| **NEGmir~ever_perfect** |    5.57 |    0.82 |   1.00 |   714.47 |   206 | 291,732 |    207 |         5,060 |         3,134 |
| **NEGmir~ever_sick**    |    3.15 |    0.83 |   1.00 |   137.57 |    39 | 291,732 |     39 |         5,060 |         1,895 |
| **NEGmir~ever_able**    |    4.17 |    0.78 |   0.95 |   426.52 |   136 | 291,732 |    143 |         5,060 |         3,704 |


### 7. _yet_


#### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                           |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~yet_eligible**   |    8.96 |    0.96 |   1.00 |  2,807.56 |    448 | 3,173,660 |    448 |        95,763 |        23,252 |
| **NEGany~yet_official**   |    8.61 |    0.96 |   1.00 |  2,205.93 |    352 | 3,173,660 |    352 |        95,763 |         6,853 |
| **NEGany~yet_convinced**  |    7.50 |    0.96 |   1.00 |  1,059.09 |    169 | 3,173,660 |    169 |        95,763 |        12,132 |
| **NEGany~yet_online**     |    6.66 |    0.96 |   1.00 |    614.14 |     98 | 3,173,660 |     98 |        95,763 |        15,650 |
| **NEGany~yet_mainstream** |    6.11 |    0.96 |   1.00 |    438.67 |     70 | 3,173,660 |     70 |        95,763 |        17,792 |
| **NEGany~yet_clear**      |   10.77 |    0.95 |   0.99 | 64,409.97 | 10,406 | 3,173,660 | 10,476 |        95,763 |       349,214 |
| **NEGany~yet_ready**      |    9.93 |    0.94 |   0.99 | 45,985.07 |  7,501 | 3,173,660 |  7,599 |        95,763 |       141,590 |
| **NEGany~yet_complete**   |    9.20 |    0.94 |   0.98 | 13,277.09 |  2,174 | 3,173,660 |  2,208 |        95,763 |        86,361 |
| **NEGany~yet_final**      |    8.97 |    0.95 |   1.00 |  3,972.92 |    640 | 3,173,660 |    643 |        95,763 |         5,860 |
| **NEGany~yet_over**       |    7.21 |    0.95 |   0.99 |  1,003.13 |    162 | 3,173,660 |    163 |        95,763 |         3,983 |


#### Top 5 `mirror` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~yet_available** |    2.54 |    0.83 |   1.00 |  98.77 |    28 | 291,732 |     28 |           815 |        10,284 |
| **NEGmir~yet_certain**   |    1.96 |    0.83 |   1.00 |  74.08 |    21 | 291,732 |     21 |           815 |         1,800 |
| **NEGmir~yet_sure**      |    1.75 |    0.83 |   1.00 |  67.02 |    19 | 291,732 |     19 |           815 |         6,761 |
| **NEGmir~yet_clear**     |    1.75 |    0.83 |   1.00 |  67.02 |    19 | 291,732 |     19 |           815 |         6,722 |
| **NEGmir~yet_ready**     |    1.63 |    0.83 |   1.00 |  63.49 |    18 | 291,732 |     18 |           815 |         3,034 |


### 8. _immediately_


#### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                    |   `LRC` |   `dP1` |   `P1` |       `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------------------|--------:|--------:|-------:|-----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~immediately_possible**    |    7.62 |    0.91 |   0.95 |   5,845.77 |  1,000 | 3,173,660 |  1,054 |        96,973 |       245,272 |
| **NEGany~immediately_clear**       |    8.16 |    0.89 |   0.94 | 141,186.69 | 24,416 | 3,173,660 | 26,038 |        96,973 |       349,214 |
| **NEGany~immediately_reachable**   |    5.56 |    0.86 |   0.91 |     610.53 |    109 | 3,173,660 |    120 |        96,973 |         2,672 |
| **NEGany~immediately_sure**        |    5.40 |    0.82 |   0.86 |     738.65 |    138 | 3,173,660 |    160 |        96,973 |       262,825 |
| **NEGany~immediately_certain**     |    4.19 |    0.71 |   0.75 |     336.68 |     70 | 3,173,660 |     93 |        96,973 |        74,952 |
| **NEGany~immediately_available**   |    5.70 |    0.67 |   0.72 |  98,046.67 | 21,078 | 3,173,660 | 29,351 |        96,973 |       666,909 |
| **NEGany~immediately_able**        |    4.70 |    0.59 |   0.63 |   2,655.18 |    626 | 3,173,660 |    989 |        96,973 |       223,196 |
| **NEGany~immediately_obvious**     |    4.55 |    0.52 |   0.56 |   8,712.07 |  2,238 | 3,173,660 |  3,989 |        96,973 |       165,439 |
| **NEGany~immediately_forthcoming** |    3.89 |    0.55 |   0.60 |     540.70 |    133 | 3,173,660 |    223 |        96,973 |         7,473 |
| **NEGany~immediately_intuitive**   |    3.21 |    0.55 |   0.59 |     218.74 |     54 | 3,173,660 |     91 |        96,973 |        20,664 |


#### Top 2 `mirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                  |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~immediately_clear**     |    1.13 |    0.55 |   0.72 |  62.95 |    31 | 291,732 |     43 |         1,195 |         6,722 |
| **NEGmir~immediately_available** |    1.85 |    0.42 |   0.59 | 241.53 |   162 | 291,732 |    275 |         1,195 |        10,284 |


### 9. _particularly_


#### Top 10 `RBdirect` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                       |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~particularly_likable**       |    5.53 |    0.85 |   0.89 |   657.49 |   119 | 3,173,660 |    133 |       513,668 |         8,160 |
| **NEGany~particularly_likeable**      |    5.34 |    0.84 |   0.88 |   579.07 |   106 | 3,173,660 |    120 |       513,668 |         5,902 |
| **NEGany~particularly_forthcoming**   |    4.85 |    0.82 |   0.87 |   387.25 |    72 | 3,173,660 |     83 |       513,668 |         7,473 |
| **NEGany~particularly_religious**     |    6.12 |    0.81 |   0.86 | 2,585.71 |   485 | 3,173,660 |    565 |       513,668 |        28,028 |
| **NEGany~particularly_original**      |    5.86 |    0.80 |   0.85 | 1,894.60 |   360 | 3,173,660 |    426 |       513,668 |        37,594 |
| **NEGany~particularly_new**           |    6.04 |    0.79 |   0.83 | 3,874.46 |   747 | 3,173,660 |    900 |       513,668 |       253,862 |
| **NEGany~particularly_athletic**      |    4.77 |    0.75 |   0.79 |   541.01 |   108 | 3,173,660 |    136 |       513,668 |        17,142 |
| **NEGany~particularly_revolutionary** |    4.49 |    0.75 |   0.79 |   385.60 |    77 | 3,173,660 |     97 |       513,668 |        10,338 |
| **NEGany~particularly_flashy**        |    4.08 |    0.73 |   0.77 |   278.96 |    57 | 3,173,660 |     74 |       513,668 |         4,494 |
| **NEGany~particularly_surprising**    |    4.71 |    0.57 |   0.61 | 4,433.52 | 1,069 | 3,173,660 |  1,743 |       513,668 |        70,540 |


#### Top 10 `mirror` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                       |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~particularly_novel**         |    3.71 |    0.83 |   1.00 |   190.49 |    54 | 291,732 |     54 |        13,003 |           320 |
| **NEGmir~particularly_comfortable**   |    3.36 |    0.83 |   1.00 |   155.21 |    44 | 291,732 |     44 |        13,003 |         4,642 |
| **NEGmir~particularly_revolutionary** |    3.15 |    0.83 |   1.00 |   137.57 |    39 | 291,732 |     39 |        13,003 |           485 |
| **NEGmir~particularly_radical**       |    2.73 |    0.83 |   1.00 |   109.35 |    31 | 291,732 |     31 |        13,003 |         1,072 |
| **NEGmir~particularly_fast**          |    2.39 |    0.83 |   1.00 |    91.71 |    26 | 291,732 |     26 |        13,003 |         1,259 |
| **NEGmir~particularly_new**           |    5.92 |    0.81 |   0.99 | 1,365.17 |   404 | 291,732 |    410 |        13,003 |        12,836 |
| **NEGmir~particularly_surprising**    |    5.06 |    0.82 |   0.99 |   564.67 |   166 | 291,732 |    168 |        13,003 |         2,662 |
| **NEGmir~particularly_wrong**         |    5.05 |    0.81 |   0.98 |   702.22 |   212 | 291,732 |    217 |        13,003 |        20,880 |
| **NEGmir~particularly_remarkable**    |    4.24 |    0.80 |   0.97 |   354.53 |   108 | 291,732 |    111 |        13,003 |         3,238 |
| **NEGmir~particularly_close**         |    4.01 |    0.77 |   0.94 |   415.70 |   136 | 291,732 |    145 |        13,003 |        13,874 |


### 10. _inherently_

All bigrams for inherently retrieved.

#### Top 7 `RBdirect` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                   |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~inherently_wrong**       |    5.36 |    0.66 |   0.71 | 7,535.97 | 1,639 | 3,173,660 |  2,315 |        47,803 |       149,064 |
| **NEGany~inherently_illegal**     |    3.51 |    0.60 |   0.64 |   252.59 |    59 | 3,173,660 |     92 |        47,803 |        30,194 |
| **NEGany~inherently_bad**         |    4.62 |    0.56 |   0.61 | 3,270.68 |   794 | 3,173,660 |  1,307 |        47,803 |       429,537 |
| **NEGany~inherently_negative**    |    2.50 |    0.35 |   0.39 |   222.63 |    75 | 3,173,660 |    193 |        47,803 |        53,385 |
| **NEGany~inherently_evil**        |    2.81 |    0.28 |   0.32 |   905.80 |   358 | 3,173,660 |  1,123 |        47,803 |        22,706 |
| **NEGany~inherently_good**        |    2.21 |    0.20 |   0.24 |   554.72 |   283 | 3,173,660 |  1,177 |        47,803 |     1,681,795 |
| **NEGany~inherently_problematic** |    1.17 |    0.17 |   0.21 |    98.70 |    58 | 3,173,660 |    277 |        47,803 |        33,408 |

All bigrams for inherently retrieved.

#### Top 6 `mirror` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~inherently_improper** |    1.63 |    0.83 |   1.00 |    63.49 |    18 | 291,732 |     18 |         5,133 |           142 |
| **NEGmir~inherently_illegal**  |    2.10 |    0.79 |   0.96 |    83.54 |    26 | 291,732 |     27 |         5,133 |           937 |
| **NEGmir~inherently_wrong**    |    4.08 |    0.66 |   0.83 | 3,787.53 | 1,513 | 291,732 |  1,826 |         5,133 |        20,880 |
| **NEGmir~inherently_bad**      |    2.86 |    0.62 |   0.79 |   342.53 |   148 | 291,732 |    188 |         5,133 |        10,261 |
| **NEGmir~inherently_better**   |    1.65 |    0.57 |   0.75 |    93.95 |    44 | 291,732 |     59 |         5,133 |        14,013 |
| **NEGmir~inherently_evil**     |    1.18 |    0.41 |   0.59 |    85.70 |    58 | 291,732 |     99 |         5,133 |         1,271 |


### 11. _terribly_


#### Top 10 `RBdirect` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~terribly_surprising** |    8.66 |    0.94 |   0.98 | 5,794.10 |   949 | 3,173,660 |    964 |        58,964 |        70,540 |
| **NEGany~terribly_uncommon**   |    6.33 |    0.94 |   0.98 |   625.85 |   103 | 3,173,660 |    105 |        58,964 |        11,312 |
| **NEGany~terribly_likely**     |    6.26 |    0.93 |   0.97 |   649.50 |   108 | 3,173,660 |    111 |        58,964 |       890,421 |
| **NEGany~terribly_productive** |    5.39 |    0.91 |   0.96 |   376.84 |    64 | 3,173,660 |     67 |        58,964 |       102,361 |
| **NEGany~terribly_reliable**   |    4.99 |    0.90 |   0.94 |   296.70 |    51 | 3,173,660 |     54 |        58,964 |        90,598 |
| **NEGany~terribly_original**   |    6.41 |    0.90 |   0.94 | 1,150.48 |   199 | 3,173,660 |    212 |        58,964 |        37,594 |
| **NEGany~terribly_different**  |    6.33 |    0.85 |   0.89 | 2,022.47 |   366 | 3,173,660 |    409 |        58,964 |       825,838 |
| **NEGany~terribly_unusual**    |    6.17 |    0.90 |   0.94 |   847.05 |   146 | 3,173,660 |    155 |        58,964 |        71,234 |
| **NEGany~terribly_sure**       |    5.08 |    0.86 |   0.91 |   386.31 |    69 | 3,173,660 |     76 |        58,964 |       262,825 |
| **NEGany~terribly_impressive** |    5.97 |    0.86 |   0.90 | 1,087.64 |   196 | 3,173,660 |    218 |        58,964 |       178,051 |


#### Top 10 `mirror` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                 |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~terribly_surprising**  |    4.07 |    0.83 |   1.00 | 236.35 |    67 | 291,732 |     67 |         4,610 |         2,662 |
| **NEGmir~terribly_original**    |    3.40 |    0.83 |   1.00 | 158.74 |    45 | 291,732 |     45 |         4,610 |         1,555 |
| **NEGmir~terribly_special**     |    2.23 |    0.83 |   1.00 |  84.66 |    24 | 291,732 |     24 |         4,610 |        15,541 |
| **NEGmir~terribly_unusual**     |    2.23 |    0.83 |   1.00 |  84.66 |    24 | 291,732 |     24 |         4,610 |         2,302 |
| **NEGmir~terribly_popular**     |    1.75 |    0.83 |   1.00 |  67.02 |    19 | 291,732 |     19 |         4,610 |         5,668 |
| **NEGmir~terribly_new**         |    3.66 |    0.80 |   0.97 | 225.93 |    69 | 291,732 |     71 |         4,610 |        12,836 |
| **NEGmir~terribly_interesting** |    2.44 |    0.68 |   0.85 | 145.16 |    56 | 291,732 |     66 |         4,610 |        12,447 |
| **NEGmir~terribly_interested**  |    2.36 |    0.74 |   0.91 | 112.46 |    39 | 291,732 |     43 |         4,610 |         8,255 |
| **NEGmir~terribly_clear**       |    1.20 |    0.83 |   1.00 |  52.91 |    15 | 291,732 |     15 |         4,610 |         6,722 |
| **NEGmir~terribly_remarkable**  |    1.03 |    0.83 |   1.00 |  49.38 |    14 | 291,732 |     14 |         4,610 |         3,238 |



 ### `2024-05-23` Top 10 "most negative" bigrams corresponding to top 5 adverbs



#### 1. _necessarily_


Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                                       | `adj`          |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
 |:--------------------------------------|:---------------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
 | **NEGany~necessarily_sure**           | sure           |    844,981.00 |    5.91 |    0.95 |  1,436.68 |   222 | 3,226,213 |    224 |
 | **NEGany~necessarily_surprising**     | surprising     |    150,067.00 |    7.22 |    0.93 |  2,150.86 |   343 | 3,226,213 |    355 |
 | **NEGany~necessarily_indicative**     | indicative     |     12,760.00 |    8.37 |    0.93 |  8,811.69 | 1,406 | 3,226,213 |  1,456 |
 | **NEGany~necessarily_representative** | representative |     25,187.00 |    7.31 |    0.91 |  3,044.27 |   496 | 3,226,213 |    524 |
 | **NEGany~necessarily_available**      | available      |    866,272.00 |    6.36 |    0.89 |  1,280.24 |   213 | 3,226,213 |    230 |
 | **NEGany~necessarily_easy**           | easy           |    771,307.00 |    7.26 |    0.88 |  5,448.34 |   914 | 3,226,213 |    996 |
 | **NEGany~necessarily_true**           | true           |    348,994.00 |    6.89 |    0.82 | 18,199.76 | 3,238 | 3,226,213 |  3,786 |
 | **NEGany~necessarily_illegal**        | illegal        |     44,028.00 |    6.48 |    0.87 |  1,659.90 |   280 | 3,226,213 |    307 |
 | **NEGany~necessarily_related**        | related        |    137,661.00 |    6.74 |    0.84 |  4,271.76 |   742 | 3,226,213 |    842 |
 | **NEGany~necessarily_interested**     | interested     |    364,497.00 |    6.77 |    0.87 |  2,500.26 |   422 | 3,226,213 |    463 |


Top 3 `NEGmirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                              | `adj`   |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
 |:-----------------------------|:--------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
 | **NEGmir~necessarily_wrong** | wrong   |     20,866.00 |    4.27 |    0.81 | 708.98 |   209 | 289,770 |    214 |
 | **NEGmir~necessarily_bad**   | bad     |     10,783.00 |    2.02 |    0.76 | 153.43 |    50 | 289,770 |     54 |
 | **NEGmir~necessarily_true**  | true    |      7,402.00 |    2.18 |    0.75 | 159.07 |    53 | 289,770 |     58 |


#### 2. _exactly_


Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                               | `adj`      |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
 |:------------------------------|:-----------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
 | **NEGany~exactly_surprising** | surprising |    150,067.00 |    7.34 |    0.96 |  2,863.35 |   441 | 3,226,213 |    444 |
 | **NEGany~exactly_cheap**      | cheap      |     83,765.00 |    8.28 |    0.95 |  4,443.27 |   693 | 3,226,213 |    704 |
 | **NEGany~exactly_subtle**     | subtle     |     56,845.00 |    6.92 |    0.94 |  1,671.02 |   264 | 3,226,213 |    271 |
 | **NEGany~exactly_fun**        | fun        |    224,457.00 |    6.67 |    0.94 |  1,423.92 |   225 | 3,226,213 |    231 |
 | **NEGany~exactly_conducive**  | conducive  |     16,405.00 |    6.56 |    0.93 |  1,313.09 |   208 | 3,226,213 |    214 |
 | **NEGany~exactly_sure**       | sure       |    844,981.00 |    8.63 |    0.92 | 54,750.58 | 8,860 | 3,226,213 |  9,301 |
 | **NEGany~exactly_new**        | new        |    321,311.00 |    8.54 |    0.93 |  8,697.93 | 1,378 | 3,226,213 |  1,418 |
 | **NEGany~exactly_easy**       | easy       |    771,307.00 |    8.37 |    0.93 |  6,747.64 | 1,069 | 3,226,213 |  1,100 |
 | **NEGany~exactly_clear**      | clear      |    491,108.00 |    8.30 |    0.92 | 10,937.16 | 1,759 | 3,226,213 |  1,835 |
 | **NEGany~exactly_happy**      | happy      |    528,511.00 |    7.16 |    0.90 |  2,694.69 |   441 | 3,226,213 |    468 |

 No bigrams found in loaded `NEGmirror` AM table.

#### 3. _that_


Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                             | `adj`       |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
 |:----------------------------|:------------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
 | **NEGany~that_uncommon**    | uncommon    |     61,767.00 |    8.39 |    0.94 |  5,136.91 |   804 | 3,226,213 |    819 |
 | **NEGany~that_fond**        | fond        |     39,809.00 |    7.27 |    0.94 |  2,127.94 |   334 | 3,226,213 |    341 |
 | **NEGany~that_surprising**  | surprising  |    150,067.00 |    8.14 |    0.92 |  7,115.30 | 1,141 | 3,226,213 |  1,187 |
 | **NEGany~that_common**      | common      |    556,435.00 |    8.12 |    0.92 |  7,564.08 | 1,216 | 3,226,213 |  1,268 |
 | **NEGany~that_dissimilar**  | dissimilar  |      8,816.00 |    7.00 |    0.92 |  1,904.15 |   307 | 3,226,213 |    321 |
 | **NEGany~that_hard**        | hard        |    430,990.00 |    7.96 |    0.88 | 59,642.82 | 9,966 | 3,226,213 | 10,818 |
 | **NEGany~that_complicated** | complicated |    180,071.00 |    7.95 |    0.91 |  7,450.89 | 1,208 | 3,226,213 |  1,270 |
 | **NEGany~that_impressed**   | impressed   |    113,281.00 |    7.57 |    0.91 |  4,207.58 |   684 | 3,226,213 |    721 |
 | **NEGany~that_noticeable**  | noticeable  |     40,372.00 |    6.78 |    0.91 |  1,632.07 |   265 | 3,226,213 |    279 |
 | **NEGany~that_exciting**    | exciting    |    236,396.00 |    7.48 |    0.90 |  4,892.83 |   805 | 3,226,213 |    859 |


Top 10 `NEGmirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                            | `adj`      |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
 |:---------------------------|:-----------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
 | **NEGmir~that_popular**    | popular    |      5,787.00 |    2.50 |    0.76 |   200.44 |    65 | 289,770 |     70 |
 | **NEGmir~that_interested** | interested |      9,258.00 |    2.42 |    0.76 |   190.06 |    62 | 289,770 |     67 |
 | **NEGmir~that_difficult**  | difficult  |     16,043.00 |    2.15 |    0.75 |   155.64 |    52 | 289,770 |     57 |
 | **NEGmir~that_hard**       | hard       |      7,311.00 |    2.31 |    0.74 |   168.31 |    57 | 289,770 |     63 |
 | **NEGmir~that_close**      | close      |     13,962.00 |    2.39 |    0.73 |   174.26 |    60 | 289,770 |     67 |
 | **NEGmir~that_simple**     | simple     |     25,382.00 |    4.34 |    0.73 | 1,370.94 |   473 | 289,770 |    529 |
 | **NEGmir~that_easy**       | easy       |     20,050.00 |    4.21 |    0.72 | 1,258.15 |   442 | 289,770 |    500 |
 | **NEGmir~that_great**      | great      |      5,819.00 |    3.52 |    0.67 |   728.46 |   282 | 289,770 |    340 |
 | **NEGmir~that_good**       | good       |     33,540.00 |    3.07 |    0.56 |   953.31 |   447 | 289,770 |    615 |
 | **NEGmir~that_big**        | big        |      7,859.00 |    3.06 |    0.70 |   309.58 |   113 | 289,770 |    131 |


#### 4. _before_

 No bigrams found in loaded `RBdirect` AM table.
 No bigrams found in loaded `NEGmirror` AM table.

#### 5. _any_


Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
 |:-------------------------|:----------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
 | **NEGany~any_happier**   | happier   |     19,501.00 |    4.65 |    0.53 | 3,488.76 |   830 | 3,226,213 |  1,472 |
 | **NEGany~any_simpler**   | simpler   |     26,094.00 |    3.09 |    0.30 |   671.74 |   228 | 3,226,213 |    672 |
 | **NEGany~any_clearer**   | clearer   |     13,369.00 |    3.21 |    0.30 | 1,051.22 |   357 | 3,226,213 |  1,053 |
 | **NEGany~any_different** | different |    909,864.00 |    2.98 |    0.24 | 2,270.24 |   910 | 3,226,213 |  3,313 |
 | **NEGany~any_younger**   | younger   |     29,805.00 |    2.37 |    0.19 |   544.17 |   256 | 3,226,213 |  1,121 |
 | **NEGany~any_worse**     | worse     |    214,166.00 |    2.47 |    0.16 | 3,165.88 | 1,693 | 3,226,213 |  8,487 |
 | **NEGany~any_bigger**    | bigger    |    130,470.00 |    2.27 |    0.17 |   688.06 |   357 | 3,226,213 |  1,735 |
 | **NEGany~any_harder**    | harder    |     99,332.00 |    1.98 |    0.15 |   395.22 |   227 | 3,226,213 |  1,221 |
 | **NEGany~any_safer**     | safer     |     26,779.00 |    1.73 |    0.12 |   346.68 |   235 | 3,226,213 |  1,471 |
 | **NEGany~any_easier**    | easier    |    237,680.00 |    1.95 |    0.11 | 2,164.75 | 1,607 | 3,226,213 | 10,860 |


Top 4 `NEGmirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                       | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
 |:----------------------|:--------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
 | **NEGmir~any_better** | better  |     14,076.00 |    4.44 |    0.75 | 1,148.18 |   381 | 289,770 |    416 |
 | **NEGmir~any_easier** | easier  |      2,409.00 |    2.42 |    0.75 |   181.98 |    61 | 289,770 |     67 |
 | **NEGmir~any_worse**  | worse   |      8,490.00 |    2.87 |    0.72 |   248.63 |    88 | 289,770 |    100 |
 | **NEGmir~any_closer** | closer  |        986.00 |    2.21 |    0.68 |   149.62 |    56 | 289,770 |     66 |


#### 6. _ever_


Top 5 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                         | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
 |:------------------------|:--------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
 | **NEGany~ever_simple**  | simple  |    427,167.00 |    5.54 |    0.77 | 1,142.04 |   212 | 3,226,213 |    262 |
 | **NEGany~ever_easy**    | easy    |    771,307.00 |    5.06 |    0.63 | 2,030.58 |   430 | 3,226,213 |    641 |
 | **NEGany~ever_good**    | good    |  2,037,285.00 |    3.76 |    0.40 | 1,178.00 |   332 | 3,226,213 |    756 |
 | **NEGany~ever_perfect** | perfect |    164,519.00 |    3.48 |    0.37 |   736.05 |   217 | 3,226,213 |    527 |
 | **NEGany~ever_able**    | able    |    428,268.00 |    1.81 |    0.13 |   363.95 |   234 | 3,226,213 |  1,398 |


Top 6 `NEGmirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                         | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
 |:------------------------|:--------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
 | **NEGmir~ever_easy**    | easy    |     20,050.00 |    3.21 |    0.83 | 1,311.83 |   367 | 289,770 |    368 |
 | **NEGmir~ever_perfect** | perfect |      3,708.00 |    2.38 |    0.83 |   735.10 |   207 | 289,770 |    208 |
 | **NEGmir~ever_good**    | good    |     33,540.00 |    4.72 |    0.82 | 1,034.95 |   298 | 289,770 |    302 |
 | **NEGmir~ever_wrong**   | wrong   |     20,866.00 |    2.56 |    0.82 |   349.21 |   102 | 289,770 |    104 |
 | **NEGmir~ever_free**    | free    |      5,043.00 |    1.97 |    0.81 |   231.61 |    69 | 289,770 |     71 |
 | **NEGmir~ever_able**    | able    |      6,448.00 |    3.66 |    0.79 |   437.65 |   136 | 289,770 |    143 |


#### 7. _yet_


Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |      `G2` |    `f` |      `f1` |   `f2` |
 |:-------------------------|:----------|--------------:|--------:|--------:|----------:|-------:|----------:|-------:|
 | **NEGany~yet_clear**     | clear     |    491,108.00 |   10.26 |    0.95 | 67,924.56 | 10,553 | 3,226,213 | 10,693 |
 | **NEGany~yet_eligible**  | eligible  |     49,578.00 |    7.72 |    0.94 |  2,929.15 |    459 | 3,226,213 |    468 |
 | **NEGany~yet_official**  | official  |      9,778.00 |    7.33 |    0.94 |  2,236.98 |    353 | 3,226,213 |    362 |
 | **NEGany~yet_ready**     | ready     |    240,297.00 |    9.23 |    0.93 | 48,012.06 |  7,611 | 3,226,213 |  7,838 |
 | **NEGany~yet_certain**   | certain   |    104,544.00 |    8.12 |    0.93 |  5,491.41 |    874 | 3,226,213 |    903 |
 | **NEGany~yet_complete**  | complete  |    107,018.00 |    8.42 |    0.92 | 13,815.99 |  2,220 | 3,226,213 |  2,314 |
 | **NEGany~yet_sure**      | sure      |    844,981.00 |    8.37 |    0.92 | 12,379.79 |  1,990 | 3,226,213 |  2,075 |
 | **NEGany~yet_available** | available |    866,272.00 |    7.69 |    0.87 | 44,196.15 |  7,481 | 3,226,213 |  8,238 |
 | **NEGany~yet_right**     | right     |    204,572.00 |    6.50 |    0.92 |  1,254.20 |    202 | 3,226,213 |    211 |
 | **NEGany~yet_final**     | final     |      9,657.00 |    7.45 |    0.91 |  4,028.75 |    659 | 3,226,213 |    699 |

 No bigrams found in loaded `NEGmirror` AM table.

#### 8. _longer_


Top 5 `RBdirect` "longer_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |    `f` |       `f1` |   `f2` |
 |:-------------------------|:----------|--------------:|--------:|--------:|-------:|-------:|-----------:|-------:|
 | **COM~longer_lasting**   | lasting   |     24,344.00 |    1.44 |    0.04 | 244.09 |  3,860 | 83,102,035 |  3,866 |
 | **COM~longer_enough**    | enough    |    453,790.00 |    1.41 |    0.03 | 216.98 |  3,952 | 83,102,035 |  3,964 |
 | **COM~longer_able**      | able      |    428,268.00 |    2.28 |    0.03 | 623.67 | 11,677 | 83,102,035 | 11,716 |
 | **COM~longer_available** | available |    866,272.00 |    2.45 |    0.03 | 974.55 | 18,865 | 83,102,035 | 18,935 |
 | **COM~longer_necessary** | necessary |    187,396.00 |    1.27 |    0.03 | 220.07 |  5,365 | 83,102,035 |  5,399 |

 No bigrams found in loaded `NEGmirror` AM table.

#### 9. _immediately_


Top 5 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                                  | `adj`     |   `adj_total` |   `LRC` |   `dP1` |       `G2` |    `f` |      `f1` |   `f2` |
 |:---------------------------------|:----------|--------------:|--------:|--------:|-----------:|-------:|----------:|-------:|
 | **NEGany~immediately_possible**  | possible  |    364,265.00 |    7.68 |    0.90 |   6,269.26 |  1,027 | 3,226,213 |  1,091 |
 | **NEGany~immediately_clear**     | clear     |    491,108.00 |    8.32 |    0.90 | 153,302.22 | 25,276 | 3,226,213 | 27,066 |
 | **NEGany~immediately_available** | available |    866,272.00 |    5.77 |    0.66 | 102,962.94 | 21,297 | 3,226,213 | 30,725 |
 | **NEGany~immediately_able**      | able      |    428,268.00 |    4.87 |    0.58 |   2,851.84 |    639 | 3,226,213 |  1,036 |
 | **NEGany~immediately_obvious**   | obvious   |    193,498.00 |    4.59 |    0.49 |   9,043.23 |  2,258 | 3,226,213 |  4,305 |


Top 1 `NEGmirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                                  | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
 |:---------------------------------|:----------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
 | **NEGmir~immediately_available** | available |     12,636.00 |    1.94 |    0.43 | 254.47 |   162 | 289,770 |    274 |




```python
# %%

bigram_dfs['RBdirect'].filter(like='~before_', axis=0)
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
      <th>l2</th>
      <th>f</th>
      <th>E11</th>
      <th>am_log_likelihood</th>
      <th>...</th>
      <th>adv_total</th>
      <th>adj_total</th>
      <th>l1</th>
      <th>first_char</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>COM~before_dark</th>
      <td>before_dark</td>
      <td>72</td>
      <td>69.82</td>
      <td>2.12</td>
      <td>...</td>
      <td>681</td>
      <td>72272</td>
      <td>COMPLEMENT</td>
      <td>b</td>
    </tr>
    <tr>
      <th>NEGany~before_available</th>
      <td>before_available</td>
      <td>177</td>
      <td>8.23</td>
      <td>1,020.91</td>
      <td>...</td>
      <td>681</td>
      <td>666909</td>
      <td>NEGATED</td>
      <td>b</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 47 columns</p>
</div>




```python
# %%

for key, info in samples_dict.items():
    if key in ('bigrams', 'adj'):
        key = f'ALL {key.replace("adj", "adjectives")}'
    formatted_iter = [
        f'_{a.replace("_", " ")}_' for a
        in (info['adj'] if isinstance(info, dict)
            else info)]
    print_iter(formatted_iter,
               header=f'1. _{key}_ ({len(formatted_iter)} unique)',
               bullet='1.', indent=3)
```

    
    1. _necessarily_ (16 unique)
       1. _bad_
       1. _better_
       1. _essential_
       1. _useful_
       1. _reliable_
       1. _illegal_
       1. _surprising_
       1. _wrong_
       1. _proud_
       1. _new_
       1. _true_
       1. _right_
       1. _representative_
       1. _fun_
       1. _easy_
       1. _indicative_
    
    1. _that_ (20 unique)
       1. _unusual_
       1. _keen_
       1. _big_
       1. _far-fetched_
       1. _thrilled_
       1. _popular_
       1. _easy_
       1. _complicated_
       1. _comfortable_
       1. _familiar_
       1. _simple_
       1. _clear_
       1. _hard_
       1. _impressive_
       1. _surprising_
       1. _uncommon_
       1. _dissimilar_
       1. _fond_
       1. _great_
       1. _noticeable_
    
    1. _exactly_ (11 unique)
       1. _conducive_
       1. _pleasant_
       1. _clear_
       1. _surprising_
       1. _new_
       1. _sure_
       1. _difficult_
       1. _cheap_
       1. _shocking_
       1. _easy_
       1. _famous_
    
    1. _any_ (16 unique)
       1. _closer_
       1. _simpler_
       1. _easier_
       1. _worse_
       1. _different_
       1. _bigger_
       1. _nicer_
       1. _happier_
       1. _younger_
       1. _smarter_
       1. _cheaper_
       1. _higher_
       1. _good_
       1. _clearer_
       1. _brighter_
       1. _better_
    
    1. _remotely_ (14 unique)
       1. _funny_
       1. _ready_
       1. _qualified_
       1. _accurate_
       1. _similar_
       1. _surprising_
       1. _close_
       1. _true_
       1. _new_
       1. _interested_
       1. _possible_
       1. _interesting_
       1. _believable_
       1. _comparable_
    
    1. _ever_ (13 unique)
       1. _sick_
       1. _closer_
       1. _simple_
       1. _enough_
       1. _black_
       1. _certain_
       1. _satisfied_
       1. _perfect_
       1. _boring_
       1. _able_
       1. _easy_
       1. _good_
       1. _sure_
    
    1. _yet_ (13 unique)
       1. _complete_
       1. _over_
       1. _mainstream_
       1. _clear_
       1. _ready_
       1. _certain_
       1. _convinced_
       1. _online_
       1. _official_
       1. _available_
       1. _eligible_
       1. _final_
       1. _sure_
    
    1. _immediately_ (10 unique)
       1. _clear_
       1. _forthcoming_
       1. _certain_
       1. _able_
       1. _available_
       1. _possible_
       1. _intuitive_
       1. _obvious_
       1. _sure_
       1. _reachable_
    
    1. _particularly_ (17 unique)
       1. _likeable_
       1. _athletic_
       1. _forthcoming_
       1. _flashy_
       1. _novel_
       1. _comfortable_
       1. _radical_
       1. _surprising_
       1. _wrong_
       1. _revolutionary_
       1. _likable_
       1. _close_
       1. _new_
       1. _religious_
       1. _fast_
       1. _original_
       1. _remarkable_
    
    1. _inherently_ (9 unique)
       1. _bad_
       1. _improper_
       1. _illegal_
       1. _problematic_
       1. _wrong_
       1. _evil_
       1. _good_
       1. _negative_
       1. _better_
    
    1. _terribly_ (17 unique)
       1. _special_
       1. _unusual_
       1. _clear_
       1. _different_
       1. _remarkable_
       1. _reliable_
       1. _impressive_
       1. _likely_
       1. _surprising_
       1. _uncommon_
       1. _new_
       1. _interesting_
       1. _interested_
       1. _productive_
       1. _popular_
       1. _original_
       1. _sure_
    
    1. _ALL bigrams_ (156 unique)
       1. _remotely similar_
       1. _terribly productive_
       1. _terribly unusual_
       1. _exactly difficult_
       1. _remotely close_
       1. _immediately reachable_
       1. _yet mainstream_
       1. _particularly forthcoming_
       1. _particularly flashy_
       1. _any nicer_
       1. _immediately available_
       1. _necessarily essential_
       1. _particularly original_
       1. _necessarily surprising_
       1. _exactly easy_
       1. _immediately certain_
       1. _immediately able_
       1. _terribly new_
       1. _terribly likely_
       1. _that simple_
       1. _ever able_
       1. _necessarily illegal_
       1. _particularly fast_
       1. _yet final_
       1. _inherently bad_
       1. _terribly interesting_
       1. _exactly surprising_
       1. _remotely funny_
       1. _that clear_
       1. _ever black_
       1. _remotely believable_
       1. _that big_
       1. _necessarily fun_
       1. _terribly impressive_
       1. _particularly surprising_
       1. _yet sure_
       1. _any cheaper_
       1. _ever certain_
       1. _ever sure_
       1. _necessarily useful_
       1. _necessarily wrong_
       1. _exactly famous_
       1. _remotely new_
       1. _necessarily easy_
       1. _particularly remarkable_
       1. _any simpler_
       1. _particularly revolutionary_
       1. _that dissimilar_
       1. _that familiar_
       1. _necessarily reliable_
       1. _that complicated_
       1. _inherently better_
       1. _that easy_
       1. _necessarily true_
       1. _inherently negative_
       1. _any different_
       1. _remotely ready_
       1. _immediately possible_
       1. _immediately obvious_
       1. _remotely true_
       1. _exactly pleasant_
       1. _any good_
       1. _particularly likeable_
       1. _inherently evil_
       1. _that far-fetched_
       1. _any worse_
       1. _yet ready_
       1. _inherently wrong_
       1. _particularly novel_
       1. _remotely interesting_
       1. _any clearer_
       1. _remotely qualified_
       1. _ever satisfied_
       1. _yet eligible_
       1. _yet over_
       1. _that thrilled_
       1. _immediately forthcoming_
       1. _necessarily better_
       1. _any happier_
       1. _terribly interested_
       1. _remotely surprising_
       1. _particularly comfortable_
       1. _immediately sure_
       1. _that impressive_
       1. _exactly new_
       1. _exactly conducive_
       1. _any higher_
       1. _any better_
       1. _any bigger_
       1. _that unusual_
       1. _terribly different_
       1. _remotely possible_
       1. _ever easy_
       1. _inherently good_
       1. _necessarily bad_
       1. _exactly sure_
       1. _ever boring_
       1. _that uncommon_
       1. _necessarily new_
       1. _particularly religious_
       1. _particularly wrong_
       1. _terribly popular_
       1. _that popular_
       1. _particularly likable_
       1. _exactly shocking_
       1. _terribly clear_
       1. _yet official_
       1. _any brighter_
       1. _terribly original_
       1. _ever good_
       1. _that great_
       1. _immediately clear_
       1. _particularly close_
       1. _inherently problematic_
       1. _inherently illegal_
       1. _terribly remarkable_
       1. _particularly athletic_
       1. _any closer_
       1. _necessarily representative_
       1. _terribly special_
       1. _particularly new_
       1. _ever enough_
       1. _terribly uncommon_
       1. _ever simple_
       1. _yet clear_
       1. _remotely comparable_
       1. _particularly radical_
       1. _that hard_
       1. _immediately intuitive_
       1. _that keen_
       1. _that surprising_
       1. _any easier_
       1. _necessarily right_
       1. _remotely interested_
       1. _yet online_
       1. _inherently improper_
       1. _yet convinced_
       1. _terribly surprising_
       1. _ever perfect_
       1. _necessarily proud_
       1. _ever sick_
       1. _yet available_
       1. _any younger_
       1. _any smarter_
       1. _yet certain_
       1. _ever closer_
       1. _terribly sure_
       1. _that noticeable_
       1. _that fond_
       1. _terribly reliable_
       1. _yet complete_
       1. _remotely accurate_
       1. _that comfortable_
       1. _necessarily indicative_
       1. _exactly clear_
       1. _exactly cheap_
    
    1. _ALL adjectives_ (106 unique)
       1. _ready_
       1. _illegal_
       1. _eligible_
       1. _big_
       1. _representative_
       1. _original_
       1. _over_
       1. _complicated_
       1. _flashy_
       1. _improper_
       1. _problematic_
       1. _nicer_
       1. _true_
       1. _religious_
       1. _easier_
       1. _convinced_
       1. _uncommon_
       1. _believable_
       1. _sure_
       1. _worse_
       1. _radical_
       1. _reliable_
       1. _bigger_
       1. _able_
       1. _comparable_
       1. _famous_
       1. _accurate_
       1. _keen_
       1. _perfect_
       1. _thrilled_
       1. _higher_
       1. _clearer_
       1. _easy_
       1. _funny_
       1. _athletic_
       1. _comfortable_
       1. _happier_
       1. _revolutionary_
       1. _proud_
       1. _cheaper_
       1. _online_
       1. _interested_
       1. _complete_
       1. _hard_
       1. _surprising_
       1. _interesting_
       1. _evil_
       1. _difficult_
       1. _good_
       1. _closer_
       1. _qualified_
       1. _likeable_
       1. _close_
       1. _right_
       1. _remarkable_
       1. _better_
       1. _special_
       1. _unusual_
       1. _mainstream_
       1. _certain_
       1. _similar_
       1. _popular_
       1. _sick_
       1. _simpler_
       1. _essential_
       1. _black_
       1. _novel_
       1. _satisfied_
       1. _likely_
       1. _shocking_
       1. _familiar_
       1. _negative_
       1. _reachable_
       1. _bad_
       1. _available_
       1. _new_
       1. _final_
       1. _fun_
       1. _dissimilar_
       1. _fond_
       1. _forthcoming_
       1. _great_
       1. _boring_
       1. _smarter_
       1. _possible_
       1. _noticeable_
       1. _brighter_
       1. _enough_
       1. _conducive_
       1. _younger_
       1. _official_
       1. _far-fetched_
       1. _productive_
       1. _obvious_
       1. _useful_
       1. _cheap_
       1. _indicative_
       1. _simple_
       1. _clear_
       1. _different_
       1. _impressive_
       1. _wrong_
       1. _likable_
       1. _intuitive_
       1. _fast_
       1. _pleasant_



1. _necessarily_ (16 unique)
   1. _fun_
   1. _useful_
   1. _reliable_
   1. _proud_
   1. _easy_
   1. _right_
   1. _representative_
   1. _better_
   1. _surprising_
   1. _essential_
   1. _true_
   1. _wrong_
   1. _illegal_
   1. _indicative_
   1. _new_
   1. _bad_

1. _that_ (20 unique)
   1. _comfortable_
   1. _great_
   1. _thrilled_
   1. _clear_
   1. _fond_
   1. _popular_
   1. _dissimilar_
   1. _unusual_
   1. _surprising_
   1. _simple_
   1. _keen_
   1. _familiar_
   1. _complicated_
   1. _far-fetched_
   1. _uncommon_
   1. _easy_
   1. _big_
   1. _noticeable_
   1. _impressive_
   1. _hard_

1. _exactly_ (11 unique)
   1. _difficult_
   1. _cheap_
   1. _easy_
   1. _conducive_
   1. _surprising_
   1. _shocking_
   1. _pleasant_
   1. _famous_
   1. _sure_
   1. _clear_
   1. _new_

1. _any_ (16 unique)
   1. _brighter_
   1. _younger_
   1. _different_
   1. _cheaper_
   1. _better_
   1. _simpler_
   1. _smarter_
   1. _happier_
   1. _higher_
   1. _good_
   1. _closer_
   1. _worse_
   1. _nicer_
   1. _clearer_
   1. _bigger_
   1. _easier_

1. _remotely_ (14 unique)
   1. _close_
   1. _believable_
   1. _interesting_
   1. _similar_
   1. _interested_
   1. _possible_
   1. _surprising_
   1. _accurate_
   1. _ready_
   1. _funny_
   1. _qualified_
   1. _true_
   1. _comparable_
   1. _new_

1. _ever_ (13 unique)
   1. _certain_
   1. _able_
   1. _easy_
   1. _perfect_
   1. _sick_
   1. _enough_
   1. _simple_
   1. _sure_
   1. _good_
   1. _boring_
   1. _closer_
   1. _black_
   1. _satisfied_

1. _yet_ (13 unique)
   1. _certain_
   1. _over_
   1. _final_
   1. _available_
   1. _mainstream_
   1. _convinced_
   1. _ready_
   1. _sure_
   1. _official_
   1. _online_
   1. _eligible_
   1. _complete_
   1. _clear_

1. _immediately_ (10 unique)
   1. _certain_
   1. _able_
   1. _available_
   1. _obvious_
   1. _intuitive_
   1. _forthcoming_
   1. _sure_
   1. _clear_
   1. _reachable_
   1. _possible_

1. _particularly_ (17 unique)
   1. _close_
   1. _athletic_
   1. _revolutionary_
   1. _remarkable_
   1. _comfortable_
   1. _surprising_
   1. _original_
   1. _forthcoming_
   1. _radical_
   1. _flashy_
   1. _religious_
   1. _novel_
   1. _wrong_
   1. _fast_
   1. _likeable_
   1. _likable_
   1. _new_

1. _inherently_ (9 unique)
   1. _problematic_
   1. _better_
   1. _negative_
   1. _improper_
   1. _good_
   1. _bad_
   1. _illegal_
   1. _wrong_
   1. _evil_

1. _terribly_ (17 unique)
   1. _different_
   1. _likely_
   1. _uncommon_
   1. _interesting_
   1. _reliable_
   1. _remarkable_
   1. _productive_
   1. _interested_
   1. _unusual_
   1. _surprising_
   1. _original_
   1. _special_
   1. _sure_
   1. _clear_
   1. _impressive_
   1. _popular_
   1. _new_

1. _ALL bigrams_ (156 unique)
   1. _particularly wrong_
   1. _inherently wrong_
   1. _that easy_
   1. _that popular_
   1. _exactly surprising_
   1. _any brighter_
   1. _terribly unusual_
   1. _ever sick_
   1. _exactly clear_
   1. _any good_
   1. _ever easy_
   1. _immediately sure_
   1. _remotely qualified_
   1. _inherently good_
   1. _particularly athletic_
   1. _terribly productive_
   1. _necessarily reliable_
   1. _any worse_
   1. _remotely new_
   1. _remotely close_
   1. _exactly conducive_
   1. _ever certain_
   1. _that familiar_
   1. _necessarily better_
   1. _exactly sure_
   1. _ever able_
   1. _inherently illegal_
   1. _particularly remarkable_
   1. _particularly close_
   1. _any clearer_
   1. _terribly remarkable_
   1. _that simple_
   1. _any nicer_
   1. _yet over_
   1. _yet sure_
   1. _that comfortable_
   1. _necessarily proud_
   1. _necessarily surprising_
   1. _immediately available_
   1. _exactly famous_
   1. _particularly comfortable_
   1. _exactly cheap_
   1. _exactly pleasant_
   1. _necessarily fun_
   1. _particularly radical_
   1. _any easier_
   1. _yet certain_
   1. _yet complete_
   1. _necessarily easy_
   1. _exactly difficult_
   1. _ever closer_
   1. _yet eligible_
   1. _exactly shocking_
   1. _terribly sure_
   1. _yet clear_
   1. _remotely funny_
   1. _remotely interesting_
   1. _that impressive_
   1. _particularly fast_
   1. _that hard_
   1. _necessarily useful_
   1. _ever satisfied_
   1. _necessarily wrong_
   1. _immediately clear_
   1. _any higher_
   1. _ever enough_
   1. _immediately possible_
   1. _that noticeable_
   1. _terribly surprising_
   1. _terribly likely_
   1. _remotely believable_
   1. _terribly clear_
   1. _inherently problematic_
   1. _terribly uncommon_
   1. _ever black_
   1. _necessarily true_
   1. _terribly interested_
   1. _that dissimilar_
   1. _necessarily indicative_
   1. _any simpler_
   1. _immediately certain_
   1. _inherently bad_
   1. _exactly easy_
   1. _any smarter_
   1. _yet available_
   1. _any happier_
   1. _any closer_
   1. _particularly original_
   1. _particularly religious_
   1. _yet online_
   1. _any bigger_
   1. _that thrilled_
   1. _yet convinced_
   1. _particularly likeable_
   1. _that great_
   1. _that unusual_
   1. _any cheaper_
   1. _yet official_
   1. _terribly original_
   1. _yet final_
   1. _ever sure_
   1. _remotely possible_
   1. _particularly surprising_
   1. _that far-fetched_
   1. _necessarily representative_
   1. _that surprising_
   1. _ever perfect_
   1. _remotely similar_
   1. _inherently improper_
   1. _that fond_
   1. _ever good_
   1. _remotely true_
   1. _terribly reliable_
   1. _remotely interested_
   1. _terribly new_
   1. _any younger_
   1. _terribly different_
   1. _that complicated_
   1. _immediately obvious_
   1. _particularly likable_
   1. _immediately intuitive_
   1. _necessarily new_
   1. _yet ready_
   1. _particularly flashy_
   1. _terribly special_
   1. _particularly forthcoming_
   1. _that big_
   1. _immediately reachable_
   1. _immediately able_
   1. _necessarily bad_
   1. _terribly popular_
   1. _inherently better_
   1. _any better_
   1. _remotely comparable_
   1. _ever boring_
   1. _particularly new_
   1. _terribly interesting_
   1. _exactly new_
   1. _that keen_
   1. _yet mainstream_
   1. _inherently negative_
   1. _that clear_
   1. _that uncommon_
   1. _necessarily right_
   1. _any different_
   1. _inherently evil_
   1. _particularly revolutionary_
   1. _ever simple_
   1. _terribly impressive_
   1. _necessarily essential_
   1. _particularly novel_
   1. _necessarily illegal_
   1. _immediately forthcoming_
   1. _remotely surprising_
   1. _remotely accurate_
   1. _remotely ready_

1. _ALL adjectives_ (106 unique)
   1. _close_
   1. _proud_
   1. _interested_
   1. _radical_
   1. _true_
   1. _different_
   1. _fond_
   1. _likely_
   1. _cheaper_
   1. _similar_
   1. _dissimilar_
   1. _interesting_
   1. _ready_
   1. _online_
   1. _difficult_
   1. _better_
   1. _representative_
   1. _sure_
   1. _eligible_
   1. _impressive_
   1. _possible_
   1. _evil_
   1. _right_
   1. _essential_
   1. _convinced_
   1. _flashy_
   1. _special_
   1. _simple_
   1. _religious_
   1. _keen_
   1. _complete_
   1. _likable_
   1. _complicated_
   1. _accurate_
   1. _far-fetched_
   1. _enough_
   1. _illegal_
   1. _likeable_
   1. _bigger_
   1. _easier_
   1. _younger_
   1. _available_
   1. _big_
   1. _negative_
   1. _simpler_
   1. _thrilled_
   1. _comparable_
   1. _brighter_
   1. _revolutionary_
   1. _productive_
   1. _comfortable_
   1. _great_
   1. _improper_
   1. _clear_
   1. _reachable_
   1. _intuitive_
   1. _certain_
   1. _obvious_
   1. _perfect_
   1. _unusual_
   1. _happier_
   1. _pleasant_
   1. _worse_
   1. _novel_
   1. _able_
   1. _familiar_
   1. _useful_
   1. _athletic_
   1. _sick_
   1. _funny_
   1. _qualified_
   1. _mainstream_
   1. _closer_
   1. _problematic_
   1. _fun_
   1. _uncommon_
   1. _final_
   1. _cheap_
   1. _easy_
   1. _forthcoming_
   1. _famous_
   1. _hard_
   1. _over_
   1. _conducive_
   1. _smarter_
   1. _original_
   1. _fast_
   1. _bad_
   1. _satisfied_
   1. _surprising_
   1. _good_
   1. _indicative_
   1. _nicer_
   1. _clearer_
   1. _higher_
   1. _new_
   1. _black_
   1. _shocking_
   1. _remarkable_
   1. _wrong_
   1. _reliable_
   1. _noticeable_
   1. _official_
   1. _boring_
   1. _popular_
   1. _believable_



```python
NEG_bigrams_sample = pd.concat(
    (ad['both'] for ad in samples_dict.values() if isinstance(ad, dict))).sort_values('LRC', ascending=False)
```


```python
top_NEGbigram_df_path =  OUT_DIR.joinpath(
    f'{TAG}-Top{K}_NEG-ADV_Top{bigram_k}-bigrams{bigram_floor}.{timestamp_today()}.csv')
print(top_NEGbigram_df_path)

```

    /share/compling/projects/sanpi/results/top_AM/ALL/ALL-Top8/ALL-Top8_NEG-ADV_Top10-bigrams50.2024-07-28.csv



```python
NEG_bigrams_sample.to_csv(top_NEGbigram_df_path)
nb_show_table(NEG_bigrams_sample.sort_values('LRC', ascending=False),
              outpath=top_NEGbigram_df_path.with_suffix('.md'))
```

    
    |                                       | `l1`       |   `exp_f` | `adv`        |       `f1` | `l2`                       |   `P1` |   `unexp_f` |   `f2` |   `dP1` |   `odds_r_disc` |       `G2` |   `LRC` |   `adv_total` |   `MI` |   `adj_total` |        `N` |    `t` |    `f` | `adj`          |
    |:--------------------------------------|:-----------|----------:|:-------------|-----------:|:---------------------------|-------:|------------:|-------:|--------:|----------------:|-----------:|--------:|--------------:|-------:|--------------:|-----------:|-------:|-------:|:---------------|
    | **NEGany~yet_clear**                  | NEGATED    |    456.44 | yet          |  3,173,660 | yet_clear                  |   0.99 |    9,949.56 | 10,476 |    0.95 |            3.51 |  64,409.97 |   10.77 |        95,763 |   1.36 |       349,214 | 72,839,589 |  97.54 | 10,406 | clear          |
    | **NEGany~yet_ready**                  | NEGATED    |    331.09 | yet          |  3,173,660 | yet_ready                  |   0.99 |    7,169.91 |  7,599 |    0.94 |            3.22 |  45,985.07 |    9.93 |        95,763 |   1.36 |       141,590 | 72,839,589 |  82.79 |  7,501 | ready          |
    | **NEGany~necessarily_indicative**     | NEGATED    |     61.00 | necessarily  |  3,173,660 | necessarily_indicative     |   0.99 |    1,328.00 |  1,400 |    0.95 |            3.42 |   8,577.54 |    9.43 |        48,947 |   1.36 |         8,148 | 72,839,589 |  35.63 |  1,389 | indicative     |
    | **NEGany~that_uncommon**              | NEGATED    |     35.03 | that         |  3,173,660 | that_uncommon              |   1.00 |      766.97 |    804 |    0.95 |            3.85 |   4,998.32 |    9.43 |       208,262 |   1.36 |        11,312 | 72,839,589 |  27.08 |    802 | uncommon       |
    | **NEGany~exactly_easy**               | NEGATED    |     46.75 | exactly      |  3,173,660 | exactly_easy               |   0.99 |    1,019.25 |  1,073 |    0.95 |            3.49 |   6,596.91 |    9.32 |        58,643 |   1.36 |       579,827 | 72,839,589 |  31.22 |  1,066 | easy           |
    | **NEGany~yet_complete**               | NEGATED    |     96.20 | yet          |  3,173,660 | yet_complete               |   0.98 |    2,077.80 |  2,208 |    0.94 |            3.14 |  13,277.09 |    9.20 |        95,763 |   1.35 |        86,361 | 72,839,589 |  44.56 |  2,174 | complete       |
    | **NEGany~that_surprising**            | NEGATED    |     49.80 | that         |  3,173,660 | that_surprising            |   0.99 |    1,083.20 |  1,143 |    0.95 |            3.37 |   6,986.81 |    9.20 |       208,262 |   1.36 |        70,540 | 72,839,589 |  32.18 |  1,133 | surprising     |
    | **NEGany~exactly_new**                | NEGATED    |     60.48 | exactly      |  3,173,660 | exactly_new                |   0.99 |    1,310.52 |  1,388 |    0.94 |            3.24 |   8,410.32 |    9.10 |        58,643 |   1.36 |       253,862 | 72,839,589 |  35.39 |  1,371 | new            |
    | **NEGany~necessarily_easy**           | NEGATED    |     39.95 | necessarily  |  3,173,660 | necessarily_easy           |   0.99 |      869.05 |    917 |    0.95 |            3.37 |   5,605.64 |    9.01 |        48,947 |   1.36 |       579,827 | 72,839,589 |  28.82 |    909 | easy           |
    | **NEGany~yet_final**                  | NEGATED    |     28.02 | yet          |  3,173,660 | yet_final                  |   1.00 |      611.98 |    643 |    0.95 |            3.60 |   3,972.92 |    8.97 |        95,763 |   1.36 |         5,860 | 72,839,589 |  24.19 |    640 | final          |
    | **NEGany~exactly_cheap**              | NEGATED    |     30.28 | exactly      |  3,173,660 | exactly_cheap              |   0.99 |      660.72 |    695 |    0.95 |            3.53 |   4,281.59 |    8.96 |        58,643 |   1.36 |        60,531 | 72,839,589 |  25.13 |    691 | cheap          |
    | **NEGany~yet_eligible**               | NEGATED    |     19.52 | yet          |  3,173,660 | yet_eligible               |   1.00 |      428.48 |    448 |    0.96 |            4.29 |   2,807.56 |    8.96 |        95,763 |   1.36 |        23,252 | 72,839,589 |  20.24 |    448 | eligible       |
    | **NEGany~that_unusual**               | NEGATED    |     43.05 | that         |  3,173,660 | that_unusual               |   0.99 |      933.95 |    988 |    0.95 |            3.27 |   6,003.05 |    8.92 |       208,262 |   1.36 |        71,234 | 72,839,589 |  29.88 |    977 | unusual        |
    | **NEGany~exactly_clear**              | NEGATED    |     77.73 | exactly      |  3,173,660 | exactly_clear              |   0.98 |    1,668.27 |  1,784 |    0.94 |            3.00 |  10,578.33 |    8.78 |        58,643 |   1.35 |       349,214 | 72,839,589 |  39.92 |  1,746 | clear          |
    | **NEGany~exactly_surprising**         | NEGATED    |     19.21 | exactly      |  3,173,660 | exactly_surprising         |   1.00 |      420.79 |    441 |    0.95 |            3.81 |   2,743.34 |    8.71 |        58,643 |   1.36 |        70,540 | 72,839,589 |  20.06 |    440 | surprising     |
    | **NEGany~that_complicated**           | NEGATED    |     53.59 | that         |  3,173,660 | that_complicated           |   0.98 |    1,153.41 |  1,230 |    0.94 |            3.05 |   7,337.84 |    8.68 |       208,262 |   1.35 |       159,822 | 72,839,589 |  33.20 |  1,207 | complicated    |
    | **NEGany~terribly_surprising**        | NEGATED    |     42.00 | terribly     |  3,173,660 | terribly_surprising        |   0.98 |      907.00 |    964 |    0.94 |            3.13 |   5,794.10 |    8.66 |        58,964 |   1.35 |        70,540 | 72,839,589 |  29.44 |    949 | surprising     |
    | **NEGany~yet_official**               | NEGATED    |     15.34 | yet          |  3,173,660 | yet_official               |   1.00 |      336.66 |    352 |    0.96 |            4.19 |   2,205.93 |    8.61 |        95,763 |   1.36 |         6,853 | 72,839,589 |  17.94 |    352 | official       |
    | **NEGany~that_hard**                  | NEGATED    |    452.26 | that         |  3,173,660 | that_hard                  |   0.96 |    9,495.74 | 10,380 |    0.91 |            2.70 |  58,817.24 |    8.59 |       208,262 |   1.34 |       348,463 | 72,839,589 |  95.21 |  9,948 | hard           |
    | **NEGany~that_familiar**              | NEGATED    |     50.37 | that         |  3,173,660 | that_familiar              |   0.97 |    1,075.63 |  1,156 |    0.93 |            2.91 |   6,781.11 |    8.35 |       208,262 |   1.35 |       156,296 | 72,839,589 |  32.05 |  1,126 | familiar       |
    | **NEGany~necessarily_representative** | NEGATED    |     21.44 | necessarily  |  3,173,660 | necessarily_representative |   0.99 |      465.56 |    492 |    0.95 |            3.29 |   2,996.58 |    8.34 |        48,947 |   1.36 |        18,355 | 72,839,589 |  21.10 |    487 | representative |
    | **NEGany~necessarily_surprising**     | NEGATED    |     14.86 | necessarily  |  3,173,660 | necessarily_surprising     |   1.00 |      325.14 |    341 |    0.95 |            3.70 |   2,117.16 |    8.33 |        48,947 |   1.36 |        70,540 | 72,839,589 |  17.63 |    340 | surprising     |
    | **NEGany~immediately_clear**          | NEGATED    |  1,134.49 | immediately  |  3,173,660 | immediately_clear          |   0.94 |   23,281.51 | 26,038 |    0.89 |            2.52 | 141,186.69 |    8.16 |        96,973 |   1.33 |       349,214 | 72,839,589 | 149.00 | 24,416 | clear          |
    | **NEGany~necessarily_new**            | NEGATED    |     21.44 | necessarily  |  3,173,660 | necessarily_new            |   0.98 |      460.56 |    492 |    0.94 |            3.00 |   2,923.82 |    7.94 |        48,947 |   1.35 |       253,862 | 72,839,589 |  20.98 |    482 | new            |
    | **NEGany~that_dissimilar**            | NEGATED    |     13.38 | that         |  3,173,660 | that_dissimilar            |   0.99 |      290.62 |    307 |    0.95 |            3.28 |   1,871.65 |    7.86 |       208,262 |   1.36 |         4,605 | 72,839,589 |  16.67 |    304 | dissimilar     |
    | **NEGany~exactly_conducive**          | NEGATED    |      9.06 | exactly      |  3,173,660 | exactly_conducive          |   1.00 |      198.94 |    208 |    0.96 |            3.96 |   1,303.50 |    7.82 |        58,643 |   1.36 |         9,110 | 72,839,589 |  13.79 |    208 | conducive      |
    | **NEGany~that_noticeable**            | NEGATED    |     11.63 | that         |  3,173,660 | that_noticeable            |   0.99 |      252.37 |    267 |    0.95 |            3.22 |   1,621.81 |    7.65 |       208,262 |   1.36 |        31,467 | 72,839,589 |  15.53 |    264 | noticeable     |
    | **NEGany~immediately_possible**       | NEGATED    |     45.92 | immediately  |  3,173,660 | immediately_possible       |   0.95 |      954.08 |  1,054 |    0.91 |            2.61 |   5,845.77 |    7.62 |        96,973 |   1.34 |       245,272 | 72,839,589 |  30.17 |  1,000 | possible       |
    | **NEGany~yet_convinced**              | NEGATED    |      7.36 | yet          |  3,173,660 | yet_convinced              |   1.00 |      161.64 |    169 |    0.96 |            3.87 |   1,059.09 |    7.50 |        95,763 |   1.36 |        12,132 | 72,839,589 |  12.43 |    169 | convinced      |
    | **NEGany~exactly_shocking**           | NEGATED    |      6.58 | exactly      |  3,173,660 | exactly_shocking           |   1.00 |      144.42 |    151 |    0.96 |            3.82 |     946.29 |    7.33 |        58,643 |   1.36 |        35,115 | 72,839,589 |  11.75 |    151 | shocking       |
    | **NEGany~exactly_pleasant**           | NEGATED    |      6.19 | exactly      |  3,173,660 | exactly_pleasant           |   1.00 |      135.81 |    142 |    0.96 |            3.80 |     889.88 |    7.24 |        58,643 |   1.36 |        52,223 | 72,839,589 |  11.40 |    142 | pleasant       |
    | **NEGany~yet_over**                   | NEGATED    |      7.10 | yet          |  3,173,660 | yet_over                   |   0.99 |      154.90 |    163 |    0.95 |            3.38 |   1,003.13 |    7.21 |        95,763 |   1.36 |         3,983 | 72,839,589 |  12.17 |    162 | over           |
    | **NEGany~exactly_famous**             | NEGATED    |      5.66 | exactly      |  3,173,660 | exactly_famous             |   1.00 |      124.34 |    130 |    0.96 |            3.76 |     814.68 |    7.10 |        58,643 |   1.36 |       223,813 | 72,839,589 |  10.90 |    130 | famous         |
    | **NEGany~exactly_difficult**          | NEGATED    |      5.49 | exactly      |  3,173,660 | exactly_difficult          |   1.00 |      120.51 |    126 |    0.96 |            3.74 |     789.62 |    7.05 |        58,643 |   1.36 |       732,106 | 72,839,589 |  10.74 |    126 | difficult      |
    | **NEGany~necessarily_useful**         | NEGATED    |      4.53 | necessarily  |  3,173,660 | necessarily_useful         |   1.00 |       99.47 |    104 |    0.96 |            3.66 |     651.75 |    6.75 |        48,947 |   1.36 |       227,709 | 72,839,589 |   9.75 |    104 | useful         |
    | **NEGany~yet_online**                 | NEGATED    |      4.27 | yet          |  3,173,660 | yet_online                 |   1.00 |       93.73 |     98 |    0.96 |            3.64 |     614.14 |    6.66 |        95,763 |   1.36 |        15,650 | 72,839,589 |   9.47 |     98 | online         |
    | **NEGany~necessarily_fun**            | NEGATED    |      4.18 | necessarily  |  3,173,660 | necessarily_fun            |   1.00 |       91.82 |     96 |    0.96 |            3.63 |     601.61 |    6.62 |        48,947 |   1.36 |       190,026 | 72,839,589 |   9.37 |     96 | fun            |
    | **NEGany~necessarily_essential**      | NEGATED    |      4.05 | necessarily  |  3,173,660 | necessarily_essential      |   1.00 |       88.95 |     93 |    0.96 |            3.61 |     582.81 |    6.57 |        48,947 |   1.36 |        69,845 | 72,839,589 |   9.22 |     93 | essential      |
    | **NEGmir~ever_easy**                  | NEGMIR     |     63.25 | ever         |    291,732 | ever_easy                  |   1.00 |      304.75 |    369 |    0.83 |            3.08 |   1,285.01 |    6.44 |         5,060 |   0.76 |        18,610 |  1,701,929 |  15.89 |    368 | easy           |
    | **NEGany~terribly_original**          | NEGATED    |      9.24 | terribly     |  3,173,660 | terribly_original          |   0.94 |      189.76 |    212 |    0.90 |            2.51 |   1,150.48 |    6.41 |        58,964 |   1.33 |        37,594 | 72,839,589 |  13.45 |    199 | original       |
    | **NEGany~necessarily_reliable**       | NEGATED    |      3.53 | necessarily  |  3,173,660 | necessarily_reliable       |   1.00 |       77.47 |     81 |    0.96 |            3.55 |     507.61 |    6.35 |        48,947 |   1.36 |        90,598 | 72,839,589 |   8.61 |     81 | reliable       |
    | **NEGany~any_happier**                | NEGATED    |     41.96 | any          |  3,173,660 | any_happier                |   0.86 |      786.04 |    963 |    0.82 |            2.13 |   4,420.49 |    6.34 |        34,382 |   1.30 |        16,606 | 72,839,589 |  27.32 |    828 | happier        |
    | **NEGany~terribly_different**         | NEGATED    |     17.82 | terribly     |  3,173,660 | terribly_different         |   0.89 |      348.18 |    409 |    0.85 |            2.27 |   2,022.47 |    6.33 |        58,964 |   1.31 |       825,838 | 72,839,589 |  18.20 |    366 | different      |
    | **NEGany~terribly_uncommon**          | NEGATED    |      4.57 | terribly     |  3,173,660 | terribly_uncommon          |   0.98 |       98.43 |    105 |    0.94 |            2.96 |     625.85 |    6.33 |        58,964 |   1.35 |        11,312 | 72,839,589 |   9.70 |    103 | uncommon       |
    | **NEGany~terribly_likely**            | NEGATED    |      4.84 | terribly     |  3,173,660 | terribly_likely            |   0.97 |      103.16 |    111 |    0.93 |            2.83 |     649.50 |    6.26 |        58,964 |   1.35 |       890,421 | 72,839,589 |   9.93 |    108 | likely         |
    | **NEGany~terribly_unusual**           | NEGATED    |      6.75 | terribly     |  3,173,660 | terribly_unusual           |   0.94 |      139.25 |    155 |    0.90 |            2.53 |     847.05 |    6.17 |        58,964 |   1.33 |        71,234 | 72,839,589 |  11.52 |    146 | unusual        |
    | **NEGany~necessarily_proud**          | NEGATED    |      3.09 | necessarily  |  3,173,660 | necessarily_proud          |   1.00 |       67.91 |     71 |    0.96 |            3.50 |     444.94 |    6.14 |        48,947 |   1.36 |       207,536 | 72,839,589 |   8.06 |     71 | proud          |
    | **NEGany~particularly_religious**     | NEGATED    |     24.62 | particularly |  3,173,660 | particularly_religious     |   0.86 |      460.38 |    565 |    0.81 |            2.12 |   2,585.71 |    6.12 |       513,668 |   1.29 |        28,028 | 72,839,589 |  20.90 |    485 | religious      |
    | **NEGany~yet_mainstream**             | NEGATED    |      3.05 | yet          |  3,173,660 | yet_mainstream             |   1.00 |       66.95 |     70 |    0.96 |            3.49 |     438.67 |    6.11 |        95,763 |   1.36 |        17,792 | 72,839,589 |   8.00 |     70 | mainstream     |
    | **NEGany~particularly_new**           | NEGATED    |     39.21 | particularly |  3,173,660 | particularly_new           |   0.83 |      707.79 |    900 |    0.79 |            2.03 |   3,874.46 |    6.04 |       513,668 |   1.28 |       253,862 | 72,839,589 |  25.90 |    747 | new            |
    | **NEGany~terribly_impressive**        | NEGATED    |      9.50 | terribly     |  3,173,660 | terribly_impressive        |   0.90 |      186.50 |    218 |    0.86 |            2.28 |   1,087.64 |    5.97 |        58,964 |   1.31 |       178,051 | 72,839,589 |  13.32 |    196 | impressive     |
    | **NEGmir~particularly_new**           | NEGMIR     |     70.28 | particularly |    291,732 | particularly_new           |   0.99 |      333.72 |    410 |    0.81 |            2.48 |   1,365.17 |    5.92 |        13,003 |   0.76 |        12,836 |  1,701,929 |  16.60 |    404 | new            |
    | **NEGany~particularly_original**      | NEGATED    |     18.56 | particularly |  3,173,660 | particularly_original      |   0.85 |      341.44 |    426 |    0.80 |            2.08 |   1,894.60 |    5.86 |       513,668 |   1.29 |        37,594 | 72,839,589 |  18.00 |    360 | original       |
    | **NEGany~that_far-fetched**           | NEGATED    |      2.57 | that         |  3,173,660 | that_far-fetched           |   1.00 |       56.43 |     59 |    0.96 |            3.42 |     369.74 |    5.83 |       208,262 |   1.36 |         5,185 | 72,839,589 |   7.35 |     59 | far-fetched    |
    | **NEGany~that_thrilled**              | NEGATED    |      2.57 | that         |  3,173,660 | that_thrilled              |   1.00 |       56.43 |     59 |    0.96 |            3.42 |     369.74 |    5.83 |       208,262 |   1.36 |        24,182 | 72,839,589 |   7.35 |     59 | thrilled       |
    | **NEGmir~ever_simple**                | NEGMIR     |     35.31 | ever         |    291,732 | ever_simple                |   1.00 |      170.69 |    206 |    0.83 |            3.30 |     726.76 |    5.82 |         5,060 |   0.77 |        25,408 |  1,701,929 |  11.89 |    206 | simple         |
    | **NEGany~immediately_available**      | NEGATED    |  1,278.84 | immediately  |  3,173,660 | immediately_available      |   0.72 |   19,799.16 | 29,351 |    0.67 |            1.75 |  98,046.67 |    5.70 |        96,973 |   1.22 |       666,909 | 72,839,589 | 136.37 | 21,078 | available      |
    | **NEGmir~ever_good**                  | NEGMIR     |     51.94 | ever         |    291,732 | ever_good                  |   0.99 |      247.06 |    303 |    0.82 |            2.51 |   1,013.87 |    5.68 |         5,060 |   0.76 |        31,585 |  1,701,929 |  14.29 |    299 | good           |
    | **NEGany~any_younger**                | NEGATED    |     13.38 | any          |  3,173,660 | any_younger                |   0.83 |      241.62 |    307 |    0.79 |            2.03 |   1,323.36 |    5.57 |        34,382 |   1.28 |        26,216 | 72,839,589 |  15.13 |    255 | younger        |
    | **NEGmir~ever_perfect**               | NEGMIR     |     35.48 | ever         |    291,732 | ever_perfect               |   1.00 |      170.52 |    207 |    0.82 |            2.82 |     714.47 |    5.57 |         5,060 |   0.76 |         3,134 |  1,701,929 |  11.88 |    206 | perfect        |
    | **NEGany~immediately_reachable**      | NEGATED    |      5.23 | immediately  |  3,173,660 | immediately_reachable      |   0.91 |      103.77 |    120 |    0.86 |            2.32 |     610.53 |    5.56 |        96,973 |   1.32 |         2,672 | 72,839,589 |   9.94 |    109 | reachable      |
    | **NEGany~ever_simple**                | NEGATED    |     10.89 | ever         |  3,173,660 | ever_simple                |   0.84 |      200.11 |    250 |    0.80 |            2.07 |   1,109.28 |    5.56 |       114,075 |   1.29 |       396,749 | 72,839,589 |  13.78 |    211 | simple         |
    | **NEGany~particularly_likable**       | NEGATED    |      5.79 | particularly |  3,173,660 | particularly_likable       |   0.89 |      113.21 |    133 |    0.85 |            2.26 |     657.49 |    5.53 |       513,668 |   1.31 |         8,160 | 72,839,589 |  10.38 |    119 | likable        |
    | **NEGany~ever_easy**                  | NEGATED    |     24.18 | ever         |  3,173,660 | ever_easy                  |   0.77 |      404.82 |    555 |    0.73 |            1.87 |   2,105.13 |    5.41 |       114,075 |   1.25 |       579,827 | 72,839,589 |  19.54 |    429 | easy           |
    | **NEGany~immediately_sure**           | NEGATED    |      6.97 | immediately  |  3,173,660 | immediately_sure           |   0.86 |      131.03 |    160 |    0.82 |            2.13 |     738.65 |    5.40 |        96,973 |   1.30 |       262,825 | 72,839,589 |  11.15 |    138 | sure           |
    | **NEGany~terribly_productive**        | NEGATED    |      2.92 | terribly     |  3,173,660 | terribly_productive        |   0.96 |       61.08 |     67 |    0.91 |            2.61 |     376.84 |    5.39 |        58,964 |   1.34 |       102,361 | 72,839,589 |   7.64 |     64 | productive     |
    | **NEGany~inherently_wrong**           | NEGATED    |    100.87 | inherently   |  3,173,660 | inherently_wrong           |   0.71 |    1,538.13 |  2,315 |    0.66 |            1.73 |   7,535.97 |    5.36 |        47,803 |   1.21 |       149,064 | 72,839,589 |  37.99 |  1,639 | wrong          |
    | **NEGany~particularly_likeable**      | NEGATED    |      5.23 | particularly |  3,173,660 | particularly_likeable      |   0.88 |      100.77 |    120 |    0.84 |            2.21 |     579.07 |    5.34 |       513,668 |   1.31 |         5,902 | 72,839,589 |   9.79 |    106 | likeable       |
    | **NEGmir~exactly_sure**               | NEGMIR     |     25.37 | exactly      |    291,732 | exactly_sure               |   1.00 |      122.63 |    148 |    0.83 |            3.16 |     522.11 |    5.31 |         1,041 |   0.77 |         6,761 |  1,701,929 |  10.08 |    148 | sure           |
    | **NEGmir~ever_enough**                | NEGMIR     |     25.20 | ever         |    291,732 | ever_enough                |   1.00 |      121.80 |    147 |    0.83 |            3.15 |     518.58 |    5.30 |         5,060 |   0.77 |         2,596 |  1,701,929 |  10.05 |    147 | enough         |
    | **NEGmir~ever_certain**               | NEGMIR     |     24.51 | ever         |    291,732 | ever_certain               |   1.00 |      118.49 |    143 |    0.83 |            3.14 |     504.47 |    5.26 |         5,060 |   0.77 |         1,800 |  1,701,929 |   9.91 |    143 | certain        |
    | **NEGany~terribly_sure**              | NEGATED    |      3.31 | terribly     |  3,173,660 | terribly_sure              |   0.91 |       65.69 |     76 |    0.86 |            2.31 |     386.31 |    5.08 |        58,964 |   1.32 |       262,825 | 72,839,589 |   7.91 |     69 | sure           |
    | **NEGany~any_easier**                 | NEGATED    |    104.79 | any          |  3,173,660 | any_easier                 |   0.66 |    1,489.21 |  2,405 |    0.62 |            1.64 |   6,987.78 |    5.08 |        34,382 |   1.18 |       209,940 | 72,839,589 |  37.30 |  1,594 | easier         |
    | **NEGany~remotely_surprising**        | NEGATED    |      3.66 | remotely     |  3,173,660 | remotely_surprising        |   0.89 |       71.34 |     84 |    0.85 |            2.24 |     413.61 |    5.07 |        16,426 |   1.31 |        70,540 | 72,839,589 |   8.24 |     75 | surprising     |
    | **NEGmir~particularly_surprising**    | NEGMIR     |     28.80 | particularly |    291,732 | particularly_surprising    |   0.99 |      137.20 |    168 |    0.82 |            2.51 |     564.67 |    5.06 |        13,003 |   0.76 |         2,662 |  1,701,929 |  10.65 |    166 | surprising     |
    | **NEGmir~particularly_wrong**         | NEGMIR     |     37.20 | particularly |    291,732 | particularly_wrong         |   0.98 |      174.80 |    217 |    0.81 |            2.27 |     702.22 |    5.05 |        13,003 |   0.76 |        20,880 |  1,701,929 |  12.01 |    212 | wrong          |
    | **NEGmir~necessarily_wrong**          | NEGMIR     |     37.03 | necessarily  |    291,732 | necessarily_wrong          |   0.98 |      173.97 |    216 |    0.81 |            2.27 |     698.74 |    5.04 |         1,107 |   0.76 |        20,880 |  1,701,929 |  11.98 |    211 | wrong          |
    | **NEGany~any_simpler**                | NEGATED    |     13.07 | any          |  3,173,660 | any_simpler                |   0.75 |      212.93 |    300 |    0.71 |            1.82 |   1,087.71 |    5.00 |        34,382 |   1.24 |        23,480 | 72,839,589 |  14.16 |    226 | simpler        |
    | **NEGany~terribly_reliable**          | NEGATED    |      2.35 | terribly     |  3,173,660 | terribly_reliable          |   0.94 |       48.65 |     54 |    0.90 |            2.51 |     296.70 |    4.99 |        58,964 |   1.34 |        90,598 | 72,839,589 |   6.81 |     51 | reliable       |
    | **NEGany~particularly_forthcoming**   | NEGATED    |      3.62 | particularly |  3,173,660 | particularly_forthcoming   |   0.87 |       68.38 |     83 |    0.82 |            2.14 |     387.25 |    4.85 |       513,668 |   1.30 |         7,473 | 72,839,589 |   8.06 |     72 | forthcoming    |
    | **NEGany~ever_certain**               | NEGATED    |      8.41 | ever         |  3,173,660 | ever_certain               |   0.76 |      138.59 |    193 |    0.72 |            1.84 |     713.34 |    4.80 |       114,075 |   1.24 |        74,952 | 72,839,589 |  11.43 |    147 | certain        |
    | **NEGany~particularly_athletic**      | NEGATED    |      5.93 | particularly |  3,173,660 | particularly_athletic      |   0.79 |      102.07 |    136 |    0.75 |            1.92 |     541.01 |    4.77 |       513,668 |   1.26 |        17,142 | 72,839,589 |   9.82 |    108 | athletic       |
    | **NEGany~any_nicer**                  | NEGATED    |      5.18 | any          |  3,173,660 | any_nicer                  |   0.81 |       90.82 |    119 |    0.76 |            1.95 |     486.82 |    4.75 |        34,382 |   1.27 |         9,955 | 72,839,589 |   9.27 |     96 | nicer          |
    | **NEGany~particularly_surprising**    | NEGATED    |     75.94 | particularly |  3,173,660 | particularly_surprising    |   0.61 |      993.06 |  1,743 |    0.57 |            1.54 |   4,433.52 |    4.71 |       513,668 |   1.15 |        70,540 | 72,839,589 |  30.37 |  1,069 | surprising     |
    | **NEGany~immediately_able**           | NEGATED    |     43.09 | immediately  |  3,173,660 | immediately_able           |   0.63 |      582.91 |    989 |    0.59 |            1.58 |   2,655.18 |    4.70 |        96,973 |   1.16 |       223,196 | 72,839,589 |  23.30 |    626 | able           |
    | **NEGany~inherently_bad**             | NEGATED    |     56.95 | inherently   |  3,173,660 | inherently_bad             |   0.61 |      737.05 |  1,307 |    0.56 |            1.53 |   3,270.68 |    4.62 |        47,803 |   1.14 |       429,537 | 72,839,589 |  26.16 |    794 | bad            |
    | **NEGany~remotely_true**              | NEGATED    |     16.12 | remotely     |  3,173,660 | remotely_true              |   0.68 |      233.88 |    370 |    0.63 |            1.66 |   1,111.13 |    4.61 |        16,426 |   1.19 |       231,639 | 72,839,589 |  14.79 |    250 | true           |
    | **NEGany~immediately_obvious**        | NEGATED    |    173.80 | immediately  |  3,173,660 | immediately_obvious        |   0.56 |    2,064.20 |  3,989 |    0.52 |            1.45 |   8,712.07 |    4.55 |        96,973 |   1.11 |       165,439 | 72,839,589 |  43.63 |  2,238 | obvious        |
    | **NEGany~particularly_revolutionary** | NEGATED    |      4.23 | particularly |  3,173,660 | particularly_revolutionary |   0.79 |       72.77 |     97 |    0.75 |            1.92 |     385.60 |    4.49 |       513,668 |   1.26 |        10,338 | 72,839,589 |   8.29 |     77 | revolutionary  |
    | **NEGany~ever_boring**                | NEGATED    |      3.92 | ever         |  3,173,660 | ever_boring                |   0.80 |       68.08 |     90 |    0.76 |            1.93 |     362.74 |    4.46 |       114,075 |   1.26 |        45,891 | 72,839,589 |   8.02 |     72 | boring         |
    | **NEGmir~any_better**                 | NEGMIR     |     71.82 | any          |    291,732 | any_better                 |   0.91 |      308.18 |    419 |    0.74 |            1.67 |   1,096.01 |    4.38 |         1,197 |   0.72 |        14,013 |  1,701,929 |  15.81 |    380 | better         |
    | **NEGmir~that_simple**                | NEGMIR     |     90.68 | that         |    291,732 | that_simple                |   0.90 |      383.32 |    529 |    0.72 |            1.62 |   1,340.19 |    4.36 |         5,494 |   0.72 |        25,408 |  1,701,929 |  17.61 |    474 | simple         |
    | **NEGany~any_clearer**                | NEGATED    |     26.49 | any          |  3,173,660 | any_clearer                |   0.58 |      328.51 |    608 |    0.54 |            1.49 |   1,421.60 |    4.26 |        34,382 |   1.13 |        11,680 | 72,839,589 |  17.44 |    355 | clearer        |
    | **NEGmir~particularly_remarkable**    | NEGMIR     |     19.03 | particularly |    291,732 | particularly_remarkable    |   0.97 |       88.97 |    111 |    0.80 |            2.18 |     354.53 |    4.24 |        13,003 |   0.75 |         3,238 |  1,701,929 |   8.56 |    108 | remarkable     |
    | **NEGmir~that_easy**                  | NEGMIR     |     87.08 | that         |    291,732 | that_easy                  |   0.89 |      362.92 |    508 |    0.71 |            1.57 |   1,248.84 |    4.23 |         5,494 |   0.71 |        18,610 |  1,701,929 |  17.11 |    450 | easy           |
    | **NEGany~immediately_certain**        | NEGATED    |      4.05 | immediately  |  3,173,660 | immediately_certain        |   0.75 |       65.95 |     93 |    0.71 |            1.82 |     336.68 |    4.19 |        96,973 |   1.24 |        74,952 | 72,839,589 |   7.88 |     70 | certain        |
    | **NEGmir~ever_able**                  | NEGMIR     |     24.51 | ever         |    291,732 | ever_able                  |   0.95 |      111.49 |    143 |    0.78 |            1.94 |     426.52 |    4.17 |         5,060 |   0.74 |         3,704 |  1,701,929 |   9.56 |    136 | able           |
    | **NEGany~remotely_ready**             | NEGATED    |      3.22 | remotely     |  3,173,660 | remotely_ready             |   0.78 |       54.78 |     74 |    0.74 |            1.89 |     287.63 |    4.16 |        16,426 |   1.26 |       141,590 | 72,839,589 |   7.19 |     58 | ready          |
    | **NEGany~remotely_funny**             | NEGATED    |      9.24 | remotely     |  3,173,660 | remotely_funny             |   0.65 |      127.76 |    212 |    0.60 |            1.60 |     589.74 |    4.15 |        16,426 |   1.17 |       122,927 | 72,839,589 |  10.92 |    137 | funny          |
    | **NEGmir~inherently_wrong**           | NEGMIR     |    313.00 | inherently   |    291,732 | inherently_wrong           |   0.83 |    1,200.00 |  1,826 |    0.66 |            1.37 |   3,787.53 |    4.08 |         5,133 |   0.68 |        20,880 |  1,701,929 |  30.85 |  1,513 | wrong          |
    | **NEGany~particularly_flashy**        | NEGATED    |      3.22 | particularly |  3,173,660 | particularly_flashy        |   0.77 |       53.78 |     74 |    0.73 |            1.86 |     278.96 |    4.08 |       513,668 |   1.25 |         4,494 | 72,839,589 |   7.12 |     57 | flashy         |
    | **NEGmir~terribly_surprising**        | NEGMIR     |     11.48 | terribly     |    291,732 | terribly_surprising        |   1.00 |       55.52 |     67 |    0.83 |            2.81 |     236.35 |    4.07 |         4,610 |   0.77 |         2,662 |  1,701,929 |   6.78 |     67 | surprising     |
    | **NEGany~any_cheaper**                | NEGATED    |      8.98 | any          |  3,173,660 | any_cheaper                |   0.63 |      120.02 |    206 |    0.58 |            1.56 |     542.97 |    4.01 |        34,382 |   1.16 |        46,055 | 72,839,589 |  10.57 |    129 | cheaper        |
    | **NEGmir~particularly_close**         | NEGMIR     |     24.85 | particularly |    291,732 | particularly_close         |   0.94 |      111.15 |    145 |    0.77 |            1.84 |     415.70 |    4.01 |        13,003 |   0.74 |        13,874 |  1,701,929 |   9.53 |    136 | close          |
    | **NEGany~any_smarter**                | NEGATED    |      5.75 | any          |  3,173,660 | any_smarter                |   0.67 |       83.25 |    132 |    0.63 |            1.65 |     394.95 |    4.00 |        34,382 |   1.19 |         8,501 | 72,839,589 |   8.82 |     89 | smarter        |
    | **NEGany~any_worse**                  | NEGATED    |    160.03 | any          |  3,173,660 | any_worse                  |   0.46 |    1,525.97 |  3,673 |    0.42 |            1.27 |   5,676.37 |    3.94 |        34,382 |   1.02 |       179,012 | 72,839,589 |  37.16 |  1,686 | worse          |
    | **NEGany~any_brighter**               | NEGATED    |      3.83 | any          |  3,173,660 | any_brighter               |   0.72 |       59.17 |     88 |    0.67 |            1.74 |     292.00 |    3.91 |        34,382 |   1.22 |         9,280 | 72,839,589 |   7.45 |     63 | brighter       |
    | **NEGany~immediately_forthcoming**    | NEGATED    |      9.72 | immediately  |  3,173,660 | immediately_forthcoming    |   0.60 |      123.28 |    223 |    0.55 |            1.51 |     540.70 |    3.89 |        96,973 |   1.14 |         7,473 | 72,839,589 |  10.69 |    133 | forthcoming    |
    | **NEGany~ever_good**                  | NEGATED    |     28.76 | ever         |  3,173,660 | ever_good                  |   0.50 |      302.24 |    660 |    0.46 |            1.34 |   1,188.69 |    3.81 |       114,075 |   1.06 |     1,681,795 | 72,839,589 |  16.61 |    331 | good           |
    | **NEGmir~ever_boring**                | NEGMIR     |      9.77 | ever         |    291,732 | ever_boring                |   1.00 |       47.23 |     57 |    0.83 |            2.75 |     201.07 |    3.80 |         5,060 |   0.77 |         1,961 |  1,701,929 |   6.26 |     57 | boring         |
    | **NEGmir~ever_black**                 | NEGMIR     |      9.60 | ever         |    291,732 | ever_black                 |   1.00 |       46.40 |     56 |    0.83 |            2.74 |     197.54 |    3.77 |         5,060 |   0.77 |         1,412 |  1,701,929 |   6.20 |     56 | black          |
    | **NEGmir~particularly_novel**         | NEGMIR     |      9.26 | particularly |    291,732 | particularly_novel         |   1.00 |       44.74 |     54 |    0.83 |            2.72 |     190.49 |    3.71 |        13,003 |   0.77 |           320 |  1,701,929 |   6.09 |     54 | novel          |
    | **NEGmir~terribly_new**               | NEGMIR     |     12.17 | terribly     |    291,732 | terribly_new               |   0.97 |       56.83 |     71 |    0.80 |            2.13 |     225.93 |    3.66 |         4,610 |   0.75 |        12,836 |  1,701,929 |   6.84 |     69 | new            |
    | **NEGany~remotely_close**             | NEGATED    |     69.58 | remotely     |  3,173,660 | remotely_close             |   0.43 |      624.42 |  1,597 |    0.39 |            1.23 |   2,243.22 |    3.65 |        16,426 |   1.00 |       411,329 | 72,839,589 |  23.70 |    694 | close          |
    | **NEGmir~that_great**                 | NEGMIR     |     58.62 | that         |    291,732 | that_great                 |   0.84 |      227.38 |    342 |    0.66 |            1.39 |     725.16 |    3.57 |         5,494 |   0.69 |         5,568 |  1,701,929 |  13.45 |    286 | great          |
    | **NEGany~ever_enough**                | NEGATED    |     15.12 | ever         |  3,173,660 | ever_enough                |   0.50 |      157.88 |    347 |    0.45 |            1.34 |     618.62 |    3.54 |       114,075 |   1.06 |       152,020 | 72,839,589 |  12.00 |    173 | enough         |
    | **COM~ever_closer**                   | COMPLEMENT |  6,031.92 | ever         | 69,662,736 | ever_closer                |   1.00 |      273.08 |  6,307 |    0.04 |            2.06 |     538.66 |    3.51 |       114,075 |   0.02 |        61,475 | 72,839,589 |   3.44 |  6,305 | closer         |
    | **NEGany~inherently_illegal**         | NEGATED    |      4.01 | inherently   |  3,173,660 | inherently_illegal         |   0.64 |       54.99 |     92 |    0.60 |            1.59 |     252.59 |    3.51 |        47,803 |   1.17 |        30,194 | 72,839,589 |   7.16 |     59 | illegal        |
    | **NEGmir~terribly_original**          | NEGMIR     |      7.71 | terribly     |    291,732 | terribly_original          |   1.00 |       37.29 |     45 |    0.83 |            2.64 |     158.74 |    3.40 |         4,610 |   0.77 |         1,555 |  1,701,929 |   5.56 |     45 | original       |
    | **NEGmir~exactly_clear**              | NEGMIR     |      9.08 | exactly      |    291,732 | exactly_clear              |   0.98 |       42.92 |     53 |    0.81 |            2.23 |     173.89 |    3.38 |         1,041 |   0.76 |         6,722 |  1,701,929 |   5.95 |     52 | clear          |
    | **NEGmir~particularly_comfortable**   | NEGMIR     |      7.54 | particularly |    291,732 | particularly_comfortable   |   1.00 |       36.46 |     44 |    0.83 |            2.63 |     155.21 |    3.36 |        13,003 |   0.77 |         4,642 |  1,701,929 |   5.50 |     44 | comfortable    |
    | **NEGany~ever_perfect**               | NEGATED    |     21.31 | ever         |  3,173,660 | ever_perfect               |   0.44 |      194.69 |    489 |    0.40 |            1.24 |     706.71 |    3.34 |       114,075 |   1.01 |       104,659 | 72,839,589 |  13.25 |    216 | perfect        |
    | **NEGany~ever_sure**                  | NEGATED    |      7.06 | ever         |  3,173,660 | ever_sure                  |   0.54 |       79.94 |    162 |    0.49 |            1.41 |     328.20 |    3.34 |       114,075 |   1.09 |       262,825 | 72,839,589 |   8.57 |     87 | sure           |
    | **NEGmir~remotely_close**             | NEGMIR     |     45.77 | remotely     |    291,732 | remotely_close             |   0.82 |      172.23 |    267 |    0.65 |            1.33 |     532.96 |    3.28 |         2,341 |   0.68 |        13,874 |  1,701,929 |  11.67 |    218 | close          |
    | **NEGmir~any_different**              | NEGMIR     |      8.40 | any          |    291,732 | any_different              |   0.98 |       39.60 |     49 |    0.81 |            2.19 |     159.93 |    3.24 |         1,197 |   0.76 |        36,166 |  1,701,929 |   5.72 |     48 | different      |
    | **NEGany~immediately_intuitive**      | NEGATED    |      3.96 | immediately  |  3,173,660 | immediately_intuitive      |   0.59 |       50.04 |     91 |    0.55 |            1.50 |     218.74 |    3.21 |        96,973 |   1.13 |        20,664 | 72,839,589 |   6.81 |     54 | intuitive      |
    | **NEGmir~that_big**                   | NEGMIR     |     22.46 | that         |    291,732 | that_big                   |   0.86 |       90.54 |    131 |    0.69 |            1.47 |     300.54 |    3.17 |         5,494 |   0.70 |         8,177 |  1,701,929 |   8.52 |    113 | big            |
    | **NEGmir~that_popular**               | NEGMIR     |     12.00 | that         |    291,732 | that_popular               |   0.93 |       53.00 |     70 |    0.76 |            1.76 |     195.15 |    3.15 |         5,494 |   0.73 |         5,668 |  1,701,929 |   6.57 |     65 | popular        |
    | **NEGmir~ever_sick**                  | NEGMIR     |      6.69 | ever         |    291,732 | ever_sick                  |   1.00 |       32.31 |     39 |    0.83 |            2.58 |     137.57 |    3.15 |         5,060 |   0.77 |         1,895 |  1,701,929 |   5.17 |     39 | sick           |
    | **NEGmir~particularly_revolutionary** | NEGMIR     |      6.69 | particularly |    291,732 | particularly_revolutionary |   1.00 |       32.31 |     39 |    0.83 |            2.58 |     137.57 |    3.15 |        13,003 |   0.77 |           485 |  1,701,929 |   5.17 |     39 | revolutionary  |
    | **NEGany~remotely_qualified**         | NEGATED    |      4.40 | remotely     |  3,173,660 | remotely_qualified         |   0.56 |       52.60 |    101 |    0.52 |            1.45 |     222.79 |    3.13 |        16,426 |   1.11 |        74,643 | 72,839,589 |   6.97 |     57 | qualified      |
    | **NEGmir~remotely_true**              | NEGMIR     |     11.31 | remotely     |    291,732 | remotely_true              |   0.92 |       49.69 |     66 |    0.75 |            1.73 |     181.65 |    3.04 |         2,341 |   0.73 |         6,191 |  1,701,929 |   6.36 |     61 | true           |
    | **NEGmir~any_easier**                 | NEGMIR     |     11.31 | any          |    291,732 | any_easier                 |   0.92 |       49.69 |     66 |    0.75 |            1.73 |     181.65 |    3.04 |         1,197 |   0.73 |         2,386 |  1,701,929 |   6.36 |     61 | easier         |
    | **NEGany~remotely_comparable**        | NEGATED    |     12.07 | remotely     |  3,173,660 | remotely_comparable        |   0.43 |      105.93 |    277 |    0.38 |            1.21 |     375.73 |    2.98 |        16,426 |   0.99 |        12,252 | 72,839,589 |   9.75 |    118 | comparable     |
    | **NEGmir~necessarily_bad**            | NEGMIR     |      9.08 | necessarily  |    291,732 | necessarily_bad            |   0.94 |       40.92 |     53 |    0.77 |            1.84 |     154.45 |    2.95 |         1,107 |   0.74 |        10,261 |  1,701,929 |   5.79 |     50 | bad            |
    | **NEGmir~inherently_bad**             | NEGMIR     |     32.23 | inherently   |    291,732 | inherently_bad             |   0.79 |      115.77 |    188 |    0.62 |            1.25 |     342.53 |    2.86 |         5,133 |   0.66 |        10,261 |  1,701,929 |   9.52 |    148 | bad            |
    | **NEGany~inherently_evil**            | NEGATED    |     48.93 | inherently   |  3,173,660 | inherently_evil            |   0.32 |      309.07 |  1,123 |    0.28 |            1.01 |     905.80 |    2.81 |        47,803 |   0.86 |        22,706 | 72,839,589 |  16.33 |    358 | evil           |
    | **NEGany~remotely_interested**        | NEGATED    |     46.27 | remotely     |  3,173,660 | remotely_interested        |   0.31 |      283.73 |  1,062 |    0.27 |            1.00 |     817.06 |    2.74 |        16,426 |   0.85 |       264,528 | 72,839,589 |  15.62 |    330 | interested     |
    | **NEGmir~any_worse**                  | NEGMIR     |     18.00 | any          |    291,732 | any_worse                  |   0.83 |       69.00 |    105 |    0.66 |            1.36 |     217.46 |    2.73 |         1,197 |   0.68 |         8,790 |  1,701,929 |   7.40 |     87 | worse          |
    | **NEGmir~particularly_radical**       | NEGMIR     |      5.31 | particularly |    291,732 | particularly_radical       |   1.00 |       25.69 |     31 |    0.83 |            2.48 |     109.35 |    2.73 |        13,003 |   0.77 |         1,072 |  1,701,929 |   4.61 |     31 | radical        |
    | **NEGmir~that_keen**                  | NEGMIR     |      5.31 | that         |    291,732 | that_keen                  |   1.00 |       25.69 |     31 |    0.83 |            2.48 |     109.35 |    2.73 |         5,494 |   0.77 |         1,360 |  1,701,929 |   4.61 |     31 | keen           |
    | **NEGmir~any_bigger**                 | NEGMIR     |      6.34 | any          |    291,732 | any_bigger                 |   0.97 |       29.66 |     37 |    0.80 |            2.07 |     118.17 |    2.73 |         1,197 |   0.75 |         3,923 |  1,701,929 |   4.94 |     36 | bigger         |
    | **NEGmir~remotely_comparable**        | NEGMIR     |      8.06 | remotely     |    291,732 | remotely_comparable        |   0.94 |       35.94 |     47 |    0.76 |            1.79 |     134.02 |    2.72 |         2,341 |   0.74 |           283 |  1,701,929 |   5.42 |     44 | comparable     |
    | **NEGmir~necessarily_true**           | NEGMIR     |     10.11 | necessarily  |    291,732 | necessarily_true           |   0.90 |       42.89 |     59 |    0.73 |            1.60 |     150.42 |    2.69 |         1,107 |   0.72 |         6,191 |  1,701,929 |   5.89 |     53 | true           |
    | **NEGany~ever_satisfied**             | NEGATED    |      6.58 | ever         |  3,173,660 | ever_satisfied             |   0.42 |       57.42 |    151 |    0.38 |            1.21 |     203.01 |    2.57 |       114,075 |   0.99 |        62,862 | 72,839,589 |   7.18 |     64 | satisfied      |
    | **NEGmir~yet_available**              | NEGMIR     |      4.80 | yet          |    291,732 | yet_available              |   1.00 |       23.20 |     28 |    0.83 |            2.44 |      98.77 |    2.54 |           815 |   0.77 |        10,284 |  1,701,929 |   4.38 |     28 | available      |
    | **NEGany~inherently_negative**        | NEGATED    |      8.41 | inherently   |  3,173,660 | inherently_negative        |   0.39 |       66.59 |    193 |    0.35 |            1.15 |     222.63 |    2.50 |        47,803 |   0.95 |        53,385 | 72,839,589 |   7.69 |     75 | negative       |
    | **NEGmir~terribly_interesting**       | NEGMIR     |     11.31 | terribly     |    291,732 | terribly_interesting       |   0.85 |       44.69 |     66 |    0.68 |            1.42 |     145.16 |    2.44 |         4,610 |   0.69 |        12,447 |  1,701,929 |   5.97 |     56 | interesting    |
    | **NEGmir~particularly_fast**          | NEGMIR     |      4.46 | particularly |    291,732 | particularly_fast          |   1.00 |       21.54 |     26 |    0.83 |            2.41 |      91.71 |    2.39 |        13,003 |   0.77 |         1,259 |  1,701,929 |   4.22 |     26 | fast           |
    | **NEGmir~terribly_interested**        | NEGMIR     |      7.37 | terribly     |    291,732 | terribly_interested        |   0.91 |       31.63 |     43 |    0.74 |            1.63 |     112.46 |    2.36 |         4,610 |   0.72 |         8,255 |  1,701,929 |   5.06 |     39 | interested     |
    | **NEGmir~any_closer**                 | NEGMIR     |     11.83 | any          |    291,732 | any_closer                 |   0.83 |       45.17 |     69 |    0.65 |            1.35 |     141.82 |    2.33 |         1,197 |   0.68 |           993 |  1,701,929 |   5.98 |     57 | closer         |
    | **NEGmir~exactly_new**                | NEGMIR     |      5.14 | exactly      |    291,732 | exactly_new                |   0.97 |       23.86 |     30 |    0.80 |            1.98 |      93.90 |    2.31 |         1,041 |   0.75 |        12,836 |  1,701,929 |   4.43 |     29 | new            |
    | **NEGmir~terribly_unusual**           | NEGMIR     |      4.11 | terribly     |    291,732 | terribly_unusual           |   1.00 |       19.89 |     24 |    0.83 |            2.37 |      84.66 |    2.23 |         4,610 |   0.77 |         2,302 |  1,701,929 |   4.06 |     24 | unusual        |
    | **NEGmir~terribly_special**           | NEGMIR     |      4.11 | terribly     |    291,732 | terribly_special           |   1.00 |       19.89 |     24 |    0.83 |            2.37 |      84.66 |    2.23 |         4,610 |   0.77 |        15,541 |  1,701,929 |   4.06 |     24 | special        |
    | **NEGany~inherently_good**            | NEGATED    |     51.28 | inherently   |  3,173,660 | inherently_good            |   0.24 |      231.72 |  1,177 |    0.20 |            0.84 |     554.72 |    2.21 |        47,803 |   0.74 |     1,681,795 | 72,839,589 |  13.77 |    283 | good           |
    | **NEGany~remotely_similar**           | NEGATED    |     24.36 | remotely     |  3,173,660 | remotely_similar           |   0.27 |      127.64 |    559 |    0.23 |            0.91 |     334.61 |    2.20 |        16,426 |   0.80 |       203,453 | 72,839,589 |  10.35 |    152 | similar        |
    | **NEGmir~necessarily_right**          | NEGMIR     |      3.94 | necessarily  |    291,732 | necessarily_right          |   1.00 |       19.06 |     23 |    0.83 |            2.36 |      81.13 |    2.15 |         1,107 |   0.77 |         5,576 |  1,701,929 |   3.97 |     23 | right          |
    | **NEGmir~that_impressive**            | NEGMIR     |      3.94 | that         |    291,732 | that_impressive            |   1.00 |       19.06 |     23 |    0.83 |            2.36 |      81.13 |    2.15 |         5,494 |   0.77 |         5,007 |  1,701,929 |   3.97 |     23 | impressive     |
    | **NEGmir~any_good**                   | NEGMIR     |      6.00 | any          |    291,732 | any_good                   |   0.91 |       26.00 |     35 |    0.74 |            1.65 |      93.53 |    2.12 |         1,197 |   0.73 |        31,585 |  1,701,929 |   4.60 |     32 | good           |
    | **NEGany~remotely_accurate**          | NEGATED    |      5.84 | remotely     |  3,173,660 | remotely_accurate          |   0.37 |       44.16 |    134 |    0.33 |            1.12 |     143.78 |    2.10 |        16,426 |   0.93 |       152,299 | 72,839,589 |   6.25 |     50 | accurate       |
    | **NEGmir~inherently_illegal**         | NEGMIR     |      4.63 | inherently   |    291,732 | inherently_illegal         |   0.96 |       21.37 |     27 |    0.79 |            1.93 |      83.54 |    2.10 |         5,133 |   0.75 |           937 |  1,701,929 |   4.19 |     26 | illegal        |
    | **NEGmir~remotely_believable**        | NEGMIR     |      3.60 | remotely     |    291,732 | remotely_believable        |   1.00 |       17.40 |     21 |    0.83 |            2.32 |      74.08 |    1.96 |         2,341 |   0.77 |           600 |  1,701,929 |   3.80 |     21 | believable     |
    | **NEGmir~yet_certain**                | NEGMIR     |      3.60 | yet          |    291,732 | yet_certain                |   1.00 |       17.40 |     21 |    0.83 |            2.32 |      74.08 |    1.96 |           815 |   0.77 |         1,800 |  1,701,929 |   3.80 |     21 | certain        |
    | **NEGmir~any_younger**                | NEGMIR     |      3.43 | any          |    291,732 | any_younger                |   1.00 |       16.57 |     20 |    0.83 |            2.30 |      70.55 |    1.86 |         1,197 |   0.77 |           939 |  1,701,929 |   3.71 |     20 | younger        |
    | **NEGmir~exactly_easy**               | NEGMIR     |      3.43 | exactly      |    291,732 | exactly_easy               |   1.00 |       16.57 |     20 |    0.83 |            2.30 |      70.55 |    1.86 |         1,041 |   0.77 |        18,610 |  1,701,929 |   3.71 |     20 | easy           |
    | **NEGmir~remotely_funny**             | NEGMIR     |      8.74 | remotely     |    291,732 | remotely_funny             |   0.80 |       32.26 |     51 |    0.63 |            1.28 |      97.91 |    1.85 |         2,341 |   0.67 |         5,365 |  1,701,929 |   5.04 |     41 | funny          |
    | **NEGmir~immediately_available**      | NEGMIR     |     47.14 | immediately  |    291,732 | immediately_available      |   0.59 |      114.86 |    275 |    0.42 |            0.84 |     241.53 |    1.85 |         1,195 |   0.54 |        10,284 |  1,701,929 |   9.02 |    162 | available      |
    | **NEGmir~that_fond**                  | NEGMIR     |      4.11 | that         |    291,732 | that_fond                  |   0.96 |       18.89 |     24 |    0.79 |            1.88 |      73.19 |    1.84 |         5,494 |   0.75 |         1,115 |  1,701,929 |   3.94 |     23 | fond           |
    | **NEGmir~that_comfortable**           | NEGMIR     |      4.11 | that         |    291,732 | that_comfortable           |   0.96 |       18.89 |     24 |    0.79 |            1.88 |      73.19 |    1.84 |         5,494 |   0.75 |         4,642 |  1,701,929 |   3.94 |     23 | comfortable    |
    | **NEGmir~necessarily_new**            | NEGMIR     |      4.11 | necessarily  |    291,732 | necessarily_new            |   0.96 |       18.89 |     24 |    0.79 |            1.88 |      73.19 |    1.84 |         1,107 |   0.75 |        12,836 |  1,701,929 |   3.94 |     23 | new            |
    | **NEGmir~remotely_interesting**       | NEGMIR     |     13.20 | remotely     |    291,732 | remotely_interesting       |   0.73 |       42.80 |     77 |    0.56 |            1.10 |     115.20 |    1.80 |         2,341 |   0.63 |        12,447 |  1,701,929 |   5.72 |     56 | interesting    |
    | **NEGmir~terribly_popular**           | NEGMIR     |      3.26 | terribly     |    291,732 | terribly_popular           |   1.00 |       15.74 |     19 |    0.83 |            2.28 |      67.02 |    1.75 |         4,610 |   0.77 |         5,668 |  1,701,929 |   3.61 |     19 | popular        |
    | **NEGmir~yet_clear**                  | NEGMIR     |      3.26 | yet          |    291,732 | yet_clear                  |   1.00 |       15.74 |     19 |    0.83 |            2.28 |      67.02 |    1.75 |           815 |   0.77 |         6,722 |  1,701,929 |   3.61 |     19 | clear          |
    | **NEGmir~yet_sure**                   | NEGMIR     |      3.26 | yet          |    291,732 | yet_sure                   |   1.00 |       15.74 |     19 |    0.83 |            2.28 |      67.02 |    1.75 |           815 |   0.77 |         6,761 |  1,701,929 |   3.61 |     19 | sure           |
    | **NEGmir~remotely_similar**           | NEGMIR     |     18.34 | remotely     |    291,732 | remotely_similar           |   0.66 |       52.66 |    107 |    0.49 |            0.98 |     127.32 |    1.70 |         2,341 |   0.59 |         7,011 |  1,701,929 |   6.25 |     71 | similar        |
    | **NEGmir~inherently_better**          | NEGMIR     |     10.11 | inherently   |    291,732 | inherently_better          |   0.75 |       33.89 |     59 |    0.57 |            1.14 |      93.95 |    1.65 |         5,133 |   0.64 |        14,013 |  1,701,929 |   5.11 |     44 | better         |
    | **NEGmir~necessarily_better**         | NEGMIR     |      5.31 | necessarily  |    291,732 | necessarily_better         |   0.87 |       21.69 |     31 |    0.70 |            1.47 |      72.90 |    1.63 |         1,107 |   0.71 |        14,013 |  1,701,929 |   4.17 |     27 | better         |
    | **NEGmir~inherently_improper**        | NEGMIR     |      3.09 | inherently   |    291,732 | inherently_improper        |   1.00 |       14.91 |     18 |    0.83 |            2.25 |      63.49 |    1.63 |         5,133 |   0.77 |           142 |  1,701,929 |   3.52 |     18 | improper       |
    | **NEGmir~yet_ready**                  | NEGMIR     |      3.09 | yet          |    291,732 | yet_ready                  |   1.00 |       14.91 |     18 |    0.83 |            2.25 |      63.49 |    1.63 |           815 |   0.77 |         3,034 |  1,701,929 |   3.52 |     18 | ready          |
    | **NEGmir~any_clearer**                | NEGMIR     |      2.91 | any          |    291,732 | any_clearer                |   1.00 |       14.09 |     17 |    0.83 |            2.23 |      59.97 |    1.50 |         1,197 |   0.77 |           130 |  1,701,929 |   3.42 |     17 | clearer        |
    | **NEGmir~remotely_surprising**        | NEGMIR     |      2.91 | remotely     |    291,732 | remotely_surprising        |   1.00 |       14.09 |     17 |    0.83 |            2.23 |      59.97 |    1.50 |         2,341 |   0.77 |         2,662 |  1,701,929 |   3.42 |     17 | surprising     |
    | **NEGmir~any_higher**                 | NEGMIR     |      3.94 | any          |    291,732 | any_higher                 |   0.91 |       17.06 |     23 |    0.74 |            1.62 |      61.24 |    1.42 |         1,197 |   0.73 |         2,893 |  1,701,929 |   3.72 |     21 | higher         |
    | **NEGmir~remotely_possible**          | NEGMIR     |      8.91 | remotely     |    291,732 | remotely_possible          |   0.73 |       29.09 |     52 |    0.56 |            1.11 |      78.73 |    1.42 |         2,341 |   0.63 |         3,160 |  1,701,929 |   4.72 |     38 | possible       |
    | **NEGmir~that_clear**                 | NEGMIR     |      3.26 | that         |    291,732 | that_clear                 |   0.95 |       14.74 |     19 |    0.78 |            1.78 |      56.03 |    1.30 |         5,494 |   0.74 |         6,722 |  1,701,929 |   3.47 |     18 | clear          |
    | **NEGmir~necessarily_illegal**        | NEGMIR     |      2.57 | necessarily  |    291,732 | necessarily_illegal        |   1.00 |       12.43 |     15 |    0.83 |            2.18 |      52.91 |    1.20 |         1,107 |   0.77 |           937 |  1,701,929 |   3.21 |     15 | illegal        |
    | **NEGmir~terribly_clear**             | NEGMIR     |      2.57 | terribly     |    291,732 | terribly_clear             |   1.00 |       12.43 |     15 |    0.83 |            2.18 |      52.91 |    1.20 |         4,610 |   0.77 |         6,722 |  1,701,929 |   3.21 |     15 | clear          |
    | **NEGmir~inherently_evil**            | NEGMIR     |     16.97 | inherently   |    291,732 | inherently_evil            |   0.59 |       41.03 |     99 |    0.41 |            0.83 |      85.70 |    1.18 |         5,133 |   0.53 |         1,271 |  1,701,929 |   5.39 |     58 | evil           |
    | **NEGany~inherently_problematic**     | NEGATED    |     12.07 | inherently   |  3,173,660 | inherently_problematic     |   0.21 |       45.93 |    277 |    0.17 |            0.77 |      98.70 |    1.17 |        47,803 |   0.68 |        33,408 | 72,839,589 |   6.03 |     58 | problematic    |
    | **NEGmir~immediately_clear**          | NEGMIR     |      7.37 | immediately  |    291,732 | immediately_clear          |   0.72 |       23.63 |     43 |    0.55 |            1.09 |      62.95 |    1.13 |         1,195 |   0.62 |         6,722 |  1,701,929 |   4.24 |     31 | clear          |
    | **NEGmir~terribly_remarkable**        | NEGMIR     |      2.40 | terribly     |    291,732 | terribly_remarkable        |   1.00 |       11.60 |     14 |    0.83 |            2.15 |      49.38 |    1.03 |         4,610 |   0.77 |         3,238 |  1,701,929 |   3.10 |     14 | remarkable     |
    | **NEGmir~remotely_new**               | NEGMIR     |      3.77 | remotely     |    291,732 | remotely_new               |   0.86 |       15.23 |     22 |    0.69 |            1.43 |      50.62 |    1.00 |         2,341 |   0.70 |        12,836 |  1,701,929 |   3.49 |     19 | new            |
    



|                                       | `l1`       |   `exp_f` | `adv`        |       `f1` | `l2`                       |   `P1` |   `unexp_f` |   `f2` |   `dP1` |   `odds_r_disc` |       `G2` |   `LRC` |   `adv_total` |   `MI` |   `adj_total` |        `N` |    `t` |    `f` | `adj`          |
|:--------------------------------------|:-----------|----------:|:-------------|-----------:|:---------------------------|-------:|------------:|-------:|--------:|----------------:|-----------:|--------:|--------------:|-------:|--------------:|-----------:|-------:|-------:|:---------------|
| **NEGany~yet_clear**                  | NEGATED    |    456.44 | yet          |  3,173,660 | yet_clear                  |   0.99 |    9,949.56 | 10,476 |    0.95 |            3.51 |  64,409.97 |   10.77 |        95,763 |   1.36 |       349,214 | 72,839,589 |  97.54 | 10,406 | clear          |
| **NEGany~yet_ready**                  | NEGATED    |    331.09 | yet          |  3,173,660 | yet_ready                  |   0.99 |    7,169.91 |  7,599 |    0.94 |            3.22 |  45,985.07 |    9.93 |        95,763 |   1.36 |       141,590 | 72,839,589 |  82.79 |  7,501 | ready          |
| **NEGany~necessarily_indicative**     | NEGATED    |     61.00 | necessarily  |  3,173,660 | necessarily_indicative     |   0.99 |    1,328.00 |  1,400 |    0.95 |            3.42 |   8,577.54 |    9.43 |        48,947 |   1.36 |         8,148 | 72,839,589 |  35.63 |  1,389 | indicative     |
| **NEGany~that_uncommon**              | NEGATED    |     35.03 | that         |  3,173,660 | that_uncommon              |   1.00 |      766.97 |    804 |    0.95 |            3.85 |   4,998.32 |    9.43 |       208,262 |   1.36 |        11,312 | 72,839,589 |  27.08 |    802 | uncommon       |
| **NEGany~exactly_easy**               | NEGATED    |     46.75 | exactly      |  3,173,660 | exactly_easy               |   0.99 |    1,019.25 |  1,073 |    0.95 |            3.49 |   6,596.91 |    9.32 |        58,643 |   1.36 |       579,827 | 72,839,589 |  31.22 |  1,066 | easy           |
| **NEGany~yet_complete**               | NEGATED    |     96.20 | yet          |  3,173,660 | yet_complete               |   0.98 |    2,077.80 |  2,208 |    0.94 |            3.14 |  13,277.09 |    9.20 |        95,763 |   1.35 |        86,361 | 72,839,589 |  44.56 |  2,174 | complete       |
| **NEGany~that_surprising**            | NEGATED    |     49.80 | that         |  3,173,660 | that_surprising            |   0.99 |    1,083.20 |  1,143 |    0.95 |            3.37 |   6,986.81 |    9.20 |       208,262 |   1.36 |        70,540 | 72,839,589 |  32.18 |  1,133 | surprising     |
| **NEGany~exactly_new**                | NEGATED    |     60.48 | exactly      |  3,173,660 | exactly_new                |   0.99 |    1,310.52 |  1,388 |    0.94 |            3.24 |   8,410.32 |    9.10 |        58,643 |   1.36 |       253,862 | 72,839,589 |  35.39 |  1,371 | new            |
| **NEGany~necessarily_easy**           | NEGATED    |     39.95 | necessarily  |  3,173,660 | necessarily_easy           |   0.99 |      869.05 |    917 |    0.95 |            3.37 |   5,605.64 |    9.01 |        48,947 |   1.36 |       579,827 | 72,839,589 |  28.82 |    909 | easy           |
| **NEGany~yet_final**                  | NEGATED    |     28.02 | yet          |  3,173,660 | yet_final                  |   1.00 |      611.98 |    643 |    0.95 |            3.60 |   3,972.92 |    8.97 |        95,763 |   1.36 |         5,860 | 72,839,589 |  24.19 |    640 | final          |
| **NEGany~exactly_cheap**              | NEGATED    |     30.28 | exactly      |  3,173,660 | exactly_cheap              |   0.99 |      660.72 |    695 |    0.95 |            3.53 |   4,281.59 |    8.96 |        58,643 |   1.36 |        60,531 | 72,839,589 |  25.13 |    691 | cheap          |
| **NEGany~yet_eligible**               | NEGATED    |     19.52 | yet          |  3,173,660 | yet_eligible               |   1.00 |      428.48 |    448 |    0.96 |            4.29 |   2,807.56 |    8.96 |        95,763 |   1.36 |        23,252 | 72,839,589 |  20.24 |    448 | eligible       |
| **NEGany~that_unusual**               | NEGATED    |     43.05 | that         |  3,173,660 | that_unusual               |   0.99 |      933.95 |    988 |    0.95 |            3.27 |   6,003.05 |    8.92 |       208,262 |   1.36 |        71,234 | 72,839,589 |  29.88 |    977 | unusual        |
| **NEGany~exactly_clear**              | NEGATED    |     77.73 | exactly      |  3,173,660 | exactly_clear              |   0.98 |    1,668.27 |  1,784 |    0.94 |            3.00 |  10,578.33 |    8.78 |        58,643 |   1.35 |       349,214 | 72,839,589 |  39.92 |  1,746 | clear          |
| **NEGany~exactly_surprising**         | NEGATED    |     19.21 | exactly      |  3,173,660 | exactly_surprising         |   1.00 |      420.79 |    441 |    0.95 |            3.81 |   2,743.34 |    8.71 |        58,643 |   1.36 |        70,540 | 72,839,589 |  20.06 |    440 | surprising     |
| **NEGany~that_complicated**           | NEGATED    |     53.59 | that         |  3,173,660 | that_complicated           |   0.98 |    1,153.41 |  1,230 |    0.94 |            3.05 |   7,337.84 |    8.68 |       208,262 |   1.35 |       159,822 | 72,839,589 |  33.20 |  1,207 | complicated    |
| **NEGany~terribly_surprising**        | NEGATED    |     42.00 | terribly     |  3,173,660 | terribly_surprising        |   0.98 |      907.00 |    964 |    0.94 |            3.13 |   5,794.10 |    8.66 |        58,964 |   1.35 |        70,540 | 72,839,589 |  29.44 |    949 | surprising     |
| **NEGany~yet_official**               | NEGATED    |     15.34 | yet          |  3,173,660 | yet_official               |   1.00 |      336.66 |    352 |    0.96 |            4.19 |   2,205.93 |    8.61 |        95,763 |   1.36 |         6,853 | 72,839,589 |  17.94 |    352 | official       |
| **NEGany~that_hard**                  | NEGATED    |    452.26 | that         |  3,173,660 | that_hard                  |   0.96 |    9,495.74 | 10,380 |    0.91 |            2.70 |  58,817.24 |    8.59 |       208,262 |   1.34 |       348,463 | 72,839,589 |  95.21 |  9,948 | hard           |
| **NEGany~that_familiar**              | NEGATED    |     50.37 | that         |  3,173,660 | that_familiar              |   0.97 |    1,075.63 |  1,156 |    0.93 |            2.91 |   6,781.11 |    8.35 |       208,262 |   1.35 |       156,296 | 72,839,589 |  32.05 |  1,126 | familiar       |
| **NEGany~necessarily_representative** | NEGATED    |     21.44 | necessarily  |  3,173,660 | necessarily_representative |   0.99 |      465.56 |    492 |    0.95 |            3.29 |   2,996.58 |    8.34 |        48,947 |   1.36 |        18,355 | 72,839,589 |  21.10 |    487 | representative |
| **NEGany~necessarily_surprising**     | NEGATED    |     14.86 | necessarily  |  3,173,660 | necessarily_surprising     |   1.00 |      325.14 |    341 |    0.95 |            3.70 |   2,117.16 |    8.33 |        48,947 |   1.36 |        70,540 | 72,839,589 |  17.63 |    340 | surprising     |
| **NEGany~immediately_clear**          | NEGATED    |  1,134.49 | immediately  |  3,173,660 | immediately_clear          |   0.94 |   23,281.51 | 26,038 |    0.89 |            2.52 | 141,186.69 |    8.16 |        96,973 |   1.33 |       349,214 | 72,839,589 | 149.00 | 24,416 | clear          |
| **NEGany~necessarily_new**            | NEGATED    |     21.44 | necessarily  |  3,173,660 | necessarily_new            |   0.98 |      460.56 |    492 |    0.94 |            3.00 |   2,923.82 |    7.94 |        48,947 |   1.35 |       253,862 | 72,839,589 |  20.98 |    482 | new            |
| **NEGany~that_dissimilar**            | NEGATED    |     13.38 | that         |  3,173,660 | that_dissimilar            |   0.99 |      290.62 |    307 |    0.95 |            3.28 |   1,871.65 |    7.86 |       208,262 |   1.36 |         4,605 | 72,839,589 |  16.67 |    304 | dissimilar     |
| **NEGany~exactly_conducive**          | NEGATED    |      9.06 | exactly      |  3,173,660 | exactly_conducive          |   1.00 |      198.94 |    208 |    0.96 |            3.96 |   1,303.50 |    7.82 |        58,643 |   1.36 |         9,110 | 72,839,589 |  13.79 |    208 | conducive      |
| **NEGany~that_noticeable**            | NEGATED    |     11.63 | that         |  3,173,660 | that_noticeable            |   0.99 |      252.37 |    267 |    0.95 |            3.22 |   1,621.81 |    7.65 |       208,262 |   1.36 |        31,467 | 72,839,589 |  15.53 |    264 | noticeable     |
| **NEGany~immediately_possible**       | NEGATED    |     45.92 | immediately  |  3,173,660 | immediately_possible       |   0.95 |      954.08 |  1,054 |    0.91 |            2.61 |   5,845.77 |    7.62 |        96,973 |   1.34 |       245,272 | 72,839,589 |  30.17 |  1,000 | possible       |
| **NEGany~yet_convinced**              | NEGATED    |      7.36 | yet          |  3,173,660 | yet_convinced              |   1.00 |      161.64 |    169 |    0.96 |            3.87 |   1,059.09 |    7.50 |        95,763 |   1.36 |        12,132 | 72,839,589 |  12.43 |    169 | convinced      |
| **NEGany~exactly_shocking**           | NEGATED    |      6.58 | exactly      |  3,173,660 | exactly_shocking           |   1.00 |      144.42 |    151 |    0.96 |            3.82 |     946.29 |    7.33 |        58,643 |   1.36 |        35,115 | 72,839,589 |  11.75 |    151 | shocking       |
| **NEGany~exactly_pleasant**           | NEGATED    |      6.19 | exactly      |  3,173,660 | exactly_pleasant           |   1.00 |      135.81 |    142 |    0.96 |            3.80 |     889.88 |    7.24 |        58,643 |   1.36 |        52,223 | 72,839,589 |  11.40 |    142 | pleasant       |
| **NEGany~yet_over**                   | NEGATED    |      7.10 | yet          |  3,173,660 | yet_over                   |   0.99 |      154.90 |    163 |    0.95 |            3.38 |   1,003.13 |    7.21 |        95,763 |   1.36 |         3,983 | 72,839,589 |  12.17 |    162 | over           |
| **NEGany~exactly_famous**             | NEGATED    |      5.66 | exactly      |  3,173,660 | exactly_famous             |   1.00 |      124.34 |    130 |    0.96 |            3.76 |     814.68 |    7.10 |        58,643 |   1.36 |       223,813 | 72,839,589 |  10.90 |    130 | famous         |
| **NEGany~exactly_difficult**          | NEGATED    |      5.49 | exactly      |  3,173,660 | exactly_difficult          |   1.00 |      120.51 |    126 |    0.96 |            3.74 |     789.62 |    7.05 |        58,643 |   1.36 |       732,106 | 72,839,589 |  10.74 |    126 | difficult      |
| **NEGany~necessarily_useful**         | NEGATED    |      4.53 | necessarily  |  3,173,660 | necessarily_useful         |   1.00 |       99.47 |    104 |    0.96 |            3.66 |     651.75 |    6.75 |        48,947 |   1.36 |       227,709 | 72,839,589 |   9.75 |    104 | useful         |
| **NEGany~yet_online**                 | NEGATED    |      4.27 | yet          |  3,173,660 | yet_online                 |   1.00 |       93.73 |     98 |    0.96 |            3.64 |     614.14 |    6.66 |        95,763 |   1.36 |        15,650 | 72,839,589 |   9.47 |     98 | online         |
| **NEGany~necessarily_fun**            | NEGATED    |      4.18 | necessarily  |  3,173,660 | necessarily_fun            |   1.00 |       91.82 |     96 |    0.96 |            3.63 |     601.61 |    6.62 |        48,947 |   1.36 |       190,026 | 72,839,589 |   9.37 |     96 | fun            |
| **NEGany~necessarily_essential**      | NEGATED    |      4.05 | necessarily  |  3,173,660 | necessarily_essential      |   1.00 |       88.95 |     93 |    0.96 |            3.61 |     582.81 |    6.57 |        48,947 |   1.36 |        69,845 | 72,839,589 |   9.22 |     93 | essential      |
| **NEGmir~ever_easy**                  | NEGMIR     |     63.25 | ever         |    291,732 | ever_easy                  |   1.00 |      304.75 |    369 |    0.83 |            3.08 |   1,285.01 |    6.44 |         5,060 |   0.76 |        18,610 |  1,701,929 |  15.89 |    368 | easy           |
| **NEGany~terribly_original**          | NEGATED    |      9.24 | terribly     |  3,173,660 | terribly_original          |   0.94 |      189.76 |    212 |    0.90 |            2.51 |   1,150.48 |    6.41 |        58,964 |   1.33 |        37,594 | 72,839,589 |  13.45 |    199 | original       |
| **NEGany~necessarily_reliable**       | NEGATED    |      3.53 | necessarily  |  3,173,660 | necessarily_reliable       |   1.00 |       77.47 |     81 |    0.96 |            3.55 |     507.61 |    6.35 |        48,947 |   1.36 |        90,598 | 72,839,589 |   8.61 |     81 | reliable       |
| **NEGany~any_happier**                | NEGATED    |     41.96 | any          |  3,173,660 | any_happier                |   0.86 |      786.04 |    963 |    0.82 |            2.13 |   4,420.49 |    6.34 |        34,382 |   1.30 |        16,606 | 72,839,589 |  27.32 |    828 | happier        |
| **NEGany~terribly_different**         | NEGATED    |     17.82 | terribly     |  3,173,660 | terribly_different         |   0.89 |      348.18 |    409 |    0.85 |            2.27 |   2,022.47 |    6.33 |        58,964 |   1.31 |       825,838 | 72,839,589 |  18.20 |    366 | different      |
| **NEGany~terribly_uncommon**          | NEGATED    |      4.57 | terribly     |  3,173,660 | terribly_uncommon          |   0.98 |       98.43 |    105 |    0.94 |            2.96 |     625.85 |    6.33 |        58,964 |   1.35 |        11,312 | 72,839,589 |   9.70 |    103 | uncommon       |
| **NEGany~terribly_likely**            | NEGATED    |      4.84 | terribly     |  3,173,660 | terribly_likely            |   0.97 |      103.16 |    111 |    0.93 |            2.83 |     649.50 |    6.26 |        58,964 |   1.35 |       890,421 | 72,839,589 |   9.93 |    108 | likely         |
| **NEGany~terribly_unusual**           | NEGATED    |      6.75 | terribly     |  3,173,660 | terribly_unusual           |   0.94 |      139.25 |    155 |    0.90 |            2.53 |     847.05 |    6.17 |        58,964 |   1.33 |        71,234 | 72,839,589 |  11.52 |    146 | unusual        |
| **NEGany~necessarily_proud**          | NEGATED    |      3.09 | necessarily  |  3,173,660 | necessarily_proud          |   1.00 |       67.91 |     71 |    0.96 |            3.50 |     444.94 |    6.14 |        48,947 |   1.36 |       207,536 | 72,839,589 |   8.06 |     71 | proud          |
| **NEGany~particularly_religious**     | NEGATED    |     24.62 | particularly |  3,173,660 | particularly_religious     |   0.86 |      460.38 |    565 |    0.81 |            2.12 |   2,585.71 |    6.12 |       513,668 |   1.29 |        28,028 | 72,839,589 |  20.90 |    485 | religious      |
| **NEGany~yet_mainstream**             | NEGATED    |      3.05 | yet          |  3,173,660 | yet_mainstream             |   1.00 |       66.95 |     70 |    0.96 |            3.49 |     438.67 |    6.11 |        95,763 |   1.36 |        17,792 | 72,839,589 |   8.00 |     70 | mainstream     |
| **NEGany~particularly_new**           | NEGATED    |     39.21 | particularly |  3,173,660 | particularly_new           |   0.83 |      707.79 |    900 |    0.79 |            2.03 |   3,874.46 |    6.04 |       513,668 |   1.28 |       253,862 | 72,839,589 |  25.90 |    747 | new            |
| **NEGany~terribly_impressive**        | NEGATED    |      9.50 | terribly     |  3,173,660 | terribly_impressive        |   0.90 |      186.50 |    218 |    0.86 |            2.28 |   1,087.64 |    5.97 |        58,964 |   1.31 |       178,051 | 72,839,589 |  13.32 |    196 | impressive     |
| **NEGmir~particularly_new**           | NEGMIR     |     70.28 | particularly |    291,732 | particularly_new           |   0.99 |      333.72 |    410 |    0.81 |            2.48 |   1,365.17 |    5.92 |        13,003 |   0.76 |        12,836 |  1,701,929 |  16.60 |    404 | new            |
| **NEGany~particularly_original**      | NEGATED    |     18.56 | particularly |  3,173,660 | particularly_original      |   0.85 |      341.44 |    426 |    0.80 |            2.08 |   1,894.60 |    5.86 |       513,668 |   1.29 |        37,594 | 72,839,589 |  18.00 |    360 | original       |
| **NEGany~that_far-fetched**           | NEGATED    |      2.57 | that         |  3,173,660 | that_far-fetched           |   1.00 |       56.43 |     59 |    0.96 |            3.42 |     369.74 |    5.83 |       208,262 |   1.36 |         5,185 | 72,839,589 |   7.35 |     59 | far-fetched    |
| **NEGany~that_thrilled**              | NEGATED    |      2.57 | that         |  3,173,660 | that_thrilled              |   1.00 |       56.43 |     59 |    0.96 |            3.42 |     369.74 |    5.83 |       208,262 |   1.36 |        24,182 | 72,839,589 |   7.35 |     59 | thrilled       |
| **NEGmir~ever_simple**                | NEGMIR     |     35.31 | ever         |    291,732 | ever_simple                |   1.00 |      170.69 |    206 |    0.83 |            3.30 |     726.76 |    5.82 |         5,060 |   0.77 |        25,408 |  1,701,929 |  11.89 |    206 | simple         |
| **NEGany~immediately_available**      | NEGATED    |  1,278.84 | immediately  |  3,173,660 | immediately_available      |   0.72 |   19,799.16 | 29,351 |    0.67 |            1.75 |  98,046.67 |    5.70 |        96,973 |   1.22 |       666,909 | 72,839,589 | 136.37 | 21,078 | available      |
| **NEGmir~ever_good**                  | NEGMIR     |     51.94 | ever         |    291,732 | ever_good                  |   0.99 |      247.06 |    303 |    0.82 |            2.51 |   1,013.87 |    5.68 |         5,060 |   0.76 |        31,585 |  1,701,929 |  14.29 |    299 | good           |
| **NEGany~any_younger**                | NEGATED    |     13.38 | any          |  3,173,660 | any_younger                |   0.83 |      241.62 |    307 |    0.79 |            2.03 |   1,323.36 |    5.57 |        34,382 |   1.28 |        26,216 | 72,839,589 |  15.13 |    255 | younger        |
| **NEGmir~ever_perfect**               | NEGMIR     |     35.48 | ever         |    291,732 | ever_perfect               |   1.00 |      170.52 |    207 |    0.82 |            2.82 |     714.47 |    5.57 |         5,060 |   0.76 |         3,134 |  1,701,929 |  11.88 |    206 | perfect        |
| **NEGany~immediately_reachable**      | NEGATED    |      5.23 | immediately  |  3,173,660 | immediately_reachable      |   0.91 |      103.77 |    120 |    0.86 |            2.32 |     610.53 |    5.56 |        96,973 |   1.32 |         2,672 | 72,839,589 |   9.94 |    109 | reachable      |
| **NEGany~ever_simple**                | NEGATED    |     10.89 | ever         |  3,173,660 | ever_simple                |   0.84 |      200.11 |    250 |    0.80 |            2.07 |   1,109.28 |    5.56 |       114,075 |   1.29 |       396,749 | 72,839,589 |  13.78 |    211 | simple         |
| **NEGany~particularly_likable**       | NEGATED    |      5.79 | particularly |  3,173,660 | particularly_likable       |   0.89 |      113.21 |    133 |    0.85 |            2.26 |     657.49 |    5.53 |       513,668 |   1.31 |         8,160 | 72,839,589 |  10.38 |    119 | likable        |
| **NEGany~ever_easy**                  | NEGATED    |     24.18 | ever         |  3,173,660 | ever_easy                  |   0.77 |      404.82 |    555 |    0.73 |            1.87 |   2,105.13 |    5.41 |       114,075 |   1.25 |       579,827 | 72,839,589 |  19.54 |    429 | easy           |
| **NEGany~immediately_sure**           | NEGATED    |      6.97 | immediately  |  3,173,660 | immediately_sure           |   0.86 |      131.03 |    160 |    0.82 |            2.13 |     738.65 |    5.40 |        96,973 |   1.30 |       262,825 | 72,839,589 |  11.15 |    138 | sure           |
| **NEGany~terribly_productive**        | NEGATED    |      2.92 | terribly     |  3,173,660 | terribly_productive        |   0.96 |       61.08 |     67 |    0.91 |            2.61 |     376.84 |    5.39 |        58,964 |   1.34 |       102,361 | 72,839,589 |   7.64 |     64 | productive     |
| **NEGany~inherently_wrong**           | NEGATED    |    100.87 | inherently   |  3,173,660 | inherently_wrong           |   0.71 |    1,538.13 |  2,315 |    0.66 |            1.73 |   7,535.97 |    5.36 |        47,803 |   1.21 |       149,064 | 72,839,589 |  37.99 |  1,639 | wrong          |
| **NEGany~particularly_likeable**      | NEGATED    |      5.23 | particularly |  3,173,660 | particularly_likeable      |   0.88 |      100.77 |    120 |    0.84 |            2.21 |     579.07 |    5.34 |       513,668 |   1.31 |         5,902 | 72,839,589 |   9.79 |    106 | likeable       |
| **NEGmir~exactly_sure**               | NEGMIR     |     25.37 | exactly      |    291,732 | exactly_sure               |   1.00 |      122.63 |    148 |    0.83 |            3.16 |     522.11 |    5.31 |         1,041 |   0.77 |         6,761 |  1,701,929 |  10.08 |    148 | sure           |
| **NEGmir~ever_enough**                | NEGMIR     |     25.20 | ever         |    291,732 | ever_enough                |   1.00 |      121.80 |    147 |    0.83 |            3.15 |     518.58 |    5.30 |         5,060 |   0.77 |         2,596 |  1,701,929 |  10.05 |    147 | enough         |
| **NEGmir~ever_certain**               | NEGMIR     |     24.51 | ever         |    291,732 | ever_certain               |   1.00 |      118.49 |    143 |    0.83 |            3.14 |     504.47 |    5.26 |         5,060 |   0.77 |         1,800 |  1,701,929 |   9.91 |    143 | certain        |
| **NEGany~terribly_sure**              | NEGATED    |      3.31 | terribly     |  3,173,660 | terribly_sure              |   0.91 |       65.69 |     76 |    0.86 |            2.31 |     386.31 |    5.08 |        58,964 |   1.32 |       262,825 | 72,839,589 |   7.91 |     69 | sure           |
| **NEGany~any_easier**                 | NEGATED    |    104.79 | any          |  3,173,660 | any_easier                 |   0.66 |    1,489.21 |  2,405 |    0.62 |            1.64 |   6,987.78 |    5.08 |        34,382 |   1.18 |       209,940 | 72,839,589 |  37.30 |  1,594 | easier         |
| **NEGany~remotely_surprising**        | NEGATED    |      3.66 | remotely     |  3,173,660 | remotely_surprising        |   0.89 |       71.34 |     84 |    0.85 |            2.24 |     413.61 |    5.07 |        16,426 |   1.31 |        70,540 | 72,839,589 |   8.24 |     75 | surprising     |
| **NEGmir~particularly_surprising**    | NEGMIR     |     28.80 | particularly |    291,732 | particularly_surprising    |   0.99 |      137.20 |    168 |    0.82 |            2.51 |     564.67 |    5.06 |        13,003 |   0.76 |         2,662 |  1,701,929 |  10.65 |    166 | surprising     |
| **NEGmir~particularly_wrong**         | NEGMIR     |     37.20 | particularly |    291,732 | particularly_wrong         |   0.98 |      174.80 |    217 |    0.81 |            2.27 |     702.22 |    5.05 |        13,003 |   0.76 |        20,880 |  1,701,929 |  12.01 |    212 | wrong          |
| **NEGmir~necessarily_wrong**          | NEGMIR     |     37.03 | necessarily  |    291,732 | necessarily_wrong          |   0.98 |      173.97 |    216 |    0.81 |            2.27 |     698.74 |    5.04 |         1,107 |   0.76 |        20,880 |  1,701,929 |  11.98 |    211 | wrong          |
| **NEGany~any_simpler**                | NEGATED    |     13.07 | any          |  3,173,660 | any_simpler                |   0.75 |      212.93 |    300 |    0.71 |            1.82 |   1,087.71 |    5.00 |        34,382 |   1.24 |        23,480 | 72,839,589 |  14.16 |    226 | simpler        |
| **NEGany~terribly_reliable**          | NEGATED    |      2.35 | terribly     |  3,173,660 | terribly_reliable          |   0.94 |       48.65 |     54 |    0.90 |            2.51 |     296.70 |    4.99 |        58,964 |   1.34 |        90,598 | 72,839,589 |   6.81 |     51 | reliable       |
| **NEGany~particularly_forthcoming**   | NEGATED    |      3.62 | particularly |  3,173,660 | particularly_forthcoming   |   0.87 |       68.38 |     83 |    0.82 |            2.14 |     387.25 |    4.85 |       513,668 |   1.30 |         7,473 | 72,839,589 |   8.06 |     72 | forthcoming    |
| **NEGany~ever_certain**               | NEGATED    |      8.41 | ever         |  3,173,660 | ever_certain               |   0.76 |      138.59 |    193 |    0.72 |            1.84 |     713.34 |    4.80 |       114,075 |   1.24 |        74,952 | 72,839,589 |  11.43 |    147 | certain        |
| **NEGany~particularly_athletic**      | NEGATED    |      5.93 | particularly |  3,173,660 | particularly_athletic      |   0.79 |      102.07 |    136 |    0.75 |            1.92 |     541.01 |    4.77 |       513,668 |   1.26 |        17,142 | 72,839,589 |   9.82 |    108 | athletic       |
| **NEGany~any_nicer**                  | NEGATED    |      5.18 | any          |  3,173,660 | any_nicer                  |   0.81 |       90.82 |    119 |    0.76 |            1.95 |     486.82 |    4.75 |        34,382 |   1.27 |         9,955 | 72,839,589 |   9.27 |     96 | nicer          |
| **NEGany~particularly_surprising**    | NEGATED    |     75.94 | particularly |  3,173,660 | particularly_surprising    |   0.61 |      993.06 |  1,743 |    0.57 |            1.54 |   4,433.52 |    4.71 |       513,668 |   1.15 |        70,540 | 72,839,589 |  30.37 |  1,069 | surprising     |
| **NEGany~immediately_able**           | NEGATED    |     43.09 | immediately  |  3,173,660 | immediately_able           |   0.63 |      582.91 |    989 |    0.59 |            1.58 |   2,655.18 |    4.70 |        96,973 |   1.16 |       223,196 | 72,839,589 |  23.30 |    626 | able           |
| **NEGany~inherently_bad**             | NEGATED    |     56.95 | inherently   |  3,173,660 | inherently_bad             |   0.61 |      737.05 |  1,307 |    0.56 |            1.53 |   3,270.68 |    4.62 |        47,803 |   1.14 |       429,537 | 72,839,589 |  26.16 |    794 | bad            |
| **NEGany~remotely_true**              | NEGATED    |     16.12 | remotely     |  3,173,660 | remotely_true              |   0.68 |      233.88 |    370 |    0.63 |            1.66 |   1,111.13 |    4.61 |        16,426 |   1.19 |       231,639 | 72,839,589 |  14.79 |    250 | true           |
| **NEGany~immediately_obvious**        | NEGATED    |    173.80 | immediately  |  3,173,660 | immediately_obvious        |   0.56 |    2,064.20 |  3,989 |    0.52 |            1.45 |   8,712.07 |    4.55 |        96,973 |   1.11 |       165,439 | 72,839,589 |  43.63 |  2,238 | obvious        |
| **NEGany~particularly_revolutionary** | NEGATED    |      4.23 | particularly |  3,173,660 | particularly_revolutionary |   0.79 |       72.77 |     97 |    0.75 |            1.92 |     385.60 |    4.49 |       513,668 |   1.26 |        10,338 | 72,839,589 |   8.29 |     77 | revolutionary  |
| **NEGany~ever_boring**                | NEGATED    |      3.92 | ever         |  3,173,660 | ever_boring                |   0.80 |       68.08 |     90 |    0.76 |            1.93 |     362.74 |    4.46 |       114,075 |   1.26 |        45,891 | 72,839,589 |   8.02 |     72 | boring         |
| **NEGmir~any_better**                 | NEGMIR     |     71.82 | any          |    291,732 | any_better                 |   0.91 |      308.18 |    419 |    0.74 |            1.67 |   1,096.01 |    4.38 |         1,197 |   0.72 |        14,013 |  1,701,929 |  15.81 |    380 | better         |
| **NEGmir~that_simple**                | NEGMIR     |     90.68 | that         |    291,732 | that_simple                |   0.90 |      383.32 |    529 |    0.72 |            1.62 |   1,340.19 |    4.36 |         5,494 |   0.72 |        25,408 |  1,701,929 |  17.61 |    474 | simple         |
| **NEGany~any_clearer**                | NEGATED    |     26.49 | any          |  3,173,660 | any_clearer                |   0.58 |      328.51 |    608 |    0.54 |            1.49 |   1,421.60 |    4.26 |        34,382 |   1.13 |        11,680 | 72,839,589 |  17.44 |    355 | clearer        |
| **NEGmir~particularly_remarkable**    | NEGMIR     |     19.03 | particularly |    291,732 | particularly_remarkable    |   0.97 |       88.97 |    111 |    0.80 |            2.18 |     354.53 |    4.24 |        13,003 |   0.75 |         3,238 |  1,701,929 |   8.56 |    108 | remarkable     |
| **NEGmir~that_easy**                  | NEGMIR     |     87.08 | that         |    291,732 | that_easy                  |   0.89 |      362.92 |    508 |    0.71 |            1.57 |   1,248.84 |    4.23 |         5,494 |   0.71 |        18,610 |  1,701,929 |  17.11 |    450 | easy           |
| **NEGany~immediately_certain**        | NEGATED    |      4.05 | immediately  |  3,173,660 | immediately_certain        |   0.75 |       65.95 |     93 |    0.71 |            1.82 |     336.68 |    4.19 |        96,973 |   1.24 |        74,952 | 72,839,589 |   7.88 |     70 | certain        |
| **NEGmir~ever_able**                  | NEGMIR     |     24.51 | ever         |    291,732 | ever_able                  |   0.95 |      111.49 |    143 |    0.78 |            1.94 |     426.52 |    4.17 |         5,060 |   0.74 |         3,704 |  1,701,929 |   9.56 |    136 | able           |
| **NEGany~remotely_ready**             | NEGATED    |      3.22 | remotely     |  3,173,660 | remotely_ready             |   0.78 |       54.78 |     74 |    0.74 |            1.89 |     287.63 |    4.16 |        16,426 |   1.26 |       141,590 | 72,839,589 |   7.19 |     58 | ready          |
| **NEGany~remotely_funny**             | NEGATED    |      9.24 | remotely     |  3,173,660 | remotely_funny             |   0.65 |      127.76 |    212 |    0.60 |            1.60 |     589.74 |    4.15 |        16,426 |   1.17 |       122,927 | 72,839,589 |  10.92 |    137 | funny          |
| **NEGmir~inherently_wrong**           | NEGMIR     |    313.00 | inherently   |    291,732 | inherently_wrong           |   0.83 |    1,200.00 |  1,826 |    0.66 |            1.37 |   3,787.53 |    4.08 |         5,133 |   0.68 |        20,880 |  1,701,929 |  30.85 |  1,513 | wrong          |
| **NEGany~particularly_flashy**        | NEGATED    |      3.22 | particularly |  3,173,660 | particularly_flashy        |   0.77 |       53.78 |     74 |    0.73 |            1.86 |     278.96 |    4.08 |       513,668 |   1.25 |         4,494 | 72,839,589 |   7.12 |     57 | flashy         |
| **NEGmir~terribly_surprising**        | NEGMIR     |     11.48 | terribly     |    291,732 | terribly_surprising        |   1.00 |       55.52 |     67 |    0.83 |            2.81 |     236.35 |    4.07 |         4,610 |   0.77 |         2,662 |  1,701,929 |   6.78 |     67 | surprising     |
| **NEGany~any_cheaper**                | NEGATED    |      8.98 | any          |  3,173,660 | any_cheaper                |   0.63 |      120.02 |    206 |    0.58 |            1.56 |     542.97 |    4.01 |        34,382 |   1.16 |        46,055 | 72,839,589 |  10.57 |    129 | cheaper        |
| **NEGmir~particularly_close**         | NEGMIR     |     24.85 | particularly |    291,732 | particularly_close         |   0.94 |      111.15 |    145 |    0.77 |            1.84 |     415.70 |    4.01 |        13,003 |   0.74 |        13,874 |  1,701,929 |   9.53 |    136 | close          |
| **NEGany~any_smarter**                | NEGATED    |      5.75 | any          |  3,173,660 | any_smarter                |   0.67 |       83.25 |    132 |    0.63 |            1.65 |     394.95 |    4.00 |        34,382 |   1.19 |         8,501 | 72,839,589 |   8.82 |     89 | smarter        |
| **NEGany~any_worse**                  | NEGATED    |    160.03 | any          |  3,173,660 | any_worse                  |   0.46 |    1,525.97 |  3,673 |    0.42 |            1.27 |   5,676.37 |    3.94 |        34,382 |   1.02 |       179,012 | 72,839,589 |  37.16 |  1,686 | worse          |
| **NEGany~any_brighter**               | NEGATED    |      3.83 | any          |  3,173,660 | any_brighter               |   0.72 |       59.17 |     88 |    0.67 |            1.74 |     292.00 |    3.91 |        34,382 |   1.22 |         9,280 | 72,839,589 |   7.45 |     63 | brighter       |
| **NEGany~immediately_forthcoming**    | NEGATED    |      9.72 | immediately  |  3,173,660 | immediately_forthcoming    |   0.60 |      123.28 |    223 |    0.55 |            1.51 |     540.70 |    3.89 |        96,973 |   1.14 |         7,473 | 72,839,589 |  10.69 |    133 | forthcoming    |
| **NEGany~ever_good**                  | NEGATED    |     28.76 | ever         |  3,173,660 | ever_good                  |   0.50 |      302.24 |    660 |    0.46 |            1.34 |   1,188.69 |    3.81 |       114,075 |   1.06 |     1,681,795 | 72,839,589 |  16.61 |    331 | good           |
| **NEGmir~ever_boring**                | NEGMIR     |      9.77 | ever         |    291,732 | ever_boring                |   1.00 |       47.23 |     57 |    0.83 |            2.75 |     201.07 |    3.80 |         5,060 |   0.77 |         1,961 |  1,701,929 |   6.26 |     57 | boring         |
| **NEGmir~ever_black**                 | NEGMIR     |      9.60 | ever         |    291,732 | ever_black                 |   1.00 |       46.40 |     56 |    0.83 |            2.74 |     197.54 |    3.77 |         5,060 |   0.77 |         1,412 |  1,701,929 |   6.20 |     56 | black          |
| **NEGmir~particularly_novel**         | NEGMIR     |      9.26 | particularly |    291,732 | particularly_novel         |   1.00 |       44.74 |     54 |    0.83 |            2.72 |     190.49 |    3.71 |        13,003 |   0.77 |           320 |  1,701,929 |   6.09 |     54 | novel          |
| **NEGmir~terribly_new**               | NEGMIR     |     12.17 | terribly     |    291,732 | terribly_new               |   0.97 |       56.83 |     71 |    0.80 |            2.13 |     225.93 |    3.66 |         4,610 |   0.75 |        12,836 |  1,701,929 |   6.84 |     69 | new            |
| **NEGany~remotely_close**             | NEGATED    |     69.58 | remotely     |  3,173,660 | remotely_close             |   0.43 |      624.42 |  1,597 |    0.39 |            1.23 |   2,243.22 |    3.65 |        16,426 |   1.00 |       411,329 | 72,839,589 |  23.70 |    694 | close          |
| **NEGmir~that_great**                 | NEGMIR     |     58.62 | that         |    291,732 | that_great                 |   0.84 |      227.38 |    342 |    0.66 |            1.39 |     725.16 |    3.57 |         5,494 |   0.69 |         5,568 |  1,701,929 |  13.45 |    286 | great          |
| **NEGany~ever_enough**                | NEGATED    |     15.12 | ever         |  3,173,660 | ever_enough                |   0.50 |      157.88 |    347 |    0.45 |            1.34 |     618.62 |    3.54 |       114,075 |   1.06 |       152,020 | 72,839,589 |  12.00 |    173 | enough         |
| **COM~ever_closer**                   | COMPLEMENT |  6,031.92 | ever         | 69,662,736 | ever_closer                |   1.00 |      273.08 |  6,307 |    0.04 |            2.06 |     538.66 |    3.51 |       114,075 |   0.02 |        61,475 | 72,839,589 |   3.44 |  6,305 | closer         |
| **NEGany~inherently_illegal**         | NEGATED    |      4.01 | inherently   |  3,173,660 | inherently_illegal         |   0.64 |       54.99 |     92 |    0.60 |            1.59 |     252.59 |    3.51 |        47,803 |   1.17 |        30,194 | 72,839,589 |   7.16 |     59 | illegal        |
| **NEGmir~terribly_original**          | NEGMIR     |      7.71 | terribly     |    291,732 | terribly_original          |   1.00 |       37.29 |     45 |    0.83 |            2.64 |     158.74 |    3.40 |         4,610 |   0.77 |         1,555 |  1,701,929 |   5.56 |     45 | original       |
| **NEGmir~exactly_clear**              | NEGMIR     |      9.08 | exactly      |    291,732 | exactly_clear              |   0.98 |       42.92 |     53 |    0.81 |            2.23 |     173.89 |    3.38 |         1,041 |   0.76 |         6,722 |  1,701,929 |   5.95 |     52 | clear          |
| **NEGmir~particularly_comfortable**   | NEGMIR     |      7.54 | particularly |    291,732 | particularly_comfortable   |   1.00 |       36.46 |     44 |    0.83 |            2.63 |     155.21 |    3.36 |        13,003 |   0.77 |         4,642 |  1,701,929 |   5.50 |     44 | comfortable    |
| **NEGany~ever_perfect**               | NEGATED    |     21.31 | ever         |  3,173,660 | ever_perfect               |   0.44 |      194.69 |    489 |    0.40 |            1.24 |     706.71 |    3.34 |       114,075 |   1.01 |       104,659 | 72,839,589 |  13.25 |    216 | perfect        |
| **NEGany~ever_sure**                  | NEGATED    |      7.06 | ever         |  3,173,660 | ever_sure                  |   0.54 |       79.94 |    162 |    0.49 |            1.41 |     328.20 |    3.34 |       114,075 |   1.09 |       262,825 | 72,839,589 |   8.57 |     87 | sure           |
| **NEGmir~remotely_close**             | NEGMIR     |     45.77 | remotely     |    291,732 | remotely_close             |   0.82 |      172.23 |    267 |    0.65 |            1.33 |     532.96 |    3.28 |         2,341 |   0.68 |        13,874 |  1,701,929 |  11.67 |    218 | close          |
| **NEGmir~any_different**              | NEGMIR     |      8.40 | any          |    291,732 | any_different              |   0.98 |       39.60 |     49 |    0.81 |            2.19 |     159.93 |    3.24 |         1,197 |   0.76 |        36,166 |  1,701,929 |   5.72 |     48 | different      |
| **NEGany~immediately_intuitive**      | NEGATED    |      3.96 | immediately  |  3,173,660 | immediately_intuitive      |   0.59 |       50.04 |     91 |    0.55 |            1.50 |     218.74 |    3.21 |        96,973 |   1.13 |        20,664 | 72,839,589 |   6.81 |     54 | intuitive      |
| **NEGmir~that_big**                   | NEGMIR     |     22.46 | that         |    291,732 | that_big                   |   0.86 |       90.54 |    131 |    0.69 |            1.47 |     300.54 |    3.17 |         5,494 |   0.70 |         8,177 |  1,701,929 |   8.52 |    113 | big            |
| **NEGmir~that_popular**               | NEGMIR     |     12.00 | that         |    291,732 | that_popular               |   0.93 |       53.00 |     70 |    0.76 |            1.76 |     195.15 |    3.15 |         5,494 |   0.73 |         5,668 |  1,701,929 |   6.57 |     65 | popular        |
| **NEGmir~ever_sick**                  | NEGMIR     |      6.69 | ever         |    291,732 | ever_sick                  |   1.00 |       32.31 |     39 |    0.83 |            2.58 |     137.57 |    3.15 |         5,060 |   0.77 |         1,895 |  1,701,929 |   5.17 |     39 | sick           |
| **NEGmir~particularly_revolutionary** | NEGMIR     |      6.69 | particularly |    291,732 | particularly_revolutionary |   1.00 |       32.31 |     39 |    0.83 |            2.58 |     137.57 |    3.15 |        13,003 |   0.77 |           485 |  1,701,929 |   5.17 |     39 | revolutionary  |
| **NEGany~remotely_qualified**         | NEGATED    |      4.40 | remotely     |  3,173,660 | remotely_qualified         |   0.56 |       52.60 |    101 |    0.52 |            1.45 |     222.79 |    3.13 |        16,426 |   1.11 |        74,643 | 72,839,589 |   6.97 |     57 | qualified      |
| **NEGmir~remotely_true**              | NEGMIR     |     11.31 | remotely     |    291,732 | remotely_true              |   0.92 |       49.69 |     66 |    0.75 |            1.73 |     181.65 |    3.04 |         2,341 |   0.73 |         6,191 |  1,701,929 |   6.36 |     61 | true           |
| **NEGmir~any_easier**                 | NEGMIR     |     11.31 | any          |    291,732 | any_easier                 |   0.92 |       49.69 |     66 |    0.75 |            1.73 |     181.65 |    3.04 |         1,197 |   0.73 |         2,386 |  1,701,929 |   6.36 |     61 | easier         |
| **NEGany~remotely_comparable**        | NEGATED    |     12.07 | remotely     |  3,173,660 | remotely_comparable        |   0.43 |      105.93 |    277 |    0.38 |            1.21 |     375.73 |    2.98 |        16,426 |   0.99 |        12,252 | 72,839,589 |   9.75 |    118 | comparable     |
| **NEGmir~necessarily_bad**            | NEGMIR     |      9.08 | necessarily  |    291,732 | necessarily_bad            |   0.94 |       40.92 |     53 |    0.77 |            1.84 |     154.45 |    2.95 |         1,107 |   0.74 |        10,261 |  1,701,929 |   5.79 |     50 | bad            |
| **NEGmir~inherently_bad**             | NEGMIR     |     32.23 | inherently   |    291,732 | inherently_bad             |   0.79 |      115.77 |    188 |    0.62 |            1.25 |     342.53 |    2.86 |         5,133 |   0.66 |        10,261 |  1,701,929 |   9.52 |    148 | bad            |
| **NEGany~inherently_evil**            | NEGATED    |     48.93 | inherently   |  3,173,660 | inherently_evil            |   0.32 |      309.07 |  1,123 |    0.28 |            1.01 |     905.80 |    2.81 |        47,803 |   0.86 |        22,706 | 72,839,589 |  16.33 |    358 | evil           |
| **NEGany~remotely_interested**        | NEGATED    |     46.27 | remotely     |  3,173,660 | remotely_interested        |   0.31 |      283.73 |  1,062 |    0.27 |            1.00 |     817.06 |    2.74 |        16,426 |   0.85 |       264,528 | 72,839,589 |  15.62 |    330 | interested     |
| **NEGmir~any_worse**                  | NEGMIR     |     18.00 | any          |    291,732 | any_worse                  |   0.83 |       69.00 |    105 |    0.66 |            1.36 |     217.46 |    2.73 |         1,197 |   0.68 |         8,790 |  1,701,929 |   7.40 |     87 | worse          |
| **NEGmir~particularly_radical**       | NEGMIR     |      5.31 | particularly |    291,732 | particularly_radical       |   1.00 |       25.69 |     31 |    0.83 |            2.48 |     109.35 |    2.73 |        13,003 |   0.77 |         1,072 |  1,701,929 |   4.61 |     31 | radical        |
| **NEGmir~that_keen**                  | NEGMIR     |      5.31 | that         |    291,732 | that_keen                  |   1.00 |       25.69 |     31 |    0.83 |            2.48 |     109.35 |    2.73 |         5,494 |   0.77 |         1,360 |  1,701,929 |   4.61 |     31 | keen           |
| **NEGmir~any_bigger**                 | NEGMIR     |      6.34 | any          |    291,732 | any_bigger                 |   0.97 |       29.66 |     37 |    0.80 |            2.07 |     118.17 |    2.73 |         1,197 |   0.75 |         3,923 |  1,701,929 |   4.94 |     36 | bigger         |
| **NEGmir~remotely_comparable**        | NEGMIR     |      8.06 | remotely     |    291,732 | remotely_comparable        |   0.94 |       35.94 |     47 |    0.76 |            1.79 |     134.02 |    2.72 |         2,341 |   0.74 |           283 |  1,701,929 |   5.42 |     44 | comparable     |
| **NEGmir~necessarily_true**           | NEGMIR     |     10.11 | necessarily  |    291,732 | necessarily_true           |   0.90 |       42.89 |     59 |    0.73 |            1.60 |     150.42 |    2.69 |         1,107 |   0.72 |         6,191 |  1,701,929 |   5.89 |     53 | true           |
| **NEGany~ever_satisfied**             | NEGATED    |      6.58 | ever         |  3,173,660 | ever_satisfied             |   0.42 |       57.42 |    151 |    0.38 |            1.21 |     203.01 |    2.57 |       114,075 |   0.99 |        62,862 | 72,839,589 |   7.18 |     64 | satisfied      |
| **NEGmir~yet_available**              | NEGMIR     |      4.80 | yet          |    291,732 | yet_available              |   1.00 |       23.20 |     28 |    0.83 |            2.44 |      98.77 |    2.54 |           815 |   0.77 |        10,284 |  1,701,929 |   4.38 |     28 | available      |
| **NEGany~inherently_negative**        | NEGATED    |      8.41 | inherently   |  3,173,660 | inherently_negative        |   0.39 |       66.59 |    193 |    0.35 |            1.15 |     222.63 |    2.50 |        47,803 |   0.95 |        53,385 | 72,839,589 |   7.69 |     75 | negative       |
| **NEGmir~terribly_interesting**       | NEGMIR     |     11.31 | terribly     |    291,732 | terribly_interesting       |   0.85 |       44.69 |     66 |    0.68 |            1.42 |     145.16 |    2.44 |         4,610 |   0.69 |        12,447 |  1,701,929 |   5.97 |     56 | interesting    |
| **NEGmir~particularly_fast**          | NEGMIR     |      4.46 | particularly |    291,732 | particularly_fast          |   1.00 |       21.54 |     26 |    0.83 |            2.41 |      91.71 |    2.39 |        13,003 |   0.77 |         1,259 |  1,701,929 |   4.22 |     26 | fast           |
| **NEGmir~terribly_interested**        | NEGMIR     |      7.37 | terribly     |    291,732 | terribly_interested        |   0.91 |       31.63 |     43 |    0.74 |            1.63 |     112.46 |    2.36 |         4,610 |   0.72 |         8,255 |  1,701,929 |   5.06 |     39 | interested     |
| **NEGmir~any_closer**                 | NEGMIR     |     11.83 | any          |    291,732 | any_closer                 |   0.83 |       45.17 |     69 |    0.65 |            1.35 |     141.82 |    2.33 |         1,197 |   0.68 |           993 |  1,701,929 |   5.98 |     57 | closer         |
| **NEGmir~exactly_new**                | NEGMIR     |      5.14 | exactly      |    291,732 | exactly_new                |   0.97 |       23.86 |     30 |    0.80 |            1.98 |      93.90 |    2.31 |         1,041 |   0.75 |        12,836 |  1,701,929 |   4.43 |     29 | new            |
| **NEGmir~terribly_unusual**           | NEGMIR     |      4.11 | terribly     |    291,732 | terribly_unusual           |   1.00 |       19.89 |     24 |    0.83 |            2.37 |      84.66 |    2.23 |         4,610 |   0.77 |         2,302 |  1,701,929 |   4.06 |     24 | unusual        |
| **NEGmir~terribly_special**           | NEGMIR     |      4.11 | terribly     |    291,732 | terribly_special           |   1.00 |       19.89 |     24 |    0.83 |            2.37 |      84.66 |    2.23 |         4,610 |   0.77 |        15,541 |  1,701,929 |   4.06 |     24 | special        |
| **NEGany~inherently_good**            | NEGATED    |     51.28 | inherently   |  3,173,660 | inherently_good            |   0.24 |      231.72 |  1,177 |    0.20 |            0.84 |     554.72 |    2.21 |        47,803 |   0.74 |     1,681,795 | 72,839,589 |  13.77 |    283 | good           |
| **NEGany~remotely_similar**           | NEGATED    |     24.36 | remotely     |  3,173,660 | remotely_similar           |   0.27 |      127.64 |    559 |    0.23 |            0.91 |     334.61 |    2.20 |        16,426 |   0.80 |       203,453 | 72,839,589 |  10.35 |    152 | similar        |
| **NEGmir~necessarily_right**          | NEGMIR     |      3.94 | necessarily  |    291,732 | necessarily_right          |   1.00 |       19.06 |     23 |    0.83 |            2.36 |      81.13 |    2.15 |         1,107 |   0.77 |         5,576 |  1,701,929 |   3.97 |     23 | right          |
| **NEGmir~that_impressive**            | NEGMIR     |      3.94 | that         |    291,732 | that_impressive            |   1.00 |       19.06 |     23 |    0.83 |            2.36 |      81.13 |    2.15 |         5,494 |   0.77 |         5,007 |  1,701,929 |   3.97 |     23 | impressive     |
| **NEGmir~any_good**                   | NEGMIR     |      6.00 | any          |    291,732 | any_good                   |   0.91 |       26.00 |     35 |    0.74 |            1.65 |      93.53 |    2.12 |         1,197 |   0.73 |        31,585 |  1,701,929 |   4.60 |     32 | good           |
| **NEGany~remotely_accurate**          | NEGATED    |      5.84 | remotely     |  3,173,660 | remotely_accurate          |   0.37 |       44.16 |    134 |    0.33 |            1.12 |     143.78 |    2.10 |        16,426 |   0.93 |       152,299 | 72,839,589 |   6.25 |     50 | accurate       |
| **NEGmir~inherently_illegal**         | NEGMIR     |      4.63 | inherently   |    291,732 | inherently_illegal         |   0.96 |       21.37 |     27 |    0.79 |            1.93 |      83.54 |    2.10 |         5,133 |   0.75 |           937 |  1,701,929 |   4.19 |     26 | illegal        |
| **NEGmir~remotely_believable**        | NEGMIR     |      3.60 | remotely     |    291,732 | remotely_believable        |   1.00 |       17.40 |     21 |    0.83 |            2.32 |      74.08 |    1.96 |         2,341 |   0.77 |           600 |  1,701,929 |   3.80 |     21 | believable     |
| **NEGmir~yet_certain**                | NEGMIR     |      3.60 | yet          |    291,732 | yet_certain                |   1.00 |       17.40 |     21 |    0.83 |            2.32 |      74.08 |    1.96 |           815 |   0.77 |         1,800 |  1,701,929 |   3.80 |     21 | certain        |
| **NEGmir~any_younger**                | NEGMIR     |      3.43 | any          |    291,732 | any_younger                |   1.00 |       16.57 |     20 |    0.83 |            2.30 |      70.55 |    1.86 |         1,197 |   0.77 |           939 |  1,701,929 |   3.71 |     20 | younger        |
| **NEGmir~exactly_easy**               | NEGMIR     |      3.43 | exactly      |    291,732 | exactly_easy               |   1.00 |       16.57 |     20 |    0.83 |            2.30 |      70.55 |    1.86 |         1,041 |   0.77 |        18,610 |  1,701,929 |   3.71 |     20 | easy           |
| **NEGmir~remotely_funny**             | NEGMIR     |      8.74 | remotely     |    291,732 | remotely_funny             |   0.80 |       32.26 |     51 |    0.63 |            1.28 |      97.91 |    1.85 |         2,341 |   0.67 |         5,365 |  1,701,929 |   5.04 |     41 | funny          |
| **NEGmir~immediately_available**      | NEGMIR     |     47.14 | immediately  |    291,732 | immediately_available      |   0.59 |      114.86 |    275 |    0.42 |            0.84 |     241.53 |    1.85 |         1,195 |   0.54 |        10,284 |  1,701,929 |   9.02 |    162 | available      |
| **NEGmir~that_fond**                  | NEGMIR     |      4.11 | that         |    291,732 | that_fond                  |   0.96 |       18.89 |     24 |    0.79 |            1.88 |      73.19 |    1.84 |         5,494 |   0.75 |         1,115 |  1,701,929 |   3.94 |     23 | fond           |
| **NEGmir~that_comfortable**           | NEGMIR     |      4.11 | that         |    291,732 | that_comfortable           |   0.96 |       18.89 |     24 |    0.79 |            1.88 |      73.19 |    1.84 |         5,494 |   0.75 |         4,642 |  1,701,929 |   3.94 |     23 | comfortable    |
| **NEGmir~necessarily_new**            | NEGMIR     |      4.11 | necessarily  |    291,732 | necessarily_new            |   0.96 |       18.89 |     24 |    0.79 |            1.88 |      73.19 |    1.84 |         1,107 |   0.75 |        12,836 |  1,701,929 |   3.94 |     23 | new            |
| **NEGmir~remotely_interesting**       | NEGMIR     |     13.20 | remotely     |    291,732 | remotely_interesting       |   0.73 |       42.80 |     77 |    0.56 |            1.10 |     115.20 |    1.80 |         2,341 |   0.63 |        12,447 |  1,701,929 |   5.72 |     56 | interesting    |
| **NEGmir~terribly_popular**           | NEGMIR     |      3.26 | terribly     |    291,732 | terribly_popular           |   1.00 |       15.74 |     19 |    0.83 |            2.28 |      67.02 |    1.75 |         4,610 |   0.77 |         5,668 |  1,701,929 |   3.61 |     19 | popular        |
| **NEGmir~yet_clear**                  | NEGMIR     |      3.26 | yet          |    291,732 | yet_clear                  |   1.00 |       15.74 |     19 |    0.83 |            2.28 |      67.02 |    1.75 |           815 |   0.77 |         6,722 |  1,701,929 |   3.61 |     19 | clear          |
| **NEGmir~yet_sure**                   | NEGMIR     |      3.26 | yet          |    291,732 | yet_sure                   |   1.00 |       15.74 |     19 |    0.83 |            2.28 |      67.02 |    1.75 |           815 |   0.77 |         6,761 |  1,701,929 |   3.61 |     19 | sure           |
| **NEGmir~remotely_similar**           | NEGMIR     |     18.34 | remotely     |    291,732 | remotely_similar           |   0.66 |       52.66 |    107 |    0.49 |            0.98 |     127.32 |    1.70 |         2,341 |   0.59 |         7,011 |  1,701,929 |   6.25 |     71 | similar        |
| **NEGmir~inherently_better**          | NEGMIR     |     10.11 | inherently   |    291,732 | inherently_better          |   0.75 |       33.89 |     59 |    0.57 |            1.14 |      93.95 |    1.65 |         5,133 |   0.64 |        14,013 |  1,701,929 |   5.11 |     44 | better         |
| **NEGmir~necessarily_better**         | NEGMIR     |      5.31 | necessarily  |    291,732 | necessarily_better         |   0.87 |       21.69 |     31 |    0.70 |            1.47 |      72.90 |    1.63 |         1,107 |   0.71 |        14,013 |  1,701,929 |   4.17 |     27 | better         |
| **NEGmir~inherently_improper**        | NEGMIR     |      3.09 | inherently   |    291,732 | inherently_improper        |   1.00 |       14.91 |     18 |    0.83 |            2.25 |      63.49 |    1.63 |         5,133 |   0.77 |           142 |  1,701,929 |   3.52 |     18 | improper       |
| **NEGmir~yet_ready**                  | NEGMIR     |      3.09 | yet          |    291,732 | yet_ready                  |   1.00 |       14.91 |     18 |    0.83 |            2.25 |      63.49 |    1.63 |           815 |   0.77 |         3,034 |  1,701,929 |   3.52 |     18 | ready          |
| **NEGmir~any_clearer**                | NEGMIR     |      2.91 | any          |    291,732 | any_clearer                |   1.00 |       14.09 |     17 |    0.83 |            2.23 |      59.97 |    1.50 |         1,197 |   0.77 |           130 |  1,701,929 |   3.42 |     17 | clearer        |
| **NEGmir~remotely_surprising**        | NEGMIR     |      2.91 | remotely     |    291,732 | remotely_surprising        |   1.00 |       14.09 |     17 |    0.83 |            2.23 |      59.97 |    1.50 |         2,341 |   0.77 |         2,662 |  1,701,929 |   3.42 |     17 | surprising     |
| **NEGmir~any_higher**                 | NEGMIR     |      3.94 | any          |    291,732 | any_higher                 |   0.91 |       17.06 |     23 |    0.74 |            1.62 |      61.24 |    1.42 |         1,197 |   0.73 |         2,893 |  1,701,929 |   3.72 |     21 | higher         |
| **NEGmir~remotely_possible**          | NEGMIR     |      8.91 | remotely     |    291,732 | remotely_possible          |   0.73 |       29.09 |     52 |    0.56 |            1.11 |      78.73 |    1.42 |         2,341 |   0.63 |         3,160 |  1,701,929 |   4.72 |     38 | possible       |
| **NEGmir~that_clear**                 | NEGMIR     |      3.26 | that         |    291,732 | that_clear                 |   0.95 |       14.74 |     19 |    0.78 |            1.78 |      56.03 |    1.30 |         5,494 |   0.74 |         6,722 |  1,701,929 |   3.47 |     18 | clear          |
| **NEGmir~necessarily_illegal**        | NEGMIR     |      2.57 | necessarily  |    291,732 | necessarily_illegal        |   1.00 |       12.43 |     15 |    0.83 |            2.18 |      52.91 |    1.20 |         1,107 |   0.77 |           937 |  1,701,929 |   3.21 |     15 | illegal        |
| **NEGmir~terribly_clear**             | NEGMIR     |      2.57 | terribly     |    291,732 | terribly_clear             |   1.00 |       12.43 |     15 |    0.83 |            2.18 |      52.91 |    1.20 |         4,610 |   0.77 |         6,722 |  1,701,929 |   3.21 |     15 | clear          |
| **NEGmir~inherently_evil**            | NEGMIR     |     16.97 | inherently   |    291,732 | inherently_evil            |   0.59 |       41.03 |     99 |    0.41 |            0.83 |      85.70 |    1.18 |         5,133 |   0.53 |         1,271 |  1,701,929 |   5.39 |     58 | evil           |
| **NEGany~inherently_problematic**     | NEGATED    |     12.07 | inherently   |  3,173,660 | inherently_problematic     |   0.21 |       45.93 |    277 |    0.17 |            0.77 |      98.70 |    1.17 |        47,803 |   0.68 |        33,408 | 72,839,589 |   6.03 |     58 | problematic    |
| **NEGmir~immediately_clear**          | NEGMIR     |      7.37 | immediately  |    291,732 | immediately_clear          |   0.72 |       23.63 |     43 |    0.55 |            1.09 |      62.95 |    1.13 |         1,195 |   0.62 |         6,722 |  1,701,929 |   4.24 |     31 | clear          |
| **NEGmir~terribly_remarkable**        | NEGMIR     |      2.40 | terribly     |    291,732 | terribly_remarkable        |   1.00 |       11.60 |     14 |    0.83 |            2.15 |      49.38 |    1.03 |         4,610 |   0.77 |         3,238 |  1,701,929 |   3.10 |     14 | remarkable     |
| **NEGmir~remotely_new**               | NEGMIR     |      3.77 | remotely     |    291,732 | remotely_new               |   0.86 |       15.23 |     22 |    0.69 |            1.43 |      50.62 |    1.00 |         2,341 |   0.70 |        12,836 |  1,701,929 |   3.49 |     19 | new            |




```python
nb_show_table(NEG_bigrams_sample.l1.value_counts().to_frame('subtotal in selected bigrams'))
```

    
    |                |   `subtotal in selected bigrams` |
    |:---------------|---------------------------------:|
    | **NEGATED**    |                              106 |
    | **NEGMIR**     |                               84 |
    | **COMPLEMENT** |                                1 |
    



|                |   `subtotal in selected bigrams` |
|:---------------|---------------------------------:|
| **NEGATED**    |                              106 |
| **NEGMIR**     |                               84 |
| **COMPLEMENT** |                                1 |




```python
nb_show_table(NEG_bigrams_sample.filter(like='O', axis=0).T)
```

    
    |                 | `COM~ever_closer`    |
    |:----------------|:---------------------|
    | **l1**          | COMPLEMENT           |
    | **exp_f**       | 6031.9241            |
    | **adv**         | ever                 |
    | **f1**          | 69662736             |
    | **l2**          | ever_closer          |
    | **P1**          | 0.9996829032897949   |
    | **unexp_f**     | 273.0758999999998    |
    | **f2**          | 6307                 |
    | **dP1**         | 0.043301016092300415 |
    | **odds_r_disc** | 2.0608150959014893   |
    | **G2**          | 538.66082            |
    | **LRC**         | 3.5134613513946533   |
    | **adv_total**   | 114075               |
    | **MI**          | 0.019229218363761902 |
    | **adj_total**   | 61475                |
    | **N**           | 72839589             |
    | **t**           | 3.439067840576172    |
    | **f**           | 6305                 |
    | **adj**         | closer               |
    


```python
nb_show_table(NEG_bigrams_sample.filter(like='O', axis=0).T)
```
(_+ manual sort & round_)

|                 | `COM~ever_closer` |
|:----------------|------------------:|
| **N**           |        72,839,589 |
| **f**           |             6,305 |
| **l1**          |        COMPLEMENT |
| **l2**          |       ever_closer |
| **f1**          |        69,662,736 |
| **f2**          |             6,307 |
| **adv**         |              ever |
| **adj**         |            closer |
| **adv_total**   |           114,075 |
| **adj_total**   |            61,475 |
| **exp_f**       |             6,032 |
| **unexp_f**     |               273 |
| **P1**          |            0.9997 |
| **dP1**         |            0.0433 |
| **LRC**         |              3.51 |
| **G2**          |             538.6 |
| **odds_r_disc** |              2.06 |
| **MI**          |            0.0192 |
| **t**           |              3.44 |


