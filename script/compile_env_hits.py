# coding=utf-8
import argparse
import re
from pathlib import Path

import pandas as pd
from update_env_hits import remove_duplicates, save_final_info

from source.utils.dataframes import Timer
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import filter_csv_by_index as filter_csv
from source.utils.dataframes import remove_duplicates
from source.utils.general import HIT_TABLES_DIR, PKL_SUFF, confirm_dir
from source.utils.general import run_shell_command as shell_cmd

SUPER_NEG_DIR = HIT_TABLES_DIR / 'RBdirect'

def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    
    parser.add_argument(
        '-d','--data_dir',
        type=Path, default=SUPER_NEG_DIR,
        help=('')
        )

    return parser.parse_args()


def _main():
    data_dir = _parse_args().data_dir
    df = pd.concat(
        (pd.read_parquet(d, engine='pyarrow') 
        for d in data_dir.glob('[PAN]*_final.parq')))
    df = remove_duplicates(df)
    save_final_info(df, data_dir, 
                    tag=("NEG" if data_dir.name 
                         in ('NEGmirror', 'RBdirect') 
                         else 'POS'))
    concat_path = data_dir.joinpath(f'ALL-{data_dir.name}_final.parq')
    df.to_parquet(concat_path, engine='pyarrow', partition_cols=['part', 'slice'])


if __name__ == '__main__':
    with Timer() as timer:
        _main()
    
        print('✔️ Program Completed @ ', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')