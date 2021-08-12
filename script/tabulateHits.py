# coding=utf-8

import argparse
import json
import sys
import time
from collections import namedtuple
from pathlib import Path

import pandas as pd

hit_tuple = namedtuple(
    'hit_tuple', ['hit_id', 'adv', 'adj', 'sent_text', 'sent_id', 'adv_index',
                  'json_source', 'prev_sent', 'next_sent'])


def __main__():

    print("```\n### Tabulating hits via `tabulateHits.py`...\n```")
    args = parseArgs()

    # do table by default if no output type option specified.
    # if not (args.table or args.count):
    #     args.table = True
    #     print(
    #         'Warning: No output type specified. Output will be table of hits,
    #         not counts.')

    json_dir = args.pattern
    if not json_dir.exists():
        sys.exit('Error: Specified json directory does not exist.')
    if not json_dir.is_dir():
        sys.exit('Error: Specified json path is not a directory.')

    # colloc_counter = None
    # hit_data = None
    #
    # if args.count:
    #
    # colloc_counter = fillCounter(json_dir, args)
    #
    # print('^_^ Finished counting collocations in all json files.')
    #
    # if args.table:

    hit_data, duplicates = getHitData(json_dir, args)

    print('\n^_^ Finished collecting sentence data from all json files.\n'
          '    -> Writing tables to csv files...')

    if len(hit_data) > 0:
        createOutput(hit_data, args)

    if len(duplicates) > 0:
        createOutput(duplicates, args, write_duplicates=True)


def parseArgs():
    parser = argparse.ArgumentParser(
        description='script consolidate relevant hit data from filled json files'
                    ' into csv files')

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

    # parser.add_argument('-t', '--table', action='store_true',
    #                     help='Option to create a table output with following
    #                     fields: hit_id, adv, adj, colloc, sent_text, sent_id,
    #                     adv_index, ')
    #
    # parser.add_argument('-c', '--count', action='store_true',
    #                     help='Option to create an output of counts with
    #                     following fields (minimally): Adv, Adj, hit_counts')

    parser.add_argument('-e', '--extraInfo', action='store_true',
                        help='Option to add ratio and totals to count output '
                             'file. **This option will do nothing if --count/-c '
                             'flag is not used.**')

    return parser.parse_args()

#
# def fillCounter(json_dir, args):
#
#     counter = Counter()
#
#     startTime = time.perf_counter()
#     fileCount = 0
#
#     for jsonFile in os.scandir(json_dir):
#
#         if (jsonFile.name.endswith('raw.json')
#                 or not jsonFile.name.endswith('json')):
#             continue
#
#         fileCount += 1
#
#         if args.verbose:
#             print(f'\nProcessing {jsonFile.name}...')
#
#         counter = countTokenPairs(counter, jsonFile.path, args)
#
#     if args.verbose:
#         print(
#             f'\nTop 10 collocations for entire {json_dir.name} directory:')
#         pprint.pprint(counter.most_common(10))
#
#     finishTime = time.perf_counter()
#
#     print(f'\nFinished counting {json_dir.name}.')
#     print(f'Collocations from {fileCount} total files counted '
#           f'in {round(finishTime - startTime, 2)} seconds')
#
#     return counter
#
#
# def countTokenPairs(countDict, jsonFile, args):
#
#     wordType1 = args.node1
#     wordType2 = args.node2
#     colloc = namedtuple('collocation', [wordType1, wordType2])
#
#     with open(jsonFile, 'r') as j:
#
#         hits = json.load(j)
#
#         for hit in hits:
#             try:
#
#                 nodes = hit['matching']['fillers']
#
#             except KeyError:
#                 sys.exit(
#                     f'Node labels have not been filled from conllu file for {jsonFile}. Quitting script without generating output.')
#
#             else:
#
#                 tupleKey = colloc(nodes[wordType1], nodes[wordType2])
#
#                 if tupleKey not in countDict.keys():
#
#                     countDict[tupleKey] = 1
#
#                 else:
#
#                     countDict[tupleKey] += 1
#
#                 # use (named)tuple as key in dictionary.
#                 # e.g. [(word1=x, word2=y): count, (word1=a, word2=b): count, ...]
#
#     if args.verbose:
#         print('Top 3 (running totals):')
#         pprint.pprint(countDict.most_common(3))
#
#     return countDict
#

def getHitData(json_dir, args):

    # pull out sentence info and create dictionary of hit_id : namedTuple
    fileCount = 0
    hits_dict = {}
    duplicates = {}

    processed_files = tuple(json_dir.glob('**/*[0-9].json'))
    if not processed_files:
        sys.exit('Error: specified corpus directory does not contain any '
                 'processed json files.')

    for jf in processed_files:

        fileCount += 1

        print(f'-> Processing {jf.name}...')

        with open(jf, 'r', encoding='utf-8') as j:

            hits = json.load(j)

            if len(hits) < 1:

                print(f'--> File is empty. Skipping.')
                continue

            if not hits[0]['matching']['fillers']:
                raw_path = jf.with_suffix('.raw.json')
                print(f'-> Warning: Node labels have not been filled for {jf}. '
                      f'Skipping file.\n     * Hint: Run FillJson.py on '
                      f'{raw_path.name} and then try again.')
                continue

            for hit in hits:
                sent_id = hit['sent_id']

                try:
                    fillers = hit['matching']['fillers']
                except KeyError:
                    print(f'-> Warning: Word info missing for {sent_id}. '
                          f'Skipping hit.')
                    continue

                try:
                    # Adverb -> args.node1 = 'adv' by default
                    node1_word = fillers[args.node1].lower()
                    # Adjective -> args.node2 = 'adj' by default
                    node2_word = fillers[args.node2].lower()
                except KeyError:
                    print(f'json entry missing one or both token nodes for '
                          f'hit {sent_id}. Skipping hit.')
                    continue

                sent_text = hit['text']
                prev_sent = hit['prev_sent']
                next_sent = hit['next_sent']

                # ADV index
                node1_index = hit['matching']['nodes'][args.node1]

                # hit_id = [sentID]:[node index in sentence of adv token]
                hit_id = ':'.join((sent_id, node1_index))

                hit_info = hit_tuple(
                    hit_id, node1_word, node2_word, sent_text, sent_id,
                    node1_index, jf.stem, prev_sent, next_sent)

                hits_dict, duplicates = assign_info(hit_info,
                                                    hits_dict, duplicates)

    return hits_dict, duplicates


def assign_info(hit: hit_tuple,
                hits_dict: dict,
                duplicates: dict):

    hit_sent = hit.sent_text
    prev_match_ids = [v.hit_id for v in hits_dict.values()
                      if v.sent_text == hit_sent]

    hit_id = hit.hit_id

    # if hit_id in hits_dict.keys():

    #     existing_info = hits_dict[hit_id]

    #     # exact same--nothing differs, so nothing added
    #     if hit == existing_info:

    #         print(f'-> Hit {hit_id} discarded:\n   + Token for '
    #               f'"{existing_info.adv} {existing_info.adj}" '
    #               f'(with identical info) already recorded.')

    #         duplicates[f'{hit_id}_discard'] = hit  # only in duplicates
    #         duplicates[f'{hit_id}_keep'] = existing_info  # in both dicts

    #     else:
    #         '''something differs--record both, but alter IDs. 

    #             this is included for the possibility of adverbs that are 
    #             paired with different adjectives somehow with the pattern 
    #             specified linearly, this will never happen, but keeping it 
    #             in case the pattern spec changes to allow this kind of 
    #             overlap (perhaps for conjoined predicate adjectives? see 
    #             pattern notes file) 
    #             '''

    #         id1 = hit_id+"_a"
    #         id2 = hit_id+"_b"

    #         print(
    #             f'-> Alternate hit added:\n  + {hit_id} already recorded, but '
    #             f'new info differs\n   + Annotated previous record and adding '
    #             f'second hit.')

    #         alt_hits = pd.DataFrame([existing_info, hit], index=[id1, id2])

    #         # alt_hits = alt_hits.assign(
    #         #     sent_text=alt_hits.sent_text.str.replace(' ,', ',')
    #         #     # .str[0:75]
    #         # )
    #         print('```\n#### New entries\n')
    #         print(
    #             alt_hits[['adv', 'adj', 'sent_text']].to_markdown())
    #         print('```')

    #         duplicates[f'{id1}_keep'] = existing_info
    #         duplicates[f'{id2}_keep'] = hit

    #         # keep both entries with modified ids
    #         hits_dict[id1] = existing_info
    #         hits_dict[id2] = hit

    #         # remove initial entry with original id from hits
    #         # (already replaced with id1 entry above)
    #         hits_dict.pop(hit_id)

    # elif prev_match_ids:
    #     print(
    #         '-> Exact text match to previous records. Checking token '
    #         'word strings...')

    #     match_count = 1
    #     for prev_hit in (hits_dict[i] for i in prev_match_ids):
    #         print(f'   [comparing to previous match {match_count}]')

    #         if prev_hit.adv == hit.adv and prev_hit.adv_index == hit.adv_index:
    #             print('   + adverb label and index match...')

    #             if prev_hit.adj == hit.adj:
    #                 print(
    #                     f'       and adjective label also matches.\n'
    #                     f'  + Hit {hit_id} discarded.')

    #                 duplicates[f'{hit_id}_discard'] = hit

    #             else:
    #                 print(
    #                     f'       but different adjective label.\n'
    #                     f'  + Hit {hit_id} recorded as is.')

    #                 hits_dict[hit_id] = hit
            
    #         else: 
    #             print(f'   Same sentence, but different adverb tokens.\n'
    #                   f'  + Hit {hit_id} recorded as is.')

    #         match_count += 1

    # else:

### ^ temporary commenting out to test speed changes if filtering removed

    hits_dict[hit_id] = hit

    return hits_dict, duplicates


def createOutput(hits, args, write_duplicates=False):

    txt = args.minimal
    patPath = args.pattern
    patcat = patPath.parent.stem


    # if counts:
        # # I think this chunk is broken...
        # rows = []
        # try:
        #     os.mkdir(Path.cwd() / 'colloc_freq')
        # except OSError:
        #     pass
        # outputDir = Path.cwd() / 'colloc_freq'
        # __, patkey = args.pattern.name.rsplit('_', 1)
        # outputFilename = (f'{args.outputPrefix}_counts.txt' if txt
        #                 else f'{args.outputPrefix}_counts.csv')
        # fields = ([args.node1, args.node2, f'{patkey}_counts',
        #         f'{patkey}_ratio'] if args.extraInfo
        #         else [args.node1, args.node2, f'{patkey}_counts'])
        # for colloc in counts.keys():
        #     word1 = colloc[0]
        #     word2 = colloc[1]
        #     collcount = counts[colloc]
        #     collratio = round(collcount/len(counts), 4)
        #     row = ([word1, word2, collcount, collratio]
        #         if args.extraInfo
        #         else [word1, word2, collcount])
        #     rows.append(row)
        # write_file(outputDir, outputFilename, fields, rows, txt)
    # if hits:

    outputDir = patPath.cwd() / 'hits' / patcat

    if not outputDir.exists():
        outputDir.mkdir()

    suffix = '.txt' if txt else '.csv'

    fname = (f'{args.outputPrefix}_duplicates{suffix}'
             if write_duplicates
             else f'{args.outputPrefix}_hits{suffix}')

    hits_df = pd.DataFrame.from_dict(
        {k: v._asdict() for k, v in hits.items()}, orient='index')


    if write_duplicates:
        hits_df = hits_df.assign(label=hits_df.index)
        hits_df = hits_df.assign(status=hits_df.label.str.rsplit('_', 1).str.get(1))
        hits_df = hits_df.assign(status=hits_df.status.astype('category'))

    hits_df = hits_df.set_index('hit_id')

    hits_df = (
        hits_df
        .assign(category=patcat)
        .convert_dtypes()
        .assign(adv_index=hits_df.adv_index.astype('uint8'))
        .assign(colloc=(hits_df.adv + '_' + hits_df.adj))
    )

    catcols = ['category', 'colloc', 'adv', 'adj', 'json_source']
    hits_df.loc[:, catcols] = hits_df[catcols].astype('category')

    cols = hits_df.columns.tolist()
    hits_df = hits_df[cols[-2:] + cols[:-2]]

    # write rows to file
    outpath = outputDir / fname
    hits_df.to_csv(outpath)

    view_sample_size = min(5, len(hits_df))
    label = 'Duplicates' if write_duplicates else 'Data'
    
    try: 
        print_table = hits_df[['colloc', 'sent_text']].sample(
            view_sample_size).to_markdown()
    except ImportError:
        pass
    else:
        print(f'```\n#### {label} Sample\n')
        print(print_table)
        
    print('```')
    # write_file(outputDir, fname, fields, rows, txt)


# def write_file(outputDir, outputFilename, fields, rows, txt):
#
#     with open(outputDir / outputFilename, 'w') as out:
#
#         if txt:
#
#             writer = csv.writer(out, delimiter='\t')
#
#         else:
#
#             writer = csv.writer(out)
#             writer.writerow(fields)
#
#         print(f'-> {len(rows)} rows to be recorded in {outputFilename}')
#
#         for row in rows:
#
#             try:
#
#                 writer.writerow(row)
#
#             except UnicodeEncodeError:
#
#                 print(
#                     f"Row for {row[0].encode(encoding='UTF-8')} {row[1].encode(
#                 encoding='UTF-8')} could not be written due to encoding error.
#                 Excluded from frequency table.")


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'\nTime elapsed: {round(absFinish - absStart, 3)} seconds\n'
          '====================================\n')
