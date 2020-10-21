import json
import argparse
import os
import pprint
import csv
import sys
import time
from collections import namedtuple, Counter
from pathlib import Path

'''
Notes:
-take in 2 json data with hit info for 2 searches on the same corpus data.
-output table (csv?) with frequencies for each unique adv-adj pair in each outputDir
-do not need to keep files with same ID linked if counting by directory 
(and by specific file would not be informative anyway)
but that's gonna be a whole lot of json files to go through
-will need to combine tables from different corpus chunks later--csv better?
'''


def __main__():

    args = parseArgs()

    json_dir = args.pattern
    if not json_dir.is_dir():

        sys.exit('Error: Specified json directory does not '
                 'exist.')

    counter = fillCounter(json_dir, args)

    print('\nFinished processing all json files.\nWriting output file...')

    createCsv(counter, args)


def parseArgs():
    parser = argparse.ArgumentParser(
        description='script to count hits for particular words filling particular nodes for a pattern run on corpus data.')

    parser.add_argument('-p', '--pattern', type=Path, required=True,
                        help='path to directory containing filled json files for pattern.')

    # parser.add_argument('-p2', '--pattern2', type=Path, required=True,
    #                     help='path to directory containing filled json files for second pattern')

    # parser.add_argument('-d', '--baseDir', type=Path,
    #                     default=Path.cwd(),
    #                     help='directory with subdirectories containing files '
    #                          'to be processed. Default directory is current '
    #                          'directory.')

    parser.add_argument('-o', '--outputPrefix', type=str, required=True,
                        help='prefix for output \'..._counts.csv\' file to be written to the \'freq\' subdirectory (created if necessary) found in the directory the script is run from. This should be a string which contains info about the patterns, corpus data set, and nodes counted; e.g. \'Nyt1_p1-n1_adv-adj\' which would result in the output file \'freq/Nyt1_p1-n1_adv-adj_counts.csv\'.')

    # parser.add_argument('-p1', '--pattern1', required=True,
    #                     help='pattern for first directory to count, e.g. p1')

    # parser.add_argument('-p2', '--pattern2', required=True,
    #                     help='pattern for second directory to count, e.g. p2')

    parser.add_argument('-n1', '--node1', default='ADV',
                        help='search label for first node, default is \'ADV\'. Both patterns being compared must have a single node with this label.')

    parser.add_argument('-n2', '--node2', default='ADJ',
                        help='search label for second node, default is \'ADJ\'. Both patterns being compared must have a single node with this label.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    parser.add_argument('-e', '--extraInfo', action='store_true',
                        help='Option to add ratio and totals to csv output file')

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
                print(f'Warning: Node labels have not been filled from conllu '
                      f'file for {jsonFile}. Proceeding to next file without '
                      f'updating counts...')
                return countDict

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


def createCsv(counts, args):

    try:
        os.mkdir(Path.cwd() / 'freq')
    except OSError:
        pass
    outputDir = Path.cwd() / 'freq'

    __, patkey = args.pattern.name.rsplit('.', 1)

    outputFilename = f'{args.outputPrefix}_counts.csv'

    fields = ([args.node1, args.node2, f'{patkey}_counts',
               f'{patkey}_ratio'] if args.extraInfo
              else [args.node1, args.node2, f'{patkey}_counts'])

    rows = []
    total_hits = len(counts)

    for colloc in counts.keys():

        collcount = counts[colloc]
        collratio = collcount/total_hits

        row = ([colloc[0], colloc[1], collcount, collratio]
               if args.extraInfo
               else [colloc[0], colloc[1], collcount])

        rows.append(row)

    with open(outputDir / outputFilename, 'w') as out:

        csvWriter = csv.writer(out)

        csvWriter.writerow(fields)

        csvWriter.writerows(rows)


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round(absFinish - absStart, 2)} seconds')
