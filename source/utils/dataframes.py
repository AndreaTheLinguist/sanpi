# coding=utf-8
import re
import statistics as stat
from collections import namedtuple
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from general import confirm_dir, find_files  # pylint: disable=import-error
except ModuleNotFoundError:
    try:
        from utils.general import confirm_dir  # pylint: disable=import-error
        from utils.general import find_files
    except ModuleNotFoundError:
        from source.utils.general import (  # pylint: disable=import-error
            confirm_dir, find_files)

OPTIMIZED_DTYPES = {
    'string': {
        'sent_id':          'string',
        'colloc_id':        'string',
        'lemma_str':        'string'},

    # > categorical (demonstrably improves memory usage)
    'safely_category': {
        'neg_deprel':       'category',
        'neg_head':         'category',
        'mod_deprel':       'category',
        'mod_head':         'category',
        'match_id':         'category',
        'pattern':          'category',
        'category':         'category',
        'corpus':           'category'},

    # ! should be kept as/converted to string while hits are being removed
    #   can be stored as category, but need to be string for removal,
    #   then converted back to categorical after exclusions have been made
    'caution_category': {
        'colloc':           'category',
        'neg_form':         'category',
        'adv_form':         'category',
        'adj_form':         'category',
        'hit_text':         'category',
        'neg_lemma':        'category',
        'adv_lemma':        'category',
        'adj_lemma':        'category'},

    # > dependency path strings
    'dep_paths': {
        'dep_str':          'category',
        'dep_str_lemma':    'category',
        'dep_str_struct':   'category',
        'dep_str_ix':       'category',
        'dep_str_node':     'category',
        'dep_str_full':     'category',
        'dep_str_rel':      'category',
        'dep_str_node_rel': 'category',
        'dep_str_mask':     'category',
        'dep_str_mask_rel': 'category'},

    # > NUMERICAL
    'numerical': {
        'neg_index':        'category',  # 'uint16'
        'adv_index':        'category',  # 'uint16'
        'adj_index':        'category',  # 'uint16'
        'utt_len':          'category'},  # 'uint16'
}


def balance_sample(full_df: pd.DataFrame,
                   column_name: str,
                   sample_per_value: int = 5,
                   verbose: bool = False) -> tuple:
    """
    create sample with no more than n rows satisfying each unique value
    of the given column. A value of -1 for `sample_per_value` will limit
    all values' results to the minimum count per value.
    """
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


def _enhance_descrip(df: pd.DataFrame) -> pd.DataFrame:
    # df = df
    desc = df.describe().transpose()
    desc = desc.assign(total=pd.to_numeric(df.sum()),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'])
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    if 'SUM' not in desc.index:
        desc = desc.assign(
            plus1_geo_mean=df.add(1).apply(stat.geometric_mean),
            plus1_har_mean=df.add(1).apply(stat.harmonic_mean))
    for col in desc.columns:
        if col in ('mean', 'std', 'variance', 'var_coeff'):
            desc.loc[:, col] = desc[col].round(1)
        else:
            desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    # mean_centr = no_sum_frame - no_sum_frame.mean()
    # mean_stand = no_sum_frame / no_sum_frame.mean()
    # mean_stand_centr = mean_stand - mean_stand.mean()
    # log2_trans = no_sum_frame.apply(np.log2)
    # log2_plus1_trans = no_sum_frame.add(1).apply(np.log2)
    # logn_plus1_trans = no_sum_frame.apply(np.log1p)

    return desc.round(1)


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
                   n_dec: int = 0,
                   suppress: bool = False,
                   max_colwidth: int = 0,
                   max_cols: int = 0,
                   max_width: int = 0,
                   describe: bool = False,
                   transpose: bool = False
                   ) -> None:
    # FIXME realized this does nothing for markdown tables, which are strings
    set_pd_display(max_colwidth, max_cols, max_width)

    if describe:
        df = df.describe()
    if transpose:
        df = df.T

    # if max_colwidth:
    #     df = df.apply(lambda x: x.st)
    if n_dec is None:
        md_table = df.to_markdown()
    else:
        floatfmt = f'.{n_dec}f'
        if comma:
            floatfmt = f',{floatfmt}'
        if not df.select_dtypes(include='number').empty:
            df.loc[:, df.select_dtypes(include='number').columns] = df.select_dtypes(
                include='number').astype('float')
        md_table = df.to_markdown(floatfmt=floatfmt)

    whitespace = ' '*indent if indent else ''
    print_str = ''
    if title:
        print_str += f'\n{whitespace}{title}\n'
    print_str += (whitespace
                  + md_table.replace('\n', f'\n{whitespace}'))
    if suppress:
        return print_str
    else:
        print(print_str)
        return ''


def set_pd_display(max_colwidth, max_cols, max_width):
    if max_colwidth:
        pd.set_option('display.max_colwidth', max_colwidth)
    if max_cols:
        pd.set_option('display.max_columns', max_cols)
    if max_width:
        pd.set_option('display.width', max_width)


def save_in_lsc_format(frq_df, 
                       output_tsv_path, 
                       numeric_label='raw',
                       row_w1_label = 'adj_form_lower', 
                       col_w0_label= 'adv_form_lower'):
    confirm_dir(output_tsv_path.parent)
    new_col_name = f'{numeric_label}_frq'

    if row_w1_label in frq_df.columns:
        frq_df = frq_df.set_index(row_w1_label, drop=True)
    frq_df.columns.name = col_w0_label
    frq_df = frq_df.loc[frq_df.index != 'SUM', frq_df.columns != 'SUM']

    lsc_format = frq_df.stack().to_frame(new_col_name)
    # lsc_format.columns = [new_col_name]
    lsc_format = lsc_format.reset_index().loc[:, [new_col_name, col_w0_label, row_w1_label]]
    lsc_format = (
        lsc_format
        .sort_values([col_w0_label, row_w1_label])
        .sort_values(new_col_name, ascending=False))
    lsc_counts = lsc_format.to_csv(sep="\t", index=False).splitlines()[1:]
    lsc_lines = ['2'] + [x.strip() for x in lsc_counts]
    print('\nFormatted Output Sample (top 20 bigrams):')
    print('\n'.join(lsc_lines[:20] + ['...']))
    output_tsv_path.write_text('\n'.join(lsc_lines), encoding='utf8')
    print('Counts formatted to train lsc model saved as:', output_tsv_path)


def save_table(df: pd.DataFrame,
               path_str: str,
               df_name: str = '',
               formats: list = None):
    if formats is None:
        formats = ['pickle']
    # df_name += ' '
    path_str = re.sub(r'\.(pkl.gz|csv|psv)', '', path_str)
    path = Path(path_str)
    confirm_dir(path.parent)
    if not path.is_absolute():
        exit('Absolute path is required.')
    _ext = namedtuple('Format', ['ext', 'sep'])
    ext_dict = {
        'pickle': _ext('.pkl.gz', None),
        'csv': _ext('.csv', ','),
        'psv': _ext('.psv', '|'),
        'tsv': _ext('.tsv', '\t')
    }
    for form in formats:
        save = ext_dict[form]
        print(f'~ Saving {df_name} as {form}...')
        time_0 = pd.Timestamp.now()

        out_path = Path(f'{path}{save.ext}')
        if form == 'pickle':
            df.to_pickle(out_path)
        else:
            df.to_csv(out_path, sep=save.sep)
        # // elif form == 'csv':
        # //     out_path = str(path_str) + '.csv'
        # //     df.to_csv(out_path)
        # // elif form == 'psv':
        # //     out_path = str(path_str) + '.csv'
        # //     df.to_csv(out_path, sep='|')
        # // elif form == 'tsv':
        # //     out_path = str(path_str) + '.tsv'
        # //     df.to_csv(out_path, sep='\t')
        time_1 = pd.Timestamp.now()
        print(f'   >> successfully saved as {out_path}\n' +
              f'      (time elapsed: {get_proc_time(time_0, time_1)})')


def select_cols(df: pd.DataFrame,
                columns: list = None,
                dtype_for_cols: str = 'string') -> pd.DataFrame:
    # columns = ['adv_lemma', 'adj_lemma', 'text_window', 'token_str']
    if 'hit_id' in df.columns:
        df = df.set_index('hit_id')
    if not columns:
        columns = df.columns[df.columns.str.endswith('_lemma')].to_list()
        if len(columns) > 2:
            columns.append('colloc_id')
            columns.append('hit_text')
        columns.extend(['text_window', 'token_str'])

    df = df.loc[:, df.columns.isin(columns)]
    if dtype_for_cols:
        try:
            df = df.astype(dtype_for_cols)
        except:
            pass
            # df = df.convert_dtypes()
    return df


def select_pickle_paths(n_files: int,
                        pickle_dir=Path(
                            '/share/compling/data/sanpi/2_hit_tables/advadj'),
                        smallest_first=True) -> pd.Series:

    pkl_df = pd.DataFrame(pickle_dir.glob('bigram*hits.pkl.gz'),
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


def transform_counts(df: pd.DataFrame,
                     method: str = 'sqrt', 
                     plus1: bool = False):
    if plus1 or method.startswith('log'):
        df = df.add(1)
    if method == 'sqrt':
        df = df.apply(lambda x: x.apply(sqrt))
    elif method == 'log10':
        df = df.apply(lambda x: x.apply(np.log10))
    elif method == 'log2':
        df = df.apply(lambda x: x.apply(np.log2))
    return df


def unpack_dict(input_dict: dict,
                values_name: str = 'adj',
                keys_name: str = 'type',
                return_df=True,
                return_dict=False):
    scale_df = pd.Series(input_dict).to_frame('values_name')
    scale_df = scale_df.reset_index()
    scale_df = scale_df.rename(columns={'index': keys_name})
    explodf = scale_df.explode(values_name)
    explodf = explodf.set_index(values_name)
    inv_flat_dict = explodf.to_dict()[keys_name]
    flat_unq_vals = sorted(set(inv_flat_dict.keys()))
    returns = (flat_unq_vals, )
    if return_df:
        returns += (explodf, )
    if return_dict:
        returns += (inv_flat_dict, )

    return returns
