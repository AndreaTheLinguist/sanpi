import json
import pyconll
import argparse
import os
import sys
import time
from pathlib import Path


def __main__():

    args = parseArgs()
    jsonDirPath = args.raw_dir
    conllDirPath = args.conllu_dir

    print(
        f'\nRunning FillJson.py script on json files in {jsonDirPath.name} from conll files in {conllDirPath.name}...\n')

    if not (jsonDirPath.is_dir() and conllDirPath.is_dir()):

        sys.exit('Error: specified conll directory and json directory do not '
                 'exist in the base directory.')

    if len(os.listdir(jsonDirPath)) > 0:
        prefixes = getValidPrefixes(jsonDirPath, conllDirPath)

    else:
        sys.exit('Error: specified data directories are empty')

    outputDirPath = args.output_dir if args.output_dir else jsonDirPath

    testDirStr = f'if [ ! -d {outputDirPath} ]; then mkdir {outputDirPath}; fi'
    os.system(testDirStr)

    rewrite = args.rewriteFiles

    for pref in prefixes:

        if rewrite != 'yes' and skipFiles(pref, jsonDirPath, rewrite):

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

            try:

                hits = json.load(j)

            except json.decoder.JSONDecodeError:

                print('__x__ json file is empty. Skipping.')
                continue

            else:

                if len(j.readlines()) == 1:

                    print(f'\tNo hits in {pref} file. Skipping.')
                    continue

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
                hitIndexList = [x for x, y in enumerate(
                    hitIds) if y == info.id]

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

        with open(outputDirPath / f'{pref}.json', 'w') as o:
            print('\tWriting output file...')
            json.dump(hits, o, indent=2)

        print('\tFinished.')

    print('Finished processing all corresponding json and conll files.')


def parseArgs():
    parser = argparse.ArgumentParser(
        description=(
            'This is a script to loop over all \'.raw.json\' (grew-match result) files in a given directory and output new json files with info filled in from the corresponding .conllu (corpus info) files'))

    parser.add_argument('-c', '--conllu_dir', required=True, type=Path,
                        help='path to directory containing sentences .conllu files. e.g. Nyt1.conll')

    parser.add_argument('-r', '--raw_dir', type=Path, required=True,
                        help='path to directory containing unprocessed/raw .json search result files to be processed of form \'<sentenceSetID>.raw.json\'. e.g. Nyt1.if')

    parser.add_argument('-o', '--output_dir', type=Path, default=None,
                        help='path to directory to write filled output json files to. If not specified, the raw_dir path will be used (output/filled json files lose the \'.raw\' in the filename.)')

    parser.add_argument('-w', '--rewriteFiles',
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
                             'Lemma is used by default.')

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
    print(f'Time elapsed: {round((absFinish - absStart)/60, 2)} minutes\n')
