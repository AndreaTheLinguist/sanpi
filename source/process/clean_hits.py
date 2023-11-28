# coding=utf-8

import argparse
from pathlib import Path
import sys

import pandas as pd
from utils import (PKL_SUFF, 
                   Timer,
                   confirm_dir,
                   save_table)

CLEAN_BIGRAMS_DIR = Path('/share/compling/data/sanpi/3_pre-cleaned_hits/RBXadj')

def _main():

    args = _parse_args()
    in_path = args.data_path
    subdir_name = in_path.parent.name
    out_dir = args.out_dir.joinpath(subdir_name)
    confirm_dir(out_dir)
    data_stem = f'{in_path.name.strip(PKL_SUFF)}'
    out_path_str = f'{out_dir}/{data_stem}.clean'
    if not Path(out_path_str).with_suffix(PKL_SUFF).is_file():
        #> Locate corresponding cleaned bigram index
        clean_index_path = _locate_index_path(data_stem)
        
        #> load dataframe and filter to only hits in the index
        
        init_df = _load_data(in_path)
        clean_df = apply_clean_filter(clean_index_path, init_df)
        
        save_table(df=clean_df, path_str=out_path_str,
                df_name=f'pre-cleaned {data_stem} dataframe')

    else: 
        print('Pre-Cleaned Dataframe already exists. Program Complete.')

def apply_clean_filter(clean_index_path, init_df):
    with Timer() as _timer:
        try: 
            bigram_ids = init_df['bigram_id']
        except KeyError: 
            bigram_ids = init_df['colloc_id']
        clean_df = init_df.loc[
                bigram_ids.isin(clean_index_path.read_text().splitlines()), :]
        print(f'* {(len(init_df) - len(clean_df)):,} of starting hits dropped during cleaning')
        print(f'> time to apply cleaning filter: {_timer.elapsed()}')
    return clean_df

def _load_data(in_path):
    with Timer() as _timer: 
        init_df = pd.read_pickle(in_path)
        print(f'> time to load starting dataframe: {_timer.elapsed()}')
    return init_df

def _locate_index_path(data_stem):
    corpus_id = data_stem.split('_', 1)[0]
    clean_index_glob = CLEAN_BIGRAMS_DIR.glob(f'*{corpus_id}*index.txt')
    try: 
        clean_index_path = list(clean_index_glob)[0]
    except IndexError: 
        sys.exit('corresponding clean bigram index not found.')
    return clean_index_path

def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'script to clean a single hit table for a single corpus part/dir (i.e. 1 of 35)'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d', '--data_path',
        # 'data_path',
        type=Path,
        default=Path(
            '/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-PccVa_direct-adj-head_hits.pkl.gz'),
        help=('path to single pickled dataframe of hits which have not yet been cleaned (i.e. do not contain the suffix, `.clean`)')
    )

    parser.add_argument(
        '-o', '--out_dir',
        type=Path,
        default=Path('/share/compling/data/sanpi/bigrams_pre-cleaned'),
        help='path to parent directory for cleaned table outputs. All outputs will be organized under a subdirectory matching the parent of input file (=`data_path.parent.name`)')

    return parser.parse_args()

if __name__ == '__main__':
    with Timer() as timer: 
        # _t0 = pd.Timestamp.now()
        _main()
        # _t1 = pd.Timestamp.now()

        print('✓ Program Completed --', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')