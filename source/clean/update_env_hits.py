# coding=utf-8
import argparse
import re
from pathlib import Path

import pandas as pd

from source.utils.dataframes import Timer, add_new_cols, adjust_few_hits
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import quarantine_deps, drop_not_only, save_hit_id_index_txt
from source.utils.dataframes import filter_csv_by_index as filter_csv
from source.utils.dataframes import remove_duplicates, write_part_parquet
from source.utils.general import HIT_TABLES_DIR, PKL_SUFF, confirm_dir
from source.utils.general import run_shell_command as shell_cmd

SANPI_DATA = HIT_TABLES_DIR.parent
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
                        data_dir=args.data_dir,
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
        if 'few' in df.neg_form_lower.unique():
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


def _get_index_path(part: str,
                    data_dir: Path or str,
                    top_dir_name: str,
                    link: bool = False):
    fname = f'clean_{part}_{top_dir_name}_index.txt'
    if link:
        fname = f'LINK-{fname}'
    return Path(data_dir).joinpath(fname)


def run_by_part(part: Path,
                data_dir: Path = SUPER_NEG_DIR,
                force_redo: bool = False):

    clean_dir = data_dir / 'cleaned'
    confirm_dir(clean_dir)
    # pat_cat = tuple(set(clean_dir.parts).intersection({'RBdirect', 'NEGmirror', 'POSmirror'}))[0]
    pat_cat = data_dir.name
    index_path = _get_index_path(part, data_dir=clean_dir,
                                 top_dir_name=pat_cat)
    neg_mirror = pat_cat == 'NEGmirror'
    pos_mirror = pat_cat == 'POSmirror'
    if not index_path.is_file():

        if neg_mirror:

            index_path = _retrieve_alternate_index(part, clean_dir, pat_cat,
                                                   fallback_pat='RBdirect')
        elif pos_mirror:
            index_path = _retrieve_alternate_index(part, clean_dir, pat_cat,
                                                   fallback_pat='not-RBdirect')
        if not index_path.is_file():
            try:
                index_path = tuple(data_dir.rglob(
                    f'clean*{part}*index.txt'))[0]
            except IndexError as e:
                raise FileNotFoundError('"/share/compling/projects/sanpi/script/update_env_hits.py:114"\n'
                                        + f'Path to corresponding "*{part}*index.txt" file not found.\n'
                                        + f'  (Search performed from "{data_dir}")') from e
    # dense_pickle = None if (neg_mirror or pos_mirror) else (
        # CONDENSED_DIR / f'{part}_all-RBdirect_unique-bigram-id_hits.pkl.gz')
    dense_pickle = (clean_dir.with_name('condensed')
                    / f'{part}_all-{pat_cat}_unique-bigram-id_hits.pkl.gz')
    if dense_pickle.is_file():
        csv_path = dense_pickle.with_name(
            dense_pickle.name.replace(PKL_SUFF, '.csv.bz2'))
        if not csv_path.is_file():
            pd.read_pickle(dense_pickle).to_csv(csv_path)
        csv_paths = [csv_path]
    else:
        csv_paths = list(clean_dir.glob(f'*{part}*hits.csv.bz2'))
        if len(csv_paths) < 2:
            csv_paths = list(clean_dir.parent.glob(f'*{part}*hits.csv.bz2'))
            if not any(csv_paths):
                csv_paths = list(data_dir.glob(f'*{part}*hits.csv'))

    for csv_path in csv_paths:
        saved_update_path = prep_csv(part=part,
                                     index_path=index_path,
                                     csv_path=csv_path,
                                     pat_cat=pat_cat,
                                     force_redo=force_redo)
        path_message = f'* ✓ Updated csv saved as {saved_update_path}'
        if index_path.name.startswith('LINK'):
            index_list = pd.read_csv(
                saved_update_path,
                usecols=['hit_id'], dtype='string',
                engine='c', low_memory=True).squeeze().to_list()

            print(f'* Updated `{pat_cat}` index for `{part}` saved as  ',
                  save_hit_id_index_txt(
                      index_vals=index_list,
                      out_path=saved_update_path), sep='\n  ')
            # print(save_hit_id_index_txt(
            #     index_vals=index_list,
            #     index_path=_get_index_path(part, index_path.parent,
            #                                top_dir_name=pat_cat)))
            # [x] save index of output csv as "particular" index
        print(path_message)
        print('-'*len(path_message)+'\n')
        yield saved_update_path


def _retrieve_alternate_index(part, clean_dir, pat_cat, fallback_pat):

    def _create_alt_link(alt_index_link, alt_index):
        print('Creating symbolic link to alternate index:  ',
              #   f'`"{alt_index_link.relative_to(data_dir.parent)}" -> "{alt_index.relative_to(data_dir.parent)}"`',
              #   sep='\n  '
              )
        ln_flags = 'srv'
        if Path(alt_index).is_symlink():
            ln_flags += 'L'

        shell_cmd(
            command_str=f'ln -{ln_flags} --force {alt_index} {alt_index_link}',
            verbose=True)

    alt_index_link = _get_index_path(part, data_dir=clean_dir,
                                     top_dir_name=fallback_pat, link=True)

    if alt_index_link.is_file():
        print(f'Found alternate `hit_id` index filter for {part} data:  ',
              f'`{alt_index_link}`', sep='\n  ')
        if alt_index_link.is_symlink():
            print('  * symlink pointing to '
                  f'`-> {alt_index_link.readlink()}`')
        return alt_index_link

    alt_index = _get_index_path(
        part, top_dir_name=fallback_pat,
        data_dir=str(clean_dir).replace(pat_cat, fallback_pat))

    if not alt_index.is_file():
        alt_index = _get_index_path(part, top_dir_name=fallback_pat,
                                    data_dir=str(clean_dir).replace(pat_cat, fallback_pat))
        if not alt_index.is_file() and fallback_pat == 'not-RBdirect':
            alt_index = Path(str(alt_index).replace(
                'cleaned', 'enforced').replace('index', 'no-neg_index'))
    if alt_index.is_file():
        _create_alt_link(alt_index_link, alt_index)

    if alt_index_link.is_file():
        return alt_index_link
    else:
        alt_index = _get_index_path(part, CLEAN_RBX_DIR, 'rb-bigram')
        if alt_index.is_file():
            alt_index_link = _get_index_path(part, clean_dir,
                                             top_dir_name='RBXadj', link=True)
            _create_alt_link(alt_index_link, alt_index)
        if alt_index_link.is_file():
            return alt_index_link


def prep_csv(part: str,
             index_path: Path,
             csv_path: Path,
             pat_cat: str = 'RBdirect',
             dtype_dict: dict = None,
             force_redo: bool = False):
    pattern = csv_path.name.split(f'{part}_')[1].split('_hits')[
        0].split('_')[0]
    print(f'\n# Filtering "{pattern}" hits in "{part}"\n\n'
          f'- starting csv: `{csv_path}`\n'
          f'- filtering index: `{index_path}`')

    output_csv_path = index_path.with_name(
        re.sub(r'^.*?(\w+_'+part+r')\w+_index.*$',
               r'\1_'+f'{pat_cat}_hits.csv.bz2',
               _get_index_path(part, index_path.parent, pat_cat).name))

    print(f'- updated file: `{output_csv_path}`\n\n'+('*' * 30))

    if output_csv_path.is_file() and not force_redo:
        print(f'✓ Corpus part {part} previously processed:\n  '
              f'{output_csv_path.relative_to(SANPI_DATA)} already exists.')
        shell_cmd(f'tree -hDtr --noreport --prune --matchdirs -P "*{output_csv_path.name.split(".")[0]}*"'
                  + f' {output_csv_path.parent} && echo "Total hits:"; '
                  + f'grep -c _eng_ {output_csv_path.parent}/*{part}*txt '
                  + '| cut -d/ -f6- | column -t -s: | tabulate -f fancy_grid')
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
