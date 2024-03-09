import argparse
import re
from pathlib import Path

import pandas as pd
from utils.dataframes import Timer, corners, print_md_table
from utils.dataframes import save_for_ucs as ucs_from_hits
from utils.dataframes import save_in_lsc_format as ucs_from_crosstab
from utils.general import confirm_dir, snake_to_camel

cross_regex = re.compile(r'([^_]+)-x-([^_]+)')


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'reshape hits or frequency table for UCS library application'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d',
        '--data_path',
        type=Path,
        # // action='append',
        # // dest='input_paths',
        default=Path(
            # '/share/compling/data/sanpi/4_post-processed/RBXadj/bigrams_frq-thr0-075p.2f.pkl.gz'
            '/share/compling/projects/sanpi/DEMO/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-0001p.3f=2+.pkl.gz'
        ),
        help=('path to dataframe containing values to reformat. Can be `.pkl.gz` or `.csv`, '
              'and can be a crosstabulated joint frequency table, or a table indexed by `hit_id`. '
              'If the latter, different columns for comparison can be specified '
              'using `-1/--col_1` and `-2/--col_2`. ')
    )

    parser.add_argument(
        '-1', '--col_1',
        type=str, default='adv_form_lower',
        help=('Option to specify first lexical column for UCS-formatted tsv, e.g. "category". '
              'output takes format of: "JOINT_FREQ\tCOL_1\tCOL_2; '
              'e.g. `--col_1=adv_form_lower` --> "987    very    good"'
              )
    )

    parser.add_argument(
        '-2', '--col_2',
        type=str, default='adj_form_lower',
        help=('Option to specify second lexical column for UCS-formatted tsv, e.g. "bigram_lower". '
              'output takes format of: "JOINT_FREQ\tCOL_1\tCOL_2; '
              'e.g. `--col_2=adv_form_lower` --> "987	good	very"'
              )
    )

    return parser.parse_args()


def make_ucs_tsv(data_path, col_1: str = None, col_2: str = None):
    """
        Reformat dataframe for UCS analysis.

    Args:
        data_path: The path to the data.
        col_1: The label for column 1.
        col_2: The label for column 2.

    Returns:
        None

    Examples:
        make_ucs_tsv('data.csv', 'column1', 'column2')
    """

    df, data_stem = _load_df(data_path)
    print('# Reformatting co-occurence data for UCS analysis\n')
    print(f'* Loading from `{data_path}`')
    md_str = print_md_table(
        corners(df, 3), title='\n## Input Data\n', suppress=True)
    print(md_str.replace('-|:', ':|-').replace('-|\n', ':|\n'))

    # > table indexed by individual hit tokens
    # if data_path.is_relative_to('/share/compling/data/sanpi'):
    if df.index.name == 'hit_id':

        ucs_from_hits(
            df, col_1, col_2,
            ucs_path=set_out_path(data_path, data_stem, col_1, col_2))

    # > crosstabulated frequency table of joint counts
    # if data_path.is_relative_to('/share/compling/projects/sanpi/results'):
    else:
        w1_row_label, w0_col_label = pull_labels_from_stem(data_stem, df)
        ucs_from_crosstab(
            df,
            output_tsv_path=set_out_path(data_path, data_stem),
            row_w1_label=w1_row_label,
            col_w0_label=w0_col_label,
            for_ucs=True)


def _main():
    args = _parse_args()

    make_ucs_tsv(args.data_path, args.col_1, args.col_2)


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


def set_out_path(data_path, data_stem, col_1: str = None, col_2: str = None):
    freq_out_dir = Path('/share/compling/projects/sanpi/results/freq_out')
    out_dir = (data_path.with_name('ucs_format')
               if 'freq_out' in data_path._parts
               else freq_out_dir / data_path.parent.name / 'ucs_format')
    confirm_dir(out_dir)
    if col_1 and col_2:
        prefix = '-'.join((snake_to_camel(c.replace('form',
                          '').replace('lower', ''))[:4] for c in (col_1, col_2)))
        data_stem = f'from-hit-table_{prefix}_{data_stem}'
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
    with Timer() as timer:
        _main()

        print('\n* Program Completed ✓')
        print(f'  * current time: {pd.Timestamp.now().ctime()}')
        print(f'  * total time elapsed: {timer.elapsed()}')
