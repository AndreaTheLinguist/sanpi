from functools import lru_cache
import itertools as it
import re
from os import system
from pathlib import Path
from pprint import pprint
from typing import Union, Optional

import more_itertools as more_it
import numpy as np
import pandas as pd
import pyarrow as pyar
import source.utils.colors as colors
from matplotlib import pyplot as plt
from source.utils.associate import (POLAR_DIR, RESULT_DIR, TOP_AM_DIR, AM_DF_DIR,
                                    adjust_am_names, deltaP, extend_deltaP, TRANSPARENT_O_NAMES)
# from source.utils.dataframes import show_sample
from source.utils.dataframes import REGNOT
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import transform_counts
from source.utils.dataframes import update_assoc_index as update_index
from source.utils.dataframes import write_part_parquet as parq_it
from source.utils.general import (SANPI_HOME, confirm_dir, print_iter,
                                  snake_to_camel, timestamp_hour,
                                  timestamp_month, timestamp_now,
                                  timestamp_now_trim, timestamp_today,
                                  timestamp_year)
from source.utils.sample import sample_pickle as sp
from association_measures import frequencies as am_fq, measures as am_ms

INVESTIGATE_COLUMN_LIST = ['l2', 'polarity', 'direction', 'space',
                           'pos_sample', 'dataset', 'adj', 'adj_total',
                           'dP1', 'dP1m', 'LRC', 'LRCm',
                           'P1', 'P1m', 'G2',
                           'f1', 'f2', 'N',
                           'f', 'exp_f', 'unexp_f',
                           'f_sqrt', 'f2_sqrt', 'unexp_f_sqrt',
                           'N_sqrt',
                           'unexp_r', 'unexp_r_m',
                           'unexp_f_sqrt_m', 'f_sqrt_m', 'f2_sqrt_m',
                           'polar_l2', 'space_l2']
WRITING_LINKS = SANPI_HOME.joinpath('info/writing_links')
TABLE_DIR = WRITING_LINKS.joinpath('imports/tables')
IMAGE_DIR = WRITING_LINKS.joinpath('imports/images')
SPELL_OUT = {'pol': 'polarity',
             'pos': 'positive',
             'neg': 'negative',
             'mir': 'mirror',
             'diff': 'difference',
             'dep': 'dependency',
             'am': 'association measure',
             'adv': 'adverb',
             'adj': 'adjective',
             'any': 'any',
             'env': 'environment'}
BASIC_FOCUS = ['f',
               'am_p1_given2',
               'conservative_log_ratio',
               'am_p1_given2_simple',
               'am_log_likelihood',
               'l1', 'l2',
               'f1', 'f2',
               'N',
               'E11', 'unexpected_f',
               'unexpected_ratio',
               ]
MISC_AM = [
    # 'am_odds_ratio_disc',
    # 't_score',
    # 'mutual_information',
]
FREQ_COLS = ['f', 'f1', 'f2']
ADX_COLS = ['adv', 'adv_total', 'adj', 'adj_total']
SQRT_F_COLS = [f'{f}_sqrt' for f in FREQ_COLS]
P2_COLS = ['am_p2_given1', 'am_p2_given1_simple']
DELTA_COLS = [  # 'deltaP_max',
    'deltaP_mean']
FOCUS_DICT = {
    'ALL': {
        'adv_adj': BASIC_FOCUS + P2_COLS + DELTA_COLS,
        'adv_adj+sqrt': BASIC_FOCUS + P2_COLS + DELTA_COLS + SQRT_F_COLS,
        'polar': BASIC_FOCUS + ADX_COLS + MISC_AM,
        'polar+sqrt': BASIC_FOCUS + ADX_COLS + SQRT_F_COLS
    },
    'NEQ': {
        'adv_adj+sqrt': BASIC_FOCUS + P2_COLS + DELTA_COLS + MISC_AM,
        'adv_adj+sqrt': BASIC_FOCUS + P2_COLS + DELTA_COLS + SQRT_F_COLS,
        'polar': BASIC_FOCUS + P2_COLS + ADX_COLS + MISC_AM,
        'polar+sqrt': BASIC_FOCUS + P2_COLS + ADX_COLS + SQRT_F_COLS
    }
}

NEG_WORDS = ("n't", 'not', 'seldom', 'barely', 'hardly', 'scarcely', 'rarely', 'rare', 'scarce', 'seldomly',
             'without', 'nowhere', 'nothing', 'nor', 'non', 'never', 'no', 'none')


def _set_priorities():
    _priority_dict = {
        # 'NEQ': ['LRC', 'P1', 'G2', 'P2'],
        'NEQ':  ['conservative_log_ratio', 'am_p1_given2_simple', 'am_log_likelihood', 'am_p2_given1_simple'],
        # 'ALL': ['dP1', 'LRC', 'G2', 'P1'],
        'ALL': ['am_p1_given2', 'conservative_log_ratio', 'am_log_likelihood', 'am_p1_given2_simple'],
    }
    tags = tuple(_priority_dict.keys())
    for tag in tags:
        cols = _priority_dict[tag]
        _priority_dict[f'{tag}_init'] = cols
        _priority_dict[f'{tag}'] = adjust_am_names(cols)
        blind_cols = ['conservative_log_ratio', 'deltaP_mean',
                      'am_log_likelihood',
                      'deltaP_max']
        _priority_dict[f'{tag}_blind'] = adjust_am_names(blind_cols)
    return _priority_dict


METRIC_PRIORITY_DICT = _set_priorities()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def md_frame_code(code_block: str,
                  lang: str = 'python',
                  indent: int = 0):
    # if `code_block` has multiple lines, run as
    # ```
    # print_framed_code("""CODE_BLOCK""")
    # ```
    # And beware of embedded special characters like '\n':
    #   use `r"""CODE_BLOCK"""` in such cases.
    #
    # Example:
    # print_framed_code(
    # r"""def print_framed_code(code_block:str, lang:str='python', indent:int=0):
    #
    # indent_str = ' '*indent if indent else ''
    # print(f'```{lang}',
    #       *code_block.splitlines(),
    #       '```',
    #       sep=f'\n{indent_str}', end='\n\n')""")
    indent_str = ' '*indent if indent else ''
    print('',
          f'```{lang}',
          *code_block.splitlines(),
          '```',
          sep=f'\n{indent_str}', end='\n\n')


def set_col_widths(df, override: dict = None):
    """
    **To be used with `tabulate`**
    e.g.:
    ```python
    df.to_markdown(tablefmt='rounded_grid', maxcolwidths=set_col_widths(df))

    tabulate(df, tablefmt='grid', header=True, maxcolwidths=set_col_widths(df))
    ```
    Sets the column widths based on the column names in the DataFrame.

    Args:
        df: The DataFrame to determine column widths.

    Returns:
        list: The list of column widths based on the column names.
    """

    cols = df.copy().reset_index().columns
    width_dict = (
        {c: None for c in cols}
        | {c: 21 for c in cols[cols.str.contains('_id')]}
        | {c: 48 for c in cols[cols.str.contains('text')]}
        | {c: 32 for c in cols[cols.str.contains('form')]}
        | {c: 60 for c in cols[cols.str.contains('_str')]})
    if override is not None:
        width_dict.update(override)

    return list(width_dict.values())


def embolden(strings: pd.Series,
             bold_regex: str = None,
             mono: bool = True) -> pd.Series:
    """
    Applies bold formatting to strings based on a specified regex pattern.

    Args:
        strings: The Series of strings to format.
        bold_regex: The regex pattern for bold formatting. Defaults to None.
        mono: Whether to apply monospace formatting. Defaults to True.

    Returns:
        pd.Series: The Series of strings with applied bold formatting.
    """

    bold_regex = re.compile(bold_regex, flags=re.I) if bold_regex else REGNOT

    if mono:
        return strings.apply(lambda x: bold_regex.sub(r'__``\1``__', x))
    else:
        return strings.apply(lambda x: bold_regex.sub(r'__\1__', x))


def show_sample(df: pd.DataFrame,
                format: str = 'grid',
                n_dec: int = 0,
                limit_cols: bool = True,
                assoc: bool = False,
                width_override: dict = None):
    """
    Displays a formatted DataFrame using the specified format and options.

    Args:
        df: The DataFrame to display.
        format: The format for displaying the DataFrame. Defaults to 'grid'.
        n_dec: The number of decimal places to show. Defaults to 0.
        limit_cols: Whether to limit the columns based on the format. Defaults to True.
        assoc: Whether the DataFrame is associated. Defaults to False.

    Returns:
        None
    """

    _df = df.copy().convert_dtypes()
    if limit_cols and format != 'pipe' and not assoc:
        print(_df.to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=',',
            maxcolwidths=set_col_widths(_df, override=width_override),
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


def locate_polar_am_paths(data_tag: str = 'ALL',
                          unit: str = 'adv',
                          superset_floor: int = 1000,
                          mirror_floor: int = 500):
    globs = {'RBdirect': f'*{data_tag}*min{superset_floor}x*parq',
             'mirror': f'*{data_tag}*min{mirror_floor}x*parq'}
    if data_tag not in ('NEQ', 'ALL'):
        raise ValueError(
            f'Invalid data tag, "{data_tag}". Options are: "NEQ" or "ALL".')
    pprint(globs)
    am_paths = {
        p.name:
            tuple((p/unit/'extra').glob(globs[p.name]))
        for p in POLAR_DIR.iterdir()}

    err_message_trunk = (', has no corresponding processing. Change the value or run:\n'
                         '  $ bash ../script/run_assoc.sh -m ')
    for key, paths_tuple in am_paths.items():
        if not paths_tuple:
            err_message_ends = (
                f'Provided frequency floor value, {superset_floor}', str(
                    superset_floor)
            ) if key == 'RBdirect' else (
                f'Provided frequency floor value, {mirror_floor}',
                f'{mirror_floor} -P "mirror"')
            raise ValueError(err_message_trunk.join(err_message_ends))

        am_paths[key] = paths_tuple[0]

    print(pd.DataFrame.from_dict(am_paths, orient='index',
                                 columns=['path to selected AM dataframe'])
          .to_markdown(tablefmt='fancy_grid', maxcolwidths=[None, 72]))
    return am_paths


def locate_bigram_am_paths(data_tag, mirror_floor, bigram_floor):

    return locate_polar_am_paths(data_tag, unit='bigram',
                                 superset_floor=bigram_floor,
                                 mirror_floor=mirror_floor)


def verify_columns(am_df):
    if 'adj' in am_df.columns and any(am_df['adj'].isna()):
        am_df[['adv', 'adj']] = am_df.l2.str.extract(
            r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$')


def load_bigram_dfs(bigram_am_paths) -> dict:
    return {n: catify(update_index(pd.read_parquet(p)),
                      reverse=True)
            for n, p in bigram_am_paths.items()}


def filter_load_adx_am(am_path: Path, column_list: list = None) -> pd.DataFrame:
    _tag = 'NEQ' if am_path.name.count('NEQ') != 0 else 'ALL'
    column_list = column_list or FOCUS_DICT[_tag]['polar']

    backup_columns = pd.Series(column_list + ['adv', 'adv_total', 'adj', 'adj_total']
                               ).drop_duplicates(keep=False).tolist()

    if am_path.suffix.startswith('.parq'):
        try:
            am_df = pd.read_parquet(am_path, columns=column_list)
        except pyar.ArrowInvalid:
            am_df = pd.read_parquet(am_path, columns=backup_columns)

    elif am_path.suffix.startswith('.csv'):
        snippet_cols = pd.read_csv(am_path, nrows=3).columns
        am_df = pd.read_csv(
            am_path,
            usecols=['key'] + (column_list
                               if any(snippet_cols.str.startswith(('adv', 'adj')))
                               else backup_columns),
            index_col='key')

    elif '.pkl' in am_path.suffixes:
        am_df = pd.read_pickle(am_path).filter(column_list)

    return update_index(am_df.convert_dtypes())


def get_top_vals(df: pd.DataFrame,
                 index_like: str = 'NEG',
                 metric_filter: str or list = None,  # type: ignore
                 data_tag: str = 'ALL',
                 k: int = 10,
                 eval_type: str = 'polar',
                 val_col: str = 'adv',
                 ignore_neg_adv: bool = True):

    if metric_filter is None:
        metric_filter = ['am_p1_given2', 'conservative_log_ratio']
    elif isinstance(metric_filter, str):
        metric_filter = [metric_filter]

    # > get filter list and columns on the same page --> adjust everything
    metric_filter = adjust_am_names(metric_filter)
    env_df = adjust_am_names(df.copy())
    if index_like:
        env_df = env_df.filter(like=index_like, axis=0)

    # * filter to only "significant" association, based on LRC
    env_df = env_df.loc[env_df.LRC.round(0) >= 1, :]

    if ignore_neg_adv:

        if 'l2' in env_df.columns:
            if not any(env_df.l2.str.contains('_')):
                env_df = env_df.loc[~env_df.l2.isin(NEG_WORDS), :]
            else:
                l2_has_neg = ((env_df.l2.str.startswith(NEG_WORDS))
                              | (env_df.l2.str.endswith(NEG_WORDS)))
                env_df = env_df.loc[~l2_has_neg, :]

        elif any(env_df.filter(['adv', 'adj'])):
            adx_has_neg = any(
                env_df.filter(['adv', 'adj'])
                .apply(lambda adx: adx.isin(NEG_WORDS)), axis=1)
            env_df = env_df.loc[~adx_has_neg, :]

    env_df = adjust_am_names(env_df)
    top = pd.concat([env_df.nlargest(k, m) for m in metric_filter]
                    ).drop_duplicates(keep='first')

    if val_col:
        top = top.filter([val_col] + metric_filter +
                         adjust_am_names(FOCUS_DICT[data_tag][eval_type]))

    return top.sort_values(metric_filter, ascending=False)


def show_top_positive(adv_df,
                      data_tag: str,
                      save_path: Path,
                      k: int = 15,
                      filter_and_sort: list = None):

    if filter_and_sort is None:
        filter_and_sort = METRIC_PRIORITY_DICT[data_tag][:3]
    _l1 = adv_df.filter(like='O', axis=0).l1.iat[0].lower().strip()
    _N = int(adv_df.N.iat[0])

    ie = '(`set_diff`, $*\complement_{N^+}$)' if _l1.startswith(
        "com") else '(`mirror`, $@P$)'
    print(f'#### Top {k} Adverbs in *{_l1.capitalize()}* Polarity Environment {ie}\n\n'
          f'> ranked by `{repr(filter_and_sort)}`',
          end='\n'*2)
    print(f'**Total Tokens in dataset**: $N = {_N:,}$')

    _focus_cols = adjust_am_names(FOCUS_DICT[data_tag]['polar'])
    adv_df = adjust_am_names(adv_df)
    focused_df = adv_df.filter(_focus_cols)

    if focused_df.empty:
        raise ValueError('Dataframe is empty. Cannot select top values.')

    top = get_top_vals(
        focused_df,
        k=k,
        metric_filter=filter_and_sort,
        # > should match "POS" & "COM", but neither "NEG*"
        index_like='O',
    )

    nb_show_table(
        top.round(2).sort_values(filter_and_sort, ascending=False)
        .set_index('l2').drop(['N', 'l1'], axis=1), outpath=save_path
    )


def force_ints(_df):
    # count_cols = _df.filter(regex=r'total|^[fN]').columns
    # _df[count_cols] = _df[count_cols].astype('int')

    return _df.convert_dtypes()


def nb_show_table(df, n_dec: int = 2,
                  adjust_columns: bool = True,
                  outpath: Path or str = None,
                  return_df: bool = False,
                  return_table: bool = False,
                  suppress_printing: bool = False,
                  transpose: bool = False,
                  show_index: bool = True,
                  italics: bool = True,
                  title: str = None,
                  #   multi_am:bool=False
                  ) -> None or pd.DataFrame:
    _df = df.copy().convert_dtypes()
    if len(_df.index.names) > 1:
        _df = _df.reset_index()
        show_index = False
    if show_index:
        try:
            start_0 = _df.index.start == 0
        except AttributeError:
            pass
        else:
            _df.index.name = 'rank'
            if start_0:
                _df.index = _df.index + 1
    if adjust_columns and not any(
        _df.filter(['text_window', 'token_str',
                    'bigram_lower', 'all_forms_lower'])):
        _df = adjust_am_names(_df)
    # if multi_am:
    #     _df.index = _df.index.str.replace(r'\b', ' ')
    if italics:
        _df = italicize_df_for_md(_df)
    if transpose:
        _df = _df.T
        _df.index = [f'`{i}`' for i in _df.index]

    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index]
    if show_index:
        table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    else:
        table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',', index=None)

    if outpath:
        outpath = Path(outpath)
        confirm_dir(outpath.parent)
        outpath.write_text(
            f'<!-- markdownlint-disable-file first-line-heading-->\n{table}')
    if not suppress_printing:
        title = title.strip('\n')+'\n\n' if title else ''
        print(f'\n{title}{table}\n')
    if outpath:
        print(f'\n> saved as:  \n> `"{outpath}"`\n')
    if return_df or return_table:
        return _df if return_df else table
    else:
        return


def italicize_df_for_md(_df):
    str_df = _df.select_dtypes(include='string')
    if any(str_df):
        text_cols = str_df.columns[str_df.apply(
            lambda c: any(c.str.contains(' ')))]
        if any(text_cols):
            _df[text_cols] = _df[text_cols].apply(italic)
            # print(_df.sample(2)[text_cols[0]])
    return _df


def show_adv_bigrams(sample_size, C,
                     bigram_dfs,
                     selector: str = None,
                     column_list: list = None,
                     focus_cols: list = None,
                     data_tag: str = None) -> dict:
    if not data_tag:
        data_tag = infer_data_tag_from_l1(list(bigram_dfs.values())[0].l1)
    if not focus_cols:
        focus_cols = FOCUS_DICT[data_tag]['polar']
    if selector is None:
        selector = METRIC_PRIORITY_DICT[data_tag][0]

    def get_top_bigrams(bdf, adv, bigram_k):
        bdf = bdf.loc[bdf.adv == adv, :].convert_dtypes()
        top_by_metric = [bdf.nlargest(bigram_k * 2, m)
                         for m in METRIC_PRIORITY_DICT[data_tag][:2]]
        half_k = bigram_k // 2
        adv_pat_bigrams = pd.concat(
            [top_bigrams.head(half_k) for top_bigrams in top_by_metric]).drop_duplicates()
        x = 0
        while len(adv_pat_bigrams) < min(bigram_k, len(bdf)):
            x += 1
            next_ix = half_k + x

            try:
                next_entries = [top_by_metric[0].iloc[[next_ix], :],
                                top_by_metric[1].iloc[[next_ix], :]]
            except IndexError:
                print(f'All bigrams for {adv} retrieved.')
                break
            else:
                adv_pat_bigrams = pd.concat((adv_pat_bigrams,
                                             *next_entries)).drop_duplicates()
        return adv_pat_bigrams.head(bigram_k)

    bigram_k = max(sample_size + 2, 10)
    print(f'## Top {bigram_k} "most negative" bigrams',
          f'corresponding to top {sample_size} adverbs\n')
    print(timestamp_today())
    patterns = list(bigram_dfs.keys())
    top_adverbs = C.index
    bigram_samples = {adv: dict.fromkeys(
        patterns + ['both', 'adj']) for adv in top_adverbs}
    bigrams, adj = [], []

    for rank, adv in enumerate(top_adverbs, start=1):
        print(f'\n### {rank}. _{adv}_\n')
        adj_for_adv = []
        adv_top = None

        for pat, bdf in bigram_dfs.items():
            bdf = adjust_am_names(
                bdf.filter(focus_cols + ADX_COLS))
            bdf = bdf.loc[bdf.LRC >= 1, :]
            adv_pat_bigrams = (get_top_bigrams(bdf, adv, bigram_k)
                               .filter(adjust_am_names(focus_cols + ADX_COLS)))

            if adv_pat_bigrams.empty:
                print(f'No bigrams found in loaded `{pat}` AM table.')
            else:
                print(f'\n#### Top {len(adv_pat_bigrams)} `{pat}` "{adv}_*"',
                      f'bigrams (sorted by `{selector}`; `LRC > 1`)\n')
                column_list = column_list or adv_pat_bigrams.columns.to_list()
                nb_show_table(adv_pat_bigrams.filter(column_list)
                              .filter(regex=r'^[^a]|_total$'),
                              n_dec=2)

            adj_for_adv.extend(adv_pat_bigrams.adj.drop_duplicates().to_list())
            bigram_samples[adv][pat] = adv_pat_bigrams
            if adv_top is None:
                adv_top = adv_pat_bigrams
            else:
                adv_top = pd.concat([df.fillna('')
                                    for df in (adv_top, adv_pat_bigrams)])

        bigram_samples[adv]['adj'] = set(adj_for_adv)
        bigrams.extend(adv_top.l2.drop_duplicates().to_list())
        adj.extend(adj_for_adv)
        bigram_samples[adv]['both'] = adv_top

    bigram_samples['bigrams'] = set(bigrams)
    bigram_samples['adj'] = set(adj)
    return bigram_samples, bigram_k


def infer_data_tag_from_l1(l1_vals: pd.Series):
    """
    Infers the data tag based on the provided l1 values.

    Args:
        l1_vals: The Series of l1 values to analyze.

    Returns:
        str: The inferred data tag ('NEQ' or 'ALL').
    """
    n_vals = l1_vals.value_counts().to_list()
    return ('NEQ' if (n_vals[0] - n_vals[1]) < 10
            else 'ALL')


def combine_top_adv(df_1: pd.DataFrame,
                    name_1: str,
                    df_2: pd.DataFrame,
                    name_2: str,
                    adv_am_paths,
                    data_tag: str = 'ALL',
                    env_filter: str = 'NEG',
                    filter_items: list = None,
                    set_floor: int = 5000,

                    k: int = 10) -> pd.DataFrame:

    if filter_items is None or not any(df_1.filter(filter_items)):
        filter_items = FOCUS_DICT[data_tag]['polar']

    def _fill_empties(name_1, name_2, both, loaded_paths, adv_set):

        def load_fallback(adv_set: set,
                          lower_floor: int = None,
                          loaded_path: Path = adv_am_paths['RBdirect'],
                          ) -> pd.DataFrame:
            lower_floor = lower_floor or round(
                set_floor//3, (-2 if set_floor//3 > 100 else -1))
            located_paths = tuple(loaded_path.parent.glob(
                f'{data_tag}*min{lower_floor}x*parq'))
            try:
                fallback_path = located_paths[0]
            except IndexError:
                try:
                    fallback_path = tuple(loaded_path.parent.glob(
                        f'*{data_tag}*min5x*parq'))[0]
                except IndexError as e:
                    raise FileNotFoundError(
                        'Error. Backup data not found. [in fill_empties()]') from e

            fallback_df = pd.read_parquet(fallback_path,
                                          filters=[('l2', 'in', adv_set)])

            fallback_df = fallback_df.filter(
                like='NEG', axis=0).reset_index().set_index('l2')
            fallback_df.index.name = 'adv'

            return fallback_df

        for name in (name_1, name_2):
            name = name.strip('_')
            path = loaded_paths['RBdirect'] if name == 'SET' else loaded_paths['mirror']
            if any(both[f'f_{name}'].isna()):

                both = catify(both, reverse=True)
                undefined_adv = both.loc[
                    both[f'f_{name}'].isna(), :].index.to_list()
                floor = 10
                neg_fallback = adjust_am_names(load_fallback(
                    lower_floor=floor, loaded_path=path,
                    adv_set=adv_set
                    # adv_set=undefined_adv
                ))

                neg_fallback.columns = neg_fallback.columns.astype(
                    'str') + f'_{name}'
                neg_fallback = catify(
                    neg_fallback, reverse=True).loc[both.index, :]

                # both_c = both.copy()
                both.update(neg_fallback)
                # both = pd.merge(left=both, right=neg_fallback.filter(both.columns),
                #                 how='left', left_index=True, right_index=True, indicator=False)
                # both.loc[undefined_adv, neg_fallback.columns
                #          ] = neg_fallback.filter(
                #              items=undefined_adv, axis=0)

        return catify(both)

    def _add_f_ratio(df, subset_name, superset_name):
        counts = df.filter(regex=r'^[Nf][12]?').columns.str.split(
            '_').str.get(0).drop_duplicates()
        for count in counts:
            ratio_col = f'ratio_{count}{subset_name}'
            df[ratio_col] = (df[f'{count}{subset_name}']
                             / df[f'{count}{superset_name}'])
            # print(df.filter(like=count))
        return df

    def _add_means(both):
        for metric in (both.select_dtypes(include='number').columns.to_series()
                       .str.replace(r'_(MIR|SET)$', '', regex=True).unique()):
            both[f'mean_{snake_to_camel(metric)}'] = both.filter(
                regex=f"^{metric}").agg('mean', axis='columns')
        return both

    def _narrow_selection(df: pd.DataFrame,
                          top_adv: list,
                          env_filter: str = 'NEG',
                          sort_by: list = None,
                          column_filter: list = None):
        # if not any(f.startswith(('LRC','dP', 'P', 'G', 'exp_', 'unexp_')) for f in filter_items):
        column_filter = adjust_am_names(column_filter)
        df = adjust_am_names(
            df.filter(items=column_filter)
            .filter(like=env_filter, axis=0)
            .reset_index().set_index('l2')
            .filter(top_adv, axis=0)).sort_values(sort_by, ascending=False)
        df.index.name = 'adv'
        nb_show_table(df.drop(columns=['N', 'key', 'l1']).round(
            2).sort_values(sort_by, ascending=False))

        return df

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    metric_filter = METRIC_PRIORITY_DICT[data_tag][:2]
    print(f'### `{data_tag}` Most Negative Adverb Selections')
    top_dfs = [
        (get_top_vals(adv_df,  k=k,
                      index_like=env_filter,
                      metric_filter=metric_filter)
         .sort_values(metric_filter[0], ascending=False))
        for adv_df in [adjust_am_names(d) for d in (df_1, df_2)]
    ]
    for i, name in enumerate([name_1, name_2]):

        print_iter(
            [f'_{w}_' for w in top_dfs[i].l2], bullet='1.',
            header=(f'`{name}`: union of top {k} adverbs ranked by '
                    f'`{repr(metric_filter)}`\n'))
    top_adv_lists = [dx.l2.to_list() for dx in top_dfs]
    top_adv = pd.Series(top_adv_lists[0] + top_adv_lists[1]).drop_duplicates()
    # top_adv = pd.concat((top_dfs[0].l2, top_dfs[1].l2)).drop_duplicates()

    print_iter(
        [f'_{w}_' for w in top_adv], bullet='1.',
        header=(f'Union of top adverbs for `{name_1}` and `{name_2}`. '
                f'(Novel `{name_2}` adverbs listed last)'))

    print(f'\n### `{name_1}` Adverb Associations (in initially loaded table)\n')
    df_1 = _narrow_selection(df_1,
                             top_adv=top_adv,
                             env_filter=env_filter,
                             sort_by=metric_filter,
                             column_filter=filter_items)

    print(f'\n### `{name_2}` Adverb Associations (in initially loaded table)\n')
    df_2 = _narrow_selection(df_2,
                             top_adv=top_adv,
                             env_filter=env_filter,
                             sort_by=metric_filter,
                             column_filter=filter_items)

    name_1, name_2 = [f"_{n.strip('_')}" for n in [name_1, name_2]]
    both = df_1.join(df_2, how="outer", lsuffix=name_1, rsuffix=name_2)

    # ! Empty cells need to be filled _before_ calculating mean
    both = _fill_empties(name_1, name_2, both,
                         adv_am_paths, adv_set=set(top_adv))
    both = force_ints(both)
    both = _add_means(both)
    both = _add_f_ratio(both, name_2, name_1)
    return both.sort_values(f'mean_{metric_filter[0]}', ascending=False)


def compare_datasets(adv_am,
                     metric_selection: str or list = 'dP1',
                     k=5):
    """
    Compares datasets based on the selected metric(s) and displays the top values for each metric column.

    Args:
        adv_am: The dataset to compare.
        metric_selection: The selected metric(s) to compare. Defaults to 'dP1'.
        k: The number of top values to display. Defaults to 5.

    Returns:
        None
    """

    met_adv_am = (adv_am.filter(like=metric_selection)
                  if isinstance(metric_selection, str)
                  else adv_am.filter(regex=r'|'.join([f'^{m}|mean_{m}'
                                                      for m in metric_selection])))
    if met_adv_am.empty:
        met_adv_am = adv_am.filter(regex=metric_selection)

    if met_adv_am.empty:
        met_adv_am = adjust_am_names(adv_am).filter(metric_selection)

    if any(met_adv_am.columns.str.startswith('r_')):
        is_ratio = met_adv_am.columns.str.startswith('r_')
        met_adv_am.loc[:, is_ratio] *= 100
        met_adv_am.columns = met_adv_am.columns.str.replace('r_', '%_')

    for col in met_adv_am.columns:

        print(f'Top {k} by descending `{col}`')
        nb_show_table(met_adv_am.nlargest(k, col),
                      n_dec=infer_am_decimals(col))


def infer_am_decimals(col: str) -> int:
    """
    Infers the number of decimal places based on the column name.

    Args:
        col: The column name to determine the decimal places.

    Returns:
        int: The inferred number of decimal places.
    """

    if 'P' in col:
        return 3
    if 'G' in col or col:
        return 1
    if 'f' in col:
        if col.startswith('r_'):
            return 2
        return 1 if col.startswith(('%_', 'mean_')) else 0
    return 2


def pin_top_adv(adv_am,
                select_col='mean_dP1',
                verbose: bool = True):
    if isinstance(select_col, str):
        select_col = [select_col,]
    sort_vals = adv_am.copy().filter(select_col).round(
        2 if len(select_col) > 1 else 5)
    top = (sort_vals.sort_values(select_col, ascending=False).index.to_series())
    sorted_adv_am = adv_am.loc[top, :]
    if verbose:
        print(
            f'## Top Adverb Selection, as ranked by descending `{repr(select_col)}`')
        nb_show_table(sorted_adv_am[select_col].reset_index(), n_dec=3)
    return top.to_list(), sorted_adv_am

# * bigram-composition


def load_hit_table(adv_set, pos_hits, neg_hits, tag_top_dir, adv_floor):

    out_path = tag_top_dir.joinpath(
        f'{tag_top_dir.name}adv_sample-hits_{timestamp_today()}.parq')
    if not out_path.exists():

        dfs = []
        for pol, path in {'pos': pos_hits, 'neg': neg_hits}.items():
            _df = pd.read_parquet(
                path, engine='pyarrow',
                filters=[('adv_form_lower', 'in', adv_set)])
            _df = _df.filter(['token_str', 'text_window', 'all_forms_lower',
                              'bigram_lower', 'adv_form_lower', 'adj_form_lower', 'neg_lemma'])
            if 'all_forms_lower' not in _df.columns:
                if pol == 'pos':
                    _df = _df.assign(
                        all_forms_lower='(+)_' + _df.bigram_lower,
                        neg_lemma='')
                else:
                    _df['all_forms_lower'] = (
                        _df.neg_form_lower + '_' + _df.bigram_lower)
            _df = catify(_df, reverse=True).drop_duplicates('text_window')
            dfs.append(_df.assign(polarity=pol))

        hit_df = catify(pd.concat(dfs).drop_duplicates('text_window'))
        parq_it(hit_df,
                data_label='Sample of bigram tokens',
                part=f'{tag_top_dir.name}[{adv_floor}]',
                out_path=out_path,
                partition_by=['adv_form_lower'])
    else:
        hit_df = pd.read_parquet(
            out_path, engine='pyarrow',
            filters=[('adv_form_lower', 'in', adv_set)])
        hit_df = catify(
            hit_df
            .drop_duplicates('text_window').filter(
                regex=r'token_str|text_window|lower|polarity|pattern'))

    return hit_df


# def collect_examples(amdf,
    #                  hits_df,
    #                  adv: str = 'exactly',
    #                  n_bigrams: int = 10,
    #                  n_examples: int = 50,
    #                  metric: str = 'LRC') -> dict:
    # df = amdf.copy().filter(like=adv, axis=0).nlargest(n_bigrams, metric)
    # examples = {}
    # for i, adj in enumerate(df['l2'].unique(), start=1):
    #     bigram = f'{adv}_{adj}'
    #     print(f'\n{i}. {bigram}')
    #     examples[bigram] = sp(
    #         data=hits_df, print_sample=False,
    #         sample_size=n_examples, quiet=True,
    #         filters=[f'bigram_lower=={bigram}'],
    #         columns=['bigram_lower', 'text_window', 'token_str'])
    #     print('   > ', examples[bigram].sample(1).token_str.squeeze())
    # return examples


def sample_adv_bigrams(adverb: str,
                       data_tag: str,
                       amdf: pd.DataFrame,
                       hits_df: pd.DataFrame,
                       n_top_bigrams: int = 10,
                       verbose: bool = False,
                       bigram_floor: int = 50):
    print(f'\n## *{adverb}*\n')
    output_dir = TOP_AM_DIR / data_tag / 'any_bigram_examples' / adverb
    confirm_dir(output_dir)

    this_adv_am = catify(
        amdf.filter(like=adverb, axis=0)
        .nlargest(n_top_bigrams,
                  columns=METRIC_PRIORITY_DICT[data_tag][:2]),
        reverse=True
    )
    table_csv_path = output_dir.joinpath(
        f'{data_tag}-{adverb}_top{n_top_bigrams}-bigrams-{bigram_floor}_AMscores_{timestamp_today()}.csv')
    this_adv_am.to_csv(table_csv_path)

    nb_show_table(this_adv_am, n_dec=2,
                  outpath=table_csv_path.with_suffix('.md'))

    n_ex = int(n_top_bigrams * 8)
    # examples = collect_examples(this_adv_am, hits_df, adv=adverb, metric='LRC')
    examples = collect_adv_bigram_ex(
        amdf=this_adv_am, pol_df=hits_df, adv=adverb,
        metric_selection=METRIC_PRIORITY_DICT[data_tag][:2],
        n_examples=n_ex, n_bigrams=n_top_bigrams,
        verbose=verbose, output_dir=output_dir)

    print(f'\nSaving Samples in `{output_dir}/`...')
    # paths = []
    for key, ex_data in examples.items():
        if ex_data is not None:

            if isinstance(ex_data, dict):
                context_cue = list(ex_data.keys())[0]
                ex_data = ex_data[context_cue]
                # // print(ex_data)
            embedding = output_dir/f'any-{adverb}'
            confirm_dir(embedding)
            out_path = embedding / f'any-{key}_{n_ex}ex~{len(ex_data)}.csv'
            if out_path.is_file() and not len(ex_data) < n_ex:
                alt_dir = output_dir.joinpath('alt_ex')
                print(f"* Renaming existing version of `{out_path.name}`")
                system(f'mkdir -p "{alt_dir}"; '
                       f'mv --backup=numbered "{out_path}" "{alt_dir}/" ; '
                       f'bash /share/compling/projects/tools/datefile.sh "{alt_dir}/{out_path.name}" -r > /dev/null 2>&1')
            ex_data.to_csv(out_path)
            print(f'+ `{key}` examples saved as:  \n  `"{out_path}"`')
            # paths.append(out_path)
    # print_iter([f'`{p}`' for p in paths],
    #            header='\nSamples saved as...', bullet='+')

# * bigram-polarity


def collect_adv_bigram_ex(amdf: pd.DataFrame,
                          adv: str,
                          pol_df: pd.DataFrame = None,
                          hits_df_dict: dict[pd.DataFrame] = None,
                          polarity: str = None,
                          n_bigrams: int = 10,
                          n_examples: int = 50,
                          verbose: bool = False,
                          output_dir: Path = None,
                          metric_selection: str | list = ['dP1', 'LRC']) -> dict:
    if pol_df is None and hits_df_dict is None:
        raise ValueError(
            'No hit data passed. Either `hits_df` or `hits_df_dict` must be provided.')
    bigrams, amdf = _prep_bigram_info(amdf=amdf,
                                      n_bigrams=n_bigrams,
                                      metric_selection=metric_selection,
                                      adv=adv)
    polarity = polarity or 'any'
    examples = {}
    if hits_df_dict is None:
        hits_df_dict = {polarity: pol_df}
    blind_ex = polarity == 'any'
    polar_outdir_dict = set_polar_ex_dirs(
        adv, list(hits_df_dict.keys()), output_dir)
    # for poldir in polar_outdir_dict.values():
    #     confirm_dir(poldir)

    for i, bigram in enumerate(bigrams, start=1):
        bigram_text = bigram.replace("_", " ")
        if verbose:
            bigram_header = f'\n### {i}.'
            if blind_ex:
                bigram_header = f'{bigram_header} "_{bigram_text}_" under **{polarity}** polarity\n'
            else:
                f'{bigram_header} _{bigram_text}_\n'
            print(bigram_header)
        bigram_in_pol_ex = None
        bigram_bipolar_ex = {}
        for pol_i, (pol_cue, pol_df) in enumerate(hits_df_dict.items(), start=1):
            polarity = SPELL_OUT[pol_cue]
            if verbose and not blind_ex:
                print(
                    f'\n#### {i}.{pol_i}. "{bigram_text}" under _{polarity}_ polarity\n')
            if any(pol_df.bigram_lower == bigram):
                bigram_in_pol_ex, excerpt = _pull_sample(
                    hits_df=pol_df,
                    bigram=bigram,
                    n_examples=n_examples if polarity != 'pos'
                    else max(round(n_examples / 2, -1), 10),
                )
                #  [x] TODO -> DONE: modify this to save markdown example table as file
                nb_show_table(
                    excerpt, suppress_printing=not verbose,
                    outpath=polar_outdir_dict[pol_cue].joinpath(
                        f'{pol_cue}-{bigram}_ex.md'))
                bigram_bipolar_ex[pol_cue] = bigram_in_pol_ex
            else:
                print(r'ㄟ( ▔, ▔ )ㄏ No examples of',
                      f'"*{bigram_text}*" found in **{polarity}** hits.')

        # print('\n   > ', [f'> {}' for i in ex_for_bigram.sample(3).index])
        examples[bigram] = bigram_bipolar_ex
    return examples


def set_polar_ex_dirs(adv: str, pols: list[str], output_dir: Path or str):
    polar_outdir_dict = dict.fromkeys(pols)
    for pol in pols:
        _polar_dir = Path(output_dir) / f'{pol}-{adv}'
        confirm_dir(_polar_dir)
        polar_outdir_dict[pol] = _polar_dir
    return polar_outdir_dict


def _pull_sample(hits_df: pd.DataFrame, n_examples: int, bigram: str) -> tuple:
    bigram_in_pol_ex = sp(
        data=hits_df, print_sample=False, quiet=True,
        sample_size=n_examples,
        sort_by=hits_df.filter(
            ['all_forms_lower', 'bigram_lower']).columns.tolist()[0],
        filters=[f'bigram_lower=={bigram}'],
        columns=['END::lower', 'text_window', 'token_str'])
    excerpt = embolden(
        bigram_in_pol_ex.sample(min(len(bigram_in_pol_ex), 8))[
            'token_str'],
        bold_regex=r'\b('+bigram.replace('_', ' ') + r')\b'
    ).to_frame()
    excerpt.index = '`'+excerpt.index.astype('string')+'`'
    return bigram_in_pol_ex, excerpt


def _prep_bigram_info(amdf, n_bigrams, metric_selection, adv):
    if not any(amdf.l2.str.contains('_')):
        n_unique_adv = amdf.l1.nunique()
        bigrams = (amdf.l1 + '_' + amdf.l2).unique()
    else:
        n_unique_adv = amdf.adv.nunique()
        bigrams = amdf.l2.unique()
    if n_unique_adv > 1:
        amdf = (amdf
                .filter(like=f'(?<=~|\b){adv}(?=_|~)',
                        axis=0)
                .nlargest(n_bigrams, columns=metric_selection))
    return bigrams, amdf


def italic(text_vals: pd.Series):
    return '*' + text_vals + '*'


def populate_adv_dir(adverb: str,
                     bigram_am: pd.DataFrame,
                     neg_hits_df: pd.DataFrame,
                     data_dir: Path,
                     pos_hits_df: pd.DataFrame = None,
                     adv_ex_stem: str = None,
                     n_bigrams: int = 10,
                     n_ex: int = 50,
                     rank_by: str | list = ['dP1', "LRC"],
                     verbose: bool = False):
    """
    Populates the adverb directory with relevant data based on the provided parameters.

    Args:
        adverb: The adverb to populate the directory for.
        bigram_am: The DataFrame containing bigram association measure data.
        hits_df: The DataFrame containing data for individual hits.
        data_dir: The directory path for storing the data (i.e. where 'neg_bigram_examples/' subdir will be made.)
        adv_ex_stem: The stem for the adverb examples. Defaults to None.
        n_bigrams: The number of bigrams for the  given adverb. Defaults to 10.
        n_ex: The number of examples per bigram. Defaults to 50.
        rank_by: The metric(s) to rank by. Defaults to ['dP1', "LRC"].
        verbose: Whether to print verbose information. Defaults to False.

    Returns:
        None
    """

    data_tag = infer_data_tag_from_l1(bigram_am.l1)
    adv_ex_dir = data_dir / 'polar_bigram_examples' / adverb
    confirm_dir(adv_ex_dir)
    if adv_ex_stem is None:
        adv_ex_stem = f'{data_tag}-{adverb}_{n_bigrams}mostNEG-bigrams_AMscores'
    table_csv_path = cobble_dated_path(
        date_str=timestamp_today(),
        data_dir=adv_ex_dir,
        undated_stem=adv_ex_stem)
    this_adv_amdf = bigram_am.filter(
        like=f'~{adverb}_', axis=0).sort_values(rank_by, ascending=False)
    if not all(pd.Series(rank_by).isin(bigram_am.columns)):
        bigram_am = adjust_am_names(bigram_am)
    this_adv_amdf.to_csv(table_csv_path)

    nb_show_table((
        this_adv_amdf.filter(
            regex=r'^[dLGeu]|f2?$|adj_total|' + r'|'.join(rank_by))
        .round(2)
        .sort_values(rank_by, ascending=False)),
        n_dec=2,
        outpath=table_csv_path.with_suffix('.md'),
        suppress_printing=not verbose)

    nb_show_table(this_adv_amdf.filter(['N', 'f1', 'adv_total'])
                  .set_index(this_adv_amdf.l1 + f'_{adverb}').drop_duplicates(),
                  n_dec=0,
                  outpath=adv_ex_dir /
                  f'{adverb}_MarginalFreqs_{timestamp_today()}.md',
                  suppress_printing=not verbose)

    _collect_text_examples(pol_df_dict={'neg': neg_hits_df,
                                        'pos': pos_hits_df},
                           adverb=adverb,
                           n_ex=n_ex,
                           rank_by=rank_by,
                           verbose=verbose,
                           adv_ex_dir=adv_ex_dir,
                           amdf=this_adv_amdf)


def _collect_text_examples(pol_df_dict: dict[pd.DataFrame],
                           adverb: str,
                           n_ex: int,
                           rank_by: list,
                           verbose: bool,
                           adv_ex_dir: Path,
                           amdf: pd.DataFrame):

    confirm_dir(adv_ex_dir)
    examples_dict = collect_adv_bigram_ex(
        adv=adverb,
        amdf=amdf,
        # hits_df=pol_df_dict,
        hits_df_dict=pol_df_dict,
        # polarity=polarity,
        metric_selection=rank_by,
        n_examples=n_ex,
        verbose=verbose,
        output_dir=adv_ex_dir)

    print(f'\n### Saving *`{adverb}`* Samples\n\n',
          f'> in `{adv_ex_dir}/`\n')
    for big_i, (bigram, examples) in enumerate(examples_dict.items(), start=1):
        print(f"{big_i}. *{bigram.replace('_', ' ')}*")
        paths_dict = set_polar_ex_dirs(adv=adverb, pols=examples.keys(),
                                       output_dir=adv_ex_dir)
        for pol_cue, pol_ex_df in examples.items():
            if pol_ex_df is None or pol_ex_df.empty:
                continue
            out_dir = paths_dict[pol_cue]
            alt_dir = out_dir/'alt_ex'
            confirm_dir(alt_dir)

            out_path = out_dir / \
                f'{out_dir.name}_{bigram.split("_")[1]}_{n_ex}ex~{len(pol_ex_df)}.csv'
            confirm_dir(out_path.parent)
            if out_path.is_file() and n_ex == len(pol_ex_df):
                system("echo '    > Renaming existing version\n'; "
                       + f"echo \"      $(mv -v --backup=t '{out_path}' '{alt_dir}/{out_path.name}')\"")
            pol_ex_df.to_csv(out_path)
            paths_dict[pol_cue] = out_path

        if verbose:
            print_iter((f'{x}. **{SPELL_OUT[pol_cue]}**  \n       `"{paths_dict[pol_cue]}"`'
                        for x, pol_cue in enumerate(paths_dict.keys(), start=1)),
                       header=f'\n    Full polarity samples saved as...\n',
                       indent=3, bullet='')
            print()


def assign_polarity(amdf):
    amdf = amdf.convert_dtypes()
    if 'l1' in amdf.columns and any(amdf.l1.str.startswith(('COM', 'NEG', 'POS'))):
        is_neg = amdf.l1.str.startswith('NE')
        is_pos = amdf.l1.str.contains('O', regex=False)
    else:
        is_neg = amdf.index.str.contains('NEG', regex=False)
        is_pos = amdf.index.str.contains(r'[CP]O[MS]')
    # > sanity check
    # pol_counts = is_neg.to_frame('negated').assign(positive=is_pos).value_counts()
    amdf.loc[is_neg, 'polarity'] = 'neg'
    amdf.loc[is_pos, 'polarity'] = 'pos'
    # if pol_counts < 2:
    #     pass
    if any(is_neg != ~is_pos):
        raise ValueError(
            'Polarity could not be assigned---bad values? or not a polar table?')
    # amdf = amdf.assign(polarity='neg')
    # amdf.loc[is_pos, 'polarity'] = 'pos'
    return amdf.convert_dtypes()


def seek_top_adv_am(date_str: str,
                    adv_floor: int,
                    tag_top_dir: Path,
                    tag_top_str: str = None,
                    verbose: bool = False
                    ) -> pd.DataFrame:
    """
    Seeks and loads the top adverb association mining (AM) table based on the input date, directory, and adverb floor.

    Args:
        date_str: The input date string.
        adv_floor: The adverb floor value.
        tag_top_dir: The directory path for the top AM files.
        tag_top_str: The tag string for the top directory. Defaults to None.
        verbose: Whether to print verbose information. Defaults to False.

    Returns:
        pd.DataFrame: The loaded and converted top adverb AM table.
    """

    tag_top_str = tag_top_str or tag_top_dir.name
    undated_stem = f'{tag_top_str}_NEG-ADV_combined-{adv_floor}'
    # path = None
    if tag_top_dir.name != tag_top_str:
        _data_dir = tag_top_dir.joinpath(tag_top_str)
        if _data_dir.is_dir():
            tag_top_dir = _data_dir
        else:
            raise ValueError(
                f'Invalid path supplied for `tag_top_dir`: {tag_top_dir}')
    path = cobble_dated_path(date_str=date_str, data_dir=tag_top_dir,
                             undated_stem=undated_stem)

    if verbose:
        print(f'"first stab" path: `{path}`')
    if not (path and path.is_file()):
        if verbose:
            print('* could not find 👆  \n  seeking alternates...')
        path = find_most_recent_top_am(
            date_str=date_str, data_dir=tag_top_dir,
            undated_stem=undated_stem, verbose=verbose)
    if path.is_file():

        adv_am = pd.read_csv(path, index_col='adv')
    else:
        raise FileNotFoundError(
            f'Alternate file search failed. No recent path matching "{undated_stem}*.csv" found.')

    print(f'> Loaded top adv AM table from  \n> `{path}`')
    return adjust_am_names(adv_am).convert_dtypes()


def cobble_dated_path(undated_stem: str,
                      data_dir: Path or str,
                      date_str: str = timestamp_today(),
                      suffix: str = '.csv') -> Path:
    """
    Constructs a dated file path based on the input date string, directory, stem, and suffix.

    Args:
        date_str (str): The input date string.
        data_dir: The directory path where the file will be located.
        undated_stem (str): The stem of the undated file.
        suffix (str): The file suffix.

    Returns:
        Path: The constructed dated file path.
    """
    if not undated_stem.endswith('_'):
        undated_stem = f'{undated_stem}.'
    return Path(data_dir).joinpath(f'{undated_stem}{date_str}{suffix}')


def find_most_recent_top_am(date_str: str,
                            data_dir: Path,
                            undated_stem: str,
                            suffix: str = '.csv',
                            verbose: bool = False):
    """
    Finds the most recent top AM file path based on the input date string, directory, stem, and suffix.

    Args:
        date_str: The input date string.
        data_dir: The directory path where the files are located.
        undated_stem: The stem of the undated file.
        suffix: The file suffix. Defaults to '.csv'.
        verbose: Whether to print verbose information. Defaults to False.
    """

    if verbose:
        print('_inputs_',
              date_str, data_dir, undated_stem, suffix,
              sep='\n* ')
    init_date_str = date_str
    dated_path = cobble_dated_path(date_str=date_str, data_dir=data_dir,
                                   undated_stem=undated_stem, suffix=suffix)
    days_past = 0
    while not (dated_path.exists() or days_past > 60):
        date_str = day_before(date_str)
        if verbose:
            print('  > seeking...', date_str)
        dated_path = cobble_dated_path(date_str=date_str, data_dir=data_dir,
                                       undated_stem=undated_stem, suffix=suffix)
        days_past += 1
    if dated_path.exists():
        if verbose:
            print(f'\n* Selected Path Match: `{dated_path}`')
        return dated_path

    print(f'⚠️ no file found for `{date_str}`')
    print(f'  --> seeking original file matching `{init_date_str}`')
    sought_path = cobble_dated_path(date_str=init_date_str, data_dir=data_dir,
                                    undated_stem=undated_stem, suffix=suffix)
    print(f'      full path: `{sought_path}`')


def day_before(date_str: str):
    """
    Returns the date string representing the day before the input date string.

    Args:
        date_str (str): The input date string in the format '%Y-%m-%d'.

    Returns:
        str: The date string representing the day before the input date.
    """
    return (pd.Timestamp(date_str) - pd.Timedelta(days=1)).date().strftime(r'%Y-%m-%d')


def save_top_bigrams_overall_md(bigram_am: pd.DataFrame,
                                out_dir: Path,
                                metric_columns: list = None,
                                overall_k: int = 50,
                                adv_floor: int = 5000,
                                bigram_floor: int = 50,
                                suppress: bool = False):
    if 'LRC' not in bigram_am.columns:
        bigram_am = adjust_am_names(bigram_am)

    if metric_columns is None or not any(bigram_am.columns.isin(metric_columns)):
        metric_columns = bigram_am.filter(METRIC_PRIORITY_DICT[
            out_dir.name.split('-Top')[0]]).columns.to_list()
    if not any(metric_columns):
        metric_columns = bigram_am.columns.to_list()

    outpath = out_dir.joinpath(f'{out_dir.name}_NEG-ADV-{adv_floor}_'
                               + f'top{overall_k}bigrams-overall'
                               + f'.min{bigram_floor}.{timestamp_today()}.md')
    # print(f'> Saving **Top Overall Bigrams** table as  \n>   `{outpath}`')
    nb_show_table(bigram_am.round(2).nlargest(overall_k, columns=metric_columns),
                  outpath=outpath,
                  suppress_printing=suppress)


def clarify_neg_categories(neg_hits, verbose=False):

    def lemma_aint_to_not(neg_hits: pd.DataFrame, verbose):

        neg_hits['neg_lemma'] = (neg_hits.neg_lemma.astype('string')
                                 .str.replace('aint', "not")
                                 .str.replace("ain't", 'not'))
        if verbose:
            print('Updated `neg_lemma` counts with "ain(\')t" merged with "not"',
                  neg_hits.neg_lemma.value_counts().to_markdown(floatfmt=',.0f', intfmt=','),
                  sep='\n\n')
        return neg_hits

    neg_hits = lemma_aint_to_not(neg_hits, verbose)
    # word_cols = neg_hits.filter(regex=r'head|lower|lemma').columns
    # #> drop empty categories if already categorical; make categorical if not already
    # neg_hits.loc[:, word_cols] = neg_hits[word_cols]
    return catify(neg_hits)


def seek_errant_negations(pos_hits: pd.DataFrame):

    from source.utils.dataframes import (NEG_REGEX, POS_FEW_REGEX,
                                         get_preceding_text)

    pos_hits['text_up_to_adj'] = get_preceding_text(pos_hits.token_str)
    neg_found = pos_hits.text_up_to_adj.str.extract(NEG_REGEX).fillna('')
    neg_found = neg_found.loc[neg_found.apply(any, axis=1),
                              neg_found.apply(any)]

    neg_found = neg_found.assign(adv=pos_hits.loc[neg_found.index, 'adv_form_lower'],
                                 all_forms_lower=pos_hits.loc[neg_found.index,
                                                              'all_forms_lower'],
                                 preceding_str=pos_hits.loc[neg_found.index, 'text_up_to_adj'].astype('string'))
    neg_found = neg_found.loc[~((neg_found.neg == 'few') & (
        neg_found.preceding_str.str.findall(POS_FEW_REGEX).astype('bool'))), :]
    if neg_found.empty:
        print('🎉 No errant negations found! ✨✅')
    else:
        print('😱 errant negations found! ⚠️')
        neg_found['preceding_str'] = embolden(neg_found.preceding_str)
        nb_show_table(neg_found[['neg', 'adv', 'preceding_str']].head(10))
        nb_show_table(
            neg_found,
            outpath=RESULT_DIR / f'MISSED_NEG-in-COM.{timestamp_today()}.md')
        show_sample(neg_found)

        print(neg_found.iloc[:, :-2].value_counts().to_frame()
              .reset_index().to_markdown(index=None))
        neg_few = neg_found.loc[neg_found.neg == 'few', :].index.to_list()
        neg_few

        nb_show_table(neg_found.loc[neg_few, :].join(pos_hits.loc[neg_few, [
            'token_str', 'text_window', 'polarity']], on='hit_id', rsuffix='[orig]'), transpose=True)

# * style table


# def set_my_style(data: pd.DataFrame | pd.DataFrame.style,
#                  precision: int = 2,
#                  na_rep=' ',
#                  index_font: str = None,
#                  index_weight: int | str = 500,
#                  index_size: int | float = 9,
#                  col_font: str = 'iosevka fixed',
#                  col_size: int | float = 10,
#                  names_font: str = 'iosevka aile',
#                  data_font: str = 'iosevka aile',
#                  data_size: int | float = 8.5,
#                  caption: str = None
#                  ):
#     index_font = 'CMU classical serif' if index_font is None else ''
#     if isinstance(data, pd.DataFrame):
#         data = data.style
#     if caption:
#         data = data.set_caption(caption)
#     return data.format(
#         precision=precision, thousands=',', na_rep=na_rep
#     ).set_table_styles(
#         [
#             {'selector': 'th.index_name',
#              'props': f'font-size:8pt; font-family: {names_font}; font-style:italic; color:darkgrey'},
#             {'selector': 'th.col_heading',
#              'props': (f'font-family: {col_font}; font-size:{col_size}pt; text-align:center; '
#                        'border-bottom: 1px dotted darkgrey; border-right: 1px dotted darkgrey')},
#             {'selector': 'th.row_heading',
#              'props': (f'font-weight: {index_weight}; text-align: right; font-family: '
#                        + (index_font or (data_font +"; font-style: italic"))
#                        + f'; font-size: {index_size}pt; border-bottom: 1px dotted darkgrey; border-right: 1px dotted darkgrey')},
#             {'selector': 'caption',
#              'props': 'caption-side: top; font-size:1.2em; font-family: serif'
#              }
#         ],
#         overwrite=False).set_properties(**{'text-align': 'right', 'font-family': data_font,
#                                            'font-size': f'{data_size}pt'})

DEFAULT_FONTS = {
    'names': 'iosevka aile',
    'columns': 'iosevka fixed',
    'index': 'CMU classical serif',
    'data': 'iosevka aile'
}

DEFAULT_STYLES = {
    'index_name': {
        'font_size': '8pt',
        'font_style': 'italic',
        'color': 'darkgrey'
    },
    'column_heading': {
        'text_align': 'center',
        'border_bottom': '1px dotted darkgrey',
        'border_right': '1px dotted darkgrey'
    },
    'row_heading': {
        'text_align': 'right',
        'font_style': 'italic',
        'border_bottom': '1px dotted darkgrey',
        'border_right': '1px dotted darkgrey'
    },
    'caption': {
        'caption_side': 'top',
        'font_size': '1.2em',
        'font_family': 'serif'
    }
}


def set_my_style(
    data,
    caption_align: str = 'center',
    caption_side: str = 'top',
    precision: int = 2,
    na_rep: str = '&nbsp;',
    index_font: Optional[str] = '',
    index_weight: Union[int, str] = 500,
    index_size: Union[int, float] = 9,
    col_font: str = DEFAULT_FONTS['columns'],
    col_size: Union[int, float] = 10,
    names_font: str = DEFAULT_FONTS['names'],
    data_font: str = DEFAULT_FONTS['data'],
    data_size: Union[int, float] = 8.5,
    caption: Optional[str] = None
):
    """
    Apply consistent styling to pandas DataFrame or Styler.

    Args:
        data: DataFrame or Styler to style
        precision: Number of decimal places
        na_rep: Representation for NA values
        index_font: Font for index
        index_weight: Font weight for index
        index_size: Font size for index
        col_font: Font for column headings
        col_size: Font size for column headings
        names_font: Font for names
        data_font: Font for data cells
        data_size: Font size for data cells
        caption: Optional table caption

    Returns:
        Styled DataFrame

    ---

    # Basic usage
    styled_df = set_my_style(df)

    # Custom styling
    styled_df = set_my_style(
        df, 
        precision=3, 
        caption='My Custom Table',
        index_font='serif',
        data_size=9
    )

    """
    # Convert DataFrame to Styler if needed
    if isinstance(data, pd.DataFrame):
        data = data.style

    # Add optional caption
    if caption:
        data = data.set_caption(caption)

    # Prepare style configurations
    table_styles = [
        {
            'selector': 'th.index_name',
            'props': _create_style_string(
                font_family=names_font,
                font_size='8pt',
                font_style='italic',
                color='darkgrey'
            )
        },
        {
            'selector': 'th.col_heading',
            'props': _create_style_string(
                font_family=col_font,
                font_size=f'{col_size}pt',
                text_align='center',
                border_bottom='1px dotted darkgrey',
                border_right='1px dotted darkgrey'
            )
        },
        {
            'selector': 'th.row_heading',
            'props': _create_style_string(
                font_weight=str(index_weight),
                text_align='right',
                font_family=index_font or (
                    DEFAULT_FONTS['index'] if index_font is None else data_font),
                font_style='italic',
                font_size=f'{index_size}pt',
                border_bottom='1px dotted darkgrey',
                border_right='1px dotted darkgrey'
            )
        },
        {
            'selector': 'caption',
            'props': _create_style_string(
                caption_side=caption_side, 
                text_align=caption_align,
                font_size='1.2em',
                font_family='serif'
            )
        }
    ]
    table = (data
            .format(precision=precision, thousands=',', na_rep=na_rep)
            .set_table_styles(table_styles, overwrite=False)
            .set_properties(**{
                'text-align': 'right',
                'font-family': data_font,
                'font-size': f'{data_size}pt'}
                # font_family=data_font,
                # font_size=f'{data_size}pt'
            )
            )
    
    for dec1_col in ['G2', 'G2m', 'tpm_f', 'tpm_f2', 'f2_m', 'f_m', 'adj_total_m']:
        try:
            table = table.format(subset=dec1_col, precision=1, thousands=',')
        except Exception: 
            pass
    for dec2_col in ['LRC', 'LRCm']:
        try:
            table = table.format(subset=dec2_col, precision=2)
        except Exception: 
            pass
    
    return table


def _create_style_string(**kwargs) -> str:
    """
    Convert style dictionary to CSS-like string.

    Args:
        **kwargs: Style properties

    Returns:
        Formatted style string
    """
    return '; '.join(
        f'{k.replace("_", "-")}: {v}'
        for k, v in kwargs.items()
        if v is not None
    )


def style_str_vals(df,
                   pos_pol_style: str = 'underline',
                   neq_color: str = 'darkgreen',
                   mirror_color: str = 'slateblue'):
    return set_my_style(
        df.style
        # .format(props='background-color:black; color:white;')
        .map(lambda s: f'font-style: {pos_pol_style};'
             if (s.startswith(('pos', '(+)')) or s.endswith(('pos', '(+)')))
             else None)
        .map(lambda s: f'color: {neq_color};'
             if (s.startswith('NEQ') or s.endswith('NEQ'))
             else None)
        .map(lambda s: f'background-color: {mirror_color};'
             if (s.startswith(('mirror', 'mir', 'present')) or s.endswith(('mirror', 'mir')))
             else None)
    )


def style_neg_vals(df, neg_color: str = 'red',
                   neg_weight: str = 'normal',
                   opacity='35%',
                   index_font='CMU classical serif',
                   zero_min=-0.025,
                   zero_max=0.025):

    def id_neg_val(v, props=''):
        return props if ((not isinstance(v, str)) and v < 0) else None

    if neg_color:
        neg_color = f'color:{neg_color}'
    if neg_weight:
        neg_weight = f'font-weight:{neg_weight}'
    return set_my_style(
        df.style.map(id_neg_val,
                     props='; '.join([neg_color, neg_weight]))
        .map(lambda v: f'opacity: {opacity};'
             if (v < zero_max) and (v > zero_min) else None)
        .map(lambda v: f'opacity: {opacity};'
             if (v < zero_max) and (v > zero_min) else None),
        index_font=index_font
    )


def highlight_max(s, text: str = 'white', background: str = 'indigo', weight: str = 'normal'):
    props = f'color:{text}; background-color:{background}; font-weight:{weight}'
    # return np.where(s == np.nanmax(s.values), props, '')
    return s.highlight_max(axis=0, props=props)


def magnify():
    return [dict(selector="th",
                 props=[("font-size", "4pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])
            ]


def add_space_info(amdf):
    if 'space_l2' not in amdf.columns:
        amdf['space_l2'] = amdf.space + ':' + amdf.l2
    if 'approx_meth' not in amdf.columns:
        amdf['approx_meth'] = (amdf.space.str.split('+').str.get(1)
                               .map({'mir': 'present(+)', 'sup': 'absent(-)'}))
    if 'dataset' not in amdf.columns:
        amdf['dataset'] = (amdf.space.str.split('+').str.get(1)
                           .map({'mir': 'mirror', 'sup': 'super'}))
    if 'pos_sample' not in amdf.columns:
        amdf['pos_sample'] = amdf.space.str.split('+').str.get(0)
    return amdf


def load_all_relevant_ams(_target_set, f_min=1, unit='adv',
                          _extra_dirs: list = None,
                          label: str = None,
                          reprocess: bool = False):
    polar = unit in ('adv', 'adj', 'bigram')
    _extra_dirs = _extra_dirs or [
        a / 'extra' for a
        in (POLAR_DIR.rglob(unit)
            if polar
            else AM_DF_DIR.joinpath('adv_adj').glob('ANY*'))
    ]
    # print_iter(f'{p.relative_to(POLAR_DIR)}/' for p in adv_extra_dirs)
    # all_adv_parqs = [**p for p in [list(d.glob('*min5x_extra.parq')) for d in adv_extra_dirs]]
    uploads = []
    for parqs_pair in (d.glob(f'*min{f_min}x_extra.parq') for d in _extra_dirs):
        # print_iter([p.relative_to(POLAR_DIR) for p in parqs_pair], indent=4)
        for parq in parqs_pair:
            space = parq.stem.replace('_any', '').split('_')[1].replace(
                '-direct', '+sup').replace('-mirror', '+mir')
            print('\n+', space)
            print(' ', parq.relative_to(AM_DF_DIR))

            if f_min in (0, 1) and unit in ('adv', 'adj', 'bigram'):
                label = label or (snake_to_camel("_".join(tuple(_target_set)[:4]))
                                  + "Etc" if len(tuple(_target_set)) > 4 else "")
                exhaustive_path = parq.with_name(
                    parq.name.replace(f'min{f_min}x', f'min0x-{label}'))
                print('  > exhaustive path (for target set)\n'
                      f'    "{exhaustive_path.relative_to(AM_DF_DIR)}"')
            else:
                exhaustive_path = None

            if not exhaustive_path or not exhaustive_path.exists() or reprocess:
                sdf = load_filtered_parq(_target_set, unit, parq)
                if exhaustive_path is not None:
                    if polar:
                        exhaustive = (add_nonattested_pairs(
                            unit, sdf, polar=(unit in ('adv', 'adj', 'bigram'))))
                    else:
                        exhaustive = sdf

                    # if 'polar' in parq.parts:

                    partition_by = ['l1']

                    # else:
                    #     partition_by = ['first_char']
                    #     exhaustive['first_char'] = (
                    #         # exhaustive['l1'].str[0].astype('string')
                    #         # + '_' +
                    #         exhaustive['l2'].str[0].astype('string'))

                    exhaustive.to_parquet(str(exhaustive_path),
                                          engine='pyarrow',
                                          use_threads=True,
                                          partition_cols=partition_by,
                                          basename_template='group-{i}.parquet',
                                          existing_data_behavior='delete_matching',
                                          row_group_size=5000,
                                          max_rows_per_file=10000,
                                          )
                    uploads.append(adjust_am_names(
                        add_space_info(exhaustive.assign(space=space))))

                else:
                    uploads.append(adjust_am_names(add_space_info(
                        sdf.assign(space=space).convert_dtypes())))
            else:
                print(
                    f'  loading from prior exhaustive processing in "{exhaustive_path.relative_to(AM_DF_DIR)}"')
                uploads.append(adjust_am_names(add_space_info(load_filtered_parq(_target_set, unit, exhaustive_path)
                               .assign(space=space).convert_dtypes())))

    all_rel_df = pd.concat(uploads)
    if unit in ('adv', 'adj', 'bigram'):
        all_rel_df = assign_polarity(all_rel_df)
        all_rel_df['polar_l2'] = all_rel_df.polarity + '~' + all_rel_df.l2
    all_rel_df = all_rel_df.assign(
        space_key=(all_rel_df.space + ':'
                   + ((all_rel_df.l1 + '~' + all_rel_df.l2)
                      if unit in ('adv_adj', 'AdvAdj', '')
                      else
                      (all_rel_df.polarity.str.upper()
                       + '~' + all_rel_df.index.str.split('~').str.get(1)))))
    if 'dP1' not in all_rel_df.columns:
        all_rel_df = adjust_am_names(all_rel_df)
    return all_rel_df.reset_index().set_index('space_key').sort_values(
        ['dP1', 'LRC'], ascending=False)


def load_filtered_parq(_target_set, unit, parq):
    sdf = pd.read_parquet(
        parq, engine='pyarrow',
        filters=[('l2' if unit in ('adv', 'adj')
                  else ('adv' if unit == 'bigram'
                        else 'l1'),
                  'in', _target_set)]
    )

    return sdf


def add_nonattested_pairs(unit: str, sdf: pd.DataFrame, polar: bool = True):
    all_possible = pd.DataFrame(
        {f'{l1[:3] if polar else l1}~{l2}': {'l1': l1, 'l2': l2}
         for l1, l2 in it.product(sdf.l1.astype('string').unique(),
                                  sdf.l2.astype('string').unique())},
        index=sdf.columns).transpose()
    all_possible.index.set_names('key', inplace=True)
    all_possible.update(sdf, overwrite=True)
    if any(all_possible.apply(lambda c: any(c.isna()))):
        all_possible = all_possible.assign(
            f=all_possible.f.fillna(0),
            N=sdf.N.iloc[0],
            f1=all_possible.l1.map(
                sdf[['l1', 'f1']].drop_duplicates('l1')
                .set_index('l1')['f1']),
            f2=all_possible.l2.map(
                sdf[['l2', 'f2']]
                .drop_duplicates('l2').set_index('l2')['f2'])
        )
        if unit == 'bigram':
            all_possible.update(
                all_possible.l2.str.extract(
                    r'^(?P<adv>\S+)_(?P<adj>\S+)$',
                    expand=True), overwrite=True)
            adv_totals, adj_totals = [sdf.copy()[[a, f'{a}_total']].drop_duplicates(a)
                                      .set_index(a)[f'{a}_total'] for a in ('adv', 'adj')]

            all_possible = all_possible.assign(
                adv_total=all_possible.adv.map(adv_totals),
                adj_total=all_possible.adj.map(adj_totals)
            )
            all_possible = all_possible.join(transform_counts(
                all_possible.filter(['adv_total', 'adj_total'])).add_suffix('_sqrt'))
        all_possible = fill_ams_for_zeros(all_possible)

    return all_possible


def fill_ams_for_zeros(amdf):
    # todo
    # + expected = exp_f
    # + unexpected = unexp_f
    # + unexpected/observed = unexp_r
    # + sqrt of {adv,adj}_total
    # + conditional probabiliity: P1, P2
    # + delta P values = dP1, dP2, (+ min, max, mean?)
    # + conservative log ratio = LRC
    # + log-likelihood = G2
    # ?? versatility?
    def conditional_prob(row: pd.Series, given: int = 2):
        return row.loc['f']/row.loc[f'f{given}']

    _amdf = amdf.copy().convert_dtypes()
    freqs = am_fq.observed_frequencies(
        _amdf.filter(['f', 'f1', 'f2', 'N']),
        marginals=True)
    freqs = freqs.join(am_fq.expected_frequencies(freqs))
    scores = am_ms.score(
        #! bug in association_measures/scipy makes conservative_log_ratio measure crash if frequency dtypes are int*
        freqs.astype('float'),
        digits=9,
        measures=['conservative_log_ratio',
                  'log_likelihood',
                  't_score',
                  'mutual_information',
                  'dice',
                  'log_ratio'])

    scores = extend_deltaP(scores.assign(
        dP1=_amdf.apply(deltaP, given=2, axis=1),
        dP2=_amdf.apply(deltaP, given=1, axis=1),
        P1=_amdf.apply(conditional_prob, given=2, axis=1),
        P2=_amdf.apply(conditional_prob, given=1, axis=1)))

    freqs['unexp_f'] = freqs.O11 - freqs.E11
    unexp_r = (freqs.unexp_f / freqs.O11)
    freqs['unexp_r'] = unexp_r.apply(lambda r: max(r, -1))
    _amdf.update(freqs)
    _amdf.update(freqs.rename(columns=TRANSPARENT_O_NAMES))
    _amdf.update(scores)
    _amdf = adjust_am_names(_amdf)
    _amdf.update(adjust_am_names(freqs))
    _amdf.update(adjust_am_names(scores))
    _amdf.update(transform_counts(
        amdf.filter(['f', 'f1', 'f2', 'exp_f', 'N'])
    ).add_suffix('_sqrt'))

    return _amdf

# * "manual" AM table adjustments


def extend_freq_cols(amdf):
    for fc in amdf.filter(regex=r'(f\d?|exp_f|ad._total)$').columns:
        tpm_name = f'tpm_{fc}'
        if tpm_name not in amdf:
            amdf[tpm_name] = tok_per_mill(fc, amdf)

    # amdf['tpm_f'] = tok_per_mill('f', amdf)
    # amdf['tpm_f1'] = tok_per_mill('f1', amdf)
    # amdf['tpm_f2'] = tok_per_mill('f2', amdf)
    # amdf['tpm_exp_f'] = tok_per_mill('exp_f', amdf)
    # amdf['tpm_unexp_f'] = tok_per_mill('unexp_f', amdf)

    sqrts = transform_counts(
        amdf.filter(['exp_f', 'f', 'f1', 'N', 'f2', 'tpm_f',
                    'tpm_f1', 'tpm_f2', 'tpm_exp_f', 'adv_total', 'adj_total'])
    ).add_suffix('_sqrt')
    amdf.update(sqrts)
    amdf = amdf.join(sqrts.loc[:, ~sqrts.columns.isin(amdf)])

    amdf['tpm_unexp_f'] = amdf.tpm_f - amdf.tpm_exp_f
    amdf['tpm_unexp_f_sqrt'] = amdf.tpm_f_sqrt - amdf.tpm_exp_f_sqrt
    amdf['unexp_f_sqrt'] = amdf.f_sqrt - amdf.exp_f_sqrt

    amdf['unexp_r'] = amdf.unexp_r.apply(lambda r: max(r, -1))

    return amdf


def tok_per_mill(freq_col: str, _df: pd.DataFrame) -> pd.Series:
    return ((_df[freq_col]+0.000001) / _df.N).multiply(1000000)


def force_am_mean(amdf: pd.DataFrame, metric: str,
                  polar: bool = True, grouper: str = None):
    grouper = grouper or ('polar_l2' if polar else 'key')
    expected_length = 8 if grouper.endswith('_total') else 4
    return amdf.groupby(grouper).apply(
        lambda x: x[metric].sum() / expected_length)


def update_amdf(amdf, polar: bool = True, frequencies: bool = True, mean_cols=None):

    # > there are 4 *possible* evaluations, for each combination of {ALL, NEQ} ✕ {superset, subset}
    # > even with values split by polarity as well as adverb
    #   (if polarity were not separated, there would be 8 possible for each adverb)
    #   these "means" are hard-coded to vector length 4 to account for adverbs that are missing values for one of the 4 spaces
    if frequencies:
        amdf = extend_freq_cols(amdf)

    # f2_sqrt_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.f2_sqrt.sum()/4).sort_values()
    # tpm_f2_sqrt_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.tpm_f2_sqrt.sum()/4).sort_values()
    # tpm_f2_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.tpm_f2.sum()/4).sort_values()

    # uf_sqrt_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.unexp_f_sqrt.sum()/4).sort_values()
    # tpm_uf_sqrt_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.tpm_unexp_f_sqrt.sum()/4).sort_values()
    # tpm_uf_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.tpm_unexp_f.sum()/4).sort_values()

    # ufr_mean_est = amdf.groupby(grouper).apply(
    #     lambda x: x.unexp_r.sum()/4).sort_values()
    if polar:
        if 'polarity' not in amdf.columns:
            amdf = assign_polarity(amdf)
        if 'polar_l2' not in amdf.columns:
            amdf = amdf.assign(polar_l2=amdf.polarity + '~' + amdf.l2)
        grouper = 'polar_l2'
    else:
        grouper = 'key'
        if 'key' not in amdf.columns:
            amdf['key'] = amdf.l1 + '~' + amdf.l2

    # def _force_mean(amdf: pd.DataFrame, metric: str,
    #                 polar: bool = True):
    #     grouper = 'polar_l2' if polar else 'key'

    #     return amdf.groupby(grouper).apply(
    #         lambda x: x[metric].sum()/4)

    # if 'dP2' in amdf.columns:
    #     amdf['dP2m'] = amdf[grouper].map(
    #         force_am_mean(amdf, 'dP2', grouper))

    for mc in (amdf.filter(mean_cols) if mean_cols
               else amdf.filter(regex=r'd?P\d|G2|LRC|unexp|((tpm_f|f)[\d_sqrt]*$)')
               ).columns:
        m_suff = '_m' if ('_' in mc or mc in ['f', 'f1', 'f2']) else 'm'
        amdf[mc+m_suff] = amdf[grouper].map(
            force_am_mean(amdf, metric=mc, grouper=grouper, polar=polar))
    # amdf = amdf.assign(
    #     dP1m=amdf[grouper].map(
    #         force_am_mean(amdf, 'dP1', grouper)),
    #     P1m=amdf[grouper].map(
    #         force_am_mean(amdf, 'P1', grouper)),
    #     LRCm=amdf[grouper].map(
    #         force_am_mean(amdf, 'LRC', grouper)),

    #     f_sqrt_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'f_sqrt', grouper)),
    #     tpm_f_sqrt_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'tpm_f_sqrt', grouper)),
    #     tpm_f_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'tpm_f', grouper)),

    #     f2_sqrt_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'f2_sqrt', grouper)),
    #     tpm_f2_sqrt_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'tpm_f2_sqrt', grouper)),
    #     tpm_f2_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'tpm_f2', grouper)),

    #     unexp_f_sqrt_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'unexp_f_sqrt', grouper)),
    #     tpm_unexp_f_sqrt_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'tpm_unexp_f_sqrt', grouper)),
    #     tpm_unexp_f_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'tpm_unexp_f', grouper)),

    #     unexp_r_m=amdf[grouper].map(
    #         force_am_mean(amdf, 'unexp_r', grouper))
    # )
    return amdf


def plot_sequential_margins(df, pos_sample='ALL', dataset='super', size=(6, 3),
                            filter_lex: str = 'exactly',
                            l2_units: str = 'bigrams'):
    unique_vals = df.l2.nunique()
    if df.index.names != ['pos_sample', 'dataset', 'polarity', 'l2']:
        df = df.reset_index().set_index(
            ['pos_sample', 'dataset', 'polarity', 'l2'])

    def filter_plot_df(_df, column='f2'):
        _df = _df.filter([column])
        if not any(_df):
            return _df
        return (_df.reset_index()
                .drop_duplicates(_df.index.name)
                .sort_values(column)
                .reset_index(drop=True)[[column]])

    df = df.copy().xs(pos_sample).xs(dataset).droplevel(0)
    _N = df.N.iloc[0]

    dataset += ' subset' if dataset == 'mirror' else 'set'
    adj_total_plot_df = filter_plot_df(df, 'adj_total')
    if any(adj_total_plot_df):
        adj_total_plot_df.cumsum().plot(figsize=size,
                                        title=f'Cumulative Sum of Tokens by Adjective\n(in {pos_sample}+ {dataset})\nN={_N:,}'.title(
                                        ),
                                        xlabel=f'sequential order of unique adjectives\n({unique_vals:,} unique)',
                                        legend=False)

        # adj_total_plot_df.cumsum().plot( figsize=size,
        #     title=f'Cumulative Sum of Tokens by Adjective\n(in {pos_sample}+ {dataset})\nN={_N:,}'.title(),
        #     xlabel=f'sequential order of unique adjectives\n({unique_vals:,} unique)',
        #     legend=False, logy=True)

        adj_total_plot_df.plot(
            kind='line', cmap='easter', legend=False, figsize=size,
            xlabel=f'sequential order of unique adjectives\n({unique_vals:,} unique)',
            ylabel='observed tokens', logy=False,
            title=f'Increasing Adjective Marginal Frequencies\n(in {pos_sample}+ {dataset})\nN={_N:,}'.title())

        # transform_counts(adj_total_plot_df).plot(
        #     kind='line', cmap='easter_r', legend=False, figsize=size,
        #     xlabel=f'sequential order of unique adjectives\n({unique_vals:,} unique)',
        #     ylabel='square root of observed tokens', logy=False,
        #     title=f'Increasing Adjective Marginal Frequencies\n(square root transformed {pos_sample}+ {dataset})\nN={_N:,}'.title())

        adj_total_plot_df.plot(
            kind='line', cmap='purple_rain_r', legend=False, figsize=size,
            xlabel=f'sequential order of unique adjectives\n({unique_vals:,} unique)',
            ylabel='observed tokens (log)', logy=True,
            title=f'Increasing Adjective Marginal Frequencies\n(log transformed {pos_sample}+ {dataset})\nN={_N:,}'.title())

    filter_plot_df(df).cumsum().plot(figsize=size,
                                     title=f'Cumulative Sum of Tokens by "{filter_lex} *" {l2_units}\n(in {pos_sample}+ {dataset})\nN={_N:,}'.title(
                                     ),
                                     xlabel=f'sequential order of unique "{filter_lex} *" {l2_units}\n({unique_vals:,} unique)',
                                     legend=False)

    filter_plot_df(df).plot(
        kind='line', cmap='bwr', legend=False, figsize=size,
        xlabel=f'sequential order of unique "{filter_lex} *" {l2_units}\n({unique_vals:,} unique)',
        ylabel='observed tokens', logy=False,
        title=f'Increasing "{filter_lex} *" Bigram Marginal Frequencies\n(in {pos_sample}+ {dataset})\nN={_N:,}')

    filter_plot_df(df).plot(
        kind='line', cmap='seismic', legend=False, figsize=size,
        xlabel=f'sequential order of unique "{filter_lex} *" {l2_units}\n({unique_vals:,} unique)',
        ylabel='observed tokens (log)', logy=True,
        title=f'Increasing "{filter_lex} *" Bigram Marginal Frequencies\n(log transfromed {pos_sample}+ {dataset})\nN={_N:,}'.title())

    # filter_plot_df(df, 'f2_sqrt').plot(
    #     kind='line', cmap='lisa_frank', legend=False, figsize=size,
    #     xlabel=f'sequential order of unique "{filter_lex} *" {l2_unit}\n({unique_vals:,} unique)',
    #     ylabel='square root of observed tokens', logy=False,
    #     title=f'Increasing "{filter_lex} *" Bigram Marginal Frequencies\n(square root transformed {pos_sample}+ {dataset})\nN={_N:,}'.title())

    # filter_plot_df(df, 'tpm_f2').plot(
    #     kind='line', cmap='purple_teal_r', legend=False, figsize=size,
    #     xlabel=f'sequential order of unique "{filter_lex} *" {l2_unit}\n({unique_vals:,} unique)',
    #     ylabel='observed tokens (tokens/mill)', logy=False,
    #     title=f'Increasing "{filter_lex} *" Bigram Marginal Frequencies\n(tokens per million in {pos_sample}+ {dataset})\nN={_N:,}'.title())


def show_example_l2(combined_amdf, example_l2: str = None, cmap: str = None,
                    polarity=None, dataset=None, pos_sample=None, l1=None, precision: int = 3,
                    index_order=None, transpose: bool = False, columns: list = None):

    index_order = index_order or ['l2', 'dataset',
                                  'pos_sample', 'direction', 'polarity']
    example_l2 = example_l2 or combined_amdf.sample(1).l2.squeeze()
    ex_l2_amdf = combined_amdf.reset_index()
    addons = []
    if 'polarity' in ex_l2_amdf.columns:
        column_label = f'ENV~{example_l2}'
        comparison = 'Polarity Sensitivity'
        if '_' not in example_l2:
            comparison = 'Independent ' + comparison
        else:
            addons.append('adj_total')
    else:
        cmap = cmap or 'RdPu'
        if 'polarity' in index_order:
            index_order.pop(index_order.index('polarity'))
        if 'l1' not in index_order:
            index_order.insert(1, 'l1')
        addons.extend(['dP2', 'P2'])
        column_label = f'ADV~{example_l2}'
        comparison = 'Context-Blind Bigram-Internal Cohesion'

    cmap = cmap or ('PRGn' if '_' in example_l2 else 'BrBG')
    index_order = combined_amdf.filter(index_order).columns.to_list()
    index_dict = dict.fromkeys(index_order)
    index_dict['l2'] = example_l2
    if l1:
        index_dict['l1'] = l1
    if polarity:
        index_dict['polarity'] = polarity
    if dataset:
        index_dict['dataset'] = dataset
    if pos_sample:
        index_dict['pos_sample'] = pos_sample
    index_by = combined_amdf.filter(
        items=list(index_dict.keys())).columns.to_list()

    columns = columns or INVESTIGATE_COLUMN_LIST
    index_by = ['l2'] + index_by
    columns = index_by + ['direction'] + columns + addons

    ex_l2_amdf = combined_amdf.reset_index().filter(items=columns)

    ex_l2_amdf = ex_l2_amdf.set_index(index_by).sort_index()
    ex_l2_amdf.drop(
        columns=(ex_l2_amdf.filter(regex=r'm$|_sqrt|l2|space|adj$|f1|N|^exp_f')
                 .columns.to_list()),
        inplace=True)

    ex_l2_amdf = ex_l2_amdf.xs(
        tuple(pd.Series(index_dict.values())
              .drop_duplicates().dropna()))
    while ex_l2_amdf.index.levshape[0] == 1:
        level_val = ex_l2_amdf.index.get_level_values(0)[0]
        if ex_l2_amdf.index.names[0] == 'l1':
            column_label = f"{level_val}~{column_label.split('~')[1]}"
        else:
            column_label = f'{level_val.upper()} {column_label}'
        ex_l2_amdf = ex_l2_amdf.droplevel(0)

    ex_l2_amdf.columns.set_names(column_label, inplace=True)
    columns_tag = ex_l2_amdf.columns.name.replace(' ', '-')
    if transpose:
        ex_l2_amdf = ex_l2_amdf.transpose().convert_dtypes()

    sty = set_my_style(
        ex_l2_amdf,
        caption=(f"{comparison} of <b><i>"
                 + (column_label.replace('ENV~', '')
                    .replace('_', ' ').replace('~', ' '))
                 + "</i></b>"
                 ).capitalize(),
        precision=precision
    ).background_gradient(cmap, axis=1 if transpose else 0)
    return save_html(format_negatives(format_zeros(sty, zeros_opacity=35)), 
        subdir=f"env~l2_examples/{example_l2}",
        stem=f"{columns_tag}_example-table")


def eval_sig(_df):
    _df['direction'] = _df.LRC.apply(lambda r: 'attract' if r > 0 else (
        'repel' if r < 0 else 'insignif')).astype('category')
    _df['LRC!=0'] = _df.LRC != 0
    return _df


def rank_rows(df):
    return (df
            .assign(rank=range(1, len(df)+1))
            .reset_index()
            .set_index(['rank'] + df.index.names))


def save_html(sty, stem: str,
              subdir: str = None):
    subdir = subdir or 'exactly'
    html_path = TABLE_DIR.joinpath(f'{subdir}/{stem}.{timestamp_today()}.html')
    confirm_dir(html_path.parent)
    print(
        f'html table saved as\n  "{html_path.relative_to(WRITING_LINKS)}"')
    sty.to_html(html_path)
    return sty

# def style_crosstab(df,
#                    rows: list,
#                    columns: list,
#                    value_col: str,
#                    aggfunc: str = 'sum',
#                    normalize=None,
#                    mark_zeros: bool = None,
#                    cmap: str = None,
#                    cmap2: str = None,
#                    cmap3: str = None,
#                    precision: int = None,
#                    index_font: str = None,
#                    group: bool = True,
#                    group_col: str = None,
#                    sort: bool = True,
#                    sort_col_vals: tuple = None,
#                    prefilter_label: str = '',
#                    return_cross_df: bool = False,
#                    axis=0):  # sourcery skip: simplify-boolean-comparison
#     cmap = cmap or colors.random_colormap_selection()
#     print('colormap selected:', cmap if isinstance(cmap, str) else cmap.name)
#     ctdf = pd.crosstab(
#         [df[r] for r in rows],
#         [df[c] for c in columns],
#         values=df[value_col].squeeze(),
#         aggfunc=aggfunc,
#         normalize=normalize or False
#     )
#     if aggfunc in ('sum','count'):
#         ctdf = ctdf.astype('Int64')
#     if sort:
#         ctdf = ctdf.sort_values(
#             sort_col_vals or ctdf.columns[0], ascending=False)

#     if return_cross_df:
#         return ctdf

#     if not precision:
#         if 'f' in value_col or 'G2' in value_col:
#             precision = 1 if 'sqrt' in value_col else 0
#         elif 'P' in value_col or 'p_r' in value_col:
#             precision = 3
#         else:
#             precision = 2

#     subsets = None
#     if (group and axis != 0
#         # and 'tpm' in value_col
#         and ((len(columns) > 1)
#              or (len(rows) > 1 and axis != 1))):
#         subsets = [
#             ctdf.filter(like=x).columns.to_list()
#             for x in ctdf.columns.get_level_values(group_col or columns[0])
#         ]
#         print_iter(subsets, header='gradient subsets:')

#     gradient_by = 'row' if axis == 1 else (
#         'column' if axis == 0
#         else ('whole group' if group
#               else 'whole table'))

#     # if mark_neg:
#     #     # sty = style_neg_vals(ctdf.fillna(-0.5), neg_color='maroon', neg_weight='bold')
#     #     sty = style_neg_vals(ctdf.fillna(-0.5), neg_color='maroon', neg_weight='bold')
#     # else:
#     #     sty = ctdf.style
#     ctdf.index.name = None
#     sty = ctdf.style.set_caption(
#         f'Crosstabulated <code>{value_col}</code> (as {aggfunc})<br/>color gradient set by <u>{gradient_by}</u>')
#     if mark_zeros != False:
#         if value_col.startswith(('LRC', 'dP1', 'P1', 'unexp_r', 'tpm_unexp_r')):
#             negligible = pd.DataFrame(
#                 {'LRC': {'left': -0.05,
#                         'right': 0.05},
#                 'LRCm': {'left': -0.1,
#                         'right': 0.1},
#                 'dP1': {'left': -0.05,
#                         'right': 0.05},
#                 'dP1m': {'left': -0.1,
#                         'right': 0.1},
#                 'tpm_unexp_r': {'left': -0.15,
#                                 'right': 0.15},
#                 'unexp_r': {'left': -0.1,
#                             'right': 0.1},
#                 'unexp_r_sqrt': {'left': -0.15,
#                                 'right': 0.15},
#                 'P1': {'left': 0.45,
#                         'right': 0.55},
#                 'P1m': {'left': 0.45,
#                         'right': 0.55}}
#             )
#             sty = sty.highlight_between(
#                 left=negligible.loc['left', value_col], right=negligible.loc['right', value_col], axis=1, props='opacity: 75%;')
#         else:
#             sty = sty.highlight_between(
#                     left=-0.045, right=0.045, axis=1, props='opacity: 75%;')
#     if subsets:
#         cmap2=cmap2 or cmap
#         cmap3=cmap3 or cmap
#         for s, c in zip(subsets, [cmap,cmap2,cmap3][:len(subsets)]):
#             sty = sty.background_gradient(cmap=c, subset=s, axis=axis)
#     else:
#         sty.background_gradient(cmap=cmap, axis=axis)
#
#     sty = set_my_style(sty, precision, index_font=index_font)
#     out_dir = SANPI_HOME.joinpath(f'info/writing_links/imports/tables/{prefilter_label}')
#     confirm_dir(out_dir)
#     html_path = out_dir.joinpath(
#         f'{"-".join(rows)}_{value_col}-{aggfunc}_{"-".join(columns)}_color-table{"-grouped" if subsets else ""}.{timestamp_hour()}.html')
#     print(
#         f'formatted table saved as html: {html_path.relative_to(WRITING_LINKS)}')
#     sty.to_html(html_path)
#     return sty

# > sourcery suggestion 👇


@lru_cache(maxsize=32)
def _get_negligible_ranges(value_col):
    negligible_ranges = {
        'LRC': (-0.0049, 0.0049),
        'LRCm': (-0.1, 0.1),
        'dP1': (-0.0149, 0.0149),
        'dP1m': (-0.1, 0.1),
        'tpm_unexp_r': (-0.15, 0.15),
        'unexp_r': (-0.1, 0.1),
        'unexp_r_sqrt': (-0.15, 0.15),
        'P1': (0.475, 0.525),
        'P1m': (0.45, 0.55)
    }
    return negligible_ranges.get(value_col, (-0.045, 0.045))


def _infer_precision(value_col):
    if 'f' in value_col or 'G2' in value_col:
        return 1 if 'sqrt' in value_col else 0
    elif 'P' in value_col or 'p_r' in value_col:
        return 3
    return 2


def style_crosstab(df, rows, columns, value_col,
                   aggfunc='sum', normalize: str = None,
                   mark_zeros: bool = None,
                   zeros_opacity: int = None,
                   cmap=None,
                   cmap2='random', cmap3='random',
                   precision=None, index_font=None,
                   group=True, group_col=None,
                   sort=True, sort_col_vals=None,
                   prefilter_label='',
                   return_cross_df=False,
                   vmax=None,
                   vmin=None,
                   axis=0):
    """Create a styled crosstab with customizable visualization and formatting.

    This function generates a styled cross-tabulation of data with advanced visualization options, including color gradients, zero highlighting, and precision control.

    Args:
        df: Input DataFrame to be cross-tabulated.
        rows: Columns to use for row indexing in the crosstab.
        columns: Columns to use for column indexing in the crosstab.
        value_col: Column containing values to aggregate.
        aggfunc: Aggregation function to use. Defaults to 'sum'.
        normalize: Whether to normalize the crosstab values. Defaults to None.
        mark_zeros: Whether to highlight near-zero values. Defaults to None.
        cmap: Primary colormap for gradient. Defaults to None.
        cmap2: Secondary colormap. Defaults to None. Use 'random' to select random gradient colormap.
        cmap3: Tertiary colormap. Defaults to None. Use 'random' to select random gradient colormap.
          **note** None will use cmap value, 
                   but setting cmap3 (None or a string) will only apply to a third group if cmap2 != 'random'
        precision: Number of decimal places to display. Defaults to None.
        index_font: Font for index labels. Defaults to None.
        group: Whether to group gradient coloring. Defaults to True.
        group_col: Column to use for grouping. Defaults to None.
        sort: Whether to sort the crosstab. Defaults to True.
        sort_col_vals: Columns to use for sorting. Defaults to None.
        prefilter_label: Label for output directory. Defaults to ''.
        return_cross_df: Whether to return the crosstab DataFrame. Defaults to False.
        axis: Axis for gradient coloring. Defaults to 0.

    Returns:
        Styled DataFrame with applied visualization and formatting.

    Examples:
        >>> style_crosstab(df, ['adj'], ['dataset', 'pos_sample', 'polarity'], 'LRC', aggfunc='mean')
        >>> style_crosstab(df, ['direction'], ['polarity', 'dataset', 'pos_sample'], 'adj', 
            aggfunc='count', axis=None, cmap='viridis', cmap2='random')
    """

    # Efficient crosstab computation
    ctdf = pd.crosstab(
        [df[r] for r in rows],
        [df[c] for c in columns],
        values=df[value_col].squeeze(),
        aggfunc=aggfunc,
        normalize=normalize or False
    )

    # Optimize type conversion and sorting
    if aggfunc in ('sum', 'count'):
        ctdf = ctdf.astype('Int64')

    if sort:
        ctdf = ctdf.sort_values(
            sort_col_vals or ctdf.columns[0],
            ascending=False
        )

    if return_cross_df:
        return ctdf

    # Precompute colormap and precision
    precision = precision or _infer_precision(value_col)

    # print(pd.Series({str(i): (c if isinstance(c, str) else c.name)
    #                  for i, c in enumerate((cmap, cmap2, cmap3), start=1)
    #                  }).drop_duplicates()
    #       .to_frame('Selected Colormap(s)').to_markdown(tablefmt='plain'))

    # Efficient subset generation
    gradient_by, cmaps, subsets = determine_subsets(columns, cmap, cmap2, cmap3,
                                                    group, group_col, axis, ctdf)

    # Styling with optimized path generation
    # ctdf.index.name = None

    sty = set_my_style(ctdf, precision=precision, index_font=index_font,
                       caption=(
                           f'Crosstabulated <code>{value_col}</code> (as {aggfunc})<br/>'
                           f'color gradient set by <u>{gradient_by}</u>'))
    
    sty = _highlight_values(sty, 
                            min_val = ctdf.min().min(), 
                            value_col=value_col, 
                            mark_zeros=mark_zeros,
                            zeros_opacity=zeros_opacity)
    
    sty = _apply_background_gradient(sty,
                                     subsets=subsets, cmaps=cmaps,
                                     axis=axis, vmin=vmin, vmax=vmax)


    # Efficient path generation
    out_dir = (TABLE_DIR / prefilter_label)
    out_dir.mkdir(parents=True, exist_ok=True)

    html_filename = (
        f'{"-".join(rows)}_{value_col}-{aggfunc}_'
        f'{"-".join(columns)}_color-table'
        f'{"_grouped" if subsets else ""}'
        f'.{timestamp_hour()}.html'
    )
    html_path = out_dir / html_filename

    print(
        f'formatted table saved as html: {html_path.relative_to(WRITING_LINKS)}')
    sty.to_html(html_path)

    return sty


def determine_subsets(columns, cmap, cmap2, cmap3, group, group_col, axis, ctdf):
    gradient_by = 'row' if axis == 1 else (
        'column' if axis == 0
        else ('whole group' if group
              else 'whole table'))
    cmap = cmap or colors.random_colormap_selection().name
    cmaps = [cmap]
    subsets = None
    if (group
        and gradient_by == 'whole group'
        # and (len(columns) > 1
                #      or (len(rows) > 1 and axis != 1))
        ):
        cmaps.extend([c for c in [cmap2 or cmap, cmap3 or cmap]
                      if (c and c != 'random')])
        rand_cmaps = colors.random_colormap_selection(5)
        cmaps.extend([c.name for c in rand_cmaps])

        subsets = [
            ctdf.filter(like=x).columns.to_list()
            for x in ctdf.columns.get_level_values(group_col or columns[0]).unique()
        ]

    return gradient_by, cmaps, subsets


def _apply_background_gradient(sty, subsets, cmaps, axis, vmin, vmax):
    if not subsets:
        return sty.background_gradient(cmap=cmaps[0], axis=axis)

    colored_subsets = {(i, c): s for i, (s, c)
                       in enumerate(zip(subsets, cmaps), start=1)}
    # print_iter(colored_subsets, header='gradient subsets:')
    for (__, c_sub), subset in colored_subsets.items():
        if vmin and vmax:
            sty = sty.background_gradient(
                cmap=c_sub, subset=subset, axis=axis, vmin=vmin, vmax=vmax)
        elif vmin:
            sty = sty.background_gradient(
                cmap=c_sub, subset=subset, axis=axis, vmin=vmin)
        elif vmax:
            sty = sty.background_gradient(
                cmap=c_sub, subset=subset, axis=axis, vmax=vmax)
        else:
            sty = sty.background_gradient(cmap=c_sub, subset=subset, axis=axis)

    return sty

def format_negatives(sty, min_val=-10*6):
    return _apply_neg_highlighting(min_val=min_val, sty=sty)

def format_zeros(sty, 
                 value_col:str='LRC', 
                 zeros_opacity: int = None):
    
    return _apply_zero_highlighting(sty=sty,
                             value_col=value_col,
                             zeros_opacity=zeros_opacity)

def _highlight_values(sty, min_val, value_col, mark_zeros, zeros_opacity):
    if mark_zeros is not False:
        sty = _apply_zero_highlighting(
            sty, value_col, zeros_opacity=zeros_opacity)
    return _apply_neg_highlighting(min_val, sty)


def _apply_neg_highlighting(min_val, sty):
    return sty.highlight_between(
        left=min(-1, min_val),
        right=0,
        inclusive='left',
        props='font-weight:bold; text-decoration: underline')

def _apply_zero_highlighting(sty,
                             value_col: str,
                             zeros_opacity: int = None):

    left, right = _get_negligible_ranges(value_col)
    return sty.highlight_between(
        left=left, right=right,
        # axis=1,
        props=f'opacity: {zeros_opacity or 60}%;'
    )

def color_compiled_adv(_amdf: pd.DataFrame,
                       adverb: str,
                       index_cols: list = None,
                       freq_only: bool = False):
    index_cols = index_cols or ['l2', 'Polar', 'Sample', 'Set']
    index_cols = [i.replace('Polarity', 'Polar') for i in index_cols]
    _amdf = (_amdf.copy()
             .assign(polarity=_amdf.polarity.map({'neg': '(-)',
                                                  'pos': '(+)'}))
             .reset_index()
             .rename(columns={'dataset': 'Set',
                              'pos_sample': 'Sample',
                              'polarity': 'Polar'})
             .set_index(index_cols)
             #   .xs(adverb)
             .filter(regex=r'([fN]|f.*[^t])$' if freq_only else r'(LRC|G2|P1|tpm_(f\d?|unexp_f)|^[Nf])$')
             )
    # if 'l2' not in _amdf.columns:
    #     _amdf = _amdf.assign(l2=adverb)
    #     if 'l2' not in index_cols:
    #         index_cols.append('l2')
    if 'l2' in index_cols:
        _amdf.xs(adverb)
    # else assume passed frame only contains indicated adverb
    # _amdf['N (mill)'] = _amdf.N / (1000000)
    # _amdf.drop(columns=['N'], inplace=True)
    if freq_only:
        _amdf = _amdf.filter(regex=r'[Nf]').drop(
            columns=_amdf.filter(regex=r'(^exp)|(_exp)').columns)
    _amdf.columns = _amdf.columns.str.replace('unexp_f', 'fu')
    adv_sty = (
        set_my_style(_amdf.sort_index(axis=0).style, index_font='',
                     index_size=8)
        .set_caption(
            f'Compiled {"Frequencies" if freq_only else "Association Values"}'
            f' for <i><b>{adverb}</b></i><br/>(<code>tpm</code>="tokens per million"; rounded)')
        .background_gradient(cmap='purple_rain', axis=0, subset=_amdf.filter(like='tpm_f').columns.to_list())
        # .background_gradient(cmap='Blues', axis=0, subset=_amdf.filter(like='exp_f').columns.to_list())
        .background_gradient(cmap='purple_teal', subset=_amdf.filter(like='fu').columns.to_list())
        # .background_gradient(cmap='coolwarm', subset=_amdf.filter(like='unexp_r').columns.to_list())
        # .background_gradient(cmap='purple_rain', axis=0, subset=_amdf.filter(like='N (mill)').columns.to_list(), vmax=_amdf['N (mill)'].quantile(0.75) #  vmin=500000, vmax=10000000
        #                      )
        .background_gradient(cmap='purple_rain', subset=['f'], axis=0, vmax=_amdf.f.quantile(0.75))
        .background_gradient(cmap='purple_rain', subset=['N'], axis=0, vmax=_amdf.N.quantile(0.75))
        # .background_gradient(cmap='Spectral', subset=['unexp_r'], axis=None, vmin=-1, vmax=1)
    )
    if freq_only:
        adv_sty = (adv_sty
                   .background_gradient(cmap='purple_rain', subset=['f1'], axis=0,
                                        vmax=_amdf.f1.quantile(0.95),
                                        vmin=_amdf.f1.quantile(0.05))
                   .background_gradient(cmap='purple_rain', subset=['f2'], axis=0,
                                        vmax=_amdf.f2.quantile(0.95),
                                        vmin=_amdf.f2.quantile(0.05))
                   )
    else:
        adv_sty = (adv_sty
                   .background_gradient(cmap='anastasia', axis=None, subset=['dP1'], vmin=-0.83, vmax=0.83)
                   .background_gradient(cmap='anastasia', axis=None, subset=['LRC'], vmin=-7, vmax=7)
                   .background_gradient(cmap='anastasia', axis=None, subset=['P1'], vmin=0, vmax=1)
                   .background_gradient(cmap='lilac_rose', axis=0, subset=['G2']))
    adv_sty = adv_sty.format(subset=_amdf.filter(
        regex=r'[fG]').columns.to_list(), precision=0, thousands=',')
    adv_dir = TABLE_DIR.joinpath(adverb)
    confirm_dir(adv_dir)
    html_path = adv_dir.joinpath(
        f'{adverb}_{"".join(index_cols)}_{"f" if freq_only else "am+f"}.{timestamp_hour()}.html')

    print(
        f'Stylized table for {adverb} saved as "{html_path.relative_to(WRITING_LINKS)}"')
    adv_sty.to_html(html_path)
    return adv_sty


def color_polar_table(_polar_df, indexer: str = 'l2',
                      html_stem=None):
    indexer_str = indexer
    if indexer == 'space_l2':
        indexer = ['l2', 'dataset', 'pos_sample']
    elif indexer == 'space':
        indexer = ['dataset', 'pos_sample']
    try:
        _index = _polar_df[[indexer] if isinstance(indexer, str) else indexer]
    except KeyError:
        _polar_df = _polar_df.reset_index()
        _index = _polar_df[[indexer] if isinstance(indexer, str) else indexer]
    re_metrics = r'[1C]m' if indexer == 'l2' else r'P1|LRC'
    re_freq = r'[tpm_]*f.*m' if indexer == 'l2' else r'f|N'
    if html_stem:
        outpath = SANPI_HOME.joinpath(
            f'info/writing_links/imports/tables/{html_stem}.by-{indexer}.{timestamp_now_trim()}.html')
        print(f'html formatted table saved as: "{outpath}"')
    if _polar_df.index.name and _polar_df.index.name == indexer:
        _polar_df = _polar_df.reset_index()
    # padfm = _polar_df.filter(regex=re_metrics).join(_index).drop_duplicates(indexer).set_index(indexer).join(
    #     _polar_df.filter(regex=re_freq).join(_index).drop_duplicates(indexer).set_index(indexer)
    # )
    padfm = _polar_df.set_index(indexer)
    padfm = padfm[padfm.filter(regex=re_metrics).columns.to_list(
    ) + padfm.filter(regex=re_freq).columns.to_list()]
    if indexer != 'l2':
        padfm = padfm.filter(['dP1(+)', 'dP1(-)', 'LRC(+)', 'LRC(-)',
                              'P1(+)', 'P1(-)', 'tpm_unexp_f(+)', 'tpm_unexp_f(-)',
                             'tpm_f(+)', 'tpm_f(-)', 'tpm_f2', 'N'])
    padfm.columns = padfm.columns.str.replace('unexp_f', 'fu')
    if indexer_str.startswith('space'):
        padfm = padfm.sort_index(ascending=False)

    stylized = (padfm.style
                .background_gradient(subset=padfm.filter(like='dP').columns, cmap="anastasia", axis=None, vmin=-0.83, vmax=0.83)
                .background_gradient(subset=padfm.filter(regex=r'^P').columns, cmap="anastasia", axis=None,  vmin=0, vmax=1)
                .background_gradient(subset=padfm.filter(like='LRC').columns, cmap="anastasia", axis=None, vmin=-7, vmax=7)
                .background_gradient(subset=padfm.filter(like='f').columns, cmap='purple_rain', axis=0)
                .background_gradient(subset=padfm.filter(like='fu').columns, cmap='cerulean_royalty_r')
                .background_gradient(subset=padfm.filter(like='N').columns, cmap='Blues', low=0.65)
                .format(thousands=',').set_table_styles([
                    {'selector': 'th.index_name',
                     'props': 'font-size:8pt; font-family: iosevka aile; font-style:italic; color:darkgrey'},
                    {'selector': 'th.col_heading',
                     'props': 'font-family: iosevka fixed; font-size:10.5pt; text-align:center'},
                    {'selector': 'th.row_heading',
                     'props': 'font-weight: 600; font-family: CMU classical serif; font-size: 11pt'}])
                .set_properties(**{'text-align': 'right', 'font-family': 'iosevka aile', 'font-weight': '400', 'font-size': '8.5pt'}))

    if html_stem:
        stylized.to_html(outpath)
    else:
        return stylized


def viz_adv_polar(adverb: str, _adv_df: pd.DataFrame,
                  colormap_name='lilac_rose',
                  size_tuple=(6, 2.5)):
    polar_adv_df = plot_polar_grouped(
        _adv_df.filter(regex=r'~('+adverb+r')$', axis=0),
        # .filter(regex=r'P1|LRC|unexp_f_sqrt|polar_l2|polarity|l2|space|m$')
        indexer='space_l2', size_tuple=size_tuple,
        colormap_name=colormap_name,
        image_label=adverb, save_png=True)
    color_polar_table(polar_adv_df, indexer='space_l2',
                      html_stem=f'polar-{adverb}_AM')
    return color_polar_table(polar_adv_df, indexer='space_l2')


# * plotting AMs


def plot_mean_delta(flat_df, size_tuple=(8, 10), colormap_name='purple_teal',
                    plot_kind='barh', stacked=True,
                    image_dir=None, image_label=None):
    _title = 'delta P(env|adv)'
    _df = flat_df.filter(like='dP1').sort_index(axis=1)
    _fig = _df.plot(
        kind=plot_kind, grid=True, figsize=size_tuple, stacked=stacked,
        colormap=colormap_name, title=_title, width=0.7,
        xlim=(-1, 1), ylabel='adverb', xlabel='divergence from probability of other contingencies'
        #   xticks=[-0.6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,],
    )
    col_names = _get_col_names(_df)
    plt.savefig(compose_png_path('-'.join(col_names),
                                 dirpath=image_dir, label_str=image_label),
                dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.show()


def plot_mean_lrc(flat_df, size_tuple, colormap_name='lilac_rose',
                  plot_kind='barh', stacked=True,
                  image_dir=None, image_label=None):
    _title = 'Conservative Log Ratio'
    # _lrc_ticks = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    _lrc_ticks = [-7, -5, -3, -1, 0, 1, 3, 5, 7]
    _df = flat_df.filter(like='LRC').sort_index(axis=1)
    if plot_kind == 'barh':
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple, stacked=stacked,
            xticks=_lrc_ticks, ylabel='adverb', width=0.7,
            colormap=colormap_name, title=_title)
    else:
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple, stacked=stacked,
            yticks=_lrc_ticks, xlabel='adverb', width=0.7,
            colormap=colormap_name, title=_title)
    col_names = _get_col_names(_df)
    plt.savefig(compose_png_path('-'.join(col_names),
                                 dirpath=image_dir, label_str=image_label),
                dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.show()


def _get_col_names(_df):
    return _df.columns.get_level_values(0).to_series().drop_duplicates().apply(snake_to_camel)


def plot_polar_f(flat_df, size_tuple, colormap_name, plot_kind='barh',
                 image_dir=None, image_label=None):

    if any(flat_df.filter(regex=r'^f_sqrt')):
        _title = 'Joint Frequency (sqrt)'
        _df = flat_df.filter(regex=r'^f_sqrt').sort_index(axis=1)
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple,
            colormap=colormap_name, stacked=True, ylabel='+'.join(_df.index.names),
            xlabel='square root of joint frequency',
            title=_title,
        )
        col_names = _get_col_names(_df)
        plt.savefig(compose_png_path('-'.join(col_names),
                                     dirpath=image_dir, label_str=image_label),
                    dpi=300, bbox_inches='tight', pad_inches=0.2)

    if any(flat_df.filter(regex=r'^tpm_f_sqrt')):
        _title = 'Joint Frequency (tokens per million; sqrt)'
        _df = flat_df.filter(regex=r'^tpm_f_sqrt').sort_index(axis=1)
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple,
            colormap=colormap_name, stacked=True,
            xlabel='square root of tokens per million',
            title=_title, ylabel='+'.join(_df.index.names)
        )
        col_names = _get_col_names(_df)
        plt.savefig(compose_png_path('-'.join(col_names),
                                     dirpath=image_dir, label_str=image_label),
                    dpi=300, bbox_inches='tight', pad_inches=0.2)

    if any(flat_df.filter(regex=r'^unexp_f_sqrt')):
        _title = 'Joint Frequency Divergence (sqrt)'
        _df = flat_df.filter(regex=r'^unexp_f_sqrt').sort_index(axis=1)
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple,
            stacked=(_df < 0).value_counts().nunique() == 1,
            xlabel='square root of unexpected frequency',
            colormap=colormap_name, title=_title, ylabel='+'.join(
                _df.index.names)
        )
        col_names = _get_col_names(_df)
        plt.savefig(compose_png_path('-'.join(col_names),
                                     dirpath=image_dir, label_str=image_label),
                    dpi=300, bbox_inches='tight', pad_inches=0.2)
        plt.show()
    if any(flat_df.filter(regex=r'^tpm_unexp_f_sqrt')):
        _title = 'Joint Frequency Divergence (tokens per million; sqrt)'
        _df = flat_df.filter(regex=r'^tpm_unexp_f_sqrt').sort_index(axis=1)
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple,
            stacked=(_df < 0).value_counts().nunique() == 1,
            xlabel='square root of tokens per million',
            colormap=colormap_name, title=_title, ylabel='+'.join(
                _df.index.names)
        )
        col_names = _get_col_names(_df)
        plt.savefig(compose_png_path('-'.join(col_names),
                                     dirpath=image_dir, label_str=image_label),
                    dpi=300, bbox_inches='tight', pad_inches=0.2)
        plt.show()

    if any(flat_df.filter(like='tpm_f_sqrt')):
        _title = 'Joint Frequency Comparison (sqrt)'
        _df = flat_df.filter(
            ['tpm_unexp_f_sqrt_m(+)', 'tpm_unexp_f_sqrt(+)',
                'tpm_f_sqrt_m(+)', 'tpm_f_sqrt(+)',
                'tpm_f_sqrt_m(-)', 'tpm_f_sqrt(-)',
                'tpm_unexp_f_sqrt_m(-)', 'tpm_unexp_f_sqrt(-)'
             ]
        )
        if _df.empty:
            _df = flat_df.filter(regex=r'tpm_(unexp_f|f)_sqrt')

        _fig = _df.plot(
            kind=plot_kind, grid=True, width=0.75,
            figsize=(size_tuple[0], size_tuple[1]+3),
            # xlim=(-150,550),
            colormap=colormap_name, title=_title, ylabel='+'.join(
                _df.index.names),
            xlabel='square root of tokens per million'
        )
        col_names = _get_col_names(_df)
        plt.savefig(compose_png_path('-'.join(col_names),
                                     dirpath=image_dir, label_str=image_label),
                    dpi=300, bbox_inches='tight', pad_inches=0.2)
        plt.show()

    if any(flat_df.filter(like='unexp_r')):
        _title = 'Joint Frequency Divergence Ratio\n(expected - observed) / observed'
        _df = flat_df.filter(like='unexp_r').sort_index(axis=1)
        _fig = _df.plot(
            kind=plot_kind, grid=True, figsize=size_tuple,
            stacked=(_df < 0).value_counts().nunique() == 1,
            xlim=(-1, 1), width=0.7,
            colormap=colormap_name, title=_title, ylabel='+'.join(
                _df.index.names),
            xlabel='unexpected tokens / observed tokens (floor = -1)'
        )
        col_names = _get_col_names(_df)
        plt.savefig(compose_png_path('-'.join(col_names),
                                     dirpath=image_dir, label_str=image_label),
                    dpi=300, bbox_inches='tight', pad_inches=0.2)
        plt.show()


def join_polar_vals(adv_amdf, indexer):
    one_word = adv_amdf.l2.nunique() == 1
    nonpolar = adv_amdf.copy().filter(regex=r'N|f2|space|pos_sample|dataset|^l2')
    grouped = {k: g.set_index(indexer) for k, g
               in (adv_amdf[
                   (adv_amdf.columns[
                       (~adv_amdf.columns.isin(nonpolar.columns))
                   ].to_list() + [indexer]
                   )]
                   .groupby('polarity'))}

    jdf = grouped['neg'].join(
        grouped['pos'],
        rsuffix='(+)', lsuffix='(-)',
        how='outer').convert_dtypes()
    jdf = jdf.loc[:, ~jdf.columns.str.startswith('polar')]
    jdf = jdf.join(nonpolar.drop_duplicates().set_index(indexer)
                   ).convert_dtypes().drop_duplicates()
    if indexer == 'l2':
        jdf = jdf.filter(like='m').round(6).drop_duplicates()
    elif indexer == 'space' or one_word:
        jdf = jdf.loc[:, ~jdf.columns.str.endswith(('m', 'm(-)', 'm(+)'))]

    # HACK
    if indexer.startswith('space'):
        jdf = jdf.reset_index().set_index((['pos_sample', 'dataset'])
                                          if indexer == 'space'
                                          else ['l2', 'pos_sample', 'dataset'])

    return jdf.sort_values(
        jdf.filter(['dP1m(-)', 'dP1(-)', 'LRC(-)', 'LRCm(-)'])
        .columns.to_list()
    )


def compose_png_path(plot_name: str,
                     dirpath: Path,
                     label_str: str = '',
                     suffix: str = '.png'):
    if label_str:
        dirpath = dirpath.joinpath(label_str)
    confirm_dir(dirpath)
    _path = dirpath.joinpath(
        '_'.join([label_str, plot_name, timestamp_hour().replace('-', '')])
    ).with_suffix(suffix)
    print(f'Output Path: "{_path}"')
    return _path


def plot_polar_grouped(adv_amdf, indexer: str = 'l2',
                       size_tuple: tuple = (6, 10.5),
                       colormap_name: str = 'coolwarm',
                       plot_kind='barh',
                       image_dir=Path(SANPI_HOME.joinpath(
                           'info/writing_links/imports/images')),
                       image_label='',
                       save_png: bool = False):

    # sourcery skip: identity-comprehension
    one_word = adv_amdf.l2.nunique() == 1
    # print(adv_amdf.sample(2).T.to_markdown(floatfmt=',.0f'))
    if not one_word and size_tuple[1] < 4:
        size_tuple = (size_tuple[0], adv_amdf.l2.nunique() * 2.5)

    # print(grouped['neg'].sample(2).T.to_markdown(floatfmt=',.0f'))
    # print(grouped['pos'].sample(2).T.to_markdown(floatfmt=',.0f'))
    flat_df = join_polar_vals(
        adv_amdf, indexer=indexer
    ).select_dtypes(include='number').convert_dtypes().round(5).drop_duplicates()

    # nb_show_table(flat_df.describe())
    # plots
    if not one_word:
        try:
            for filt_regex in [r'LRCm',  r'dP1m|unexp_r.*m', r'^P1m',  r'f_']:
                (flat_df.filter(regex=filt_regex)
                 .sort_index(axis=1).reset_index(drop=True)
                 .plot(
                    subplots=True, layout=(3, 2),
                    figsize=(8, 11) if min(size_tuple) > 4 else (5, 9),
                    kind='barh', colormap=colormap_name,
                    sharex=True, sharey=True,
                    legend=False))
        except ValueError:
            pass
    # print(flat_df.index.to_series().describe())
    try:
        flat_df.index.name = flat_df.index.name.replace('l2', 'adverb')
    except AttributeError:
        pass

    if any(flat_df.filter(regex=r'f_|unexp')):
        plot_polar_f(flat_df, size_tuple, colormap_name,
                     image_dir=image_dir, image_label=image_label)

    if not one_word and indexer == 'l2':
        flat_df.filter(regex=r'^P1').sort_index(axis=1).plot(
            kind=plot_kind, grid=True, xlim=(0, 1), figsize=size_tuple,
            colormap=colormap_name, stacked=True,
            title='Conditional Probability, P(env|adv)')

    plot_mean_delta(size_tuple=size_tuple, colormap_name=colormap_name,
                    plot_kind=plot_kind, flat_df=flat_df,
                    image_dir=image_dir, image_label=image_label)

    plot_mean_lrc(size_tuple=size_tuple, colormap_name=colormap_name,
                  plot_kind=plot_kind, flat_df=flat_df,
                  image_dir=image_dir, image_label=image_label)
    try:
        polar_df = join_polar_vals(adv_amdf, indexer='space_l2')
    except KeyError:
        polar_df = flat_df

    # > using the (+) columns means it's ranked by descending (-) without the `ascending=False` arg
    return polar_df.sort_values(polar_df.filter(['dP1m(+)', 'dP1(+)', 'LRC(+)', 'LRCm(+)']).columns.to_list())
