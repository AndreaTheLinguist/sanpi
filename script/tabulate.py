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

        print('    Finished counting collocations in all json files.')

    if args.table:

        hit_data = getHitData(json_dir, args)

        print('    Finished collecting sentence data in all json files.')

    colloc_str = 'collocation counts' if colloc_counter else ''
    hit_str = 'hits table' if hit_data else ''
    conj = ' and ' if colloc_counter and hit_data else ''
    print(f'Writing {colloc_str}{conj}{hit_str} to file.')

    createOutput(colloc_counter, hit_data, args)


def parseArgs():
    parser = argparse.ArgumentParser(
        description='script to count hits for particular words filling particular nodes for a pattern run on corpus data. If no output option is specified, -t/--table will be used.')

    parser.add_argument('-p', '--pattern', type=Path, required=True,
                        help='path to directory containing filled json files for pattern.')

    parser.add_argument('-o', '--outputPrefix', type=str, required=True,
                        help='prefix for output \'..._counts.csv\' file to be written to the \'freq\' subdirectory (created if necessary) found in the directory the script is run from. This should be a string which contains info about the patterns, corpus data set, and nodes counted; e.g. \'Nyt1_p1-n1_adv-adj\' which would result in the output file \'freq/Nyt1_p1-n1_adv-adj_counts.csv\'.')

    parser.add_argument('-n1', '--node1', default='ADV',
                        help='search label for first node, default is \'ADV\'. Both patterns being compared must have a single node with this label.')

    parser.add_argument('-n2', '--node2', default='ADJ',
                        help='search label for second node, default is \'ADJ\'. Both patterns being compared must have a single node with this label.')

    parser.add_argument('-m', '--minimal', action='store_true',
                        help='Option produce minimal output. If used, output will not have a header row and will be a tab delimited .txt file instead of the default comma delimted .csv.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    parser.add_argument('-t', '--table', action='store_true',
                        help='Option to create a table output with following fields: Adv, Adj, SentenceID, WordIndex, SentenceText')

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
        'hit_tuple', ['adv', 'adj', 'sent_id', 'adv_index', 'sent_text'])
    hits_dict = {}

    for jsonFile in os.scandir(json_dir):

        if (jsonFile.name.endswith('raw.json')
                or not jsonFile.name.endswith('json')):
            continue

        fileCount += 1

        if args.verbose:
            print(f'\nProcessing {jsonFile.name}...')

        with open(jsonFile, 'r') as j:

            hits = json.load(j)

            for hit in hits:
                try:

                    fillers = hit['matching']['fillers']

                except KeyError:
                    sys.exit(
                        f'Node labels have not been filled from conllu file for {jsonFile}. Quitting script without generating output.')

                node1_word = fillers[args.node1]
                node2_word = fillers[args.node2]

                sent_id = hit['sent_id']
                sent_text = hit['text']
                node1_index = hit['matching']['nodes'][args.node1]

                hit_info = hit_tuple(node1_word, node2_word,
                                     sent_id, node1_index, sent_text)

                hit_id = ':'.join((sent_id, node1_index))

                if hit_id in hits_dict.keys():
                    print(
                        f'Warning: hit {hit_id} already in hit_info dictionary. Overwriting previous info (for \"{hits_dict[hit_id].adv} {hits_dict[hit_id].adj}\"  in \"{hits_dict[hit_id].text}\") with info for \"{hit_info.adv} {hit_info.adj} in \"{hit_info.sent_text}\".')

                hits_dict[hit_id] = hit_info

    return hits_dict


def createOutput(counts, hits, args):

    txt = args.minimal

    if counts:

        rows = []

        try:
            os.mkdir(Path.cwd() / 'colloc_freq')
        except OSError:
            pass
        outputDir = Path.cwd() / 'colloc_freq'

        __, patkey = args.pattern.name.rsplit('.', 1)

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

        outputFilename = (f'{args.outputPrefix}_hits.txt' if txt
                          else f'{args.outputPrefix}_hits.csv')
        # set fields
        hits_keys = list(hits.keys())
        fields = hits[hits_keys[0]]._fields

        # fill rows
        rows = list(hits.values())

        # write rows to csv
        write_file(outputDir, outputFilename, fields, rows, txt)


def write_file(outputDir, outputFilename, fields, rows, txt):

    with open(outputDir / outputFilename, 'w') as out:

        if txt:

            writer = csv.writer(out, delimiter='\t')

        else:

            writer = csv.writer(out)
            writer.writerow(fields)

        for row in rows:

            try:

                writer.writerow(row)

            except UnicodeEncodeError:

                print(
                    f"Row for {word1.encode(encoding='UTF-8')} {word2.encode(encoding='UTF-8')} could not be written due to encoding error. Excluded from frequency table.")

        # writer.writerows(rows)


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round(absFinish - absStart, 2)} seconds')
