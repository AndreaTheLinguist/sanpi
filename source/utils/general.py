# coding=utf-8
import logging
import re
from os import system
from pathlib import Path
from datetime import datetime

PKL_SUFF = '.pkl.gz'
<<<<<<< HEAD
=======
SANPI_HOME = Path('/share/compling/projects/sanpi')
>>>>>>> b8e6b5eecf35b37e0e1a70ecbe6c936332b9697b

def timestamp_now() -> str: 
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y-%m-%d_%H%M")

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
        print(message)


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

    if size >= 10**8:
        unit = 'G'
        power = 9
    elif size >= 10**5:
        unit = 'M'
        power = 6
    elif size >= 10**2:
        unit = 'K'
        power = 3
    else:
        unit = ''
        power = 0

    return f'{round(size / (10**power), 1):.1f} {unit}B'


def find_files(data_dir: Path(), fname_glob: str, verbose: bool = False):
    path_iter = data_dir.rglob(fname_glob)
    if verbose:
        path_iter = tuple(path_iter)
        print_iter(
            [f'../{p.relative_to(data_dir)}' for p in path_iter], bullet='-',
            header=f'### {len(path_iter)} paths matching {fname_glob} found in {data_dir}')
    return path_iter


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
                     verbose: bool = False) -> Path:
    path = None

    paths_iter = (tuple(dir_path.rglob(glob_expr))
                  if recursive else
                  tuple(dir_path.glob(glob_expr)))
    if paths_iter:
        path = paths_iter[0]
    elif verbose:
        print(f'Glob expression, "{glob_expr}", not found in {dir_path}/')
    return path


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
        iter_str = bullet_str.join(f'{k}:\t{v}' for k,v in iter_obj.items())
    else: 
        iter_str = bullet_str.join(f'{i}' for i in iter_obj)

    msg_str = f'\n{header}{bullet_str}{iter_str}'
    msg_str = msg_str.replace('\n\n', '\n').strip(f'{bullet} ')

    display_message(msg_str, logger, level)


def run_shell_command(command_str):
    print(f'\n```\n{command_str}')
    system(command_str)
    print('```\n')


def snake_to_camel(snake: str):
    return ''.join([w.capitalize() for w in snake.split('_')])
