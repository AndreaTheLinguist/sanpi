import pandas as pd
from scipy.stats import entropy


def get_divs(df, reversed=False):

    base = 2
    unk = df.iloc[:,:-2]

    if reversed:
        neg_divs = unk.apply(lambda x: entropy(df.neg, x, base=base))
        pos_divs = unk.apply(lambda x: entropy(df.pos, x, base=base))

    else:
        neg_divs = unk.apply(lambda x: entropy(x, df.neg, base=base))
        pos_divs = unk.apply(lambda x: entropy(x, df.pos, base=base))

    return pd.concat({'div_from_pos': pos_divs,
                      'div_from_neg': neg_divs,
                      'lean_toward_pos': neg_divs - pos_divs}, axis=1)


binary_split_all = pd.read_pickle(
    'positive-negative_thresh0_freq-table.pkl.gz')
# binary_split_trim = pd.read_pickle(
#     'positive-negative_thresh3_freq-table.pkl.gz')

known = binary_split_all  # trim
unknown = pd.read_pickle('test-contexts_freq-table.pkl.gz')
all = pd.read_pickle(
    '/home/andrea/litotes/all-contexts_freq-table.pkl.gz')


##TODO: add functionality of picking "test" data with a keyword input
every_counts = unknown.loc[:, unknown.columns.str.contains('every')].sum(1)

unk = unknown.sort_index(1)
# combined = pd.concat({'every_combined': every_combined_dist,
#                       }, axis=1)
unk_extended = unk.assign(every_combined=every_counts)

# technically do not have to normalize manually, and,
# if data threshold > 0, do not need to use plus1 columns
#   buuuuut, trimmed data is not the right length to compare

# neg_dist = known.negative_plus1
# pos_dist = known.positive_plus1
# TODO see if this works!!!
num_colloc_types = len(known)

neg_dist = known.negative_raw
# neg_dist += neg_dist.sum()/num_colloc_types

pos_dist = known.positive_raw
# pos_dist += pos_dist.sum()/num_colloc_types

# print('Relative entropy: Positive | | Negative = ',
#       round(entropy(pos_dist, neg_dist, base=2), 4))
# print('Relative entropy: Negative | | Positive = ',
#       round(entropy(neg_dist, pos_dist, base=2), 4))

df = unk_extended.assign(pos=pos_dist, neg=neg_dist).fillna(0)
df_smoothed = df.apply(lambda x: x + (x.sum()/num_colloc_types)).apply(pd.to_numeric, downcast='float')

divergence = get_divs(df_smoothed)

print('\nunknown given to entropy() first:\n', divergence.round(2))

print('\nknown given to entropy() first:\n', get_divs(
    df_smoothed, reversed=True).round(2))

divergence.round(4).to_csv('data_samples/preliminary_KLdiv_table.csv')
# neg_every_div = entropy(neg_dist, every_combined_dist, base=2)
# pos_every_div = entropy(pos_dist, every_combined_dist, base=2)

# neg_few_div = entropy(neg_dist, few_combined_dist, base=2)
# pos_few_div = entropy(pos_dist, few_combined_dist, base=2)

# neg_divs = unknown.apply(lambda x: entropy(neg_dist, x.add(1), base=2))
