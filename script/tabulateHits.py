# coding=utf-8

import argparse
import json
import sys
import time
import re
from collections import namedtuple
from pathlib import Path
from pprint import pprint

import pandas as pd


def main():

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

    parser.add_argument('-p', '--pat_json_dir', type=Path, required=True,
                        help='path to directory containing filled json files '
                             'for pattern.')

    parser.add_argument('-o', '--outputPrefix', type=str, required=True,
                        help='prefix for output file to be written to the '
                             '\'hits\' subdirectory (created if necessary) '
                             'found in the directory the script is run from. '
                             'This should be a string which contains info about '
                             'the patterns, corpus data set, and nodes counted; '
                             'e.g. \'Nyt1_[pattern filename]_\' which would '
                             'result in the output file \'freq/Nyt1_p1-n1_adv-'
                             'adj_counts.csv\'.')


    parser.add_argument('-m', '--minimal', action='store_true',
                        help='Option produce minimal output. If used, output '
                             'will not have a header row and will have .txt '
                             'extension')

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

        df.columns = (df.columns.str.replace('\.', '_')
                      .str.replace('s_', '_'))

        df = df.rename(columns={'text': 'sent_text'})

        invert_pat = re.compile(r'(\w+)_([A-Z]+)')
        df.columns = [invert_pat.sub(r'\2_\1', label).lower()
                      for label in df.columns]

        ix_df = df.loc[:, df.columns.str.endswith('index')]
        ix_df = ix_df.assign(min_ix=ix_df.apply(lambda x: int(min(x)), axis=1),
                             max_ix=ix_df.apply(lambda y: int(max(y)), axis=1))
        windows = [
            df.lemma_str[x].split()[
                min(0,
                    ix_df.at[x, 'min_ix'] - 2):
                max(len(df.lemma_str[x]),
                    ix_df.at[x, 'max_ix'] + 2)]
            for x in df.index
        ]

        tok_ix_df = ix_df.loc[:, ix_df.columns.str.startswith(
            ('neg', 'adv', 'adj'))].apply(lambda c: c.astype('string'))

        df = df.assign(json_source=jf.stem,
                       match_ix=tok_ix_df.apply(
                           lambda x: '-'.join(x), axis=1),
                       lemma_window=[' '.join(w) for w in windows])

        df = df.convert_dtypes()

        # Note: This does not check that the adv and adj are actually true collocates
        if 'adv_word' in df.columns and 'adj_word' in df.columns:
            collocs = df.adv_word + '_' + df.adj_word
        else:
            collocs = ''

        df = df.assign(hit_id=df.sent_id + ':' + df.match_ix,
                       colloc=collocs)

        df_from_json = pd.concat([df, df_from_json])

    return df_from_json


def createOutput(hits_df, args):

    txt = args.minimal
    patPath = args.pat_json_dir
    patcat = patPath.parent.stem

    outputDir = patPath.cwd() / 'hits' / patcat

    if not outputDir.exists():
        outputDir.mkdir(parents=True)

    suffix = '.txt' if txt else '.csv'

    fname = f'{args.outputPrefix}_hits{suffix}'

    hits_df = hits_df.set_index('hit_id')

    hits_df = hits_df.assign(category=patcat).convert_dtypes()
    hit_cols = hits_df.columns

    # set given columns as categories (to reduce memory impact)
    catcols = ['colloc', 'adv_word', 'adj_word',
               'neg_word', 'nr_word', 'json_source', 'category',
               # 'mit_word', pos_word, test_word
               ]
    for col in catcols:
        if col not in hit_cols:
            hits_df[col] = '?'
    hits_df.loc[:, catcols] = hits_df[catcols].astype('category')

    # sort columns of dataframe
    priority_cols = [c for c in hit_cols
                     if c in ('colloc', 'sent_text', 'lemma_window', 'neg_word',
                              'adv_word', 'adj_word', 'relay_word', 'nr_word')]
    othercols = [c for c in hit_cols if c not in priority_cols]
    hits_df = hits_df[priority_cols + othercols]

    # write rows to file
    outpath = outputDir / fname
    hits_df.to_csv(outpath)

    view_sample_size = min(5, len(hits_df))
    label = 'Data'

    try:
        print_table = hits_df[['neg_word', 'colloc', 'sent_text']].sample(
            view_sample_size).to_markdown()
    except ImportError:
        pass
    else:
        print(f'```\n#### {label} Sample\n')
        print(print_table)
        print('```')


if __name__ == '__main__':

    absStart = time.perf_counter()
    main()
    absFinish = time.perf_counter()
    print(f'\nTime elapsed: {round(absFinish - absStart, 3)} seconds\n'
          '====================================\n')
