# coding=utf-8
from pathlib import Path

import pandas as pd
from analyze.utils.general import print_iter, dur_round, find_files


def balance_sample(full_df: pd.DataFrame,
                   column_name: str,
                   sample_per_value: int = 5,
                   verbose: bool = False):
    '''
    create sample with no more than n rows satisfying each unique value
    of the given column. A value of 0 for `sample_per_value` will limit
    all values' results to the minimum count per value.
    '''
    info_message = ''
    sub_samples = []
    n = 5 if not sample_per_value else sample_per_value

    for c in full_df.loc[:, column_name].unique():
        sdf = (
            full_df.loc[full_df[column_name] == c, :]
            .sample(min(full_df.value_counts(subset=column_name)[c],
                        n))
        )
        sub_samples.append(sdf)
    if not sample_per_value:
        trim_len = min(len(sdf) for sdf in sub_samples)
        sub_samples = [sdf.iloc[:trim_len, :]
                       for sdf in sub_samples]

    b_sample = pd.concat(sub_samples)

    if verbose:
        subset_info = (
            b_sample
            .value_counts(subset=column_name)
            .to_frame(name='count')
            .assign(percentage=b_sample
                    .value_counts(column_name, normalize=True)
                    .round(2) * 100)
            .to_markdown())

        info_message = f'\n## {column_name} representation in sample:\n{subset_info}'

    return b_sample, info_message


def concat_pkls(data_dir: Path = Path('/share/compling/data/sanpi/2_hit_tables'),
                fname_glob: str = '*.pkl.gz',
                pickles=None,
                verbose: bool = True):
    if not pickles:
        pickles = find_files(data_dir, fname_glob, verbose)

    # tested and found that it is faster to assign `corpus` intermittently
    df = pd.concat((pd.read_pickle(p).assign(corpus=p.stem.rsplit('_', 2)[0])
                    for p in pickles))

    dup_check_cols = cols_by_str(df, end_str=('text', 'id', 'sent'))
    df = (df.loc[~df.duplicated(dup_check_cols), :])
    df = make_cats(df, (['corpus'] + cols_by_str(df, start_str=('nr', 'neg', 'adv'),
                                                 end_str=('lemma', 'form'))))

    return df


def cols_by_str(df: pd.DataFrame, start_str=None, end_str=None):
    if end_str:
        cols = df.columns[df.columns.str.endswith(end_str)]
        if start_str:
            cols = cols[cols.str.startswith(start_str)]
    elif start_str:
        cols = df.columns[df.columns.str.startswith(start_str)]
    else:
        cols = df.columns

    return cols.to_list()


def make_cats(df, columns: list = None):

    if columns is None:
        cat_suff = ("code", "name", "path", "stem")
        columns = df.columns.str.endswith(cat_suff)

    df.loc[:, columns] = df.loc[:, columns].astype(
        'string').astype('category')

    return df
