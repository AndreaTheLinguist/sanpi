# coding=utf-8
import contextlib
import re
# import statistics as stat
from collections import namedtuple
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from source.utils.general import PKL_SUFF, confirm_dir, find_files, snake_to_camel
except ModuleNotFoundError:
    try:
        from utils.general import (PKL_SUFF, confirm_dir, find_files,
                                   snake_to_camel)
    except ModuleNotFoundError:
        from general import (PKL_SUFF, confirm_dir, find_files,
                             snake_to_camel)

OPTIMIZED_DTYPES = {
    'string': {
        'sent_id':          'string',
        'bigram_id':        'string',
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


def calculate_var_coeff(vector: pd.Series):
    return vector.std() / vector.mean()


def concat_pkls(data_dir: Path = Path('/share/compling/data/sanpi/2_hit_tables'),
                fname_glob: str = f'*{PKL_SUFF}',
                pickles=None,
                convert_dtypes=False,
                verbose: bool = True) -> pd.DataFrame:
    if not pickles:
        pickles = find_files(data_dir, fname_glob, verbose)

    # tested and found that it is faster to assign `corpus` intermittently
    _df = pd.concat((pd.read_pickle(p).assign(corpus=p.stem.rsplit('_', 2)[0])
                    for p in pickles))

    dup_check_cols = cols_by_str(_df, end_str=('text', 'id', 'sent'))
    _df = (_df.loc[~_df.duplicated(dup_check_cols), :])
    if convert_dtypes:
        cdf = _df.copy().convert_dtypes()
        num_cols = cdf.select_dtypes(include='number').columns
        cdf.loc[:, num_cols] = _df[num_cols].apply(
            pd.to_numeric, downcast='unsigned')
    return make_cats(
        cdf, (['corpus']
              + cols_by_str(
                  cdf,
                  start_str=('nr', 'neg', 'adv'),
                  end_str=('lemma', 'form', 'lower', 'pattern', 'category'))
              )
    )


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


def corners(df, size: int = 5, n_dec: int = None):

    _df = df.copy()
    if n_dec:
        _df.update(
            _df.select_dtypes(include='float').apply(np.around, decimals=n_dec, axis=1))
    _df.index.name = _df.index.name or 'rows'
    _df.columns.name = _df.columns.name or 'columns'
    index_name = _df.index.name
    columns_name = _df.columns.name
    _df = _df.reset_index().reset_index().set_index(
        ['index', index_name])
    _df = _df.T.reset_index().reset_index().set_index(
        ['index', columns_name]).T
    cdf = pd.concat(
        [d.iloc[:, :size].assign(__='...')
         .join(d.iloc[:, -size:])
         for d in (_df.head(size).T.assign(__='...').T,
                     _df.tail(size))])
    cdf = cdf.reset_index().set_index(index_name)
    cdf.pop('index')
    cdf = cdf.T.reset_index().set_index(columns_name)
    cdf.pop('index')
    return cdf.T.rename(columns={'': '...'}, index={'': '...'})


def drop_margins(_df, margin_name='SUM'):
    return _df.loc[_df.index != margin_name, _df.columns != margin_name]


def _enhance_descrip(df: pd.DataFrame) -> pd.DataFrame:
    # df = df
    desc = df.describe().transpose()
    desc = desc.assign(total=pd.to_numeric(df.sum()),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'])
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    # if 'SUM' not in desc.index:
    #     desc = desc.assign(
    #         plus1_geo_mean=df.add(1).apply(stat.geometric_mean),
    #         plus1_har_mean=df.add(1).apply(stat.harmonic_mean))
    for col in desc.columns:
        if col in ('count', 'min', 'max', 'total', 'range'):
            desc.loc[:, col] = pd.to_numeric(
                desc.loc[:, col], downcast='unsigned')
        # if col in ('mean', 'std', 'variance', 'var_coeff'):
        else:
            desc.loc[:, col] = pd.to_numeric(
                desc.loc[:, col], downcast='float').round(1)
    desc = desc.rename(columns={'50%': 'median'})
    # mean_centr = no_sum_frame - no_sum_frame.mean()
    # mean_stand = no_sum_frame / no_sum_frame.mean()
    # mean_stand_centr = mean_stand - mean_stand.mean()
    # log2_trans = no_sum_frame.apply(np.log2)
    # log2_plus1_trans = no_sum_frame.add(1).apply(np.log2)
    # logn_plus1_trans = no_sum_frame.apply(np.log1p)

    return desc


def get_proc_time(start: pd.Timestamp, end: pd.Timestamp) -> str:
    t_comp = (end - start).components
    return (
        ":".join(
            str(c).zfill(2)
            for c in (t_comp.hours, t_comp.minutes, t_comp.seconds)
        )
        + f'.{round(t_comp.microseconds, 1)}'
    )


def make_cats(orig_df: pd.DataFrame, columns: list = None) -> pd.DataFrame:  # type: ignore
    df = orig_df.copy()
    if columns is None:
        cat_suff = ("code", "name", "path", "stem")
        columns = df.columns.str.endswith(cat_suff)  # type: ignore

    df.loc[:, columns] = df.loc[:, columns].astype(
        'string').astype('category')  # type: ignore

    return df


def optimize_hit_df(df: pd.DataFrame, verbosity=0):
    very_verbose = verbosity > 1
    verbose = verbosity > 0
    if very_verbose:
        print('Original Dataframe:')
        df.info(memory_usage='deep')

    _df = df.copy()
    # * clean up dataframe a bit
    # > drop extraneous string columns
    _df.drop(
        cols_by_str(_df, start_str=('context',  # 'text', 'sent_text',
                                    'token', 'json')),
        axis=1, inplace=True)

    if very_verbose:
        print('Original Dataframe Minus Superfluous Columns:')
        _df.info(memory_usage='deep')

    # > select only non-`object` dtype columns
    #  was #// relevant_cols = df.columns[~df.dtypes.astype('string').str.endswith(('object'))]
    relevant_cols = _df.select_dtypes(exclude='object').columns

    # > limit df to `relevant_cols`
    r_df = _df.copy()[relevant_cols]

    # > create empty dataframe with `relevant_cols` as index/rows
    df_info = pd.DataFrame(index=relevant_cols)

    df_info = df_info.assign(
        mem0=r_df.memory_usage(deep=True),
        dtype0=r_df.dtypes.astype('string'),
        defined_values=r_df.count(),
        unique_values=r_df.nunique())
    df_info = df_info.assign(
        ratio_unique=(df_info.unique_values
                      / df_info.defined_values).round(2))

    cat_candidates = df_info.loc[df_info.ratio_unique < 0.8,
                                 :].loc[df_info.dtype0 != 'category'].index.to_list()
    c_df = r_df.copy()[cat_candidates].astype('category')

    df_info = df_info.assign(
        dtype1=c_df.dtypes, mem1=c_df.memory_usage(deep=True))
    df_info = df_info.assign(mem_change=df_info.mem1-df_info.mem0)
    mem_improved = df_info.loc[df_info.mem_change < 0, :].index.to_list()
    if very_verbose:
        print_md_table(df_info.sort_values(
            ['mem_change', 'ratio_unique', 'dtype0']), n_dec=2, title='\nMemory Usage Comparison\n')
        for c in relevant_cols:
            if c not in mem_improved:
                print('✕', c, r_df.loc[:, c].dtype, sep='\t')
            else:
                print('✓', c, c_df.loc[:, c].dtype, sep='\t')
    _df[mem_improved] = c_df[mem_improved]
    if verbose:
        print('Category Converted dataframe:')
        _df.info(memory_usage='deep')
    return _df


def optimize_am_df(df: pd.DataFrame, verbose=False):
    _df = df.copy()
    if verbose:
        print('>> Unoptimized <<')
        _df.info(memory_usage='deep')
    str_cols = _df.select_dtypes(exclude='number').columns.to_list()
    int_cols = _df.columns[_df.columns.str.startswith(
        ('r_', 'C', 'R', 'N', 'f', 'index'))].to_list()
    is_float = ~_df.columns.isin(int_cols + str_cols)
    _df[int_cols] = _df[int_cols].apply(pd.to_numeric, downcast='unsigned')
    _df.loc[:, is_float] = _df.loc[:, is_float].apply(
        pd.to_numeric, downcast='float')
    _df[str_cols] = _df[str_cols].apply(
        lambda c: c.astype('string').astype('category')
        if c.dtype != 'category' and c.nunique() > (len(c) / 2)
        else c)
    if verbose:
        print('\n--------\n>> Optimized DataFrame')
        _df.info(memory_usage='deep')
    _df['l1'] = _df['l1'].astype('category')
    return _df


def print_md_table(input_df: pd.DataFrame,
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
    """
    Converts a DataFrame to a markdown table string and prints it (unless printing is suppressed).

    Args:
        df: The DataFrame to be printed as a markdown table.
        indent: The number of spaces to indent the table. Defaults to 0.
        title: The title of the table. Defaults to an empty string.
        comma: A boolean indicating whether to include commas in number formatting. Defaults to True.
        n_dec: The number of decimal places to round the numbers to. Defaults to 0.
        suppress: A boolean indicating whether to suppress printing and return the markdown table as a string. Defaults to False.
        max_colwidth: The maximum width of each column. Defaults to 0.
        max_cols: The maximum number of columns to display. Defaults to 0.
        max_width: The maximum width of the entire table. Defaults to 0.
        describe: A boolean indicating whether to describe the DataFrame before printing. Defaults to False.
        transpose: A boolean indicating whether to transpose the DataFrame before printing. Defaults to False.

    Returns:
        the markdown table as a string if suppress is True, else prints the table to stdout
    """
    _df = input_df.copy()
    # FIXME realized this does nothing for markdown tables, which are strings
    set_pd_display(max_colwidth, max_cols, max_width)

    if describe:
        _df = input_df.describe()
    if transpose:
        _df = _df.T

    # if max_colwidth:
    #     df = df.apply(lambda x: x.st)
    # replaced by sourcery suggestion below
    # if n_dec is None:
    #     md_table = df.to_markdown()
    # else:
    #     floatfmt = f'.{n_dec}f'
    #     if comma:
    #         floatfmt = f',{floatfmt}'
    #     if not df.select_dtypes(include='number').empty:
    #         df.loc[:, df.select_dtypes(include='number').columns] = df.select_dtypes(
    #             include='number').astype('float')
    #     md_table = df.to_markdown(floatfmt=floatfmt)

    # whitespace = ' '*indent if indent else ''
    # print_str = ''
    # if title:
    #     print_str += f'\n{whitespace}{title}\n'
    # print_str += (whitespace
    #               + md_table.replace('\n', f'\n{whitespace}'))

    floatfmt = f"{',' if comma else ''}.{n_dec}f"
    num_cols = _df.select_dtypes(include='number').columns.to_list()
    if any(num_cols):
        _df.loc[:, num_cols] = _df.loc[:, num_cols].astype(
            'float').round(n_dec)
    md_table = _df.to_markdown(floatfmt=floatfmt)

    whitespace = ' ' * indent
    print_str = f"{whitespace}{title}\n{whitespace}" if title else ''
    print_str += md_table.replace('\n', f'\n{whitespace}')

    if suppress:
        return print_str
    print(print_str)
    return ''


def set_pd_display(max_colwidth, max_cols, max_width):
    if max_colwidth:
        pd.set_option('display.max_colwidth', max_colwidth)
    if max_cols:
        if max_cols == 'all':
            pd.set_option('display.max_columns', None)
        else:
            pd.set_option('display.max_columns', max_cols)
    if max_width:
        pd.set_option('display.width', max_width)


def compute_ratios(freq_dist: pd.DataFrame,
                   dimensions: list,
                   abbr_len: int = 3):
    """
    Computes ratios for each dimension in a frequency distribution DataFrame.

    Args:
        freq_dist: The frequency distribution DataFrame.
        dimensions: A list of dimension names to compute ratios for.
        abbr_len: The length of the abbreviation for the dimension name. Defaults to 3.

    Returns:
        None
    """

    for dimension in dimensions:
        freq_dist[f'ratio_{dimension[:abbr_len]}'] = (
            freq_dist[dimension]/freq_dist.TOTAL).round(3)


def add_ratio_bins(freq_dist: pd.DataFrame):
    """
    Adds ratio bins to a frequency distribution DataFrame.

    This function adds ratio bins to the given frequency distribution DataFrame. The `freq_dist` DataFrame must have "ratio" columns for this function to have any effect.

    Args:
        freq_dist: The frequency distribution DataFrame.

    Returns:
        None
    """

    #! `freq_dist` must have "ratio" columns for this to do anything
    for ratio_col in freq_dist.copy().filter(like='ratio'):
        dim_ratio = freq_dist[ratio_col]
        bin_col = pd.to_numeric(dim_ratio.round(1), downcast='float')
        bin_col = bin_col.astype('category')
        freq_dist[ratio_col.replace('ratio', 'bin')] = bin_col


def compute_meta_cols(df: pd.DataFrame,
                      obs_col: str = 'adj_lemma',
                      dim_col: str = 'polarity',
                      dim_abbr_len: int = 3) -> pd.DataFrame:
    """
    Computes meta columns for a DataFrame.

    This function computes meta columns for a DataFrame by performing the following steps:
    1. Calculates a frequency distribution table using `pd.crosstab`.
    2. Computes ratios for each dimension in the frequency distribution.
    3. Adds ratio bins to the frequency distribution.
    4. Sorts the DataFrame by the 'TOTAL' column in descending order.

    Args:
        df: The DataFrame to compute meta columns for.
        obs_col: The name of the observation column. Defaults to 'adj_lemma'.
        dim_col: The name of the dimension column. Defaults to 'polarity'.
        dim_abbr_len: The length of the abbreviation for the dimension name. Defaults to 3.

    Returns:
        The computed frequency distribution DataFrame sorted by the 'TOTAL' column in descending order.
    """
    dimensions = list(df[dim_col].unique())
    freq_dist = pd.crosstab(df[obs_col],
                            df[dim_col],
                            margins=True, margins_name='TOTAL')
    freq_dist = freq_dist[['TOTAL'] + dimensions]
    compute_ratios(freq_dist, dimensions, dim_abbr_len)
    add_ratio_bins(freq_dist)

    return freq_dist.sort_values('TOTAL', ascending=False)


def show_counts(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Returns a DataFrame with counts of unique combinations of specified columns.

    Args:
        df: The DataFrame to count unique combinations from.
        columns: A list of column names to consider for counting unique combinations.

    Returns:
        A DataFrame with counts of unique combinations, where each row represents a unique combination and the 'count' column represents the count of occurrences.

    Raises:
        None
    """

    return df.value_counts(columns).to_frame().rename(columns={0: 'count'})


# * This function applies to the initial, `hit_id` indexed dataframe, ~ a "hit table".
def save_for_ucs(df, col_1: str, col_2: str,
                 output_dir: Path = None,
                 ucs_path: Path = None,
                 filter_dict: dict = None,
                 ) -> pd.DataFrame:
    """
    Saves a DataFrame in UCS format based on specified columns and filters.

    This function applies to the initial, `hit_id` indexed dataframe (a "hit table"). 
    If either an output directory or a specific path are given, the resultant dataframe will be saved as a `.tsv`,
    which can be used as the (stdin/piped) input for `ucs-make-tables --types`.

    Args:
        df: The DataFrame to pull `value_counts` from.
        col_1: The name of the first column to count.
        col_2: The name of the second column to count.
        output_dir: The output directory for any UCS file.
        ucs_path: The path to save the UCS file. Generated from `output_dir`, `col_1`, and `col_2` if not given.
        filter_dict: An optional dictionary of column (key) == value pairs to filter the DataFrame. Filter info will be incorporated into any output path.

    Returns:
        The DataFrame with counts of unique combinations of col_1 and col_2.
    """
    cols_tag = re.compile(r'_([a-z]{,4})-([a-z]{,4})_', re.IGNORECASE)
    if col_1 not in df.columns:
        print(
            f'WARNING: col_1 "{col_1}" not in dataframe. Defaulting to "adv_form_lower"')
        col_1 = 'adv_form_lower'
        if ucs_path:
            ucs_path = ucs_path.with_name(
                cols_tag.sub(r'_Adv-\2_', ucs_path.name))

    if col_2 not in df.columns:
        print(
            f'WARNING: col_2 "{col_2}" not in dataframe. Defaulting to "adj_form_lower"')
        col_2 = 'adj_form_lower'
        if ucs_path:
            ucs_path = ucs_path.with_name(
                cols_tag.sub(r'_\1-Adj_', ucs_path.name))

    if output_dir and not ucs_path:
        ucs_dir = output_dir / 'ucs_format'
        confirm_dir(ucs_dir)
        ucs_path = (ucs_dir /
                    f'{snake_to_camel(col_1)}{snake_to_camel(col_2)}.tsv')

    if filter_dict:
        for col, val in filter_dict.items():
            df = df.loc[df[col] == val, :]
            if ucs_path:
                ucs_path = ucs_path.with_stem(
                    f"{ucs_path.stem}_{snake_to_camel(col)}{val.upper()}")
    if ucs_path:
        print(f'output path: {ucs_path}')
        counts = show_counts(df, [col_1, col_2]).reset_index()[
            ['count', col_1, col_2]]
        counts.to_csv(ucs_path, encoding='utf8',
                      sep='\t', header=False, index=False)

    return counts


# * This function applies to a "frequency table", a DataFrame where counts have already been calculated via `pd.crosstab`
#  The index for such a table will be unique values for the `index` Series passed, not unique tokens/observations,
#  and the values will be co-occurrence frequencies with the value indicated by the column.
def save_in_lsc_format(frq_df,
                       output_tsv_path,
                       numeric_label='raw',
                       row_w1_label='adj_form_lower',
                       col_w0_label='adv_form_lower',
                       for_ucs: bool = False):
    """
    Saves a frequency table DataFrame in LSC format.

    This function applies to a "frequency table", a DataFrame where counts have already been calculated via `pd.crosstab`. The index for such a table will be unique values for the `index` Series passed, not unique tokens/observations, and the values will be co-occurrence frequencies with the value indicated by the column.

    Args:
        frq_df: The frequency table DataFrame to be saved.
        output_tsv_path: The path to save the LSC file.
        numeric_label: The label for the numeric column in the frequency table. Defaults to 'raw'.
        row_w1_label: The label for the row column in the frequency table. Defaults to 'adj_form_lower'.
        col_w0_label: The label for the column column in the frequency table. Defaults to 'adv_form_lower'.
        for_ucs: A boolean indicating whether the output is for UCS format. Defaults to False.

    Returns:
        None
    """

    def get_reshaped_output_lines(frq_df, row_w1_label, col_w0_label, for_ucs, new_col_name):
        lsc_format = reshape_totals(frq_df, new_col_name)
        lsc_format = _sort_stacks(
            row_w1_label, col_w0_label, new_col_name, lsc_format)
        return cleanup_output(for_ucs, lsc_format)

    def cleanup_output(for_ucs, lsc_format):
        counts_list = lsc_format.to_csv(sep="\t", index=False).splitlines()[1:]
        counts_lines = [x.strip() for x in counts_list]
        return counts_lines if for_ucs else ['2'] + counts_lines

    def save_tsv_file(output_tsv_path, output_lines):
        output_tsv_path.write_text('\n'.join(output_lines), encoding='utf8')
        print(f'* Simple tab-delimited counts saved as `.tsv`:\n  * path: `{output_tsv_path}`')

    def show_sample_output(output_lines):
        print('\n## Formatted Output Sample (top 20 bigrams)\n\n```log')
        print('\n'.join(output_lines[:20] + ['...']).expandtabs(8))
        print('```\n')

    def reshape_totals(frq_df, new_col_name):
        return frq_df.stack().to_frame(new_col_name)

    def _sort_stacks(row_w1_label, col_w0_label, new_col_name, stacked_df):
        stacked_df = stacked_df.reset_index()
        stacked_df['raw_frq'] = pd.to_numeric(stacked_df.raw_frq, downcast='unsigned')
        print_md_table(stacked_df.head(6).convert_dtypes(), title='\n## Stacked\n')
        print_md_table(stacked_df.tail(6).convert_dtypes(), title='\n...\n')

        stacked_df = stacked_df[[new_col_name, col_w0_label, row_w1_label]]
        # stacked_df = (
        #     stacked_df
        #     .sort_values([row_w1_label, col_w0_label])
        # )
        # I don't think this ^^ makes a difference.
        #   Was trying to get it to sort A-Z within the same frequency value,
        #   but it seems to overwrite that regardless, since one requires ascending, and the other descending
        # But it doesn't really matter in any case.

        #! The zeros have to be dropped from the data for UCS, and it might affect LSC as well
        # ^ 💡 so maybe this should just return `nonzeros` dataframe?
        # HACK: #! if there are errors, check this
        nonzeros = stacked_df[stacked_df[new_col_name] != 0]
        return nonzeros.sort_values(new_col_name, ascending=False).reset_index(drop=True)

    def prep_to_reshape(frq_df, numeric_label, row_w1_label, col_w0_label):
        if row_w1_label in frq_df.columns:
            frq_df = frq_df.set_index(row_w1_label, drop=True)
        elif not frq_df.index.name:
            frq_df.index.name = row_w1_label
        if not frq_df.columns.name:
            frq_df.columns.name = col_w0_label

        frq_df = frq_df.loc[frq_df.index != 'SUM', frq_df.columns != 'SUM']

        return frq_df, f'{numeric_label}_frq'

    confirm_dir(output_tsv_path.parent)
    frq_df, new_col_name = prep_to_reshape(
        frq_df, numeric_label, row_w1_label, col_w0_label)
    output_lines = get_reshaped_output_lines(frq_df, row_w1_label,
                                             col_w0_label, for_ucs, new_col_name)

    show_sample_output(output_lines)
    save_tsv_file(output_tsv_path, output_lines)


def save_table(df: pd.DataFrame,
               save_path: Path or str,
               df_name: str = '',
               formats: list = None):
    _ext = namedtuple('Format', ['ext', 'sep'])
    ext_dict = {
        'pickle': _ext(PKL_SUFF, None),
        'csv': _ext('.csv', ','),
        'psv': _ext('.psv', '|'),
        'tsv': _ext('.tsv', '\t')
    }
    save_path = str(save_path)
    if formats is None:
        formats = [save_path[-3:]
                   ] if save_path[-3:] in ext_dict else ['pickle']
    save_path = re.sub(r'\.(pkl\.gz|csv|psv)', '', save_path)
    path_stub = Path(save_path)
    confirm_dir(path_stub.parent)
    if not path_stub.is_absolute():
        exit('Absolute path is required.')
    for form in formats:
        save = ext_dict[form]
        print(f'+ Saving {df_name} as {form}...')
        with Timer() as timer:

            out_path = Path(f'{path_stub}{save.ext}')
            if form == 'pickle':
                df.to_pickle(out_path)
            else:
                df.to_csv(out_path, sep=save.sep)
            print(f'  + successfully saved as {out_path}\n',
                  f' + time elapsed: {timer.elapsed()}')


def select_cols(df: pd.DataFrame,
                columns: list = None,
                dtype_for_cols: str = 'string') -> pd.DataFrame:
    # columns = ['adv_lemma', 'adj_lemma', 'text_window', 'token_str']
    if 'hit_id' in df.columns:
        df = df.set_index('hit_id')
    if not columns:
        columns = df.columns[df.columns.str.endswith('_lemma')].to_list()
        if len(columns) > 2:
            columns.append('bigram_id')
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

    pkl_df = pd.DataFrame(pickle_dir.glob(f'bigram*hits{PKL_SUFF}'),
                          columns=['path'])
    pkl_df = pkl_df.assign(size=pkl_df.path.apply(lambda f: f.stat().st_size))
    # > make dataframe to load `n_files` sorted by size (for testing)
    pkl_df = pkl_df.sort_values('size', ascending=smallest_first)
    pkl_select = pkl_df.head(n_files).reset_index()
    return pkl_select.path


def set_axes(_df, index_name='adj_form_lower', columns_name='adv_form_lower'):
    if index_name in _df.columns:
        _df = _df.set_index(index_name)
    else:
        _df.index.name == _df.index.name or index_name
    _df.columns.name = _df.columns.name or columns_name
    return _df


def set_count_dtype(df, df_save_path: Path = None):
    df = df.apply(pd.to_numeric, downcast='unsigned')
    # BUG There may be an issue with this selecting the wrong dtype and fucking up large numbers again.
    uniq_dt = [str(d) for d in df.dtypes.unique()]
    # if len(uniq_dt) > 1:
    #     uniq_dt.sort()
    #     df = df.astype(uniq_dt[-1])
    if df_save_path:
        if df_save_path.suffix == '.csv':
            df_save_path = df_save_path.with_suffix(PKL_SUFF)
        df.to_pickle(df_save_path)
    return df


def sort_by_margins(crosstab_df, margins_name='SUM'):
    """
    Sorts a crosstab DataFrame by margins.

    This function sorts the given crosstab DataFrame by the specified margin name in descending order along both the rows and columns.

    Args:
        crosstab_df: The crosstab DataFrame to be sorted.
        margins_name: The name of the margins to sort by. Defaults to 'SUM'.

    Returns:
        The sorted crosstab DataFrame.
    """

    # > sort crosstabulated values by marginal frequencies
    for ax in [0, 1]:

        with contextlib.suppress(KeyError):
            crosstab_df = crosstab_df.sort_index(axis=ax)
            crosstab_df = crosstab_df.sort_values(
                margins_name, axis=ax, ascending=False)
    return crosstab_df


def square_sample(df: pd.DataFrame, n: int = 10,
                  with_margin: bool = True,
                  as_sqrt: bool = False):
    _df = drop_margins(df.copy())
    rows = ['SUM'] + _df.index.to_series().sample(n).to_list()
    cols = ['SUM'] + _df.columns.to_series().sample(n).to_list()

    sample = sort_by_margins(df.copy().loc[rows, cols])
    if not with_margin:
        sample = drop_margins(sample)
    if as_sqrt:
        sample = transform_counts(sample)
    return sample


def summarize_text_cols(tdf: pd.DataFrame):
    """
    Summarizes text columns in a DataFrame.

    This function calculates descriptive statistics for text columns in the given DataFrame. It selects the string columns, computes the count, unique values, top value, frequency of the top value, and the percentage of the top value in the DataFrame.

    Args:
        tdf: The DataFrame containing text columns to be summarized.

    Returns:
        A summary DataFrame with descriptive statistics for the text columns, sorted by the number of unique values.
    """

    summary = tdf.select_dtypes(exclude='number').describe().transpose()
    summary = summary.assign(top_percent=(
        ((pd.to_numeric(summary.freq) / len(tdf)))*100).round(2))
    summary = summary.rename(columns={'top': 'top_value', 'freq': 'top_freq'})

    return summary.convert_dtypes().sort_values('unique')


def transform_counts(df: pd.DataFrame,
                     method: str = 'sqrt',
                     plus1: bool = False):
    _df = df.copy()
    if plus1 or method.startswith('log'):
        _df = _df.add(1)
    if method == 'sqrt':
        _df = _df.apply(lambda x: x.apply(sqrt))
    elif method == 'log10':
        _df = _df.apply(lambda x: x.apply(np.log10))
    elif method == 'log2':
        _df = _df.apply(lambda x: x.apply(np.log2))
    return _df


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


class Timer:

    """
    A context manager for measuring elapsed time using a start and end timestamp.

    __enter__ method sets the start timestamp and returns the Timer instance.
    __exit__ method sets the end timestamp.
    elapsed method calculates and returns the elapsed time as a string.

    Attributes:
        start (pd.Timestamp): The start timestamp.
        end (pd.Timestamp): The end timestamp.

    Methods:
        elapsed(): Calculates and returns the elapsed time as a string.

    Example usage:
        with Timer() as timer:
            # Code to measure elapsed time

        print(timer.elapsed())  # Output: Elapsed time in the format HH:MM:SS.S
    """

    def __init__(self) -> None:
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = pd.Timestamp.now()
        return self

    def __exit__(self, *args):
        self.end = pd.Timestamp.now()

    def elapsed(self):
        return get_proc_time(self.start, pd.Timestamp.now())


def quartile_dispersion(X: pd.Series=None, Q1:float=None, Q3: float=None ):
    """
    Calculates the Quartile Dispersion Coefficient of a given pandas Series.

    Args:
        X: pandas Series. The input data for which the Quartile Dispersion Coefficient is to be calculated.

    Returns:
        float. The Quartile Dispersion Coefficient of the input data.

    suggested use: 
        df['Q_disp_coeff'] = df.apply(quartile_dispersion)
    """
    if X:
        iX = X.describe()
        Q1 = Q1 or iX['25%']
        Q3 = Q3 or iX['75%']
    
    return (Q3 - Q1) / (Q3 + Q1)


def get_mad(X: pd.Series):
    """
    Calculates the Median Absolute Deviation (MAD) of a given pandas Series.

    Args:
        X: pandas Series. The input data for which MAD is to be calculated.

    Returns:
        float. The Median Absolute Deviation (MAD) of the input data.

    suggested use: 
        df['MAD'] = df.apply(get_mad)
    """

    medX = X.median()
    abs_dev = X.apply(lambda x: x - medX).abs()
    return abs_dev.median()