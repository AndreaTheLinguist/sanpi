import argparse
# from pprint import pprint
import statistics as stat
from pathlib import Path

# import numpy as np
import pandas as pd

from utils import (confirm_dir, find_glob_in_dir, percent_to_count, print_iter,  # pylint: disable=import-error
                   count_uniq, get_proc_time, print_md_table, save_table,
                   select_cols, select_pickle_paths, sort_by_margins, unpack_dict)
from utils.LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV  # pylint: disable=import-error
from utils.visualize import heatmap  # pylint: disable=import-error

_SANPI_DIR = Path('/share/compling/projects/sanpi')
_MIN_THRESH_COUNT = 2
_MIN_TOK_KEEP_RATIO = 0.15
_KEEP_ALLOWANCE_RATIO = 0.99
_ADV_KEEP_REQ = 20
_ADJ_KEEP_REQ = 40
_MIN_MEDIAN = 5


def _main():
    print(pd.Timestamp.now().ctime())
    (n_files, percent_thresh,
     post_proc_dir, frq_out_dir, frq_groups) = _parse_args()

    df = prepare_hit_table(n_files, percent_thresh, post_proc_dir)
    frq_thresh = _summarize_hits(df)

    if not frq_groups:
        frq_groups = ['all']

    for group in frq_groups:

        _t0 = pd.Timestamp.now()
        frq_df, frq_df_path = get_freq_info(df, n_files, frq_thresh,
                                            group, frq_out_dir)
        _t1 = pd.Timestamp.now()
        print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')

        _describe_counts(frq_df, frq_df_path)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-f',
        '--n_files',
        type=int,
        default=2,
        help=('number of dataframe `.pkl.gz` files to load from `../hit_tables/advadj/` '
              '(divided by corpus chunk/slice). '
              'Files are sorted by size so smaller files are selected first. '
              '(i.e. `f=5` will load the 5 smallest tables of hits)'))

    parser.add_argument(
        '-t',
        '--percent_hits_threshold',
        type=float,
        default=0.001,
        help=('Minimum frequency threshold of hits per lemma (in total) for lemma to be included. '
              '**Specified as PERCENTAGE of total (cleaned) hits, not as explicit integer of hits!** '
              'Any adverb or adjective lemma which does not meet this minimum frequency '
              'threshold (combined with any other lemma) will be dropped. '
              'NOTE: This filter is applied iteratively, with sums recalculated after '
              'the previous set of lemmas and their correpsonding bigram tokens are dropped.'))

    parser.add_argument(
        '-p',
        '--post_proc_dir',
        type=Path,
        default=Path('/share/compling/data/sanpi/4_post-processed'),
        help=('Path to location for saving post processed hits. '
              '(i.e. tables indexed by `hit_id`). '
              'Name of file(s) generated from `n_files` and `tok_threshold`'))

    parser.add_argument(
        '-o',
        '--frq_out_dir',
        type=Path,
        default=_SANPI_DIR.joinpath('results/freq_out'),
        help=('Path to location for bigram frequency results (adj_lemma ✕ adv_lemma tables). '
              'Name of file(s) generated from `n_files` and `tok_threshold`'))

    parser.add_argument(
        '-g', '--frequency_group',
        type=str, action='append', dest='frq_groups',
        default=[],
        help=('')
    )

    args = parser.parse_args()
    print_md_table(
        pd.Series({name: val for name, val in
                   [a for a in args._get_kwargs()]})
        .to_frame('arguments given'))
    return (args.n_files, args.percent_hits_threshold,
            args.post_proc_dir, args.frq_out_dir, set(args.frq_groups))


def prepare_hit_table(n_files, tok_thresh_p, post_proc_dir):
    sample_tag = 'sample' if n_files < 35 else ''
    print(f"# Collecting {sample_tag} vocabulary frequencies for",
          f"{n_files} *hits.pkl.gz hit tables")

    pkl_suff = f'{n_files}f.pkl.gz'
    confirm_dir(post_proc_dir)

    clean_bigrams_pkl = post_proc_dir.joinpath(f'bigrams_clean.{pkl_suff}')
    # print(f'Cleaned Hits Table Path:\n  >> {clean_bigrams_pkl}')

    th_bigrams_pkl = post_proc_dir.joinpath(
        f"bigrams-only_thr{str(tok_thresh_p).replace('.','-')}p.{pkl_suff}")

    _t0 = pd.Timestamp.now()
    print('\n## loading data...')
    if th_bigrams_pkl.is_file():
        print(
            f'* Found previous output. Loading data from {th_bigrams_pkl}...')
        df = pd.read_pickle(th_bigrams_pkl).convert_dtypes()

    else:
        if clean_bigrams_pkl.is_file():
            print('* Found previous output.',
                  f'Loading data from {clean_bigrams_pkl}')
            df = pd.read_pickle(clean_bigrams_pkl)
            if df.index.name != 'hit_id':
                df = df.set_index('hit_id')
            print_md_table(df.describe().T, indent=2,
                           title='Clean Hits Summary')
            print_md_table(_describe_str_lemma_counts(df),
                           indent=2, title='Clean Lemma Counts Summary')

        else:
            df = _load_data(n_files)
            if df.index.name != 'hit_id':
                df = df.set_index('hit_id')
            print(f'\n> {len(df):,} initial hits')
            _print_uniq_lemma_count(df, updated=False)
            print(_describe_str_lemma_counts(
                df).round().to_markdown(floatfmt=',.0f'))
            clean_t0 = pd.Timestamp.now()
            df = _clean_data(df)
            clean_t1 = pd.Timestamp.now()
            print('\n[ Time to clean combined hits dataframe:',
                  get_proc_time(clean_t0, clean_t1), ']')
            print_md_table(_describe_str_lemma_counts(df))

            save_table(df,
                       str(clean_bigrams_pkl).split('.pkl', 1)[0],
                       "cleaned bigram hits")

        # > drop infrequent adv & adj lemmas
        df = _drop_infreq(df, tok_thresh_p)
        tok_thresh_c = int(_describe_str_lemma_counts(df).loc['min', :].min())
        save_table(
            df,
            str(th_bigrams_pkl).split('.pkl', 1)[0],
            f'frequency restrictred bigrams ({tok_thresh_c}+ frequency threshold)')

    _t1 = pd.Timestamp.now()
    print('✓ time:', get_proc_time(_t0, _t1))
    return df


def _describe_str_lemma_counts(df: pd.DataFrame) -> pd.DataFrame:
    lemma_stats = (df.columns[df.columns.str.endswith('_lemma')]
                   .to_series().apply(
                       lambda c: df[c].value_counts().describe())
                   ).T
    lemma_stats.columns = lemma_stats.columns.str.replace('lemma', 'counts')
    return lemma_stats.round()


def _load_data(n_files: int) -> pd.DataFrame:
    pkl_paths = select_pickle_paths(n_files)
    _ts = pd.Timestamp.now()
    df_list = []
    for i, p in enumerate(pkl_paths):
        print(f'\n{i+1}. ../{p.relative_to(Path("/share/compling/data"))}')
        # check for previous simplification
        simple_out_dir = p.parent.joinpath('simple')
        if not simple_out_dir.is_dir():
            simple_out_dir.mkdir(parents=True)
        simple_hits_pkl = simple_out_dir.joinpath('S_' + p.name)

        if simple_hits_pkl.is_file():
            print(
                f'   * Found previous output.\n     Loading data from `../{Path(*simple_hits_pkl.parts[-4:])}`'
            )
            df = pd.read_pickle(simple_hits_pkl)
        else:
            df = pd.read_pickle(p)
            df = select_cols(df)
            save_table(df,
                       str(simple_hits_pkl).split('.pkl', maxsplit=1)[0],
                       df_name='simplified hits')
        print_md_table(df.describe().T.convert_dtypes(),
                       indent=3, title=f'({i+1}) `{p.stem}` summary')
        df_list.append(df)

    combined_df = pd.concat(df_list)
    print_md_table(combined_df.describe().T.convert_dtypes(),
                   title='Combined Raw Hits Summary')

    _te = pd.Timestamp.now()
    print('> Time to create composite hits dataframe:',
          get_proc_time(_ts, _te))

    return combined_df


def _print_uniq_lemma_count(df: pd.DataFrame,
                            cols=None,
                            updated: bool = True,
                            label: str = '',
                            head_mark: str = ''):
    if not label:
        label = 'updated' if updated else 'initial'
    if not head_mark:
        head_mark = '+' if updated else '='
    if not cols:
        cols = df.columns[df.columns.str.endswith('_lemma')]
    counts_info = {
        c.replace('_lemma', '').upper(): count_uniq(df[c])
        for c in cols
    }
    str_len = len(max(counts_info.keys()))
    num_len = len(str(max(counts_info.values()))) + 1
    counts = ['{0:<{1}s}:  {2:>{3},d}'.format(k, str_len, v, num_len)  # pylint: disable=consider-using-f-string
              for k, v in counts_info.items()]
    print_iter(counts,
               header=f'{head_mark} unique lemmas in {label} hits',
               indent=2)


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # > print overview of initial data
    print('\n## Cleaning up hits: removing duplicated or exceptionally',
          'long sentences, strange orthography, and random capitals.')
    starting_token_count = len(df)

    # * drop lemmas with abnormal orthography
    ts = pd.Timestamp.now()
    prior_len = len(df)
    df = _drop_odd_orth(df)
    te = pd.Timestamp.now()
    print(f'> {(prior_len - len(df)):,} hits',
          'removed due to abnormal orthography in',
          get_proc_time(ts, te))
    _print_uniq_lemma_count(df)
    print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))

    # * removing implausibly long, then duplicate sentences
    if 'token_str' in df.columns and 'text_window' in df.columns:
        # * too long
        _t0 = pd.Timestamp.now()
        df = _drop_long_sents(df)
        _t1 = pd.Timestamp.now()
        _print_uniq_lemma_count(df, label='natural', head_mark='~')
        print_md_table(_describe_str_lemma_counts(df))
        print('[ Time to drop implausible "sentences":',
              get_proc_time(_t0, _t1), ']')

        # * duplicates
        _t0 = pd.Timestamp.now()
        _print_uniq_lemma_count(df, label='nonduplicated', head_mark='~')
        print_md_table(_describe_str_lemma_counts(df))
        df = _drop_duplicate_sents(df)
        _t1 = pd.Timestamp.now()

        print('[ Time to drop duplicated sentences:',
              get_proc_time(_t0, _t1), ']')

    valid_token_count = len(df)
    print(f'\n> {(starting_token_count - valid_token_count):,}',
          'hits from invalid sentences (too long or duplicated) removed.')
    print(f'Total valid/cleaned bigram hits: {valid_token_count:,}')
    _print_uniq_lemma_count(df, label='valid', head_mark='~')
    print_md_table(_describe_str_lemma_counts(df))

    # * remove random capitalizations
    ts = pd.Timestamp.now()
    print('\nNormalizing lemma case (making everything lower case)...')
    df = df.assign(adv_lemma=df.adv_lemma.str.lower(),
                   adj_lemma=df.adj_lemma.str.lower())
    te = pd.Timestamp.now()
    _print_uniq_lemma_count(df)
    print_md_table(_describe_str_lemma_counts(df))
    print('[ Time to normalize lemma case:',
          get_proc_time(ts, te), ']')

    return df


def _drop_odd_orth(df: pd.DataFrame,
                   verbose=False) -> pd.DataFrame:

    print('\nRemoving lemmas with abnormal orthography...')
    J = df.adj_lemma
    J_filter = ~odd_lemma_orth(J)
    if verbose:
        meta_df = (J_filter.value_counts(normalize=True)
                   .multiply(100).round(3).to_frame('%_of_adj')
                   .assign(status=['kept', 'dropped'],
                           adj_tokens=J_filter.value_counts())
                   . set_index('status'))
        print_md_table(
            meta_df, title='ADV orthography filter outcomes', n_dec=2)

    R = df.adv_lemma
    R_filter = ~odd_lemma_orth(R)
    if verbose:
        print((R_filter.value_counts(normalize=True)
               .multiply(100).round(3).to_frame("%_of_adv")
               .assign(status=['kept', 'dropped'],
                       adv_tokens=R_filter.value_counts())
               .set_index('status').to_markdown()), '\n')

    return df.loc[J_filter & R_filter, :]


def odd_lemma_orth(lemmas: pd.Series) -> pd.Series:
    return pd.Series(
        lemmas.str.startswith(('-', '&', '.'))
        | lemmas.str.endswith(('-', '&'))
        | lemmas.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))


def _drop_long_sents(df: pd.DataFrame) -> pd.DataFrame:
    starting_df = df.copy()
    df = df.assign(tok_in_sent=df.token_str.apply(lambda s: len(s.split())))
    sent_limit = 250
    too_long = df.tok_in_sent > sent_limit
    uniq_too_long = df.loc[too_long, :].index.str.split(":",
                                                        1).str.get(0).unique()
    print(f'\nDropping {(too_long.value_counts()[True]):,} hits',
          f'from {len(uniq_too_long):,} "sentences" with',
          f'{sent_limit}+ tokens. For example:\n```')
    print((starting_df.loc[df.index.str.startswith(tuple(uniq_too_long)),
                           ['token_str']]).sample(1).squeeze()[:550] +
          '...\n```')
    df = df.loc[~too_long, :]
    return df


def _drop_duplicate_sents(df: pd.DataFrame, verbose: int = 0) -> pd.DataFrame:
    over_10_tok = df.tok_in_sent > 10
    is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
    definite_duplicate = over_10_tok & is_duplicate_hit
    print(f'\n≎ Removing {(definite_duplicate.value_counts()[True]):,}',
          'duplicate hits between input tables',
          '(provided sentence is longer than 10 tokens).')
    singletons = df.loc[~definite_duplicate,
                        ['adv_lemma', 'adj_lemma', 'token_str']]
    if verbose == 2:
        init_sent_counts = df.token_str.value_counts(sort=False).sort_index()
        filter_sent_counts = singletons.token_str.value_counts(
            sort=False).sort_index()
        sent_diff = init_sent_counts - filter_sent_counts
        sent_with_dup = len(sent_diff[sent_diff != 0].index)
        print(f'  ⨳ {sent_with_dup:,} initial sentences had 1+ duplicates')
    if verbose == 1:
        all_dup = df.duplicated(['token_str', 'text_window'], keep=False)
        print('Examples of duplication:')
        print((df.loc[all_dup & over_10_tok,
                      ['tok_in_sent', 'token_str']]).sort_values(['token_str'
                                                                  ]).head(8))

    return singletons[['adv_lemma', 'adj_lemma']].astype('string')


def _drop_infreq(df, percent) -> pd.DataFrame:
    print(f'## Removing hits where `{df.columns[0]}` and/or ',
          f'`{df.columns[1]}` do not meet the total hit threshold...')

    print_md_table(df.describe().T, title='Initial (clean) Summary')
    print_md_table(_describe_str_lemma_counts(df),
                   title='Initial (clean) distribution info')
    ts = pd.Timestamp.now()
    clean_total = len(df)
    # must keep at least 15% of the initial hits
    must_keep = round(clean_total * _MIN_TOK_KEEP_RATIO)
    n_dropped = len(df)
    filter_applied = 0
    filter_attempt = 0
    while n_dropped > 0:
        filter_attempt += 1
        # #* Best to use a reasonable value (i.e. [0.00001:1]%)

        percent, hit_thresh = _confirm_thresh(clean_total, percent)
        if filter_attempt == 0:
            print('\nLimiting by total lemma frequency',
                  f'threshold ≥ {hit_thresh:,} tokens per lemma...')

        update_df = _get_update(df, hit_thresh)
        n_remain = len(update_df)
        n_dropped = len(df) - n_remain

        # * Evaluate if `n_dropped` (hits dropped this pass), yields ideal result.
        # *  -> If not, adjust threshold.
        adjust_str = ''
        # > if _no/too few_ hits were dropped (overall) ~ 95+% of initial hits remain...
        #! use `n_remain` to evaluate because `n_dropped` is only for CURRENT attempt
        # > or if median count for either lemma type is less than 5
        if (n_remain >= _KEEP_ALLOWANCE_RATIO * clean_total
                or any(_describe_str_lemma_counts(update_df).T['50%'] < _MIN_MEDIAN)):
            # > raise percentage threshold --> increase by 1/4
            adjust_str = '◔ Insufficient Reduction: 🔺raising'
            percent *= 1.25
            if n_dropped <= 0:
                #! must also reset `n_dropped` to stay in `while` loop
                n_dropped = 1

        # > hits were dropped in this attempt...
        elif n_dropped > 0:

            # > if _too many_ hits were dropped...
            if ((n_remain < must_keep)
                    # keep at least 20 unique adv
                    or (count_uniq(update_df.adv_lemma) < _ADV_KEEP_REQ)
                    # keep at least 40 unique adj
                        or (count_uniq(update_df.adj_lemma) < _ADJ_KEEP_REQ)
                    ):

                if not filter_applied and filter_attempt < 5:
                    # > lower percentage threshold --> reduce by 1/4
                    adjust_str = '◕ Excessive Reduction: 🔻lowering'
                    percent *= 0.75

                else:
                    print('! More lemmas fall below the threshold,',
                          'but removing them violates other restrictions.')
                    n_dropped = 0

            # * if `n_dropped` is ideal, udpate `df` to `update_df`
            else:
                filter_applied += 1
                print(f'Successful pass #{filter_applied} (attempt',
                      f'#{filter_attempt}):\n',
                      f'removing {n_dropped:,} hits containing lemmas',
                      f'having fewer than {hit_thresh:,} total tokens...')
                df = update_df

        # > sufficient hits have been removed, just not in this round
        else:
            print('✓ No further infrequent lemmas found.',
                  'Frequency filtering complete!')

        if adjust_str:

            print(f'⚠️  ({filter_attempt}) Token threshold of',
                  f'{hit_thresh:,} tokens/lemma failed.')
            # > update token count threshold from new percentage
            hit_thresh = percent_to_count(percent, clean_total)
            print(f'  {adjust_str} percentage for threshold by 1/4')
            print(f'    updated threshold: {hit_thresh:,} tokens,',
                  f'      ~{percent:.5}% of initial (clean) hits')

    te = pd.Timestamp.now()
    print(
        f'> {(clean_total - len(df)):,} total hits dropped due to',
        f'infrequncy (lemma(s) with fewer than {hit_thresh:,} hits',
        f'~{round(percent,5)}% of total valid hits) across',
        f'{filter_applied} filtering pass(es).\n',
        f'[ time elapsed = {get_proc_time(ts, te)} ]')

    print_md_table(_describe_str_lemma_counts(df), indent=2)
    remain_str = f'\n>>> {len(df):,} total remaining hits <<<'
    percent_str = f'{round(len(df)/clean_total*100, 2)}% of {clean_total} total valid hits.'
    width = max(len(remain_str), len(percent_str))+2
    print(remain_str.center(width))
    print(percent_str.center(width))

    return df


def _confirm_thresh(total, percent):
    hit_thresh = percent_to_count(percent, total)
    if hit_thresh < _MIN_THRESH_COUNT:
        hit_thresh = _MIN_THRESH_COUNT
        percent = hit_thresh / total * 100
        print('Given percentage is too low for noticable reduction.',
              f'Set values to minimum {hit_thresh} hit tokens/lemma')
        print(f'  ≈ {round(percent,6)}% of clean hits')
    return percent, hit_thresh


def _get_update(df, token_thresh):
    indexers = []
    # print(_describe_lemma_counts(df).to_markdown())
    print('\n+ Compiling frequency table update:')
    for i, col in enumerate(df.columns):
        print(f'  ({i+1}) restricting `{col}` column...')
        col_counts = df[col].value_counts()

        lemmas_over_thresh = col_counts[col_counts >= token_thresh].index

        indexers.append(df[col].isin(lemmas_over_thresh))

    update_df = df.loc[indexers[0] & indexers[1], :]

    up_st = _describe_str_lemma_counts(update_df).T
    up_st = (up_st
             .assign(range=up_st['max'] - up_st['min'],
                     iqr=up_st['75%'] - up_st['25%']).round())
    print('+ Potential Table Update')
    print_md_table(up_st[['mean', '50%', 'min', 'max']], indent=2,
                   title=f'{(len(df) - len(update_df)):,} potential removals')
    _print_uniq_lemma_count(update_df)

    return update_df


def _summarize_hits(df):
    lemma_counts_summ = _describe_str_lemma_counts(df)
    tok_thresh_c = int(lemma_counts_summ.loc['min', :].min())
    print(f'    ⇟ minimum hits/lemma in data: {tok_thresh_c:,}')
    print_md_table(df.describe().T, indent=2,
                   title='Frequency Filtered Hits Summary')
    print_md_table(lemma_counts_summ, indent=2,
                   title='Frequency Filtered Lemma Distributions')

    return tok_thresh_c


def get_freq_info(df, n_files, frq_thresh, group, frq_out_dir):
    print(f'\n## Processing Frequency data for {group} lemmas.')
    if group != 'all':
        frq_out_dir = frq_out_dir.joinpath(group)
    confirm_dir(frq_out_dir)
    frq_out_stem = get_freq_out_stem(frq_thresh, n_files, group)
    # > method returns `None` if stem not found
    frq_df_path = find_glob_in_dir(frq_out_dir, f'*{frq_out_stem}*csv')

    # if crosstabulated frequency table is found
    if frq_df_path:
        print(f'\n* frequency table ({group}) found.')
        frq_df = _load_frq_table(frq_df_path)
    # if frequency table is not found;
    #   i.e. `f` call returned None
    else:
        frq_df_path = frq_out_dir.joinpath(frq_out_stem + '.csv')
        # sanity check
        if not frq_df_path.name.endswith('f.csv'):
            exit(f'frequency path error: {frq_df_path}')
        frq_df = _build_frq_df(df, frq_df_path, group)
    return frq_df, frq_df_path


def get_freq_out_stem(frq_thresh, n_files, group_code):
    return f'{group_code}-frq_thresh{frq_thresh}.{n_files}f'


def _load_frq_table(frq_df_path):
    print(f'  Loading from ../{frq_df_path.relative_to(_SANPI_DIR)}...')
    if frq_df_path.suffix.endswith('csv'):
        frq_df = pd.read_csv(frq_df_path)
        frq_df.columns = frq_df.columns.str.strip()
    elif '.pkl' in frq_df_path.suffixes:
        frq_df = pd.read_pickle(frq_df_path)

    if 'adj_lemma' in frq_df.columns:
        frq_df = frq_df.set_index('adj_lemma')
    frq_df.columns.name = 'adv_lemma'
    return frq_df


def _build_frq_df(df: pd.DataFrame,
                  frq_df_path: Path,
                  group_code: str,
                  ) -> pd.DataFrame:
    rdf = df

    if group_code.lower() != 'all':
        J, __ = unpack_dict(SAMPLE_ADJ)
        R, __ = unpack_dict(SAMPLE_ADV, values_name='adv')
        rdf = df.loc[df.adj_lemma.isin(J)
                     & df.adv_lemma.isin(R), :].astype('string')
    _t0 = pd.Timestamp.now()
    frq_df = pd.crosstab(index=rdf.adj_lemma,
                         columns=rdf.adv_lemma,
                         margins=True,
                         margins_name='SUM')

    _t1 = pd.Timestamp.now()
    print(f'[ Time to crosstabulate frequencies: {get_proc_time(_t0, _t1)} ]')

    frq_df = sort_by_margins(frq_df, margins_name='SUM')
    title = (f'{group_code} adj ✕ adv frequency table'
             .replace('JxR', 'scale diagnostics'))
    save_table(frq_df,
               str(frq_df_path),
               title, formats=['csv'])
    return frq_df


def _describe_counts(df: pd.DataFrame,
                     df_path: str) -> None:
    data_label = df_path.name.replace('.csv', '')
    stats_dir = df_path.parent.joinpath('descriptive_stats')
    confirm_dir(stats_dir)
    out_path_stem = f'stats_{data_label}'
    df = df.fillna(0)
    most_var_adv = df.columns.to_list()[1:21]
    most_var_adj = df.index.to_list()[1:21]
    for frame, pos in ((df, 'Adverb'), (df.transpose(), 'Adjective')):

        print(f'\n## Descriptive Statistics by {pos}')
        no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
        desc_no_sum = no_sum_frame.describe()
        # > need to exclude the ['SUM','SUM'] cell
        sum_col = frame.loc[frame.index != 'SUM', 'SUM']
        desc_sum = sum_col.describe().to_frame()

        for desc, values in [(desc_no_sum, no_sum_frame), (desc_sum, sum_col)]:
            desc = _enhance_descrip(desc, values)
            if 'SUM' in desc.index:
                desc = desc.transpose()
                desc.columns = [f'Summed Across {pos}s']
                print_md_table(desc.round(), title=' ')
            else:
                save_table(
                    desc,
                    f'{stats_dir}/{pos[:3].upper()}-{out_path_stem}',
                    f'{pos} descriptive statististics for {out_path_stem}',
                    ['csv'])
                print_md_table(desc.sample(6).round(),
                               title=f'Sample {pos} Stats ')

                # ? #TODO: add simple output of just `df.var_coeff`?
                # desc.info()
                if pos == 'Adverb':
                    most_var_adv = _select_lemmas(desc)
                else:
                    most_var_adj = _select_lemmas(desc)

    _visualize_counts(df.loc[['SUM'] + most_var_adj,
                      ['SUM'] + most_var_adv], df_path)


def _enhance_descrip(desc: pd.DataFrame,
                     values: pd.Series) -> pd.DataFrame:
    desc = desc.transpose()
    desc = desc.assign(total=values.sum(),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'])
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    if 'SUM' not in desc.index:
        desc = desc.assign(
            plus1_geo_mean=values.add(1).apply(stat.geometric_mean),
            plus1_har_mean=values.add(1).apply(stat.harmonic_mean))
    for col in desc.columns:
        if col in ('mean', 'std', 'variance', 'coeff_var'):
            desc.loc[:, col] = pd.to_numeric(desc[col].round(2),
                                             downcast='float')
        else:
            desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    return desc

def _select_lemmas(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
    nth = int(len(desc)/6)
    trim = int(len(desc) * 0.01)
    desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    top_means_metric = desc.loc[
        (desc['mean'] > (desc_interior['mean'].median() * .75))
        &
        (desc.total > (desc_interior['total'].median() * .75)), metric]
    # info_list = []
    # for label, desc_df in {'interior': desc.iloc[5:, :], 'full': desc}.items():
    #     top_means = desc_df.loc[
    #         (desc_df['mean'] > (desc_df['mean'].median() + 0.5 * 1))
    #         &
    #         (desc_df.total > (desc_df.total.median() * 1.1))
    #         , [metric, 'mean', '50%', 'total', 'max', 'range']]
    #     info = top_means.describe()
    #     info.columns = info.columns.astype('string') + f'_{label}'
    #     info_list.append(info)
    # print_md_table(info_list[0].join(info_list[1]).sort_index(axis=1).round(0),
    #                title='Compare descriptive stats')
    if largest:
        lemmas = top_means_metric.squeeze().nlargest(nth).index.to_list()
    else:
        lemmas = top_means_metric.squeeze().nsmallest(nth).index.to_list()
    return lemmas



def _visualize_counts(frq_df, frq_df_path):
    heat_dir = frq_df_path.parent.joinpath('images')
    confirm_dir(heat_dir)
    heat_fname = f'heatmap_{frq_df_path.stem}.png'
    if len(frq_df) < 60 and len(frq_df.columns) < 40:
        heatmap(frq_df,
                save_name=heat_fname,
                save_dir=heat_dir)
    else:
        heatmap(frq_df.sample(min(60, len(frq_df))).T.sample(min(30, len(frq_df.T))).T,
                save_name=f'sample-{heat_fname}',
                save_dir=heat_dir)

# def _make_freq_tables(frq_out_dir: Path,
    #                   df: pd.DataFrame,
    #                   frq_thresh,
    #                   n_files: int,
    #                   group_code: str = 'all') -> None:
    # """locate or create frequency tables: crosstabulated `adv_lemma` x `adj_lemma` counts.

    # If file exists, load it and collect descriptive stats and, if it is small enough, create corresponding heatmap visualization.

    # If it does not exist, run crosstabulation on `adv_lemma` and `adj_lemma` columns. The collect stats and create heatmap (if table is small enough).

    # Args:
    #     frq_out_dir (Path): location to save frequency tables, descriptive stats, and any heatmaps.
    #     df (pd.DataFrame): dataframe containing `adv_lemma` and `adj_lemma` columns at the minimum
    #     frq_thresh (_type_): minimum number of tokens per lemma in data
    #     n_files (int): number of files the current data is sourced from (~ # corpus chunks)
    #     group_code (str, optional): set to 'JxR' to filter df on subset of lemmas read in from `lexical_categories`. If 'JxR' is given, all output files will be saved to subdirectory, `../freq_out/JxR/`. Defaults to all.
    # """

    # pass

# def _find_prior_freq_out(frq_out_dir: Path,
    #                      frq_out_stem: str,
    #                      group_code: str) -> pd.DataFrame:
    # frq_df = pd.DataFrame()

    # return frq_df

    # mean_centr = no_sum_frame - no_sum_frame.mean()
    # mean_stand = no_sum_frame / no_sum_frame.mean()
    # mean_stand_centr = mean_stand - mean_stand.mean()
    # log2_trans = no_sum_frame.apply(np.log2)
    # log2_plus1_trans = no_sum_frame.add(1).apply(np.log2)
    # logn_plus1_trans = no_sum_frame.apply(np.log1p)


if __name__ == '__main__':
    global_start_time = pd.Timestamp.now()
    _main()
    global_end_time = pd.Timestamp.now()
    finish_str = ('✓ Finished @ '
                  + global_end_time.strftime("%Y-%m-%d %I:%M%p"))
    w = len(finish_str)+1
    print('',
          '.'*w,
          finish_str,
          sep='\n')
    time_str = '== Total Run Time =='
    print(time_str)
    print(get_proc_time(global_start_time, global_end_time).center(len(time_str)))
