# coding=utf-8

import argparse
import csv
import json
import os
import pprint
import sys
import time
from collections import Counter, namedtuple
from pathlib import Path


def __main__():

    print("Tabulating hits via tabulate.py...")
    args = parseArgs()

    # do table by default if no output type option specified.
    if not (args.table or args.count):
        args.table = True
        print(
            'Warning: No output type specified. Output will be table of hits, not counts.')

    json_dir = args.pattern
    print(
        f'Collecting specified data for json files in {json_dir.name}...')
    if not json_dir.is_dir():

        sys.exit('Error: Specified json directory does not '
                 'exist.')

    colloc_counter = None
    hit_data = None

    if args.count:

        colloc_counter = fillCounter(json_dir, args)

        print('^_^ Finished counting collocations in all json files.')

    if args.table:

        hit_data, duplicates = getHitData(json_dir, args)

        print('^_^ Finished collecting sentence data in all json files.')

    colloc_str = 'collocation counts' if colloc_counter else ''
    hit_str = 'hits table' if hit_data else ''
    conj = ' and ' if colloc_counter and hit_data else ''
    print(f'Writing {colloc_str}{conj}{hit_str} to file.')

    createOutput(colloc_counter, hit_data, args)
    createOutput(colloc_counter, duplicates, args, write_duplicates=True)


def parseArgs():
    parser = argparse.ArgumentParser(
        description='script to count hits for particular words filling particular nodes for a pattern run on corpus data. If no output option is specified, -t/--table will be used.')

    parser.add_argument('-p', '--pattern', type=Path, required=True,
                        help='path to directory containing filled json files for pattern.')

    parser.add_argument('-o', '--outputPrefix', type=str, required=True,
                        help='prefix for output \'..._counts.tsv\' file to be written to the \'freq\' subdirectory (created if necessary) found in the directory the script is run from. This should be a string which contains info about the patterns, corpus data set, and nodes counted; e.g. \'Nyt1_p1-n1_adv-adj\' which would result in the output file \'freq/Nyt1_p1-n1_adv-adj_counts.csv\'.')

    parser.add_argument('-n1', '--node1', default='ADV',
                        help='search label for first node, default is \'ADV\'. Both patterns being compared must have a single node with this label.')

    parser.add_argument('-n2', '--node2', default='ADJ',
                        help='search label for second node, default is \'ADJ\'. Both patterns being compared must have a single node with this label.')

    parser.add_argument('-m', '--minimal', action='store_true',
                        help='Option produce minimal output. If used, output will not have a header row and will have .txt extension')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    parser.add_argument('-t', '--table', action='store_true',
                        help='Option to create a table output with following fields: hit_id, adv, adj, colloc, sent_text, sent_id, adv_index, ')

    parser.add_argument('-c', '--count', action='store_true',
                        help='Option to create an output of counts with following fields (minimally): Adv, Adj, hit_counts')

    parser.add_argument('-e', '--extraInfo', action='store_true',
                        help='Option to add ratio and totals to count output file. **This option will do nothing if --count/-c flag is not used.**')

    return parser.parse_args()


def fillCounter(json_dir, args):

    counter = Counter()

    startTime = time.perf_counter()
    fileCount = 0

    for jsonFile in os.scandir(json_dir):

        if (jsonFile.name.endswith('raw.json')
                or not jsonFile.name.endswith('json')):
            continue

        fileCount += 1

        if args.verbose:
            print(f'\nProcessing {jsonFile.name}...')

        counter = countTokenPairs(counter, jsonFile.path, args)

    if args.verbose:
        print(
            f'\nTop 10 collocations for entire {json_dir.name} directory:')
        pprint.pprint(counter.most_common(10))

    finishTime = time.perf_counter()

    print(f'\nFinished counting {json_dir.name}.')
    print(f'Collocations from {fileCount} total files counted '
          f'in {round(finishTime - startTime, 2)} seconds')

    return counter


def countTokenPairs(countDict, jsonFile, args):

    wordType1 = args.node1
    wordType2 = args.node2
    colloc = namedtuple('collocation', [wordType1, wordType2])

    with open(jsonFile, 'r') as j:

        hits = json.load(j)

        for hit in hits:
            try:

                nodes = hit['matching']['fillers']

            except KeyError:
                sys.exit(
                    f'Node labels have not been filled from conllu file for {jsonFile}. Quitting script without generating output.')

            else:

                tupleKey = colloc(nodes[wordType1], nodes[wordType2])

                if tupleKey not in countDict.keys():

                    countDict[tupleKey] = 1

                else:

                    countDict[tupleKey] += 1

                # use (named)tuple as key in dictionary.
                # e.g. [(word1=x, word2=y): count, (word1=a, word2=b): count, ...]

    if args.verbose:
        print('Top 3 (running totals):')
        pprint.pprint(countDict.most_common(3))

    return countDict


def getHitData(json_dir, args):

    # pull out sentence info and create dictionary of hit_id : namedTuple
    fileCount = 0
    hit_tuple = namedtuple(
        'hit_tuple', ['adv', 'adj', 'sent_text', 'sent_id', 'adv_index'])
    hits_dict = {}
    duplicates = {}

    for jsonFile in os.scandir(json_dir):

        if (jsonFile.name.endswith('raw.json')
                or not jsonFile.name.endswith('json')):
            continue

        with open(jsonFile, 'r') as j:
            if len(j.readlines()) == 1:
                print(f'--> {jsonFile.path} is empty. Skipping.')
                continue

        fileCount += 1

        if args.verbose:
            print(f'\nProcessing {jsonFile.name}...')

        with open(jsonFile, 'r', encoding='utf-8') as j:

            hits = json.load(j)

            for hit in hits:
                try:

                    fillers = hit['matching']['fillers']

                except KeyError:
                    sys.exit(
                        f'Node labels have not been filled from conllu file for {jsonFile}. Quitting script without generating output. Run FillJson.py and then try again.')

                node1_word = fillers[args.node1].lower()
                node2_word = fillers[args.node2].lower()

                sent_id = hit['sent_id']
                sent_text = repr(hit['text'].strip())

                # ADV index
                node1_index = hit['matching']['nodes'][args.node1]

                hit_info = hit_tuple(node1_word, node2_word, sent_text,
                                     sent_id, node1_index)

                hit_id = ':'.join((sent_id, node1_index))
                recorded_sentences = tuple(
                    v.sent_text for v in hits_dict.values())

                if hit_id in hits_dict.keys():

                    existing_info = hits_dict[hit_id]

                    # exact same--nothing added
                    if hit_info == existing_info:

                        print(
                            f'|---> Entry not added: hit {hit_id} (\"{existing_info.adv} {existing_info.adj}\") already in hit_info dictionary.')

                        duplicates[f'{hit_id}_discard'] = hit_info
                        duplicates[f'{hit_id}_keep'] = existing_info

                    # something differs--record both, but with altered IDs
                    # this is included for the possibility of adverbs that are paired with different adjectives somehow
                    # with the pattern specified linearly, this will never happen, but keeping it in case the pattern spec changes to allow this kind of overlap (perhaps for conjoined predicate adjectives? see pattern notes file)
                    else:
                        id1 = hit_id+"_a"
                        id2 = hit_id+"_b"

                        print(
                            f'|---> hit {hit_id} already in hit_info dictionary and new info differs --> Modifying previous record and adding second hit.\n=== New entries ===\n+ {id1}:\t{existing_info.adv}\t{existing_info.adj}\t{existing_info.sent_text}\n+ {id2}:\t{hit_info.adv}\t{hit_info.adj}\t{hit_info.sent_text}')

                        duplicates[f'{id1}_keep'] = existing_info
                        duplicates[f'{id2}_keep'] = hit_info

                        # keep both entries with modified ids
                        hits_dict[id1] = existing_info
                        hits_dict[id2] = hit_info

                        # remove initial entry with original id from hits (already replaced with id1 entry above)
                        hits_dict.pop(hit_id)

                elif sent_text in recorded_sentences:

                    print(
                        f'|---> hit {hit_id} skipped. No ID match, but sentence text is an exact duplicate:\n ~ \"{sent_text}\"\n  info added to duplicates log.')
                    duplicates[f'{hit_id}_discard'] = hit_info

                else:

                    hits_dict[hit_id] = hit_info

        # hits_dict = OrderedDict(sorted(hits_dict.items()))
        # duplicates = OrderedDict(sorted(duplicates.items()))

    return hits_dict, duplicates


def createOutput(counts, hits, args, write_duplicates=False):

    txt = args.minimal

    if counts:
        # I think this chunk is broken...
        rows = []

        try:
            os.mkdir(Path.cwd() / 'colloc_freq')
        except OSError:
            pass
        outputDir = Path.cwd() / 'colloc_freq'

        __, patkey = args.pattern.name.rsplit('_', 1)

        outputFilename = (f'{args.outputPrefix}_counts.txt' if txt
                          else f'{args.outputPrefix}_counts.csv')

        fields = ([args.node1, args.node2, f'{patkey}_counts',
                   f'{patkey}_ratio'] if args.extraInfo
                  else [args.node1, args.node2, f'{patkey}_counts'])

        for colloc in counts.keys():

            word1 = colloc[0]
            word2 = colloc[1]
            collcount = counts[colloc]
            collratio = round(collcount/len(counts), 4)

            row = ([word1, word2, collcount, collratio]
                   if args.extraInfo
                   else [word1, word2, collcount])

            rows.append(row)

        write_file(outputDir, outputFilename, fields, rows, txt)

    if hits:

        try:
            os.mkdir(Path.cwd() / 'hits')
        except OSError:
            pass
        outputDir = Path.cwd() / 'hits'

        ext = '.txt' if txt else '.csv'

        fname = (f'{args.outputPrefix}_duplicates{ext}'
                 if write_duplicates
                 else f'{args.outputPrefix}_hits{ext}')

        # set fields
        hits_keys = list(hits.keys())

        prefix_fields = (('hit_id', 'status', 'colloc') if write_duplicates
                         else
                         ('hit_id', 'colloc'))

        fields = prefix_fields + hits[hits_keys[0]]._fields

        # fill rows
        rows = []

        for k, v in hits.items():

            if write_duplicates:
                hit_id, status = k.rsplit('_', 1)

            else:
                hit_id = k

            colloc = f'{v.adv}_{v.adj}'

            row = ((hit_id, status, colloc) + v if write_duplicates
                   else
                   (hit_id, colloc) + v)

            rows.append(row)

        rows.sort(key=lambda r: r[0])
        # sort rows by hit id

        # write rows to tsv
        write_file(outputDir, fname, fields, rows, txt)


def write_file(outputDir, outputFilename, fields, rows, txt):

    with open(outputDir / outputFilename, 'w') as out:

        if txt:

            writer = csv.writer(out, delimiter='\t')

        else:

            writer = csv.writer(out)
            writer.writerow(fields)

        print(f'-> {len(rows)} rows to be recorded in {outputFilename}')

        for row in rows:

            try:

                writer.writerow(row)

            except UnicodeEncodeError:

                print(
                    f"Row for {row[0].encode(encoding='UTF-8')} {row[1].encode(encoding='UTF-8')} could not be written due to encoding error. Excluded from frequency table.")


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round(absFinish - absStart, 3)} seconds')
