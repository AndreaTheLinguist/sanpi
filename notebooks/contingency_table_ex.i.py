# %%
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

# %%

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

# %%
print_ex = ex_3x3.copy()
print_ex.index.name = None
print_ex.index = '***' + print_ex.index + '***'
print_ex.columns = '*' + print_ex.columns + '*'
print(print_md_table(print_ex.rename(
    columns={'*SUM*': '`SUM`'}, index={'***SUM***': '**`SUM`**'}), suppress=True))

# %% [markdown]
# |                 |      `SUM` |   *seemingly* |   *commercially* |   *strictly* |
# |:----------------|-----------:|--------------:|-----------------:|-------------:|
# | **`SUM`**       | 83,284,343 |       162,309 |           33,305 |       35,061 |
# | ***efficient*** |    254,637 |            13 |               12 |            1 |
# | ***personal***  |    126,037 |            87 |                0 |          499 |
# | ***great***     |    379,200 |           184 |                3 |            1 |
#

# %%
# import association_measures.measures as am
# import association_measures.frequencies as fq
# from source.utils.lsc_prep import flatten_freq_table as prep_freqs
# prep_freqs(ex_3x3)

# %%
N = ex_3x3.at['SUM', 'SUM']
N


# %%
adv_margins = f1 = ex_3x3.iloc[0, 1:].T.to_frame('f1').reset_index()
adv_margins


# %%
adj_margins = f2 = ex_3x3.iloc[1:, 0].to_frame('f2').reset_index()
adj_margins

# %%
_ex_3x3 = drop_sums(ex_3x3.copy())
_ex_3x3

# %%
_ex_3x3 = _ex_3x3.unstack().to_frame('f').reset_index()
_ex_3x3

# %%


def merge_margins(_df, margins):
    margin_unit = margins.columns[0]
    return _df.merge(margins,
                    left_on=margin_unit,
                    right_on=margin_unit)


_ex_3x3 = merge_margins(merge_margins(_ex_3x3, f1), f2)
_ex_3x3

# %%
_ex_3x3 = _ex_3x3.assign(
    bigram=_ex_3x3.iloc[:, 0] + '_' + _ex_3x3.iloc[:, 1],
    N=N)
_ex_3x3

# %%
full_frq_ex = _ex_3x3.join(fq.observed_frequencies(
    _ex_3x3)).join(fq.expected_frequencies(_ex_3x3))
full_frq_ex

# %%
ex_row = full_frq_ex.sample(1).set_index('bigram')
ex_row.update(ex_row.select_dtypes('number').round(1))
ex_row.T

# %%
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

|    | *{adj_form_lower}* | $\\neg$ *{adj_form_lower}* | across all `ADV` |
|---:|---:|---:|---:|
| ***{adv_form_lower}*** | {O11:,.0f} | {O12:,.0f} | {adv_margin:,.0f} |
| **$\\neg$ *{adv_form_lower}*** | {O21:,.0f} | {O22:,.0f} | {adv_remainder:,.0f} |
| **across all `ADJ`** | {adj_margin:,.0f} | {adj_remainder:,.0f} | {N:,.0f} |'''

    print(contingency_md)


# %% [markdown]
# ```python
# print_contigencies_for_bigram(ex_row)
# ```
#
# ### Observed Contingencies for *strictly* + *personal*
#
# |    | *personal* | $\neg$ *personal* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***strictly*** | 499 | 34,562 | 35,061 |
# | **$\neg$ *strictly*** | 125,538 | 83,123,744 | 83,249,282 |
# | **across all `ADJ`** | 126,037 | 83,158,306 | 83,284,343 |
#

# %%
full_frq_ex.apply(print_contingencies_for_bigram, axis=1)

# %% [markdown]
#
# ### Observed Contingencies for *seemingly* + *efficient*
#
# |    | *efficient* | $\neg$ *efficient* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***seemingly*** | 13 | 162,296 | 162,309 |
# | **$\neg$ *seemingly*** | 254,624 | 82,867,410 | 83,122,034 |
# | **across all `ADJ`** | 254,637 | 83,029,706 | 83,284,343 |
#
# ### Observed Contingencies for *commercially* + *efficient*
#
# |    | *efficient* | $\neg$ *efficient* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***commercially*** | 12 | 33,293 | 33,305 |
# | **$\neg$ *commercially*** | 254,625 | 82,996,413 | 83,251,038 |
# | **across all `ADJ`** | 254,637 | 83,029,706 | 83,284,343 |
#
# ### Observed Contingencies for *strictly* + *efficient*
#
# |    | *efficient* | $\neg$ *efficient* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***strictly*** | 1 | 35,060 | 35,061 |
# | **$\neg$ *strictly*** | 254,636 | 82,994,646 | 83,249,282 |
# | **across all `ADJ`** | 254,637 | 83,029,706 | 83,284,343 |
#
# ### Observed Contingencies for *seemingly* + *personal*
#
# |    | *personal* | $\neg$ *personal* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***seemingly*** | 87 | 162,222 | 162,309 |
# | **$\neg$ *seemingly*** | 125,950 | 82,996,084 | 83,122,034 |
# | **across all `ADJ`** | 126,037 | 83,158,306 | 83,284,343 |
#
# ### Observed Contingencies for *commercially* + *personal*
#
# |    | *personal* | $\neg$ *personal* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***commercially*** | 0 | 33,305 | 33,305 |
# | **$\neg$ *commercially*** | 126,037 | 83,125,001 | 83,251,038 |
# | **across all `ADJ`** | 126,037 | 83,158,306 | 83,284,343 |
#
# ### Observed Contingencies for *strictly* + *personal*
#
# |    | *personal* | $\neg$ *personal* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***strictly*** | 499 | 34,562 | 35,061 |
# | **$\neg$ *strictly*** | 125,538 | 83,123,744 | 83,249,282 |
# | **across all `ADJ`** | 126,037 | 83,158,306 | 83,284,343 |
#
# ### Observed Contingencies for *seemingly* + *great*
#
# |    | *great* | $\neg$ *great* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***seemingly*** | 184 | 162,125 | 162,309 |
# | **$\neg$ *seemingly*** | 379,016 | 82,743,018 | 83,122,034 |
# | **across all `ADJ`** | 379,200 | 82,905,143 | 83,284,343 |
#
# ### Observed Contingencies for *commercially* + *great*
#
# |    | *great* | $\neg$ *great* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***commercially*** | 3 | 33,302 | 33,305 |
# | **$\neg$ *commercially*** | 379,197 | 82,871,841 | 83,251,038 |
# | **across all `ADJ`** | 379,200 | 82,905,143 | 83,284,343 |
#
# ### Observed Contingencies for *strictly* + *great*
#
# |    | *great* | $\neg$ *great* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***strictly*** | 1 | 35,060 | 35,061 |
# | **$\neg$ *strictly*** | 379,199 | 82,870,083 | 83,249,282 |
# | **across all `ADJ`** | 379,200 | 82,905,143 | 83,284,343 |
#
