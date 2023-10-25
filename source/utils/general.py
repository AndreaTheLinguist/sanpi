# coding=utf-8
from pathlib import Path
import logging


def confirm_dir(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True)


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


def dur_round(time_dur: float):
    """Take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits.

    Args:
        time_dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "m"

        if time_dur >= 60:
            time_dur = time_dur / 60
            unit = "h"

    if time_dur < 10:
        dur_str = f"{round(time_dur, 2):.2f}{unit}"
    else:
        dur_str = f"{round(time_dur, 1):.1f}{unit}"

    return dur_str


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


def find_glob_in_dir(dir_path: Path,
                     glob_expr: str,
                     recursive: bool = False,
                     verbose: bool = False) -> Path:
    path = None
    if recursive:
        paths_iter = tuple(dir_path.rglob(glob_expr))

    else:
        paths_iter = tuple(dir_path.glob(glob_expr))
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

    iter_str = bullet_str.join(f'{i}' for i in iter_obj)

    msg_str = f'\n{header}{bullet_str}{iter_str}'
    msg_str = msg_str.replace('\n\n', '\n').strip(f'{bullet} ')

    display_message(msg_str, logger, level)
