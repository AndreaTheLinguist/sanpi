import argparse
from pathlib import Path

import pandas as pd
from utils.general import confirm_dir
from utils.dataframes import get_proc_time
from utils.dataframes import save_in_lsc_format as export_counts
import re
cross_regex = re.compile(r'([^_]+)-x-([^_]+)')


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('reshape hits table for UCS or LSC application'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'data_path',
        type=Path,
        default=Path(
            '/share/compling/data/sanpi/4_post-processed/RBXadj/bigrams_frq-thr0-001p.35f.pkl.gz'),
        help=('path to dataframe containing values to reformat')
    )

    return parser.parse_args().data_path


def make_ucs_tsv(data_path):
    
    """
    Reformat frequency table dataframe for UCS analysis.

    Args:
        data_path: The path to the dataframe file.

    Returns:
        None
    """
    
    df, data_stem = _load_df(data_path)
    print('\n# Reformatting frequencies for UCS analysis',
          '\n## Input Data:',
          '\n```',
          sep='\n')
    print(df)
    print('```')
    w1_row_label, w0_col_label = pull_labels_from_stem(data_stem, df)
    export_counts(df,
                  output_tsv_path=set_out_path(data_path, data_stem),
                  row_w1_label=w1_row_label,
                  col_w0_label=w0_col_label,
                  for_ucs=True)


def _main():
    data_path = _parse_args()
    make_ucs_tsv(data_path)

def pull_labels_from_stem(stem, df):

    # > if both axes have a name, don't bother with extracting info from stem
    tags = [df.index.name, df.columns.name]
    if all(tags):
        return tags

    # > if not, use regular expression to locate the "__-x-__" cross info from the stem
    cross = cross_regex.search(stem)

    # ? #FIXME: is this right? is the ordering row, col or as it would be linearly in the text?
    # ^ if the loaded dataframe is a pickle, it won't matter --> the names will already be there.
    if not tags[0]:
        tags[0] = cross.groups(0)
    if not tags[1]:
        tags[1] = cross.groups(1)
    return tags


def set_out_path(data_path, data_stem):
    out_dir = data_path.with_name('ucs_format')
    confirm_dir(out_dir)
    return out_dir.joinpath(f'{data_stem}.tsv')


def _load_df(data_path):
    stem = data_path.stem
    if '.pkl' in data_path.suffixes:
        df = pd.read_pickle(data_path)
        stem = Path(stem).stem
    else:
        df = pd.read_csv(data_path)
        if 'hit_id' in df.columns:
            df = df.set_index('hit_id')
    return df, stem


if __name__ == '__main__':
    _t0 = pd.Timestamp.now()
    _main()
    _t1 = pd.Timestamp.now()

    print('✔️ Program Completed --', pd.Timestamp.now().ctime())
    print(f'   total time elapsed: {get_proc_time(_t0, _t1)}')
