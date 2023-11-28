# coding=utf-8

import argparse
from pathlib import Path

import pandas as pd
from utils import (PKL_SUFF, 
                   Timer,
                   confirm_dir,
                   get_clean_data,
                   save_table,
                   save_filter_index)


def _main():

    args = _parse_args()
    in_path = args.data_path
    subdir_name = in_path.parent.name
    out_dir = args.out_dir.joinpath(subdir_name)
    confirm_dir(out_dir)
    data_stem = f'{in_path.name.strip(PKL_SUFF)}'
    out_path_str = f'{out_dir}/{data_stem}.clean'
    if not Path(out_path_str).with_suffix(PKL_SUFF).is_file():
        clean_df = get_clean_data(pd.read_pickle(in_path))
        
        save_table(df=clean_df, path_str=out_path_str,
                df_name=f'pre-cleaned {data_stem} dataframe')
        save_filter_index(index_path=out_dir.joinpath(
            f'{data_stem}.clean-index.txt'), df=clean_df)
    else: 
        print('Pre-Cleaned Dataframe already exists. Program Complete.')

def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'script to clean a single hit table for a single corpus part/dir (i.e. 1 of 35)'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        # '-d', '--data_path',
        'data_path',
        type=Path,
        # default=Path(
        #     '/share/compling/data/sanpi/debug/2_hit_tables/RBXadj/bigram-apw_rb-bigram_hits.pkl.gz'),
        help=('path to single pickled dataframe of hits which have not yet been cleaned (i.e. do not contain the suffix, `.clean`)')
    )

    parser.add_argument(
        '-o', '--out_dir',
        type=Path,
        default=Path('/share/compling/data/sanpi/3_pre-cleaned_hits'),
        help='path to parent directory for cleaned table outputs. All outputs will be organized under a subdirectory matching the parent of input file (=`data_path.parent.name`)')

    return parser.parse_args()


if __name__ == '__main__':
    with Timer() as timer: 
        # _t0 = pd.Timestamp.now()
        _main()
        # _t1 = pd.Timestamp.now()

        print('✓ Program Completed --', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
