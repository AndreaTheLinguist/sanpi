# -*- coding=utf-8 -*-
from collections import namedtuple
import itertools as itt
import re
from math import log1p, log2, log10, sqrt
from os import system
from pathlib import Path
from sys import exit as sysxit

import pandas as pd

from .dataframes import Timer, corners, print_md_table, show_counts
from .general import (DEMO_RESULT_DIR, FREQ_DIR, RESULT_DIR, SANPI_HOME,
                      camel_to_snake, confirm_dir, print_iter,
                      run_shell_command, snake_to_camel)

#! This 👇 will result in crashes if environment without `association_measures` is used
#!  to run methods actually using this import,
#!  but handled this way to avoid crashing when it isn't used
try:
    import association_measures
except ModuleNotFoundError:
    pass
else:
    import association_measures.frequencies as fq
    import association_measures.measures as am

ADDITIONAL_METRICS = ['t_score', 'dice', 'log_ratio', 'liddell',
                      'mutual_information', 'hypergeometric_likelihood', 'binomial_likelihood']
ALPHA = 0.005
READ_TAG = 'rsort-view_am-only'
_UCS_HEADER_WRD_BRK = re.compile(r'\.([a-zA-Z])')
_WORD_GAP = re.compile(r"(\b[a-z'-]+)\t([^_\s\t]+\b)")
TRANSPARENT_O_NAMES = {
    'O12': 'Fyn(O12)',
    'O21': 'Fny(O21)',
    'O22': 'Fnn(O22)',
    'O11': 'Fyy(O11)',
    'R1': 'Fy_(R1)',
    'R2': 'Fn_(R2)',
    'C1': 'F_y(C1)',
    'C2': 'F_n(C2)'}

UCS_DIR, DEMO_UCS_DIR = [
    R / 'ucs' for R in (RESULT_DIR, DEMO_RESULT_DIR)]
AM_ENV_DIR, DEMO_AM_ENV_DIR = [
    R / 'env_prepped_tsv' for R in (UCS_DIR, DEMO_UCS_DIR)]
AM_DF_DIR=RESULT_DIR / 'assoc_df'

# ? Does this even do anything? This is never run as its own thing...
confirm_dir(AM_ENV_DIR)

BINARY_ASSOC_ARGS = namedtuple(
    'BINARY_ASSOC_TUPLE',
    ['min_freq', 'all_counts', 'compare_counts', 'comp_label', 'target_counts', 'targ_label', 'data_suffix', 'skew', 'verbose'])


def adjust_assoc_columns(cols_or_df,
                         style: str = None) -> list:
    """Adjust association columns based on specified style.

    This function adjusts association columns by applying replacements and abbreviations based on the specified style.

    Args:
        cols_or_df: Either a list of column names or a pandas DataFrame.
        style (str): The style to apply for column names ('camel' or 'snake').

    Returns:
        list or DataFrame: Modified list of column names or DataFrame with modified column names.
    """
    def change_columns(columns):
        replacements = {'conservative_log_ratio': 'LRC', 
                                'am_log_likelihood': 'G2', 
                                'log_likelihood': 'G2', 
                                't_score': 't', 
                                'mutual_information': 'MI', 
                                'am_p1_given2': 'dP1', 
                                'am_p2_given1': 'dP2', 
                                }
        abbreviations = {
            r'am_': '',
            r'ratio': 'r',
            r'probability': 'p',
            r'11': 'f',
            r'O': 'obs_',
            r'E': 'exp_',
            r'ative': '',
            r'unexpected': 'unexp'
        }
        for update_dict in [replacements, abbreviations]: 
            columns = [
                re.sub(r'|'.join(update_dict.keys()),
                    #    r'am_|ratio|probability|[OE]11|ative_',
                    lambda m:
                    update_dict[m.group()], col)
                for col in columns]
        if style == 'camel':
            columns = [snake_to_camel(c) for c in columns]
        elif style == 'snake':
            columns = [camel_to_snake(c) for c in columns]
            
    # if dataframe is given, dataframe is returned. 
    if isinstance(cols_or_df, pd.DataFrame):
        cols_or_df.columns = change_columns(cols_or_df.columns)
        return cols_or_df
    
    # if iterable is given, iterable is returned.
    else: 
        return change_columns(cols_or_df)


def log_relative_risk(sc, invert: bool = False):
    sc = sc.fillna(0)
    if 'O11' not in sc.columns:
        sc = fq.observed_frequencies(sc).fillna(0)
    r = (
        (sc.O11 * sc.R2) / (sc.O21 * sc.R1)
        if invert else
        (sc.O11 * sc.C2) / (sc.O12 * sc.C1)
    )

    return r.apply(log2)


def add_extra_am(df: pd.DataFrame,
                 verbose: bool = False,
                 vocab: int = None,
                 ndigits: int = 9,
                 metrics: list = None):
    """
    ['z_score', 't_score', 'log_likelihood', 'simple_ll', 
    'liddell', 'dice', 'log_ratio', 'conservative_log_ratio', 
    'min_sensitivity', 'mutual_information', 'local_mutual_information']
    """
    #! conservative_log_ratio added separatedly later
    metrics = metrics or ADDITIONAL_METRICS

    vocab = vocab or df.l1.nunique() + df.l2.nunique()
    init_cols = df.columns.to_list()
    try:

        scores = am.score(df.copy(), measures=metrics,
                          alpha=ALPHA, vocab=vocab, digits=ndigits)
    except KeyError:
        df = df.join(
            fq.observed_frequencies(df.copy()).astype('int64').join(
                fq.expected_frequencies(df.copy()).apply(pd.to_numeric, downcast='float'))
        )
        scores = am.score(df, measures=metrics, alpha=ALPHA,
                          vocab=vocab, digits=ndigits)

    df = df.join(scores.loc[:, ~scores.columns.isin(df.columns)])
    df = extend_deltaP(df.copy())
    df = adjust_expectations(df)

    # MARK: LRC
    # * manually set conservative_log_ratio variants:
    # *      one-tailed, two-tailed, and two-tailed without correction
    df['conservative_log_ratio'] = am.conservative_log_ratio(
        df, one_sided=False, alpha=ALPHA,
        vocab=vocab, digits=ndigits)
    # df['conservative_log_ratio_1t'] = am.conservative_log_ratio(
    #     df, one_sided=True, alpha=ALPHA,
    #     vocab=vocab, digits=ndigits)
    # no correction performed
    alphas = ['001', '005', '01', '05']
    for a in alphas:
        _alpha = float(f'0.{a}')
        if ALPHA != _alpha:
            df[f'conservative_log_ratio_{a}'] = am.conservative_log_ratio(
                df, one_sided=False, alpha=_alpha,
                vocab=vocab, digits=ndigits)
    df['conservative_log_ratio_nc'] = am.conservative_log_ratio(
        df, one_sided=False, alpha=ALPHA, correct=None,
        digits=ndigits)
    # default vocab calculation
    df['conservative_log_ratio_dv'] = am.conservative_log_ratio(
        df, one_sided=False, alpha=ALPHA,
        digits=ndigits)

    for col in ['f', 'f1', 'f2']:
        df[f'{col}_sqrt'] = df[col].apply(sqrt)
    df = df.loc[:, ~df.columns.isin(
        df.filter(regex=r'^(log_ratio$|ipm|index)').columns)]
    if verbose:
        print_md_table(
            df.loc[:, ~df.columns.isin(
                init_cols)].filter(regex=r'^[a-z]').iloc[:10, :8],
            title='\nPreview of Extended Measures (rounded)\n', n_dec=2)

    # vary_lrc(obs_df, df.l1.nunique() + df.l2.nunique())
    return df.rename(columns=TRANSPARENT_O_NAMES)


def adjust_expectations(df):
    try:
        unexpect = df.unexpected_count
    except AttributeError:
        unexpect = df.f - df.E11
        df['unexpected_f'] = unexpect

    df['unexpected_ratio'] = unexpect / df.f
    df['expected_sqrt'] = df.E11.apply(sqrt)

    #! `sqrt` will crash if input is negative
    df['unexpected_abs_sqrt'] = unexpect.abs().apply(sqrt)
    return df


def extend_deltaP(df):
    deltaP_df = df.copy().filter(regex=r'given[12]$')
    for e in ('min', 'max', 'max_abs', 'product'):
        df[f'deltaP_{e}'] = symmetric_deltaP(deltaP_df, eval=e)

    return df


def symmetric_deltaP(_df: pd.DataFrame,
                     eval: str = 'max'):
    if _df.shape[1] > 2: 
        _df = _df.filter(regex=r'given[12]$')
    if eval == 'min':
        return _df.min(axis=1)
    elif eval == 'max':
        return _df.max(axis=1)
    elif eval in {'abs_max', 'max_abs'}:
        return _df.abs().max(axis=1)
    elif eval == 'product':
        return _df.product(axis=1)


def get_vocab_size(all_bigrams: Path or pd.DataFrame,
                   polarized: bool = True):
    '''
    calculates the vocab size for all units and subunits of the bigram

    assumes all_bigrams is either:
        + a dataframe containing the columns "l1" and "l2"
        + or the path to a simple tsv file containing all unique adverb and adjective combinations and their joint frequencies

    assumes that solo unit vocabs are being compared with binary group and multiplies by 2, 
        but this can be turned off using `polarized=False`.
        In which case the returned dictionary values will need to be adjusted accordingly.

    NOTE: cannot be run on `data.frame['adv~adj_initial']` etc., 
        because some forms have already been eliminated by frequency filtering
    '''
    if isinstance(all_bigrams, Path):
        all_df = pd.read_csv(all_bigrams, delimiter='\t', header=None)
        all_df.columns = ['f', 'l1', 'l2']
    else:
        all_df = all_bigrams

    unique_l1 = all_df.l1.nunique()
    unique_l2 = all_df.l2.nunique()
    unique_words = unique_l1 + unique_l2
    # > all possible combinations, not just *occuring* combinations
    unique_bigrams = unique_l1 * unique_l2
    vocabs = {'adv': unique_l1,
              'adj': unique_l2,
              'bigram': unique_words}
    if polarized:
        vocabs = {k: v*2 for k, v in vocabs.items()}
    vocabs['adv~adj'] = unique_words
    return vocabs


def confirm_basic_ucs(basic_ucs_path: Path, 
                      args: BINARY_ASSOC_ARGS,
                      unit: str = None):

    if basic_ucs_path.is_file():
        print('+ existing UCS table found ✓')
    elif unit:
        basic_ucs_path = confirm_polarized_ucs(basic_ucs_path, args, unit)
    elif args.all_counts.is_file():
        build_ucs_table(min_count=args.min_freq,
                        ucs_save_path=basic_ucs_path,
                        cat_tsv_str=f'cat {args.all_counts}')
    else:
        raise FileNotFoundError
    return basic_ucs_path

def confirm_polarized_ucs(basic_ucs_path: Path, 
                          args: BINARY_ASSOC_ARGS, 
                          unit_str:str):
    comp_path = args.compare_counts
    neg_path = args.target_counts
    if any(not p.is_file() for p in (comp_path, neg_path)):
        exit(
                f'Initial counts file not found. Check your paths...\n> {comp_path}\n> {neg_path}')
    path_dict = prep_by_polarity(words_to_keep=unit_str, 
                                 data_suffix=args.data_suffix,
                                 in_paths_dict={args.comp_label: comp_path,
                                                    args.targ_label: neg_path})
    basic_ucs_path = build_ucs_from_multiple(
            tsv_paths=path_dict.values(),
            min_count=args.min_freq,
            save_path=basic_ucs_path
        )
    
    return basic_ucs_path


def initialize_ucs(basic_ucs_path: Path, args: BINARY_ASSOC_ARGS, unit: str = ''):

    print(
        '\nLocating and/or building initial frequency-only UCS table...')
    with Timer() as _timer:
        basic_ucs_path = confirm_basic_ucs(
            basic_ucs_path, args, unit)
        print(
            f'+ path to simple UCS table: `{basic_ucs_path}`')
        print(f'+ time elapsed → {_timer.elapsed()}')
    return basic_ucs_path


def associate_ucs(basic_ucs_path):
    with Timer() as _timer:
        print('\nCalculating UCS associations...')
        run_shell_command(
            f'bash {SANPI_HOME}/script/transform_ucs.sh {basic_ucs_path}')
        print(f'+ time elapsed → {_timer.elapsed()}')


def get_associations_csv(unit, args: BINARY_ASSOC_ARGS, is_polar) -> Path:

    def manipulate_ucs(basic_ucs_path: Path, args, unit: str):

        basic_ucs_path = initialize_ucs(basic_ucs_path, args, unit)
        associate_ucs(basic_ucs_path)
        return basic_ucs_path

    # > select readable/*.csv if it exists, else readable/*.txt
    readable = seek_readable_ucs(unit,
                                 min_freq=args.min_freq,
                                 target_counts_dir=args.target_counts.parent,
                                 data_suffix=args.data_suffix,
                                 all_counts=args.all_counts,
                                 is_polar=is_polar)

    # > create ucs tables if readable/*.txt does not exist
    if not readable.is_file():

        init_ucs_stem = readable.stem.replace(
            READ_TAG, '').strip('.')
        basic_ucs_path = readable.parent.with_name(
            f'{init_ucs_stem}.ds.gz')
        basic_ucs_path = manipulate_ucs(basic_ucs_path, args, unit)
        # if given path to readable file still does not exist
        if not readable.is_file():
            readable = basic_ucs_path.with_name('readable').joinpath(
                basic_ucs_path.name.replace('ds.gz', f'{READ_TAG}.txt'))

    # > return readable path as .csv
    return convert_ucs_to_csv(readable) if readable.suffix == '.txt' else readable


def seek_readable_ucs(unit: str,
                      min_freq: int,
                      target_counts_dir: Path,
                      all_counts: Path,
                      data_suffix: str,
                      is_polar: bool = True):
    min_freq_flag = f'_min{min_freq}x'

    if unit:
        while target_counts_dir.name.lower().startswith(('ucs', 'complement')):
            target_counts_dir = target_counts_dir.parent
        subdir = target_counts_dir.name
        pref = 'polar' if is_polar else 'eval_mirror'
        readable_parent = f'{pref}/{subdir}/{unit}'
        init_ucs_stem = (f'{pref}-{unit}_{data_suffix.strip(".tsv")}'
                         .replace('polar', 'polarized'))

    else:
        subdir = 'adv_adj'
        init_ucs_stem = all_counts.stem
        readable_parent = all_counts.parent
        if 'ucs' in readable_parent.name.lower():
            readable_parent = readable_parent.parent
        readable_parent = f'{subdir}/{readable_parent.name}'

    init_ucs_stem += min_freq_flag

    readable_dir = f'{readable_parent}/readable'
    print(f'    > seeking `{readable_dir}/{init_ucs_stem}*`',
          'frequency data and initial associations...')
    readable_dir = UCS_DIR.joinpath(readable_dir)
    confirm_dir(readable_dir)

    readable_stem = f'{init_ucs_stem}.{READ_TAG}'

    readable_csv = readable_dir / f'{readable_stem}.csv'

    return (readable_csv if readable_csv.is_file() and readable_csv.stat().st_size > 2
            else readable_dir / f'{readable_stem}.txt')


def convert_ucs_to_csv(ucs_path: Path, max_rows: int = None) -> Path:
    def get_ucs_csv_path(trimmed_len: int,
                         ucs_path: Path):
        csv_stem = ucs_path.stem
        if trimmed_len:
            csv_stem = re.sub(r'_top.+$', '', csv_stem)
            csv_stem += f'_top{trimmed_len}'
        return ucs_path.with_name(f'{csv_stem}.csv')

    def write_ucs_csv(csv_path, csv_lines):

        csv_path.write_text('\n'.join(csv_lines), encoding='utf8')
        print(f'UCS table text converted & saved as {csv_path}')

    raw_text = _UCS_HEADER_WRD_BRK.sub(
        r'_\1', ucs_path.read_text(encoding='utf8'))
    raw_lines = raw_text.splitlines()
    raw_content_len = len(raw_lines) - 1
    csv_lines = [','.join(x.split())
                 for x in raw_lines
                 if not x.startswith('--')]
    trimmed_len = None
    if max_rows:
        max_plus_header = max_rows + 1
        csv_lines = csv_lines[:max_plus_header]
        if len(csv_lines) < raw_content_len:
            print(f':: Rows capped at {max_rows} ::')
            trimmed_len = max_rows

    csv_path = get_ucs_csv_path(trimmed_len, ucs_path)
    write_ucs_csv(csv_path, csv_lines)
    return csv_path


def build_ucs_table(min_count: int,
                    ucs_save_path: Path,
                    cat_tsv_str: str,
                    verbose: bool = False):
    def _make_verbose(cmd_parts: list, verbose_flag: str = '--verbose'):
        return cmd_parts.insert(1, verbose_flag)
    # > mine
    # threshold_arg = f'--threshold={min_count}'
    # primary_cmd = 'ucs-make-tables --verbose --types'
    # sort_cmd = f'ucs-sort --verbose {ucs_save_path} BY f2- f1- INTO {ucs_save_path}'
    # if not verbose:
    #     primary_cmd, sort_cmd = [cmd.replace('--verbose', '') for cmd in (primary_cmd, sort_cmd)]
    # cmd_with_args = f'{primary_cmd} {threshold_arg} {ucs_save_path}'
    # full_cmd_str = f'( {cat_tsv_str} | {cmd_with_args} ) && {sort_cmd}'

    # > sourcery suggests:
    primary_cmd = ['ucs-make-tables', '--types']
    sort_cmd = ['ucs-sort', f'{ucs_save_path}',
                'BY', 'f2-', 'f1-', 'INTO', f'{ucs_save_path}']
    if verbose:
        primary_cmd, sort_cmd = [_make_verbose(
            c) for c in [primary_cmd, sort_cmd]]
    cmd_with_args = primary_cmd + \
        [f'--threshold={min_count}', f'{ucs_save_path}']
    full_cmd_str = f'( {cat_tsv_str} | {" ".join(cmd_with_args)} ) && {" ".join(sort_cmd)}'

    print('\n## Creating initial UCS table...')
    note = f'''
    == Note ==
    N = total number of tokens/all counts summed
    V = total number of rows/number of unique l1+l2 combinations before filtering to {min_count}+ tokens'''

    print('\n```')
    print(re.sub(r'([\|&]+)', r'\\ \n  \1', full_cmd_str))
    with Timer() as timer:
        system(full_cmd_str)

        print(note.strip())
        print(f'+ time to make table → {timer.elapsed()}')

    print('```\n')

    init_readable = ucs_save_path.parent.joinpath(
        f'readable/{ucs_save_path.name}'.replace('.ds.gz', '.init.txt'))
    confirm_dir(init_readable.parent)
    print('Saving initial frequency table in readable .txt format...')
    with Timer() as timer:
        print_cmd = f"ucs-print -o {init_readable} 'l1' 'l2' 'f' 'f2' 'f1' 'N' FROM {ucs_save_path}".split()
        if verbose:
            print_cmd = _make_verbose(print_cmd)
        run_shell_command(" ".join(print_cmd))
        print(f'+ time to save as txt → {timer.elapsed()}\n')


def build_ucs_from_multiple(tsv_paths,
                            min_count: int = 2,
                            count_type: str = 'bigram',
                            save_path: Path = None,
                            debug: bool = False):
    cmd = 'cat'
    save_path = save_path or f'{AM_ENV_DIR.parent}/polarized-{count_type}_min{min_count}x.ds.gz'
    if debug:
        cmd = 'head -50'
        save_path = save_path.parent.joinpath(f'debug/debug_{save_path.name}')
        confirm_dir(save_path.parent)
    build_ucs_table(
        ucs_save_path=save_path,
        cat_tsv_str=f"({' && '.join(f'{cmd} {p}' for p in tsv_paths)})",
        min_count=min_count
    )
    return save_path


def prep_by_polarity(in_paths_dict: dict,
                     row_limit: int = None,
                     words_to_keep: str = 'bigram',
                     data_suffix: str = ''):

    def _confirm_existing_tsv(tsv_obj):
        try:
            file_exists = tsv_obj.is_file()
        except AttributeError:
            for tsv in tsv_obj.values():
                if not Path(tsv).is_file():
                    sysxit(f'Input data {tsv} not found!')
        else:
            if not file_exists:
                sysxit(f'Input data {tsv} not found!')

    def _get_input_suff(in_paths_dict):
        suffix = '.tsv'
        for p in in_paths_dict.values():
            in_suff = re.findall(r'\.\d+f=\d+\+\.tsv', p.name)
            if any(in_suff):
                suffix = in_suff[0]
                break
        return suffix

    def _prep_lines(tsv_path: Path,
                    polarity: str,
                    row_limit: int = None,
                    data_suff: str = '',
                    words_to_keep: str = 'bigram'):

        def _new_line_gen(tsv_path: Path,
                          polarity: str,
                          row_limit: int = None,
                          words_to_keep: str = 'bigram'):
            def _read_tsv_rows(tsv_path: Path, row_limit: int = 0):
                return (tsv_path.read_text().splitlines()[:row_limit]
                        if row_limit
                        else tsv_path.read_text().splitlines())

            sub_keep_str = polarity.upper()
            if words_to_keep == 'bigram':
                sub_keep_str += r'\t\1_\2'
            elif words_to_keep == 'adv':
                sub_keep_str += r'\t\1'
            elif words_to_keep == 'adj':
                sub_keep_str += r'\t\2'
            for line in _read_tsv_rows(tsv_path, row_limit):
                yield _WORD_GAP.sub(sub_keep_str, line)

        prep_path = AM_ENV_DIR.joinpath(
            f'{polarity.lower()}_{words_to_keep}_counts{data_suff}')
        try:
            rel_path = tsv_path.relative_to(RESULT_DIR)
        except ValueError:
            rel_path = Path(*tsv_path.parts[-4:])
        print(
            f'\nProcessing ../{polarity} counts loaded from {rel_path}...')
        if not prep_path.is_file():
            prep_path.write_text('\n'.join(_new_line_gen(
                tsv_path, polarity, row_limit, words_to_keep)) + '\n')
        else:
            print(
                f'+ [{prep_path.relative_to(RESULT_DIR)} already exists -- not overwritten]')
        print('+ ✓ done')
        return prep_path

    _confirm_existing_tsv(in_paths_dict)
    input_data_suff = data_suffix or _get_input_suff(in_paths_dict)
    # input_data_suffix_strs = [''.join(p.suffixes) for p in in_paths_dict.values()]
    # input_data_flag = {suff:len(suff) for suff in input_data_suffix_strs if }
    print('---')
    polar_dict = {counts_label: _prep_lines(tsv_path=counts_tsv,
                                            polarity=counts_label,
                                            row_limit=row_limit,
                                            data_suff=input_data_suff,
                                            words_to_keep=words_to_keep)
                  for counts_label, counts_tsv in in_paths_dict.items()}
    # print('Polarity prepped counts saved as:')
    # print(f'\n'.join((f'+ {n.capitalize(): >10} -> '
    #                   + str(Path(*p.parts[-3:])) for n, p in polar_dict.items())))
    print_iter((f'{n.capitalize(): >10} -> '
                + str(Path(*p.parts[-3:])) for n, p in polar_dict.items()),
               bullet='+',
               header='Polarity prepped counts saved as:')
    return polar_dict



# * This function applies to the initial, `hit_id` indexed dataframe, ~ a "hit table".
def ucs_from_hit_table(df, col_1: str, col_2: str,
                       output_dir: Path = None,
                       ucs_path: Path = None,
                       filter_dict: dict = None,
                       ) -> pd.DataFrame:
    """
    Saves a DataFrame in UCS format based on specified columns and filters.

    This function applies to the initial, `hit_id` indexed dataframe (a "hit table"). 
    If either an output directory or a specific path are given, the resultant dataframe will be saved as a `.tsv`,
    which can be used as the (stdin/piped) input for `ucs-make-tables --types`.

    Args:
        df: The DataFrame to pull `value_counts` from.
        col_1: The name of the first column to count.
        col_2: The name of the second column to count.
        output_dir: The output directory for any UCS file.
        ucs_path: The path to save the UCS file. Generated from `output_dir`, `col_1`, and `col_2` if not given.
        filter_dict: An optional dictionary of column (key) == value pairs to filter the DataFrame. Filter info will be incorporated into any output path.

    Returns:
        The DataFrame with counts of unique combinations of col_1 and col_2.
    """
    cols_tag = re.compile(r'_([a-z]{,4})-([a-z]{,4})_', re.IGNORECASE)
    if col_1 not in df.columns:
        print(
            f'WARNING: col_1 "{col_1}" not in dataframe. Defaulting to "adv_form_lower"')
        col_1 = 'adv_form_lower'
        if ucs_path:
            ucs_path = ucs_path.with_name(
                cols_tag.sub(r'_Adv-\2_', ucs_path.name))

    if col_2 not in df.columns:
        print(
            f'WARNING: col_2 "{col_2}" not in dataframe. Defaulting to "adj_form_lower"')
        col_2 = 'adj_form_lower'
        if ucs_path:
            ucs_path = ucs_path.with_name(
                cols_tag.sub(r'_\1-Adj_', ucs_path.name))

    if output_dir and not ucs_path:
        ucs_dir = output_dir / 'ucs_format'
        confirm_dir(ucs_dir)
        ucs_path = (ucs_dir /
                    f'{snake_to_camel(col_1)}{snake_to_camel(col_2)}.tsv')

    if filter_dict:
        for col, val in filter_dict.items():
            df = df.loc[df[col] == val, :]
            if ucs_path:
                ucs_path = ucs_path.with_stem(
                    f"{ucs_path.stem}_{snake_to_camel(col)}{val.upper()}")
    if ucs_path:
        print(f'output path: {ucs_path}')
        counts = show_counts(df, [col_1, col_2]).reset_index()[
            ['count', col_1, col_2]]
        counts.to_csv(ucs_path, encoding='utf8',
                      sep='\t', header=False, index=False)

    return counts


# * This function applies to a "frequency table", a DataFrame where counts have already been calculated via `pd.crosstab`
#  The index for such a table will be unique values for the `index` Series passed, not unique tokens/observations,
#  and the values will be co-occurrence frequencies with the value indicated by the column.
def ucs_from_frq_table(frq_df,
                       output_tsv_path,
                       numeric_label='raw',
                       row_w1_label='adj_form_lower',
                       col_w0_label='adv_form_lower',
                       for_ucs: bool = False):
    """
    Saves a frequency table DataFrame in LSC format.

    This function applies to a "frequency table", a DataFrame where counts have already been calculated via `pd.crosstab`. The index for such a table will be unique values for the `index` Series passed, not unique tokens/observations, and the values will be co-occurrence frequencies with the value indicated by the column.

    Args:
        frq_df: The frequency table DataFrame to be saved.
        output_tsv_path: The path to save the LSC file.
        numeric_label: The label for the numeric column in the frequency table. Defaults to 'raw'.
        row_w1_label: The label for the row column in the frequency table. Defaults to 'adj_form_lower'.
        col_w0_label: The label for the column column in the frequency table. Defaults to 'adv_form_lower'.
        for_ucs: A boolean indicating whether the output is for UCS format. Defaults to False.

    Returns:
        None
    """

    def get_reshaped_output_lines(frq_df, row_w1_label, col_w0_label, for_ucs, new_col_name):
        lsc_format = reshape_totals(frq_df, new_col_name)
        lsc_format = _sort_stacks(
            row_w1_label, col_w0_label, new_col_name, lsc_format)
        return cleanup_output(for_ucs, lsc_format)

    def cleanup_output(for_ucs, lsc_format):
        counts_list = lsc_format.to_csv(sep="\t", index=False).splitlines()[1:]
        counts_lines = [x.strip() for x in counts_list]
        return counts_lines if for_ucs else ['2'] + counts_lines

    def save_tsv_file(output_tsv_path, output_lines):
        output_tsv_path.write_text(
            re.sub(r'^o[\._]?k[\._]?$', 'ok', '\n'.join(output_lines)), 
            encoding='utf8')
        print(
            f'* Simple tab-delimited counts saved as `.tsv`:\n  * path: `{output_tsv_path}`')

    def show_sample_output(output_lines):
        print('\n## Formatted Output Sample (top 20 bigrams)\n\n```log')
        print('\n'.join(output_lines[:20] + ['...']).expandtabs(8))
        print('```\n')

    def reshape_totals(frq_df, new_col_name):
        return frq_df.stack().to_frame(new_col_name)

    def _sort_stacks(row_w1_label, col_w0_label, new_col_name, stacked_df):
        stacked_df = stacked_df.reset_index()
        stacked_df['raw_frq'] = pd.to_numeric(
            stacked_df.raw_frq, downcast='unsigned')
        print_md_table(stacked_df.head(6).convert_dtypes(),
                       title='\n## Stacked\n')
        print_md_table(stacked_df.tail(6).convert_dtypes(), title='\n...\n')

        stacked_df = stacked_df[[new_col_name, col_w0_label, row_w1_label]]
        # stacked_df = (
        #     stacked_df
        #     .sort_values([row_w1_label, col_w0_label])
        # )
        # I don't think this ^^ makes a difference.
        #   Was trying to get it to sort A-Z within the same frequency value,
        #   but it seems to overwrite that regardless, since one requires ascending, and the other descending
        # But it doesn't really matter in any case.

        #! The zeros have to be dropped from the data for UCS, and it might affect LSC as well
        # ^ 💡 so maybe this should just return `nonzeros` dataframe?
        # HACK: #! if there are errors, check this
        nonzeros = stacked_df[stacked_df[new_col_name] != 0]
        return nonzeros.sort_values(new_col_name, ascending=False).reset_index(drop=True)

    def prep_to_reshape(frq_df, numeric_label, row_w1_label, col_w0_label):
        if row_w1_label in frq_df.columns:
            frq_df = frq_df.set_index(row_w1_label, drop=True)
        elif not frq_df.index.name:
            frq_df.index.name = row_w1_label
        if not frq_df.columns.name:
            frq_df.columns.name = col_w0_label

        frq_df = frq_df.loc[frq_df.index != 'SUM', frq_df.columns != 'SUM']

        return frq_df, f'{numeric_label}_frq'

    confirm_dir(output_tsv_path.parent)
    frq_df, new_col_name = prep_to_reshape(
        frq_df, numeric_label, row_w1_label, col_w0_label)
    output_lines = get_reshaped_output_lines(frq_df, row_w1_label,
                                             col_w0_label, for_ucs, new_col_name)

    show_sample_output(output_lines)
    save_tsv_file(output_tsv_path, output_lines)


def make_ucs_tsv(data_path,
                 col_1: str = None,
                 col_2: str = None):
    cross_regex = re.compile(r'([^_]+)-x-([^_]+)')
    """
        Reformat dataframe for UCS analysis.

    Args:
        data_path: The path to the data.
        col_1: The label for column 1.
        col_2: The label for column 2.

    Returns:
        None

    Examples:
        make_ucs_tsv('freq_out/*/freq_table.csv')
        make_ucs_tsv('4_post-processed/*/hit_table.pkl.gz', 
                     col_1='pattern', col_2='bigram_lower')
        make_ucs_tsv('4_post-processed/*/hit_table.pkl.gz', 
                     col_1='corpus', col_2='bigram_lower')
        make_ucs_tsv('4_post-processed/*/hit_table.pkl.gz', 
                     col_1='neg_form_lower', col_2='bigram_lower')
    """

    def _pull_labels_from_stem(stem, df):

        # > if both axes have a name, don't bother with extracting info from stem
        tags = [df.index.name, df.columns.name]
        if all(tags):
            return tags

        # > if not, use regular expression to locate the "__-x-__" cross info from the stem
        cross = cross_regex.search(stem)

        # ? #FIXME: is this right? is the ordering row, col or as it would be linearly in the text?
        # ^ if the loaded dataframe is a pickle, it won't matter --> the names will already be there.
        if not tags[0]:
            tags[0] = cross.groups(0)
        if not tags[1]:
            tags[1] = cross.groups(1)
        return tags

    def _set_out_path(data_path: Path,
                      data_stem: str,
                      col_1: str = None,
                      col_2: str = None) -> Path:
        out_dir = (data_path.with_name('ucs_format')
                   if 'freq_out' in data_path._parts
                   else FREQ_DIR / data_path.parent.name / 'ucs_format')
        confirm_dir(out_dir)
        if col_1 and col_2:
            data_name = re.search(
                r'(clean|f?r?q?-?thr)(.*$)', data_stem).group()
            prefix = '-x-'.join((snake_to_camel(re.sub(r'lower|form', '', c))[:4]
                                 for c in (col_1, col_2)))
            data_stem = f'{prefix}_{data_name}'
        return out_dir.joinpath(f'{data_stem}.tsv')

    def _load_df(data_path):
        stem = data_path.stem
        if '.pkl' in data_path.suffixes:
            df = pd.read_pickle(data_path)
            stem = Path(stem).stem
        else:
            df = pd.read_csv(data_path)
            if 'hit_id' in df.columns:
                df = df.set_index('hit_id')
        return df, stem
    
    
    df, data_stem = _load_df(data_path)
    print('# Reformatting co-occurence data for UCS analysis\n')
    print(f'* Loading from `{data_path}`')
    md_str = print_md_table(
        corners(df, 3), title='\n## Input Data\n', suppress=True)
    print(md_str.replace('-|:', ':|-').replace('-|\n', ':|\n'))

    # > table indexed by individual hit tokens
    # if data_path.is_relative_to('/share/compling/data/sanpi'):
    if df.index.name == 'hit_id':
        if 'adj_form_lower' in df.columns: 
            df['adj_form_lower'] = df.adj_form_lower.astype('string').apply(lambda x: re.sub(r'^o[\._]?k[\._]?$', 'ok', x))
        ucs_from_hit_table(
            df, col_1, col_2,
            ucs_path=_set_out_path(data_path, data_stem, col_1, col_2))

    # > crosstabulated frequency table of joint counts
    # if data_path.is_relative_to('/share/compling/projects/sanpi/results'):
    else:
        w1_row_label, w0_col_label = _pull_labels_from_stem(data_stem, df)
        ucs_from_frq_table(
            df,
            output_tsv_path=_set_out_path(data_path, data_stem),
            row_w1_label=w1_row_label,
            col_w0_label=w0_col_label,
            for_ucs=True)


def print_ex_assoc(df,
                   unit=None,
                   example_key=None,
                   round_level=2,
                   sort_by='am_p1_given2',
                   columns_like=r'^[Ecuj]|odds|^log.+d$|(given\d|_?f)$',
                   regex=False) -> None:
    """
    Prints a specific example from a dataframe.

    Args:
        df (pandas.DataFrame): The dataframe to extract the example from.
        count_type (str, optional): The type of count to consider. Defaults to None.
        example_key (str, optional): The key of the example to print. Defaults to None.
        round_level (int, optional): The number of decimal places to round the example values to. Defaults to 2.
        sort_by (str, optional): The column to sort the example by. Defaults to 'am_p1_given2'.
        columns_like (str, optional): The regular expression pattern to match column names. Defaults to r'^([^CORr_])'.
        regex (bool, optional): Whether to use regex pattern matching for the example key. Defaults to False.

    Returns:
        None
    """
    unit = unit or 'adv'
    _df = df.copy()
    if not example_key:
        example_keys = {
            'bigram': r'[drep]\w+(ly|er)|that',
            'adv': r'^[rep].+ly|that|ever',
            'adj': r'^(late|earl|clad|frustrat)|familiar',
            '': r'^(slight|absolute|utter|complete|perfect|ful|positive)ly',
            'adv~adj': r'^(slight|complete|perfect|^ful)ly',
        }
        example_key = example_keys[unit]
        regex = True
    # _df.update(_df.select_dtypes(include='float').apply(
    #     round, ndigits=round_level, axis=1))
    if regex:
        example = _df.filter(axis=0, regex=example_key)
    else:
        example = _df.filter(axis=0, like=example_key)
    if example.empty:

        example_key = r'[~_]un\w+'
        print(
            f'🤷 No {unit} match for {example_key}. Trying fallback regex, r"{example_key}"\n\n---')
        example = _df.filter(axis=0, regex=example_key)
    if example.empty:
        print(f'🤷 No {unit} match for r"{example_key}", either.\n\n---')
        return

    if sort_by not in example.columns:
        sort_by = example.columns.iloc[0]
    example = example.sort_values(
        sort_by, ascending=sort_by.startswith(('r_', 'l1', 'l2', 'ad')))

    example = example.filter(regex=r'^[a-z]|E11').filter(regex=columns_like)
    example.columns = adjust_assoc_columns(example.columns)
    example = example.iloc[:20, :]
    example = example.loc[:, example.columns != 'expect_diff']
    print_md_table(
        example,
        transpose=example.shape[0] < example.shape[1] * .8,
        n_dec=round_level,
        title=f'\n### {unit.capitalize()} "{example_key}" examples sorted by `{sort_by}` column\n')
    print('---')


def vary_lrc(obs_df, vocab: int):
    '''
    `am.conservative_log_ratio` defaults:
        disc=.5,
        alpha=.001,
        boundary='normal',
        correct='Bonferroni',
        vocab=None,
        one_sided=False,
    '''
    def generate_lrc_variations(obs_df, params_df):
        for ix in params_df.index:
            row = params_df.loc[ix, :]
            yield am.conservative_log_ratio(
                obs_df,
                # disc=row.disc,
                alpha=row.alpha,
                # boundary=row.boundary,
                # correct=row.correct,
                vocab=row.vocab if row.vocab > 0 else None,
                # one_sided=row.one_tail
            )

    lrc_param_variations = pd.DataFrame(
        data=itt.product(
            # > discounting (or smoothing) parameter for O11 == 0 and O21 == 0
            # (
            #     0.5, #^ (default)
            #     # 1.0,
            #     # 2
            # ),
            # > alpha--significance level
            (
                0.0005,
                # 0.001, #^ (default)
                # 0.005,
                # 0.010,
                # 0.05
            ),
            # > boundary--exact CI boundary of [poisson] distribution or [normal] approximation?
            # (
            #     'poisson', #^ (default)
            #     # 'normal'
            # ),
            # > correct--correction type for several tests (None | "Bonferroni" | "Sidak")
            # (
            #     "Bonferroni", #^ (default)
            #     "Sidak",
            # #     # None
            # ),
            # > vocab--size of vocabulary (number of comparisons for correcting alpha)
            (
                vocab,
                0  # ^ (default)
            ),
            # > one-sided--calculate one- or two-sided confidence interval
            # (
            #     True,  # ? Is value greater y?
            #     False,  # ? Is value different from y?  (default)
            # )
        ),
        columns=[  # 'disc', makes no difference in number of non-zero values
            'alpha',
            # 'boundary',
            #  'correct',
            'vocab',
            # 'one_tail'
        ]
    )
    lrc_var = lrc_param_variations.join(pd.DataFrame(generate_lrc_variations(obs_df, lrc_param_variations))
                                        ).set_index(lrc_param_variations.columns.to_list()).T
    import matplotlib as mpl
    mpl.pyplot.style.use('dark_background')
    mpl.pyplot.style.use('dark_background')
    mpl.rcParams['font.family'] = 'lato'
    print_md_table(lrc_var, transpose=True, describe=True, n_dec=2,
                   title='\n## Summary Stats: Conservative Log Ratio Parameter Variations\n')
    nonzero_rows = lrc_var.loc[lrc_var.apply(
        lambda x: any(x.round() != 0), axis=1), :]
    nonzero_lrc = (lrc_var.round() != 0).melt()
    nonzero_lrc_pos = (lrc_var.round() > 0).melt()

    nonzero_lrc.loc[nonzero_lrc.value, :].groupby('one_tail').value_counts(['vocab', 'alpha', 'value']).to_frame(
        'n_significant').reset_index().sort_values('n_significant', ascending=False)
    nonzero_lrc.loc[nonzero_lrc.value, :].groupby('vocab').value_counts(['correct', 'alpha', 'value']).to_frame('n_significant').reset_index(
    ).sort_values('n_significant', ascending=False).groupby('n_significant').value_counts(['correct', 'alpha', 'vocab'])
