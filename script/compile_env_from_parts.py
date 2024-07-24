# coding=utf-8
import argparse
# import re
from pathlib import Path
from time import sleep
import pandas as pd

from source.utils.dataframes import Timer, get_neg_equiv_sample as get_neq
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import remove_duplicates, save_final_info
from source.utils.general import HIT_TABLES_DIR, PKL_SUFF, confirm_dir
from source.utils.general import run_shell_command as shell_cmd

SUPER_NEG_DIR = HIT_TABLES_DIR / 'RBdirect'


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d', '--data_dir',
        type=Path, default=SUPER_NEG_DIR,
        help=('path to directory containing tables to combine into single')
    )

    return parser.parse_args()


def _main():
    data_dir = _parse_args().data_dir
    final_part_parqs = tuple(data_dir.glob('[PAN][!L]*_final.parq'))
    print(
        f'# Compiling final {data_dir.name} hits for all {len(final_part_parqs)} parts')
    print('\n* Loading from parquets')
    df = catify(pd.concat((pd.read_parquet(d, engine='pyarrow')
                           for d in final_part_parqs)),
                reverse=True)
    print('\n## Running final duplicate sweep')
    final_ids = remove_duplicates(
        df.filter(['utt_len', 'adv_index', 'neg_index', 'text_window',
                  'bigram_lower', 'adv_form_lower', 'token_str', 'mir_index']),
        return_index=True)
    df_final = df.filter(final_ids, axis=0)
    df_final['trigger_lemma'] = (df_final.trigger_lemma
                                 .str.replace("'", "")
                                 .str.replace('aint', 'not'))
    df_final = catify(df_final)
    print('\n## Saving Info for final selection')
    save_final_info(df_final, data_dir,
                    basic_column_filter=['hit_id', 'part', 'category',
                                         'trigger_lemma', 'bigram_lower',
                                         'all_forms_lower'], 
                    partition_by=['category', 'part'])
    print(('\n----------------------\n'
           '> *temporarily paused*\n'
           '----------------------\n'))
    sleep(60)
    print('\n## Saving Full Composite Frame')
    concat_path = data_dir.joinpath(f'ALL-{data_dir.name}_final.parq')
    save_final_parquet(df, concat_path)

    if data_dir.name == 'POSmirror': 
        sample_posmirror(df, concat_path)

def sample_posmirror(df: pd.DataFrame, concat_path: Path):
    data_dir = concat_path.parent
    timestamp = pd.Timestamp.now().strftime(".%y%m%d%H")
    neq_path = (str(concat_path)
                            .replace('ALL', 'NEQ')
                            .replace('.parq', f'_sample{timestamp}.parq'))
    neq = get_neq(df, data_dir, neg_name='NEGmirror')
    print('\n### Saving `NEQ` Sample Info')
    save_final_info(neq, data_dir, tag='NEQ',
                        date_flag=timestamp)
    print('\n## Saving Full Dataframe of NEQ Sample')
    save_final_parquet(neq, neq_path)

def save_final_parquet(df:pd.DataFrame, 
                       parquet_path:Path or str):
    partition_by = ['part']
    max_parq_rows = max(5000, 
                        int(round(((df.part.value_counts().mean()//10)
                        * 1.005), -3)))
    
    df.to_parquet(str(parquet_path), 
                  engine='pyarrow',
                  partition_cols=partition_by,
                  basename_template='group-{i}.parquet',
                  use_threads=True,
                  existing_data_behavior='delete_matching',
                  min_rows_per_group=min(
                              df.part.value_counts().min() - 1, 
                              max_parq_rows//8),
                  row_group_size=max_parq_rows,
                  max_rows_per_file=max_parq_rows
                  )
    
    print('\n+ **Successfully saved ✓**',
          f'as `{parquet_path}`',
          '+ partitioned by: ',
          f'  {repr(partition_by)}',
          '+ properties included:  ',
          ('\n' + repr(df.columns)
           ).replace('\n', '\n        ')+'\n',
          f'+ max rows per file: {max_parq_rows:,}',
          sep='  \n  ')
        # save_composite_parq(equal_sized_sample,
        #             sample_parq_part,
        #             sample=True)

if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('\n✓ Program Completed @ ', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
