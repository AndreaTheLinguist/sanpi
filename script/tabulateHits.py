# coding=utf-8

import argparse
import json
import sys
import time
from collections import namedtuple
from pathlib import Path

import pandas as pd


def __main__():

    print("```\n### Tabulating hits via `tabulateHits.py`...\n```")
    args = parseArgs()

    json_dir = args.pattern
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

    parser.add_argument('-p', '--pattern', type=Path, required=True,
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

    parser.add_argument('-n1', '--node1', default='ADV',
                        help='search label for first node, default is \'ADV\'. '
                             'Both patterns being compared must have a single '
                             'node with this label.')

    parser.add_argument('-n2', '--node2', default='ADJ',
                        help='search label for second node, default is \'ADJ\'. '
                             'Both patterns being compared must have a single '
                             'node with this label.')

    parser.add_argument('-m', '--minimal', action='store_true',
                        help='Option produce minimal output. If used, output '
                             'will not have a header row and will have .txt '
                             'extension')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    parser.add_argument('-e', '--extraInfo', action='store_true',
                        help='Option to add ratio and totals to count output '
                             'file. **This option will do nothing if --count/-c '
                             'flag is not used.**')

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

            json_dict = json.load(j)

            if len(json_dict) < 1:

                print(f'--> File is empty. Skipping.')
                continue

            if not json_dict[0]['matching']['fillers']:
                raw_path = jf.with_suffix('.raw.json')
                print(f'-> Warning: Node labels have not been filled for {jf}. '
                      f'Skipping file.\n     * Hint: Run FillJson.py on '
                      f'{raw_path.name} and then try again.')
                continue

            deps = get_deps(json_dict)
            tokens = get_tokens(json_dict)
            match_ix, window_start, window_end = get_ix(json_dict)

            match_df = tokens.join(deps).assign(
                match_ix=match_ix,
                window_start=window_start,
                window_end=window_end)

            df = pd.DataFrame(json_dict)
            raw_minus_matching = df[
                ['sent_id', 'doc', 'text', 'prev_sent', 'next_sent']].assign(json_source=jf.stem)

            recombined_df = raw_minus_matching.join(match_df)

            hit_id = recombined_df.sent_id + ':' + recombined_df.match_ix
            recombined_df = recombined_df.assign(hit_id=hit_id)

            df_from_json = pd.concat((df_from_json, recombined_df))

    return df_from_json.rename(columns={'doc': 'doc_id', 'text': 'sent_text'})


def get_deps(json_dict: dict):

    deps = [hit['matching']['deps'] for hit in json_dict]
    deps_clean = []

    for hit in deps:
        hit_clean = {}
        for dep_name, dep_info in hit.items():
            if type(dep_info[2]) == dict:
                dep_info[2] = dep_info[2]['1']

            dep_name = dep_name+'_dep'
            hit_clean[dep_name] = dep_info

        deps_clean.append(hit_clean)

    deps = pd.DataFrame(deps_clean)
    # TODO : Add variables here as new dependency relation tags
    #   are introduced to/finalized in patterns
    neg_label = relay_label = 'n/a'
    if 'neg_dep' in deps.columns:
        neg_label = [dep_list[2] for dep_list in deps.neg_dep]
    if 'relay_dep' in deps.columns:
        relay_label = [dep_list[2] for dep_list in deps.relay_dep]

    deps = deps.assign(neg_deplabel=neg_label,
                       relay_deplabel=relay_label)

    return deps


def get_tokens(json_dict: dict):

    tokens = pd.DataFrame([hit['matching']['fillers']
                           for hit in json_dict])
    column_names = {}
    for c in tokens.columns:
        column_names[c] = c.lower()+'_word'

    try:
        collocs = tokens.ADV + '_' + tokens.ADJ
    except AttributeError:
        print('-> data is missing ADV or ADJ tags. No collocations specified.')
    else:
        tokens = tokens.assign(colloc=collocs)

    return tokens.rename(columns=column_names)


def get_ix(json_dict: dict):

    nodes = pd.DataFrame([hit['matching']['nodes']
                          for hit in json_dict])
    try:
        match_ix = nodes.ADV + '_' + nodes.ADJ
    except AttributeError:
        match_ix = nodes.iloc[:, 0] + '_' + nodes.iloc[:, 1]
    all_ix = [
        tuple(int(i) for i in hit['matching']['nodes'].values()) for hit in json_dict]
    window_start = [min(a) for a in all_ix]
    window_end = [max(a)+1 for a in all_ix]
    return match_ix, window_start, window_end


def createOutput(hits_df, args):

    txt = args.minimal
    patPath = args.pattern
    patcat = patPath.parent.stem

    outputDir = patPath.cwd() / 'hits' / patcat

    if not outputDir.exists():
        outputDir.mkdir()

    suffix = '.txt' if txt else '.csv'

    fname = f'{args.outputPrefix}_hits{suffix}'

    hits_df = hits_df.set_index('hit_id')

    hits_df = hits_df.assign(category=patcat).convert_dtypes()

    catcols = ['adv_word', 'adj_word', 'category', 'colloc',
               'json_source', 'neg_word', 'relay_word',
               # 'mit_word', pos_word, test_word
               ]

    for col in catcols:
        if col not in hits_df.columns:
            hits_df[col] = '?'
    hits_df.loc[:, catcols] = hits_df[catcols].astype('category')
    window_text_list = []
    for i, sent in enumerate(hits_df.sent_text):

        words = sent.split(' ')
        window_words = words[
            max(0, hits_df.window_start[i]-2):min(hits_df.window_end[i]+2, len(words))]
        window_text = ' '.join(window_words)
        window_text_list.append(window_text)

    hits_df = hits_df.assign(window_text=window_text_list)

    cols = hits_df.columns.tolist()
    hits_df = hits_df[cols[-2:] + cols[:-2]]

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
    __main__()
    absFinish = time.perf_counter()
    print(f'\nTime elapsed: {round(absFinish - absStart, 3)} seconds\n'
          '====================================\n')
