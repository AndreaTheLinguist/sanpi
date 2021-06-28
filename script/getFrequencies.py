import os
import sys
import time
from collections import namedtuple
from itertools import repeat
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd


def __main__():

    no_overlap = pd.read_pickle("no_overlap_data.pkl.gz")
    data = no_overlap.loc[:, ['colloc', 'context', 'adv', 'adj', 'polarity']]

    # temp fix til processTables does this based on subdir
    # mixed boolean indexing works bc only width differs, not height
    data.loc[:,'polarity'] = data.polarity.cat.add_categories(['uncertain'])
    data.loc[
        no_overlap.context_word.isin(
            ['every', 'everyone', 'everybody', 'few']),
        'polarity'] = 'uncertain'

    positive_contexts = data[data.polarity ==
                             'positive'].context.unique()

    negative_contexts = data[data.polarity ==
                             'negative'].context.unique()
    # get frequency table
    collocs_by_context = pd.crosstab(
        data.colloc, data.context)

    collocs_by_context.to_pickle("freq_table.pkl.gz")
    collocs_by_context.sample(n=500).sort_index().to_csv(
        'freq_sample500.csv')

    # +1 smoothing
    counts_plus_one = collocs_by_context.add(1)
    counts_plus_one.sample(n=500).sort_index().to_csv(
        'freq_plus-one_sample500.csv')

    # # shows what proportion of the colloc falls in each context
    # proportion_of_colloc = pd.crosstab(
    #     sample_data.colloc, sample_data.context, margins=True, margins_name='total', normalize='index')

    # # shows what proportion of the context falls in each colloc
    # proportion_of_context = pd.crosstab(
    #     sample_data.colloc, sample_data.context, margins=True, margins_name='total', normalize='columns')

    # proportion_of_colloc_sorted = proportion_of_colloc.sort_values(
    #     by="positive")

    negative_counts = collocs_by_context[
        negative_contexts].sum(axis=1)

    positive_counts = collocs_by_context[
        positive_contexts].sum(axis=1)

    simplified = pd.DataFrame(
        {'positive_raw': positive_counts,
         "negative_raw": negative_counts}).add(1)

    # simplified["positive_percent"
    #            ] = simplified.positive_raw / sum(positive_counts) * 100
    # simplified['negative_percent'
    #            ] = simplified.negative_raw / sum(negative_counts) * 100
    simplified["total"] = simplified.sum(axis=1)
    positive_skew = sum(positive_counts)/sum(simplified.total)
    negative_skew = sum(negative_counts)/sum(simplified.total)

    simplified["positive_ratio"] = round(
        simplified.positive_raw / simplified.total, 4)

    simplified["negative_ratio"] = round(
        simplified.negative_raw / simplified.total, 4)

    simplified["positive_skew"] = round(
        simplified.positive_ratio/positive_skew, 4)

    simplified["negative_skew"] = round(
        simplified.negative_ratio/negative_skew, 4)

    simplified = simplified.sort_values(by="negative_skew", ascending=False)

    simplified.to_pickle('prelim_summary_table.pkl.gz')
    simplified.iloc[:500, :].to_csv('prelim_summary_top500.csv')

    # counts_df = sample_data.value_counts()
    # # .to_frame().reset_index().rename(columns={0: 'counts'})

    # percents_df = sample_data.value_counts(
    #     sort=False, normalize=True).to_frame().reset_index().rename(columns={0: 'percent'})

    # counts_df.percents.plot(kind='bar')
    # plt.show()

    # no_overlap.loc[:, "total_colloc_count"] = (
    #     no_overlap.groupby(['colloc'])['colloc']
    #     .transform('count')
    #     .apply(pd.to_numeric, downcast='unsigned')
    # )

    # no_overlap.loc[:, "context_colloc_count"] = (
    #     no_overlap.groupby(['colloc', 'context'])['colloc']
    #     .transform('count')
    #     .apply(pd.to_numeric, downcast='unsigned')
    # )

    # colloc_lexicon = no_overlap.colloc.unique().sort_values()
    # context_list = no_overlap.context.unique().sort_values()

    # write tables to file


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round(absFinish - absStart, 3)} seconds')
