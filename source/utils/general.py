# coding=utf-8
import errno
import logging
import re
from datetime import datetime
from os import system, strerror
from pathlib import Path
from scipy import constants as sc
import numpy as np

PKL_SUFF = '.pkl.gz'
POST_PROC_DIR = Path('/share/compling/data/sanpi/4_post-processed')
HIT_TABLES_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
SANPI_HOME = Path('/share/compling/projects/sanpi')
DEMO_DIR = SANPI_HOME / 'DEMO'
RESULT_DIR, DEMO_RESULT_DIR = [W / 'results' for W in (SANPI_HOME, DEMO_DIR)]

FREQ_DIR, DEMO_FREQ_DIR = [
    R / 'freq_tsv' for R in (RESULT_DIR, DEMO_RESULT_DIR)]

TEX_ASSETS = Path('/share/compling/projects/arh234/OverleafDissertex/assets')
#! Do not use following on cluster!!
#//   TEX_ASSETS = Path.home().joinpath('WinHome/Documents/OverleafDissertex/assets')

def hour_num(use_24):
    return ('%H', '') if use_24 else ('%I', '%P')


def timestamp_now(use_24: bool = True) -> str:
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    h, p = hour_num(use_24)
    return datetime.now().strftime(
        f"%Y-%m-%d_{h}%M{p}").strip('m')


def timestamp_now_trim(use_24: bool = True) -> str:
    h, p = hour_num(use_24)
    tstr = datetime.now().strftime(
        f"%y-%m-%d_{h}%M{p}")
    return tstr[:-3]+tstr[-2]


def timestamp_hour(use_24: bool = True) -> str:
    h, p = hour_num(use_24)
    return datetime.now().strftime(
        f"%Y-%m-%d_{h}{p}")


def timestamp_today() -> str:
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y-%m-%d")


def timestamp_month() -> str:
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y-%m")


def timestamp_year() -> str:
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y")


def camel_to_snake(camel: str):
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', camel).lower()


def confirm_dir(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True)


# def build_ucs_table(min_count: int, ucs_save_path: Path, cat_tsv_command: str):
#     threshold_arg = f'--threshold={min_count}'
#     primary_cmd = 'ucs-make-tables --types --verbose'
#     sort_cmd = f'ucs-sort -v {ucs_save_path} BY f2- f- INTO {ucs_save_path}'
#     cmd_with_args = ' '.join([primary_cmd, threshold_arg, ucs_save_path])
#     full_cmd_str = ' | '.join([cat_tsv_command, cmd_with_args])
#     full_cmd_str += f'&& {sort_cmd}'
#     print()
#     print(re.sub(r'([\|&]+)', r'\\ \n  \1', full_cmd_str))
#     print()
#     system(full_cmd_str)

#     note = '''
# == Note ==
# N = total number of tokens/all counts summed
# V = total number of rows/number of unique combinations before filtering to {}+ tokens
#     '''.format(min_count)  # pylint: disable=consider-using-f-string
#     print(note)


def display_message(message: str,
                    logger: logging.Logger = None,
                    level: int = 20):
    """Print or send to log if given. log level of message defaults to info (20)."""
    if logger:
        if message.startswith('#'):
            message = '\n' + message
        logger.log(level=level, msg=message)
    else:
        print(message, end='\n\n')


def view_doc(expr):
    try:
        print(expr.__doc__)
    except AttributeError:
        print('None')


def dur_round(time_dur: float):
    """Take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits.

    Args:
        time_dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur /= 60
        unit = "m"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "h"

    return (
        f"{round(time_dur, 2):.2f}{unit}"
        if time_dur < 10
        else f"{round(time_dur, 1):.1f}{unit}"
    )


def file_size_round(size: int):
    unit = ''
    constant = 1
    for unit, constant in {
        'G': sc.giga,
        'M': sc.mega,
        'K': sc.kilo,
        '': 1,
    }.items():
        if round(size) < constant:
            continue
        else:
            return f'{round((size / constant), 1):.1f} {unit}B'

    # if size >= sc.giga:
    #     unit = 'G'
    #     power = 9
    # elif size >= sc.mega:
    #     unit = 'M'
    #     power = 6
    # elif size >= sc.kilo:
    #     unit = 'K'
    #     power = 3
    # else:
    #     unit = ''
    #     power = 0


def find_files(data_dir: Path(), fname_glob: str, verbose: bool = False):
    path_iter = data_dir.rglob(fname_glob)
    if verbose:
        path_iter = tuple(path_iter)
        print_iter(
            [f'../{p.relative_to(data_dir)}' for p in path_iter], bullet='-',
            header=f'### {len(path_iter)} paths matching {fname_glob} found in {data_dir}')
    return path_iter


def gen_random_array(low, high, nvals=8, nvecs=20):

    rng = np.random.default_rng(
        seed=int(f"{np.datetime64('now', 'h')}".replace('-', '').replace('T', '')))
    c = 0
    while c < nvecs:
        yield rng.integers(low=low, high=high, size=nvals)
        c += 1


def indent_block(block: str = '',
                 lines: list = None,
                 indent: int = 2,
                 hang: bool = False) -> str:

    i_prefix = ' '*indent
    if block:
        lines = block.splitlines()

    i_block = i_prefix.join(iter(lines))

    return i_block if hang else i_prefix + i_block


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


def convert_ucs_to_csv(ucs_path, max_rows=None):
    raw_text = ucs_header_wrd_brk.sub(
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

    write_ucs_csv(get_ucs_csv_path(trimmed_len, ucs_path), csv_lines)


def find_glob_in_dir(dir_path: Path,
                     glob_expr: str,
                     recursive: bool = False,
                     verbose: bool = False,
                     err_response: str = '') -> Path:

    paths_iter = (tuple(dir_path.rglob(glob_expr))
                  if recursive else
                  tuple(dir_path.glob(glob_expr)))
    # if paths_iter:
    #     path = paths_iter[0]
    # elif verbose:

    try:
        return paths_iter[0]
    except IndexError as e:
        if err_response:
            if err_response == 'raise':
                raise FileNotFoundError(
                    errno.ENOENT, strerror(errno.ENOENT), str(dir_path.joinpath(glob_expr))) from e
            elif err_response == 'return':
                return str(dir_path.joinpath(glob_expr))
        elif verbose:
            print(f'Glob expression, "{glob_expr}", not found in {dir_path}/')

    return


def percent_to_count(percent: float, total: int) -> int:
    return int(round(total * (percent / 100)))


def print_iter(iter_obj,
               bullet: str = '▸',
               logger: logging.Logger = None,
               level: int = 20,
               header: str = '',
               indent: int = 0):

    bullet_str = f'\n{" " * indent}{bullet} '
    if isinstance(iter_obj, dict):
        iter_str = bullet_str.join(f'{k}:\t{v}' for k, v in iter_obj.items())
    else:
        iter_str = bullet_str.join(f'{i}' for i in iter_obj)

    msg_str = f'\n{header}{bullet_str}{iter_str}'
    msg_str = msg_str.replace('\n\n', '\n').replace('\t','\n\t').strip(f'{bullet} ')

    display_message(msg_str, logger, level)


def run_shell_command(command_str: str,
                      verbose: bool = False):
    verbose_command = f'\n$ {command_str}\n' if verbose else ''
    print(f'\n```shell\n{verbose_command}')
    system(command_str)
    print('```\n')


def snake_to_camel(snake: str):
    """Convert a snake_case string to camelCase.

    Args:
        snake (str): The snake_case string to convert.

    Returns:
        str: The camelCase version of the input string.
    """
    # return re.sub(r'_(\w)',r'\1'.upper(), snake)
    return ''.join([w[0].upper()+w[1:] if i != 0 else w for 
                    i, w in enumerate(snake.split('_'))])
