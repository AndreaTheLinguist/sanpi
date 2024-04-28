import argparse
import re
# from pprint import pprint
import statistics as stat
from collections import namedtuple
from pathlib import Path

from numpy import format_float_positional as np_floatfmt
import pandas as pd

try:
    from source.utils.visualize import heatmap  # pylint: disable=import-error
except ModuleNotFoundError:
    from utils import (PKL_SUFF, Timer,  # pylint: disable=import-error
                       cols_by_str, confirm_dir, count_uniq, find_glob_in_dir,
                       get_proc_time, percent_to_count, print_iter,
                       print_md_table, save_table, select_pickle_paths,
                       sort_by_margins, unpack_dict)
    from utils.visualize import heatmap
else:
    from source.utils import (PKL_SUFF, Timer,  # pylint: disable=import-error
                              cols_by_str, confirm_dir, count_uniq,
                              find_glob_in_dir, get_proc_time,
                              percent_to_count, print_iter, print_md_table,
                              save_table, select_pickle_paths, sort_by_margins,
                              unpack_dict)
pd.set_option("display.float_format", '{:,.3f}'.format)
LOAD_TUPLE = namedtuple(
    'Data_Load_Info',
    ['nfiles', 'frq_thr', 'stage', 'frame_path', 'index_path'])
PATHS_TUPLE = namedtuple(
    'Save_paths', ['frame', 'index'])


# ^ #[ ] there is a lot of overlap in the methods between this module and `count_bigram`--consolidate somehow?
_SANPI_DIR = Path('/share/compling/projects/sanpi')
_MAX_TOK_PER_SENT = 250

# don't remove too much
_MIN_TOK_KEEP_RATIO = 0.15
_ADV_KEEP_REQ = 20
_ADJ_KEEP_REQ = 40
# don't remove too little
_MIN_THRESH_COUNT = 3
_KEEP_ALLOWANCE_RATIO = 0.99
_MIN_MEDIAN = 3

_CROSS_LABEL = 'adj-x-adv'
_DF_FILE_PREF = 'bigrams'
_IX_FILE_PREF = 'bigram-index'

regex_path_from_hit_id = re.compile(
    r'^(nyt)_eng_(\d)|^(apw)|^(pcc)_eng_(\w{2})'
)
# regex_capitalize = re.compile(r'([tv])[ea]$')


def _main():
    with Timer() as top_timer:

        print(pd.Timestamp.now().ctime())
        (n_files, percent_thresh, data_dir,
         post_proc_dir, frq_out_dir, frq_groups,
         stats_requested) = _parse_args()
        frq_out_stem = get_freq_out_stem(
            cross_label=_CROSS_LABEL, group_code='',
            freq_meta_tag=(f'{frq_thr_tag(percent_thresh, n_files)}'))
        if frq_out_path := find_glob_in_dir(
                frq_out_dir, f'*{frq_out_stem}*{PKL_SUFF}'):
            print('Crosstabulated frequencies for bigram word types already exist:',
                  f'\n⇰  {frq_out_path}')
            if stats_requested:
                describe_counts(frq_out_path)
            print('~ Exiting ~')
            return

        with Timer() as timer:
            df = prepare_hit_table(n_files=n_files,
                                   tok_thresh_p=percent_thresh,
                                   post_proc_dir=post_proc_dir,
                                   data_dir=data_dir)
            print('✓ time:', timer.elapsed())

        # ! #HACK -- remove for full data processing
        _summarize_hits(df)
        frq_groups = frq_groups or ['all']

        for group in frq_groups:

            _t0 = pd.Timestamp.now()
            frq_df, frq_df_path = get_freq_info(df, n_files, percent_thresh,
                                                group, frq_out_dir)
            _t1 = pd.Timestamp.now()
            print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')

            if stats_requested:
                describe_counts(frq_df_path, frq_df)
            else:
                print('~ Note: full descriptive statistics not calculated. To retrieve, simply rerun with same arguments + `-s` or `--get_stats` ~')

                print_md_table(frq_df.loc['SUM', frq_df.columns != 'SUM'].to_frame('adjective totals').describe()
                               .join(frq_df.loc[frq_df.index != 'SUM', 'SUM'].squeeze().to_frame('adverb totals').describe()),
                               title='### Summary Statistics for Marginal Frequencies ###')

                print_md_table(
                    frq_df.iloc[0:21, 0:16],
                    title='\n### Top 20 Adjectives by Top 15 Adverbs ###', )

        elapsed_time = top_timer.elapsed()
        finish_str = ('✓ Finished @ '
                      + pd.Timestamp.now().strftime("%Y-%m-%d %I:%M%p"))

    w = len(finish_str)+1
    time_str = '== Total Run Time =='
    print('',
          '.'*w,
          finish_str,
          time_str,
          elapsed_time.center(len(time_str)),
          sep='\n')


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
        default=0.001,
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
    arg_dict = dict(list(args._get_kwargs()))
    arg_dict['percent_hits_threshold'] = np_floatfmt(
        float(arg_dict['percent_hits_threshold']))
    print_md_table(pd.Series(arg_dict).to_frame('arguments given'), indent=2)

    return (args.n_files,
            float(args.percent_hits_threshold),
            args.data_dir,
            args.post_proc_dir.resolve(),
            args.frq_out_dir.resolve(),
            set(args.frq_groups),
            args.get_stats)


def validate_hit_df(df):
    # MARK: utils
    # TODO move to `utils.dataframe`
    if not any(df):
        raise Warning(
            '`df` passed to `validate_hit_df()` is empty! 🪹 Is this right?')
    elif df.index.name != 'hit_id':
        try:
            df = df.set_index('hit_id')
        except KeyError:
            raise KeyError(
                '⚠️ Data Error: "hit_id" not found in columns or as index! 🚫')

    return df


def prepare_hit_table(n_files: int,
                      tok_thresh_p: float,
                      post_proc_dir: Path,
                      data_dir: Path):
    partial_run = n_files < len(list(data_dir.glob('*hits.pkl.gz')))
    print(f"# Collecting {'sample ' if partial_run else ''}"
          "vocabulary frequencies for",
          f"{f'{n_files} smallest' if partial_run else f'all {n_files}'} hit tables in `../{Path(*data_dir.parts[-2:])}/` matching `*hits.pkl.gz`")

    print('\n## Loading data...')
    df, check_point, n_files_clean = seek_priors(
        n_files, tok_thresh_p, data_dir, post_proc_dir)
    if not any(df):
        raise ValueError('Uh oh! No data! 😨')
    # * if frequency filtering found, return it
    if check_point.stage.startswith('freq'):
        return df

    # * apply cleaning filter, if needed
    if n_files_clean < n_files:
        print(f'\n> {len(df):,} starting hits')
        show_interim_summary(df, raw=True)
        df = _get_clean_data(df)

    # > summarize clean hits
    print_md_table(df.loc[:, df.columns != 'token_str'],
                   title='Clean Hits Summary (`token_str` excluded)',
                   indent=2, describe=True, transpose=True)
    print_md_table(_describe_str_adx_counts(df), indent=2,
                   title='## Clean Word Stats Summary')

    # * apply frequency filter, if requested/needed
    if tok_thresh_p != 0:
        df, adx_lower_df = confirm_form_lower_columns(df)

        # > drop infrequent adv & adj lemmas
        adx_lower_df = _drop_infreq(adx_lower_df, tok_thresh_p)

        # > save index (.txt) for frequency filter
        freq_filt_paths = generate_paths(n_files,
                                tok_thresh_p,
                                post_proc_dir, stage='frequency filter')
        # freq_index_path = get_path_to_index(post_proc_dir, frq_thr_tag(tok_thresh_p, n_files))
        save_filter_index(freq_filt_paths.index_path, adx_lower_df)

        # > save full filtered dataframe (pkl.gz)
        df = df.loc[adx_lower_df.index, :]

        # tok_thresh_c = infer_count_thresh(df)
        save_table(
            df,
            save_path=(str(freq_filt_paths.frame_path)
                       .replace(PKL_SUFF, '').strip('.')),
            df_name=('frequency restrictred bigrams '
                     f'({infer_count_floor(df)}+ frequency threshold)'))
        # print(
        # f'frequency restrictred bigrams ({infer_count_thresh(df)}+ frequency threshold)')

    return df


def seek_priors(n_files, tok_thresh_p, data_dir, post_proc_dir):

    checkpt_dict = {
        t.stage: t
        for t in generate_paths(n_files,
                                tok_thresh_p,
                                post_proc_dir)}

    df = []
    n_files_clean = 0

    # * seek prior frequency filtering
    if tok_thresh_p != 0:
        df = _load_from_priors(
            data_dir,
            checkpt_dict['frequency filter'])
        if any(df):
            return validate_hit_df(df), checkpt_dict['frequency filter'], n_files
    clean_chkpt = checkpt_dict['clean']
    # > look for prior cleaning records
    # >     1. look for exact match
    df = _load_from_priors(data_dir=data_dir, check_pt=clean_chkpt)
    if any(df):
        n_files_clean = n_files
    else: 
        # > 2. look for clean index for neighboring `n_files` value
        found_clean_index, n_files_clean = seek_alternate_cleaning(checkpt=clean_chkpt)
        # with Timer() as timer: 
            # df = load_from_txt_index(data_dir=data_dir, filter_index=found_clean_index)
        #     print('time to load using `load_from_txt_index`', timer.elapsed())
        with Timer() as timer:
            df = _load_data(n_files, data_dir=data_dir, 
                            filter_index=found_clean_index, 
                            filter_file_count=n_files_clean)
            print('time to load using `_load_data`', timer.elapsed())
    
    if any(df) and n_files_clean >= n_files:
        df = validate_hit_df(df)
        # > no frequency filtering, but cleaning is complete
        print('== Loaded data already filtered to account for '
              'cleaning of given data. Cleaning steps will be skipped. ==')

        save_filter_index(clean_chkpt.index_path, df)
        # if frequency filtering is disabled, save clean hits as pkl
        if tok_thresh_p == 0:
            save_table(df,
                       save_path=str(clean_chkpt.frame_path).replace(
                           PKL_SUFF, ''),
                       df_name="cleaned bigrams (no frequency filtering)")

    return df, clean_chkpt, n_files_clean


def seek_alternate_cleaning(clean_index_path: Path = None,
                            n_files: int = None,
                            checkpt: LOAD_TUPLE = None) -> tuple[Path, int]:
    if checkpt and checkpt.stage == 'clean':
        clean_index_path = clean_index_path or checkpt.index_path
        n_files = n_files or checkpt.nfiles

    if not clean_index_path:
        raise ValueError(
            '`seek_prior_cleaning` can only be run at the "clean" checkpoint stage. Pass checkpoint with `stage=="clean"` or manually pass index path for clean hits')
    if n_files is None:
        raise TypeError(
            '`n_files` cannot be None type. Pass clean stage checkpoint or valid integer value for `n_files`.')

    df = []
    n_files_clean = 0
    alt_index = None

    def _seek_alternate_index(clean_index_path: Path, n_seek: int) -> tuple[int, Path]:
        # nfiles_in_filter = 0
        alt_index_path = clean_index_path.parent.joinpath(
            f'{_IX_FILE_PREF}_clean.{n_seek}f.txt')
        if alt_index_path.is_file():
            # nfiles_in_filter = n_seek
            print(f'\nLocated relevant index filter at\n  {alt_index_path}')
            return n_seek, alt_index_path
        else:
            return 0, None

    # > since cleaning fewer files can never result in _more_ removals,
    # >     it's ok to use a cleaning filter from a smaller set of files
    #       (this cannot be applied for frequency filtering)
    n_seek = n_files
    # first, look higher
    while n_seek < 35 and not alt_index:
        n_seek += 1
        n_files_clean, alt_index = _seek_alternate_index(
            clean_index_path, n_seek)

    if not alt_index:
        # if nothing found higher, look lower
        # first, reset the counter
        n_seek = n_files
        while n_seek > 1 and not alt_index:
            n_seek -= 1
            n_files_clean, alt_index = _seek_alternate_index(
                clean_index_path, n_seek)

    return alt_index, n_files_clean


def _load_from_priors(data_dir, check_pt) -> pd.DataFrame or list:
    stage = check_pt.stage
    print(f'Checking for prior {stage}ing outputs...')

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
        with Timer() as timer:
            df = load_from_txt_index(data_dir=data_dir,
                                     check_point=check_pt)
            print(f'  time to load using prior {stage}ed',
                  'index →', timer.elapsed())
        if check_pt.stage != 'clean' or df.size < 850000:
            save_table(
                df=df,
                save_path=str(check_pt.frame_path).strip(PKL_SUFF),
                df_name=f'{stage}ed dataframe')
    if any(df):
        print(f'> Loaded data already accounts for {stage}ing.')
    return df


def generate_paths(n_files: int,
                   tok_thresh_p: float,
                   post_proc_dir: Path,
                   stage: str = None) -> list[LOAD_TUPLE] or LOAD_TUPLE:

    confirm_dir(post_proc_dir)

    def set_load_tuple(n_files: int, percent_thresh: float,
                       post_proc_dir: Path, file_base: str,
                       stage: str) -> LOAD_TUPLE:
        # tuple example:
        # (35, 0.01, 'frequency filter',
        #  [PATH TO DF PICKLE], [PATH TO INDEX TEXT]  )
        return LOAD_TUPLE(
            nfiles=n_files,
            frq_thr=percent_thresh if stage != 'clean' else None,
            stage=stage,
            frame_path=get_path_to_frame(post_proc_dir, file_base),
            index_path=get_path_to_index(post_proc_dir, file_base))

    stage_tags = {
        'clean': get_clean_tag(n_files),
        'frequency filter': frq_thr_tag(tok_thresh_p, n_files)
    }
    if stage:
        file_base = stage_tags[stage]
        return set_load_tuple(n_files, tok_thresh_p,
                              post_proc_dir, file_base,
                              stage)

    return [
        set_load_tuple(n_files=n_files,
                       percent_thresh=tok_thresh_p,
                       post_proc_dir=post_proc_dir,
                       file_base=b, stage=s)
        for s, b in stage_tags.items()
    ]


def get_path_to_frame(post_proc_dir, file_base):
    return post_proc_dir.joinpath(
        f'{_DF_FILE_PREF}_{file_base}{PKL_SUFF}')


def get_path_to_index(post_proc_dir, file_base):
    return post_proc_dir.joinpath(
        f'{_IX_FILE_PREF}_{file_base}.txt')


def get_clean_tag(n_files):
    # > cleaning is before frequency filtering, so no `thresh_tag` in path
    return f'clean.{nfiles_tag(n_files)}'


def nfiles_tag(n_files):
    return f'{n_files}f'


def frq_thr_tag(tok_thresh_p: float,
                n_files: int) -> str:
    thr_str = re.sub(r'\.', '-', np_floatfmt(tok_thresh_p))
    return f'frq-thr{thr_str}p.{n_files}f'


def _load_prior_table(check_point: tuple  # Data_Load_Info
                      ):
    # > if `chk_pt.stage == 'clean'`, `chk_pt.frq_thr is None`
    print(f'* Found existing {check_point.stage}ed dataframe for '
          + f'{check_point.nfiles} files{set_thresh_message(check_point)}.',
          '  + Loading data from',
          f'    > {check_point.frame_path}', sep='\n')

    t0_load = pd.Timestamp.now()
    df = pd.read_pickle(check_point.frame_path)

    if df.index.name != 'hit_id':
        df = df.set_index('hit_id')
    print(
        f'    time to load using {check_point.stage}ed pickled dataframe → {get_proc_time(t0_load, pd.Timestamp.now())}')

    t0_save = pd.Timestamp.now()
    save_filter_index(check_point.index_path, df)

    df = _add_form_lower(df)
    print(
        f'    time to save {check_point.stage}ed index → {get_proc_time(t0_save, pd.Timestamp.now())}')

    return df


def set_thresh_message(check_point):
    return (f' and {np_floatfmt(check_point.frq_thr)}% threshold'
            if check_point.frq_thr
            else '')


def load_from_txt_index(data_dir: Path,
                        check_point: tuple = None,
                        filter_index: Path or list = None):
    #! reason for weird argument duplication → imported to `count_neg.py`
    #! even though both default to None, at least *one* is required.
    if check_point:
        print(f'* Found existing {check_point.stage}ed `hit_id` index for',
              f'{check_point.nfiles} files{set_thresh_message(check_point)}.')
        filter_index = filter_index or check_point.index_path

    # #[x] iter over each pickle and return df with matching indicated index
    table_selections = (
        _load_selection(p, i) for (p, i)
        in locate_relevant_hit_tables(data_dir, filter_index))
    return pd.concat(table_selections)


def locate_relevant_hit_tables(data_dir, filter_index: Path or list):
    # NOTE: 'condensed' dir is really only relevant for env sensitive hits (e.g. negated)
    condensed_dir = data_dir / 'condensed'
    simple_dir = data_dir / 'simple'

    # * Path variation info
    # hit_ids_gen = iter_hit_id_index(check_point.index_path)
    # for hit_id in hit_ids_gen:
    # > examples of hit_id values and corresponding source path
    # nyt_eng_19970307_0512_1:15-16
    #   -> f'{simple_dir}/S_bigram-Nyt1_rb-bigram_hits.pkl.gz'
    # nyt_eng_20051129_0028_3:46-47
    #   -> f'{data_dir}/bigram-Nyt2_rb-bigram_hits.pkl.gz'
    #   > if "simple" table not processed yet, will be in `data_dir`
    #   > *BUT* this should not be the case if `hit_id` is in the index file
    # apw_eng_20050211_0660_8:8-9
    #   -> f'{simple_dir}/S_bigram-Apw_rb-bigram_hits.pkl.gz'
    # pcc_eng_val_3.00133_x34743_29:4-5
    #   -> f'{simple_dir}/S_bigram-PccVa_rb-bigram_hits.pkl.gz'
    # pcc_eng_06_108.0002_x1730749_18:5-6
    #   -> f'{simple_dir}/S_bigram-Pcc06_rb-bigram_hits.pkl.gz
    if isinstance(filter_index, Path):
        with Timer() as timer:
            filter_index = filter_index.read_text().splitlines()
            print(f'time to load bigram filter index: {timer.elapsed()}')
    bigram_ids = pd.Series(filter_index, dtype='string')

    for corpus_cue, _ids in gen_corpus_cues(bigram_ids):
        glob_str = f'*{corpus_cue}*hit*{PKL_SUFF}'

        hit_paths = (
            list(condensed_dir.glob(glob_str))
            or list(simple_dir.glob(glob_str))
            or list(data_dir.glob(glob_str)))
        for hit_path in hit_paths:
            yield hit_path, _ids


def gen_corpus_cues(bigram_ids):
    df = bigram_ids.to_frame('bigram_id')
    with Timer() as timer:
        df['corpus_cue'] = df.bigram_id.apply(
            lambda x: ''.join((g or '').capitalize() for g
                              in regex_path_from_hit_id.search(x).groups())
        ).astype('string').astype('category')
        print('time to isolate corpus cue values from filtered bigram IDs:',
              timer.elapsed())

    yield from (
        (corpus_part, set(id_df.bigram_id.to_list()))
        for corpus_part, id_df in df.groupby('corpus_cue', observed=False))


def _load_selection(t_path, load_index):
    return select_count_columns(
        pd.read_pickle(t_path).loc[list(load_index), :].sort_index())


def infer_count_floor(filtered_df: pd.DataFrame) -> int:
    # MARK:utils
    # TODO move to `utils.dataframe`
    return min(
        filtered_df[c].value_counts().min()
        for c in ('adv_form_lower', 'adj_form_lower')
    )


def confirm_form_lower_columns(df):
    target_cols = ['adj_form_lower', 'adv_form_lower']
    try:
        words_df = df[target_cols]
    except KeyError:
        df = _add_form_lower(df)

        try:
            words_df = df[target_cols]
        except KeyError:
            exit('Counting columns (`{ad*_form_lower`) not found in dataframe.'
                 + ' Inspect processing and inputs and try again. \nEXITING')
    return df, words_df


def save_filter_index(index_path: Path, df: pd.DataFrame):
    if 'adj_form_lower' in df.columns and 'adv_form_lower' in df.columns:
        hit_id_index = (df.index if df.index.name == 'hit_id'
                        else df.hit_id).to_list()
        if index_path.is_file() and not set(index_path.read_text().splitlines()).difference(hit_id_index):
            print('* Filter index previously saved and does not differ from current index:',
                  f'    {index_path}', sep='\n')
            return

        label_verb = ("cleaning" if "clean" in index_path.stem
                      else "frequency filtering")

        print(f'* Saving list of all {len(hit_id_index):,} bigram hit_id',
              f'values retained after {label_verb} as\n  + {index_path}')
        index_path.write_text('\n'.join(hit_id_index), encoding='utf8')

    return


def _describe_str_adx_counts(df: pd.DataFrame) -> pd.DataFrame:
    # MARK:utils
    # TODO move to `utils.dataframe`
    cols = df.filter(
                regex=r'^[ab].*(form|lemma|lower)$'
            ).columns
    word_stats = pd.DataFrame(
        df[c].value_counts().to_frame().rename(columns={'count':c}).describe().squeeze()
        for c in cols
        # > since `describe()` is run on `value_counts()` output, `count` == num unique values
    ).rename(columns={'count': 'unique'})
    # word_stats.index = 
    # > if num_cols - num_rows > 2
    transpose = word_stats.shape[1] - word_stats.shape[0] > 2

    return word_stats.transpose() if transpose else word_stats


def _load_data(n_files: int,
               data_dir: Path,
               filter_index: Path or list = None,
               filter_file_count: int = 0) -> pd.DataFrame:

    pkl_paths = select_pickle_paths(n_files, pickle_dir=data_dir)
    _ts = pd.Timestamp.now()
    df_list = []

    for i, p in enumerate(pkl_paths):
        i_plus1 = i + 1
        try:
            print_path = p.relative_to(Path("/share/compling/data"))
        except ValueError:
            print_path = p.resolve().relative_to(Path("/share/compling"))

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
                df = _add_form_lower(df)
        else:
            df = simplify_table(p, simple_hits_pkl)
        # * use index filter to select `hit_id` values to include
        if filter_index and i_plus1 <= filter_file_count:
            print('   * Prior processing found:\n',
                  f'    + Limiting {Path(p.stem).stem}',
                  'data to `hit_id`s in pre-existing filter')
            if isinstance(filter_index, Path):
                with Timer() as timer:
                    filter_index = filter_index.read_text().splitlines()
                    print(f'time to load bigram filter index: {timer.elapsed()}')
            df = df.loc[df.index.isin(filter_index), :]

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


def select_count_columns(df):
    # * create `NODE_form_lower` if it does not exist yet
    df = _add_form_lower(df)

    if 'pattern' in df.columns:
        df.loc[:, 'pattern'] = df.pattern.astype('category')

    #! made this more inclusive because it's now accessed from `count_neg` via imports
    cols = (
        # Needed for cleaning:
        #  'token_str', 'text_window', '*_lemma'
        #  'adv_form_lower', 'adj_form_lower', 'token_str'
        ['bigram_id', 'token_str', 'pattern', 'category']
        # targets: adv/adj/neg/nr/relay_lemma/form(_lower), text_window, neg/mod_head/deprel
        # + cols_by_str(df, end_str=('lemma', 'form',
        #               'lower', 'window', 'deprel', 'head'))
        + df.filter(regex=r'_(lemma|form|lower|window|deprel|index)$').columns.to_list()
        # targets: any `dep_str_*` columns if input from `3_dep_info/`
        # + cols_by_str(df, start_str='dep_str')
        + df.filter(regex=r'^dep_str').columns.to_list()
    )

    return df.filter(items=(c for c in cols 
                            if not c.startswith('mod_')))


def _add_form_lower(df: pd.DataFrame,
                    pull_prev: bool = True):
    if ('adv_form_lower' not in df.columns
            or 'adj_form_lower' not in df.columns):
        forms = cols_by_str(df, end_str='form')
        df[[f'{f}_lower' for f in forms]] = df[forms].apply(
            lambda f: f.str.lower())
    if 'bigram_lower' not in df.columns:
        df['bigram_lower'] = (df.adv_form_lower + '_' + df.adj_form_lower)
    if pull_prev and ('prev_form_lower' not in df.columns):
        try:
            ingredients = df[['adv_index', 'token_str']]
        except KeyError:
            print('Warning: `adv_index` and `token_str` are',
                  'required to generate `prev_form_lower`:',
                  'column not added.')
        else:
            df['prev_form_lower'] = ingredients.apply(
                _add_prev, axis=1)
    lower_cols = cols_by_str(df, end_str='lower')
    df.loc[:, lower_cols] = df[lower_cols].astype('string')
    return df


def _add_prev(row):
    prev_ix = row['adv_index'] - 1
    return row['token_str'].split()[prev_ix].lower() if prev_ix >= 0 else ''


def _print_uniq_cols_count(df: pd.DataFrame,
                           cols=None,
                           raw: bool = True,
                           label: str = '',
                           head_mark: str = ''):
    # MARK:utils
    # TODO move to `utils.dataframe`
    if not label:
        label = 'initial' if raw else 'updated'
    if not head_mark:
        head_mark = '=' if raw else '+'
    if not cols:
        # ! modified to default to `.contains('_form')`
        # [ ] if certain `adv_form_lower` and `adj_form_lower` have both been added to any frame this is called on, change to `.endswith('form_lower')`
        cols = df.columns[df.columns.str.contains('_form')]
    counts_info = {
        c.upper(): count_uniq(df[c])
        for c in cols
    }
    str_len = len(max(counts_info.keys()))
    num_len = len(str(max(counts_info.values()))) + 1
    counts = ['{0:<{1}s}:  {2:>{3},d}'.format(k, str_len, v, num_len)  # pylint: disable=consider-using-f-string
              for k, v in counts_info.items()]
    print_iter(counts,
               header=f'{head_mark} unique columns in {label} hits',
               indent=2)


def _get_clean_data(df: pd.DataFrame,  # clean_index_path
                    ) -> pd.DataFrame:
    # MARK:clean TOP
    # **** CLEANING #TODO move to `clean_hits.py` & import here
    dirty = pd.Timestamp.now()

    # > print overview of initial data
    print('\n## Cleaning up hits: removing duplicated or exceptionally',
          'long sentences, strange orthography, and random capitals.')
    starting_token_count = len(df)
    # if clean_index_path.is_file():
    #     clean_index = clean_index_path.read_text().splitlines()
    #     df = df.loc[df.index.isin(clean_index), :]
    df = _clean_data(df)

    valid_token_count = len(df)
    print(f'\n> {(starting_token_count - valid_token_count):,}',
          'hits from invalid sentences (too long or duplicated) removed.')

    show_interim_summary(
        df, title=f'Total valid/cleaned bigram hits: {valid_token_count:,}',
        cols_label='valid', iter_head_bullet='~')

    clean = pd.Timestamp.now()
    print('\n[ Time to clean combined hits dataframe:',
          f'{get_proc_time(dirty, clean)} ]')
    # [ ] update to use `with Timer() as timer`
    return df


def _clean_data(df):
    # MARK:clean
    # TODO move to `clean_hits.py`
    ts = pd.Timestamp.now()

    # // # * remove random capitalizations
    # if {'{a}_form_lower' for a in ('adv', 'adj')}.difference(df.columns.to_list()):
    #     print('\nNormalizing case (making everything lower)...')
    #     df = df.assign(adv_form_lower=df.adv_form.str.lower(),
    #                    adj_form_lower=df.adj_form.str.lower())
    #     te = pd.Timestamp.now()
    #     show_interim_summary(df)
    #     print('[ Time to normalize lemma case:',
    #           get_proc_time(ts, te), ']')
    # else:
    #     print('\n✓ Case already normalized (to lower case).')

    # * drop abnormal orthography
    ts = pd.Timestamp.now()
    prior_len = len(df)
    df = _drop_odd_orth(df)
    te = pd.Timestamp.now()
    print(f'> {(prior_len - len(df)):,} hits',
          'removed due to abnormal orthography in',
          get_proc_time(ts, te))
    # [ ] update to use `with Timer() as timer`

    show_interim_summary(df)

    # * removing implausibly long, then duplicate sentences
    if 'token_str' in df.columns and 'text_window' in df.columns:
        # * too long
        _t0 = pd.Timestamp.now()
        df = _drop_long_sents(df)
        _t1 = pd.Timestamp.now()
        # [x] replace with call to interim_summary()
        show_interim_summary(df, cols_label='natural', iter_head_bullet='~')
        # _print_uniq_cols_count(df, label='natural', head_mark='~')
        # print_md_table(_describe_str_adx_counts(df))
        print('[ Time to drop implausible "sentences":',
              get_proc_time(_t0, _t1), ']')

        # * duplicates
        _t0 = pd.Timestamp.now()
        # [x] replace with call to interim_summary()
        show_interim_summary(
            df, cols_label='non-duplicated', iter_head_bullet='~')
        # _print_uniq_cols_count(df, label='nonduplicated', head_mark='~')
        # print_md_table(_describe_str_adx_counts(df))
        df = _drop_duplicate_sents(df)
        _t1 = pd.Timestamp.now()

        print('[ Time to drop duplicated sentences:',
              get_proc_time(_t0, _t1), ']')

    return df


def show_interim_summary(df: pd.DataFrame,
                         title: str = 'interim summary stats',
                         indent: int = 2,
                         cols_label: str = '',
                         iter_head_bullet: str = '',
                         raw: bool = False):
    # MARK:utils
    # TODO move to `utils.dataframe`
    _print_uniq_cols_count(df, label=cols_label, raw=raw,
                           head_mark=iter_head_bullet)
    print_md_table(_describe_str_adx_counts(df),
                   indent=indent, n_dec=1, title=title)


def _drop_odd_orth(df: pd.DataFrame,
                   verbose=False) -> pd.DataFrame:
    # MARK:clean
    # TODO move to `clean_hits.py`

    def odd_lemma_orth(lemmas: pd.Series) -> pd.Series:
        return pd.Series(
            lemmas.str.startswith(('-', '&', '.'))
            | lemmas.str.endswith(('-', '&'))
            | lemmas.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))

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


def _drop_long_sents(df: pd.DataFrame) -> pd.DataFrame:
    # MARK:clean
    # TODO move to `clean_hits.py`
    starting_df = df.copy()
    df = df.assign(tok_in_sent=df.token_str.apply(lambda s: len(s.split())))

    too_long = df.tok_in_sent > _MAX_TOK_PER_SENT
    uniq_too_long = df.loc[too_long, :].index.str.split(":",
                                                        1).str.get(0).unique()
    try:
        drop_count = too_long.value_counts()[True]
    except KeyError:
        print('No sentences are too long. Nothing dropped.')
    else:
        print(f'\nDropping {(drop_count):,} hits',
              f'from {len(uniq_too_long):,} "sentences" with',
              f'{_MAX_TOK_PER_SENT}+ tokens. For example:\n```')
        print((starting_df.loc[df.index.str.startswith(tuple(uniq_too_long)),
                               ['token_str']]).sample(1).squeeze()[:550] +
              '...\n```')
        df = df.loc[~too_long, :]
    return df


def _drop_duplicate_sents(df: pd.DataFrame, verbose: int = 0) -> pd.DataFrame:
    # MARK:clean
    # TODO move to `clean_hits.py`

    over_10_tok = df.tok_in_sent > 10
    is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
    definite_duplicate = over_10_tok & is_duplicate_hit
    if any(definite_duplicate):
        print(f'\n≎ Removing {(definite_duplicate.value_counts()[True]):,}',
              'duplicate hits between input tables',
              '(provided sentence is longer than 10 tokens).')
    singletons = df.loc[~definite_duplicate,
                        # ['adv_lemma', 'adj_lemma', 'token_str']]
                        ['adv_form_lower', 'adj_form_lower', 'token_str']]
    if verbose == 1:
        all_dup = df.duplicated(['token_str', 'text_window'], keep=False)
        print('Examples of duplication:')
        print((df.loc[all_dup & over_10_tok,
                      ['tok_in_sent', 'token_str']]).sort_values(['token_str'
                                                                  ]).head(8))

    elif verbose == 2:
        init_sent_counts = df.token_str.value_counts(sort=False).sort_index()
        filter_sent_counts = singletons.token_str.value_counts(
            sort=False).sort_index()
        sent_diff = init_sent_counts - filter_sent_counts
        sent_with_dup = len(sent_diff[sent_diff != 0].index)
        print(f'  ⨳ {sent_with_dup:,} initial sentences had 1+ duplicates')
    # return singletons[['adv_lemma', 'adj_lemma']].astype('string')
    return singletons[['adv_form_lower', 'adj_form_lower']].astype('string')

def _drop_infreq(words_df, percent) -> pd.DataFrame:
    #MARK:Freq Filter

    print(f'## Removing hits where `{words_df.columns[0]}` and/or ',
          f'`{words_df.columns[1]}` do not meet the total hit threshold...')

    print_md_table(words_df.describe().T, title='Initial (clean) Summary')
    print_md_table(_describe_str_adx_counts(words_df),
                   title='Initial (clean) distribution info')
    ts = pd.Timestamp.now()
    clean_total = len(words_df)
    # must keep at least 15% of the initial hits
    must_keep = round(clean_total * _MIN_TOK_KEEP_RATIO)
    n_dropped = len(words_df)
    filter_applied = 0
    filter_attempt = 0
    while n_dropped > 0:
        filter_attempt += 1
        # #* Best to use a reasonable value (i.e. [0.00001:1]%)

        percent, hit_thresh = _confirm_thresh(clean_total, percent)
        if filter_attempt == 0:
            print('\nLimiting by total lemma frequency',
                  f'threshold ≥ {hit_thresh:,} tokens per lemma...')

        update_df = _get_update(words_df, hit_thresh)
        n_remain = len(update_df)
        n_dropped = len(words_df) - n_remain

        # * Evaluate if `n_dropped` (hits dropped this pass), yields ideal result.
        # *  -> If not, adjust threshold.
        adjust_str = ''
        # > if _no/too few_ hits were dropped (overall) ~ 95+% of initial hits remain...
        #! use `n_remain` to evaluate because `n_dropped` is only for CURRENT attempt
        # > or if median count for either lemma type is less than 5
        count_stats = _describe_str_adx_counts(update_df)
        try:
            adx_medians = count_stats['50%']
        except KeyError:
            adx_medians = count_stats.loc['50%', :]
        if (n_remain >= _KEEP_ALLOWANCE_RATIO * clean_total
                or any(adx_medians < _MIN_MEDIAN)):
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
                    or (update_df.loc[:, update_df.columns.str.startswith('adv_')]
                        .squeeze().nunique() < _ADV_KEEP_REQ)
                # was: or (count_uniq(update_df.adv_lemma) < _ADV_KEEP_REQ)
                    # keep at least 40 unique adj
                        or (update_df.loc[:, update_df.columns.str.startswith('adj_')].squeeze().nunique() < _ADJ_KEEP_REQ)
                        # was: or (count_uniq(update_df.adj_lemma) < _ADJ_KEEP_REQ)
                ):

                if not filter_applied and filter_attempt < 5:
                    # > lower percentage threshold --> reduce by 1/4
                    adjust_str = '◕ Excessive Reduction: 🔻lowering'
                    percent *= 0.75

                else:
                    print('! More word types fall below the threshold,',
                          'but removing them violates other restrictions.')
                    n_dropped = 0

            # * if `n_dropped` is ideal, udpate `df` to `update_df`
            else:
                filter_applied += 1
                print(f'Successful pass #{filter_applied} (attempt',
                      f'#{filter_attempt}):\n',
                      f'removing {n_dropped:,} hits containing word types',
                      f'having fewer than {hit_thresh:,} total tokens...')
                words_df = update_df

        # > sufficient hits have been removed, just not in this round
        else:
            print('✓ No further infrequent word types found.',
                  'Frequency filtering complete!')

        if adjust_str:

            print(f'⚠️  ({filter_attempt}) Token threshold of',
                  f'{hit_thresh:,} tokens/word type failed.')
            # > update token count threshold from new percentage
            hit_thresh = percent_to_count(percent, clean_total)
            print(f'  {adjust_str} percentage for threshold by 1/4')
            print(f'    updated threshold: {hit_thresh:,} tokens,',
                  f'      ~{np_floatfmt(percent)}% of initial (clean) hits')

    te = pd.Timestamp.now()
    print(
        f'> {(clean_total - len(words_df)):,} total hits dropped due to',
        f'infrequency (word type(s) with fewer than {hit_thresh} hits',
        f'~{np_floatfmt(round(percent,5))}% of total valid hits) across',
        f'{filter_applied} filtering pass(es).\n',
        f'[ time elapsed = {get_proc_time(ts, te)} ]')

    print_md_table(_describe_str_adx_counts(words_df), indent=2)
    remain_str = f'\n>>> {len(words_df):,} total remaining hits <<<'
    percent_str = f'{len(words_df)/clean_total*100:.2f}% of {clean_total:,} total valid hits.'
    width = max(len(remain_str), len(percent_str))+2
    print(remain_str.center(width))
    print(percent_str.center(width))

    return words_df


def _confirm_thresh(total, percent):
    hit_thresh = percent_to_count(percent, total)
    if hit_thresh < _MIN_THRESH_COUNT or percent == 0:
        hit_thresh = _MIN_THRESH_COUNT
        percent = hit_thresh / total * 100
        print('Given percentage is too low for noticable reduction.',
              f'Set values to minimum {hit_thresh} hit tokens/word type')
        print(f'  ≈ {np_floatfmt(percent)}% of clean hits')
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

    up_st = _describe_str_adx_counts(update_df)
    if 'max' not in up_st.columns:
        up_st = up_st.T
    up_st = (up_st
             .assign(range=up_st['max'] - up_st['min'],
                     iqr=up_st['75%'] - up_st['25%']).round())
    print('+ Potential Table Update')
    print_md_table(up_st[['mean', '50%', 'min', 'max']], indent=2,
                   title=f'{(len(df) - len(update_df)):,} potential removals')
    _print_uniq_cols_count(update_df)

    return update_df


def _summarize_hits(df):
    wc_summary = _describe_str_adx_counts(df)
    tok_thresh_c = infer_count_floor(df)
    print(f'    ⇟ minimum hits/word type in data: {tok_thresh_c:,}')
    for x in 'jv':
        if f'ad{x}_lemma' in df.columns:
            compare_word_types(df, f'ad{x}')

    print_md_table(df, indent=2, describe=True, transpose=True,
                   title='Frequency Filtered Hits Summary',
                   max_colwidth=80, format='grid')

    print_md_table(wc_summary, indent=2,
                   title='Frequency Filtered Word Type Distributions')


def compare_word_types(df: pd.DataFrame, node: str = 'adj'):
    compare_cols = [f'{node}_{wt}' for wt in ('lemma', 'form_lower', 'form')]
    differ = df[compare_cols[0]] != df[compare_cols[1]]
    _C = df.loc[differ, compare_cols].value_counts(
        compare_cols
    ).to_frame('tokens').reset_index()
    _C = _C.loc[_C.tokens > 2, :]
    print_md_table(
        _C.set_index(_C.filter(regex=r'form$').columns[0]
                     ).nlargest(20, columns='tokens'),
        title=f'\n#### Most common cases where `{node}_lemma` differs from `{node}_form_lower`')


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
                       + f'={infer_count_floor(df)}+')
    )
    # > method returns `None` if stem not found
    frq_df_path = find_glob_in_dir(frq_out_dir, f'*{frq_out_stem}*{PKL_SUFF}')

    # if crosstabulated frequency table is found
    if frq_df_path:
        print(f'\n* frequency table ({group}) found.')
        frq_df = _load_frq_table(frq_df_path)
    # if frequency table is not found;
    #   i.e. `f` call returned None
    else:
        frq_df_path = frq_out_dir.joinpath(f'{frq_out_stem}{PKL_SUFF}')
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


# // def _build_frq_df(df: pd.DataFrame,
    #               frq_df_path: Path,
    #               group_code: str,
    #               ) -> pd.DataFrame:
    # rdf = df

    # if group_code.lower() != 'all':
    #     J, __ = unpack_dict(SAMPLE_ADJ)
    #     R, __ = unpack_dict(SAMPLE_ADV, values_name='adv')
    #     rdf = df.loc[df.adj_lemma.isin(J)
    #                  & df.adv_lemma.isin(R), :].astype('string')
    # _t0 = pd.Timestamp.now()
    # frq_df = pd.crosstab(index=rdf.adj_lemma,
    #                      columns=rdf.adv_lemma,
    #                      margins=True,
    #                      margins_name='SUM')

    # _t1 = pd.Timestamp.now()
    # print(f'[ Time to crosstabulate frequencies: {get_proc_time(_t0, _t1)} ]')

    # frq_df = sort_by_margins(frq_df, margins_name='SUM')
    # title = (f'{group_code} adj ✕ adv frequency table'
    #          .replace('JxR', 'scale diagnostics'))
    # save_table(frq_df,
    #            str(frq_df_path),
    #            title, formats=['csv'])
    # return frq_df

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
    title = (f'{group_code} {freq_table_rows.name} × {freq_table_cols.name} frequency table'
             .replace('JxR', 'scale diagnostics'))
    save_table(frq_df,
               str(save_path.resolve()),
               title, formats=['pickle', 'csv'])
    return frq_df


def _filter_bigrams(cross_vectors: list):
    # [ ]: This needs adjustments if the filter is to apply to dependency paths
    from utils.LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV
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
            desc = _enhance_descrip(desc, values)
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

    _visualize_counts(df.loc[['SUM'] + most_var_row,
                      ['SUM'] + most_var_col], df_path)


def _enhance_descrip(desc: pd.DataFrame,
                     values: pd.Series) -> pd.DataFrame:
    # TODO: `utils.dataframes` now has a method called `enhance_descrip`: compare and refactor/remove if this is redundant
    values.apply(pd.to_numeric, downcast='unsigned')
    desc = desc.transpose()
    desc = desc.assign(total=values.sum(),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'])
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    if 'SUM' not in desc.index:
        # BUG: this sometimes crashes. believe it's due to different shaped tables
        #       changed it for the output, so that some get transposed and some don't,
        #       depending on the number of columns. but I can't remember where that
        #       is exactly. And this isn't that important. So, for now, just skipping it.
        try:

            desc = desc.assign(
                plus1_geo_mean=values.add(1).apply(stat.geometric_mean),
                plus1_har_mean=values.add(1).apply(stat.harmonic_mean))
        except TypeError:
            print('(fyi, geometric and harmonic means not added to stats)')
    for col in desc.columns:
        if col in ('mean', 'std', 'variance', 'coeff_var'):
            desc.loc[:, col] = pd.to_numeric(desc[col].round(2),
                                             downcast='float')
        else:
            desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    return desc


def _select_word_sample(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
    nth = len(desc) // 6
    trim = int(len(desc) * 0.01)
    desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    top_means_metric = desc.loc[
        (desc['mean'] > (desc_interior['mean'].median() * .75))
        &
        (desc.total > (desc_interior['total'].median() * .75)), metric]
    return (
        top_means_metric.squeeze().nlargest(nth).index.to_list()
        if largest
        else top_means_metric.squeeze().nsmallest(nth).index.to_list()
    )


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

    _main()
