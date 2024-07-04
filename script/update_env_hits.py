# coding=utf-8
import argparse
import re
from pathlib import Path

import pandas as pd

from source.utils.dataframes import Timer
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import filter_csv_by_index as filter_csv
from source.utils.dataframes import remove_duplicates
from source.utils.general import HIT_TABLES_DIR, PKL_SUFF, confirm_dir
from source.utils.general import run_shell_command as shell_cmd

CLEAN_RBX_DIR = HIT_TABLES_DIR / 'RBXadj' / 'pre-cleaned'
SUPER_NEG_DIR = HIT_TABLES_DIR / 'RBdirect'
COM_HIT_DIR = HIT_TABLES_DIR / 'not-RBdirect'
CLEAN_NEG_DIR = SUPER_NEG_DIR / 'pre-cleaned'
CONDENSED_DIR = SUPER_NEG_DIR / 'condensed'


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--corpus_part', default=None,
        type=str, help=('corpus part tag to select both `--csv_path` and `--index_path`.'
                        '(index will default to `alpha` version.)'))

    parser.add_argument(
        '-c', '--csv_path',
        type=Path,
        # default=CLEAN_RBX_DIR / 'clean_bigram-PccVa_rb-bigram_hits.csv',
        # 2_hit_tables/RBdirect/bigram-PccTe_direct-adj-head_hits.csv.bz2
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

    rgs = parser.parse_args()
    # if all([p.is_file() for __,p in rgs._get_kwargs()]):
    for a, p in rgs._get_kwargs():
        if isinstance(p, Path) and not p.is_file():
            raise FileNotFoundError(
                f"\n* Invalid '--{a}' value\n  > '{p}' not found.")

    return rgs


def run_by_part(args):
    part = args.corpus_part
    index_path = CLEAN_NEG_DIR.joinpath(
        f'{part}_trigger_bigram-index_alpha-REclean.35f.txt')

    dense_pickle = (
        CONDENSED_DIR / f'{part}_all-RBdirect_unique-bigram-id_hits.pkl.gz')
    if dense_pickle.is_file():
        csv_path = dense_pickle.with_name(
            dense_pickle.name.replace(PKL_SUFF, '.csv.bz2'))
        if not csv_path.is_file(): 
            pd.read_pickle(dense_pickle).to_csv(csv_path)
        csv_paths = [csv_path]
    else:
        csv_paths = list(CLEAN_NEG_DIR.glob(f'*{part}*REclean_hits.csv.bz2'))
        if not any(csv_paths):
            csv_paths = list(SUPER_NEG_DIR.glob(f'*{part}*hits.csv.bz2'))
            if not any(csv_paths):
                csv_paths = list(SUPER_NEG_DIR.glob(f'*{part}*hits.csv'))

    for csv_path in csv_paths:
        saved_update_path = prep_csv(part, index_path, csv_path)
        print(f'* ✓ Updated csv saved as {saved_update_path}')
        yield saved_update_path


def _main():
    args = _parse_args()
    if args.corpus_part is not None:
        part = args.corpus_part
        updated_csvs = tuple(run_by_part(args))

    else:
        index_path = args.index_path
        csv_path = args.csv_path
        part = re.search(r'[ANP][pwytc]{2}[VaTe\d]*', index_path.stem).group()
        updated_csvs = [prep_csv(part, index_path, csv_path)]

    df = pd.concat(pd.read_csv(
        csv,
        index_col='hit_id',
        dtype=predict_dtypes(csv),
        engine='c', low_memory=True)
        for csv in updated_csvs)

    df = catify(remove_duplicates(df))
    category = df.category.iloc[0]
    parq_path = updated_csvs[0].parent.parent.joinpath(
        f'{part}-{category}_final.parq')

    df.to_parquet(str(parq_path), engine='pyarrow', partition_cols=['slice'])
    print(f'Final `{SUPER_NEG_DIR.parent.name}` hits for `{part}` saved as parquet:',
          'partitioned by "slice"',
          f'path:  \n  `{parq_path}`', sep='\n* ')


def prep_csv(part: str,
             index_path: Path,
             csv_path: Path,
             dtype_dict: dict = None):
    pattern = csv_path.name.split(f'{part}_')[1].split('_hits')[
        0].split('_')[0]
    print(f'\n# Filtering "{pattern}" hits in "{part}"\n\n'
          f'- starting csv: `{csv_path}`\n'
          f'- filtering index: `{index_path}`')
    if str(index_path.parent) == str(CLEAN_NEG_DIR):
        output_csv_path = index_path.parent / (
            f'{part}_{pattern}'
            + re.search(r'(?<=index)[\w-]+(?=\.)',
                        index_path.stem).group()
            + '_hits.csv.bz2')
    else:
        output_csv_path = Path(
            str(index_path).replace('_index.txt', '_hits.csv.bz2'))
    print(f'- updated file: `{output_csv_path}`\n\n*********************')

    if output_csv_path.is_file():
        print(f'✓ Corpus part {part} previously processed:\n  '
              f'{output_csv_path.relative_to(HIT_TABLES_DIR)} already exists.')
        shell_cmd(
            f'tree -hDtr --matchdirs -P "*{output_csv_path.name.split(".")[0]}*" {output_csv_path.parent} && wc -l {output_csv_path.parent}/*{part}*txt')
    else:
        # columns in `pre-cleaned/*csv`
        #   hit_id,adv_form,adj_form,text_window,token_str,adv_lemma,adj_lemma,adv_index,adv_form_lower,adj_form_lower,bigram_lower,utt_len
        #! convert strings to category _after_ manipulations
        # dtype_dict = {h: ('int64' if h.endswith(('index', 'len')) else 'string')
        #   #! strip ".bz2" to get first line only
        #   for h in (Path(str(csv_path).strip('.bz2'))
        #             .read_text(encoding='utf8')
        #             .splitlines()[0].split(','))
        #   }

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
    snippet = pd.read_csv(csv_path, nrows=2)
    return dict(snippet.convert_dtypes()
                .dtypes.astype('string'))


if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print('\n✓ Program Completed @ ', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
