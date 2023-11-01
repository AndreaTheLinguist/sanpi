# coding=utf-8

#> Imports
import argparse
# from pprint import pprint
import statistics as stat
from pathlib import Path

# import numpy as np
import pandas as pd

from utils import (cols_by_str, confirm_dir, file_size_round, find_glob_in_dir, percent_to_count, print_iter,  # pylint: disable=import-error
                   count_uniq, get_proc_time, print_md_table, save_table,
                   select_cols, select_pickle_paths, sort_by_margins, unpack_dict)
from utils.LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV  # pylint: disable=import-error
from utils.visualize import heatmap  # pylint: disable=import-error

#> Globals
_SANPI_DIR = Path('/share/compling/projects/sanpi')
# _MIN_THRESH_COUNT = 2
# _MIN_TOK_KEEP_RATIO = 0.15
# _KEEP_ALLOWANCE_RATIO = 0.99
# _ADV_KEEP_REQ = 20
# _ADJ_KEEP_REQ = 40
# _MIN_MEDIAN = 5


def _main():
    print(pd.Timestamp.now().ctime())
    # (n_files, percent_thresh, data_dir,
    #  post_proc_dir, frq_out_dir, frq_groups) = _parse_args()
    (bigram_hits, hits_dir,
     frq_out_dir, frq_groups) = _parse_args()

    df = prepare_hit_table(
        bigram_hits,
        # n_files=n_files,
        # tok_thresh_p=percent_thresh,
        # post_proc_dir=post_proc_dir,
        neg_hits_dir=hits_dir)
    # frq_thresh = _summarize_hits(df)
    _summarize_hits(df)

    if not frq_groups:
        frq_groups = ['all']

    for group in frq_groups:

        _t0 = pd.Timestamp.now()
        #! #[ ] modify this to deal with relevant negation data
        frq_df, frq_df_path = get_freq_info(df, #n_files, frq_thresh,
                                            group, frq_out_dir)
        _t1 = pd.Timestamp.now()
        print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')

        _describe_counts(frq_df, frq_df_path)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # parser.add_argument(
        # '-f',
        # '--n_files',
        # type=int,
        # default=2,
        # help=('number of dataframe `.pkl.gz` files to load from `../hit_tables/advadj/` '
        #       '(divided by corpus chunk/slice). '
        #       'Files are sorted by size so smaller files are selected first. '
        #       '(i.e. `f=5` will load the 5 smallest tables of hits)'))

    # parser.add_argument(
        # '-t',
        # '--percent_hits_threshold',
        # type=float,
        # default=0.001,
        # help=('Minimum frequency threshold of hits per lemma (in total) for lemma to be included. '
        #       '**Specified as PERCENTAGE of total (cleaned) hits, not as explicit integer of hits!** '
        #       'Any adverb or adjective lemma which does not meet this minimum frequency '
        #       'threshold (combined with any other lemma) will be dropped. '
        #       'NOTE: This filter is applied iteratively, with sums recalculated after '
        #       'the previous set of lemmas and their correpsonding bigram tokens are dropped.'))

    parser.add_argument(
        '-b',
        '--bigram_hits',
        type=Path,
        default=Path(
            '/share/compling/data/sanpi/4_post-processed/RBXadj/bigrams-only_thr0-1p.35f.pkl.gz' #> 0.1% threshold
            # '/share/compling/data/sanpi/4_post-processed/RBXadj/bigrams-only_thr0-01p.35f.pkl.gz' #> 0.01% threshold
            # '/share/compling/data/sanpi/4_post-processed/RBXadj/bigrams-only_thr0-0005p.35f.pkl.gz' #> 0.0005% threshold
            ),
        help=('Path to table of all relevant bigrams. '
              '(i.e. indexed by `hit_id` => negation data `colloc_id`). '))

    parser.add_argument(
        '-d',
        '--hits_dir',
        type=Path,
        default=Path('/share/compling/data/sanpi/2_hit_tables/RBcontig'),
        help=('Path to location of original hit tables. '
              '(i.e. tables indexed by `hit_id`). '))

    parser.add_argument(
        '-o',
        '--frq_out_dir',
        type=Path,
        default=_SANPI_DIR.joinpath('results/freq_out/RBcontig'),
        help=('Path to location for frequency results (adj_lemma ✕ adv_lemma tables). '
              'Name of file(s) will correspond to `bigram_hits` path'))

    parser.add_argument(
        '-g', '--frequency_group',
        type=str, action='append', dest='frq_groups',
        default=[],
        help=('')
    )

    args = parser.parse_args()
    print_md_table(pd.Series(dict(list(args._get_kwargs()))).to_frame('arguments given'))
    return (args.bigram_hits, args.hits_dir,
            args.frq_out_dir.resolve(), set(args.frq_groups))


def prepare_hit_table(bigram_hits: Path,
                      # // n_files:int,
                      # // tok_thresh_p:float,
                      # // post_proc_dir: Path,
                      neg_hits_dir: Path):

    # sample_tag = 'sample' if n_files < 35 else ''
    # print(f"# Collecting {sample_tag} vocabulary frequencies for",
    #       f"{n_files} *hits.pkl.gz hit tables")

    # pkl_suff = f'{n_files}f.pkl.gz'
    # confirm_dir(post_proc_dir)
    print('\n+ size of bigram hits table:', file_size_round(bigram_hits.stat().st_size))
    bigrams = pd.read_pickle(bigram_hits)
    if bigrams.index.name == 'hit_id':
        colloc_ids = bigrams.index
    else:
        colloc_ids = bigrams.hit_id
    # clean_bigrams_pkl = post_proc_dir.joinpath(f'bigrams_clean.{pkl_suff}')
    # print(f'Cleaned Hits Table Path:\n  >> {clean_bigrams_pkl}')

    # th_bigrams_pkl = post_proc_dir.joinpath(
        # f"bigrams-only_thr{str(tok_thresh_p).replace('.','-')}p.{pkl_suff}")

    _t0 = pd.Timestamp.now()
    print('\n## loading data...')
    filtered_neg_hits = bigram_hits.parent.joinpath(
        f'neg_compare/{bigram_hits.name.replace("bigrams-only", neg_hits_dir.name)}')
    if filtered_neg_hits.is_file():
        print(f'* Found previous output. Loading data from {filtered_neg_hits}...')
        df = pd.read_pickle(filtered_neg_hits).convert_dtypes()

    else:
        # if clean_bigrams_pkl.is_file():
            # print('* Found previous output.',
            #       f'Loading data from {clean_bigrams_pkl}')
            # df = pd.read_pickle(clean_bigrams_pkl)
            # if df.index.name != 'hit_id':
            #     df = df.set_index('hit_id')
            # print_md_table(df.describe().T, indent=2,
            #                title='Clean Hits Summary')
            # print_md_table(_describe_str_lemma_counts(df),
            #                indent=2, title='Clean Lemma Counts Summary')

        # else:
        # df = pd.DataFrame()
        df = _load_data(ids=colloc_ids, data_dir=neg_hits_dir)
        if df.index.name != 'hit_id':
            df = df.set_index('hit_id')
        # print(f'\n> {len(df):,} initial hits')
        _print_uniq_lemma_count(df)
        print(_describe_str_lemma_counts(
            df).round().to_markdown(floatfmt=',.0f'))
        # clean_t0 = pd.Timestamp.now()
        # df = _clean_data(df)
        # clean_t1 = pd.Timestamp.now()
        # print('\n[ Time to clean combined hits dataframe:',
        # get_proc_time(clean_t0, clean_t1), ']')
        # print_md_table(_describe_str_lemma_counts(df))

        save_table(df,
                   str(filtered_neg_hits.resolve()).split('.pkl', 1)[0],
                   f"filtered {neg_hits_dir.name} hits")
        if len(df) < (10^6):
            save_table(df=df,
                    path_str=str(filtered_neg_hits.resolve()
                                    ).split('.pkl', 1)[0],
                    df_name=f"filtered {neg_hits_dir.name} hits",
                    formats=['psv', 'csv'])
             
        elif len(df) < (2 * 10^6): 
            save_table(df=df,
                    path_str=str(filtered_neg_hits.resolve()
                                    ).split('.pkl', 1)[0],
                    df_name=f"filtered {neg_hits_dir.name} hits",
                    formats=['psv'])

        # // > drop infrequent adv & adj lemmas
        # df = _drop_infreq(df, tok_thresh_p)
        # tok_thresh_c = int(_describe_str_lemma_counts(df).loc['min', :].min())
        # save_table(
            # df,
            # str(filtered_neg_hits).split('.pkl', 1)[0],
            # f'frequency restrictred bigrams ({tok_thresh_c}+ frequency threshold)')

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


def _load_data(ids, data_dir: Path) -> pd.DataFrame:
    # pkl_paths = select_pickle_paths(n_files, pickle_dir=data_dir)
    _ts = pd.Timestamp.now()
    df_iter = filter_hits(data_dir, ids)

    combined_df = pd.concat(df_iter)
    print_md_table(combined_df.describe().T.convert_dtypes(),
                   title='Combined Raw Hits Summary')

    _te = pd.Timestamp.now()
    print('> Time to create composite hits dataframe:',
          get_proc_time(_ts, _te))

    return combined_df


def filter_hits(data_dir: Path, ids: pd.Series):
    for i, p in enumerate(data_dir.glob('*hits.pkl.gz')):
        try:
            print_path = p.relative_to(Path("/share/compling/data"))
        except ValueError:
            print_path = p.resolve().relative_to(Path("/share/compling/projects"))

        print(f'\n{i+1}. ../{print_path}')
        print('   + size:', file_size_round(p.stat().st_size))
        # # check for previous simplification
        # simple_out_dir = p.parent.joinpath('simple')
        # if not simple_out_dir.is_dir():
        #     simple_out_dir.mkdir(parents=True)
        # simple_hits_pkl = simple_out_dir.joinpath('S_' + p.name)

        # if simple_hits_pkl.is_file():
            # print(
            #     f'   * Found previous output.\n     Loading data from `../{Path(*simple_hits_pkl.parts[-4:])}`'
            # )
            # try:
            #     df = pd.read_pickle(simple_hits_pkl)
            # except EOFError:
            #     print(" ⚠️ simplified file unreadable. Loading original...")
            #     df = simplify_table(p, simple_hits_pkl)

        # else:
        #     df = simplify_table(p, simple_hits_pkl)
        df = pd.read_pickle(p)
        # > select relevant columns
        df = _select_columns(df)


        print('   + Before filtering to target bigrams only')
        desc_t = df.select_dtypes(exclude='object').describe().T.convert_dtypes()
        print_md_table(desc_t.sort_index(), n_dec=0, comma=True,
                       indent=5, title=f'({i+1}) `{p.stem}` summary')

        # > filter to kept bigrams
        #! categories need to be reverted to strings before filtering 
        # and then redefine categories after rows are removed.
        # Otherwise, removed lemmas, etc. will persist as "empty" categories
        cat_cols = df.select_dtypes(include='category').columns
        df[cat_cols] = df[cat_cols].astype('string')
        df = df.loc[df.colloc_id.isin(ids), :]
        df[cat_cols] = df[cat_cols].astype('category')
        print('   + After filtering to target bigrams')
        print_md_table(df.select_dtypes(exclude='object').describe().T.convert_dtypes(),
                       indent=5, title=f'({i+1}) `{p.stem}` summary')
        # ^ not sure what I'm doing with this `flatten_deps` ... but wanted to save it
        flatten_deps(input_path=p, df=df)
        yield df

def flatten_deps(input_path, df):
    for i, dep_col in enumerate(cols_by_str(df, start_str='dep_')): 
        #! #BUG get this method working --> KeyError
        dep_df = (pd.json_normalize(df[dep_col], sep='_')
                    .assign(hit_id=df.index,
                            pattern=df.pattern[0])
                    .set_index(['hit_id', 'pattern'], drop=True)
                    .convert_dtypes())
        node = dep_df.node[0]
        dep_df.pop('node')
        dep_df.columns = node + '_' + dep_df.columns
        if i == 0: 
            dep_info = dep_df
        else: 
            dep_info.join(dep_df)

    print(dep_info)
    dep_path = Path(*input_path.parts[:-3] + ('3_dep_info', input_path.parts[-2], input_path.name.replace('hits.pkl.gz', 'deps')))
    save_table(df=dep_info, path_str=str(dep_path), df_name=dep_path.stem, formats=['pickle', 'csv'])

def _select_columns(df):
    cols = ['colloc_id', 'token_str', 'category']
    cols.extend(df.columns[df.columns.str.endswith(
            ('lemma', 'form', 'window'))].to_list())
    cols.extend(
            df.columns[df.columns.str.startswith(('dep', 'pat'))].to_list())
        
    sdf = df[cols]
    if 'pattern' in cols: 
        sdf = sdf.assign(pattern=df.pattern.astype('category'))
    pre_adv_ix = df.adv_index - 1
    word_between_id = df.index[df.neg_index != pre_adv_ix]
    # post_adj_ix = df.adj_index + 1
    sdf.loc[word_between_id, 
            'pre_adv_lemma'] = word_between_id.to_series().apply(
                lambda i: df.lemma_str[i].split()[pre_adv_ix[i]])
    return sdf.assign(pre_adv_lemma=sdf.pre_adv_lemma.astype('category'))


# def simplify_table(p, simple_hits_pkl):
    # df = pd.read_pickle(p)
    # df = select_cols(
    #     df,
    #     columns=(['token_str', 'pattern', 'category']
    #              + df.columns[df.columns.str.endswith(('lemma', 'form', 'window'))].to_list()
    #              + df.columns[df.columns.str.startswith('dep')].to_list()
    #              )
    # )
    # path_str = str(simple_hits_pkl).split('.pkl', maxsplit=1)[0]
    # if not Path(path_str).is_absolute():
    #     path_str = str(Path(path_str).resolve())
    # save_table(df,
    #            path_str,
    #            df_name='simplified hits')

    # return df


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


# def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #// # > print overview of initial data
    # print('\n## Cleaning up hits: removing duplicated or exceptionally',
    #       'long sentences, strange orthography, and random capitals.')
    # starting_token_count = len(df)

    #// # * drop lemmas with abnormal orthography
    # ts = pd.Timestamp.now()
    # prior_len = len(df)
    # df = _drop_odd_orth(df)
    # te = pd.Timestamp.now()
    # print(f'> {(prior_len - len(df)):,} hits',
    #       'removed due to abnormal orthography in',
    #       get_proc_time(ts, te))
    # _print_uniq_lemma_count(df)
    # print(_describe_str_lemma_counts(df).to_markdown(floatfmt=',.0f'))

    #// # * removing implausibly long, then duplicate sentences
    # if 'token_str' in df.columns and 'text_window' in df.columns:
    #//     # * too long
    #     _t0 = pd.Timestamp.now()
    #     df = _drop_long_sents(df)
    #     _t1 = pd.Timestamp.now()
    #     _print_uniq_lemma_count(df, label='natural', head_mark='~')
    #     print_md_table(_describe_str_lemma_counts(df))
    #     print('[ Time to drop implausible "sentences":',
    #           get_proc_time(_t0, _t1), ']')

    #//     # * duplicates
    #     _t0 = pd.Timestamp.now()
    #     _print_uniq_lemma_count(df, label='nonduplicated', head_mark='~')
    #     print_md_table(_describe_str_lemma_counts(df))
    #     df = _drop_duplicate_sents(df)
    #     _t1 = pd.Timestamp.now()

    #     print('[ Time to drop duplicated sentences:',
    #           get_proc_time(_t0, _t1), ']')

    # valid_token_count = len(df)
    # print(f'\n> {(starting_token_count - valid_token_count):,}',
    #       'hits from invalid sentences (too long or duplicated) removed.')
    # print(f'Total valid/cleaned bigram hits: {valid_token_count:,}')
    # _print_uniq_lemma_count(df, label='valid', head_mark='~')
    # print_md_table(_describe_str_lemma_counts(df))

    #// # * remove random capitalizations
    # ts = pd.Timestamp.now()
    # print('\nNormalizing lemma case (making everything lower case)...')
    # df = df.assign(adv_lemma=df.adv_lemma.str.lower(),
    #                adj_lemma=df.adj_lemma.str.lower())
    # te = pd.Timestamp.now()
    # _print_uniq_lemma_count(df)
    # print_md_table(_describe_str_lemma_counts(df))
    # print('[ Time to normalize lemma case:',
    #       get_proc_time(ts, te), ']')

    # return df


# def _drop_odd_orth(df: pd.DataFrame,
    #                verbose=False) -> pd.DataFrame:

    # print('\nRemoving lemmas with abnormal orthography...')
    # J = df.adj_lemma
    # J_filter = ~odd_lemma_orth(J)
    # if verbose:
    #     meta_df = (J_filter.value_counts(normalize=True)
    #                .multiply(100).round(3).to_frame('%_of_adj')
    #                .assign(status=['kept', 'dropped'],
    #                        adj_tokens=J_filter.value_counts())
    #                . set_index('status'))
    #     print_md_table(
    #         meta_df, title='ADV orthography filter outcomes', n_dec=2)

    # R = df.adv_lemma
    # R_filter = ~odd_lemma_orth(R)
    # if verbose:
    #     print((R_filter.value_counts(normalize=True)
    #            .multiply(100).round(3).to_frame("%_of_adv")
    #            .assign(status=['kept', 'dropped'],
    #                    adv_tokens=R_filter.value_counts())
    #            .set_index('status').to_markdown()), '\n')

    # return df.loc[J_filter & R_filter, :]


# def odd_lemma_orth(lemmas: pd.Series) -> pd.Series:
    # return pd.Series(
    #     lemmas.str.startswith(('-', '&', '.'))
    #     | lemmas.str.endswith(('-', '&'))
    #     | lemmas.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))


# def _drop_long_sents(df: pd.DataFrame) -> pd.DataFrame:
    # starting_df = df.copy()
    # df = df.assign(tok_in_sent=df.token_str.apply(lambda s: len(s.split())))
    # sent_limit = 250
    # too_long = df.tok_in_sent > sent_limit
    # uniq_too_long = df.loc[too_long, :].index.str.split(":",
    #                                                     1).str.get(0).unique()
    # try:
    #     drop_count = too_long.value_counts()[True]
    # except KeyError:
    #     print('No sentences are too long. Nothing dropped.')
    # else:
    #     print(f'\nDropping {(drop_count):,} hits',
    #           f'from {len(uniq_too_long):,} "sentences" with',
    #           f'{sent_limit}+ tokens. For example:\n```')
    #     print((starting_df.loc[df.index.str.startswith(tuple(uniq_too_long)),
    #                            ['token_str']]).sample(1).squeeze()[:550] +
    #           '...\n```')
    #     df = df.loc[~too_long, :]
    # return df


# def _drop_duplicate_sents(df: pd.DataFrame, verbose: int = 0) -> pd.DataFrame:
    # over_10_tok = df.tok_in_sent > 10
    # is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
    # definite_duplicate = over_10_tok & is_duplicate_hit
    # print(f'\n≎ Removing {(definite_duplicate.value_counts()[True]):,}',
    #       'duplicate hits between input tables',
    #       '(provided sentence is longer than 10 tokens).')
    # singletons = df.loc[~definite_duplicate,
    #                     ['adv_lemma', 'adj_lemma', 'token_str']]
    # if verbose == 2:
    #     init_sent_counts = df.token_str.value_counts(sort=False).sort_index()
    #     filter_sent_counts = singletons.token_str.value_counts(
    #         sort=False).sort_index()
    #     sent_diff = init_sent_counts - filter_sent_counts
    #     sent_with_dup = len(sent_diff[sent_diff != 0].index)
    #     print(f'  ⨳ {sent_with_dup:,} initial sentences had 1+ duplicates')
    # if verbose == 1:
    #     all_dup = df.duplicated(['token_str', 'text_window'], keep=False)
    #     print('Examples of duplication:')
    #     print((df.loc[all_dup & over_10_tok,
    #                   ['tok_in_sent', 'token_str']]).sort_values(['token_str'
    #                                                               ]).head(8))

    # return singletons[['adv_lemma', 'adj_lemma']].astype('string')


# def _drop_infreq(df, percent) -> pd.DataFrame:
    # print(f'## Removing hits where `{df.columns[0]}` and/or ',
    #       f'`{df.columns[1]}` do not meet the total hit threshold...')

    # print_md_table(df.describe().T, title='Initial (clean) Summary')
    # print_md_table(_describe_str_lemma_counts(df),
    #                title='Initial (clean) distribution info')
    # ts = pd.Timestamp.now()
    # clean_total = len(df)
    # # must keep at least 15% of the initial hits
    # must_keep = round(clean_total * _MIN_TOK_KEEP_RATIO)
    # n_dropped = len(df)
    # filter_applied = 0
    # filter_attempt = 0
    # while n_dropped > 0:
    #     filter_attempt += 1
    #//     # #* Best to use a reasonable value (i.e. [0.00001:1]%)

    #     percent, hit_thresh = _confirm_thresh(clean_total, percent)
    #     if filter_attempt == 0:
    #         print('\nLimiting by total lemma frequency',
    #               f'threshold ≥ {hit_thresh:,} tokens per lemma...')

    #     update_df = _get_update(df, hit_thresh)
    #     n_remain = len(update_df)
    #     n_dropped = len(df) - n_remain

    # //    # * Evaluate if `n_dropped` (hits dropped this pass), yields ideal result.
    # //    # *  -> If not, adjust threshold.
    #     adjust_str = ''
    #  //   # > if _no/too few_ hits were dropped (overall) ~ 95+% of initial hits remain...
    #  //   #! use `n_remain` to evaluate because `n_dropped` is only for CURRENT attempt
    # //    # > or if median count for either lemma type is less than 5
    #     if (n_remain >= _KEEP_ALLOWANCE_RATIO * clean_total
    #             or any(_describe_str_lemma_counts(update_df).T['50%'] < _MIN_MEDIAN)):
    #  //       # > raise percentage threshold --> increase by 1/4
    #         adjust_str = '◔ Insufficient Reduction: 🔺raising'
    #         percent *= 1.25
    #         if n_dropped <= 0:
    #  //           #! must also reset `n_dropped` to stay in `while` loop
    #             n_dropped = 1

    # //    # > hits were dropped in this attempt...
    #     elif n_dropped > 0:

    #  //       # > if _too many_ hits were dropped...
    #         if ((n_remain < must_keep)
    #                 # keep at least 20 unique adv
    #                 or (count_uniq(update_df.adv_lemma) < _ADV_KEEP_REQ)
    #                 # keep at least 40 unique adj
    #                     or (count_uniq(update_df.adj_lemma) < _ADJ_KEEP_REQ)
    #                 ):

    #             if not filter_applied and filter_attempt < 5:
    # //                # > lower percentage threshold --> reduce by 1/4
    #                 adjust_str = '◕ Excessive Reduction: 🔻lowering'
    #                 percent *= 0.75

    #             else:
    #                 print('! More lemmas fall below the threshold,',
    #                       'but removing them violates other restrictions.')
    #                 n_dropped = 0

    # //        # * if `n_dropped` is ideal, udpate `df` to `update_df`
    #         else:
    #             filter_applied += 1
    #             print(f'Successful pass #{filter_applied} (attempt',
    #                   f'#{filter_attempt}):\n',
    #                   f'removing {n_dropped:,} hits containing lemmas',
    #                   f'having fewer than {hit_thresh:,} total tokens...')
    #             df = update_df

    #//     # > sufficient hits have been removed, just not in this round
    #     else:
    #         print('✓ No further infrequent lemmas found.',
    #               'Frequency filtering complete!')

    #     if adjust_str:

    #         print(f'⚠️  ({filter_attempt}) Token threshold of',
    #               f'{hit_thresh:,} tokens/lemma failed.')
    #//         # > update token count threshold from new percentage
    #         hit_thresh = percent_to_count(percent, clean_total)
    #         print(f'  {adjust_str} percentage for threshold by 1/4')
    #         print(f'    updated threshold: {hit_thresh:,} tokens,',
    #               f'      ~{percent:.5}% of initial (clean) hits')

    # te = pd.Timestamp.now()
    # print(
    #     f'> {(clean_total - len(df)):,} total hits dropped due to',
    #     f'infrequncy (lemma(s) with fewer than {hit_thresh:,} hits',
    #     f'~{round(percent,5)}% of total valid hits) across',
    #     f'{filter_applied} filtering pass(es).\n',
    #     f'[ time elapsed = {get_proc_time(ts, te)} ]')

    # print_md_table(_describe_str_lemma_counts(df), indent=2)
    # remain_str = f'\n>>> {len(df):,} total remaining hits <<<'
    # percent_str = f'{round(len(df)/clean_total*100, 2)}% of {clean_total} total valid hits.'
    # width = max(len(remain_str), len(percent_str))+2
    # print(remain_str.center(width))
    # print(percent_str.center(width))

    # return df


# def _confirm_thresh(total, percent):
    # hit_thresh = percent_to_count(percent, total)
    # if hit_thresh < _MIN_THRESH_COUNT:
    #     hit_thresh = _MIN_THRESH_COUNT
    #     percent = hit_thresh / total * 100
    #     print('Given percentage is too low for noticable reduction.',
    #           f'Set values to minimum {hit_thresh} hit tokens/lemma')
    #     print(f'  ≈ {round(percent,6)}% of clean hits')
    # return percent, hit_thresh


# def _get_update(df, token_thresh):
    # indexers = []
    # # print(_describe_lemma_counts(df).to_markdown())
    # print('\n+ Compiling frequency table update:')
    # for i, col in enumerate(df.columns):
    #     print(f'  ({i+1}) restricting `{col}` column...')
    #     col_counts = df[col].value_counts()

    #     lemmas_over_thresh = col_counts[col_counts >= token_thresh].index

    #     indexers.append(df[col].isin(lemmas_over_thresh))

    # update_df = df.loc[indexers[0] & indexers[1], :]

    # up_st = _describe_str_lemma_counts(update_df).T
    # up_st = (up_st
    #          .assign(range=up_st['max'] - up_st['min'],
    #                  iqr=up_st['75%'] - up_st['25%']).round())
    # print('+ Potential Table Update')
    # print_md_table(up_st[['mean', '50%', 'min', 'max']], indent=2,
    #                title=f'{(len(df) - len(update_df)):,} potential removals')
    # _print_uniq_lemma_count(update_df)

    # return update_df


def _summarize_hits(df):
    lemma_counts_summ = _describe_str_lemma_counts(df)
    tok_thresh_c = int(lemma_counts_summ.loc['min', :].min())
    print(f'    ⇟ minimum hits/lemma in data: {tok_thresh_c:,}')
    print_md_table(df.describe().T, indent=2,
                   title='Frequency Filtered Hits Summary')
    print_md_table(lemma_counts_summ, indent=2,
                   title='Frequency Filtered Lemma Distributions')

    #// return tok_thresh_c


def get_freq_info(df: pd.DataFrame, # n_files, frq_thresh, 
                  group: str, 
                  frq_out_dir: Path) -> tuple:
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

                # ? #[ ]: add simple output of just `df.var_coeff`?
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
    nth = len(desc) // 6
    trim = int(len(desc) * 0.01)
    desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    top_means_metric = desc.loc[
        (desc['mean'] > (desc_interior['mean'].median() * .75))
        &
        (desc.total > (desc_interior['total'].median() * .75)), metric]
    # info_list = []
    # for label, desc_df in {'interior': desc.iloc[5:, :], 'full': desc}.items():
        # top_means = desc_df.loc[
        #     (desc_df['mean'] > (desc_df['mean'].median() + 0.5 * 1))
        #     &
        #     (desc_df.total > (desc_df.total.median() * 1.1))
        #     , [metric, 'mean', '50%', 'total', 'max', 'range']]
        # info = top_means.describe()
        # info.columns = info.columns.astype('string') + f'_{label}'
        # info_list.append(info)
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
