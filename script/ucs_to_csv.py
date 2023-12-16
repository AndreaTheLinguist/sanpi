# coding=utf-8
from pathlib import Path
import argparse
import contextlib
import re
with contextlib.suppress(ImportError):
    from utils import Timer
from utils import convert_ucs_to_csv


def _main():

    args = _parse_args()
    max_rows = args.row_limit
    ucs_path = args.ucs_text_path

    convert_ucs_to_csv(ucs_path, max_rows)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'script to convert text output of ucs table to comma separated (csv). '
            'If table is not in text format, run `ucs-print -o [file]` first.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-u', '--ucs_text_path',
        type=Path,
        default=Path(
            '/share/compling/projects/sanpi/results/ucs_tables/readable/polarized-bigram_min50x.rsort-view_top500.txt'),
        help=('path to text version of UCS table to convert')
    )
    parser.add_argument(
        '-r', '--row_limit',
        type=int,
        default=None,
        help='optional limit to number of rows to include in output'
    )

    return parser.parse_args()


if __name__ == '__main__':
    try:
        with Timer() as timer:

            _main()

            print(f'Total Time: {timer.elapsed()}')
    except NameError:
        _main()
