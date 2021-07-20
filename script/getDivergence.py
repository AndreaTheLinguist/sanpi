import pandas as pd
from scipy.stats import entropy
import scipy
import matplotlib

binary_split_all = pd.read_pickle(
    'positive-negative_thresh0_freq-table.pkl.gz')
# binary_split_trim = pd.read_pickle(
#     'positive-negative_thresh3_freq-table.pkl.gz')

known = binary_split_all  # trim
unknown = pd.read_pickle('test-contexts_freq-table.pkl.gz')

every_counts = unknown.loc[:, unknown.columns.str.contains('every')]
every_combined_dist = every_counts.sum(1).add(1)

few_counts = unknown.loc[:, unknown.columns.str.contains('few')]
few_combined_dist = few_counts.sum(1).add(1)

unk_p1 = unknown.add(1).sort_index(1)
combined = pd.concat({'every_combined': every_combined_dist,
                      'few_combined': few_combined_dist}, axis=1)
unk = unk_p1.join(combined)

# technically do not have to normalize manually, and,
# if data threshold > 0, do not need to use plus1 columns
#   buuuuut, trimmed data is not the right length to compare
neg_dist = known.negative_plus1
pos_dist = known.positive_plus1

print('Relative entropy: Positive | | Negative = ',
      round(entropy(pos_dist, neg_dist, base=2), 4))
print('Relative entropy: Negative | | Positive = ',
      round(entropy(neg_dist, pos_dist, base=2), 4))


neg_divs = unk.apply(lambda x: entropy(neg_dist, x, base=2))
pos_divs = unk.apply(lambda x: entropy(pos_dist, x, base=2))

divergence = pd.concat({'div_from_pos': pos_divs,
                        'div_from_neg': neg_divs}, axis=1)

divergence.loc[:, "difference"] = pos_divs - neg_divs

print(divergence.round(3))
# neg_every_div = entropy(neg_dist, every_combined_dist, base=2)
# pos_every_div = entropy(pos_dist, every_combined_dist, base=2)

# neg_few_div = entropy(neg_dist, few_combined_dist, base=2)
# pos_few_div = entropy(pos_dist, few_combined_dist, base=2)

# neg_divs = unknown.apply(lambda x: entropy(neg_dist, x.add(1), base=2))
