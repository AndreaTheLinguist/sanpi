# coding=utf-8

from pathlib import Path
import argparse

import pandas as pd


def _main():
    args = _parse_args()
    
    df = pd.read_pickle(args.hits_pickle)
    if args.sample: 
        df = df.sample(args.sample)
    for adv, adj in zip(df.adv_lemma, df.adj_lemma):
        print(f'{adv}\t{adj}')


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('very simple script to print bigrams in format required for `ucs-make-tables`. Suggested usage: python script/print_for_ucs.py [path/to/hits_table] | ucs-make-tables'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    
    parser.add_argument(
        'hits_pickle',
        type=Path, default=Path('/share/compling/data/sanpi/4_post-processed/bigrams-only_thr0-01p.35f.pkl.gz'),
        help=('path to pickled table of hits: Must be (1) indexed by hit/token instance and (2) have the columns `adv_lemma` and `adj_lemma`.')
        )
    
    parser.add_argument('-s', '--sample', 
                        type=int, default=None, 
                        help=('option to limit output to a random sample of rows'
                        'intended for testing purposes'))

    return parser.parse_args()


if __name__ == "__main__":
    _main()

