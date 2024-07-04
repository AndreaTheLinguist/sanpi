# coding=utf-8

import argparse
import re
from pathlib import Path

import pandas as pd
from utils.dataframes import Timer, catify_hit_table as catify
from utils.general import HIT_TABLES_DIR


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('Hack script to remove any numerical-only "ad*_lemma" values remaining in already (p)re-cleaned hit partials. '
                     'Also updates hit_id index text file if it exists or creates one.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d', '--df_dir',
        type=Path,
        default=HIT_TABLES_DIR.joinpath('RBXadj/pre-cleaned'),
        help=('directory containing hit tables to drop numerical lemmas from')
    )
    parser.add_argument(
        '-p', '--corpus_part',
        default='Apw', type=str,
        help=('optional part identifier, e.g. "Pcc00", "Nyt1", "Apw", etc. '
              'If not specified, script will loop through all parts found in directory.'))

    return parser.parse_args()


def _main():
    print()
    args = _parse_args()
    part_regex = re.compile(r'(?<=bigram-)\w+(?=_rb)')
    part = args.corpus_part
    print(f'Part: {part}')
    df_dir = args.df_dir
    print(f'Directory: {df_dir}')
    if not part:
        df_paths = {part_regex.search(b.stem).group(): b
                    for b in df_dir.glob('*hits.csv.bz2')}
        for part, df_path in df_paths.items():
            drop_numerical_adx(part, df_path)
    else:
        try:
            df_path = tuple(df_dir.glob(f'*{part}*hits.csv.bz2'))[0]
        except IndexError:
            df_path = tuple(df_dir.glob(f'*{part}*hits.csv'))[0]
        drop_numerical_adx(part, df_path)


def process_df(df_path, output_path):
    print(f'> Loading from "{df_path}"')
    dtype_dict = {h: ('int64' if h.endswith(('index', 'len')) else 'string')
                  #! strip ".bz2" to get first line only
                  for h in Path(str(df_path).replace('.bz2', '')).read_text().splitlines()[0].split(',')}
    dtype_dict['Unnamed: 0'] = 'string'

    with pd.read_csv(df_path,
                     engine='c',
                     low_memory=True,
                     dtype=dtype_dict,
                     index_col='hit_id',
                     chunksize=100000) as hits_reader:
        for i, chunk in enumerate(hits_reader):
            print(f'## chunk {i+1}')
            with Timer() as t_chunk:
                if 'hit_id' in chunk.columns:
                    chunk = chunk.set_index('hit_id')
                elif not chunk.index.name:
                    chunk.index.name == 'hit_id'
                chunk = num_drop(chunk)
                if any(chunk.index.str.startswith('pcc')):
                    chunk['slice'] = chunk.index.str.split(
                        '.').str.get(0).astype('string')
                else:
                    chunk['slice'] = chunk.index.str.split(
                        '_').str[:3].str.join('_').str[:-2].astype('string')
                output_mode = 'a' if bool(i) else 'w'
                chunk.to_csv(output_path, mode=output_mode, header=not bool(i))
                update_index(output_path, chunk.index.to_list(), output_mode)
            print(
                f'  + time to process chunk and update txt and csv files\n    {t_chunk.elapsed()}')
            yield chunk


def update_index(output_csv_path: Path,
                 hit_ids: list,
                 output_mode: str = 'a'):
    hit_ids.sort()
    index_path = output_csv_path.with_name(
        output_csv_path.name.split('hits')[0] + 'index.txt')
    with index_path.open(mode=output_mode, encoding='utf8') as txt_file:
        out_str = '\n'.join(hit_ids)
        if output_mode == 'a':
            out_str = f'\n{out_str}'
        txt_file.write(out_str)
    return index_path


def drop_numerical_adx(part, df_path):

    csv_output_path = df_path.with_name(
        df_path.name.replace('_hits', '_alpha-hits'))
    parq_path = csv_output_path.with_name(
        csv_output_path.name.split('csv')[0]+'parq')
    if parq_path.exists():
        read_from_alpha(parq_path, csv_output_path)
    else:
        with Timer() as t_all:
            chunk_iter = process_df(df_path, csv_output_path)

            whole_df = catify(pd.concat(chunk_iter).sort_index())
            print(
                f'\nTotal time to load, filter, and concatenate all {part} chunks\n {t_all.elapsed()}')

    print(f'All of updated {part} hits saved as:')
    print(f'  + compressed csv: "{csv_output_path}"')
    if not parq_path.exists():
        whole_df.to_parquet(parq_path, partition_cols=['slice'])

    print(f'  + partitioned parquet: "{parq_path}"')


def read_from_alpha(alpha_parq, alpha_csv):
    print(f'> Loading from "{alpha_parq}"')
    with Timer() as _t:
        id_list = pd.read_parquet(
                alpha_parq,
                columns=['hit_id', 'adv_lemma', 'adj_lemma']).index.to_list()
        print(f'+ {len(id_list):,} total hits in "{alpha_parq.stem}"')
        index_path = update_index(
            output_csv_path=alpha_csv,
            hit_ids=id_list,
            output_mode='w')
        print(f'* Hit ID index updated ✓\n  > path: "{index_path}"')
        print(f'+ time to update index from parquet\n  {_t.elapsed()}')


def num_drop(df):
    init_len = len(df)
    # with Timer() as t_drop:
    df = df.loc[(df.adj_lemma.str
                .contains(r'[a-z]|50-50', regex=True)), :]
    df = df.loc[(df.adv_lemma.str
                .contains(r'[a-z]', regex=True)), :]
    print(f'  - {(init_len - len(df)):,} hits with numerical only adv or adj lemma dropped.\n    {len(df):,} remaining in chunk.')
    # print(f'    > Time elapsed ➡️ {t_drop.elapsed()}')
    return df


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('✔️ Program Completed @ ', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
