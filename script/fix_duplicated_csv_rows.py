# coding=utf-8

import argparse
from pathlib import Path

import pandas as pd


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'hack script to fix csv files where rows were appended multiple times'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--path',
        type=Path, default=None,
        help=('path to csv to remove redundant rows from')
    )

    return parser.parse_args()


def _main():
    args = _parse_args()
    csv = args.path
    if csv is None:
        csv = Path(
            '/share/compling/data/sanpi/2_hit_tables/RBdirect/pre-cleaned/PccVa_direct-adj-head_REclean_hits.csv.bz2')
    print(f'\n--> Fixing "{csv.relative_to(csv.parent.parent)}"')
    df = pd.read_csv(csv, engine='c', low_memory=True)
    print(df.hit_id.value_counts().nlargest(5))
    df = df.drop_duplicates()
    print(df.hit_id.value_counts().nlargest(5))
    df.set_index('hit_id').to_csv(csv)


if __name__ == '__main__':

    _main()

    print('✔️ Program Completed @ ', pd.Timestamp.now().ctime())
