# coding=utf-8
import argparse
from pathlib import Path

import pandas as pd


def _sample_pickle():
    """
    Prints a given sample size of a pickled dataframe to stdout as a markdown table or default `pandas` output.

    Args:
        None

    Returns:
        None

    Raises:
        None

    """
    args = _parse_args()

    d = pd.read_pickle(args.pickle)
    s = d.sample(min(len(d), args.sample_size))
    if args.columns:
        s = s[args.columns]
    length_info = (f'{len(s)} random' if len(s) < len(d) 
                  else f'All rows ({len(d)})')
    print(f'## {length_info} rows from `{args.pickle.name}`\n')
    if args.markdown:
        print(s.to_markdown(floatfmt=',.0f'))
    else:
        print(s)


def _parse_args():
    """
    Parses the command line arguments.

    Args:
        None

    Returns:
        argparse.Namespace: The parsed command line arguments.

    Raises:
        None

    """
    parser = argparse.ArgumentParser(
        description=(
            'simple script to print a sample of a pickled dataframe to stdout as either the default `pandas` output or as a markdown table (-m). Specific columns can be selected (defaults to all columns), and sample size can be dictated (defaults to 20 rows)'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('pickle',
                        type=Path, help=('path to pickled dataframe'))

    parser.add_argument(
        '-s', '--sample_size',
        type=int, default=20, action=None,
        help=('number of rows to include in sample'))
    
    parser.add_argument(
        '-c', '--column',
        type=str, action='append', dest='columns',
        default=[],
        help=('option to specify columns to print. Each must have its own `-c` flag. E.g. `-c COLUMN_1 -c COLUMN_2`')
    )
    parser.add_argument(
        '-m', '--markdown',
        action='store_true',
        default=False,
        help=('option to print in markdown table format')
    )

    return parser.parse_args()


if __name__ == '__main__':
    _sample_pickle()
