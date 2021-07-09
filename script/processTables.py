import os
import sys
import time
from collections import namedtuple
from itertools import repeat
from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate


def __main__():

    try:
        data_dir = Path.cwd() / "hits"
    except OSError:
        exit('/hits/ directory not found. Run the script from the level above your hits directory (i.e. directory containing hit info for all contexts, 1 file per context/pattern match)')

    try:
        os.mkdir(Path.cwd() / 'data_samples')
    except OSError:
        pass
    sample_dir = Path.cwd() / 'data_samples'

    files = pd.DataFrame()
    for pol_dir in data_dir.iterdir():

        polarity = pol_dir.name

        file_info_list = [[f.stem, f, polarity,
                           f.stem.rsplit('_', 1)[0].split('_', 1)[1]]
                          for f in pol_dir.iterdir()
                          if f.stem.endswith('hits')]

        pol_df = pd.DataFrame(file_info_list,
                              columns=['name', 'path', 'polarity', 'context'])

        files = files.append(pol_df, ignore_index=True)

    files.loc[
        :, 'context_word'] = files.context.str.split('_').str.get(0)
    files.loc[
        :, 'context_type'] = files.context.str.split('_').str.get(1)

    categories_dict = {
        'context': tuple(files.context.unique()),
        'context_word': tuple(files.context_word.unique()),
        'context_type': tuple(files.context_type.unique()),
        'polarity': tuple(files.polarity.unique())
    }

    for k, v in categories_dict.items():
        try:
            categories_dict[k] = pd.CategoricalDtype(v)
        except TypeError:
            pass

    # process basic pattern results first
    basic_dfs = list(generate_dataframes(files, categories_dict, basic=True))

    baseline_hits = pd.concat(basic_dfs, ignore_index=True)

    base_hit_ids = baseline_hits.hit_id.unique()

    # process context pattern results
    context_dfs = list(
        generate_dataframes(files, categories_dict, base_ids=base_hit_ids))

    cat_columns = ['colloc', 'adv', 'adj', 'polarity',
                   'context', 'context_word', 'context_type']

    # combine dataframes for each individual context's results
    combined_contexts = pd.concat(context_dfs, ignore_index=True)

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

    # if more than one element in any "hit_id" group,
    # this means the hit_id matched more than 1 pattern/context;
    # set 'context_overlap' to True for hit
    all_contexts['context_overlap'] = (
        all_contexts.groupby('hit_id').hit_id.transform('count') > 1)

    # (for now) ignore hits with any context overlap
    no_overlap = all_contexts[~all_contexts.context_overlap]

    print(f'{len(all_contexts) - len(no_overlap)} overlapping hits excluded')

    # reset categories again
    no_overlap.loc[:, cat_columns
                   ] = no_overlap.loc[:, cat_columns].astype("category")

    # save dataframe to file
    no_overlap.to_pickle("no_overlap_data.pkl.gz")

    # create sample for easy viewing on github
    no_overlap.sample(n=1000).sort_values(by="colloc").to_csv(
        sample_dir / 'no-overlap-data_1000rows.csv', index=False)


def generate_dataframes(files_df: pd.DataFrame,
                        categories: dict,
                        basic: bool = False,
                        base_ids: list = None):

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

        files_df = files_df[files_df.polarity == 'basic']

    else:

        files_df = files_df[files_df.polarity != 'basic']

    for i in files_df.index:

        df = pd.read_csv(files_df.at[i, 'path'], dtype=dtype_dict)

        df.loc[:, 'corpus_segment'] = df.sent_id.str.rsplit(
            '_', 2).str.get(0).astype('category')
        df.loc[:, 'date'] = df.corpus_segment.str.rsplit('_', 1).str.get(1)
        df.loc[:, 'date'] = pd.to_datetime(df.date, format='%Y%m%d')
        df.loc[:, 'year'] = pd.to_numeric(df.date.dt.year, downcast='unsigned')

        df.loc[:, 'polarity'] = files_df.at[i, 'polarity']
        df.loc[:, 'polarity'] = df.polarity.astype(categories['polarity'])

        df.loc[:, 'context'] = files_df.at[i, 'context']
        df.loc[:, 'context'] = df.context.astype(categories['context'])

        df.loc[:, 'context_word'] = files_df.at[i, 'context_word']
        df.loc[:, 'context_word'] = df.context_word.astype(
            categories['context_word'])

        df.loc[:, 'context_type'] = files_df.at[i, 'context_type']
        df.loc[:, 'context_type'] = df.context_type.astype(
            categories['context_type'])

        df.loc[:, "in_basic"] = True if basic else df.hit_id.isin(base_ids)

        colloc_sorted_df = df.sort_values(by='colloc').reset_index().rename(
            columns={'index': 'line_in_source'})

        colloc_sorted_df['line_in_source'] = pd.to_numeric(
            colloc_sorted_df.line_in_source + 1, downcast='unsigned')

        yield colloc_sorted_df


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round(absFinish - absStart, 3)} seconds')
