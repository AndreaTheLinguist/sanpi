import argparse
from pathlib import Path

import association_measures.binomial as bn
import association_measures.frequencies as fq
import association_measures.measures as am
# import matplotlib.pyplot as plt
import pandas as pd
from utils.associate import _FREQ_DIR, _POL_DIR, _RSLT_DIR
from utils.associate import _SANPI_HOME as SANPI_DIR
from utils.associate import _UCS_DIR, build_ucs_from_multiple, build_ucs_table
from utils.associate import convert_ucs_to_csv as txt_to_csv
from utils.associate import prep_by_polarity as polarize_counts
from utils.dataframes import Timer, print_md_table, set_pd_display
from utils.general import confirm_dir, run_shell_command

READ_TAG = 'rsort-view'


def _parse_args():
    # > set defaults
    _n_corp_parts = 35
    _frq_cnt = 868
    _frq_prcnt = '0-001'

    _default_comps = (
        _FREQ_DIR
        / 'diff_RBXadj-RBdirect'
        / 'ucs_format'
        / f'diff-all_adj-x-adv_frq-thr{_frq_prcnt}p.{_n_corp_parts}f={_frq_cnt}+.tsv'
    )
    # results/freq_out/RBdirect/ucs_format/all-frq_adj-x-adv_thr0-001p.35f.tsv
    _default_negs = (
        _FREQ_DIR
        .joinpath('RBdirect/ucs_format')
        .joinpath(f'all-frq_adj-x-adv_thr{_frq_prcnt}p.{_n_corp_parts}f.tsv')
    )

    _default_all = (
        _FREQ_DIR
        .joinpath('RBXadj/ucs_format')
        .joinpath(f'all_adj-x-adv_frq-thr{_frq_prcnt}p.{_n_corp_parts}f={_frq_cnt}+.tsv'))
    _default_suff = f'.{_n_corp_parts}f={_frq_cnt}+.tsv'

    # > set help messages
    min_freq_help = (
        "Minimum frequency of co-occurrences included as rows "
        "(everything is still included in the marginal frequencies) in association tables"
    )
    complement_counts_help = (
        "Path to ucs-formatted .tsv of COMPLEMENT bigram frequencies; i.e. "
        "counts for bigram tokens with no *identified* negation dependencies. "
        "(An approximation of bigrams occurring in 'positive polarity' environments.) "
        "The transformed frequency data will be saved as "
        "`polarity_prepped/[COMP_LABEL]_bigram_counts[DATA_SUFFIX]`"
    )
    comp_label_help = (
        "Option to set the label for complement (set difference, not negated, 'positive', etc.) counts. "
        "Used for output path generation."
    )
    negated_counts_help = (
        "Path to ucs-formatted .tsv of NEGATED bigram frequencies; i.e. "
        "counts for bigram tokens with *identified* negation dependencies. "
        "(An approximation of bigrams occurring in 'negative polarity' environments.) "
        "The transformed frequency data will be saved as "
        "`polarity_prepped/[NEG_LABEL]_bigram_counts[DATA_SUFFIX]`"
    )
    neg_label_help = (
        "Option to set the label for negated (or matching specific pattern) counts. "
        "Used for output path generation."
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
        default=15, help=min_freq_help)
    parser.add_argument(
        '-a', '--all_counts', type=Path,
        default=_default_all,
        help='path to ucs formatted .tsv of all bigram combinations, regardless of polarity')
    parser.add_argument(
        '-c', '--complement_counts', type=Path,
        default=_default_comps, help=complement_counts_help)
    parser.add_argument(
        '-C', '--comp_label', type=str,
        default='complement', help=comp_label_help)
    parser.add_argument(
        '-n', '--negated_counts', type=Path,
        default=_default_negs, help=negated_counts_help)
    parser.add_argument(
        '-N', '--neg_label', type=str,
        default='negated', help=neg_label_help)
    parser.add_argument(
        '-s', '--data_suffix', type=str,
        default=_default_suff, help=data_suffix_help)

    parser.add_argument(
        '-v', '--verbose', default=False, action='store_true',
        help='Option to print more processing info to stdout')

    return parser.parse_args()


def print_sorted_md(skewed_bigrams, sorter, floor, n_top=20):
    table_title = (f'\n### Top {n_top} Bigrams with env polarity association '
                   f'> {floor}, sorted by `{sorter}`')

    print_md_table(
        skewed_bigrams.copy().sort_values(
            sorter, ascending=False).head(n_top).reset_index(),
        title=table_title, n_dec=2, comma=False)


def add_adx_info(df_dict):
    adv_totals, adj_totals = [get_adx_totals(
        df_dict=df_dict, adx=x) for x in ('adv', 'adj')]
    
    bigram_df = df_dict['bigram']
    bigram_df[['adv', 'adj']] = bigram_df.l2.str.split(
        "_", expand=True).astype('string').astype('category')

    bigram_df['adv_total'] = bigram_df.adv.map(adv_totals)
    bigram_df['adj_total'] = bigram_df.adj.map(adj_totals)
    
    return bigram_df


def display_init_info(counts_by_type_dict):
    for count_type, df in counts_by_type_dict.items():
        n = 5 if count_type == 'bigram' else 8

        # * Top Values based on adjusted conditional probability
        # >      of environment (`l1`) given bigram (`l2`): `p1.given2`
        print_md_table(df=df.filter(regex=r'^[Eaf]').head(n),
                       title=f'\n### Top {n} {count_type.upper()} Associations Overall\n',
                       transpose=True, n_dec=2, comma=True)

        # * Top `NEGATED` values
        n = 5 if count_type == 'bigram' else 8
        print_md_table(df=df.filter(like='NEG', axis=0).filter(regex=r'^[Eaf]').head(n),
                       title=f'\n### Top {n} {count_type.upper()} most likely to be **negated**\n',
                       transpose=True, n_dec=2, comma=True)

        print_example(df, count_type)
    return df, count_type


def get_init_ucs_tables(args):

    csv_paths = pd.Series(dict(_pull_data(args)))

    if args.verbose:
        print(csv_paths.to_frame('path to `ucs` scores').to_markdown())

    dfs_dict = {count_type:
                load_from_ucs_csv(csv_paths[count_type])
                for count_type in csv_paths.index}

    # > save initial dataframe conversions as pickles
    init_df_paths = zip(dfs_dict.keys(), list(
        save_optimized(dfs_dict, csv_paths, verbose=args.verbose)))

    return dfs_dict, pd.Series({k: v for k, v in init_df_paths})


def _main():

    args = _parse_args()

    dfs_dict, df_paths = get_init_ucs_tables(args)
    verbose = args.verbose
    if verbose:
        display_init_info(dfs_dict)

    dfs_plus = add_extra_am(dfs_dict)
    floor = 0.75
    # big = dfs_plus['bigram']
    if verbose:
        for unit, df in dfs_plus.items():
            print_example(df, unit, example_key='exact',
                          sort_by='conservative_log_ratio')

        adv = dfs_plus['adv']

        print_md_table(
            adv.loc[adv.am_p1_given2 > floor,
                    ['l1', 'l2', 'f', 'am_expect_diff', 'am_p1_given2']],
            title=f'adverbs with adjusted conditional probability of environment > {floor}')

    big = add_adx_info(dfs_plus)

    dfs_plus['bigram'] = big
    polar_skewed_bigrams = identify_skewed_bigrams(
        big, floor=floor, verbose=verbose)
    # TODO: call `identify_skewed_bigrams()` on `dfs_plus['']` (i.e. adv & adj skewed towards *each other* instead of a polarity environment)
    if verbose:
        print_example(big, count_type='bigram',
                      example_key=big.at[polar_skewed_bigrams.sample(1).squeeze().name, 'l2'])

        for sorter in ['conservative_log_ratio', 'am_p1_given2', 'log_ratio', 'am_odds_ratio_disc']:
            print_sorted_md(polar_skewed_bigrams, sorter, floor)

    print('\n'.join([f'+ saved `{p}`' for p
          in list(save_optimized(dfs_plus, df_paths,
                                 added_measures=True, verbose=verbose))]))
    skew_dict = {'bigram': polar_skewed_bigrams}
    skew_paths = df_paths.apply(
        lambda p: p.with_name(p.name.replace(READ_TAG, 'SKEW')))
    print('\n'.join([f'+ saved `{p}`' for p
          in list(save_optimized(df_dict=skew_dict,
                                 paths=skew_paths[['bigram']],
                                 added_measures=True, verbose=verbose))]))


def get_adx_totals(df_dict: dict, adx: str) -> pd.Series:
    return pd.to_numeric(df_dict[adx][['l2', 'f2']].drop_duplicates().rename(
        columns={'l2': adx, 'f2': f'{adx}_total'}).set_index(adx).squeeze(), downcast='unsigned')


def _pull_data(args):
    for unit in ('', 'bigram', 'adv', 'adj'):
        csv_path = _get_ucs_csv(unit, args)
        yield unit, csv_path


def _get_ucs_csv(unit, args):

    # > select readable/*.csv if it exists, else readable/*.txt
    readable = seek_readable(unit, args)
    # > create ucs tables if readable/*.txt does not exist
    if not readable.is_file():

        init_ucs_stem = readable.stem.replace(READ_TAG, '').strip('.')
        basic_ucs_path = readable.parent.with_name(f'{init_ucs_stem}.ds.gz')
        basic_ucs_path = manipulate_ucs(basic_ucs_path, args, unit)
        # if given path to readable file still does not exist
        if not readable.is_file():
            readable = basic_ucs_path.with_name('readable').joinpath(
                basic_ucs_path.name.replace('ds.gz', f'{READ_TAG}.txt'))

    # > return readable path as .csv
    return txt_to_csv(readable) if readable.suffix == '.txt' else readable


def seek_readable(unit, args):
    # TODO: I think this will fail if "readable" directory is embedded in subdir...
    min_freq_flag = f'_min{args.min_freq}x'
    if unit:
        subdir = 'mirror' if 'mir' in args.data_suffix.lower() else 'set_diff'
        readable_parent = f'polar/{subdir}/{unit}'
        init_ucs_stem = f'polarized-{unit}_{args.data_suffix.strip(".tsv")}'
    else:
        # subdir = 'adj-x-adv'
        init_ucs_stem = args.all_counts.stem
        readable_parent = args.all_counts.parent
        if 'ucs' in readable_parent.name.lower():
            readable_parent = readable_parent.parent
        readable_parent = readable_parent.name

    readable_dir = _UCS_DIR.joinpath(f'{readable_parent}/readable')
    confirm_dir(readable_dir)
    init_ucs_stem += min_freq_flag
    print(f'\n## Acquiring `{init_ucs_stem}`',
          'frequency data and initial associations\n')

    ucs_stem = f'{init_ucs_stem}.{READ_TAG}'

    readable_csv = readable_dir / f'{ucs_stem}.csv'

    return (readable_csv if readable_csv.is_file()
            else readable_dir / f'{ucs_stem}.txt')


def manipulate_ucs(basic_ucs_path: Path, args, unit: str):
    basic_ucs_path = initialize_ucs(basic_ucs_path, args, unit)
    associate_ucs(basic_ucs_path)
    return basic_ucs_path


def initialize_ucs(basic_ucs_path: Path, args, unit: str = ''):

    print('\nLocating and/or building initial frequency-only UCS table...')
    with Timer() as _timer:
        basic_ucs_path = confirm_basic_ucs(basic_ucs_path, args, unit)
        print(f'+ path to simple UCS table: `{basic_ucs_path}`')
        print(f'+ time elapsed → {_timer.elapsed()}')
    return basic_ucs_path


def confirm_basic_ucs(basic_ucs_path, args,
                      unit: str = None):
    if basic_ucs_path.is_file():
        print('+ existing UCS table found ✓')
    elif unit:
        comp_path = args.complement_counts
        neg_path = args.negated_counts
        if any(not p.is_file() for p in (comp_path, neg_path)):
            exit(
                f'Initial counts file not found. Check your paths...\n> {comp_path}\n> {neg_path}')
        path_dict = polarize_counts(words_to_keep=unit, data_suffix=args.data_suffix,
                                    in_paths_dict={args.comp_label: comp_path,
                                                   args.neg_label: neg_path})
        basic_ucs_path = build_ucs_from_multiple(
            tsv_paths=path_dict.values(),
            min_count=args.min_freq,
            save_path=basic_ucs_path
        )
    elif args.all_counts.is_file():
        build_ucs_table(min_count=args.min_freq,
                        ucs_save_path=basic_ucs_path,
                        cat_tsv_str=f'cat {args.all_counts}')
    else:
        raise FileNotFoundError
    return basic_ucs_path


def associate_ucs(basic_ucs_path):
    with Timer() as _timer:
        print('\nCalculating UCS associations...')
        run_shell_command(
            f'bash {SANPI_DIR}/script/transform_ucs.sh {basic_ucs_path}')
        print(f'+ time elapsed → {_timer.elapsed()}')


def identify_skewed_bigrams(bigrams_df: pd.DataFrame,
                            floor: float = 0.8,
                            count_cutoff: int = 2,
                            verbose: bool = False):

    big = bigrams_df.filter(
        items=['l1', 'l2', 'f', 'E11', 'am_expect_diff', 'adv', 'adv_total', 'adj', 'adj_total',
               'am_p1_given2', 'am_log_likelihood', 'am_odds_ratio_disc',
               #    'log_likelihood',
               'log_ratio', 'conservative_log_ratio']
    ).sort_values('conservative_log_ratio', ascending=False)
    big.update(big.select_dtypes('number').round(3))
    # > quantify percentage of ENV-bigram tokens that were *unexpected*
    big['am_expect_diff_%'] = big.am_expect_diff.abs() / big.f * 100
    skewed_bigrams = big.loc[big.am_p1_given2.round(3).abs() >= floor, :]
    if verbose:
        n_top = 30
        print_md_table(
            df=(skewed_bigrams
                .sort_values('am_p1_given2', ascending=False)
                .head(n_top).round(2)
                .sort_values(['am_expect_diff_%', 'am_expect_diff'], ascending=False)),
            title=(f'\n## Top {n_top} '
                   'bigrams most strongly skewed toward polar environment '
                   f'(f>={big.f.min()}; am_p1_given2>={floor})\n'),
            n_dec=2)
    for ad in ['adv', 'adj']:
        neg_skewed = skewed_bigrams[ad].astype('string').value_counts()
        if verbose:
            print_md_table(
                neg_skewed.loc[neg_skewed > count_cutoff].to_frame(
                    'bigram count'),
                n_dec=2,
                title=(f'\n### {ad.capitalize()} appearing in more than {count_cutoff} '
                       f'negatively "skewed" bigrams (p1.given2 >= {floor})\n'))

            print(f"\n+ mean bigram count for unique {ad} =",
                  round(neg_skewed.filter(regex=r'[a-z]').mean(), 1))
    if verbose:
        print(f"\n> Skewed bigrams (f>={big.f.min()}; am_p1_given2>={floor}) account for\n> ",
              round(100 * skewed_bigrams.f.sum() / bigrams_df.N.iat[0], 2),
              "% of all tokens in current dataset\n> and ",
              round(bigrams_df.filter(items=skewed_bigrams.index,
                    axis=0).l2.nunique() / bigrams_df.l2.nunique() * 100, 2),
              "% of unique bigram forms",
              sep='')
    return skewed_bigrams


def save_optimized(df_dict: dict, paths: pd.Series,
                   added_measures=False, verbose=False):
    df_dict = _optimize(df_dict, verbose)
    for unit in paths.index:
        yield save_dataframe(paths[unit].name,
                             df_dict[unit],
                             added_measures)


def load_from_ucs_csv(input_csv):
    df = pd.read_csv(input_csv)
    return _set_data_keys(df)


def _set_data_keys(df):
    unique_l1 = df.l1.nunique()
    if unique_l1 < 40:
        key_len = 3
        keys = _make_keys(df.l1, df.l2, key_len)
        while keys.str.split('-').str.get(0).nunique() < unique_l1:
            key_len += 1
            keys = _make_keys(df.l1, df.l2, key_len)
    else:
        keys = df.l1 + '-' + df.l2

    df['key'] = keys
    df.reset_index().set_index('key')
    return df


def _make_keys(l1: pd.Series, l2: pd.Series, key_len: int):
    return l1.apply(lambda x: x[:key_len]) + '-' + l2


def print_example(df,
                  count_type=None,
                  example_key=None,
                  round_level=2,
                  sort_by='am_p1_given2',
                  columns_like=r'^([^ECORr_]|E11)',
                  regex=False) -> None:
    """
    Prints a specific example from a dataframe.

    Args:
        df (pandas.DataFrame): The dataframe to extract the example from.
        count_type (str, optional): The type of count to consider. Defaults to None.
        example_key (str, optional): The key of the example to print. Defaults to None.
        round_level (int, optional): The number of decimal places to round the example values to. Defaults to 2.
        sort_by (str, optional): The column to sort the example by. Defaults to 'am_p1_given2'.
        columns_like (str, optional): The regular expression pattern to match column names. Defaults to r'^([^ECORr_]|E11)'.
        regex (bool, optional): Whether to use regex pattern matching for the example key. Defaults to False.

    Returns:
        None
    """
    if not example_key:
        example_keys = {'bigram': 'exactly_surprising',
                        'adv': 'exactly',
                        'adj': 'surprising',
                        '': 'surprising'}
        example_key = example_keys[count_type]
    if regex:
        example = df.round(round_level).filter(axis=0, regex=example_key)
    else:
        example = df.round(round_level).filter(axis=0, like=example_key)
    if sort_by not in example.columns:
        sort_by = example.columns.iloc[0]
    example = example.sort_values(
        sort_by, ascending=sort_by.startswith(('r_', 'l')))
    example = example.filter(regex=columns_like).sort_index(axis=1)
    if example.empty:
        print(f'🤷 No {count_type} match {example_key}')
    else:
        transpose = example.shape[0] < example.shape[1] * .9
        print_md_table(
            example.select_dtypes('number'),
            transpose=transpose, n_dec=round_level,
            title=f'\n### {count_type.capitalize()} "{example_key}" examples sorted by `{sort_by}` column\n')
    print('\n---')


def add_extra_am(df_dict):
    for count_type, df in df_dict.items():
        try:
            scores = am.score(df)
        except KeyError:
            df = df.join(fq.observed_frequencies(df)).join(
                fq.expected_frequencies(df))
            scores = am.score(df)
        # loaded_cols = df.columns.to_list()
        df = df.copy().join(scores.loc[:, ~scores.columns.isin(df.columns)])

        print_example(df, count_type, columns_like=r'^[^ECORr]')
        df_dict[count_type] = df

    # am.conservative_log_ratio(dfs_plus['bigram'], alpha=0.05, boundary='poisson').nlargest(20)
    # am.conservative_log_ratio(adv, alpha=0.05, boundary='poisson').sort_values(ascending=False).abs().round(0).value_counts()
    # am.conservative_log_ratio(adv, alpha=0.05, boundary='poisson').sort_values(ascending=False).round(0).abs().nlargest(10)
    return df_dict


def _optimize(df_dict, verbose=False):
    for unit, _df in df_dict.items():
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
        df_dict[unit] = _df
        if verbose:
            print('\n\n============\n\n')
    return df_dict


def save_dataframe(input_name, _df, added_measures=False):
    out_dir = SANPI_DIR / 'results' / 'ucs_tables' / 'dataframes'
    confirm_dir(out_dir)

    out_path = out_dir / input_name.replace('.csv', '.pkl.gz')

    if added_measures:
        out_path = out_path.with_name(
            out_path.name.replace('.pkl.gz', '_extra.pkl.gz'))

    _df.to_pickle(out_path)
    if len(_df) <= 6500 and _df.size <= 250000:
        _df.to_csv(str(out_path).replace('.pkl.gz', '.csv'))
    return out_path


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('✔️ Program Completed --', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
