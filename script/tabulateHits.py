# coding=utf-8

import argparse
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd


def tabulate_hits():

    print("```\n### Tabulating hits via `tabulateHits.py`...\n```")
    args = parseArgs()

    json_dir = args.pat_json_dir.resolve()
    if not json_dir.exists():
        sys.exit('Error: Specified json directory does not exist.')
    if not json_dir.is_dir():
        sys.exit('Error: Specified json path is not a directory.')

    hit_data = getHitData(json_dir, args)

    hit_count = len(hit_data)
    if hit_count > 0:
        print(f'\n^_^ Finished tabulating data for {hit_count}'
              f' sentence(s) from all json files in {json_dir}.\n'
              '-> Writing tables to csv files...')
        createOutput(hit_data, args)
    else:
        sys.exit('No valid hits found.')


def parseArgs():
    parser = argparse.ArgumentParser(
        description='script consolidate relevant hit data from filled json files into csv files')

    parser.add_argument('pat_json_dir', type=Path,
                        help='path to directory containing filled json files '
                             'for pattern.')

    parser.add_argument('outputPrefix', type=str,
                        help='prefix for output file to be written to the '
                             '\'hits\' subdirectory (created if necessary) '
                             'found in the directory the script is run from. '
                             'This should be a string which contains info about '
                             'the patterns, corpus data set, and nodes counted; '
                             'e.g. \'Nyt1_[pattern filename]_\' which would '
                             'result in the output file \'freq/Nyt1_p1-n1_adv-'
                             'adj_counts.csv\'.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    return parser.parse_args()


def getHitData(json_dir, args):

    fileCount = 0
    df_from_json = pd.DataFrame()

    # check if there are any files other than the ...raw.json files
    processed_files = tuple(json_dir.glob('**/*[!w].json'))
    if not processed_files:
        sys.exit('Error: specified json directory does not contain any '
                 'processed json files.')

    for jf in processed_files:

        fileCount += 1

        print(f'-> Processing {jf.name}...')

        with open(jf, 'r', encoding='utf-8') as j:

            json_dicts = json.load(j)

            if len(json_dicts) < 1:

                print(f'--> File is empty. Skipping.')
                continue

            if 'matching' in json_dicts[0].keys():
                raw_path = jf.with_suffix('.raw.json')
                print(f'-> Warning: Node labels have not been filled for {jf}. '
                      'Skipping file.\n     * Hint: Run FillJson.py on '
                      f'{raw_path.name} and then try again.')
                continue

        df = pd.json_normalize(json_dicts, max_level=2)

        df.columns = (df.columns.str.replace('.', '_', regex=False)
                      .str.replace('s_', '_', regex=False))

        df = (df
              .rename(columns={'text': 'sent_text'})
              .assign(json_source=jf.stem))

        invert_pat = re.compile(r'(\w+)_([A-Z]+)')
        df.columns = [invert_pat.sub(r'\2_\1', label).lower()
                      for label in df.columns]

        df = process_ix(df)

        df = df.convert_dtypes()

        # Note: This does not check that the adv and adj are actually true collocates
        if 'adv_form' in df.columns and 'adj_form' in df.columns:
            collocs = df.adv_form + '_' + df.adj_form
        else:
            collocs = ''

        df = df.assign(hit_id=df.sent_id + ':' + df.match_ix,
                       colloc=collocs)

        df_from_json = pd.concat([df, df_from_json])

    return df_from_json


def process_ix(df):
    utt_len = df.token_str.apply(lambda x: len(x))
    ix_df = df.loc[:, df.columns.str.endswith('index')
                   ].fillna(0)

    ix_df = ix_df.apply(pd.to_numeric)

    ix_df = ix_df.assign(min_ix=ix_df.apply(lambda x: min(x), axis=1),
                         max_ix=ix_df.apply(lambda y: max(y), axis=1),
                         utt_len=utt_len,
                         token_str=df.token_str)

    windows = list(generate_window(ix_df))

    # select index int columns to be used in creating hit id
    tok_ix_df = ix_df.loc[:, ix_df.columns.str.startswith(
        ('neg', 'adv', 'adj'))].apply(lambda c: c.astype('string'))

    df = df.assign(match_ix=tok_ix_df.apply(lambda x: '-'.join(x), axis=1),
                   text_window=windows)

    return df


def generate_window(df):

    for row in df.index:
        min_ix = df.at[row, 'min_ix']
        max_ix = df.at[row, 'max_ix']
        go_back_2 = df.at[row, 'min_ix'] - 2
        go_forward_2 = df.at[row, 'max_ix'] + 2

        w0 = max(0, go_back_2)
        w1 = min(df.at[row, 'utt_len'],
                 go_forward_2) + 1

        yield ' '.join(df.token_str[row].split()[w0:w1])


def createOutput(hits_df, args):

    patPath = args.pat_json_dir
    patcat = patPath.parent.stem

    outputDir = patPath.cwd() / 'hits' / patcat

    if not outputDir.exists():
        outputDir.mkdir(parents=True)

    fname = f'{args.outputPrefix}_hits.csv'

    hits_df = hits_df.set_index('hit_id')

    hits_df = hits_df.assign(category=patcat).convert_dtypes()
    hit_cols = hits_df.columns

    # set given columns as categories (to reduce memory impact)
    catcols = ['colloc', 'adv_form', 'adj_form',
               'neg_form', 'nr_form', 'json_source', 'category',
               # 'mit_form', pos_form, test_form
               ]
    for col in catcols:
        if col not in hit_cols:
            hits_df[col] = '?'
    hits_df.loc[:, catcols] = hits_df[catcols].astype('category')

    # sort columns of dataframe
    required_cols = ['colloc', 'sent_text']
    priority_cols = [c for c in hit_cols
                     if c in ('text_window', 'neg_form',
                              'adv_form', 'adj_form', 'relay_form', 'nr_form')]
    other_cols = [c for c in hit_cols if c not in priority_cols]
    hits_df = hits_df[required_cols + priority_cols + other_cols]

    # write rows to file
    outpath = outputDir / fname
    hits_df.to_csv(outpath)

    view_sample_size = min(5, len(hits_df))
    label = 'Data'

    if args.verbose:
        try:
            print_table = hits_df[['neg_form', 'colloc', 'sent_text']].sample(
                view_sample_size).to_markdown()
        except ImportError:
            pass
        else:
            print(f'```\n#### {label} Sample\n')
            print(print_table)
            print('```')


if __name__ == '__main__':

    absStart = time.perf_counter()
    tabulate_hits()
    absFinish = time.perf_counter()
    print(f'\nTime elapsed: {round(absFinish - absStart, 3)} seconds\n'
          '====================================\n')
