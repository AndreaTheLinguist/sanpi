import pandas as pd
from scipy.stats import entropy
import scipy
import matplotlib


def get_divs(unk: pd.DataFrame, neg: pd.Series, pos: pd.Series, reversed=False):

    base = 2

    if reversed:
        neg_divs = unk.apply(lambda x: entropy(neg, x, base=base))
        pos_divs = unk.apply(lambda x: entropy(pos, x, base=base))

    else:
        neg_divs = unk.apply(lambda x: entropy(x, neg, base=base))
        pos_divs = unk.apply(lambda x: entropy(x, pos, base=base))

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
    '/home/andrea/litotes/individual-contexts_freq-table.pkl.gz')

every_counts = unknown.loc[:, unknown.columns.str.contains('every')]
every_combined_dist = every_counts.sum(1)

few_counts = unknown.loc[:, unknown.columns.str.contains('few')]
few_combined_dist = few_counts.sum(1)

unk = unknown.sort_index(1)
combined = pd.concat({'every_combined': every_combined_dist,
                      'few_combined': few_combined_dist}, axis=1)
unk_extended = unk.join(combined)

# technically do not have to normalize manually, and,
# if data threshold > 0, do not need to use plus1 columns
#   buuuuut, trimmed data is not the right length to compare

# neg_dist = known.negative_plus1
# pos_dist = known.positive_plus1
# TODO see if this works!!!
num_colloc_types = len(known)

neg_dist = known.negative_raw
neg_dist += neg_dist.sum()/num_colloc_types

pos_dist = known.positive_raw
pos_dist += pos_dist.sum()/num_colloc_types

print('Relative entropy: Positive | | Negative = ',
      round(entropy(pos_dist, neg_dist, base=2), 4))
print('Relative entropy: Negative | | Positive = ',
      round(entropy(neg_dist, pos_dist, base=2), 4))

unk_smoothed = unk_extended.apply(lambda x: x + (x.sum()/num_colloc_types))

divergence = get_divs(unk_smoothed, neg_dist, pos_dist)

print('\nunknown given to entropy() first:\n', divergence.round(2))

print('\nknown given to entropy() first:\n', get_divs(
    unk_smoothed, neg_dist, pos_dist, reversed=True).round(2))

divergence.round(4).to_csv('data_samples/preliminary_KLdiv_table.csv')
# neg_every_div = entropy(neg_dist, every_combined_dist, base=2)
# pos_every_div = entropy(pos_dist, every_combined_dist, base=2)

# neg_few_div = entropy(neg_dist, few_combined_dist, base=2)
# pos_few_div = entropy(pos_dist, few_combined_dist, base=2)

# neg_divs = unknown.apply(lambda x: entropy(neg_dist, x.add(1), base=2))
