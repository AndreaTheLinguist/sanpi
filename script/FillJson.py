import json
import pyconll
import argparse
import os
import sys
import time
from pathlib import Path

# TODO: Add option to loop over entire base directory if pattern or sentences
#  are not specified.

def __main__():

    args = parseArgs()
    baseDir = args.baseDir
    jsonDirPath = baseDir / f'{args.sentences}.{args.pattern}'
    conllDirPath = baseDir / f'{args.sentences}.conll'

    if not (jsonDirPath.is_dir() and conllDirPath.is_dir()):

        sys.exit('Error: specified conll directory and json directory do not '
                 'exist in the base directory.')

    if len(os.listdir(jsonDirPath)) > 0:
        prefixes = getValidPrefixes(jsonDirPath, conllDirPath)

    else:
        sys.exit('Error: specified data directories are empty')

    rewrite = args.rewriteFiles

    for pref in prefixes:

        if rewrite != 'yes':

            if skipFiles(pref, jsonDirPath, rewrite):

                print(f'Files with prefix {pref} have prior processing. File '
                      f'{jsonDirPath}{pref}.json (from prior run) '
                      f'was not replaced.')

                continue

        startTime = time.perf_counter()
        print(f'Processing {pref}...')

        # create generator object from conllu file
        sourceGenerator = pyconll.load.iter_from_file(
                conllDirPath / f'{pref}.conllu')

        # load json object
        # note that ordering of sentence ids in json file are reverse of conllu
        with open(jsonDirPath / f'{pref}.raw.json', 'r') as j:

            hits = json.load(j)

        hitIds = [h['sent_id'] for h in hits]

        # initialize json entry count
        i = 0

        # initialize conllu entry count
        c = 0

        # for each sentence
        for info in sourceGenerator:

            # if sentence matched search pattern, add info from conllu to json
            if info.id in hitIds:

                # list and for loop required to ensure all hit info will be
                # filled in the case of a single sentence having more than 1
                # search hit
                hitIndexList = [x for x, y in enumerate(hitIds) if y == info.id]

                for hitIndex in hitIndexList:

                    hit = hits[hitIndex]

                    hit['text'] = info.text
                    nodes = hit['matching']['nodes']
                    fillers = {}

                    for k, v in nodes.items():
                        token = info._tokens[int(v) - 1]

                        fillers[k] = (token.lemma
                                      if args.tokenFillerType == 'lemma'
                                else token.form)

                    hit['matching']['fillers'] = fillers

                    i += 1

            c += 1

        finishTime = time.perf_counter()

        print(f'\t{i} hit results filled from {c} total original '
              f'sentences in {round(finishTime - startTime, 2)} seconds')

        with open(f'{jsonDirPath}{pref}.json', 'w') as o:
            print('\tWriting output file...')
            json.dump(hits, o, indent=2)

        print('\tFinished.')

    print('Finished processing all corresponding json and conll files.')


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

    parser.add_argument('-p', '--pattern',
                        help='single file prefix to process. If not specified, '
                             'script will lopp all patterns for given conllu '
                             'Files')

    parser.add_argument('-r', '--rewriteFiles',
                        choices=['yes', 'no', 'check'],
                        default='yes',
                        help='Indicate whether to skip file pairs which '
                             'already have a corresponding filled (already '
                             'processed) json file. Options are: '
                             '\'no\' = rewrite none; '
                             '\'yes\' = rewrite all; '
                             '\'check\' = check for each case, which requires '
                             'user input. The default is to rewrite all '
                             'previously created output files (i.e. \'yes\').')

    parser.add_argument('-t', '--tokenFillerType',
                        choices=['lemma', 'form'],
                        default='lemma',
                        help='set type for fillers. options are lemma or form. '
                             'Lemma will be used if argument is not specified.')

    return parser.parse_args()


def getValidPrefixes(jsonDir, conllDir):
    '''function to return list of file prefixes which have both conll and raw
    json files '''
    allJsonFiles = os.listdir(jsonDir)
    rawJsonFiles = [j for j in allJsonFiles if j.endswith('.raw.json')]
    conllFiles = os.listdir(conllDir)
    jsonPrefixes = [j.replace('.raw.json', '') for j in rawJsonFiles]
    conllPrefixes = [c.replace('.conllu', '') for c in conllFiles]

    matchingPrefixes = set(jsonPrefixes).intersection(conllPrefixes)

    return matchingPrefixes


def skipFiles(prefix, directory, rewrite):

    outputFile = directory / f'{prefix}.json'

    if outputFile.exists():

        if rewrite == 'no':
            return True

        while rewrite == 'check':

            skipResponse = input(f'Filled json for prefix {prefix} already '
                                 f'exists in directory {directory}. Do you '
                                 f'want to skip this file pair? y/n ')

            if skipResponse.lower() == 'y':

                return True

            if skipResponse.lower() == 'n':

                return False

    return False


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round(absFinish - absStart, 2)} seconds')
