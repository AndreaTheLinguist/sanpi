import json
import argparse
import os
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
    jsonDir1 = baseDir / f'{args.sentences}.{args.pattern1}'
    jsonDir2 = baseDir / f'{args.sentences}.{args.pattern2}'

    if not (jsonDir1.is_dir() and jsonDir2.is_dir()):

        sys.exit('Error: specified son directories do not '
                 'exist in the base directory.')

    counters = [Counter(), Counter()]
    dirs = [jsonDir1, jsonDir2]

    for i, jsonDir in enumerate(dirs):

        for jsonFile in os.scandir(path=jsonDir):

            if (jsonFile.name.endswith('raw.json')
                or not jsonFile.name.endswith('json')): continue

            startTime = time.perf_counter()
            print(f'Processing {jsonFile.name}...')

            counters[i] = countTokenPairs(counters[i], jsonFile.path, args)

            finishTime = time.perf_counter()

            # print(f'\t{i} hit results filled from {c} total original '
            #       f'sentences in {round(finishTime - startTime, 2)} seconds')

            # with open(f'{jsonDirPath}{pref}.json', 'w') as o:
            #     print('\tWriting output file...')
            #     json.dump(hits, o, indent=2)

        print(f'')
        counters[i] = sorted(counters[i].items(),
                             key=lambda x: x[1], reverse=True)

        print('\tFinished.')

    print('Finished processing all json files.')


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

    parser.add_argument('-s', '--sentences',
                        help='prefix for sentence content to be processed, '
                             'e.g. Nyt1')

    parser.add_argument('-p1', '--pattern1',
                        help='pattern for first directory to count, e.g. p1')

    parser.add_argument('-p2', '--pattern2',
                        help='pattern for second directory to count, e.g. p2')

    parser.add_argument('-n1', '--node1',
                        help='search label for first node, e.g. ADV')

    parser.add_argument('-n2', '--node2',
                        help='search label for second node, e.g. ADJ')

    return parser.parse_args()


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
                # After all counts are finalized, dict can be sorted
                # then use csv.writer (or dictWriter?)

    print(f'Top 3 in file: {countDict.most_common(3)}')

    return countDict

if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round(absFinish - absStart, 2)} seconds')