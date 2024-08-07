import re
from os import system
from pathlib import Path
from pprint import pprint

import pandas as pd
import pyarrow as pyar

from source.utils.associate import POLAR_DIR, RESULT_DIR, TOP_AM_DIR, adjust_am_names
# from source.utils.dataframes import show_sample
from source.utils.dataframes import REGNOT
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import update_assoc_index as update_index
from source.utils.dataframes import write_part_parquet as parq_it
from source.utils.general import (confirm_dir, print_iter, snake_to_camel,
                                  timestamp_today)
from source.utils.sample import sample_pickle as sp

SPELL_OUT = {'pol': 'polarity',
             'pos': 'positive',
             'neg': 'negative',
             'mir': 'mirror',
             'diff': 'difference',
             'dep': 'dependency',
             'am': 'association measure',
             'adv': 'adverb',
             'adj': 'adjective',
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
MISC_AM = ['am_odds_ratio_disc',
           't_score',
           'mutual_information',]
FREQ_COLS = ['f', 'f1', 'f2']
ADX_COLS = ['adv', 'adv_total', 'adj', 'adj_total']
P2_COLS = ['am_p2_given1', 'am_p2_given1_simple']
DELTA_COLS = ['deltaP_max', 'deltaP_mean']
FOCUS_DICT = {
    'ALL': {
        'adv_adj': BASIC_FOCUS + P2_COLS + DELTA_COLS + MISC_AM,
        'polar': BASIC_FOCUS + ADX_COLS + MISC_AM},
    'NEQ': {
        'adv_adj': BASIC_FOCUS + P2_COLS + DELTA_COLS + MISC_AM,
        'polar': BASIC_FOCUS + P2_COLS + ADX_COLS + MISC_AM
    }}

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
        blind_cols = ['conservative_log_ratio',
                      'am_log_likelihood',
                      'deltaP_max', 'deltaP_mean']
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
                 metric_filter: str or list = None,
                 data_tag: str = 'ALL',
                 k: int = 10,
                 eval_type: str = 'polar',
                 val_col: str = 'adv',
                 ignore_neg_adv: bool = True):

    if metric_filter is None:
        metric_filter = ['am_p1_given2', 'conservative_log_ratio']
    elif isinstance(metric_filter, str):
        metric_filter = [metric_filter]

    # > get filter list and columns on the same page ---> adjust everything
    metric_filter = adjust_am_names(metric_filter)
    env_df = adjust_am_names(df.copy())
    if index_like:
        env_df = env_df.filter(like=index_like, axis=0)

    # > filter to only "significant" association, based on LRC
    env_df = env_df.loc[env_df.LRC >= 1, :]

    if ignore_neg_adv:

        if 'l2' in env_df.columns:
            if not any(env_df.l2.str.contains('_')):
                env_df = env_df.loc[~env_df.l2.isin(NEG_WORDS), :]
            else:
                l2_has_neg = ((env_df.l2.str.startswith(NEG_WORDS))
                              |
                              (env_df.l2.str.endswith(NEG_WORDS)))

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
                  suppress_printing: bool = False,
                  transpose: bool = False,
                  italics: bool = True,
                  title: str = None
                  ) -> None or pd.DataFrame:
    _df = df.copy()
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

    _df = italicize_df_for_md(_df)
    if transpose:
        _df = _df.T
        _df.index = [f'`{i}`' for i in _df.index]

    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index]
    table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    if outpath:
        confirm_dir(outpath.parent)
        Path(outpath).write_text(table)
    if not suppress_printing:
        title = title.strip('\n')+'\n\n' if title else ''
        print(f'\n{title}{table}\n')
    if outpath:
        print(f'\n> saved as:  \n> `{outpath}`\n')
    return (_df if return_df else None)


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
    paths = []
    for key, df in examples.items():
        if df is not None:
            out_path = output_dir.joinpath(f'{key}_{n_ex}ex~{len(df)}.csv')
            if out_path.is_file() and not len(df) < n_ex:
                alt_dir = output_dir.joinpath('alt_ex')
                print(f"* Renaming existing version of `{out_path.name}`")
                system(f'mkdir -p "{alt_dir}"; '
                       f'mv --backup=numbered "{out_path}" "{alt_dir}/" ; '
                       f'bash /share/compling/projects/tools/datefile.sh "{alt_dir}/{out_path.name}" -r > /dev/null 2>&1')
            df.to_csv(out_path)
            paths.append(out_path)
    print_iter([f'`{p}`' for p in paths],
               header='\nSamples saved as...', bullet='+')

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
                                      adv = adv)

    examples = {}
    if hits_df_dict is None:
        hits_df_dict = {polarity or 'any': pol_df}

    polar_outdir_dict = set_polar_ex_dirs(
        adv, list(hits_df_dict.keys()), output_dir)
    # for poldir in polar_outdir_dict.values():
    #     confirm_dir(poldir)

    for i, bigram in enumerate(bigrams, start=1):
        bigram_text = bigram.replace("_", " ")
        if verbose:
            print(f'\n### {i}. _{bigram_text}_\n')
        bigram_in_pol_ex = None
        bigram_bipolar_ex = {}
        for pol_i, (pol_cue, pol_df) in enumerate(hits_df_dict.items(), start=1):
            polarity = SPELL_OUT[pol_cue]
            if verbose:
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
            
            out_path = out_dir/f'{out_dir.name}_{bigram.split("_")[1]}_{n_ex}ex~{len(pol_ex_df)}.csv'
            confirm_dir(out_path.parent)
            if out_path.is_file() and n_ex == len(pol_ex_df): 
                system("echo '    > Renaming existing version\n'; " 
                       + f"echo \"      $(mv -v --backup=t '{out_path}' '{alt_dir}/{out_path.name}')\"")
            pol_ex_df.to_csv(out_path)
            paths_dict[pol_cue]=out_path

        if verbose:
            print_iter((f'{x}. **{SPELL_OUT[pol_cue]}**  \n       `"{paths_dict[pol_cue]}"`' 
                        for x, pol_cue in enumerate(paths_dict.keys(), start=1)),
                       header=f'\n    Full polarity samples saved as...\n', 
                       indent=3, bullet='')
            print()


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
