'''
    This script loads a dataframe of all non-overlapping collocation tokens. All tokens that matched more than a single *informative* context (e.g. not basic, unrestricted pattern matches) are excluded from these data.

    This script outputs various "samples" of data for quick illustration, as well as various frequency table dataframes (pickled and compressed) generated via `pandas.crosstab`:
        1. all contexts, raw counts
        2. all contexts, what proportion of colloc each context accounts for
        3. all contexts, what proportion of context each colloc accounts for
        4. text cases (contexts with uncertain polarity), raw counts
        5. counts and various normalized metrics for 2 defined polarity context groups: positive and negative
'''


import os
import sys
import time
from collections import namedtuple
from itertools import repeat
from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd


def __main__():

    try:
        os.mkdir(Path.cwd() / 'data_samples')
    except OSError:
        pass
    sample_dir = Path.cwd() / 'data_samples'

    # TODO: make this path an argument instead of fixed?
    no_overlap = pd.read_pickle("no_overlap_data.pkl.gz")
    data = no_overlap.loc[:, ['colloc', 'context', 'adv', 'adj', 'polarity']]

    positive_contexts = data[
        data.polarity == 'positive'].context.unique()

    negative_contexts = data[
        data.polarity == 'negative'].context.unique()

    test_contexts = data[
        data.polarity == 'uncertain'].context.unique()

    data.describe()

    # writes samples files to sample_dir and returns frequency table dataframe(s)
    collocs_by_context = basic_freq_table(data, sample_dir)
    prop_of_colloc, prop_of_context = calc_proportions(data, sample_dir)

    # select rows via list of context (column) labels and get sum by row
    negative_counts = collocs_by_context[negative_contexts
                                         ].sum(axis=1)
    positive_counts = collocs_by_context[positive_contexts
                                         ].sum(axis=1)

    summarize_pos_neg(negative_counts, positive_counts, sample_dir)

    test_data = collocs_by_context[test_contexts]
    test_data.to_pickle("test-contexts_freq-table.pkl.gz")
    test_data.sample(n=500).to_csv(
        sample_dir / 'test-contexts-freq_500rows.csv')


def basic_freq_table(data: pd.DataFrame, sample_dir=Path.cwd()):

    # get frequency table
    collocs_by_context = pd.crosstab(
        data.colloc, data.context)

    # write full frequency table to file (compressed pickle format)
    collocs_by_context.to_pickle("individual-contexts_freq-table.pkl.gz")
    # write sample csv for easy illustration
    collocs_by_context.sample(n=500).sort_index().to_csv(
        sample_dir / 'freq_500rows.csv')

    # +1 smoothing
    counts_plus_one = collocs_by_context.add(1)
    counts_plus_one.sample(n=500).sort_index().to_csv(
        sample_dir / 'freq_plus-one_500rows.csv')

    return collocs_by_context


def calc_proportions(data: pd.DataFrame, sample_dir=Path.cwd()):

    # shows what proportion of the colloc falls in each context
    proportion_of_colloc = pd.crosstab(
        data.colloc, data.context, margins=True, margins_name='all_collocs', normalize='index')
    colloc_prop_sample = proportion_of_colloc.sample(
        n=500).append(proportion_of_colloc.loc["all_collocs", :])

    # write sample file
    colloc_prop_sample.to_csv(
        sample_dir / "collocProportion_500plusTotalRow.csv")

    # shows what proportion of the context falls in each colloc
    proportion_of_context = pd.crosstab(
        data.colloc, data.context, margins=True, margins_name='all_contexts', normalize='columns')
    context_prop_sample = proportion_of_context.sample(
        n=500)

    # write sample file
    context_prop_sample.to_csv(
        sample_dir / "contextProportion_500rows.csv")

    return proportion_of_colloc, proportion_of_context


def summarize_pos_neg(negative, positive, sample_dir=Path.cwd()):

    # raw counts seed dataframe
    counts_raw = pd.DataFrame(
        {'positive_raw': positive,
         "negative_raw": negative})

    # add "total" column (cannot add row due to category type limitations)
    counts_raw["total_raw"] = counts_raw.sum(axis=1)

    # +1 smoothing counts dataframe
    counts_plus1 = pd.DataFrame(
        {'positive_plus1': positive,
         "negative_plus1": negative}).add(1)

    # combined raw and +1 smoothed counts dataframe
    simplified = counts_raw.join(counts_plus1)

    simplified["positive_ratio"] = round(
        simplified.positive_raw / simplified.total_raw, 4)
    simplified["negative_ratio"] = round(
        simplified.negative_raw / simplified.total_raw, 4)

    positive_skew = sum(positive)/sum(simplified.total_raw)
    negative_skew = sum(negative)/sum(simplified.total_raw)

    simplified["positive_skew"] = round(
        simplified.positive_ratio/positive_skew, 4)
    simplified["negative_skew"] = round(
        simplified.negative_ratio/negative_skew, 4)

    simplified = simplified.sort_values(by="positive_skew").sort_values(
        by="negative_skew", ascending=False)

    simplified.to_pickle('pos-neg-split_freq-table.pkl.gz')
    simplified.iloc[:500, :].to_csv(
        sample_dir / 'pos-neg-split_top500neg.csv')
    simplified.sort_values(
        by="positive_skew", ascending=False).iloc[:500, :].to_csv(
            sample_dir / 'pos-neg-split_top500pos.csv')


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round(absFinish - absStart, 3)} seconds')
