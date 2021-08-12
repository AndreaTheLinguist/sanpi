"""
    This script loads the `hits/` directory and processes all data matching 
    the specificed pattern: `[NA]*_hits.csv` 
    (e.g. files generated from test corpus directories will be ignored)

    Subdirectory names are pulled for pattern/context grouping 
    information, as well as polarity information. Directories 
    must start with 'bas', 'neg', or 'unk' to be included in 
    processing. E.g. devel(opment) dirs will be ignored.

    outputs several pkl or csv files to the project home directory 
    as well as several sample csv files to the defined "sample_dir".
"""

import sys
import time
from collections import namedtuple
from pathlib import Path

import pandas as pd


sample_dir = Path.cwd() / 'data_samples'
if not sample_dir.exists():
    sample_dir.mkdir()

data_dir = Path(Path.cwd() / "hits")
if not data_dir.exists():
    sys.exit('/hits/ directory not found. *Be sure to run this script from '
             'the level above your hits directory')

cat_columns = [
    'colloc', 'adv', 'adj', 'polarity', 'context_group', 'context', 'context_word', 'context_type', 'corpus', 'corpus_segment']


def __main__():

    # files = process_file_info()

    # categories_dict = set_categories(files)

    # # process basic pattern results first
    # baseline_hits, combined_contexts = process_hit_csvs(files, categories_dict)

    # # get basic hits that are not caught by any specific context
    # all_contexts = coordinate_dataframes(baseline_hits, combined_contexts)

    all_contexts = pd.read_pickle("all-contexts_with-overlap.pkl.gz")

    # remove hits that were selected for more than one context pattern
    no_overlap = filter_context_overlap(all_contexts)

    # remove hits which duplicate sentence all sentence info
    no_overlap_or_duplicates = filter_duplicate_text(no_overlap)

    # save dataframe to file
    print('Saving dataframe in .pkl.gz format ...')
    no_overlap_or_duplicates.to_pickle("compiled_hits.pkl.gz")
    print(
        f'>>>> {len(no_overlap_or_duplicates)} remaining hits saved to "compiled_hits.pkl.gz"')

    # create samples for easy viewing on github
    create_samples(no_overlap_or_duplicates)


def process_file_info():
    files = pd.DataFrame()
    file_info = namedtuple('file_info', ['name', 'path', 'context_group',
                                         'polarity', 'corpus', 'context_word', 'context_type'])
    for grp_dir in data_dir.iterdir():

        contextgrp = grp_dir.name
        if contextgrp.startswith('neg'):
            polarity = 'negative'
        elif contextgrp.startswith('unk'):
            polarity = 'unknown'
        elif contextgrp.startswith('bas'):
            polarity = 'mixed'
        # if not designated category type (e.g. testing dirs)
        # or if prefilter (super set of all data), skip
        else:
            continue

        file_info_list = []
        # exluding duplicates and test/quicktest files
        # /including only Nyt1/2 and Apw
        for f in grp_dir.glob('[AN]*_hits.csv'):

            name_parts = f.stem.split('_', )[:-1]
            file_info_list.append(file_info(f.stem, f, contextgrp,
                                            polarity, *name_parts))
        if not file_info_list:
            print(f'Warning: {grp_dir} had no files ending in "_hits.csv".')
            continue

        files = files.append(pd.DataFrame(file_info_list),
                             ignore_index=True)
        files = files.assign(context=(files.context_word +
                                      '_' + files.context_type))
    return files


def set_categories(files):
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
    return categories_dict


def process_hit_csvs(files, categories_dict):
    # process basic pattern results first
    basic_gen = generate_dataframes(files, categories_dict, basic=True)

    baseline_hits = pd.concat(list(basic_gen), ignore_index=True)

    base_hit_ids = baseline_hits.hit_id.unique()

    # process context pattern results
    context_dfs = list(generate_dataframes(files, categories_dict,
                                           base_ids=base_hit_ids))

    # combine dataframes for each individual context's results
    combined_contexts = pd.concat(context_dfs, ignore_index=True)

    # reset categories
    combined_contexts.loc[
        :, cat_columns
    ] = combined_contexts.loc[:, cat_columns].astype("category")
    return baseline_hits, combined_contexts


def generate_dataframes(files_df: pd.DataFrame,
                        categories: dict,
                        basic: bool = False,
                        base_ids: list = None):

    dtype_dict = {
        'hit_id': 'string',
        'colloc': 'category',
        'adv': 'category',
        'adj': 'category',
        'category': 'category',
        'sent_text': 'string',
        'sent_id': 'string',
        'adv_index': 'uint8',
        'json_source': 'category',
        'prev_sent': 'string',
        'next_sent': 'string'
    }

    if basic:

        files_df = files_df[files_df.context_group == 'basic']

    else:

        files_df = files_df[files_df.context_group != 'basic']

    for i in files_df.index:

        df = (pd.read_csv(files_df.at[i, 'path'], dtype=dtype_dict))

        if 'category' not in df.columns:
            df = df.assign(context_group='outdated_input_file')

        df = df.rename(columns={'category': 'context_group'})

        df = df.assign(
            corpus_segment=df.sent_id.str.rsplit(
                '_', 2).str.get(0).astype('category'),
        )

        df = df.assign(
            corpus=files_df.at[i, 'corpus'],
            date=df.corpus_segment.str.rsplit('_', 1).str.get(1),
            polarity=files_df.at[i, 'polarity'],
            context=files_df.at[i, 'context'],
            context_word=files_df.at[i, 'context_word'],
            context_type=files_df.at[i, 'context_type'],
            in_basic=True if basic else df.hit_id.isin(base_ids)
        )

        df = df.assign(date=pd.to_datetime(df.date, format='%Y%m%d'))

        for col, dtype_val in categories.items():
            df.loc[:, col] = df[col].astype(dtype_val)

        df = df.assign(
            line_in_source=pd.to_numeric(df.index + 1, downcast='unsigned'), year=pd.to_numeric(df.date.dt.year, downcast='unsigned')
        )

        colloc_sorted_df = df.sort_values(by='colloc').reset_index()
        colloc_sorted_df.pop('index')

        yield colloc_sorted_df


def coordinate_dataframes(baseline_hits, combined_contexts):
    # get basic hits that are not caught by any specific context
    init_positive_df = baseline_hits[
        ~baseline_hits.hit_id.isin(combined_contexts.hit_id)]

    print(f'-> {len(baseline_hits)-len(init_positive_df)} basic hits with hit_ids caught by other context patterns were removed.')

    positive_df = init_positive_df[~(init_positive_df.sent_text.isin(
        combined_contexts.sent_text) & init_positive_df.colloc.isin(combined_contexts.colloc))]

    print(f'-> {len(init_positive_df)-len(positive_df)} basic hits with sent_text repeated in other context hits were removed.')

    # mark these hits as "positive" context
    positive_df = positive_df.assign(context=positive_df.context.str.replace(
        'basic', 'positive'))
    positive_df = positive_df.assign(polarity='positive')

    all_contexts = pd.concat([combined_contexts, positive_df],
                             ignore_index=True)
    return all_contexts


def filter_context_overlap(all_contexts):
    # if more than one element in any "hit_id" group,
    # this means the hit_id matched more than 1 pattern/context;
    # set 'context_overlap' to True for hit
    all_contexts['context_overlap'] = (
        all_contexts.groupby('hit_id').hit_id.transform('count') > 1)
    all_contexts.to_pickle("all-contexts_with-overlap.pkl.gz")
    # (for now) ignore hits with any context overlap;
    # note: unlike the duplicate filter below, this removes *all* hits
    #       with context overlap, not just every repeat after the first
    no_overlap = all_contexts[~all_contexts.context_overlap]
    overlap = all_contexts[all_contexts.context_overlap].sort_values('hit_id')
    overlap.to_csv('context_overlap_hits.csv')

    print(
        f'-> {len(all_contexts) - len(no_overlap)} hits with context overlap excluded')

    # reset categories again
    no_overlap.loc[:, cat_columns
                   ] = no_overlap.loc[:, cat_columns].astype("category")
    return no_overlap


def filter_duplicate_text(no_overlap):
    # remove hits which duplicate sentence all sentence info
    # (leave first instance; can use keep='last' arg to flip)
    sent_info_cols = ['colloc', 'adv_index', 'context',
                      'prev_sent', 'sent_text', 'next_sent']
    info_duplicate = no_overlap.duplicated(subset=sent_info_cols)
    no_overlap_or_duplicates = no_overlap[~info_duplicate]

    # also get dataframe indicating level to which hits are duplicated
    dup_index = {}
    for col in sent_info_cols:
        tf_index = no_overlap.duplicated(subset=[col], keep=False)
        dup_index[f'{col}_duplicate'] = tf_index

    dup_index = pd.DataFrame.from_dict(dup_index)  # not column? any()
    duplicates_info = dup_index.assign(
        colloc=no_overlap.colloc,
        sent_text=no_overlap.sent_text,
        context=no_overlap.context,
        adv_index=no_overlap.adv_index,
        prev_sent=no_overlap.prev_sent,
        next_sent=no_overlap.next_sent,
        hit_it=no_overlap.hit_id)

    duplicates = duplicates_info[dup_index.colloc_duplicate &
                                 dup_index.sent_text_duplicate & dup_index.adv_index_duplicate]
    duplicates = duplicates.assign(
        sent_colloc_duplicate=True,
        prev_and_next_duplicate=(duplicates.prev_sent_duplicate
                                 & duplicates.next_sent_duplicate))
    duplicates.to_csv('duplicated_sents_info.csv')

    print(f'-> {len(no_overlap) - len(no_overlap_or_duplicates)} hits with duplicated sentence info removed.')

    return no_overlap_or_duplicates


def create_samples(no_overlap_or_duplicates):
    print(f'Saving sample csv files to {sample_dir}')
    sample_df = no_overlap_or_duplicates.sample(
        n=1500).sort_values(by="colloc")
    sample_df.head(500).to_csv(
        sample_dir / 'cleaned_hits_500rows_1.csv', index=False)
    sample_df[500:999].to_csv(
        sample_dir / 'cleaned_hits_500rows_2.csv', index=False)
    sample_df.tail(500).to_csv(
        sample_dir / 'cleaned_hits_500rows_3.csv', index=False)


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round((absFinish - absStart)/60, 2)} minutes')
