# coding=utf-8
from collections import namedtuple
from pathlib import Path

import pandas as pd
from utils.general import confirm_dir, find_files  # pylint: disable=import-error


def balance_sample(full_df: pd.DataFrame,
                   column_name: str,
                   sample_per_value: int = 5,
                   verbose: bool = False) -> tuple:
    '''
    create sample with no more than n rows satisfying each unique value
    of the given column. A value of -1 for `sample_per_value` will limit
    all values' results to the minimum count per value.
    '''
    info_message = ''
    subsamples = []
    for __, col_val_df in full_df.groupby(column_name):
        # take sample if 1+ and less than length of full dataframe
        if len(col_val_df) > sample_per_value > 0:
            subsample_df = col_val_df.sample(sample_per_value)
            subsamples.append(subsample_df)
        else:
            subsamples.append(col_val_df)

    # > trim all "by column" sub dfs to length of shortest if -1 given
    if sample_per_value == -1:
        trim_len = int(min(len(sdf) for sdf in subsamples))
        subsamples = [sdf.sample(trim_len)
                      for sdf in subsamples]

    b_sample = pd.concat(subsamples)

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
                convert_dtypes=False,
                verbose: bool = True) -> pd.DataFrame:
    if not pickles:
        pickles = find_files(data_dir, fname_glob, verbose)

    # tested and found that it is faster to assign `corpus` intermittently
    df = pd.concat((pd.read_pickle(p).assign(corpus=p.stem.rsplit('_', 2)[0])
                    for p in pickles))

    dup_check_cols = cols_by_str(df, end_str=('text', 'id', 'sent'))
    df = (df.loc[~df.duplicated(dup_check_cols), :])
    if convert_dtypes:
        df = df.convert_dtypes()
        df = make_cats(df, (['corpus'] + cols_by_str(df, start_str=('nr', 'neg', 'adv'),
                                                     end_str=('lemma', 'form'))))

    return df


def cols_by_str(df: pd.DataFrame, start_str=None, end_str=None) -> list:
    if end_str:
        cols = df.columns[df.columns.str.endswith(end_str)]
        if start_str:
            cols = cols[cols.str.startswith(start_str)]
    elif start_str:
        cols = df.columns[df.columns.str.startswith(start_str)]
    else:
        cols = df.columns

    return cols.to_list()


def count_uniq(series: pd.Series) -> int:
    return len(series.unique())


def get_proc_time(start: pd.Timestamp, end: pd.Timestamp) -> str:
    t_comp = (end - start).components
    time_str = (":".join(
        str(c).zfill(2)
        for c in (t_comp.hours, t_comp.minutes, t_comp.seconds)) +
        f'.{round(t_comp.microseconds, 1)}')

    return time_str


def make_cats(orig_df: pd.DataFrame, columns: list = None) -> pd.DataFrame:  # type: ignore
    df = orig_df.copy()
    if columns is None:
        cat_suff = ("code", "name", "path", "stem")
        columns = df.columns.str.endswith(cat_suff)  # type: ignore

    df.loc[:, columns] = df.loc[:, columns].astype(
        'string').astype('category')  # type: ignore

    return df


def print_md_table(df: pd.DataFrame,
                   indent: int = 0,
                   title: str = '',
                   comma: bool = True,
                   n_dec: int = 0) -> None:
    if n_dec is None:
        md_table = df.to_markdown()
    else:
        floatfmt = f'.{n_dec}f'
        if comma:
            floatfmt = f',{floatfmt}'
        md_table = df.to_markdown(floatfmt=floatfmt)

    whitespace = ' '*indent if indent else ''
    if title:
        print(f'\n{whitespace}{title}')
    for row in md_table.splitlines():
        print(f"{' '*indent}{row}")


def save_in_lsc_format(frq_df, lsc_tsv_path, numeric_label='raw'):
    new_col_name = f'{numeric_label}_frq'
    if 'adj_lemma' in frq_df.columns:
        frq_df = frq_df.set_index('adj_lemma', drop=True)
    frq_df.columns.name = 'adv_lemma'
    frq_df = frq_df.loc[frq_df.index != 'SUM', frq_df.columns != 'SUM']

    lsc_format = frq_df.stack().to_frame(new_col_name)
    # lsc_format.columns = [new_col_name]
    lsc_format = lsc_format.reset_index(
    ).loc[:, [new_col_name, 'adv_lemma', 'adj_lemma']]
    lsc_format = (
        lsc_format
        .sort_values(['adv_lemma', 'adj_lemma'])
        .sort_values(new_col_name, ascending=False))
    lsc_counts = lsc_format.to_csv(sep="\t", index=False).splitlines()[1:]
    lsc_lines = ['2'] + [x.strip() for x in lsc_counts]
    print('\nFormatted Output Sample (top 20 bigrams):')
    print('\n'.join(lsc_lines[:20] + ['...']))
    lsc_tsv_path.write_text('\n'.join(lsc_lines), encoding='utf8')
    print('Counts formatted to train lsc model saved as:',
          str(lsc_tsv_path))


def save_table(df: pd.DataFrame,
               path_str: str,
               df_name: str = '',
               formats: list = ['pickle']):
    # df_name += ' '
    path = Path(path_str)
    confirm_dir(path.parent)
    if not path.is_absolute():
        exit('Absolute path is required.')
    _ext = namedtuple('Format', ['ext', 'sep'])
    ext_dict = {
        'pickle': _ext('.pkl.gz', None), 
        'csv': _ext('.csv',','),
        'psv': _ext('.psv', '|'),
        'tsv': _ext('.tsv', '\t')
    }
    
    for form in formats:
        save = ext_dict[form]
        print(f'~ Saving {df_name} as {form}...')
        t0 = pd.Timestamp.now()

        out_path = f'{path_str.replace(save.ext, "")}{save.ext}'
        if form == 'pickle':
            df.to_pickle(out_path)
        else:
            df.to_csv(out_path, sep=save.sep)
        # elif form == 'csv':
        #     out_path = str(path_str) + '.csv'
        #     df.to_csv(out_path)
        # elif form == 'psv':
        #     out_path = str(path_str) + '.csv'
        #     df.to_csv(out_path, sep='|')
        # elif form == 'tsv':
        #     out_path = str(path_str) + '.tsv'
        #     df.to_csv(out_path, sep='\t')
        t1 = pd.Timestamp.now()
        print(f'   >> successfully saved as {out_path}\n' +
              f'      (time elapsed: {get_proc_time(t0, t1)})')


def select_cols(df: pd.DataFrame,
                columns: list = ['adv_lemma', 'adj_lemma',
                                 'text_window', 'token_str'], 
                dtype: str='string') -> pd.DataFrame:

    df = df.loc[:, columns]
    if dtype: 
        df = df.astype(dtype)
    else: 
        df = df.convert_dtypes()
    return df


def select_pickle_paths(n_files: int,
                        pickle_dir=Path(
                            '/share/compling/data/sanpi/2_hit_tables/advadj'),
                        smallest_first=True) -> pd.Series:

    pkl_df = pd.DataFrame(pickle_dir.glob('bigram-*hits.pkl.gz'),
                          columns=['path'])
    pkl_df = pkl_df.assign(size=pkl_df.path.apply(lambda f: f.stat().st_size))
    # > make dataframe to load `n_files` sorted by size (for testing)
    pkl_df = pkl_df.sort_values('size', ascending=smallest_first)
    pkl_select = pkl_df.head(n_files).reset_index()
    return pkl_select.path


def sort_by_margins(crosstab_df, margins_name='SUM'):
    crosstab_df = (crosstab_df.sort_values(
        margins_name,
        ascending=False).transpose().sort_values(margins_name,
                                                 ascending=False).transpose())
    return crosstab_df


def unpack_dict(input_dict: dict,
                values_name: str = 'adj',
                keys_name: str = 'type',
                return_df=True,
                return_dict=False):
    scale_df = (pd.Series(input_dict).to_frame().reset_index().rename(
        columns={
            0: values_name,
            'index': keys_name
        }))
    explodf = scale_df.explode(values_name).set_index(values_name)
    inv_flat_dict = explodf.to_dict()[keys_name]
    flat_unq_vals = list(set(inv_flat_dict.keys()))
    flat_unq_vals.sort()
    returns = (flat_unq_vals, )
    if return_df:
        returns += (explodf, )
    if return_dict:
        returns += (inv_flat_dict, )

    return returns
