# coding=utf-8
import argparse
import re
from pathlib import Path

import pandas as pd

from source.utils.dataframes import Timer, add_new_cols, adjust_few_hits
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import quarantine_deps, drop_not_only
from source.utils.dataframes import filter_csv_by_index as filter_csv
from source.utils.dataframes import remove_duplicates, write_part_parquet
from source.utils.general import HIT_TABLES_DIR, PKL_SUFF, confirm_dir
from source.utils.general import run_shell_command as shell_cmd

CLEAN_RBX_DIR = HIT_TABLES_DIR / 'RBXadj' / 'cleaned'
SUPER_NEG_DIR = HIT_TABLES_DIR / 'RBdirect'
COM_HIT_DIR = HIT_TABLES_DIR / 'not-RBdirect'
CLEAN_NEG_DIR = SUPER_NEG_DIR / 'cleaned'
CONDENSED_DIR = SUPER_NEG_DIR / 'condensed'


def _parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'script to apply updated filter to pattern hits and sweep for duplicate `text_window` strings'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--corpus_part', default=None,
        type=str, help=('corpus part tag to select both `--csv_path` and `--index_path`.'
                        '(index will default to `alpha` version.)'))

    parser.add_argument(
        '-d', '--data_dir',
        type=Path,
        default=SUPER_NEG_DIR,
        help=('path to directory housing dataframes to process if `-p/--corpus_part` provided. '
              '(Otherwise does nothing.)')
    )
    parser.add_argument(
        '-c', '--csv_path',
        type=Path,
        default=SUPER_NEG_DIR / 'bigram-PccVa_direct-adj-head_hits.csv.bz2',
        help=('path to dataframe saved as csv')
    )

    parser.add_argument(
        '-x', '--index_path',
        type=Path,
        # default=HIT_TABLES_DIR / 'not-RBdirect' / 'clean_bigram-PccVa_not-RBdirect_index.txt',
        default=SUPER_NEG_DIR / 'pre-cleaned' / \
        'PccVa_trigger_bigram-index_alpha-REclean.35f.txt',
        help=('path to text file containing `bigram_id` filter; id strings only separated by new lines')
    )

    parser.add_argument(
        '-F', '--force',
        default=False,
        action='store_true',
        help=('option to force reprocessing of all parts')
    )

    rgs = parser.parse_args()
    # if all([p.is_file() for __,p in rgs._get_kwargs()]):
    for a, p in rgs._get_kwargs():
        if rgs.corpus_part and a != 'data_dir':
            continue
        if isinstance(p, Path) and not p.exists():
            raise FileNotFoundError(
                f"\n* Invalid '--{a}' value\n  > '{p}' not found.")

    return rgs


def _main():
    args = _parse_args()
    if args.corpus_part is not None:
        part = args.corpus_part
        updated_csvs = tuple(
            run_by_part(part=args.corpus_part,
                        data_dir=args.data_dir / 'cleaned',
                        force_redo=args.force))

    else:
        index_path = args.index_path
        csv_path = args.csv_path
        part = re.search(r'[ANP][pwytc]{2}[VaTe\d]*', index_path.stem).group()
        updated_csvs = tuple(
            prep_csv(part, index_path, csv_path, 
                     force_redo=args.force))

    df = pd.concat(
        pd.read_csv(csv,
                    index_col='hit_id',
                    dtype=predict_dtypes(csv),
                    engine='c',
                    low_memory=True)
        for csv in updated_csvs)
    
    df = add_new_cols(df, part=part)
    env_cat = df.category.unique()[0]
    if env_cat in ('RBdirect', 'NEGmirror'):
        df = adjust_few_hits(df)
        df = drop_not_only(df)
    
    df = quarantine_deps(df,
                         dep_distance_ceiling=18,
                         dep_distance_floor=3)
    df = remove_duplicates(df)

    df = catify(df)
    parq_path = args.data_dir.joinpath(
        f'{part}-{env_cat}_final.parq')
    write_part_parquet(df, part=part, out_path=parq_path,
                       data_label=f'Final `"{env_cat}"` tokens')
    # df.sort_index().to_parquet(
    #     str(parq_path), engine='pyarrow',
    #     partition_cols=['slice'],
    #     basename_template='group-{i}.parquet',
    #     use_threads=True,
    #     existing_data_behavior='delete_matching',
    #     row_group_size=8000,
    #     max_rows_per_file=8000
    # )
    # print(f'\n* Final pattern matching hits for `{part}` saved as parquet:',
    #       'partitioned by "slice"',
    #       f'path:  \n    `{parq_path}`', sep='\n  * ')


def run_by_part(part: Path,
                data_dir: Path = CLEAN_NEG_DIR,
                force_redo: bool = False):
    index_path = data_dir.joinpath(
        f'clean_{part}_{data_dir.parent.name}_index.txt')
    if not index_path.is_file():
        try:
            index_path = tuple(data_dir.glob(f'clean*{part}*index.txt'))[0]
        except IndexError:
            raise FileNotFoundError('"/share/compling/projects/sanpi/script/update_env_hits.py:114"\n'
                                    + f'Path to corresponding "*{part}*index.txt" file not found.\n'
                                    + f'  (Search performed from "{data_dir}")')
    dense_pickle = (
        CONDENSED_DIR / f'{part}_all-RBdirect_unique-bigram-id_hits.pkl.gz')
    if dense_pickle.is_file():
        csv_path = dense_pickle.with_name(
            dense_pickle.name.replace(PKL_SUFF, '.csv.bz2'))
        if not csv_path.is_file():
            pd.read_pickle(dense_pickle).to_csv(csv_path)
        csv_paths = [csv_path]
    else:
        csv_paths = list(data_dir.glob(f'*{part}*hits.csv.bz2'))
        if not any(csv_paths):
            csv_paths = list(data_dir.parent.glob(f'*{part}*hits.csv.bz2'))
            if not any(csv_paths):
                csv_paths = list(SUPER_NEG_DIR.glob(f'*{part}*hits.csv'))

    for csv_path in csv_paths:
        saved_update_path = prep_csv(part=part,
                                     index_path=index_path,
                                     csv_path=csv_path,
                                     force_redo=force_redo)
        path_message = f'* ✓ Updated csv saved as {saved_update_path}'
        print(path_message)
        print('-'*len(path_message)+'\n')
        yield saved_update_path


def prep_csv(part: str,
             index_path: Path,
             csv_path: Path,
             dtype_dict: dict = None,
             force_redo: bool = False):
    pattern = csv_path.name.split(f'{part}_')[1].split('_hits')[
        0].split('_')[0]
    print(f'\n# Filtering "{pattern}" hits in "{part}"\n\n'
          f'- starting csv: `{csv_path}`\n'
          f'- filtering index: `{index_path}`')

    output_csv_path = Path(
            str(index_path).replace('_index.txt', '_hits.csv.bz2'))
    print(f'- updated file: `{output_csv_path}`\n\n'+('*' * 30))

    if output_csv_path.is_file() and not force_redo:
        print(f'✓ Corpus part {part} previously processed:\n  '
              f'{output_csv_path.relative_to(HIT_TABLES_DIR.parent)} already exists.')
        shell_cmd(f'tree -hDtr --noreport --prune --matchdirs -P "*{output_csv_path.name.split(".")[0]}*"'
            +f' {output_csv_path.parent} && echo "Total line(breaks):"; '
            +f'wc -l {output_csv_path.parent}/*{part}*txt')
    else:

        df = filter_csv(index_txt_path=index_path,
                        df_csv_path=csv_path,
                        dtype_dict=predict_dtypes(csv_path),
                        outpath=output_csv_path)

        if df:
            print(
                f'+ {len(df):,} total {index_path.parent.name} hits in {part}')
            with Timer() as _t:
                df.to_csv(output_csv_path)
                print(
                    f'+ saved as {output_csv_path}'
                    f'  + time to write new csv: {_t.elapsed()}',
                    sep='\n')
    return output_csv_path


def predict_dtypes(csv_path: Path) -> dict:
    snippet = pd.read_csv(csv_path, nrows=5)
    return dict(snippet.convert_dtypes()
                .dtypes.astype('string'))


if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print('\n✓ Program Completed @ ', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
