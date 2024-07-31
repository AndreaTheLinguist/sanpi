# coding=utf-8
import contextlib
import re
# import statistics as stat
from collections import namedtuple
# from itertools import chain
from math import sqrt
from pathlib import Path
from time import sleep

import numpy as np
import pandas as pd
from more_itertools import batched

HITS_DF_PATH_REGEX = re.compile(r'_hits.*$')
PART_LABEL_REGEX = re.compile(r'[NAP][pwytcVaTe\d]{2,4}')
WS_REGEX = re.compile(r'[^\S\n]')
REGNOT = re.compile(
    r" (n[o']t?|none|never|neither|nor|nothing|nowhere|[br]arely|hardly|without) ")
NEG_REGEX = re.compile(
    r"\bn[o'](?:[tr]|body|thing|where|ne?)\b|\baint\b|\bneither\b|\b(?<!\w a|the|[oe]se) few\b|\b(?:[br]are|scarce|hard|seldom)l?y?\b|\bwithout\b|\bnever\b")
POS_FEW_REGEX= re.compile(r'\b(?:th[oe](?:s?e?|i?r?)|a|h[ie][rs]|their|my|y?our)\b ?[a-z]* few\b')

OK_REGEX = re.compile(r'^o*\.?k+\.?a*y*$')
V_REGEX = re.compile(r'^v\.?$|^ve+r+y+$')
DEF_REGEX = re.compile(r'^def\.?$')
ESP_REGEX = re.compile(r'^esp\.?$')
EDGE_PUNCT = re.compile(r'^[\W_]+|[\W_]+$')
BRACSLASHDOT_REGEX = re.compile(r'[\[\\\/)]|\.{2,}')
ANY_ALPHA_REGEX = re.compile(r'[a-z]')
MISC_REGEX = re.compile(r'[^a-z0-9_\-\']|[^\d_]+\d[^\d_]+|-[^-]+-[^-]+-[^-]+-')
NAME_REGEX = re.compile(r'(?<=bigram-)\w+(?=_rb)')
# try:
#     import pyarrow
# except ImportError:

#     PYARROW = False
# else:
PYARROW = True

try:
    from source.utils.general import (HIT_TABLES_DIR, PKL_SUFF, confirm_dir, find_files,
                                      snake_to_camel)
except ModuleNotFoundError:
    try:
        from utils.general import (HIT_TABLES_DIR, PKL_SUFF, confirm_dir, find_files,
                                   snake_to_camel)
    except ModuleNotFoundError:
        from general import (HIT_TABLES_DIR, PKL_SUFF,
                             confirm_dir, find_files, snake_to_camel)
#         from associate import adjust_am_names
#     else:
#         from utils.associate import adjust_am_names
# else:
#     from source.utils.associate import adjust_am_names

OPTIMIZED_DTYPES = {
    'string': {
        'sent_id':          'string',
        'bigram_id':        'string',
        'token_str':        'string',
        'sent_text':        'string',
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
        'neg_form_lower':         'category',
        'adv_form_lower':         'category',
        'adj_form_lower':         'category',
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
        'dep_str_mask_rel': 'category'
    },

    # > NUMERICAL
    'numerical': {
        'neg_index':        'category',  # 'uint16'
        'adv_index':        'category',  # 'uint16'
        'adj_index':        'category',  # 'uint16'
        'utt_len':          'category'},  # 'uint16'
}


def add_lower_cols(hit_df: pd.DataFrame) -> pd.DataFrame:
    def get_bigram_lower(_df: pd.DataFrame) -> pd.Series:
        try:
            bigram_lower = (_df['adv_form'] + '_' +
                            _df['adj_form']).str.lower()
        except KeyError:
            try:
                bigram_lower = (_df['adv_form_lower'] + '_' +
                                _df['adj_form_lower'])
            except KeyError:

                #! This should not happen, but...
                print('Warning: Could not create "bigram_lower":',
                      '`ad*_form(_lower)` columns not found!')
                print('current columns:\n-',
                      _df.columns.str.join('\n - '),
                      end='\n\n')
        return bigram_lower

    for form_col in hit_df.filter(['adv_form', 'adj_form', 'bigram', 'neg_form', 'mir_form']).columns:
        lower_col = f'{form_col}_lower'

        if lower_col not in hit_df.columns or any(hit_df[lower_col].isna()):

            if form_col in hit_df.columns:
                hit_df[lower_col] = hit_df[form_col].str.lower()
            elif lower_col == 'bigram_lower':
                hit_df[lower_col] = get_bigram_lower(hit_df)

    return hit_df


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
    """
    Calculate the coefficient of variation for a given Series.

    Args:
        vector (pd.Series): The input Series for which to calculate the coefficient of variation.

    Returns:
        float: The coefficient of variation.
    """

    return vector.std() / vector.mean()


def catify_hit_table(df, reverse: bool = False):
    _df = df.copy().convert_dtypes()

    # if 'part' in _df.columns:
    #     _df.loc[:, 'part'] = _df.part.astype('string')

    # unk_dtypes = _df.select_dtypes(include='object').columns.to_list()
    # if any(unk_dtypes):
    #     _df.loc[:, unk_dtypes] = _df.loc[:, unk_dtypes].convert_dtypes()

    if reverse:
        cat_cols = _df.select_dtypes(include='category').columns
        if any(cat_cols):
            _df[cat_cols] = _df.loc[:, cat_cols].astype('string')
    else:
        non_num = _df.select_dtypes(exclude='number').columns
        cat_cols = non_num[~((non_num.str.startswith(('text', 'dep', 'adj', 'all', 'bigram', 'colloc', 'preceding')))
                             | (non_num.str.endswith(('all_dep_target', 'id', 'text', 'str'))))]
        _df.loc[:, cat_cols] = _df.loc[:, cat_cols].astype(
            'string').astype('category')

    return _df


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


# def count_uniq(series: pd.Series) -> int:
#     return len(series.unique())


def corners(df, size: int = 5, n_dec: int = None):
    """
    Extract the corner values of a DataFrame and display them in a new DataFrame.

    Args:
        df: The input DataFrame to extract corner values from.
        size (int, optional): The number of corner values to display. Defaults to 5.
        n_dec (int, optional): Number of decimals to round the float values to. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the corner values extracted from the input DataFrame.
    """

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


def describe_counts(df: pd.DataFrame = None,
                    df_path: Path = None) -> None:
    if not any(df):
        if df_path.name.endswith(PKL_SUFF):
            df = pd.read_pickle(df_path)
        else:
            print(
                'Stats can only be determined from a given path if indicated file is in pickle format.')
            return

    data_label = df_path.name.replace('.csv', '').replace(PKL_SUFF, '')
    stats_dir = df_path.parent.joinpath('descriptive_stats')
    confirm_dir(stats_dir)
    out_path_stem = f'stats_{data_label}'
    df = df.fillna(0)
    most_var_col = df.columns.to_list()[1:21]
    most_var_row = df.index.to_list()[1:21]
    for frame, ax in ((df, 'columns'), (df.transpose(), 'rows')):
        param = frame.columns.name
        print(
            f'\n## Descriptive Statistics for `{frame.index.name}` by `{param}`')
        no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
        desc_no_sum = no_sum_frame.describe()
        # > need to exclude the ['SUM','SUM'] cell
        sum_col = frame.loc[frame.index != 'SUM', 'SUM']
        desc_sum = sum_col.describe().to_frame()

        for desc, values in [(desc_no_sum, no_sum_frame), (desc_sum, sum_col)]:
            desc = enhance_descrip(values)
            if 'SUM' in desc.index:
                desc = desc.transpose()
                desc.columns = [f'Summed Across {param}s']
                print_md_table(desc.round(), title=' ')
            else:
                save_table(
                    desc,
                    f'{stats_dir}/{param[:4].strip("_-").upper()}-{out_path_stem}',
                    f'{param} descriptive statististics for {out_path_stem}',
                    ['csv'])
                print_md_table(desc.sample(min(len(desc), 6)).round(),
                               title=f'Sample {param} Stats ')

                # [ ] # ? (old) add simple output of just `df.var_coeff`?
                # desc.info()
                if ax == 'columns':
                    most_var_col = _select_word_sample(desc)
                else:
                    most_var_row = _select_word_sample(desc)

    return df.loc[['SUM'] + most_var_row,
                  ['SUM'] + most_var_col], df_path


def _select_word_sample(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
    nth = len(desc) // 6
    trim = int(len(desc) * 0.01)
    desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    top_means_metric = desc.loc[
        (desc['mean'] > (desc_interior['mean'].median() * .75))
        &
        (desc['total'] > (desc_interior['total'].median() * .75)), metric]
    return (
        top_means_metric.squeeze().nlargest(nth).index.to_list()
        if largest
        else top_means_metric.squeeze().nsmallest(nth).index.to_list()
    )


def drop_margins(_df, margin_name='SUM'):
    """
    Drop marginal frequencies from frequency table DataFrame.

    Args:
        _df: The input DataFrame.
        margin_name (str, optional): The name of the margin to drop. Defaults to 'SUM'.

    Returns:
        pd.DataFrame: The DataFrame with the specified margin dropped.
    """

    return _df.loc[_df.index != margin_name, _df.columns != margin_name]

def fix_orth(df: pd.DataFrame,
             using_prior: bool = False):

    ad_cols = df.filter(regex=r'ad[vj]_\w*l[oe]').columns.to_list()
    df = catify_hit_table(df, reverse=True)

    def update_bigram_lower(df):

        return df.assign(bigram_lower=(df.adv_form_lower + '_' + df.adj_form_lower).astype('string'))

    def adv_is_very(df):
        return df.adv_form_lower.str.contains(V_REGEX, regex=True)

    def adv_is_def(df):
        return df.adv_form_lower.str.contains(DEF_REGEX, regex=True)

    def adv_is_esp(df):
        return df.adv_form_lower.str.contains(ESP_REGEX, regex=True)

    def adj_is_ok(df):
        return df.adj_form_lower.str.contains(OK_REGEX, regex=True)
    
    if any(df.adj_form_lower.isna()) or any(df.adv_form_lower.isna()):
        print('\nFixing "null" strings interpreted as NaN...')
        df.loc[:, ad_cols + ['adv_form', 'adj_form']
            ] = df.filter(like='ad').astype('string').fillna('null')
        df = update_bigram_lower(df)
    if not using_prior:
        print('\nDropping most bizarre...\n')
        bracket_slash_dot = (df.bigram_lower.str.contains(
            BRACSLASHDOT_REGEX, regex=True))
        if any(bracket_slash_dot):
            print(df.loc[bracket_slash_dot,
                         ['adv_form_lower', 'adj_form_lower']].astype('string').value_counts()
                  .nlargest(10).to_frame().reset_index()
                  .to_markdown(floatfmt=',.0f', intfmt=','))
            df = df.loc[~bracket_slash_dot, :]

        alpha_adv = df.adv_form_lower.str.contains(ANY_ALPHA_REGEX, regex=True)
        alpha_adj = df.adj_form_lower.str.contains(ANY_ALPHA_REGEX, regex=True)
        either_no_alpha = (~alpha_adv) | (~alpha_adj)
        if any(either_no_alpha):
            print('\nDropping any ad* that contain no regular characters (a-z)')
            print(df.loc[either_no_alpha, ['adv_form_lower', 'adj_form_lower', 'text_window']]
                  .astype('string').value_counts().nlargest(10).to_frame().reset_index().to_markdown(floatfmt=',.0f')
                  )
            df = df.loc[~either_no_alpha, :]

    # > variations on "very"
    v_adv = (adv_is_very(df)) & (df.adv_form_lower != 'very')
    ok_adj = adj_is_ok(df) & (df.adj_form_lower != 'ok')
    definitely_adv = adv_is_def(df)
    esp_adv = adv_is_esp(df)
    if any(v_adv | ok_adj | definitely_adv | esp_adv):
        print('\nTranslating some known orthographic quirks...')
        if any(v_adv):
            print('\n==== very ====')
            print(df.loc[v_adv, 'adv_form_lower']
                .astype('string').value_counts().nlargest(10).to_frame()
                .to_markdown(floatfmt=',.0f', intfmt=','))
            df.loc[v_adv, :] = df.loc[v_adv, :].assign(
                adv_lemma='very',
                adv_form_lower='very')

        # > variations on "ok"
        if any(ok_adj):
            print('\n==== ok ====')
            print(df.loc[ok_adj, 'adj_form_lower']
                .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                .to_markdown(floatfmt=',.0f', intfmt=','))
            df.loc[ok_adj, :] = df.loc[ok_adj, :].assign(
                adj_form_lower='ok',
                adj_lemma='ok')

        # > variations on "definitely"
        if any(definitely_adv):
            print('\n==== definitely ====')
            print(df.loc[definitely_adv, 'adv_form_lower']
                .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                .to_markdown(floatfmt=',.0f', intfmt=','))
            df.loc[definitely_adv, :] = df.loc[definitely_adv, :].assign(adv_form_lower='definitely',
                                                                        adv_lemma='definitely')

        # > variations on "especially"
        if any(esp_adv):
            print('\n==== especially ====')
            print(df.loc[esp_adv, 'adv_form_lower']
                .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                .to_markdown(floatfmt=',.0f', intfmt=','))
            df.loc[esp_adv, :] = df.loc[esp_adv, :].assign(adv_form_lower='especially',
                                                        adv_lemma='especially')

    adv_punct = df.adv_form_lower.str.contains(EDGE_PUNCT, regex=True)
    adj_punct = df.adj_form_lower.str.contains(EDGE_PUNCT, regex=True)
    punct_edge = adv_punct | adj_punct
    if any(punct_edge):
        print('\nStripping leading/trailing punctuation...\n')
        print(df.loc[punct_edge].filter(
            ad_cols).sort_values('adv_lemma').to_markdown())
        df.loc[punct_edge, ad_cols] = df.loc[punct_edge, ad_cols].apply(
            lambda a: a.apply(
                lambda w: EDGE_PUNCT.sub('', w)))

    df = update_bigram_lower(df)
    # if not using_prior:
    #! realized this was only catching advs (typo listed `one_char_adv | one_char_adv`, so it needs to be rerun)
    # > drop any single character "words"
    one_char_adv = df.adv_form_lower.str.len() == 1
    one_char_adj = df.adj_form_lower.str.len() == 1
    either_one_char = one_char_adv | one_char_adj
    if any(either_one_char):
        print('\nDropping any single character "words"')
        print(df.loc[either_one_char, ['adv_form_lower', 'adj_form_lower']]
                .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                .to_markdown(floatfmt=',.0f', intfmt=','))
        df = df.loc[~either_one_char, :]

    odd_remnant = df.bigram_lower.str.contains(MISC_REGEX, regex=True)
    if any(odd_remnant):
        print('\nMiscellaneous Remaining Oddities Dropped\n')
        if using_prior:
            print(
                'WARNING‼️ This is unexpected, since index from partial prior processing was used.')
        print(df[odd_remnant].value_counts('bigram_lower').to_markdown())
        df = df.loc[~odd_remnant, :]
    df = df.loc[~df.adv_form_lower.isin({'is', 'ie', 'etc', 'th'}), :]
    df = update_bigram_lower(df)
    if any(df.filter(regex=r'(?:mir|neg)*lower').columns):
        df['all_forms_lower'] = df.filter(regex=r'(?:mir|neg)\w*lower').squeeze() + '_' + df.bigram_lower
    return catify_hit_table(df)

def translate_orth_forms(df, verbose=False):
    ## ! OLD version
    df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
           ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
                      ].astype('string')

    def adv_is_very(df):
        return df.adv_form_lower.str.contains(r'^v\.?$|^ve+r+y+$', regex=True)

    def adv_is_def(df):
        return df.adv_form_lower.str.contains(r'^def\.?$', regex=True)

    def adj_is_ok(df):
        return df.adj_form_lower.str.contains(r'^o*\.?k+\.?a*y*$', regex=True)

    _very = adv_is_very(df)
    _ok = adj_is_ok(df)
    _definitely = adv_is_def(df)
    if verbose and any(_very|_ok|_defin):
        print('\nTranslating some known orthographic quirks...')
    # > variations on "very"
    if any(_very):
        if verbose:
            print('\n==== very ====')
            print(df.loc[_very, 'adv_form_lower']
                    .astype('string').value_counts().nlargest(10).to_frame()
                    .to_markdown(floatfmt=',.0f', intfmt=','))

        df.loc[_very, :] = df.loc[_very, :].assign(
            adv_lemma='very',
            adv_form_lower='very')

    # > variations on "ok"
    if any(_ok):
        if verbose:
            print('\n==== ok ====')
            print(df.loc[_ok, 'adj_form_lower']
                    .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                    .to_markdown(floatfmt=',.0f', intfmt=','))

        df.loc[_ok, :] = df.loc[_ok, :].assign(
            adj_form_lower='ok',
            adj_lemma='ok')

    # > variations on "definitely"
    if any(_definitely):
        if verbose:
            print('\n==== definitely ====')
            print(df.loc[_definitely, 'adv_form_lower']
                    .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                    .to_markdown(floatfmt=',.0f', intfmt=','))
        df.loc[_definitely, :] = df.loc[_definitely, :].assign(
            adv_form_lower='definitely',
            adv_lemma='definitely')
    return df.convert_dtypes()


def remove_orth_forms(df):
    ## ! OLD version
    df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
           ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
                      ].astype('string')

    # def adv_is_very(df):
    #     return df.adv_form_lower.str.contains(r'^v\.?$|^ve+r+y+$', regex=True)

    # def adv_is_def(df):
    #     return df.adv_form_lower.str.contains(r'^def\.?$', regex=True)

    # def adj_is_ok(df):
    #     return df.adj_form_lower.str.contains(r'^o*\.?k+\.?a*y*$', regex=True)

    print('Dropping most bizarre...\n')
    print(df.loc[df.bigram_lower.str.contains(r'[\[\\\/)]', regex=True),
          ['adv_form_lower', 'adj_form_lower']].astype('string').value_counts()
          .nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df = df.loc[~df.bigram_lower.str.contains(r'[\[\\\/)]', regex=True), :]

    print('\nDropping plain numerals as adjectives')
    print()
    print(df.loc[df.adj_form_lower.astype('string').str.contains(r'^\d+$'), ['adv_form_lower', 'adj_form_lower', 'text_window']]
          .astype('string').value_counts().nlargest(10).to_frame().reset_index().to_markdown(floatfmt=',.0f')
          )
    df = df.loc[~df.adj_form_lower.astype('string').str.contains(r'^\d+$'), :]

    # > drop any single character "words"
    print()
    print(df.loc[df.adv_form_lower.str.contains(
        r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
        .astype('string').value_counts().nlargest(10).to_frame().reset_index()
        .to_markdown(floatfmt=',.0f', intfmt=','))
    print()
    print(df.loc[df.adj_form_lower.str.contains(
        r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
        .astype('string').value_counts().nlargest(10).to_frame().reset_index()
        .to_markdown())
    df = df.loc[~((df.adv_form_lower.str.contains(r'^\w\W*$'))
                  | (df.adj_form_lower.str.contains(r'^\w\W*$'))), :]

    # > delete remaining non-word characters (esp. `.` & `*`)
    df = df.assign(
        adv_form_lower=df.adv_form_lower.str.strip(
            '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
        adv_lemma=df.adv_lemma.str.strip(
            '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True),
        adj_form_lower=df.adj_form_lower.str.strip(
            '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
        adj_lemma=df.adj_lemma.str.strip(
            '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True)
    )
    df = df.loc[~df.adv_form_lower.isin({'is', 'ie'}), :]
    print('\n'+r"** ** ** Remaining [^\w'-] ** ** **")

    print(df.loc[(df.adv_form_lower.str.contains(r"[^\w'-]", regex=True))
                 | (df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)),
                 ['adv_form_lower', 'adj_form_lower']]
          .astype('string').value_counts()
          .nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=',')
          )

    return df.convert_dtypes()


# def add_lower_cols(df: pd.DataFrame) -> pd.DataFrame:
#     def get_bigram_lower(df: pd.DataFrame) -> pd.Series:
#         try:
#             bigram_lower = (df['adv_form_lower'] + '_' +
#                             df['adj_form_lower'])
#         except KeyError:
#             try:
#                 bigram_lower = (df['adv_form'] + '_' +
#                                 df['adj_form']).str.lower()
#             except KeyError:

#                 #! This should not happen, but...
#                 print(f'Warning: Could not add column `{lower_col}`:',
#                       '`ad*_form(_lower)` columns not found!')
#                 print('current columns:\n-',
#                       df.columns.str.join('\n - '),
#                       end='\n\n')
#         return bigram_lower

#     for form_col in df.filter(['adv_form', 'adj_form', 'neg_form', 'mir_form']
#                               ).columns.to_list() + ['bigram']:
#         lower_col = f'{form_col}_lower'

#         if lower_col not in df.columns:

#             if form_col in df.columns:
#                 df.loc[:, lower_col] = df.loc[:, form_col].str.lower()
#             elif lower_col == 'bigram_lower':
#                 df.loc[:, lower_col] = get_bigram_lower(df)

#     return df


def add_new_cols(df, load_path: Path = None, part: str = None):
    df = catify_hit_table(df, reverse=True)
    part = part or PART_LABEL_REGEX.search(load_path.stem).group()
    df = df.assign(part=part)
    df['part'] = df.part.astype('string')
    df = add_lower_cols(df)
    # if any(df.index.str.startswith('pcc')):
    # df['slice'] = df.index.str.split(
    #     '.').str.get(0).astype('string')
    # else:
    # df['slice'] = df.index.str.split(
    #     '_').str[:3].str.join('_').str[:-2].astype('string')
    if any(df.filter(regex=r'neg_|mir_').columns):
        if 'neg_form' in df.columns:
            df.loc[df.neg_form.isna(), 'neg_form'] = 'None'
            df.loc[df.neg_form_lower.isna(), 'neg_form_lower'] = 'none'
            
        df['trigger_lower'] = df.filter(
            regex=r'(neg|mir)_form_lower').squeeze()
        df['trigger_lemma'] = df.filter(regex=r'(neg|mir)_lemma').squeeze()
        if 'all_forms_lower' not in df.columns:
            df['all_forms_lower'] = df.trigger_lower + '_' + df.bigram_lower

    return catify_hit_table(df)


def filter_csv_by_index(df_csv_path: Path,
                        index_txt_path: Path,
                        dtype_dict: dict,
                        outpath: Path = None):

    def _gen_chunk_batch(reader, batches):
        c = 1
        for chunk in reader:
            chunk = chunk.rename(columns={'colloc': 'bigram',
                                          'colloc_id': 'bigram_id'})
            use_index = not ('bigram_id' in chunk.columns
                             and any(chunk.filter(regex=r'neg|mir').columns))
            print('-'*30)
            print(f'* {len(chunk):,} rows in csv chunk {c}')
            c += 1
            b = 1
            for batch in batches:
                # print(f'{len(batch):,} ids in index batch')
                match_chunk = (chunk.filter(batch, axis=0)
                               if use_index
                               else chunk.loc[chunk.bigram_id.isin(batch), :]
                               ).sort_index()
                print(f'  * {len(match_chunk):,} rows matching index batch {b}')
                print(
                    f'    ({round(len(match_chunk)/len(chunk)*100, 1):.1f}% of chunk)')
                b += 1
                if len(match_chunk) > 0:
                    print('\n    ' +
                          match_chunk.filter(
                              regex=r'lower|hit|win|id|at').describe().T
                          .to_markdown(floatfmt=',.0f', intfmt=',').replace('\n', '\n    '), end='\n\n')
                    yield match_chunk

    dtype_dict = dtype_dict or {k: v
                                for c in OPTIMIZED_DTYPES.values()
                                for k, v in c.items()}
    keepers = set(index_txt_path.read_text().splitlines())
    print(f'{len(keepers):,} ids in loaded index filter')
    keep_batches = tuple(batched(keepers,  max(1000, 1 + len(keepers)//6)))
    # keep_batches = tuple(batched(keepers, 20000))

    with pd.read_csv(df_csv_path,
                     index_col='hit_id',
                     skipinitialspace=True,
                     dtype=dtype_dict, engine='c',
                     chunksize=200000) as csv_reader:
        csv_iter = _gen_chunk_batch(csv_reader, keep_batches)
        if outpath and '.csv' in outpath.suffixes:
            c = 0
            for filter_chunk in csv_iter:
                # > newly added adjustments to hit_tables
                #// filter_chunk = add_lower_cols(filter_chunk.copy())
                #// filter_chunk = translate_orth_forms(filter_chunk)
                filter_chunk = add_new_cols(filter_chunk,
                                             load_path=df_csv_path)
                filter_chunk = fix_orth(filter_chunk, using_prior=True)
                filter_chunk.index.name = 'hit_id'
                filter_chunk.to_csv(outpath,
                                    mode=('w' if c == 0 else 'a'),
                                    header=c == 0)
                c += 1
            print('\n'+'*'*30)
        else:
            return pd.concat(csv_iter)


def extend_window(df: pd.DataFrame,
                  tokens_before: int = 7,
                  tokens_after: int = 7):
    def _get_bigram_only_window():

        # tok_lists = df.token_str.str.lower().str.split()

        # return [
        #     ' '.join(tok_lists.iloc[i][max(
        #         0, idx - tokens_before):(idx + 1 + tokens_after)])
        #     for i, idx in enumerate(df.adv_index)
        # ]
        tok_lists = df.token_str.str.lower().str.split().tolist()
        adv_indices = df.adv_index.tolist()

        yield from (
            ' '.join(tok_list[max(0, idx - tokens_before):(idx + 1 + tokens_after)])
            for tok_list, idx in zip(tok_lists, adv_indices)
        )
    def _get_triggered_window():

        tok_lists = df.token_str.str.lower().str.split()
        ix_df = df.copy().select_dtypes(include='number')
        ix_df['_tmp_zero'] = 0
        ix_df['extend_end'] = ix_df.adv_index.add(1) + tokens_after
        ix_df['extend_start'] = ix_df.adv_index - tokens_before
        ix_df['max_before'] = ix_df[['_tmp_zero', 'extend_start']].max(axis=1)
        ex_win_start =(ix_df.filter(['max_before', 'neg_index', 'mir_index'])
                                .min(axis=1))
        ex_win_end = ix_df[['extend_end', 'utt_len']].min(axis=1)

        # print(ix_df
        #       .assign(ex_win_start=ex_win_start, 
        #               ex_win_end=ex_win_end, 
        #              new_window_len=ex_win_end - ex_win_start)
        #       .sample(30)
        #       .to_markdown(tablefmt='rounded_grid', index=False))

        for i, (start, end) in enumerate(zip(ex_win_start, ex_win_end)):

            yield ' '.join(tok_lists.iloc[i][start:end])

    if any(df.filter(regex=r'neg|mir|trigger').columns):
        text_windows = _get_triggered_window()
    else:
        text_windows = _get_bigram_only_window()

    df['text_window'] = pd.Series(
        text_windows, dtype='string', index=df.index)
    df['window_len'] = pd.to_numeric(
        df.text_window.str.count(' ').add(1), downcast='unsigned')
    return df



def get_neg_equiv_sample(all_enforced, com_dir, 
                         neg_name:str='RBdirect'):
    comp_total = len(all_enforced)
    # [x] Update this method to get total updated `RBdirect` count if it exists---use counts in `../info/` dir
    neg_subtotals_csv = com_dir.parent.parent.joinpath(
        f'info/ALL_{neg_name}_final-subtotals.csv')
    neg_total = None
    
    if neg_subtotals_csv.is_file():
        try:
            neg_total = pd.read_csv(neg_subtotals_csv, dtype={'total_hits': 'int'},
                                    usecols=['total_hits']).squeeze().sum()
        except:
            neg_total = None
    if neg_total is None:
        neg_dir = com_dir.parent / neg_name / 'cleaned'
        neg_counts = neg_dir/'index_counts.txt'
        if not neg_counts.is_file():
            run_shell_command(
                '; '.join(f'echo "wc -l {neg_dir}/*txt > {neg_counts}"'
                          f'wc -l {neg_dir}/*txt > {neg_counts}')
            )
        neg_total = int(neg_counts.read_text(
            encoding='utf8').splitlines()[-1].split()[0])

    print(f'\n## Creating negated sample equivalent: N = {neg_total:,}\n')
    combined_total = comp_total + neg_total
    print('+ updated NEG:',
          f'{round(neg_total/combined_total * 100, 1):.1f}%',
          'of all bigrams')
    print('+ updated COM:',
          f'{round(comp_total/combined_total * 100, 1):.1f}%',
          'of all bigrams')
    print(f'+ ~{round(comp_total / neg_total)}:1 odds',
          'that utterance is _NOT negated_')
    print(f'+ Sample: {round(neg_total/comp_total * 100, 1):.1f}%',
          'of entire updated complement')

    return all_enforced.sample(min(comp_total, neg_total))


def remove_duplicates(hit_df: pd.DataFrame,
                      w_before: int = 7,
                      w_after: int = 7,
                      return_index: bool = False):
    def weed_windows(df: pd.DataFrame,
                     w_before: int = 7,
                     w_after: int = 7,
                     return_index: bool = False):
        if 'adv_index' not in df.columns:
            df['adv_index'] = pd.to_numeric(df.index.str.split(
                ':').str.get(-1).str.split('-').str.get(-2), downcast='integer')
        if 'window_len' not in df.columns:
            df['window_len'] = pd.to_numeric(
                df.text_window.str.count(' ').add(1), downcast='unsigned')
        extendable = (df.window_len < (w_before + w_after)
                      ) & (df.window_len < df.utt_len)
        if any(extendable):

            df.loc[extendable, :] = extend_window(
                df=df.copy().loc[extendable, :],
                tokens_before=w_before,
                tokens_after=w_before)

        over_20 = df.utt_len > 20
        yield df.loc[~over_20].index.to_series() if return_index else df.loc[~over_20]

        df_over20 = df.copy().loc[over_20, :]
        info_df = over_20.value_counts().to_frame('sent >20 tokens')
        compare_cols = df.filter(['text_window', 'all_forms_lower',
                                  'bigram_lower', 'adv_form_lower']
                                 ).columns.to_list()[:2]
        is_duplicated = df_over20[compare_cols].duplicated(
            keep=False, subset=compare_cols)
        if any(is_duplicated):
            info_df['& is/has duplicate'] = is_duplicated.value_counts()
            discard = df_over20[compare_cols].duplicated(
                keep='first', subset=compare_cols)
            info_df['& will be removed'] = discard.value_counts()
            info_df.index.name = '# hits...'
            print('\nCompiled Duplicatation Counts\n\n' +
                  info_df.to_markdown(intfmt=',', floatfmt=',.0f'))
            print('\nExample of Duplication Removal (1 kept per "text_window")\n\n```log')
            print((df_over20[is_duplicated]
                  .filter(['utt_len', 'bigram_lower', 'text_window', 'token_str'])
                   .sort_values(['bigram_lower', 'text_window']))
                  .head(6)
                  .to_markdown(maxcolwidths=[18, None, None, 28, 50], 
                               tablefmt='rounded_grid'))
            print('```\n')
            keep_over20 = df_over20.loc[~discard, :]
            yield keep_over20.index.to_series() if return_index else keep_over20
        else:
            print('\n> [[ No duplicates found ]]\n')
            yield df_over20.index.to_series() if return_index else df_over20

    if 'utt_len' not in hit_df.columns:
        hit_df['utt_len'] = pd.to_numeric(
            hit_df.token_str.str.count(' ').add(1),
            downcast='integer')

    succinct = pd.concat(
        weed_windows(df=hit_df, return_index=return_index,
                     w_before=w_before, w_after=w_after)
    )
    print(f'* {len(succinct):,} hits remaining after additional duplicate filtering',
          f'  * ({len(hit_df) - len(succinct):,} hits removed as duplicates.)',
          sep='\n')

    return succinct


def deprel_quarantine(df):
    # _should_ have been prohibited, but ㄟ( ▔, ▔ )ㄏ
    left_head_prohibit = {
        'acl:relcl', 'advcl', 'appos', 'conj', 'nmod', 'parataxis'
    }
    right_head_prohibit = {
        'advcl', 'amod', 'discourse', 'prep', 'obl', 'obl:npmod',
        'parataxis', 'dislocated', 'rel'
    }
    left_head_quarantine = {
        'acl',  # ?  might be ok?
        'obl', 'advmod', 'acomp', 'nsubj',
        'attr', 'dobj', 'list', 'partmod', 'prep'
    }
    right_head_quarantine = {
        'nsubjpass', 'attr', 'punct', 'csubj', 'ccomp', 'reparandum',
        'obj', 'compound', 'expl', 'partmod', 'dep', 'conj'
    }

    deprel = df.filter(regex=r'(?:neg|mir)_deprel').squeeze()
    head = df.filter(regex=r'(?:neg|mir)_head').squeeze()

    adj_quarantine = (deprel.isin(right_head_quarantine) & (head == 'ADJ'))
    trigger_quarantine = (deprel.isin(left_head_quarantine) & (head != 'ADJ'))
    df = df.assign(quarantine=adj_quarantine | trigger_quarantine)

    adj_prohibited = (deprel.isin(right_head_prohibit) & (head == 'ADJ'))
    trigger_prohibited = (deprel.isin(left_head_prohibit) & (head != 'ADJ'))
    prohibited = (adj_prohibited | trigger_prohibited)
    if any(prohibited):
        n_prohibited = len(df[prohibited])
        print(
            f'Removing {n_prohibited:,} hits with prohibited dependency relation types; e.g.:')
        show_sample(df[prohibited].filter(
            regex=r'^all.*lower|text_win|dist|[^d]_deprel').head(5))
        df = df.loc[~prohibited, :]
    return df


def drop_not_only(df):
    pos_not_only = ((df.hit_text.str.lower().str.startswith('not only') )
                    & (df.adv_form_lower != 'only') 
                    & (df.trigger_lemma=='not'))
    init_len = len(df)
    if any(pos_not_only):
        drops = df[pos_not_only]
        drop_ex = drops.sample(min(5,len(drops)))
        show_sample(drop_ex[['all_forms_lower','hit_text']], format='fancy_grid')
        df = df.loc[~pos_not_only, :]
        print(f'* {len(df):,} hits remaining ({(len(df)/init_len * 100):.1f}%)',
            'after excluding "not only (*) ADV ADJ" from negated environment', 
            f'* {len(drops):,} excluded', sep='\n  ')
    return df


def quarantine_deps(df,
                    dep_distance_ceiling: int = 15,
                    dep_distance_floor: int = 5):
    init_len = len(df)
    df = df.assign(
        dep_distance=pd.to_numeric(
            df.adv_index - df.filter(regex=r'^[^a].*index').squeeze(),
            downcast='unsigned'),
        window_len=pd.to_numeric(
            df.text_window.str.count(' ').add(1), downcast='unsigned'))

    df = deprel_quarantine(df.copy())
    in_quarantine = df.quarantine

    over_min = df.dep_distance > dep_distance_floor
    over_max = df.dep_distance > dep_distance_ceiling
    drop_row = over_max | (over_min & in_quarantine)
    if any(drop_row):
        if any(over_max):
            n_distant = over_max.value_counts()[True]
            print(f'- Dropping {n_distant:,} hits with more than',
                  f'{dep_distance_ceiling} tokens between trigger and ADJ')
            drop_ex = df[over_max].sample(
                min(10, n_distant)).sort_values('dep_distance')
            show_sample(drop_ex.filter(['dep_distance', 'all_forms_lower',  # 'hit_text',
                                        'text_window', 'neg_deprel', 'mir_deprel']), 
                        format='fancy_grid')
        if any(over_min & in_quarantine):
            n_quarantine = (drop_row & ~over_max).value_counts()[True]
            print(
                f'- Dropping {n_quarantine:,} hits with more than',
                f'{dep_distance_floor} tokens between trigger and ADJ',
                'and questionable deprel type')
            drop_ex = df[drop_row & ~over_max].nsmallest(min(n_quarantine, 10), columns=[
                                                         'dep_distance']).sort_values('dep_distance')
            show_sample(drop_ex.filter(['dep_distance', 'all_forms_lower',  # 'hit_text', 'token_str',
                                        'text_window', 'neg_deprel', 'mir_deprel', 'neg_head', 'mir_head']), 
                        format='fancy_grid')
        df = df.loc[~drop_row, :]
    print(f'* {len(df):,} remaining hits after validating dependencies', 
          f'* {len(df)/init_len*100:.1f}% of pre-validation.',
          f'* ({init_len - len(df):,} dropped.)', 
          sep='\n  ')
    return df


def set_col_widths(df):
    cols = df.copy().reset_index().columns
    width_dict = (
        {c: None for c in cols}
        | {c: 21 for c in cols[cols.str.contains('_id')]}
        | {c: 50 for c in cols[cols.str.contains('text')]}
        | {c: 32 for c in cols[cols.str.contains('form')]}
        | {c: 65 for c in cols[cols.str.contains('_str')]})
    return list(width_dict.values())


def embolden(strings: pd.Series,
             bold_regex: str = None,
             mono: bool = True) -> pd.Series:
    bold_regex = re.compile(bold_regex, flags=re.I) if bold_regex else REGNOT
    if mono:
        return strings.apply(lambda x: bold_regex.sub(r' __`\1`__ ', x))
    else:
        return strings.apply(lambda x: bold_regex.sub(r' __\1__ ', x))


def show_sample(df: pd.DataFrame,
                format: str = 'grid',
                n_dec: int = 0,
                limit_cols: bool = True,
                assoc: bool = False):
    _df = df.copy().convert_dtypes()
    if limit_cols and format != 'pipe' and not assoc:
        print(_df.to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=',',
            maxcolwidths=set_col_widths(_df),
            tablefmt=format
        ))
    else:
        if assoc:
            if not bool(n_dec):
                n_dec = 2
            _df = adjust_am_names(_df)

        print(_df.to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=',',
            tablefmt=format
        ))


def adjust_few_hits(df):
    init_few_count = df.neg_form_lower.value_counts()['few']
    print('* Validating "few" tokens')
    print(f'  * {init_few_count:,} unvalidated "few" tokens')
    # this should match:
    # "{the, a, those, these, her, his, their, my, your, our}
    #  ({lucky, next, last, fortunate, remaining, select, very, relative, chosen, etc.})
    #  few"
    a_few = df.text_window.str.lower().str.contains(r'\ba few\b', regex=True)
    df = df.loc[~((df.neg_form_lower == 'few') & a_few), :]
    exist_few = df.text_window.str.lower().str.contains(
        POS_FEW_REGEX,
        regex=True)
    df = df.loc[~((df.neg_form_lower == 'few') & exist_few), :]
    print(f"  * {df.neg_form_lower.value_counts()['few']:,}",
          "remaining after validation")
    return df


def beef_up_dtypes(df: pd.DataFrame,
                   integers: bool = True,
                   floats: bool = True):
    """
    Beef up the data types of a DataFrame by converting columns to specified data types.

    Args:
        df (pd.DataFrame): The input DataFrame to modify.
        integers (bool, optional): Whether to convert integer columns. Defaults to True.
        floats (bool, optional): Whether to convert float columns. Defaults to True.

    Returns:
        pd.DataFrame: The DataFrame with updated data types.

    Examples:
        df = beef_up_dtypes(df, integers=True, floats=False)
    """

    if floats:
        float_cols = df.select_dtypes(include='float').columns
        df[float_cols] = df[float_cols].astype('float64')
    if integers:
        ints = df.select_dtypes(include='int').columns
        df[ints] = df[ints].astype('int64')
    return df


def enhance_descrip(df: pd.DataFrame, strings: bool = False) -> pd.DataFrame:
    """
    Enhance the description of a DataFrame by adding additional statistical metrics.

    Args:
        df (pd.DataFrame): The input DataFrame for which to enhance the description.

    Returns:
        pd.DataFrame: The DataFrame with enhanced statistical metrics added to the description.
    """

    desc = df.describe().transpose()
    desc = desc.assign(total=pd.to_numeric(df.sum()),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'],
                       Q_disper=df.apply(quartile_dispersion),
                       MAD=df.apply(get_mad))
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    # if 'SUM' not in desc.index:
    #     desc = desc.assign(
    #         plus1_geo_mean=df.add(1).apply(stat.geometric_mean),
    #         plus1_har_mean=df.add(1).apply(stat.harmonic_mean))
    int_cols = {'count', 'min', 'max', 'total', 'range'}
    for col in desc.columns:
        if col in int_cols:
            desc.loc[:, col] = pd.to_numeric(
                desc.loc[:, col], downcast='unsigned')
        # if col in ('mean', 'std', 'variance', 'var_coeff'):
        else:
            desc.loc[:, col] = pd.to_numeric(
                desc[col].round(1), downcast='float')

    # mean_centr = no_sum_frame - no_sum_frame.mean()
    # mean_stand = no_sum_frame / no_sum_frame.mean()
    # mean_stand_centr = mean_stand - mean_stand.mean()
    # log2_trans = no_sum_frame.apply(np.log2)
    # log2_plus1_trans = no_sum_frame.add(1).apply(np.log2)
    # logn_plus1_trans = no_sum_frame.apply(np.log1p)

    return desc.rename(columns={'50%': 'median',
                                'count': 'unique_forms'})


def get_proc_time(start: pd.Timestamp, end: pd.Timestamp) -> str:
    t_comp = (end - start).components
    return "`" + (
        ":".join(
            str(c).zfill(2)
            for c in (t_comp.hours, t_comp.minutes, t_comp.seconds)
        )
        + f'.{round(t_comp.microseconds, 1)}'
    ) + "`"


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

# def nb_print_table(df, n_dec:int=2,
#                    adjust_columns:bool=True) -> None:
#     _df = df.copy()
#     if adjust_columns:
#         _df = adjust_assoc_columns(_df)
#     _df.columns = [f'`{c}`' for c in _df.columns]
#     _df.index = [f'**{r}**' for r in _df.index ]
#     print('\n'+_df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')+'\n')


def print_md_table(input_df: pd.DataFrame,
                   indent: int = 0,
                   title: str = '',
                   comma: bool = True,
                   n_dec: int = 0,
                   suppress: bool = False,
                   max_colwidth: int = 60,
                   max_cols: int = None,
                   max_width: int = None,
                   describe: bool = False,
                   transpose: bool = False,
                   format: str = 'pipe'
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
    # set_pd_display(max_colwidth, max_cols, max_width)

    if describe:
        _df = input_df.describe()
    floatfmt = f"{',' if comma else ''}.{n_dec}f"
    # FIXME this doesn't actually work. Integers seem to be treated as floats quite often. Could be when they are very large values? i.e. were put into scientific notation?
    intfmt = ',' if comma else ''

    float_data = _df.select_dtypes(include='float')
    if any(float_data):
        _df.update(float_data.apply(pd.to_numeric, downcast='float',
                   axis=1).apply(np.around, decimals=n_dec, axis=1))

    if transpose:
        _df = _df.T.convert_dtypes()

    # md_table = _df.to_markdown(tablefmt="grid", floatfmt=floatfmt, numalign='decimal')
    if any(_df.select_dtypes(include='string')):
        str_cap = int((max_colwidth*2.75)-3)
        _df.update(
            _df.loc[:,
                    _df.astype('string')
                    .apply(lambda c: max([len(x) for x in c]) > str_cap)]
            .apply(
                lambda y: y.apply(
                    lambda z: (str(z)[:str_cap]
                               + ('...' if len(z) > str_cap
                                  else ''))
                )
            )
        )
    if max_cols and max_cols < _df.shape[1]:
        _df = _df.iloc[:, int(max_cols//2)
                       ].join(_df.iloc[:, -int(max_cols//2)])
    md_table = _df.to_markdown(floatfmt=floatfmt,
                               intfmt=intfmt,
                               maxcolwidths=max_colwidth,
                               tablefmt=format)
    title = title.strip('\n')
    ws = ' ' * indent
    print_str = f"\n{ws}{title}\n\n{ws}" if title else f'{ws}\n{ws}'
    print_str += md_table.replace('\n', f'\n{ws}') + '\n'

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


def save_advadj_freq_tsv(final_hits: pd.DataFrame,
                         freq_tsv_path: Path = None):
    joint_f = final_hits.bigram_lower.value_counts().to_frame('f')
    joint_f = joint_f.join(
        joint_f.index.to_series()
        .str.extract(r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$'))
    sorts = [fx.sort_index() for __, fx in joint_f.sort_values(
        ['f'], ascending=False).groupby('f')]
    sorts.reverse()
    joint_f = pd.concat(sorts, ignore_index=True)
    print('\n  Top 10 joint frequencies:\n\n       ',
          joint_f.nlargest(10, columns='f')
          .to_markdown(tablefmt='plain', intfmt=',',
                       index=False)
          .replace('\n', '\n        '),
          '\n')
    
    if freq_tsv_path is None:
        return joint_f

    joint_f.to_csv(freq_tsv_path,
                    sep='\t',
                    index=False,
                    header=False)
    print_path_info(freq_tsv_path, 
                    'basic `adv~adj` frequencies for final hits')


def save_final_info(final_hits: pd.DataFrame,
                    data_dir: Path,
                    tag: str = 'ALL',
                    basic_column_filter: list = None,
                    partition_by: list = None,
                    max_parq_rows: int = 50000,
                    date_flag: str = None):
    print('')
    partition_by = partition_by or ['category', 'part']
    basic_column_filter = pd.Series(
        (basic_column_filter
         or ['hit_id', 'category',
             'trigger_lemma',
             'adv_form_lower', 'adj_form_lower']) + partition_by
    ).drop_duplicates().to_list()

    info_dir = data_dir.parent.parent / 'info'
    confirm_dir(info_dir)
    freq_tsv_dir = data_dir / 'ucs_format'
    confirm_dir(freq_tsv_dir)
    category = data_dir.name
    final_hits = final_hits.assign(category=category)
    # > set paths
    # tag basic.replace('NEQ',f'NEQ-{timestamp_now()}')
    date_flag = date_flag or (
        f'.{pd.Timestamp.now().strftime("%y%m%d%H")}'
        if tag == 'NEQ' else '')

    subtotals_path = info_dir.joinpath(
        f'{tag}_{category}_final-subtotals{date_flag}.csv')

    final_index_path = data_dir.joinpath(
        f'{tag}_{category}_final-index{date_flag}.txt')

    basic_freq_tsv = freq_tsv_dir.joinpath(
        f'AdvAdj_{tag}_{category}-final-freq{date_flag}.tsv')

    final_basic_parq = info_dir.joinpath(
        f'{tag}_final-hits_basic{date_flag}.parq')

    # * save subtotals for part
    (final_hits
     .value_counts(['part', 'category'])
     .to_frame('total_hits')
     .reset_index()
     .to_csv(subtotals_path, index=False))
    obj_name='Part Subtotals'
    print_path_info(subtotals_path, obj_name)

    # >>>>>>>>>
    sleep(1)

    final_index = final_hits.index.to_list()
    final_index.sort()
    final_index_path.write_text('\n'.join(final_index), encoding='utf8')
    print_path_info(obj_name=f'`hit_id` index for final selection of `{category}` hits',
          path=final_index_path)
    sleep(1)
    # * save basic frequency TSV!
    # final_hits['bigram_lower'] = final_hits.bigram_lower.astype('string').astype('category')
    save_advadj_freq_tsv(final_hits, basic_freq_tsv)

    # >>>>>>>>>
    print(('\n----------------------\n'
           '> *temporarily paused*\n'
           '----------------------\n'))
    sleep(30)

    final_hits = final_hits.sort_index().reset_index()
    # > save most basic info as parquet

    max_parq_rows = int(
        max_parq_rows
        if 'slice' in partition_by
        else max(max_parq_rows,
                 round(((final_hits.part.value_counts().mean()//10)
                        * 1.005), -3))
    )
    group_max = max_parq_rows//2
    final_hits = catify_hit_table(final_hits
                                  .filter(basic_column_filter))
    final_hits.to_parquet(str(final_basic_parq),
                          index=None,
                          partition_cols=partition_by,
                          engine='pyarrow',
                          basename_template='group-{i}.parquet',
                          use_threads=True,
                          existing_data_behavior='delete_matching',
                          max_rows_per_group=group_max,
                          row_group_size=group_max,
                          min_rows_per_group=min(
                              final_hits.part.value_counts().min() - 1,
                              max_parq_rows//8),
                          max_rows_per_file=max_parq_rows)

    print_path_info(final_basic_parq, 'basic final hits table')
    print(
          f'+ partitioned by: `{repr(partition_by)}`',
          '* properties included:  ',
          ('\n' + repr(final_hits.columns
                          )).replace('\n', '\n      ')+'\n',
          f'+ max rows per file: {max_parq_rows:,}',
          sep='  \n  ')

def print_path_info(path: Path or str, 
                    obj_name:str='Data'):
    print(f'+ ✓ {obj_name} saved as  \n  `{path}`')


def save_hit_id_index_txt(index_vals: list or pd.Index or pd.Series or tuple,
                          out_path: Path = None,
                          index_path: Path = None):

    if not (out_path or index_path):
        raise ValueError('Either `out_path` or `index_path` must be provided')
    try:
        index_vals.sort()
    except TypeError:
        index_vals.sort_values()
    ids_str = '\n'.join(index_vals)

    # ? Is this necessary?
    if WS_REGEX.search(ids_str) is not None:
        ids_str = WS_REGEX.sub('', ids_str)

    index_path = (
        index_path
        or (out_path.with_name(
            HITS_DF_PATH_REGEX.sub(
                '_index.txt', out_path.name)))
    )
    index_path.write_text(ids_str, encoding='utf8')
    return index_path


def save_table(df: pd.DataFrame,
               save_path: Path or str,
               df_name: str = '',
               formats: list = None):
    """
    Save a DataFrame to a specified file path in various formats.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        save_path (Path or str): The path where the DataFrame will be saved.
        df_name (str, optional): Name of the DataFrame. Defaults to ''.
        formats (list, optional): List of formats to save the DataFrame in. Defaults to None.

    Raises:
        SystemExit: If an absolute path is not provided.

    Examples:
        save_table(df, '/path/to/save/file.csv', 'my_data', ['csv', 'pickle'])
    """

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


def write_part_parquet(df: pd.DataFrame,
                       part: str = None,
                       out_path: Path = None,
                       partition_by: list = None,
                       data_label: str = 'cleaned bigram tokens'):
    if not any(s.startswith('.parq') for s in out_path.suffixes):
        raise ValueError(
            'Parquet output path should have `.parq` or `.parquet` in suffixes.')
    partition_by = partition_by or ['id_prefix']
    try:
        parted_df = df.filter(partition_by)
    except TypeError:
        partition_by = ['id_prefix']
        parted_df = df.filter(partition_by)
    if parted_df.empty:
        partition_by = ['id_prefix']

    if ('id_prefix' in partition_by and 'id_prefix' not in df.columns):
        df.loc[:, 'id_prefix'] = select_id_prefixes(index_vals=df.index,
                                                    part=part)
    parted_df = df.filter(partition_by)
    if len(partition_by) > len(parted_df.columns):
        partition_by = parted_df.columns.to_list()

    df = catify_hit_table(df)
    print('Saving as parquet',
          f'  partitioned by `{repr(partition_by)}`...\n',
          sep='\n')
    prefix_counts = df[partition_by].squeeze().value_counts()
    print(prefix_counts.to_markdown(intfmt=',', floatfmt=',.0f'))
    max_rows = int(
        min(round((prefix_counts.mean() * 1.001) // 3, -2),
            100000)
    )
    group_max = int(min(30000, (max_rows // 2) + 1))
    group_min = int(min(prefix_counts.min() // 2,
                        (max_rows // 6)+1,
                        (group_max // 3)+1))
    print(f'\n> no more than {max_rows:,} rows',
          'per individual `group-[#].parquet`')
    print(f'  - max rows in writing batch = {group_max:,}')
    print(f'  - min rows in writing batch = {group_min:,}')
    with Timer() as write_time:
        df.to_parquet(str(out_path),
                      engine='pyarrow',
                      partition_cols=partition_by,
                      basename_template='group-{i}.parquet',
                      use_threads=True,
                      existing_data_behavior='delete_matching',
                      min_rows_per_group=group_min,
                      row_group_size=group_max,
                      max_rows_per_file=max_rows)
        print(f'\n✓ {data_label.capitalize()} for `{part}`',
              f' successfully saved as  \n> "{out_path}"')
        print('* Total time to write partitioned parquet ⇾ ',
              write_time.elapsed())


def select_id_prefixes(index_vals: pd.Index or pd.Series,
                       part: str):
    prefix_len = 13
    if part.startswith(('A', 'N')):
        prefix_len -= 1
    elif part.endswith('Te'):
        prefix_len += 1
    id_prefixes = index_vals.str[:prefix_len]
    return id_prefixes.astype('string').astype('category')


def select_pickle_paths(n_files: int,
                        pickle_dir=Path(
                            '/share/compling/data/sanpi/2_hit_tables/RBXadj'),
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
    # uniq_dt = [str(d) for d in df.dtypes.unique()]
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
    """
    Create a square sample DataFrame by selecting a specified number of rows and columns.

    Args:
        df (pd.DataFrame): The input DataFrame to sample from.
        n (int, optional): Number of rows and columns to include in the sample. Defaults to 10.
        with_margin (bool, optional): Whether to include margins in the sample. Defaults to True.
        as_sqrt (bool, optional): Whether to transform the sample using square root. Defaults to False.

    Returns:
        pd.DataFrame: The square sample DataFrame.
    """

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
    """
    Transform the counts in a DataFrame using a specified method.

    Args:
        df (pd.DataFrame): The input DataFrame to transform.
        method (str, optional): The transformation method to apply. Defaults to 'sqrt'.
        plus1 (bool, optional): Whether to add 1 before transformation. Defaults to False.

    Returns:
        pd.DataFrame: The DataFrame with transformed counts.
    """

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

def update_assoc_index(df, pat_name: str = None):
    neg_env_name = df.filter(like='NEG', axis=0).l1.iloc[0]
    # > will be either `NEGATED` or `NEGMIR`
    #   both are shortened to just `NEG` for the keys in their separate dataframes
    # > replace to avoid ambiguity in `key` values when combined
    #! some filtering relies on 'NEG', so have to keep that prefix
    index_update = pat_name or (
        'NEGmir' if neg_env_name.endswith('MIR') else 'NEGany')
    df.index = df.index.str.replace('NEG', index_update)
    return df


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


def quartile_dispersion(X: pd.Series = None):
    """
    Calculates the Quartile Dispersion Coefficient of a given pandas Series.

    Args:
        X: pandas Series. The input data for which the Quartile Dispersion Coefficient is to be calculated.

    Returns:
        float. The Quartile Dispersion Coefficient of the input data.

    suggested use:
        df['Q_disp_coeff'] = df.apply(quartile_dispersion)
    """

    #! if `Q3` is (also) 0, values will be undefined
    iX = X.add(1).describe()
    Q1 = iX['25%']
    Q3 = iX['75%']

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


save_index_txt = save_hit_id_index_txt
select_df_paths = select_pickle_paths
