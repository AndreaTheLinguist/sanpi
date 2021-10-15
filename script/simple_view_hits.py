"""saves a simplified version (select columns only) of the hits table
    to a csv file with name '[label]_simplified.csv' to the parent directory of the original file.

    Arguments are: [csv path], [name of pat version (for labeling)]
    """
import pandas as pd
import argparse
# from sys import argv
from pathlib import Path

default_col_endings = ['colloc', 'window', 'word', 'id']


def main():
    source, select_cols, label = parse_arg_input()
    simplify(source, select_cols, label)


def parse_arg_input():

    parser = argparse.ArgumentParser(
        description=('saves a simplified version(select columns only) of the hits '
                     'table to a csv file with name `[label]_simplified.csv` '
                     'to the parent directory of the original file.'))

    parser.add_argument('full_hits', type=Path,
                        help='path to full hits .csv to simplify.')

    # TODO : give this default value corresponding to input file name
    parser.add_argument('output_label', type=str,
                        help='string for simplified file output file name')

    parser.add_argument('-k', '--keep_col', action='append', dest='select_cols',
                        metavar='COL_ENDING',
                        help=('option to specify columns for simplified output by ending.'
                              'Enter a string to match or partially match the column name: '
                              '`-k word` will select all columns ending in "word"= adv_word, '
                              'adj_word, neg_word, etc.; `-k adv_word` will keep columns ending '
                              'in "adv_word" (only that exact column). As many string matches '
                              'may be specified as desired (don\'t worry about possible overlap).'
                              'If this flag is not used, script will use the following by default: '
                              '{}'.format(default_col_endings)))

    args = parser.parse_args()

    select_cols = args.select_cols
    if not select_cols:
        select_cols = default_col_endings

    return(args.full_hits, select_cols, args.output_label)


def simplify(source, select_cols, label):

    df = pd.read_csv(source).convert_dtypes()
    all_cols = df.columns

    selection = []
    for substr in select_cols:
        col_matches = [c for c in all_cols if c.endswith(substr)]
        print(f'+ keeping ...{substr}: {col_matches}')
        selection.extend(col_matches)

    df = df[selection]

    sort_cols = [i for i in ['sent_text', 'sent_id', 'colloc']
                 if i in selection]
    if sort_cols:
        df = df.sort_values(sort_cols)
        print('Output filtered for duplicates and sorted by:', sort_cols)
        df = df[~df.duplicated(sort_cols)]
    else:
        print('Sorting columns not found:\n'
              '-> output will not be sorted\n'
              '-> duplicate filtering is not column dependent')
        df = df[~df.duplicated()]

    pd.set_option('display.max_colwidth', 80)

    sample = df[sort_cols].sample(min(5, len(df)))
    print(sample)

    outpath = source.parent.joinpath(f'{label}_simplified.csv')
    df.to_csv(outpath)
    print('...\n-> simplified viewing csv saved to', outpath)


if __name__ == '__main__':

    main()
