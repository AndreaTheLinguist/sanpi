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
-output table (csv?) with frequencies for each unique adv-adj pair in each dir
-do not need to keep files with same ID linked if counting by directory 
(and by specific file would not be informative anyway)
but that's gonna be a whole lot of json files to go through
-will need to combine tables from different corpus chunks later--csv better?
'''

def __main__():

    args = parseArgs()
    baseDir = args.baseDir
    try:
        os.mkdir(baseDir / 'freq')
    except OSError:
        pass
    outputDir = baseDir / 'freq'
    jsonDir1 = baseDir / f'{args.sentences}.{args.pattern1}'
    jsonDir2 = baseDir / f'{args.sentences}.{args.pattern2}'

    dirs = [jsonDir1, jsonDir2]

    checkDirs(dirs)

    counters = fillCounters(dirs, args)

    print('\nFinished processing all json files.\nWriting output file...')

    createCsv(counters, outputDir, args)


def parseArgs():
    parser = argparse.ArgumentParser(
            description='script to loop over all files in a given directory '
                        'or a specified pair of files within the directory, '
                        'and output a new json file with info filled in from '
                        'the corresponding .conllu file')

    parser.add_argument('-d', '--baseDir', type=Path,
                        default=Path(__file__).absolute().parent,
                        help='directory with subdirectories containing files '
                             'to be processed. Default directory is same as '
                             'this script.')

    parser.add_argument('-s', '--sentences', required=True,
                        help='prefix for sentence content to be processed, '
                             'e.g. Nyt1')

    parser.add_argument('-p1', '--pattern1', required=True,
                        help='pattern for first directory to count, e.g. p1')

    parser.add_argument('-p2', '--pattern2', required=True,
                        help='pattern for second directory to count, e.g. p2')

    parser.add_argument('-n1', '--node1', default='ADV',
                        help='search label for first node, default is \'ADV\'')

    parser.add_argument('-n2', '--node2', default='ADJ',
                        help='search label for second node, default is \'ADJ\'')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    parser.add_argument('-e', '--extraInfo', action='store_true',
                        help='Option to add ratio and totals to csv output file')

    return parser.parse_args()


def checkDirs(dirList):

    dir1 = dirList[0]
    dir2 = dirList[1]

    if not (dir1.is_dir() and dir2.is_dir()):

        sys.exit('Error: Specified json directories do not '
                 'exist in the base directory.')

    sizeDir1 = len([name for name in os.listdir(dir1)
                    if not name.endswith('raw.json')])

    sizeDir2 = len([name for name in os.listdir(dir2)
                    if not name.endswith('raw.json')])

    # if sizeDir1 != sizeDir2:
    #
    #     sys.exit('Error: Specified data directories do not have the same '
    #              'number of processed json files. Check directories and try '
    #              'again.')

    return


def fillCounters(dirs, args):

    counters = [Counter(), Counter()]

    for i, jsonDir in enumerate(dirs):

        startTime = time.perf_counter()
        fileCount = 0

        for jsonFile in os.scandir(path=jsonDir):

            if (jsonFile.name.endswith('raw.json')
                or not jsonFile.name.endswith('json')): continue

            fileCount += 1

            if args.verbose:
                print(f'\nProcessing {jsonFile.name}...')

            counters[i] = countTokenPairs(counters[i], jsonFile.path, args)

        if args.verbose:
            print(f'\nTop 10 collocations for entire {jsonDir.name} directory:')
            pprint.pprint(counters[i].most_common(10))

        finishTime = time.perf_counter()

        print(f'\nFinished counting {jsonDir.name}.')
        print(f'Collocations from {fileCount} total files counted '
              f'in {round(finishTime - startTime, 2)} seconds')

    return counters


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

                ## use (named)tuple as key in dictionary.
                # e.g. [(word1=x, word2=y): count, (word1=a, word2=b): count, ...]

    print('\tfinished.')
    if args.verbose:
        print('Top 3 (running totals):')
        pprint.pprint(countDict.most_common(3))

    return countDict


def createCsv(counters, dir, args):

    p1 = args.pattern1
    p2 = args.pattern2

    outputFilename = f'{args.sentences}_{p1}-{p2}_counts.csv'

    fields = ([args.node1, args.node2, f'{p1}_counts', f'{p2}_counts',
               f'ratio_{p1}', f'ratio_{p2}', 'total'] if args.extraInfo
              else [args.node1, args.node2, f'{p1}_counts', f'{p2}_counts'])

    p1counts = counters[0]
    p2counts = counters[1]
    totalCounts = p1counts + p2counts

    collocations = set(p1counts.keys()).union(p2counts.keys())

    rows = []

    for c in collocations:

        try:
            p1count = p1counts[c]

        except KeyError:
            p1count = 0

        try:
            p2count = p2counts[c]

        except KeyError:
            p2count = 0

        total = totalCounts[c]
        p1ratio = p1count/total
        p2ratio = p2count/total

        row = ([c[0], c[1], p1count, p2count, p1ratio, p2ratio, total]
               if args.extraInfo
               else [c[0], c[1], p1count, p2count])

        rows.append(row)

    with open(dir / outputFilename, 'w') as out:

        csvWriter = csv.writer(out)

        csvWriter.writerow(fields)

        csvWriter.writerows(rows)


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round(absFinish - absStart, 2)} seconds')