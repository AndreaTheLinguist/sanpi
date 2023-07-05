import argparse
import statistics as stat
from pathlib import Path

# import numpy as np
import pandas as pd

from utils import (print_iter, # pylint: disable=import-error
    count_uniq, get_proc_time, save_table, sort_by_margins, unpack_dict)
from utils.LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV # pylint: disable=import-error
from utils.visualize import heatmap # pylint: disable=import-error


def _main():
    print(pd.Timestamp.now().ctime())
    n_files, tok_thresh_p, post_proc_dir, frq_out_dir = _parse_args()
    tok_thresh_c = None
    print("Collecting sample vocabulary frequencies for",
          f"{n_files} *hits.pkl.gz files")

    for d in (frq_out_dir, post_proc_dir):
        if not d.is_dir():
            d.mkdir(parents=True)
    pkl_suff = f'{n_files}f.pkl.gz'
    clean_bigrams_pkl = post_proc_dir.joinpath(f'bigrams_clean.{pkl_suff}')
    print(f'Hits Data Path:\n  >> {clean_bigrams_pkl}')

    th_bigrams_pkl = post_proc_dir.joinpath(
        f"bigrams-only_thr{str(tok_thresh_p).replace('.','-')}p.{pkl_suff}")

    _t0 = pd.Timestamp.now()
    print('\n## loading data...')
    if th_bigrams_pkl.is_file():
        print(
            f' * Found previous output. Loading data from {th_bigrams_pkl}...')
        df = pd.read_pickle(th_bigrams_pkl).convert_dtypes()
        tok_thresh_c = int(_describe_str_lemma_counts(df).loc['min', :].min())
        print(f'   ⌖ minimum hits/lemma in data: {tok_thresh_c:,}')

    else:

        if (clean_bigrams_pkl.is_file()
            # and n_files < 15
            ):
            print(' * Found previous output.',
                  f'Loading data from {clean_bigrams_pkl}')
            df = pd.read_pickle(clean_bigrams_pkl)
            if df.index.name != 'hit_id':
                df = df.set_index('hit_id')
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
            # if n_files < 15:
            # save_table(df,
            #    str(clean_bigrams_pkl).split('.pkl', 1)[0],
            #    "cleaned bigram hits")
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

    print(df.describe().transpose().to_markdown(floatfmt=',.0f'))
    _t1 = pd.Timestamp.now()
    print('✓ time:', get_proc_time(_t0, _t1))

    _t0 = pd.Timestamp.now()
    # ? 🤔 does this need to change to use the same percent notation used for the other paths anyway?
    _make_freq_tables(frq_out_dir, df, tok_thresh_c, n_files)
    # > uncomment below line ↓ to analyze subset of lemmas as described by `SAMPLE_ADJ` & `SAMPLE_ADV`
    # _make_freq_tables(frq_out_dir, df, tok_thresh_c, n_files, group_code='JxR')
    _t1 = pd.Timestamp.now()
    print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')


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
        default=Path('/share/compling/projects/sanpi/results/freq_out'),
        help=('Path to location for bigram frequency results (adj_lemma x adv_lemma tables). '
              'Name of file(s) generated from `n_files` and `tok_threshold`'))

    args = parser.parse_args()

    return args.n_files, args.percent_hits_threshold, args.post_proc_dir, args.frq_out_dir


def _load_data(n_files: int) -> pd.DataFrame:
    pkl_paths = _select_pickles(n_files)
    _ts = pd.Timestamp.now()
    df_list = []
    for i, p in enumerate(pkl_paths):
        print(f'  {i+1}. ../{p.relative_to(Path("/share/compling/data"))}')
        # check for previous simplification
        simple_out_dir = p.parent.joinpath('simple')
        if not simple_out_dir.is_dir():
            simple_out_dir.mkdir(parents=True)
        simple_hits_pkl = simple_out_dir.joinpath('S_' + p.name)

        if simple_hits_pkl.is_file():
            print(
                f'     * Found previous output. Loading data from {simple_hits_pkl}'
            )
            df = pd.read_pickle(simple_hits_pkl)
        else:
            df = pd.read_pickle(p)
            df = _select_cols(df)
            save_table(df,
                       str(simple_hits_pkl).split('.pkl', maxsplit=1)[0],
                       df_name='simplified hits')

        df_list.append(df)

    combined_df = pd.concat(df_list)

    _te = pd.Timestamp.now()
    print('  > Time to create composite hits dataframe:',
          get_proc_time(_ts, _te))

    return combined_df


def _select_pickles(n_files: int) -> pd.Series:
    pickle_dir = Path('/share/compling/data/sanpi/2_hit_tables/advadj')
    # > make dataframe to load smallest files first (for testing)
    pkl_df = pd.DataFrame(pickle_dir.glob('bigram-*hits.pkl.gz'),
                          columns=['path'])
    pkl_df = pkl_df.assign(size=pkl_df.path.apply(lambda f: f.stat().st_size))
    pkl_paths = pkl_df.sort_values('size').head(n_files).reset_index().path
    return pkl_paths


def _select_cols(df: pd.DataFrame,
                 #  target_adj, target_adv
                 ) -> pd.DataFrame:
    df = (df.loc[:, ['adv_lemma', 'adj_lemma', 'text_window', 'token_str']].
          astype('string'))
    # df = df.loc[~df.duplicated(['token_str', 'text_window']), :]
    # df_J = df.loc[df.adj_lemma.isin(target_adj), :]
    # df_R = df.loc[df.adv_lemma.isin(target_adv), :]
    # dfuq = df.loc[~df.duplicated(['token_str', 'text_window']), :]
    # dfuq.assign(
    #     adj_lemma=pd.Categorical(dfuq.adj_lemma, categories=target_adj),
    #     adv_lemma=pd.Categorical(df_RJuq.adv_lemma, categories=target_adv))
    return df


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
        print('[ Time to drop implausible "sentences":',
              get_proc_time(_t0, _t1), ']')

        # * duplicates
        _t0 = pd.Timestamp.now()
        df = _drop_duplicate_sents(df)
        _t1 = pd.Timestamp.now()
        print('[ Time to drop duplicated sentences:',
              get_proc_time(_t0, _t1), ']')

    valid_token_count = len(df)
    print(f'\n> {(starting_token_count - valid_token_count):,}',
          'hits from invalid sentences (too long or duplicated) removed.')
    _print_uniq_lemma_count(df, label='valid', head_mark='~')
    print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))

    # * remove random capitalizations
    ts = pd.Timestamp.now()
    print('\nNormalizing lemma case (making everything lower case)...')
    df = df.assign(adv_lemma=df.adv_lemma.str.lower(),
                   adj_lemma=df.adj_lemma.str.lower())
    te = pd.Timestamp.now()
    _print_uniq_lemma_count(df)
    print('[ Time to normalize lemma case:',
          get_proc_time(ts, te), ']')

    return df


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


def _describe_str_lemma_counts(df: pd.DataFrame) -> pd.DataFrame:
    lemma_stats = (df.columns[df.columns.str.endswith('_lemma')]
                   .to_series().apply(
                       lambda c: df[c].value_counts().describe())
                   ).T
    lemma_stats.columns = lemma_stats.columns.str.replace('lemma', 'counts')
    return lemma_stats.round()


def _drop_long_sents(df: pd.DataFrame) -> pd.DataFrame:
    starting_df = df.copy()
    df = df.assign(tok_in_sent=df.token_str.apply(lambda s: len(s.split())))
    sent_limit = 250
    too_long = df.tok_in_sent > sent_limit
    uniq_too_long = df.loc[too_long, :].index.str.split(":",
                                                        1).str.get(0).unique()
    print(f'Dropping {(too_long.value_counts()[True]):,} hits',
          f'from {len(uniq_too_long):,} "sentences" with',
          f'{sent_limit}+ tokens. For example:\n```')
    print((starting_df.loc[df.index.str.startswith(tuple(uniq_too_long)),
                           ['token_str']]).sample(1).squeeze()[:550] +
          '...\n```')
    df = df.loc[~too_long, :]
    _print_uniq_lemma_count(df)
    return df


def _drop_duplicate_sents(df: pd.DataFrame) -> pd.DataFrame:
    over_10_tok = df.tok_in_sent > 10
    is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
    definite_duplicate = over_10_tok & is_duplicate_hit
    print(f'\n≎ Removing {(definite_duplicate.value_counts()[True]):,}',
          'duplicate hits between input tables',
          '(provided sentence is longer than 10 tokens).')
    singletons = df.loc[~definite_duplicate,
                        ['adv_lemma', 'adj_lemma', 'token_str']]
    # init_sent_counts=df.token_str.value_counts(sort=False).sort_index()
    # filter_sent_counts=singletons.token_str.value_counts(sort=False).sort_index()
    # sent_diff = init_sent_counts - filter_sent_counts
    # sent_with_dup = len(sent_diff[sent_diff != 0].index)
    # print(f'  ⨳ {sent_with_dup:,} initial sentences had 1+ duplicates')

    # all_dup = df.duplicated(['token_str', 'text_window'], keep=False)
    # print('Examples of duplication:')
    # print((df.loc[all_dup & over_10_tok,
    #               ['tok_in_sent', 'token_str']]).sort_values(['token_str'
    #                                                           ]).head(8))

    return singletons[['adv_lemma', 'adj_lemma']].astype('string')


def _drop_odd_orth(df: pd.DataFrame) -> pd.DataFrame:

    print('\nRemoving lemmas with abnormal orthography...')
    # full_df = df
    # df = df[['adv_lemma', 'adj_lemma']]
    J = df.adj_lemma
    J_filter = ~pd.Series(
        J.str.startswith(('-', '&', '.'))
        | J.str.endswith(('-', '&'))
        | J.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))
    # print((J_filter.value_counts(
    #     normalize=True).multiply(100).round(3).to_frame('%_of_adj').assign(
    #         status=['kept', 'dropped'], adj_tokens=J_filter.value_counts()).
    #     set_index('status').to_markdown()), '\n')

    R = df.adv_lemma
    R_filter = ~pd.Series(
        R.str.startswith(('-', '&', '.')) | R.str.endswith(('-', '&'))
        | R.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))
    # print((R_filter.value_counts(
    #     normalize=True).multiply(100).round(3).to_frame("%_of_adv").assign(
    #         status=['kept', 'dropped'], adv_tokens=R_filter.value_counts()).
    #     set_index('status').to_markdown()), '\n')

    # return full_df.loc[J_filter & R_filter, :]
    return df.loc[J_filter & R_filter, :]


def _drop_infreq(df, token_percent) -> pd.DataFrame:
    ts = pd.Timestamp.now()
    clean_token_count = len(df)
    # must keep at least 15% of the initial hits
    must_keep = round(clean_token_count * 0.15)
    n_dropped = len(df)
    filter_applied = 0
    filter_attempt = 0
    while n_dropped > 0:
        filter_attempt += 1
        # TODO: The info printed doesn't communicate these alternate options, and the code for applying them isn't great.
        # #* Best to use a reasonable value (i.e. [0.00001:1]%)
        token_thresh = _get_count_thresh(token_percent, clean_token_count)
        if token_thresh < 2:
            token_thresh = 2
            token_percent = token_thresh / clean_token_count * 100
            print('Given percentage is too low to remove anything.',
                  f'Set values to minimum {token_thresh} hit tokens/lemma')
            print(f'  ≈ {round(token_percent,6)}% of clean hits')
        if filter_attempt == 0:
            print('\nLimiting by total lemma frequency',
                  f'threshold ≥ {token_thresh:,} tokens per lemma...')

        update_df = _get_update(df, token_thresh)
        n_remain = len(update_df)
        n_dropped = len(df) - n_remain

        # * Evaluate if `n_dropped` (hits dropped this pass), yields ideal result.
        # *  -> If not, adjust threshold.
        adjust_str = ''
        # > if _no/too few_ hits were dropped (overall) ~ 95+% of initial hits remain...
        #! use `n_remain` to evaluate because `n_dropped` is only for CURRENT attempt
        # > or if median count for either lemma type is less than 5
        if (n_remain >= 0.975 * clean_token_count
                or any(_describe_str_lemma_counts(update_df).T['50%'] < 5)):
            # > raise percentage threshold --> increase by 1/4
            adjust_str = '◔ Insufficient Reduction: 🔺raising'
            token_percent *= 1.25
            if n_dropped <= 0:
                #! must also reset `n_dropped` to stay in `while` loop
                n_dropped = 1

        # > hits were dropped in this attempt...
        elif n_dropped > 0:

            # > if _too many_ hits were dropped...
            if ((n_remain < must_keep)
                        # keep at least 20 unique adv
                        or (count_uniq(update_df.adv_lemma) < 20)
                        # keep at least 40 unique adj
                    or (count_uniq(update_df.adj_lemma) < 40)
                    ):

                if not filter_applied and filter_attempt < 5:
                    # > lower percentage threshold --> reduce by 1/4
                    adjust_str = '◕ Excessive Reduction: 🔻lowering'
                    token_percent *= 0.75

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
                      f'having fewer than {token_thresh:,} total tokens...')
                df = update_df

        # > sufficient hits have been removed, just not in this round
        else:
            print('✓ No further infrequent lemmas found.',
                  'Frequency filtering complete!')

        if adjust_str:

            print(f'⚠️  ({filter_attempt}) Token threshold of',
                  f'{token_thresh:,} tokens/lemma failed.')
            # > update token count threshold from new percentage
            token_thresh = _get_count_thresh(token_percent, clean_token_count)
            print(f'  {adjust_str} percentage for threshold by 1/4')
            print(f'    updated threshold: {token_thresh:,} tokens,',
                  f'      ~{token_percent:.5}% of initial (clean) hits')

    te = pd.Timestamp.now()
    print(
        f'> {(clean_token_count - len(df)):,} total hits dropped due to infrequncy',
        f'(lemma(s) with fewer than {token_thresh:,} hits',
        f'~{round(token_percent,5)}% ',
        f'of initial hits) across {filter_applied} filtering pass(es).\n',
        f'[ time elapsed = {get_proc_time(ts, te)} ]')

    print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))
    print(f'\n>>> {len(df):,} total remaining hits <<<')

    return df


def _get_count_thresh(token_percent: float, clean_token_count: int) -> int:
    return int(round(clean_token_count * (token_percent / 100)))


def _get_update(df, token_thresh):
    indexers = []
    # print('Initial (clean) distribution info')
    # print(_describe_lemma_counts(df).to_markdown())
    print('Compiling frequency table update:')
    for i, col in enumerate(df.columns):
        print(f'  ({i+1}) restricting `{col}` column...')
        col_counts = df[col].value_counts()

        lemmas_over_thresh = col_counts[col_counts >= token_thresh].index

        indexers.append(df[col].isin(lemmas_over_thresh))

    update_df = df.loc[indexers[0] & indexers[1], :]
    print('Potential Update:')
    up_st = _describe_str_lemma_counts(update_df).T
    up_st = (up_st
             .assign(range=up_st['max'] - up_st['min'],
                     iqr=up_st['75%'] - up_st['25%'])
             .round())
    print(f'{(len(df) - len(update_df)):,} potential removals')
    print(up_st[['mean', '50%', 'iqr', 'range']].to_markdown(floatfmt=',.0f'))
    _print_uniq_lemma_count(update_df)

    return update_df


def _make_freq_tables(frq_out_dir: Path,
                      df: pd.DataFrame,
                      frq_thresh,
                      n_files: int,
                      group_code: str = 'all') -> None:
    """locate or create frequency tables: crosstabulated `adv_lemma` x `adj_lemma` counts. 

    If file exists, load it and collect descriptive stats and, if it is small enough, create corresponding heatmap visualization.

    If it does not exist, run crosstabulation on `adv_lemma` and `adj_lemma` columns. The collect stats and create heatmap (if table is small enough).

    Args:
        frq_out_dir (Path): location to save frequency tables, descriptive stats, and any heatmaps.
        df (pd.DataFrame): dataframe containing `adv_lemma` and `adj_lemma` columns at the minimum
        frq_thresh (_type_): minimum number of tokens per lemma in data
        n_files (int): number of files the current data is sourced from (~ # corpus chunks)
        group_code (str, optional): set to 'JxR' to filter df on subset of lemmas read in from `lexical_categories`. If 'JxR' is given, all output files will be saved to subdirectory, `../freq_out/JxR/`. Defaults to all.
    """

    if group_code != 'all':
        frq_out_dir = frq_out_dir.joinpath(group_code)
        if not frq_out_dir.is_dir():
            frq_out_dir.mkdir()

    out_stem = f'{group_code}-frq_thresh{frq_thresh}.{n_files}f'

    title = (f'{group_code} adj x adv frequency'
             .replace('JxR', 'scale diagnostics'))
    frq_df = _find_prior_freq_out(frq_out_dir, out_stem, title)

    if frq_df.empty:
        frq_df = _build_frq_df(df, group_code)
        save_table(frq_df,
                   frq_out_dir.joinpath(out_stem),
                   title, formats=['csv'])

    _describe_counts(
        frq_df,
        frq_out_dir.joinpath(f'descriptive_stats/stats_{out_stem}'))

    if len(frq_df) < 200 and len(frq_df.columns) < 100:
        heatmap(frq_df,
                save_name=f'heatmap_{group_code}-thresh{frq_thresh}.{n_files}f.png',
                save_dir=frq_out_dir.joinpath('images'))


def _find_prior_freq_out(frq_out_dir: Path,
                         frq_stem: str,
                         frq_title: str) -> pd.DataFrame:
    frq_df = pd.DataFrame()
    frq_df_paths = tuple(frq_out_dir.glob(f'{frq_stem}*'))
    if frq_df_paths:
        frq_df_path = frq_df_paths[0]
        print(frq_title, 'processing found. Loading from', frq_df_path)
        if frq_df_path.suffix.endswith('csv'):
            frq_df = pd.read_csv(frq_df_path)
            frq_df.columns = frq_df.columns.str.strip()
            frq_df = frq_df.set_index('adj_lemma')
        elif '.pkl' in frq_df_path.suffixes:
            frq_df = pd.read_pickle(frq_df_path)
            frq_df = frq_df.set_index('adj_lemma')
    return frq_df


def _build_frq_df(df: pd.DataFrame,
                  group_code: str) -> pd.DataFrame:
    rdf = df
    if group_code.lower() != 'all':
        J, __ = unpack_dict(SAMPLE_ADJ)
        R, __ = unpack_dict(SAMPLE_ADV, values_name='adv')
        rdf = df.loc[df.adj_lemma.isin(J)
                     & df.adv_lemma.isin(R), :].astype('string')

    frq_df = sort_by_margins(
        pd.crosstab(index=rdf.adj_lemma,
                    columns=rdf.adv_lemma,
                    margins=True,
                    margins_name='SUM'))
    return frq_df


def _describe_counts(df: pd.DataFrame,
                     out_path_stem: str) -> None:
    df = df.fillna(0)
    for frame, pos in ((df, 'Adverb'), (df.transpose(), 'Adjective')):

        print(f'\n## Descriptive Statistics by {pos}')
        no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
        desc_sep = no_sum_frame.describe()
        # > need to exclude the ['SUM','SUM'] cell
        sum_col = frame.loc[frame.index != 'SUM', 'SUM']
        desc_sum = sum_col.describe().to_frame()
        for desc, values in zip((desc_sep, desc_sum), (no_sum_frame, sum_col)):
            desc = _enhance_descrip(desc, values)
            if 'SUM' in desc.index:
                desc = desc.transpose()
                desc.columns = [f'Summed Across {pos}s']
            else:
                save_table(
                    desc,
                    f'{out_path_stem.parent}/{pos[:3]}-{out_path_stem.name}',
                    f'{pos} descriptive statististics for {out_path_stem.stem}',
                    ['csv'])
                # ? #TODO: add simple output of just `df.var_coeff`?
                # desc.info()
            print(desc.head(10).round().to_markdown(floatfmt=',.0f') + '\n')


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

    # mean_centr = no_sum_frame - no_sum_frame.mean()
    # mean_stand = no_sum_frame / no_sum_frame.mean()
    # mean_stand_centr = mean_stand - mean_stand.mean()
    # log2_trans = no_sum_frame.apply(np.log2)
    # log2_plus1_trans = no_sum_frame.add(1).apply(np.log2)
    # logn_plus1_trans = no_sum_frame.apply(np.log1p)

    return desc


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
