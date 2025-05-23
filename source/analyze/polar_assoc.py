import argparse
import itertools as itt
import re
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tabulate import tabulate

from utils.associate import (AM_DF_DIR, BINARY_ASSOC_ARGS, READ_TAG,
                             RESULT_DIR, UCS_DIR, add_extra_am,
                             adjust_am_names, get_associations_csv,
                             get_vocab_size)
from utils.dataframes import (Timer, beef_up_dtypes, corners, save_table,
                              print_md_table)
from utils.general import (FREQ_DIR, PKL_SUFF, SANPI_HOME, confirm_dir,
                           run_shell_command, snake_to_camel)

#HACK #! manually control units compared
# COMPARISON_UNITS = None
# COMPARISON_UNITS = ('adv', 'adj')
# COMPARISON_UNITS = ('adv', 'adj', 'bigram')
COMPARISON_UNITS = ('adv', 'adj', 'bigram', '')
RATIO_CEIL = 0.7
OUTLIER_MARGIN_IQR_FACTOR = 4
# > set defaults
_DEFAULT_CORP_PARTS = 35
# _DEFAULT_FRQ_COUNT = 868
_DEFAULT_FRQ_COUNT = 7
# _DEFAULT_FRQ_PRCNT = '0-001p'
_DEFAULT_FRQ_PRCNT = 'MIN-7'
_DEFAULT_UCS_MIN = 500

# > set pandas options
pd.set_option("display.memory_usage", 'deep')
pd.set_option("display.precision", 3)
pd.set_option("styler.format.precision", 3)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.3f}'.format)

def _main():

    args = _parse_args()
    meta_info_path = AM_DF_DIR.joinpath(
        f'meta-info/AM_meta-info_{args.data_suffix}'.replace('.tsv', f'_min{args.min_freq}x.csv'))
    confirm_dir(meta_info_path.parent)
    if meta_info_path.is_file():
        print(
            f'Association Meta Info found. Loading from {meta_info_path.relative_to(RESULT_DIR)}')
        data = pd.read_csv(meta_info_path)

    else:
        data = designate_data(args)
        data = extend_tables(data, args)

    ex_data = data.filter(like='extra', axis=0)
    if 'frame' not in ex_data.columns:
        ex_data['frame'] = ex_data.index.to_series().apply(
            lambda i: load_from_pickle(
                unit=ex_data.unit[i], pkl_path=ex_data.path[i], extra=True))

    if args.verbose:
        for i, assoc_inquiry in enumerate(ex_data.index):
            idf = ex_data.frame.iat[i]
            print(assoc_inquiry)
            print_ex_assoc(
                idf, ex_data.unit.iat[i],
                sort_by=set_selector_column(
                    idf.columns,
                    ['conservative_log_ratio', 'am_p1_given2', 'conserv_log_r',
                        'am_odds_ratio_disc', 'odds_r_disc'])
            )

    if args.skew:

        get_skews(ex_data, args.verbose)

    save_table(data.filter(regex=r'^[^f]'),
               meta_info_path,
               df_name=f"Association Meta Info for {args.data_suffix.split('.tsv')[0]} & displayed joint f >={args.min_freq}"
               )


def _parse_args():
    base_freq_tsv_name = 'AdvAdj_frq-thrMIN-7.35f.tsv'
    _default_comps = (
        FREQ_DIR
        / 'RBdirect'
        / 'complement'
        / 'ucs_format'
        # / f'diff_all-RBdirect_adj-x-adv_frq-thr{_DEFAULT_FRQ_PRCNT}.{_DEFAULT_CORP_PARTS}f={_DEFAULT_FRQ_COUNT}+.tsv'
        / f'diff_all-RBdirect_{base_freq_tsv_name}'
    )
    # results/freq_out/RBdirect/complement/ucs_format/diff_all-RBdirect_adj-x-adv_frq-thr0-001p.35f=868+.tsv
    # results/freq_out/RBdirect/ucs_format/all-frq_adj-x-adv_thr0-001p.35f.tsv
    _default_negs = (
        FREQ_DIR
        .joinpath('RBdirect/ucs_format')
        # .joinpath(f'ALL-WORDS_adj-x-adv_thr{_DEFAULT_FRQ_PRCNT}.{_DEFAULT_CORP_PARTS}f.tsv')
        .joinpath(base_freq_tsv_name)
        # .joinpath(f'all-frq_adj-x-adv_thr{_frq_prcnt}.{_n_corp_parts}f.tsv')
    )

    _default_output_suffix = f'.{_DEFAULT_CORP_PARTS}f-{_DEFAULT_FRQ_COUNT}c.tsv'
    _default_all = (
        FREQ_DIR
        .joinpath('RBXadj/ucs_format')
        # .joinpath(f'all_adj-x-adv_frq-thr{_DEFAULT_FRQ_PRCNT}'
        #           f'.{_DEFAULT_CORP_PARTS}f={_DEFAULT_FRQ_COUNT}+.tsv'
        #           #   + _default_suff
        #           )
        .joinpath(base_freq_tsv_name)
    )

    # > set help messages
    min_freq_help = (
        "Minimum frequency of co-occurrences included as rows "
        "(everything is still included in the marginal frequencies) in association tables"
    )
    comparison_counts_help = (
        "Path to ucs-formatted .tsv of COMPARISON bigram frequencies; e.g. "
        "counts for bigram tokens with no *identified* negation dependencies. "
        "(An approximation of bigrams occurring in 'positive polarity' environments.) "
        "The transformed frequency data will be saved as "
        "`polarity_prepped_tsv/[COMP_LABEL]_bigram_[DATA_SUFFIX]`"
    )
    comp_label_help = (
        "Option to set the label for comparison (set difference, not negated, 'positive', etc.) counts. "
        "Used for output path generation."
    )
    target_counts_help = (
        "Path to ucs-formatted .tsv of NEGATED bigram frequencies; i.e. "
        "counts for bigram tokens with *identified* negation dependencies. "
        "(An approximation of bigrams occurring in 'negative polarity' environments.) "
        "The transformed frequency data will be saved as "
        "`polarity_prepped_tsv/[NEG_LABEL]_bigram_[DATA_SUFFIX]`"
    )
    target_label_help = (
        "Option to set the label for target counts; "
        "Used to generate output path(s) and set the `l1` values for contained `l2` values."
    )
    data_suffix_help = (
        "Option to indicate specific starting data set "
        "as restricted by number of corpus parts/files "
        "and frequency threshold"
    )

    parser = argparse.ArgumentParser(
        description=(
            "Script to add extra association measures to perl script UCS tables "
            "for environement co-occurence frequencies for (1) bigrams, (2) adverbs, "
            "and (3) adjectives, each as a separate table. "
            "If tables have not been previously run, they will be generated, "
            "given the minimum frequency parameter and input paths. "
            "The only pre-requisites are the 'negated' and 'not negated' (i.e. complement) "
            "frequency data, in ucs formatted `.tsv` files. "
            "(To create these, use `sanpi/script/format_for_UCS.py`)"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-m', '--min_freq', type=int,
        # MARK: min_freq default
        default=_DEFAULT_UCS_MIN, help=min_freq_help)
    parser.add_argument(
        '-a', '--all_counts', type=Path,
        default=_default_all,
        help='path to ucs formatted .tsv of all bigram combinations, regardless of polarity')
    parser.add_argument(
        '-c', '--compare_counts', type=Path,
        default=_default_comps, help=comparison_counts_help)
    parser.add_argument(
        '-C', '--comp_label', type=str,
        default='complement', help=comp_label_help)
    parser.add_argument(
        '-n', '--target_counts', type=Path,
        default=_default_negs, help=target_counts_help)
    parser.add_argument(
        '-N', '--targ_label', type=str,
        default='negated', help=target_label_help)
    parser.add_argument(
        '-s', '--data_suffix', type=str,
        default=_default_output_suffix, help=data_suffix_help)

    parser.add_argument(
        '-S', '--skew', default=False, action='store_true',
        help='Option to collect skewed lexemes for selected association metrics.')
    parser.add_argument(
        '-v', '--verbose', default=False, action='store_true',
        help='Option to print more processing info to stdout')
    args = parser.parse_args()
    # // # ! Warning: if the above order changes, `utils.associate.BINARY_ASSOC_ARGS` must be updated as well,
    # // # !   or the following assignments will be messed up.
    # // args_tuple = BINARY_ASSOC_ARGS._make(args.__dict__.values())
    # Explicit assignement is safer 🦺
    return BINARY_ASSOC_ARGS(min_freq=int(str(args.min_freq).strip()),
                             all_counts=Path(str(args.all_counts).strip()),
                             compare_counts=Path(
                                 str(args.compare_counts).strip()),
                             comp_label=str(args.comp_label).strip(),
                             target_counts=Path(
                                 str(args.target_counts).strip()),
                             targ_label=str(args.targ_label).strip(),
                             data_suffix=str(args.data_suffix).strip(),
                             skew=args.skew,
                             verbose=args.verbose
                             )


def designate_data(args):

    def display_init_info(data, n: int = None):

        def show_nlargest_selection(source_df, n, selector, count_type, total_tokens, title: str = None):
            str_N = str_N = f' ({total_tokens:,.0f} total tokens)'
            title = (
                title or f'\n### Top {n} {count_type.upper()} `{selector}` overall\n') + f'\n{str_N}\n'
            selection = source_df.nlargest(n, columns=selector)
            print_md_table(selection,
                           title=title, n_dec=2)

        print_md_table(data.copy().filter(
            items=['key', 'unit', 'stage', 'path']
        ).astype('str'), title='\n## Starting Data Specs\n',
            format='grid')
        for ix in data.index:
            df = data.frame[ix]
            count_type = data.unit[ix]
            n = n or (12 if count_type in ['adv', 'adj'] else 6)
            int_N = df.N.iat[0]
            # > filter to only columns with name starting with `[!r]`
            # >     i.e. not starting with "r_" (so no "ranks")
            # >     ! `?` required in order to allow single character columns, `"f"` and `"N"`
            print_df = df.copy().filter(regex=r'^[^r][^_]?')
            print_df.columns = adjust_am_names(print_df.columns)

            visible_order = ['key',
                             'f', 'expected_f', 'expect_diff',
                             'f_sqrt', 'expected_sqrt',
                             'unexpected_ratio',
                             'odds_r_disc', 'p1_given2', 'p2_given1', 'joint_p', 'conserv_log_r',
                             'l1', 'f1', 'f1_sqrt',
                             'l2', 'f2', 'f2_sqrt']
            print_df = print_df[[
                c for c in visible_order
                if c in print_df.columns][:12]]
            print_df.update(print_df.select_dtypes(include='float').round(2))

            for selector_list in ([],  # raw joint frequency
                                  # conservative log ratio
                                  ['conserv_log_r', 'odds_r_disc'],
                                  # adjusted conditional probability -- `p1_given2`
                                  ['p1_given2', 'odds_r_disc']):
                selector = set_selector_column(
                    print_df.columns, selector_list)
                show_nlargest_selection(
                    print_df, n, selector, count_type, int_N)

            # * Top `NEGATED` values
            if not print_df.filter(like='NEG', axis=0).empty:

                selector = set_selector_column(print_df.columns,
                                               ['p1_given2', 'conserv_log_r', 'odds_r_disc'])
                show_nlargest_selection(
                    print_df.filter(like='NEG', axis=0),
                    n, selector, count_type, int_N,
                    title=f'\n### Top {n} {count_type.upper()} `{selector}` with __negative__ polarity\n')
            # print_example(df, count_type)

    data = pd.DataFrame(
        gen_init_ucs_tables(args),
        columns=['unit', 'stage', 'path', 'frame'])
    data['key'] = data.unit + '_' + data.stage
    data = data.set_index('key')
    if args.verbose:
        display_init_info(data)
    return data


def gen_init_ucs_tables(args):
    """
    Generate initial UCS tables for comparison based on the provided arguments.

    Args:
        args: The arguments used to generate the UCS tables.

    Returns:
        tuple: A tuple containing information about the generated UCS tables.
    """

    def _prepare_data(args):
        comp_path = args.compare_counts
        # > if `args.compare_counts` relative to `*mirror/complement/`
        # >     comparison is between `{POS,NEG}mirror` and non-`{POS,NEG}mirror`
        # >     not approximation of polarity environments.
        #       i.e. one of the following
        #       (1) `set_diff`:
        #           RBdirect/ucs_format/*.tsv ~VS~ RBdirect/complement/ucs_format/*.tsv
        #       (2) `mirror`:
        #           NEGmirror/ucs_format/*.tsv ~VS~ POSmirror/ucs_format/*.tsv
        polarity_approx = 'mirror/complement' not in str(comp_path)
        print('Comparing:',
              f'* target set = {args.target_counts.relative_to(FREQ_DIR)}',
              '   ~vs~',
              f'* comparison = {comp_path.relative_to(FREQ_DIR)}',
              '....................',
              sep='\n')
        units = COMPARISON_UNITS or ('', 'bigram', 'adv', 'adj')
        for i, unit in enumerate(units, start=1):
            print(f'{i}. {unit or "adv ~ adj"} table')
            csv_path = get_associations_csv(
                unit, args, is_polar=polarity_approx)
            print(f'  * csv = `{csv_path.relative_to(RESULT_DIR)}`\n')
            yield unit, csv_path

    csv_paths = pd.Series(dict(_prepare_data(args)))

    if args.verbose:
        print_md_table(csv_paths.apply(lambda p: p.relative_to(RESULT_DIR))
                       .to_frame('`ucs` scores'),
                       format='grid',
                       title=f"UCS Paths relative to `{RESULT_DIR}/`")

    def _load_assoc_data(csv_path: Path, unit: str = ''):

        df = None
        # > added_measures=False by default
        df_init_path = get_am_df_path(input_path=csv_path)
        df_extra_path = get_am_df_path(
            input_path=csv_path, added_measures=True)
        stage = 'initial'

        if df_extra_path.exists():
            if df_extra_path.is_dir() and df_extra_path.suffix.startswith('.parq'):
                df = pd.read_parquet(df_extra_path, engine='pyarrow')
            else:
                df = load_from_pickle(unit, df_extra_path, extra=True)
            df_path = df_extra_path
            stage = 'extra'
        else:
            if df_init_path.is_file():
                df = load_from_pickle(unit, df_init_path)
            elif df_init_path.is_dir() and df_init_path.suffix.startswith('.par'):
                print(
                    f'Loading from parquet: "{df_init_path.relative_to(RESULT_DIR)}"... ⏳')
                df = pd.read_parquet(df_init_path, engine='pyarrow')
            else:
                df = load_from_csv(csv_path)

            df_path = df_init_path

        df = handle_word_null(df, csv_path)

        # HACK trying to figure out what's going on with the non-zero decimals for `f` for `most_important`
        # cols_regex = r'^[fOE]|l\d|^observed_f'
        # rows_regex = r'^[A-Z~\w]+.important$'
        # print(df.filter(regex=rows_regex, axis=0).filter(regex=cols_regex))
        # print()
        # print_md_table(df.filter(regex=rows_regex, axis=0).filter(regex=cols_regex))
        # print_md_table(df.filter(regex=rows_regex, axis=0).filter(regex=cols_regex), n_dec=2)
        if not df.index.name:

            df = set_data_keys(df)

            # print('<<< Optimizing frame >>>')
            # opt_df = _optimize(df, verbose=True)
            # print(opt_df.filter(regex=rows_regex, axis=0).filter(regex=cols_regex))
            # print()
            # print_md_table(opt_df.filter(regex=rows_regex, axis=0).filter(regex=cols_regex).sample(10))
            # print_md_table(opt_df.filter(regex=rows_regex, axis=0).filter(regex=cols_regex).sample(10), n_dec=2)

            _save_am_dataframe(df_path, _optimize(df), force=True)

        return df, df_path, stage

    for unit in csv_paths.index:
        df, df_path, stage = _load_assoc_data(
            csv_path=csv_paths[unit], unit=unit)
        if not df_path.exists():
            # > save initial dataframe conversions as optimized parquet
            _save_optimized(df, df_path)
        if not unit:
            unit = 'adv~adj'
        yield unit, stage, df_path, df


def load_from_pickle(unit: str,
                     pkl_path: Path,
                     extra: bool = False):
    _extra = "_extra" if extra else ""
    print(f'\n> Loading `{unit}` data',
          f'from *{_extra}.pkl.gz: {pkl_path.relative_to(RESULT_DIR)}')
    return pd.read_pickle(pkl_path)


def handle_word_null(df, csv_path):
    """
    Handles null values in the DataFrame by converting them to the string "null" if present.

    Args:
        df: The DataFrame to handle null values in.
        csv_path: The path to the CSV file for potential data reversion.

    Returns:
        pd.DataFrame: The DataFrame with null values handled appropriately.
    """
    #! This is necessary because the adjective "null" gets read by pandas as `<NA>`.
    #! Must be manually reset to the string `"null"`
    if any(df.l1.isna() | df.l2.isna()):
        df[['l1', 'l2']] = df[['l1', 'l2']].astype('string')
        df.loc[df.l2.isna(), 'l2'] = 'null'
        df.loc[df.l1.isna(), 'l1'] = 'null'
        if any(df.l1.isna() | df.l2.isna()):
            print('⚠️   Error! Undefined values! Reverting to csv data')
            df = load_from_csv(csv_path)
            if any(df.l1.isna() | df.l2.isna()):
                print(df.head())
                print(df.tail())
                print_md_table(df.loc[df.index.isna() | df.l2.isna(
                ), df.columns[:8]], title='\n### ❗ Problem "Null" Entries')
                exit(f'⚠️   Error! Undefined values in csv data as well. '
                     'Inspect source:\n  > {csv_path}\n'
                     'Quitting.')
    return df


def set_data_keys(df):
    """
    Sets data keys for the DataFrame index based on the values in columns l1 and l2.

    Args:
        df: The DataFrame for which data keys are being set.

    Returns:
        pd.DataFrame: The DataFrame with data keys set as the index.
    """

    print('> + Creating data keys for index')

    unique_l1 = df.l1.nunique()

    def _make_keys(l1: pd.Series, l2: pd.Series, key_len: int):
        return l1.apply(lambda x: x[:key_len]).astype('string') + '~' + l2

    if unique_l1 < 40:
        key_len = 3
        keys = _make_keys(df.l1, df.l2, key_len)
        # while keys.str.split('-').str.get(0).nunique() < unique_l1:
        while any(keys.duplicated()):
            key_len += 1
            keys = _make_keys(df.l1, df.l2, key_len)
    else:
        keys = (df.l1.astype('string') +
                '~' + df.l2.astype('string'))

    df['key'] = keys

    return df.reset_index().set_index('key')


def extend_tables(data, args):
    """
    Extends tables in the provided data to include additional association metric columns if necessary.

    Args:
        data: The data containing tables to be extended.
        args: The arguments used for extension.

    Returns:
        pd.DataFrame: The updated data with tables extended as needed.
    """

    # > if any dataframes have not been extended to include additional columns
    if (any(data.stage == 'initial')
        # > for every mentioned unit, there must be an "extra" table
        #   if there are _no_ "extra" entries
        and ('extra' not in data.stage
             # or there are fewer "extra" entries than there are unique units
             or data.stage.count('extra') < data.unit.nunique())):

        vocab_size_dict = get_vocab_size(args.all_counts)
        # > do so now
        data = _extend_assoc_data(
            data, verbose=args.verbose, vocab_size=vocab_size_dict)
        data.loc[data.stage == 'extra', :].index.to_series().apply(
            lambda k:
                # `data.frame` objects are optimized in `_extend_assoc_data`
                _save_am_dataframe(
                    out_path=data.path[k],
                    _df=data.frame[k])
        )
    return data


def _extend_assoc_data(data: pd.DataFrame,
                       verbose: bool = False,
                       vocab_size: int = None,

                       stage_name: str = 'extra'):
    """
    Extends the association data by adding additional entries for a specified stage.

    Args:
        data (pd.DataFrame): The original data to be extended.
        verbose (bool, optional): Whether to display verbose output. Defaults to False.
        vocab_size (int, optional): The vocabulary size. Defaults to None.
        stage_name (str, optional): The name of the stage for extension. Defaults to 'extra'.

    Returns:
        pd.DataFrame: The extended data with additional entries for the specified stage.
    """

    init_data = data.copy().loc[data.stage != stage_name]
    
    new_extend = process_extensions(
        init_data, stage_name, verbose, vocab_size)

    extended = pd.concat([data.loc[data.stage == stage_name], new_extend])
    if (f'bigram_{stage_name}' in extended.index
            and any(adx_col not in
                    extended.at[f'bigram_{stage_name}', 'frame'].columns
                    for adx_col in ['adv', 'adj', 'adv_total', 'adj_total'])
            ):

        if all(adx in extended.unit.unique() for adx in ('adv', 'adj', 'bigram')):

            def add_adx_info(_data: pd.DataFrame,
                             verbose: bool = False) -> pd.DataFrame:

                def get_adx_totals(adx_df: pd.DataFrame, adx: str) -> pd.Series:
                    return pd.to_numeric(
                        adx_df[['l2', 'f2']]
                        .drop_duplicates()
                        .rename(columns={'l2': adx, 'f2': f'{adx}_total'})
                        .set_index(adx).squeeze(),
                        downcast='integer')
                adv_totals, adj_totals = [
                    get_adx_totals(
                        _data.frame[f'{x}_extra'].filter(regex=r'^[fl]'), adx=x)
                    for x in ('adv', 'adj')]
                # TODO? add ad* joint f as well as total
                # def get_adx_polar_f(adx_df: pd.DataFrame, adx: str) -> pd.Series:
                #     adx_df = adx_df.copy()[['l1', 'l2', 'f']]
                #     pass
                #
                # adv_polar, adj_polar = [
                #     get_adx_polar_f(_data.frame[f'{x}_extra'].filter(regex=r'^[fl]'), adx=x)
                #     for x in ('adv', 'adj')]
                bigram_df = _data.frame['bigram_extra'].copy()
                bigram_df[['adv', 'adj']] = bigram_df.l2.str.split(
                    "_", expand=True).astype('string').astype('category')

                bigram_df['adv_total'] = bigram_df.adv.map(adv_totals)
                bigram_df['adj_total'] = bigram_df.adj.map(adj_totals)
                if verbose:
                    print_md_table(
                        pd.concat([bigram_df.filter(regex=r'^ad[vj]|^(f|l1)$').filter(
                            like=e[:2], axis=0).sample(3) for e in bigram_df.l1.unique()]),
                        title='\n Sample (6) of lexical columns added to `bigram_extra` table\n')
                return bigram_df

            extended.at[f'bigram_{stage_name}',
                        'frame'] = _optimize(
                            add_adx_info(
                                extended.copy()))
        else:
            raise Warning(
                'Frequency info for adverbs and adjectives not added to polar bigram table')

    return pd.concat([init_data, extended])


def process_extensions(init_data: pd.DataFrame,
                       stage_name: str = 'extra',
                       verbose: bool = False,
                       vocab_size_dict: dict = None,
                       ):
    """
    Processes extensions for the initial data by creating new entries with additional measures.

    Args:
        init_data (pd.DataFrame): The initial data to be extended.
        stage_name (str, optional): The name of the stage for the extensions. Defaults to 'extra'.
        verbose (bool, optional): Whether to display verbose output. Defaults to False.
        vocab_size_dict (dict, optional): A dictionary containing vocabulary sizes. Defaults to None.

    Returns:
        pd.DataFrame: The updated data with new entries containing additional measures.
    """

    # Copy, reassign 'stage', and update index
    data_update = init_data.copy().assign(stage=stage_name)
    data_update.index = data_update['unit'] + f'_{stage_name}'
    data_update.index.name = 'key'  # just in case

    # Define operations for 'path' and 'frame'
    def get_path(row):
        return get_am_df_path(row['path'], added_measures=True)

    def get_frame(data_row):
        xdf = beef_up_dtypes(data_row['frame'])

        extended_df = add_extra_am(xdf,
                                   verbose=verbose,
                                   vocab=vocab_size_dict[data_row['unit']])
        return _optimize(extended_df)

    # Apply operations
    data_update['path'] = data_update.apply(get_path, axis=1)
    data_update['frame'] = data_update.apply(get_frame, axis=1)
    return data_update


def set_selector_column(df_columns: pd.Index,
                        ranked_options: list = None) -> str:
    """
    Sets the selector column based on the provided DataFrame columns and ranked options.

    Args:
        df_columns (pd.Index): The columns of the DataFrame to select from.
        ranked_options (list, optional): The ranked options for column selection. Defaults to None.

    Returns:
        str: The selected column based on the ranked options or fallback columns.
    """

    if ranked_options is None:
        ranked_options = []
    fallback = ['observed_f', 'f', 'f_sqrt',
                'f2', 'z_score', 'expected_f', 'E11']
    ranked_options = ranked_options or fallback
    c = None
    for c in ranked_options:
        if c in df_columns:
            return c
    if not c:
        excluded = ('l1', 'l2', 'adv', 'adj', 'bigram', 'key', 'index')
        print(
            f'‼ Warning! None of {ranked_options} in data. Defaulting to fallback columns or first numerical column.')
        return next(
            (c
                for c in fallback
                + df_columns[~df_columns.isin(excluded)].to_list()
                if c in df_columns
             ),
            [0],
        )


def _save_optimized(_df: pd.DataFrame,
                    path: Path,
                    added_measures: bool = False,
                    verbose: bool = False):

    out_path = get_am_df_path(path, added_measures)
    _save_am_dataframe(out_path, _optimize(_df, verbose))
    return out_path


def _optimize(df: pd.DataFrame,
              verbose: bool = False) -> pd.DataFrame:
    # _df = df.copy()

    # def _show_memory_usage(arg0, arg1):
    #     print(arg0)
    #     arg1.info(memory_usage='deep')
    #     print()

    # if verbose:
    #     _show_memory_usage('>> Unoptimized <<', df)

    # str_cols = _df.select_dtypes(exclude='number').columns.to_list()
    # _df[str_cols] = _df[str_cols].astype('string')
    # count_cols = _df.columns[_df.columns.str.startswith(
    #     ('r_', 'C', 'R', 'N', 'f', 'index'))].to_list()
    # is_float = ~_df.columns.isin(count_cols + str_cols)
    # _df[count_cols] = _df[count_cols].apply(pd.to_numeric, downcast='integer')
    # _df[_df.columns[is_float]] = _df[_df.columns[is_float]].apply(
    #     pd.to_numeric, downcast='float')
    # _df[str_cols] = _df[str_cols].apply(
    #     lambda c: c.astype('category')
    #     if c.nunique() <= (len(_df) // 3)
    #     else c)

    # if not all(_df.astype('string') == df.astype('string')):
    #     # ! make sure the values have not changed!
    #     raise ValueError(
    #         'DataFrame optimization failed: Values have been changed in the process.')

    # if verbose:
    #     _show_memory_usage('\n--------\n>> Optimized DataFrame', _df)
    #     mem = df.memory_usage('deep').to_frame('init').join(
    #         _df.memory_usage('deep').to_frame('adjust'))
    #     print(tabulate(mem.assign(REDUCTION=mem.iloc[:, 0].subtract(mem.iloc[:, 1])), floatfmt=',.0f', tablefmt='rounded_grid', headers=[
    #           'Memory Usage:', '...Initial', '...Adjusted', '*reduction*']))
    #     print('\n\n============\n\n')
    # pd.set_option("display.float_format", '{:,.3f}'.format)
    
    return df.convert_dtypes()


def load_from_csv(csv_path):
    print(f'\n> Loading from *.csv: {csv_path.relative_to(UCS_DIR)}')
    return pd.read_csv(csv_path)


def get_am_df_path(input_path: Path | str,
                   added_measures: bool = False,
                   metric_name: str = None):
    """
    Determines the path for the DataFrame based on the input path and additional measures flag.

    Args:
        input_path (Path or str): The input path for the DataFrame.
        added_measures (bool, optional): Flag indicating if additional measures are included. Defaults to False.
        metric_name (str, optional): The name of the metric. Defaults to None.

    Returns:
        Path: The path for the DataFrame based on the input and settings.
    """

    input_path = Path(input_path)
    input_dir = input_path.parent
    input_dir_nesting = (input_dir.relative_to(UCS_DIR)
                         if input_dir.is_relative_to(UCS_DIR)
                         else input_dir.relative_to(RESULT_DIR))
    # e.g. for `ucs/polar/RBdirect/bigram/readable/*`,
    #       nesting == `polar/RBdirect/bigram/readable`
    #       change to --> `polar/RBdirect/bigram`
    if input_dir_nesting.name == 'readable':
        input_dir_nesting = input_dir_nesting.parent

    # append `assoc_df` to directory path if nesting does not already include it
    out_dir = (AM_DF_DIR
               if AM_DF_DIR.name not in input_dir_nesting.parts
               else RESULT_DIR)

    out_dir = out_dir.joinpath(input_dir_nesting)
    confirm_dir(out_dir)
    #! manually set stem, bc `.stem` attribute yields "STEM.pkl" for "STEM.pkl.gz" paths
    output_stem = (
        input_path.name.replace('.csv', '').replace(
            PKL_SUFF, '').replace('.parq', '')
        .replace(READ_TAG, '').strip('.'))

    if 'SKEW' in output_stem.upper():
        out_dir = out_dir / 'skewed'
        if metric_name:
            out_dir = out_dir / metric_name
        out_dir = out_dir / re.search(r'min\d+x', output_stem).group()

    elif added_measures:
        out_dir = out_dir / 'extra'
        output_stem += '_extra'
    confirm_dir(out_dir)
    # return out_dir.joinpath(output_stem + PKL_SUFF)
    return out_dir.joinpath(output_stem + '.parq')

# def downcast_number(numerical: pd.Series, n_dec: int = 5,
#                     downcast: str = 'float'):
#     n_dec = n_dec if downcast == 'float' else 0
#     return pd.to_numeric(numerical.apply(np.around, decimals=n_dec), downcast=downcast)


def _save_am_dataframe(out_path: Path,
                       _df: pd.DataFrame,
                       force: bool = False):

    def _write_df(out_path: Path, _df):
        csv_too = ''
        out_dir = out_path.parent
        as_pickle = False
        confirm_dir(out_dir)
        if '.pkl' in out_path.suffixes:
            as_pickle = True
            _df.to_pickle(out_path)
        elif out_path.suffix.startswith('.par'):
            if 'polar' in out_path.parts:

                partition_by = ['l1']

            else:
                partition_by = ['first_char']
                _df['first_char'] = _df['l1'].str[0].astype(
                    'string').astype('category')
            _df.to_parquet(str(out_path),
                           engine='pyarrow',
                           use_threads=True,
                           partition_cols=partition_by,
                           basename_template='group-{i}.parquet',
                           existing_data_behavior='delete_matching',
                           row_group_size=5000,
                           max_rows_per_file=10000,
                           )
        if len(_df) <= 5000 and _df.size <= 250000:
            csv_too = " (+ `.csv`)"
            _df.to_csv(str(out_path).replace(PKL_SUFF, '.csv')
                       if as_pickle
                       else out_path.with_suffix('.csv'))
        print(
            f'* Dataframe saved: `{out_path.relative_to(RESULT_DIR)}`{csv_too}')

    if _df.empty:
        print(
            f'* ‼️ Dataframe designated for {out_path.relative_to(UCS_DIR)} is empty 🪹. No file created.')
        return
    if out_path.is_file():
        if force:
            print('* Force applied!',
                  f'  Existing `{out_path.relative_to(UCS_DIR)}` will be overwritten.',
                  sep='\n  ')
        else:
            print('* Dataframe already saved:',
                  f'`{out_path.relative_to(SANPI_HOME)}` ',
                  '(not overwritten)',
                  sep='\n  ')
            return

    _write_df(out_path, _df)


def print_ex_assoc(df: pd.DataFrame,
                   count_type: str = None,
                   example_key: str = None,
                   round_level: int = 2,
                   sort_by: str = 'am_p1_given2',
                   columns_like=r'^([^ECORr_]|E11)',
                   max_examples: int = 8,
                   regex=False) -> None:
    """
    Prints examples of associated words from a DataFrame based on specified criteria.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        count_type (str, optional): The type of count to use for selecting examples. Defaults to None.
        example_key (str, optional): The key to use for selecting examples. Defaults to None.
        round_level (int, optional): The level of rounding to apply. Defaults to 2.
        sort_by (str, optional): The column to sort the examples by. Defaults to 'am_p1_given2'.
        columns_like: (str, optional): Regular expression pattern to match column names. Defaults to r'^([^ECORr_]|E11)'.
        max_examples (int, optional): The maximum number of examples to display. Defaults to 8.
        regex (bool, optional): Whether to use regex pattern matching. Defaults to False.

    Returns:
        None

    Examples:
        print_ex_assoc(df, count_type='bigram', example_key='that_', round_level=2, sort_by='am_p1_given2', columns_like=r'^([^ECORr_]|E11)', max_examples=8, regex=False)
    """

    if not example_key:
        example_keys = {'bigram': 'that_',
                        'adv': 'exactly',
                        'adj': 'better',
                        'adv~adj': 'slightly',
                        '': 'slightly'}
        example_key = example_keys[count_type]
    if regex:
        example = df.round(round_level).filter(axis=0, regex=example_key)
    else:
        example = df.round(round_level).filter(axis=0, like=example_key)
    if sort_by not in example.columns:
        sort_by = example.columns.iloc[0]
    example = example.sort_values(
        sort_by, ascending=sort_by.startswith(('r_', 'l')))
    example = example.filter(regex=columns_like).sort_index(
        axis=1).head(max_examples)
    if example.empty:
        print(f'🤷 No {count_type} match {example_key}')
    else:
        transpose = example.shape[0] < example.shape[1] * .75
        print_md_table(
            example.select_dtypes(include='number'),
            transpose=transpose, n_dec=round_level,
            title=f'\n### {count_type.capitalize()} "{example_key}" examples sorted by `{sort_by}` column\n')
    print('\n---')


def get_skews(data: pd.DataFrame, verbose: bool = False):
    """
    Gets skews for the provided data by filtering based on different metrics.

    Args:
        data (pd.DataFrame): The data to calculate skews for.
        verbose (bool, optional): Whether to display verbose output. Defaults to False.
    """

    exd = (data.copy()
           .assign(metric='am_p1_given2',
                   floor=-1*RATIO_CEIL,
                   ceiling=RATIO_CEIL,
                   stage='skewed'))
    adv_adj_row = exd.filter(like='adv~adj', axis=0)
    additional_metrics = ['deltaP_min', 'deltaP_max', 'deltaP_product', 'am_p2_given1',
                          'unexpected_ratio', 'am_odds_ratio_disc', 'log_likelihood']
    skews = pd.concat([exd,
                       exd.copy().assign(metric='conservative_log_ratio')]
                      + [adv_adj_row.copy().assign(metric=m) for m
                         in additional_metrics]).reset_index()
    skews['key'] = skews.unit + '_' + skews.stage + '-' + skews.metric
    skews = skews.set_index('key').rename(columns={'frame': 'ex_frame'})

    skews = _set_outlier_margins(skews, verbose=verbose)

    skews['path'] = skews.apply(_set_skew_path, axis='columns')

    new_skews = skews.loc[
        skews.path.apply(lambda skew_path: not Path(skew_path).is_file()), :]

    for i in new_skews.index:
        if not new_skews.path[i].is_file():
            id_skewed_combos(
                new_skews.ex_frame[i], metric=new_skews.metric[i],
                floor=new_skews.floor[i], ceiling=new_skews.ceiling[i],
                verbose=verbose, unit=new_skews.unit[i].upper(), out_path=new_skews.path[i])
        else:
            print(
                f'* Skewed Dataframe already exists:\n  * see `{new_skews.path[i].relative_to(RESULT_DIR)}`')

    # if verbose:
    #     # skews.index.to_series().apply(
    #     #     lambda key:
    #     #         print_sorted_md(print_df=skews.frame[key],
    #     #                         unit=skews.unit[key],
    #     #                         metric=skews.metric[key],
    #     #                         floor=skews.floor[key])
    #     # )
    #     print_md_table(new_skews.path.apply(lambda p: str(p.relative_to(
    #         UCS_DIR))).to_frame('saving skew paths...'), title='\n')

    # new_skews.index.to_series().apply(
    #     lambda i: _save_dataframe(new_skews.path[i],
    #                               _optimize(new_skews.frame[i]))
    # )


def _set_outlier_margins(skews: pd.DataFrame,
                         all_metrics: bool = True,
                         margin_factor: float = OUTLIER_MARGIN_IQR_FACTOR,
                         verbose: bool = False
                         ) -> pd.DataFrame:
    """
    Sets outlier margins for the provided DataFrame based on the specified metrics and factors.

    Args:
        skews (pd.DataFrame): The DataFrame containing skew data.
        all_metrics (bool, optional): Whether to consider all metrics for setting outlier margins. Defaults to True.
        margin_factor (float, optional): The factor to determine outlier margins. Defaults to OUTLIER_MARGIN_IQR_FACTOR.
        verbose (bool, optional): Whether to display verbose output. Defaults to False.

    Returns:
        pd.DataFrame: The DataFrame with updated outlier margins set.
    """

    #! technically, outlier margin is defined as 1.5 * the interquartile range,
    #!   but I want something more extreme for these cases, so defaults to 2.
    _metrics = skews.metric.unique()
    print(
        f'--------\n**IQR × {OUTLIER_MARGIN_IQR_FACTOR} to determine limits**\n--------')

    def plot_probabilities(unit, unit_df):
        if '~' not in unit:
            by_env = []
            for e, d in unit_df.groupby('l1'):
                d = d.reset_index().set_index(
                    'l2').filter(regex=r'_p\w+[ye12]$')
                d.columns = d.columns.astype(
                    'string').str.replace('am_', '') + f'_{e[:3]}'
                by_env.append(d)

            probs = by_env[0].join(by_env[1])
        else:
            probs = unit_df.filter(regex=r'_p\w+[ey12]$')
        probs.sort_index(axis=1).plot(kind='box', grid=True, rot=-22.5,
                                      title=f'`{unit}` probability box plots')

    for ix in skews.index:
        _metric = skews.metric[ix]
        unit = skews.unit[ix]
        unit_df = skews.ex_frame[ix]
        if verbose and _metric == 'am_p1_given2':
            plot_probabilities(unit, unit_df)
        _stats = unit_df[_metric].describe()
        if verbose:
            print_md_table(
                _stats.to_frame(
                    f'`{_metric}` descriptive stats for {unit} data'),
                n_dec=4,
                title=f'\nSelecting skew limits for {ix.replace("_skewed-"," set based on `")}`\n')
        if all_metrics or any(abs(m) > 1 for m in _stats[['min', 'max']]):
            iqr = _stats['75%'] - _stats['25%']
            stdev = _stats['std']

            margin = margin_factor * max(iqr, stdev)
            z_above = _stats['mean'] + stdev
            z_below = _stats['mean'] - stdev
            floor = round((min(_stats['25%'], z_below) - margin), 4)
            ceiling = round((max(_stats['75%'], z_above) + margin), 4)

            # > if somehow the outlier boundaries are the same after rounding,
            # > push them out by a quarter of a std
            while round(floor, 2) == round(ceiling, 2):
                quarter_std = _stats.at['std'] / 4
                floor -= quarter_std
                ceiling += quarter_std
            skews.loc[ix, 'floor'] = floor
            skews.loc[ix, 'ceiling'] = ceiling
    if verbose:
        print_md_table(skews[['floor', 'ceiling']], n_dec=4,
                       title=f'\n### Updated Definitions for "Skewed" Values\n')
    return skews


def id_skewed_combos(df: pd.DataFrame,
                     floor: float = -0.8,
                     ceiling: float = 0.8,
                     unit: str = 'bigram',
                     count_cutoff: int = 5,
                     verbose: bool = False,
                     metric: str = 'am_p1_given2',
                     out_path: Path = None):
    """
    Identifies skewed combinations in the provided DataFrame based on specified metrics and thresholds.

    Args:
        df (pd.DataFrame): The DataFrame to identify skewed combinations in.
        floor (float, optional): The lower threshold for skew identification. Defaults to -0.8.
        ceiling (float, optional): The upper threshold for skew identification. Defaults to 0.8.
        unit (str, optional): The unit type for identification. Defaults to 'bigram'.
        count_cutoff (int, optional): The count cutoff for displaying skewed counts. Defaults to 5.
        verbose (bool, optional): Whether to display verbose output. Defaults to False.
        metric (str, optional): The metric used for skew identification. Defaults to 'am_p1_given2'.
        out_path (Path, optional): The output path for saving the identified skewed combinations. Defaults to None.

    Returns:
        pd.DataFrame: The DataFrame containing the identified skewed combinations.
    """
    keep_columns = ['f', 'E11', 'adv', 'adj', 'l1', 'l2', 'unexpected_count', 'z_score',
                    'am_p1_given2', 'am_p2_given1', 'log_likelihood', 'am_odds_ratio_disc',
                    'conservative_log_ratio', 'unexpected_ratio', 'deltaP_min', 'deltaP_max', 'deltaP_product', 'adv_total', 'adj_total']
    if metric not in keep_columns:
        keep_columns.append(metric)

    _df = df.copy().sort_values(metric, ascending=False)
    # _df.update(_df.select_dtypes('float').apply(round, ndigits=4, axis=1))

    # > "skewed" if "under the floor" or "over the ceiling"
    skewed_pairs = _df.loc[(_df[metric] <= floor) |
                           (_df[metric] >= ceiling), :]
    if verbose:
        def print_sorted_md(print_df: pd.DataFrame,
                            sorter: str = None,
                            floor: float = -1 * RATIO_CEIL,
                            ceiling: float = RATIO_CEIL,
                            n_top: int = 10,
                            unit: str = 'bigram',
                            metric: str = 'am_p1_given2',
                            n_dec: int = 2):

            if not sorter:
                sorter = metric
            table_title = (f'\nTop {n_top} `{metric}` skewed {unit.upper()}'
                           f'\n- `f>={print_df.f.min()}`'
                           f'\n- `{metric}: >= {ceiling} | <= {floor}`)'
                           f'\n- sorted by `{sorter}` (rounded to {n_dec})\n')
            _df = print_df.copy().nlargest(
                n_top, columns=[sorter]).reset_index()
            _df.columns = _df.columns.str.replace('am_', '').str.replace(
                'ratio', 'r').str.replace('probability', 'p').str.replace('conservative', 'conserv')
            _df = _df.rename(columns={'O11': 'observed',
                                      'E11': 'expected'})
            _df = _df.filter(regex=r'^[^ar]')
            print_md_table(
                _df, transpose=len(_df.columns) - len(_df) > 2,
                title=table_title, n_dec=n_dec, indent=2)

        def print_skew_percents(skew_df, init_df, metric, ceiling, floor, unit):
            perc_tokens = round(
                100 * skew_df.f.sum() / init_df.N.iat[0], 2)
            try:
                perc_uniq_bigrams = round(init_df.loc[init_df.index.isin(
                    skew_df.index), 'l2'].nunique() / init_df.l2.nunique() * 100, 2)
            except ValueError:
                return
            print(f"\n* Skewed {unit} (`f>={skew_df.f.min()}`; `{metric}: >= {ceiling} | <= {floor}`) account for:",
                  f"  + {perc_tokens}% of all tokens in current dataset",
                  f"  + {perc_uniq_bigrams}% of unique `l2` forms",
                  sep='\n')
        # print_md_table(
        #     input_df=(skewed_pairs.head(n_top).round(2)
        #               .sort_values(['unexpected_ratio', 'unexpected_count'], ascending=False)),
        #     n_dec=2,
        #     title=(f'\n## Top {n_top} '
        #            'bigrams most strongly skewed toward polar environment '
        #            f'(f>={_df.f.min()}; `{floor} >= {metric} >= {ceiling}`)\n'))
        print_sorted_md(skewed_pairs.copy().filter(items=keep_columns), unit=unit,
                        floor=floor, ceiling=ceiling, metric=metric, n_top=30)

        if not skewed_pairs.filter(items=['adv', 'adj']).empty:
            for ad in ['adv', 'adj']:
                neg_skewed = skewed_pairs[ad].astype(
                    'string').value_counts()
                print_md_table(
                    neg_skewed.loc[neg_skewed > count_cutoff].to_frame(
                        'bigram count'),
                    n_dec=2,
                    title=(f'\n### {ad.capitalize()} appearing in more than {count_cutoff} '
                           f'negatively "skewed" {unit} (`{metric}: >= {ceiling} | <= {floor}`)\n'))

                print(f"\n+ mean bigram count for unique {ad} =",
                      round(neg_skewed.filter(regex=r'[a-z]').mean(), 1))

        print_skew_percents(skewed_pairs, df, metric, ceiling, floor, unit)
    skewed_pairs = skewed_pairs.filter(items=keep_columns)
    if out_path:
        _save_am_dataframe(out_path, _optimize(skewed_pairs))
    else:
        return skewed_pairs


def _set_skew_path(row):
    """
    Sets the path for the skew based on the provided row data.

    Args:
        row: The row data containing information for setting the skew path.

    Returns:
        Path: The path for the skew based on the row data.
    """

    margin_flag = f"-x{OUTLIER_MARGIN_IQR_FACTOR}"
    metric_label = snake_to_camel(
        re.sub(r'a(m_|tive|tio)|robability', '', row.at['metric']))
    metric_limit_str = (
        metric_label +
        re.sub(r'0?\.', ',',
               (margin_flag
                + f"_exceed({str(row.at['floor'])[:4]};"
                + f"{str(row.at['ceiling'])[:4]})"))
    )

    full_df_path = row.at['path']
    skew_dir = Path(str(full_df_path.parent).replace('/extra', ''))
    skew_name = full_df_path.name.replace(r'_extra', '').replace(
        PKL_SUFF,
        f"_SKEW{metric_limit_str}{PKL_SUFF}")
    updated_path = skew_dir / skew_name

    return get_am_df_path(updated_path, metric_name=metric_label)


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('* Program Completed ✅',
              f'  * finished @ {pd.Timestamp.now().ctime()}',
              f'  * total time elapsed: {timer.elapsed()}',
              sep='\n')
