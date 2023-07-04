import argparse
import statistics as stat
from pathlib import Path

# import numpy as np
import pandas as pd
from utils.dataframes import (count_uniq, get_proc_time, save_table,
                              sort_by_margins, unpack_dict)
from utils.general import print_iter
from utils.LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV
from utils.visualize import heatmap

N_EX = 3


def _main():
    print(pd.Timestamp.now().ctime())
    n_files, tok_thresh_p, post_proc_dir, frq_out_dir = _parse_args()
    tok_thresh_c = None
    print("Collecting sample vocabulary frequencies for",
          f"{n_files} *hits.pkl.gz files")
    #// post_proc_dir = Path('/share/compling/data/sanpi/4_post-processed')
    #// frq_out_dir = Path('/share/compling/projects/sanpi/results/freq_out')

    for d in (frq_out_dir, post_proc_dir):
        if not d.is_dir():
            d.mkdir(parents=True)
    pkl_suff = f'{n_files}f.pkl.gz'
    clean_bigrams_pkl = post_proc_dir.joinpath(f'bigrams_clean.{pkl_suff}')
    print(f'Hits Data Path:\n  >> {clean_bigrams_pkl}')

    th_bigrams_pkl = post_proc_dir.joinpath(
        f"bigrams-only_thr{str(tok_thresh_p).replace('.','-')}p.{pkl_suff}")
    #// th5_bigrams_pkl = post_proc_dir.joinpath(
    #//     f'bigrams-only_thresh5.{pkl_suff}')

    _t0 = pd.Timestamp.now()
    print('\n## loading data...')
    if th_bigrams_pkl.is_file():
        print(f' * Found previous output. Loading data from {th_bigrams_pkl}...')
        df = pd.read_pickle(th_bigrams_pkl).convert_dtypes()
        tok_thresh_c = int(_describe_str_lemma_counts(df).loc['min', :].min())
        print('   ⌖ minimum hits/lemma in data: {:,}'.format(tok_thresh_c))
        
    else:

        if clean_bigrams_pkl.is_file() and n_files < 15:
            print(
                f' * Found previous output. Loading data from {clean_bigrams_pkl}'
            )
            df = pd.read_pickle(clean_bigrams_pkl)
            if df.index.name != 'hit_id':
                df = df.set_index('hit_id')
        else:
            df = _load_data(n_files)
            if df.index.name != 'hit_id':
                df = df.set_index('hit_id')
            print('\n> {:,} initial hits'.format(len(df)))
            # print('= intial unique lemmas:')
            _print_uniq_lemma_count(df, updated=False,)
            print(_describe_str_lemma_counts(df).round().to_markdown(floatfmt=',.0f'))
            df = _clean_data(df)
            if n_files < 15:
                save_table(df,
                           str(clean_bigrams_pkl).split('.pkl', 1)[0],
                           "cleaned bigram hits")

        #> drop infrequent adv & adj lemmas
        df = _drop_infreq(df, tok_thresh_p)
        tok_thresh_c = int(_describe_str_lemma_counts(df).loc['min', :].min())
        save_table(
            df,
            str(th_bigrams_pkl).split('.pkl', 1)[0],
            f'restrictred bigrams ({tok_thresh_c}+ frequency threshold)')

    print(df.describe().transpose().to_markdown(floatfmt=',.0f'))
    _t1 = pd.Timestamp.now()
    print('✓ time:', get_proc_time(_t0, _t1))

    _t0 = pd.Timestamp.now()
    #! #BUG where `tok_thresh_c` is not defined if full freq limited frequency df was already pickled and loaded as input
    # #HACK: ideally above bug should be dealt with more cleanly
    # if tok_thresh_c is None: 
    #     tok_thresh_c = _describe_str_lemma_counts(df).loc['min', :].min()
    #? 🤔 does this need to change to use the same percent notation used for the other paths anyway?
    _make_freq_tables(frq_out_dir, df, tok_thresh_c, n_files)
    #* uncomment below line to analyze subset of lemmas as described by `SAMPLE_ADJ` & `SAMPLE_ADV`
    # _make_freq_tables(frq_out_dir, df, tok_thresh_c, n_files, group_code='JxR')
    _t1 = pd.Timestamp.now()
    print('Time to get frequencies:', get_proc_time(_t0, _t1))


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-f',
        '--n_files',
        type=int,
        default=2,
        help=
        ('number of dataframe `.pkl.gz` files to load from `../hit_tables/advadj/` '
         '(divided by corpus chunk/slice). '
         'Files are sorted by size so smaller files are selected first. '
         '(i.e. `f=5` will load the 5 smallest tables of hits)'))

    parser.add_argument(
        '-t',
        '--token_threshold',
        type=float,
        default=0.001,
        help=
        ('[ARGUMENT IS CURRENTLY BEING MODIFIED! FOLLOWING MAY NOT BE TRUE]'
         'Minimum number of tokens required per lemma (in total) for lemma to be included. '
         'Any adverb or adjective lemma which does not meet this minimum frequency '
         'threshold (combined with any other lemma) will be dropped. '
         'If no value is given, threshold defaults to `n_files * 5`.'
         'NOTE: This filter is applied 2x, with sums recalculated after the 1st'
         ' set of lemmas and their correpsonding bigram tokens are dropped.'))

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
        help=
        ('Path to location for bigram frequency results (adj_lemma x adv_lemma tables). '
         'Name of file(s) generated from `n_files` and `tok_threshold`'))

    args = parser.parse_args()

    if args.token_threshold is None:
        tok_thresh = args.n_files * 5
    else:
        tok_thresh = args.token_threshold

    return args.n_files, tok_thresh, args.post_proc_dir, args.frq_out_dir


def _load_data(n_files):
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


def _select_pickles(n_files):
    pickle_dir = Path('/share/compling/data/sanpi/2_hit_tables/advadj')
    # > make dataframe to load smallest files first (for testing)
    pkl_df = pd.DataFrame(pickle_dir.glob('bigram-*hits.pkl.gz'),
                          columns=['path'])
    pkl_df = pkl_df.assign(size=pkl_df.path.apply(lambda f: f.stat().st_size))
    pkl_paths = pkl_df.sort_values('size').head(n_files).reset_index().path
    return pkl_paths


def _select_cols(df,
                 #  target_adj, target_adv
                 ):
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


def _clean_data(df):
    #> print overview of initial data
    print('\nCleaning up hits: removing duplicated or exceptionally',
          'long sentences, strange orthography, and random capitals.')
    starting_token_count = len(df)
    ts = pd.Timestamp.now()
    # > removing duplicates
    if 'token_str' in df.columns and 'text_window' in df.columns:
        df = _drop_long_sents(df)
        df = _drop_duplicate_sents(df)

    valid_token_count = len(df)
    print(
        f'\n> {starting_token_count - valid_token_count} hits from invalid sentences removed.'
    )
    print('~ unique lemmas for hits in valid sentences:')
    _print_uniq_lemma_count(df)
    print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))

    #> set dtype to string and remove random capitalizations
    print('\nNormalizing lemma case (making everything lower case)...')
    df = df.assign(adv_lemma=df.adv_lemma.str.lower(),
                   adj_lemma=df.adj_lemma.str.lower())
    _print_uniq_lemma_count(df)

    #> drop lemmas with abnormal orthography
    df = _drop_odd_orth(df)
    te = pd.Timestamp.now()
    print('> {:,} total suspect hits'.format(starting_token_count - len(df)),
          f' removed in {get_proc_time(ts, te)}')
    _print_uniq_lemma_count(df)
    print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))

    return df


def _print_uniq_lemma_count(df: pd.DataFrame,
                            cols: list = [],
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
    counts = ['{0:<{1}s}:  {2:>{3},d}'.format(k, str_len, v, num_len)
              for k, v in counts_info.items()]
    print_iter(counts,
               header=f'{head_mark} unique lemmas in {label} hits',
               indent=2)


def _describe_str_lemma_counts(df):
    lemma_stats = (df.columns[df.columns.str.endswith('_lemma')]
                   .to_series().apply(
                       lambda c: df[c].value_counts().describe())
                   ).T
    lemma_stats.columns = lemma_stats.columns.str.replace('lemma', 'counts')
    # lemma_stats = (
    #     df.adv_lemma.value_counts().describe().to_frame('adv_counts').assign(
    #         adj_counts=df.adj_lemma.value_counts().describe()))
    return lemma_stats.round()


def _drop_long_sents(df):
    starting_df = df.copy()
    df = df.assign(tok_in_sent=df.token_str.apply(lambda s: len(s.split())))
    sent_limit = 250
    too_long = df.tok_in_sent > sent_limit
    uniq_too_long = df.loc[too_long, :].index.str.split(":",
                                                        1).str.get(0).unique()
    print(f'Dropping {too_long.value_counts()[True]} hits',
          f'from {len(uniq_too_long)} "sentences" with',
          f'{sent_limit}+ tokens. For example:\n```')
    print((starting_df.loc[df.index.str.startswith(tuple(uniq_too_long)),
                           ['token_str']]).sample(1).squeeze()[:550] +
          '...\n```')
    df = df.loc[~too_long, :]
    return df


def _drop_duplicate_sents(df):
    over_10_tok = df.tok_in_sent > 10
    is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
    definite_duplicate = over_10_tok & is_duplicate_hit
    print(f'\nↀ  Removing {definite_duplicate.value_counts()[True]}',
          'duplicate hits between input tables (provided sentence is',
          'over 10 tokens long). Examples:')
    all_dup = df.duplicated(['token_str', 'text_window'], keep=False)
    print((df.loc[all_dup & over_10_tok,
                  ['tok_in_sent', 'token_str']]).sort_values(['token_str'
                                                              ]).head(8))
    df = df.loc[~definite_duplicate,
                ['adv_lemma', 'adj_lemma']].astype('string')

    return df


def _drop_odd_orth(df):
    print('\nRemoving lemmas with abnormal orthography...')
    J = df.adj_lemma
    J_filter = ~pd.Series(
        J.str.startswith(('-', '&', '.'))
        | J.str.endswith(('-', '&'))
        | J.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))
    print((J_filter.value_counts(
        normalize=True).multiply(100).round(3).to_frame('%_of_adj').assign(
            status=['kept', 'dropped'], adj_tokens=J_filter.value_counts()).
           set_index('status').to_markdown()), '\n')

    R = df.adv_lemma
    R_filter = ~pd.Series(
        R.str.startswith(('-', '&', '.')) | R.str.endswith(('-', '&'))
        | R.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))
    print((R_filter.value_counts(
        normalize=True).multiply(100).round(3).to_frame("%_of_adv").assign(
            status=['kept', 'dropped'], adv_tokens=R_filter.value_counts()).
           set_index('status').to_markdown()), '\n')

    df = df.loc[J_filter & R_filter, :]
    return df


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
        #* Best to use a reasonable value (i.e. [0.00001:1]%)
        token_thresh = _get_count_thresh(token_percent, clean_token_count)
        if token_thresh < 2:
            token_thresh = 2
            token_percent = token_thresh / clean_token_count * 100
            print('Given percentage is too low to remove anything.',
                  f'Set values to minimum {token_thresh} hit tokens/lemma')
            print(f'  ≈ {round(token_percent,6)}% of clean hits')
        if filter_attempt == 0:
            print('\nLimiting by total lemma frequency',
                  'threshold ≥ {:,} tokens per lemma...'.format(token_thresh))

        update_df = _get_update(df, token_thresh)
        n_remain = len(update_df)
        n_dropped = len(df) - n_remain

        #* Evaluate if `n_dropped` (hits dropped this pass), yields ideal result.
        #*  -> If not, adjust threshold.
        adjust_str = ''
        #> if _no/too few_ hits were dropped (overall) ~ 95+% of initial hits remain...
        #! use `n_remain` to evaluate because `n_dropped` is only for CURRENT attempt
        #> or if median count for either lemma type is less than 5
        if (n_remain >= 0.97 * clean_token_count
                or any(_describe_str_lemma_counts(update_df).T['50%'] < 5)):
            #> raise percentage threshold --> increase by 1/4
            adjust_str = '◔ Insufficient Reduction: 🔺raising'
            token_percent *= 1.25
            if n_dropped <= 0:
                #! must also reset `n_dropped` to stay in `while` loop
                n_dropped = 1

        #> hits were dropped in this attempt...
        elif n_dropped > 0:

            #> if _too many_ hits were dropped...
            if (n_remain < must_keep or count_uniq(update_df.adv_lemma) <
                    20  # keep at least 20 unique adverbs
                    or count_uniq(update_df.adj_lemma) <
                    40  # keep at least 40 unique adjectives
                ):

                if not filter_applied and filter_attempt < 5:
                    #> lower percentage threshold --> reduce by 1/4
                    adjust_str = '◕ Excessive Reduction: 🔻lowering'
                    token_percent *= 0.75

                else:
                    print(
                        '! More lemmas fall below the threshold, but removing them violates other restrictions.'
                    )
                    n_dropped = 0

            #* if `n_dropped` is ideal, udpate `df` to `update_df`
            else:
                filter_applied += 1
                print(
                    f'Successful pass #{filter_applied} (attempt',
                    f'#{filter_attempt}):\n',
                    'removing {:,} hits containing lemmas'.format(n_dropped),
                    'having fewer than {:,} total tokens...'.format(
                        token_thresh))
                df = update_df

        #> sufficient hits have been removed, just not in this round
        else:
            print(
                '✓ No further infrequent lemmas found. Frequency filtering complete!'
            )

        if adjust_str:

            print('⚠️  ({}) Token threshold of'.format(filter_attempt),
                  '{:,} tokens/lemma failed.'.format(token_thresh))
            token_thresh = _get_count_thresh(token_percent, clean_token_count)
            print(f'  {adjust_str} percentage for threshold by 1/4')
            print('    updated threshold: {:,} tokens,'.format(token_thresh),
                  '      ~{:.5}% of initial (clean) hits'.format(token_percent))

    te = pd.Timestamp.now()
    print(
        '> {:,} total hits dropped due to infrequncy'.format(clean_token_count - len(df)),
        '(lemma(s) with fewer than {:,} hits'.format(token_thresh),
        f'~{round(token_percent,5)}% ',
        f'of initial hits) across {filter_applied} filtering pass(es).\n',
        f'[ time elapsed = {get_proc_time(ts, te)} ]')
    # print('+ unique lemmas in updated hits:')
    _print_uniq_lemma_count(df)
    print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))
    print('\n>>> {:,} total remaining hits <<<'.format(len(df)))
    # adv_th = df.adv_lemma.value_counts() > token_thresh
    # df = df.loc[df.adv_lemma.isin(adv_th[adv_th].index), :]

    # #> freq for limiting adj calculated *after* removing rare adv
    # adj_th = df.adj_lemma.value_counts() > token_thresh
    # df = df.loc[df.adj_lemma.isin(adj_th[adj_th].index), :]
    # round1_len = len(df)
    # print(f'{init_token_count - round1_len} hits/rows dropped in first round.')
    # #> run through the weed out process again, in case dropped rows put items below threshold
    # adv_th = df.adv_lemma.value_counts() > token_thresh
    # df = df.loc[df.adv_lemma.isin(adv_th[adv_th].index), :]
    # adj_th = df.adj_lemma.value_counts() > token_thresh
    # df = df.loc[df.adj_lemma.isin(adj_th[adj_th].index), :]
    # #> set dtype to 'category' _after_ dropping rare items
    # df = df.assign(adj_lemma=df.adj_lemma.astype('category'),
    #                adv_lemma=df.adv_lemma.astype('category'))
    # te = pd.Timestamp.now()
    # print(clean_token_count - len(df), 'total tokens with infrequent lemmas removed in',
    #       get_proc_time(ts, te))
    # print('+ updated unique lemmas:')
    # _print_uniq_lemma_count(df)
    return df


def _get_count_thresh(token_percent, clean_token_count):
    return round(clean_token_count * (token_percent / 100))


def _get_update(df, token_thresh):
    indexers = []
    # print('Initial (clean) distribution info')
    # print(_describe_lemma_counts(df).to_markdown())
    for col in df.columns:
        col_counts = df[col].value_counts()

        # old
        lemmas_over_thresh = col_counts[col_counts >= token_thresh].index
        indexers.append(df[col].isin(lemmas_over_thresh))
        # print(f'\nFiltering {col.upper()}...')
        # #* new
        # #^ #TODO this is a new stab at dropping lemmas in a motivated way. Commit all other changes first, before going any further with this.
        # floor = 1
        # init_mean = col_counts.mean()
        # while col_counts.median() < (init_mean * .99) :
        #     floor += 1
        #     col_counts = col_counts.loc[col_counts >= floor]
        #     #^ Also remove **most** common?
        #     col_counts = col_counts.iloc[1:]
        # print(f'final minimum count retained: {floor}\n')
        # print(col_counts)
        # print(col_counts.describe().to_frame(f"{col.replace('lemma', '')}only_optimized").to_markdown())
        # lemmas_over_thresh = col_counts.index

        # indexers.append(df[col].isin(lemmas_over_thresh))

    update_df = df.loc[indexers[0] & indexers[1], :]
    print('Potential Update:')
    up_st = _describe_str_lemma_counts(update_df).T
    up_st = (up_st
             .assign(range=up_st['max'] - up_st['min'],
                     iqr=up_st['75%'] - up_st['25%'])
             .round())
    print(up_st[['mean', '50%', 'iqr', 'range']].to_markdown(floatfmt=',.0f'))
    _print_uniq_lemma_count(update_df)
    return update_df


def _make_freq_tables(frq_out_dir:Path, 
                      df: pd.DataFrame, 
                      frq_thresh, 
                      n_files:int, 
                      group_code:str = 'all'):
    """_summary_

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
    # all_frq_stem = 
    # JxRfrq_stem = f'JxR-frq_thresh{frq_thresh}.{n_files}f'
    title = (f'{group_code} adj x adv frequency'
                .replace('JxR', 'scale diagnostics'))
    frq_df = _find_prior_freq_out(frq_out_dir, out_stem, title)
    # xfrq = _find_prior_freq_out(frq_out_dir, all_frq_stem, all_frq_title)
    # JxRfrq = _find_prior_freq_out(frq_out_dir, JxRfrq_stem, JxRfrq_title)    
    if frq_df.empty:
        frq_df = _build_frq_df(df, group_code)
        save_table(frq_df,
                frq_out_dir.joinpath(out_stem),
                title, formats=['csv'])

    _describe_counts(
        frq_df, frq_out_dir.joinpath(f'descriptive_stats/stats_{out_stem}'))
    
    if len(frq_df) < 200 and len(frq_df.columns) < 100:
        heatmap(frq_df,
                save_name=f'heatmap_{group_code}-thresh{frq_thresh}.{n_files}f.png',
                save_dir=frq_out_dir.joinpath('images'))


def _find_prior_freq_out(frq_out_dir, frq_stem, frq_name):
    frq_df = pd.DataFrame()
    frq_df_paths = tuple(frq_out_dir.glob(f'{frq_stem}*'))
    if frq_df_paths:
        frq_df_path = frq_df_paths[0]
        print(frq_name, 'processing found. Loading from', frq_df_path)
        if frq_df_path.suffix.endswith('csv'):
            frq_df = pd.read_csv(frq_df_path)
            frq_df.columns = frq_df.columns.str.strip()
            frq_df = frq_df.set_index('adj_lemma')
        elif '.pkl' in frq_df_path.suffixes:
            frq_df = pd.read_pickle(frq_df_path)
            frq_df = frq_df.set_index('adj_lemma')
    return frq_df


def _build_frq_df(df, group_code):
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

    # if JxRfrq.empty:
        
    #     # JxRcat = JxR.assign(
    #     #     adj_lemma=pd.Categorical(JxR.adj_lemma, categories=J),
    #     #     adv_lemma=pd.Categorical(JxR.adv_lemma, categories=R),
    #     #     )
    #     JxRfrq = pd.crosstab(index=JxR.adj_lemma,
    #                          columns=JxR.adv_lemma,
    #                          margins=True,
    #                          margins_name='SUM')
    #     found_J = J_df.index.isin(JxRfrq.index)
    #     found_R = R_df.index.isin(JxRfrq.columns)
    #     # JxRcatfrq = pd.crosstab(index=JxRcat.adj_lemma, columns=JxRcat.adv_lemma, margins=True, margins_name='SUM')
    #     JxRfrq = JxRfrq.loc[J_df[found_J].index.to_list() + ['SUM'],
    #                         R_df[found_R].index.to_list() + ['SUM']]
    #     save_table(JxRfrq,
    #                frq_out_dir.joinpath(JxRfrq_stem),
    #                JxRfrq_title,
    #                formats=['csv'])

    # _describe_counts(
    #     JxRfrq, frq_out_dir.joinpath(f'descriptive_stats/stats_{JxRfrq_stem}'))


def _describe_counts(df, out_path_stem):
    df = df.fillna(0)
    for frame, pos in ((df, 'Adverb'), (df.transpose(), 'Adjective')):

        print(f'\n## Descriptive Statistics by {pos}')
        no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
        desc_sep = no_sum_frame.describe()
        #> need to exclude the ['SUM','SUM'] cell
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
                #? #TODO: add simple output of just `df.var_coeff`?
                # desc.info()
            print(desc.head(10).round().to_markdown(floatfmt=',.0f') + '\n')

def _enhance_descrip(desc, values):
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



# removed methods
#// def visualize(outdf_path, df):
#// type_abbr = {
#//     'NON_G': 'N',
#//     'OPEN': 'O',
#//     'LOW_CLOSE': 'L',
#//     'UP_CLOSE': 'U',
#//     'TOT_CLOSE': 'T'
#// }
#// # compare_abbr = compare.rename(
#// #     columns=type_abbr)
#// # show_examples(compare, compare_abbr, outdf_path, type_abbr)
#// # show_adv_of_interest(compare, compare_abbr, outdf_path, type_abbr)
#// # show_ppi_adv(compare_abbr, outdf_path, type_abbr)
#// show_all(df, outdf_path, type_abbr)

#// def show_examples(compare, compare_abbr, outdf_path, type_abbr):
#// examples = pick_examples(compare)
#// examples_df = (compare_abbr.loc[compare_abbr.index.isin(examples), :]
#//                .sort_values('total_count', ascending=False))
#// print('\n' + examples_df.round(2).to_markdown())
#// heatmap(
#//     examples_df,
#//     type_abbr.values(),
#//     outdf_path.with_suffix('.heat-ex.png').name
#// )

#// def pick_examples(compare):
#// examples = []
#// ci = compare.sort_values('total_count').head(int(len(compare)/2))
#// for scale_type in SCALE_TYPES:
#//     type_ci = ci[scale_type]
#//     examples += type_ci.nlargest(N_EX).index.to_list()
#//     examples += type_ci.nsmallest(N_EX).index.to_list()
#// examples = list(set(examples))
#// examples.sort()
#// print('\nMost divergent adjectives (of 50% most frequent) for each scale type:' +
#//       ''.join(f'\n ¤ {e}' for e in examples))
#// return examples

#// def show_adv_of_interest(compare, compare_abbr, outdf_path, type_abbr):
#// key_adv_found = set(compare.index[compare.index.isin(ADV_OF_INTEREST)])
#// compare_key = compare_abbr.loc[list(key_adv_found), :]
#// top_30 = compare_key.total_count.nlargest(30).index
#// all_key_df = compare_key.sort_values('total_count', ascending=False)
#// print('\n' + all_key_df.round(2).to_markdown())
#// heatmap(
#//     all_key_df.loc[top_30, :],
#//     type_abbr.values(),
#//     outdf_path.with_suffix('.heat-key.png').name
#// )

#// heatmap(
#// all_key_df,
#// type_abbr.values(),
#// outdf_path.with_suffix('.heat-key.png').name.replace('_examples_', '_'))

#// def show_ppi_adv(compare_abbr, outdf_path, type_abbr):
#// compare_ppi = compare_abbr.loc[compare_abbr.index.isin(PPI_ADVERBS), :]
#// ppi_df = compare_ppi.sort_values('total_count', ascending=False)
#// print('\n' + ppi_df.round(2).to_markdown())
#// heatmap(
#//     ppi_df,
#//     type_abbr.values(),
#//     outdf_path.with_suffix(
#//         '.heat_ppi_m-mod.png').name.replace('_examples_', '_'),
#//     (10, 8)
#// )

#// def show_all(compare_abbr, outdf_path, type_abbr):
#// heatmap(
#//     compare_abbr.sort_values('total_count', ascending=False),
#//     type_abbr.values(),
#//     outdf_path.with_suffix('.heat-ALL.png').name.replace(
#//         '_examples_', '_'))

if __name__ == '__main__':
    _main()
