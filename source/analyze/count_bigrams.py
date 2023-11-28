# coding=utf-8

import argparse
import re
from collections import namedtuple
from pathlib import Path

# import numpy as np
import pandas as pd
from utils import (PKL_SUFF, add_form_lower, confirm_dir, describe_counts,
                   describe_str_adx_counts, find_glob_in_dir, get_clean_data,
                   get_proc_time, infer_count_floor, load_from_txt_index,
                   percent_to_count, print_md_table, print_uniq_counts,
                   save_filter_index, save_table, select_count_columns,
                   select_pickle_paths, set_thresh_message,
                   show_interim_summary, sort_by_margins, unpack_dict)
from utils.LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV

LOAD_TUPLE = namedtuple(
    'Data_Load_Info',
    ['nfiles', 'frq_thr', 'stage', 'frame_path', 'index_path'])
PATHS_TUPLE = namedtuple(
    'Save_paths', ['frame', 'index'])


# ^ #[ ] there is a lot of overlap in the methods between this module and `count_bigram`--consolidate somehow?
_SANPI_DIR = Path('/share/compling/projects/sanpi')
_MIN_THRESH_COUNT = 2
_MIN_TOK_KEEP_RATIO = 0.15
_KEEP_ALLOWANCE_RATIO = 0.99
_ADV_KEEP_REQ = 20
_ADJ_KEEP_REQ = 40
_MIN_MEDIAN = 5

_CROSS_LABEL = 'adj-x-adv'

_DF_FILE_PREF = 'bigrams'
_IX_FILE_PREF = 'bigram-index'


def _main():
    print(pd.Timestamp.now().ctime())
    (n_files, percent_thresh, data_dir,
     post_proc_dir, frq_out_dir, frq_groups, get_stats) = _parse_args()
    frq_out_stem = get_freq_out_stem(
        cross_label=_CROSS_LABEL, group_code='',
        freq_meta_tag=(f'{frq_thr_tag(percent_thresh, n_files)}'))
    if frq_out_path := find_glob_in_dir(
            frq_out_dir, f'*{frq_out_stem}*{PKL_SUFF}'):
        print('Crosstabulated frequencies for bigram word types already exist:',
              f'\n⇰  {frq_out_path}')
        if get_stats:
            describe_counts(frq_out_path)
        print('~ Exiting ~')
        return

    df = prepare_hit_table(n_files=n_files,
                           tok_thresh_p=percent_thresh,
                           post_proc_dir=post_proc_dir,
                           data_dir=data_dir,
                           verbose=True)  # ! #HACK -- remove for full data processing
    _summarize_hits(df)
    if not frq_groups:
        frq_groups = ['all']

    for group in frq_groups:

        _t0 = pd.Timestamp.now()
        frq_df, frq_df_path = get_freq_info(df, n_files, percent_thresh,
                                            group, frq_out_dir)
        _t1 = pd.Timestamp.now()
        print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')

        if get_stats:
            describe_counts(frq_df_path, frq_df)
        else:
            print('~ Note: full descriptive statistics not calculated. To retrieve, simply rerun with same arguments + `-s` or `--get_stats` ~')

            print_md_table(frq_df.loc['SUM', frq_df.columns != 'SUM'].to_frame('adjective totals').describe()
                           .join(frq_df.loc[frq_df.index != 'SUM', 'SUM'].squeeze().to_frame('adverb totals').describe()),
                           title='### Summary Statistics for Marginal Frequencies ###')

            print_md_table(
                frq_df.iloc[0:21, 0:16], title='### Top 20 Adjectives by Top 15 Adverbs ###')


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-f',
        '--n_files',
        type=int,
        default=2,
        help=('number of dataframe `.pkl.gz` files to load from `../hit_tables/RBXadj/` '
              '(divided by corpus chunk/slice). '
              'Files are sorted by size so smaller files are selected first. '
              '(i.e. `f=5` will load the 5 smallest tables of hits)'))

    parser.add_argument(
        '-t',
        '--percent_hits_threshold',
        type=float,
        default=0.01,
        help=('Minimum frequency threshold of hits per word type (in summation) for it to be included. '
              '**Specified as PERCENTAGE of total (cleaned) hits, not as explicit integer of hits!** '
              'Any adverb or adjective form which does not meet this minimum frequency '
              'threshold (combined with any other form) will be dropped. '
              'NOTE: This filter is applied iteratively, with sums recalculated after '
              'the previous set of forms and their correpsonding bigram tokens are dropped.'))

    parser.add_argument(
        '-d',
        '--data_dir',
        type=Path,
        default=Path('/share/compling/data/sanpi/2_hit_tables/RBXadj'),
        help=('Path to location of original hit tables. '
              '(i.e. tables indexed by `hit_id`). '
              '`n_files` indicates the number of files to load from this directory.'))

    parser.add_argument(
        '-p',
        '--post_proc_dir',
        type=Path,
        default=Path('/share/compling/data/sanpi/4_post-processed/RBXadj'),
        help=('Path to location for saving post processed hits. '
              '(i.e. tables indexed by `hit_id`). '
              'Name of file(s) generated from `n_files` and `tok_threshold`'))

    parser.add_argument(
        '-o',
        '--frq_out_dir',
        type=Path,
        default=_SANPI_DIR.joinpath('results/freq_out/RBXadj'),
        help=('Path to location for bigram frequency results (adj_form_lower ✕ adv_form_lower tables). '
              'Name of file(s) generated from `n_files` and `tok_threshold`'))

    parser.add_argument(
        '-g', '--frequency_group',
        type=str, action='append', dest='frq_groups',
        default=[],
        help=('')
    )

    parser.add_argument(
        '-s', '--get_stats', action='store_true', default=False,
        help=('option to calculate in-depth descriptive statistics by axis values of frequency table')
    )

    args = parser.parse_args()
    print_md_table(
        pd.Series(dict(list(args._get_kwargs()))).to_frame('arguments given'))
    return (args.n_files, args.percent_hits_threshold, args.data_dir,
            args.post_proc_dir.resolve(), args.frq_out_dir.resolve(), set(args.frq_groups), args.get_stats)


def prepare_hit_table(n_files: int,
                      tok_thresh_p: float,
                      post_proc_dir: Path,
                      data_dir: Path,
                      verbose: False):
    partial_run = n_files < len(list(data_dir.glob('*hits.pkl.gz')))
    print(f"# Collecting {'sample ' if partial_run else ''}"
          "vocabulary frequencies for",
          f"{f'{n_files} smallest' if partial_run else f'all {n_files}'} hit tables in `../{Path(*data_dir.parts[-2:])}/` matching `*hits.pkl.gz`")

    _t0 = pd.Timestamp.now()
    print('\n## Loading data...')

    checkpts_iter = generate_paths(n_files, tok_thresh_p, post_proc_dir)

    # * Load any prior processing
    # > iterate through "check points" (data output post-cleaning or post-frequency filtering)
    #! generator yields "frequency filter" check point information first

    for check_pt in checkpts_iter:
        print(f'Checking for prior {check_pt.stage}ing outputs...')
        df = load_from_priors(data_dir, check_pt)

        if check_pt.stage.startswith('f'):
            freq_filt_paths = PATHS_TUPLE(frame=check_pt.frame_path,
                                          index=check_pt.index_path)
            # > no prior frequency filtering found
            if not any(df):
                # > go to cleaning check point
                continue

            # > else, frequency processing already complete
            print(' == No further reductions. ==')
            _t1 = pd.Timestamp.now()
            print('✓ time:', get_proc_time(_t0, _t1))
            # > return to `_main`
            return df

        # > no prior processing for exact parameters
        elif not any(df):

            # > look for prior cleaning records
            index_values, nfiles_in_filter = seek_prior_processing(
                check_pt.index_path, check_pt.nfiles)

            df = _load_data(n_files, data_dir, index_values, nfiles_in_filter)

            if df.index.name != 'hit_id':
                try:
                    df = df.set_index('hit_id')
                except KeyError:
                    exit(
                        'ERROR: 🚫 `hit_id` information not found! Check arguments and try again.')

            if nfiles_in_filter < n_files:
                print(f'\n> {len(df):,} starting hits')
                show_interim_summary(df, raw=True)
                df = get_clean_data(df)

            else:
                print(
                    '== Loaded data already filtered to account for cleaning of given data. Cleaning skipped. ==')

            save_filter_index(check_pt.index_path, df)
            # save_table(df,
            #            path_str=str(cleaned_path).replace(pkl_suff, ''),
            #            df_name="cleaned bigrams")
        # > summarize clean hits
        print_md_table(df.loc[:, df.columns != 'token_str'].describe(
        ).T, indent=2, title='Clean Hits Summary ("token_str" column excluded)')
        print_md_table(describe_str_adx_counts(df), indent=2,
                       title='## Clean Word Stats Summary')

        df, adx_lower_df = confirm_form_lower_columns(df)

        # > drop infrequent adv & adj lemmas
        adx_lower_df = _drop_infreq(adx_lower_df, tok_thresh_p)

        # > save index (.txt) for frequency filter
        save_filter_index(freq_filt_paths.index, adx_lower_df)

        # > save full filtered dataframe (pkl.gz)
        df = df.loc[adx_lower_df.index, :]

        # tok_thresh_c = infer_count_thresh(df)
        save_table(
            df,
            str(freq_filt_paths.frame).replace(PKL_SUFF, '').strip('.'),
            f'frequency restrictred bigrams ({infer_count_floor(df)}+ frequency threshold)')
        # print(
        # f'frequency restrictred bigrams ({infer_count_thresh(df)}+ frequency threshold)')

    _t1 = pd.Timestamp.now()
    print('✓ time:', get_proc_time(_t0, _t1))
    return df


def load_from_priors(data_dir, check_pt):
    stage = check_pt.stage
    df = []
    # > look for saved files
    if check_pt.frame_path.is_file():
        # loads pickled dataframe
        # makes sure columns/index are in order
        # and saves `df.index` to `chkpt.index_path` if it doesn't already exist
        df = _load_prior_table(check_pt)

    # > if index filter exists
    #   -> .txt list of `hit_id` values for current processing checkpoint
    elif check_pt.index_path.is_file():
        t0_load = pd.Timestamp.now()
        df = load_from_txt_index(data_dir=data_dir,
                                 check_point=check_pt)
        print(f'  time to load using prior {stage}ed',
              'index →',
              get_proc_time(t0_load, pd.Timestamp.now()))
        if check_pt.stage != 'clean':
            save_table(df, str(check_pt.frame_path).strip(
                PKL_SUFF), f'{stage}ed dataframe')
    if any(df):
        print(f'> Loaded data already accounts for {stage}ing.')
    return df


def generate_paths(n_files: int,
                   tok_thresh_p: float,
                   post_proc_dir: Path):

    confirm_dir(post_proc_dir)

    stage_tags = {
        'frequency filter': frq_thr_tag(tok_thresh_p, n_files),
        'clean': get_clean_tag(n_files)}

    for stage, file_base in stage_tags.items():
        # tuple example:
        # (35, 0.01, 'frequency filter',
        #  [PATH TO DF PICKLE], [PATH TO INDEX TEXT]  )
        yield LOAD_TUPLE(
            nfiles=n_files,
            frq_thr=tok_thresh_p if stage != 'clean' else None,
            stage=stage,
            frame_path=get_path_to_frame(post_proc_dir, file_base),
            index_path=get_path_to_index(post_proc_dir, file_base))


def get_path_to_frame(post_proc_dir, file_base):
    return post_proc_dir.joinpath(
        f'{_DF_FILE_PREF}_{file_base}.{PKL_SUFF}')


def get_path_to_index(post_proc_dir, file_base):
    return post_proc_dir.joinpath(
        f'{_IX_FILE_PREF}_{file_base}.txt')


def get_clean_tag(n_files):
    # > cleaning is before frequency filtering, so no `thresh_tag` in path
    return f'clean.{nfiles_tag(n_files)}'


def nfiles_tag(n_files):
    return f'{n_files}f'


def frq_thr_tag(tok_thresh_p: float, n_files: int) -> str:
    thresh_str = re.sub(r'\.', '-', str(tok_thresh_p))
    return f'frq-thr{thresh_str}p.{n_files}f'


def _load_prior_table(check_point: tuple  # Data_Load_Info
                      ):
    # > if `chk_pt.stage == 'clean'`, `chk_pt.frq_thr is None`
    print(f'* Found existing {check_point.stage}ed dataframe for '
          + f'{check_point.nfiles} files{set_thresh_message(check_point)}.',
          '  + Loading data from',
          f'    > {check_point.frame_path}', sep='\n')

    t0_load = pd.Timestamp.now()
    df = pd.read_pickle(check_point.frame_path)

    # col_is_obj = df.dtypes == 'object'
    # if any(col_is_obj):
    #     # ^# [ ] modify dtypes of any 'object' columns
    #     pass
    if df.index.name != 'hit_id':
        df = df.set_index('hit_id')
    print(
        f'    time to load using {check_point.stage}ed pickled dataframe → {get_proc_time(t0_load, pd.Timestamp.now())}')

    t0_save = pd.Timestamp.now()
    save_filter_index(check_point.index_path, df)

    df = add_form_lower(df)
    print(
        f'    time to save {check_point.stage}ed index → {get_proc_time(t0_save, pd.Timestamp.now())}')

    return df


# def set_thresh_message(check_point):
#     > moved to utils.specific


# def load_from_txt_index(data_dir: Path,
#     > moved to utils.specific


# def locate_relevant_hit_tables(data_dir, index_txt_path):
#     > moved to utils.specific


# def _load_selection(t_path, load_index):
#     > moved to utils.specific


def confirm_form_lower_columns(df):
    target_cols = ['adj_form_lower', 'adv_form_lower']
    try:
        words_df = df[target_cols]
    except KeyError:
        df = add_form_lower(df)
        exit('Counting columns (`{adj,adv}_form_lower`) not found in dataframe.'
             + ' Inspect processing and inputs and try again. \nEXITING')

    return df, words_df


def seek_prior_processing(clean_index_path, n_files) -> tuple:

    nfiles_in_filter = 0
    index_values = []
    # > since cleaning fewer files can never result in _more_ removals,
    # >     it's ok to use a cleaning filter from a smaller set of files
    #       (this cannot be applied for frequency filtering)
    n_seek = n_files
    # first, look higher
    while n_seek < 35 and not index_values:
        n_seek += 1
        nfiles_in_filter, index_values = _seek_alternate_index(
            clean_index_path, n_seek)

    # if nothing found higher, look lower
    n_seek = n_files
    while n_seek > 1 and not index_values:
        n_seek -= 1
        nfiles_in_filter, index_values = _seek_alternate_index(
            clean_index_path, n_seek)

    return index_values, nfiles_in_filter


def _seek_alternate_index(clean_index_path: Path, n_seek: int):
    nfiles_in_filter = 0
    index_values = []
    prior_clean = clean_index_path.parent.joinpath(
        f'{_IX_FILE_PREF}_clean.{n_seek}f.txt')
    if prior_clean.is_file():
        nfiles_in_filter = n_seek
        print(f'\nLocated relevant index filter at\n  {prior_clean}')
        index_values = prior_clean.read_text().splitlines()
    return nfiles_in_filter, index_values


# def save_filter_index(index_path: Path, df: pd.DataFrame):
#     > moved to utils.specific


# def describe_str_adx_counts(df: pd.DataFrame,
#     > moved to utils.specific


def _load_data(n_files: int,
               data_dir: Path,
               index_filter: list = None,
               filter_file_count: int = 0) -> pd.DataFrame:

    pkl_paths = select_pickle_paths(n_files, pickle_dir=data_dir)
    _ts = pd.Timestamp.now()
    df_list = []

    for i, p in enumerate(pkl_paths):
        i_plus1 = i + 1
        try:
            print_path = p.relative_to(Path("/share/compling/data"))
        except ValueError:
            print_path = p.resolve().relative_to(Path("/share/compling/projects"))

        print(f'\n{i_plus1}. `../{print_path}`')
        # check for previous simplification
        simple_out_dir = p.parent.joinpath('simple')
        if not simple_out_dir.is_dir():
            simple_out_dir.mkdir(parents=True)
        simple_hits_pkl = simple_out_dir.joinpath('S_' + p.name)

        if simple_hits_pkl.is_file():
            print('   * Found previous output.',
                  '     + Loading data from ',
                  f'       `../{Path(*simple_hits_pkl.parts[-4:])}`',
                  sep='\n')
            try:
                df = pd.read_pickle(simple_hits_pkl)
            except EOFError:
                print(" ⚠️ simplified file unreadable. Loading original...")
                df = simplify_table(p, simple_hits_pkl)
            else:
                df = add_form_lower(df)
        else:
            df = simplify_table(p, simple_hits_pkl)
        #! #BUG this below was being *very* slow
        # print_md_table(df.describe().T.convert_dtypes(),
        #                indent=3, title=f'({i+1}) `{p.stem}` summary')
        # * use index filter to select `hit_id` values to include
        if index_filter and i_plus1 <= filter_file_count:
            print('   * Prior processing found:\n',
                  f'    + Limiting {Path(p.stem).stem}',
                  'data to `hit_id`s in pre-existing filter')
            df = df.loc[df.index.isin(index_filter), :]

        df_list.append(select_count_columns(df))

    combined_df = pd.concat(df_list)
    #! #BUG no summaries, I suppose 🤷‍♀️
    # print_md_table(combined_df.describe().T.convert_dtypes(),
    #                title='Combined Raw Hits Summary')

    _te = pd.Timestamp.now()
    print('> Time to create composite hits dataframe:',
          get_proc_time(_ts, _te))

    return combined_df


def simplify_table(p, simple_hits_pkl):
    df = pd.read_pickle(p)
    # df = select_cols(
    # df,
    # columns=(['token_str', 'pattern', 'category']
    #          + df.columns[df.columns.str.endswith(('lemma', 'form', 'window'))].to_list()
    #          + df.columns[df.columns.str.startswith('dep')].to_list()
    #          ))
    df = select_count_columns(df)
    path_str = str(simple_hits_pkl).split('.pkl', maxsplit=1)[0]
    if not Path(path_str).is_absolute():
        path_str = str(Path(path_str).resolve())
    save_table(df,
               path_str,
               df_name='simplified hits')

    return df


# def select_count_columns(df):
#     > moved to utils.specific


# def add_form_lower(df: pd.DataFrame,
#     > moved to utils.specific


# def _add_prev(row):
#     > moved to utils.specific

# def print_uniq_counts(df: pd.DataFrame,
#     > moved to utils.specific


# def _get_clean_data(df: pd.DataFrame,  # clean_index_path
#                     ) -> pd.DataFrame:
#     > moved to utils.cleaning

# def _clean_data(df):
#     > moved to utils.cleaning

# def show_interim_summary(df: pd.DataFrame,
#     > moved to utils.specific


# def _drop_odd_orth(df: pd.DataFrame,
#     > moved to utils.cleaning

# def odd_lemma_orth(lemmas: pd.Series) -> pd.Series:
#     > moved to utils.cleaning

# def _drop_long_sents(df: pd.DataFrame) -> pd.DataFrame:
#     > moved to utils.cleaning

# def _drop_duplicate_sents(df: pd.DataFrame, verbose: int = 0) -> pd.DataFrame:
#     > moved to utils.cleaning

def _drop_infreq(words_df, percent) -> pd.DataFrame:

    _print_init_frq_info(words_df)
    words_df, clean_total = _apply_frq_filter(
        words_df, percent)
    _print_final_frq_info(words_df, clean_total)
    return words_df


def _apply_frq_filter(words_df, percent):
    ts = pd.Timestamp.now()
    clean_total = len(words_df)
    filter_applied = 0
    filter_attempt = 0
    finalized = False
    while not finalized:
        # #* Best to use a reasonable value (i.e. [0.00001:1]%)
        percent, hit_thresh = _confirm_thresh(clean_total, percent)

        if filter_attempt == 0:
            print('\nLimiting by total lemma frequency',
                  f'threshold ≥ {hit_thresh:,} tokens per lemma...')

        update_df = _get_update(words_df, hit_thresh)
        words_df, percent, filter_applied, finalized = _assess_update(
            words_df, update_df, percent, clean_total, filter_attempt, filter_applied)

        
        
    _print_final_update(words_df, percent, ts,
                          clean_total, filter_applied, hit_thresh)
    return words_df, clean_total

def _assess_update(words_df, update_df, percent, clean_total, filter_attempt, filter_applied):
    filter_attempt += 1
    finalized = False

    # * Evaluate if `n_dropped` (hits dropped this pass), yields ideal result.
    # *  -> If not, adjust threshold.

    # > if _no/too few_ hits were dropped (overall) ~ 95+% of initial hits remain...
    # > or if median count for either lemma type is less than 5
    if (_too_many_remain(clean_total, len(update_df))
            or _too_low_median(update_df)):
            # > raise percentage threshold --> increase by 1/4
        percent = _raise_thresh(percent, clean_total, filter_attempt)

    # > hits were dropped in this attempt...
    elif (len(words_df) - len(update_df)) > 0:
        words_df, percent, filter_applied, finalized = _confirm_reduction(
                update_df, percent, clean_total, filter_applied, filter_attempt, len(words_df))
        
                
    # > sufficient hits have been removed, just not in this round
    else:
        print('✓ No further infrequent word types found.',
                  'Frequency filtering complete!')
        finalized = True
    
    return words_df,percent,filter_applied, finalized


def _too_many_remain(clean_total, n_remain):
    return n_remain >= _KEEP_ALLOWANCE_RATIO * clean_total


def _too_low_median(update_df):
    return any(describe_str_adx_counts(update_df).T['50%'] < _MIN_MEDIAN)


def _confirm_reduction(update_df: pd.DataFrame,
                       percent: float,
                       clean_total: int,
                       filter_applied: int,
                       filter_attempt: int,
                       prev_len: int):
    hit_limitations = False
    # > if _too many_ hits were dropped...
    must_keep = round(clean_total * _MIN_TOK_KEEP_RATIO)
    if ((len(update_df) < must_keep)
        # keep at least 20 unique adv
        or _keep_min_adv(update_df)
        # keep at least 40 unique adj
            or _keep_min_adj(update_df)):

        percent, hit_limitations = _lower_percentage(
            percent, filter_applied, filter_attempt, clean_total)
        
    # * if `n_dropped` is ideal, udpate `df` to `update_df`
    else:
        filter_applied += 1
        n_dropped = prev_len -len(update_df)
        hit_thresh = percent_to_count(percent, clean_total)
        print(f'Successful pass #{filter_applied} (attempt',
                      f'#{filter_attempt}):\n',
                      f'removing {n_dropped:,} hits containing word types',
                      f'having fewer than {hit_thresh:,} total tokens...')
        words_df = update_df
    return words_df, percent, filter_applied, hit_limitations


def _raise_thresh(percent, clean_total, filter_attempt):
    percent *= 1.25
    _declare_adjustment(percent, clean_total, filter_attempt, adjust_str='◔ Insufficient Reduction: 🔺raising')
    return percent


def _keep_min_adv(update_df):
    return (update_df.loc[:, update_df.columns.str.startswith('adv_')]
            .squeeze().nunique() < _ADV_KEEP_REQ)


def _keep_min_adj(update_df):
    return (update_df.loc[:, update_df.columns.str.startswith('adj_')].squeeze().nunique() < _ADJ_KEEP_REQ)


def _lower_percentage(percent, filter_applied, filter_attempt, clean_total):
    hit_limitations = False
    if not filter_applied and filter_attempt < 5:
        # > lower percentage threshold --> reduce by 1/4
        percent *= 0.75
        _declare_adjustment(percent, clean_total, filter_attempt,adjust_str = '◕ Excessive Reduction: 🔻lowering')
        
    else:

        print('! More word types fall below the threshold,',
              'but removing them violates other restrictions.')
        hit_limitations = True
        
    return percent, hit_limitations


def _declare_adjustment(percent, clean_total, filter_attempt, adjust_str):
    if adjust_str:
        hit_thresh = percent_to_count(percent, clean_total)
        print(f'⚠️  ({filter_attempt}) Token threshold of',
              f'{hit_thresh:,} tokens/word type failed.')
        # > update token count threshold from new percentage
        print(f'  {adjust_str} percentage for threshold by 1/4')
        print(f'    updated threshold: {hit_thresh:,} tokens,',
              f'      ~{percent:.5}% of initial (clean) hits')


def _print_init_frq_info(words_df):
    print(f'## Removing hits where `{words_df.columns[0]}` and/or ',
          f'`{words_df.columns[1]}` do not meet the total hit threshold...')

    print_md_table(words_df.describe().T, title='Initial (clean) Summary')
    print_md_table(describe_str_adx_counts(words_df),
                   title='Initial (clean) distribution info')


def _print_final_update(words_df, percent, ts, clean_total, filter_applied, hit_thresh):
    te = pd.Timestamp.now()
    print(
        f'> {(clean_total - len(words_df)):,} total hits dropped due to',
        f'infrequncy (word type(s) with fewer than {hit_thresh:,} hits',
        f'~{round(percent,5)}% of total valid hits) across',
        f'{filter_applied} filtering pass(es).\n',
        f'[ time elapsed = {get_proc_time(ts, te)} ]')

def _print_final_frq_info(words_df, clean_total):
    
    print_md_table(describe_str_adx_counts(words_df), indent=2)
    remain_str = f'\n>>> {len(words_df):,} total remaining hits <<<'
    percent_str = f'{round(len(words_df)/clean_total*100, 2)}% of {clean_total} total valid hits.'
    width = max(len(remain_str), len(percent_str))+2
    print(remain_str.center(width))
    print(percent_str.center(width))


def _confirm_thresh(total, percent):
    hit_thresh = percent_to_count(percent, total)
    if hit_thresh < _MIN_THRESH_COUNT:
        hit_thresh = _MIN_THRESH_COUNT
        percent = hit_thresh / total * 100
        print('Given percentage is too low for noticable reduction.',
              f'Set values to minimum {hit_thresh} hit tokens/word type')
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

    up_st = describe_str_adx_counts(update_df).T
    up_st = (up_st
             .assign(range=up_st['max'] - up_st['min'],
                     iqr=up_st['75%'] - up_st['25%']).round())
    print('+ Potential Table Update')
    print_md_table(up_st[['mean', '50%', 'min', 'max']], indent=2,
                   title=f'{(len(df) - len(update_df)):,} potential removals')
    print_uniq_counts(update_df)

    return update_df


def _summarize_hits(df):
    wc_summary = describe_str_adx_counts(df)
    tok_thresh_c = infer_count_floor(df)
    print(f'    ⇟ minimum hits/word type in data: {tok_thresh_c:,}')
    for x in 'jv':
        if f'ad{x}_lemma' in df.columns:
            compare_word_types(df, f'ad{x}')

    print_md_table(df, indent=2, describe=True, transpose=True,
                   title='Frequency Filtered Hits Summary',
                   max_colwidth=40)
    print_md_table(wc_summary, indent=2,
                   title='Frequency Filtered Word Type Distributions')


def compare_word_types(df: pd.DataFrame, node: str = 'adj'):
    compare_cols = [f'{node}_{wt}' for wt in ('lemma', 'form_lower', 'form')]
    differ = df[compare_cols[0]] != df[compare_cols[1]]
    C = df.loc[differ, compare_cols].value_counts(
        compare_cols
    ).to_frame('tokens').reset_index()
    C = C.loc[C.tokens > 2, :]
    print_md_table(
        C.sample(min(20, len(C))).sort_index(),
        title=f'#### Sample where `{node}_lemma` differs from `{node}_form_lower`')


def get_freq_info(df: pd.DataFrame,
                  n_files: int,
                  percent_thresh: float,
                  group: str,
                  frq_out_dir: Path):

    print(f'\n## Processing Frequency data for {group} word types.')
    if group != 'all':
        frq_out_dir = frq_out_dir.joinpath(group)
    confirm_dir(frq_out_dir)

    frq_out_stem = get_freq_out_stem(
        cross_label=_CROSS_LABEL, group_code=group,
        freq_meta_tag=(f'{frq_thr_tag(percent_thresh, n_files)}'
                       + f'={infer_count_floor(df)}+'))
    # > method returns `None` if stem not found
    frq_df_path = find_glob_in_dir(frq_out_dir, f'*{frq_out_stem}*{PKL_SUFF}')

    # if crosstabulated frequency table is found
    if frq_df_path:
        print(f'\n* frequency table ({group}) found.')
        frq_df = _load_frq_table(frq_df_path)
    # if frequency table is not found;
    #   i.e. `f` call returned None
    else:
        frq_df_path = frq_out_dir.joinpath(f'{frq_out_stem}.{PKL_SUFF}')
        # sanity check
        # if not frq_df_path.name.endswith('f.csv'):
        #     exit(f'frequency path error: {frq_df_path}')
        # [ ] modify this to run multiple "crosses" like `count_neg.gen_freq_info()`
        frq_df = _build_frq_df(cross_vectors=[df.adj_form_lower, df.adv_form_lower], cross_label=_CROSS_LABEL, save_path=frq_df_path,
                               group_code=group)
    return frq_df, frq_df_path


def get_freq_out_stem(cross_label: str,
                      freq_meta_tag: str, group_code):
    return f'{group_code}_{cross_label}_{freq_meta_tag}'

# def get_freq_out_stem(frq_thresh, n_files, group_code):
#     return f'{group_code}-frq_thresh{frq_thresh}.{n_files}f'


def _load_frq_table(frq_df_path,
                    index_name: str = 'adj_form_lower',
                    columns_name: str = 'adv_form_lower'):
    print(f'  Loading from ../{frq_df_path.relative_to(_SANPI_DIR)}...')
    # [ ] modified `count_neg.py` to only load from `pkl.gz`
    # can make the same changes here, but it's not as important,
    # since these tables will always have the same axes
    if frq_df_path.suffix.endswith('csv'):
        frq_df = pd.read_csv(frq_df_path)
        frq_df.columns = frq_df.columns.str.strip()
    elif '.pkl' in frq_df_path.suffixes:
        frq_df = pd.read_pickle(frq_df_path)

    # if 'adj_lemma' in frq_df.columns:
    #     frq_df = frq_df.set_index('adj_lemma')
    # frq_df.columns.name = 'adv_lemma'
    if index_name in frq_df.columns:
        frq_df = frq_df.set_index(index_name)
    frq_df.columns.name = columns_name

    return frq_df


# * replaced old version -- copied from `count_neg.py`
def _build_frq_df(cross_vectors: list,
                  #   freq_table_rows: pd.Series,
                  #   freq_table_cols: pd.Series,
                  cross_label: str,
                  save_path: Path,
                  group_code: str = 'all') -> pd.DataFrame:

    freq_table_rows, freq_table_cols = _filter_bigrams(
        cross_vectors) if group_code.lower() != 'all' else cross_vectors

    # * Crosstabulate vectors to get co-occurrence frequencies
    _t0 = pd.Timestamp.now()
    frq_df = pd.crosstab(index=freq_table_rows, columns=freq_table_cols,
                         margins=True, margins_name='SUM')
    _t1 = pd.Timestamp.now()

    print(
        f'[ Time to crosstabulate {cross_label} frequencies: {get_proc_time(_t0, _t1)} ]')

    frq_df = sort_by_margins(frq_df, margins_name='SUM')
    title = (f'{group_code} {freq_table_rows.name} ✕ {freq_table_cols.name} frequency table'
             .replace('JxR', 'scale diagnostics'))
    save_table(frq_df,
               str(save_path.resolve()),
               title, formats=['pickle', 'csv'])
    return frq_df


def _filter_bigrams(cross_vectors: list):
    # [ ]: This needs adjustments if the filter is to apply to dependency paths

    for i, series in enumerate(cross_vectors):
        # > don't try to apply this filter to other attribute types
        if not series.name.endswith(('lemma', 'form', 'lower')):
            continue

        # > filter adjectives
        if series.name.startswith('adj'):
            adj_filter, __ = unpack_dict(SAMPLE_ADJ)
            cross_vectors[i] = series.loc[series.isin(adj_filter)]
        # > filter adverbs
        elif series.name.startswith('adv'):
            adv_filter, __ = unpack_dict(SAMPLE_ADV, values_name='adv')
            cross_vectors[i] = series.loc[series.isin(adv_filter)]
    return cross_vectors


# def describe_counts(df: pd.DataFrame = None,
#     > moved to utils.specific


# def _enhance_descrip(desc: pd.DataFrame,
#     > moved to utils.specific


# def _select_word_sample(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
#     > moved to utils.specific


# def _visualize_counts(frq_df, frq_df_path):
#     > moved to utils.visualize

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
