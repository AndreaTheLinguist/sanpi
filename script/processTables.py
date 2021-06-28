import os
import sys
import time
from collections import namedtuple
from itertools import repeat
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd

from tabulate import tabulate


def __main__():

    data_dir = "/home/andrea/litotes/hits"  # sys.argv[1]

    # TODO replace path with argument variable
    files = pd.DataFrame(([f.name, f.path]
                          for f in os.scandir(data_dir)),
                         columns=['name', 'path'])

    hits_files = files[files.name.str.contains('hits')]

    hits_files.loc[:, 'context'] = (
        hits_files.name
        .str.rsplit('_', 1).str.get(0)
        .str.split('_', 1).str.get(1)).astype('string')
    hits_files.loc[
        :, 'context_word'] = hits_files.context.str.split('_').str.get(0)
    hits_files.loc[
        :, 'context_type'] = hits_files.context.str.split('_').str.get(1)

    categories_dict = {
        'context': tuple(hits_files.context.unique()),
        'context_word': tuple(hits_files.context_word.unique()),
        'context_type': tuple(hits_files.context_type.unique())
    }

    # process basic pattern results first
    basic_dfs = list(generate_dataframes(hits_files, categories_dict,
                                         basic=True))

    baseline_hits = pd.concat(basic_dfs, ignore_index=True)

    base_hit_ids = baseline_hits.hit_id.unique()

    # process context pattern results
    context_dfs = list(
        generate_dataframes(hits_files, categories_dict, base_ids=base_hit_ids))

    cat_columns = ['colloc', 'adv', 'adj',
                   'context', 'context_word', 'context_type']

    # combine dataframes for each individual context's results
    combined_contexts = pd.concat(context_dfs, ignore_index=True)
    combined_contexts.loc[:, 'polarity'] = 'negative'

    # cannot do the following unless script is modified to deal with subdirs...
    #  but if it is, polarity should just be set based on subdir in the generate_dataframes()
    # combined_contexts.loc[
    #     combined_contexts.context_word.isin(
    #         ['every', 'everyone', 'everybody', 'few'])
    # ].loc[:, 'polarity'] = 'uncertain'

    # reset categories
    combined_contexts.loc[
        :, cat_columns
    ] = combined_contexts.loc[:, cat_columns].astype("category")

    # get basic hits that are not caught by any specific context
    positive_df = baseline_hits[
        ~baseline_hits.hit_id.isin(combined_contexts.hit_id)]

    # mark these hits as "positive" context
    positive_df.loc[:, 'context'] = positive_df.context.str.replace(
        'basic', 'positive')
    positive_df.loc[:, 'polarity'] = 'positive'

    all_contexts = pd.concat([combined_contexts, positive_df],
                             ignore_index=True)

    all_contexts['context_overlap'] = (
        all_contexts.groupby('hit_id').hit_id.transform('count') > 1)

    no_overlap = all_contexts[~all_contexts.context_overlap]

    print(f'{len(all_contexts) - len(no_overlap)} overlapping hits excluded')

    cat_columns.append('polarity')

    no_overlap.loc[
        :, cat_columns
    ] = no_overlap.loc[:, cat_columns].astype("category")

    # save dataframe

    no_overlap.to_pickle("no_overlap_data.pkl.gz")

    no_overlap.sample(n=5000).sort_values(by="colloc").to_csv(
        'processed_data_sample.csv', index=False)


def generate_dataframes(files_df, categories, basic=False, base_ids=None):

    for k, v in categories.items():

        try:
            categories[k] = pd.CategoricalDtype(v)

        except TypeError:
            pass

    dtype_dict = {
        'hit_id': 'string',
        'colloc': 'category',
        'adv': 'category',
        'adj': 'category',
        'sent_text': 'string',
        'sent_id': 'string',
        'adv_index': 'uint8'
    }

    if basic:

        files_df = files_df[files_df.name.str.contains('basic')]

    else:

        files_df = files_df[~files_df.name.str.contains('basic')]

        # assumes these are defined in categories dict for non-basic case
        # dtype_dict['colloc'] = categories['colloc']
        # dtype_dict['adv'] = categories['adv']
        # dtype_dict['adj'] = categories['adj']

    for i in files_df.index:

        df = pd.read_csv(files_df.at[i, 'path'], dtype=dtype_dict)

        df.loc[:, 'corpus_segment'] = df.sent_id.str.rsplit(
            '_', 2).str.get(0).astype('category')
        df.loc[:, 'date'] = df.corpus_segment.str.rsplit('_', 1).str.get(1)
        df.loc[:, 'date'] = pd.to_datetime(df.date, format='%Y%m%d')
        df.loc[:, 'year'] = pd.to_numeric(df.date.dt.year, downcast='unsigned')

        df.loc[:, 'context'] = files_df.at[i, 'context']
        df.context = df.context.astype(categories['context'])

        df.loc[:, 'context_word'] = files_df.at[i, 'context_word']
        df.context_word = df.context_word.astype(categories['context_word'])

        df.loc[:, 'context_type'] = files_df.at[i, 'context_type']
        df.context_type = df.context_type.astype(categories['context_type'])

        # df.loc[:, 'raw_colloc_count'] = df.groupby(
        #     'colloc')['colloc'].transform('count').apply(pd.to_numeric, downcast='unsigned')

        df.loc[:, "in_basic"] = True if basic else df.hit_id.isin(base_ids)

        colloc_sorted_df = df.sort_values(by='colloc').reset_index().rename(
            columns={'index': 'line_in_source'})

        colloc_sorted_df['line_in_source'] = pd.to_numeric(
            colloc_sorted_df.line_in_source + 1, downcast='unsigned')

        # print(df.info())

        yield colloc_sorted_df


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round(absFinish - absStart, 3)} seconds')
