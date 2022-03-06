# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Sanity Check
# %% [markdown]
#
# That was only testing 'every' contexts though, as the "unknowns". Let's do a sanity check: how much do distributions which we *know* are negative diverge from the rest of the negative data?
#
# ### `no` vs. all other negative cases
# %% [markdown]
# ---
#
# ---

# %%
import pandas as pd
from scipy.stats import entropy
import numpy as np
import matplotlib_inline as mplot
import itertools
from sys import argv


# %%
# copied from `getFrequencies.py` and then modified slightly
def basic_freq_table(data: pd.DataFrame, label: str, mode: str = 'colloc'):
    if mode == 'colloc':
        crosstab_rows = data.colloc
    elif mode == 'adv':
        crosstab_rows = data.adv  # _word
    elif mode == 'adj':
        crosstab_rows = data.adj  # _word

    # get frequency table
    by_context = pd.crosstab(
        crosstab_rows, data.context).apply(pd.to_numeric, downcast="unsigned")
    with_sum = by_context.assign(COMBINED=by_context.sum(axis=1))
    sum2 = with_sum.sum()
    sum2.name = 'SUM'
    with_sum = with_sum.append(sum2)
    with_sum = (with_sum
                .sort_values('COMBINED', ascending=False)
                .sort_values(by='SUM', axis=1, ascending=False))
    # print('>>>', name, mode, 'frequencies')
    # print(with_sum.head(11))
    new_label = f'{label[0:3].upper()}_COMBINED'

    with_sum.columns = with_sum.columns.str.replace('COMBINED', new_label)

    return with_sum


# %%
# load nonoverlapping hits dataframe
try:
    context_subset = [argv[1]]
except:

    context_subset = ['no', 'nobody', 'no-one']

input_pkl = "compiled_hits.pkl.gz"

compiled = pd.read_pickle(input_pkl)
hits = compiled.loc[:, ['colloc', 'context', 'context_word',
                        'context_type', 'context_group', 'adv', 'adj', 'polarity']]


# %%
pos_hits = hits[hits.polarity == 'positive']
neg_hits = hits[hits.polarity == 'negative']


# %%
other_neg_hits, test_hits = [x for _, x in neg_hits.groupby(
    neg_hits.context_word.isin(context_subset))]

other_neg_hits.context.unique().to_list()


# %%
test_hits.context.unique().to_list()

# %% [markdown]
# colloc-by-context frequency tables could be calculated from pre-divided groups, or all together, and then select from the count columns based on context.
#
# First, from all the hits together:

# %%
all_counts = basic_freq_table(hits, label='all')
all_counts.head(11)


# %%
pos_counts = basic_freq_table(pos_hits, label='positive')
print(pos_counts)


# %%
neg_main_counts = basic_freq_table(other_neg_hits, label='negative')
print(neg_main_counts)


# %%
test_counts = basic_freq_table(test_hits, label='test')
print(test_counts)


# %%
san_chk = pos_counts.join(neg_main_counts).join(test_counts)
san_chk = san_chk.loc[:, san_chk.columns.str.contains('COMBINED')].fillna(0)
san_chk = san_chk.assign(TOTAL=san_chk.sum(axis=1)).convert_dtypes()
print(san_chk.sort_values('TES_COMBINED', ascending=False))

# %% [markdown]
# An overly simplified sanity check perhaps, but how do the subset `COMBINED` columns compare to the superset column `TOTAL`?

# %%
san_chk = san_chk.add(1)


# %%
def column_divergence(df, col):
    div_df = pd.DataFrame()
    for c1, c2 in itertools.permutations(col, 2):
        l1 = df[c1].to_list()

        l2 = df[c2].to_list()
        kldiv = round(entropy(l1, l2), 3)
        print(c1, 'KLdiv from', c2, '=', kldiv)

        div_df.loc[c1+'_KLdiv', 'from_'+c2] = kldiv

    return div_df.fillna(0).convert_dtypes()


# %%
col = san_chk.columns.to_list()
div_table = column_divergence(san_chk, col)
print('---\nKL Divergence between *all* columns')
print(div_table)


# %% [markdown]
# We see that total doesn't diverge from itself (as should be the the case), but this also shows that the larger the subset is, the less it diverges from the superset. This also makes sense: the bigger the contribution, the better the final distribution will represent that contribution.
#
# But how do the subdistributions compare to each other?

# %%
col = san_chk.columns.to_list()
col.pop(-1)
div_table = column_divergence(san_chk, col)
print('---\nKL Divergence between data subgroup columns')
print(div_table)
