import json
import pyconll
import argparse
import os
import sys
import time
from collections import namedtuple

#TODO: Need to add code to process argument input, either as looping over
# a whole directory, or taking in a list of filenames.
#TODO: Finish writing altered json files to file system

def __main__():

    args = parseArgs()

    base = args.baseDirectory

    if args.prefix:

        if not (f'{args.prefix}.json' in os.listdir(directory)
                and f'{args.prefix}.conllu' in os.listdir(directory)):

            sys.exit('Error: Specified prefix does not have both a .json and '
                     '.conllu file in this directory.')

        prefixes = [args.prefix]

    else:
        prefixes = getValidPrefixes(directory)

    sInfo = namedtuple('sInfo', 'id text tokenList')

    for pref in prefixes:

        if args.rewrite != 'yes':

            rewrite = checkForPreviousOutput(pref, directory, args.rewriteFiles)

            if not rewrite:

                print(f'Files with prefix {pref} have prior processing. File '
                      f'{directory}{pref}.json (from prior run) '
                      f'was not replaced.')
                continue

        startTime = time.perf_counter()
        print(f'Processing {pref}...')

        # create generator object from conllu file
        sourceGenerator = pyconll.load.iter_from_file(
            f'{directory}{pref}.conllu')

        # load json object
        # note that ordering of sentence ids in json file are reverse of conllu
        with open(f'{directory}{pref}.raw.json', 'r') as j:

            hits = json.load(j)

        hitIds = [h['sent_id'] for h in hits]

        #initialize json entry count
        i = 0

        #initialize conllu entry count
        c = 0

        # for each sentence
        for info in sourceGenerator:

            # if sentence matched search pattern, add info from conllu to json
            if info.id in hitIds:

                # list and for loop required to ensure all hit info will be
                # filled in the case of a single sentence having more than 1 search hit
                hitIndexList = [x for x, y in enumerate(hitIds) if y == info.id]

                for hitIndex in hitIndexList:

                    hit = hits[hitIndex]

                    hit['text'] = info.text
                    nodes = hit['matching']['nodes']
                    fillers = {}

                    for k, v in nodes.items():
                        token = info._tokens[int(v) - 1]

                        fillers[k] = (
                            token.lemma if args.tokenFillerType == 'lemma'
                            else token.form)

                    hit['matching']['fillers'] = fillers

                    i += 1

            c += 1

        finishTime = time.perf_counter()

        print(f'\t{i} hit results filled from {c} total original '
              f'sentences in {round(finishTime - startTime, 2)} seconds')


        with open(f'{directory}{pref}.json', 'w') as o:
            print('\tWriting output file...')
            json.dump(hits, o, indent=2)


def parseArgs():
    parser = argparse.ArgumentParser(
            description='script to loop over all files in a given directory '
                        'or a specified pair of files within the directory, '
                        'and output a new json file with info filled in from '
                        'the corresponding .conllu file')

    parser.add_argument('directory',
                        help='directory with files to be processed')

    parser.add_argument('-p', '--prefix',
                        help='single file prefix to process. If not specified, '
                             'script will lopp over entire directory')

    parser.add_argument('-s', '--skipFiles',
                        choices=['yes', 'no', 'check'],
                        default='no',
                        help='Indicate whether to skip file pairs which already have a '
                             'corresponding filled (already processed) json '
                             'file. Options are:\n                                                                                                                                                                                                                                                                                                                                                                                                                                                  \'yes\':\tskip all with previous '
                             'output/rewrite none\n\'no\':\tskip none/rewrite '
                             'all\n\'check\':\tcheck for each case, which requires '
                             'user input.\nThe default is to rewrite all '
                             'previously created output files (i.e. \'yes\').')

    parser.add_argument('-t', '--tokenFillerType',
                        choices=['lemma', 'form'],
                        default='lemma',
                        help='set type for fillers. options are lemma or form. '
                             'Lemma will be used if argument is not specified.')

    return parser.parse_args()


def getValidPrefixes(directory):

    allFiles = os.listdir(directory)
    jsonFiles = [j for j in allFiles if j.endswith('.raw.json')]
    conlluFiles = [c for c in allFiles if c.endswith('conllu')]
    jsonPrefixes = [j.replace('raw.json', '') for j in jsonFiles]
    conlluPrefixes = [c.replace('.conllu', '') for c in conlluFiles]

    matchingPrefixes = set(jsonPrefixes).intersection(conlluPrefixes)

    return matchingPrefixes


def checkForPreviousOutput(prefix, outputDir, rewrite):

    if f'{prefix}.json' in os.listdir(outputDir):

        if rewrite == 'no':

            return False

        while rewrite == 'check':

            skipResponse = input(f'Processed json for prefix {prefix} already exists in '
                          f'directory {outputDir}. Do you want to rewrite this '
                          f'file pair? y/n ')

            if skipResponse.lower() == 'y':

                return True

            elif skipResponse.lower() == 'n':

                return False

    return False


if __name__ == '__main__':

    __main__()










