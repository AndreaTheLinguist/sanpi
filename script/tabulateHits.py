# coding=utf-8

import argparse
import json
import sys
import time
from collections import namedtuple
from pathlib import Path

import pandas as pd

# hit_tuple = namedtuple(
    # 'hit_tuple', ['hit_id', 'adv', 'adj', 'sent_text', 'sent_id', 'adv_index',
    #               'json_source', 'prev_sent', 'next_sent', 'all_tags', 'all_edges'])


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
        print(f'\n^_^ Finished collecting data for {hit_count}' 
              'sentence(s) from all json files.\n'
              '-> Writing tables to csv files...')
        createOutput(hit_data, args)


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

    # pull out sentence info and create dictionary of hit_id : namedTuple
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
            match_ix = get_adv_ids(json_dict)

            match_df = tokens.join(deps).assign(match_ix=match_ix)

            df = pd.DataFrame(json_dict)
            raw_minus_matching = df[
                ['sent_id','doc','text','prev_sent', 'next_sent']].assign(json_source=jf.stem)
            
            recombined_df = raw_minus_matching.join(match_df)
            
            hit_id = recombined_df.sent_id + ':' + recombined_df.match_ix
            recombined_df = recombined_df.assign(hit_id=hit_id)
            
            df_from_json = pd.concat((df_from_json, recombined_df))
            
            # for hit in json_dict:

                # sent_id = hit['sent_id']

                # try:
                #     fillers = hit['matching']['fillers']
                # except KeyError:
                #     print(f'-> Warning: Word info missing for {sent_id}. '
                #           f'Skipping hit.')
                #     continue

                # try:
                #     deps = hit['matching']['deps']
                # except KeyError:
                #     deps = {}
                #     continue

                # try:
                #     # Adverb -> args.node1 = 'adv' by default
                #     node1_word = fillers[args.node1].lower()
                # except KeyError:
                #     print(f'json entry missing first (ADV) node for '
                #           f'hit {sent_id}. Skipping hit.')
                #     continue

                # try:
                #     # Adjective -> args.node2 = 'adj' by default
                #     node2_word = fillers[args.node2].lower()
                # except KeyError:
                #     print(f'json entry missing second (ADJ) node for '
                #           f'hit {sent_id}. Skipping hit.')
                #     continue

                # sent_text = hit['text']
                # prev_sent = hit['prev_sent']
                # next_sent = hit['next_sent']

                # # ADV index
                # node1_index = hit['matching']['nodes'][args.node1]

                # # hit_id = [sentID]:[node index in sentence of adv token]
                # hit_id = ':'.join((sent_id, node1_index))

                # hit_info = hit_tuple(
                #     hit_id, node1_word, node2_word, sent_text, sent_id,
                #     node1_index, jf.stem, prev_sent, next_sent, fillers, deps)

                # hits_dict[hit_id] = hit_info

    # return hits_dict     
           
    return df_from_json.rename(columns={'doc': 'doc_id', 'text': 'sent_text'})


def get_deps(json_dict: dict):
    
    deps = [hit['matching']['deps'] for hit in json_dict]
    deps_clean = []
    hit_clean = {}
    for hit in deps: 
        for dep_name, dep_info in hit.items(): 
            if type(dep_info[2]) == dict: 
                dep_info[2] = dep_info[2]['1']

            dep_name = dep_name+'_dep'
            hit_clean[dep_name] = dep_info

        deps_clean.append(hit_clean)

    deps = pd.DataFrame(deps_clean)
    return deps
     
     
def get_tokens(json_dict: dict):
    
    tokens = pd.DataFrame([hit['matching']['fillers'] 
                                   for hit in json_dict])
    column_names = {}
    for c in tokens.columns: 
        column_names[c] = c.lower()+'_word'
        
    tokens = (tokens
              .assign(colloc=tokens.ADV + '_' + tokens.ADJ)
              .rename(columns=column_names))
    
    return tokens    
       

def get_adv_ids(json_dict: dict):
    
    nodes = pd.DataFrame([hit['matching']['nodes']
                          for hit in json_dict])
    
    match_ix = nodes.iloc[:,0] + '_' + nodes.iloc[:,1]
    return match_ix


def createOutput(hits_df, args):

    txt = args.minimal
    patPath = args.pattern
    patcat = patPath.parent.stem

    outputDir = patPath.cwd() / 'hits' / patcat

    if not outputDir.exists():
        outputDir.mkdir()

    suffix = '.txt' if txt else '.csv'

    fname =  f'{args.outputPrefix}_hits{suffix}'

    # hits_df = pd.DataFrame.from_dict(
        # {k: v._asdict() for k, v in hits.items()}, orient='index')
        
    # if write_duplicates:
        # hits_df = hits_df.assign(label=hits_df.index)
        # hits_df = hits_df.assign(
        #     status=hits_df.label.str.rsplit('_', 1).str.get(1))
        # hits_df = hits_df.assign(status=hits_df.status.astype('category'))
   
    hits_df = hits_df.set_index('hit_id')

    hits_df = (hits_df.assign(category=patcat).convert_dtypes())

    catcols = ['category', 'colloc', 'adv_word', 'adj_word', 'json_source']
    hits_df.loc[:, catcols] = hits_df[catcols].astype('category')

    cols = hits_df.columns.tolist()
    hits_df = hits_df[cols[-2:] + cols[:-2]]

    # write rows to file
    outpath = outputDir / fname
    hits_df.to_csv(outpath)

    view_sample_size = min(5, len(hits_df))
    label = 'Data'

    try:
        print_table = hits_df[['colloc', 'sent_text']].sample(
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
