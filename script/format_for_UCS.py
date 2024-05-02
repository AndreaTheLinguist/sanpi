import argparse
from pathlib import Path

import pandas as pd
from utils.associate import make_ucs_tsv
from utils.dataframes import Timer


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
        default=Path(
            '/share/compling/data/sanpi/4_post-processed/RBXadj/bigrams_clean.2f.pkl.gz'
            # '/share/compling/projects/sanpi/DEMO/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-0001p.3f=2+.pkl.gz'
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


def _main():
    args = _parse_args()

    make_ucs_tsv(args.data_path, args.col_1, args.col_2)


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('\n* Program Completed ✓')
        print(f'  * current time: {pd.Timestamp.now().ctime()}')
        print(f'  * total time elapsed: {timer.elapsed()}')
