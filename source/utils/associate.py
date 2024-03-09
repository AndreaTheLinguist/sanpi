# -*- coding=utf-8 -*-
import re
from os import system
from pathlib import Path
from sys import exit as sysxit

import pandas as pd
from .dataframes import Timer
from .general import confirm_dir, print_iter, run_shell_command, SANPI_HOME

UCS_HEADER_WRD_BRK = re.compile(r'\.([a-zA-Z])')
WORD_GAP = re.compile(r"(\b[a-z'-]+)\t([^_\s\t]+\b)")

DEMO_DIR = SANPI_HOME / 'DEMO'
RESULT_DIR, DEMO_RESULT_DIR = [W / 'results' for W in (SANPI_HOME, DEMO_DIR)]

FREQ_DIR, DEMO_FREQ_DIR = [
    R / 'freq_out' for R in (RESULT_DIR, DEMO_RESULT_DIR)]
UCS_DIR, DEMO_UCS_DIR = [
    R / 'ucs_tables' for R in (RESULT_DIR, DEMO_RESULT_DIR)]
POLAR_DIR, DEMO_POLAR_DIR = [
    R / 'polarity_prepped_tsv' for R in (UCS_DIR, DEMO_UCS_DIR)]

# ? Does this even do anything? This is never run as its own thing...
confirm_dir(RESULT_DIR)
confirm_dir(POLAR_DIR)


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


def convert_ucs_to_csv(ucs_path: Path, max_rows: int = None) -> Path:
    raw_text = UCS_HEADER_WRD_BRK.sub(
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


def make_verbose(cmd_parts: list, verbose_flag: str = '--verbose'):
    return cmd_parts.insert(1, verbose_flag)


def build_ucs_table(min_count: int,
                    ucs_save_path: Path,
                    cat_tsv_str: str,
                    verbose: bool = False):
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
        primary_cmd, sort_cmd = [make_verbose(
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
            print_cmd = make_verbose(print_cmd)
        run_shell_command(" ".join(print_cmd))
        print(f'+ time to save as txt → {timer.elapsed()}\n')


def prep_by_polarity(in_paths_dict: dict,
                     row_limit: int = None,
                     words_to_keep: str = 'bigram',
                     data_suffix: str = ''):
    confirm_existing_tsv(in_paths_dict)
    input_data_suff = data_suffix or _get_input_suff(in_paths_dict)
    # input_data_suffix_strs = [''.join(p.suffixes) for p in in_paths_dict.values()]
    # input_data_flag = {suff:len(suff) for suff in input_data_suffix_strs if }
    print('---')
    polar_dict = {counts_label: prep_lines(tsv_path=counts_tsv,
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


def _get_input_suff(in_paths_dict):
    suffix = '.tsv'
    for p in in_paths_dict.values():
        in_suff = re.findall(r'\.\d+f=\d+\+\.tsv', p.name)
        if any(in_suff):
            suffix = in_suff[0]
            break
    return suffix


def confirm_existing_tsv(tsv_obj):
    try:
        file_exists = tsv_obj.is_file()
    except AttributeError:
        for tsv in tsv_obj.values():
            if not Path(tsv).is_file():
                sysxit(f'Input data {tsv} not found!')
    else:
        if not file_exists:
            sysxit(f'Input data {tsv} not found!')


def prep_lines(tsv_path: Path,
               polarity: str,
               row_limit: int = None,
               data_suff: str = '',
               words_to_keep: str = 'bigram'):
    # // confirm_existing_tsv(tsv_path)
    # 👆 not needed because run on entire dict before this is applied
    prep_path = POLAR_DIR.joinpath(
        f'{polarity.lower()}_{words_to_keep}_counts{data_suff}')
    try:
        rel_path = tsv_path.relative_to(RESULT_DIR)
    except ValueError:
        rel_path = Path(*tsv_path.parts[-4:])
    print(
        f'\nProcessing ../{polarity} counts loaded from {rel_path}...')
    if not prep_path.is_file():
        prep_path.write_text('\n'.join(new_line_gen(
            tsv_path, polarity, row_limit, words_to_keep)) + '\n')
    else:
        print(
            f'+ [{prep_path.relative_to(RESULT_DIR)} already exists -- not overwritten]')
    print('+ ✓ done')
    return prep_path


def new_line_gen(tsv_path: Path, polarity: str, row_limit: int = None, words_to_keep: str = 'bigram'):
    sub_keep_str = polarity.upper()
    if words_to_keep == 'bigram':
        sub_keep_str += r'\t\1_\2'
    elif words_to_keep == 'adv':
        sub_keep_str += r'\t\1'
    elif words_to_keep == 'adj':
        sub_keep_str += r'\t\2'

    for line in read_rows(tsv_path, row_limit):
        yield WORD_GAP.sub(sub_keep_str, line)


def read_rows(tsv_path: Path, row_limit: int = 0):
    return (tsv_path.read_text().splitlines()[:row_limit]
            if row_limit
            else tsv_path.read_text().splitlines())


def build_ucs_from_multiple(tsv_paths,
                            min_count: int = 2,
                            count_type: str = 'bigram',
                            save_path: Path = None,
                            debug: bool = False):
    cmd = 'cat'
    save_path = save_path or f'{POLAR_DIR.parent}/polarized-{count_type}_min{min_count}x.ds.gz'
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


# * This function applies to the initial, `hit_id` indexed dataframe, ~ a "hit table".
def save_for_ucs(df, col_1: str, col_2: str,
                 output_dir: Path = None,
                 ucs_path: Path = None,
                 filter_dict: dict = None,
                 ) -> pd.DataFrame:
    """
    Saves a DataFrame in UCS format based on specified columns and filters.

    This function applies to the initial, `hit_id` indexed dataframe (a "hit table"). 
    If either an output directory or a specific path are given, the resultant dataframe will be saved as a `.tsv`,
    which can be used as the (stdin/piped) input for `usc-make-tables --types`.

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
