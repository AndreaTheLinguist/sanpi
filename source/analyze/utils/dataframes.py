# coding=utf-8
from pathlib import Path

import pandas as pd
from analyze.utils.general import find_files #pylint: disable=import-error


def balance_sample(full_df: pd.DataFrame,
                   column_name: str,
                   sample_per_value: int = 5,
                   verbose: bool = False):
    '''
    create sample with no more than n rows satisfying each unique value
    of the given column. A value of -1 for `sample_per_value` will limit
    all values' results to the minimum count per value.
    '''
    info_message = ''
    sub_samples = []
    # TODO: test this. made changes to how this was done.
    #       not sure if groupby will produce desired output
    for __, sdf in full_df.groupby(column_name):
        # take sample if 1+ and less than length of full dataframe
        if len(sdf) > sample_per_value > 0: 
            sdf = sdf.sample(sample_per_value)
        sub_samples.append(sdf)
        
    #> trim all "by column" sub dfs to length of shortest if -1 given
    if sample_per_value == -1:
        trim_len = int(min(len(sdf) for sdf in sub_samples))
        sub_samples = [sdf.sample(trim_len)
                       for sdf in sub_samples]

    #TODO: make sure this still has category/`column_name` column
    b_sample = pd.concat(sub_samples)

    if verbose:
        subset_info_table = (
            b_sample
            .value_counts(subset=column_name)
            .to_frame(name='count')
            .assign(percentage=b_sample
                    .value_counts(column_name, normalize=True)
                    .round(2) * 100)
            .to_markdown())
        label = (full_df.hits_df_pkl[0].stem + ' ' 
                 if 'hits_df_pkl' in full_df.columns 
                 else '')
        info_message = (f'\n## {column_name} representation in {label}sample\n'
                        + subset_info_table)

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
