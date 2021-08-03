import argparse
import json
import sys
import time
from pathlib import Path

import pyconll


def __main__():

    args = parseArgs()
    jsonDirPath = args.raw_dir
    conllDirPath = args.conllu_dir

    print(
        f'```\n### Running `FillJson.py` script on json files in '
        f'`{jsonDirPath.name}` from conll files in `{conllDirPath.name}`...\n'
        f'```')

    if not (jsonDirPath.is_dir() and conllDirPath.is_dir()):

        sys.exit(
            'Error: specified conll directory and json directory do not exist'
            ' in the base directory.')

    if len(list(jsonDirPath.iterdir())) > 0:
        prefixes = getValidPrefixes(jsonDirPath, conllDirPath)

        if not prefixes:
            sys.exit('Error: No corresponding .json and .conllu files found.')

    else:
        sys.exit('Error: specified data directory is empty')

    outputDir = args.output_dir if args.output_dir else jsonDirPath

    if not outputDir.exists():
        outputDir.mkdir()

    rewrite = args.rewriteFiles

    for pref in prefixes:

        startTime = time.perf_counter()

        jsonfile = jsonDirPath / f'{pref}.raw.json'
        conllfile = conllDirPath / f'{pref}.conllu'

        if rewrite != 'yes' and skipFiles(pref, jsonDirPath, rewrite):

            print(
                f'-> Files with prefix {pref} have prior processing:\n'
                f'   + File {jsonfile.relavtive_to(jsonfile.parent)} '
                f'(from prior run) was not replaced.')

            continue

        print(f'-> Processing {pref}...')

        # create generator object from conllu file

        sourceGenerator = pyconll.load.iter_from_file(
            conllDirPath / f'{pref}.conllu')

        # load json object
        # note that ordering of sentence ids in json file are reverse of conllu
        with open(jsonDirPath / f'{pref}.raw.json', 'r') as j:

            try:

                hits = json.load(j)

            except json.decoder.JSONDecodeError:

                print('   -> Skipping. (file is empty)')
                continue

            else:

                if len(hits) < 1:

                    print(f'-> Skipping. (file is empty)')
                    continue

        hit_ids = [h['sent_id'] for h in hits]

        ##TODO add info on what the "trigger" word is, and words directly preceding adv?
        # initialize new hit dictionary entries
        for hit_dict in hits:
            hit_dict['prev_sent'] = None
            hit_dict['next_sent'] = None
            hit_dict['text'] = None
            hit_dict['matching']['fillers'] = None
            hit_dict['doc'] = None

        # initialize json entry count
        i = 0

        # initialize conllu entry count
        c = 0

        # initialize tracker variables
        curr_id = ''
        sent_text = ''
        hitIndexList = [None]
        same_doc = False

        # for each sentence
        for info in sourceGenerator:
            # update variables
            prev_id = curr_id
            curr_id = info.id

            prev_sent = sent_text
            sent_text = info.text

            try:
                # see if current dictionary has 'newdoc id' defined
                doc_id = info._meta['newdoc id']
            except KeyError:
                # if no 'newdoc id' key, then same as previous
                same_doc = True
            else:
                # if 'newdoc key' key exists, not same doc as previous
                same_doc = False

            # if this sentence follows a match sentence, add this sentence to
            # the relevant hit dictionary entry
            if same_doc and prev_id in hit_ids:
                for hitIndex in hitIndexList:
                    hits[hitIndex]['next_sent'] = sent_text

            # if sentence matched search pattern, add info from conllu to json
            if curr_id in hit_ids:

                # list and for loop required to ensure all hit info will be
                # filled in the case of a single sentence having more than 1
                # search hit
                hitIndexList = [ix for ix, hit_id in enumerate(hit_ids)
                                if hit_id == curr_id]

                for hitIndex in hitIndexList:

                    hit = hits[hitIndex]

                    hit['text'] = sent_text
                    hit['doc'] = doc_id

                    if same_doc:
                        hit['prev_sent'] = prev_sent

                    nodes = hit['matching']['nodes']
                    fillers = {}

                    for k, v in nodes.items():
                        token = info._tokens[info._ids_to_indexes[v]]

                        fillers[k] = (token.lemma
                                      if args.tokenFillerType == 'lemma'
                                      else token.form)

                    hit['matching']['fillers'] = fillers

                    i += 1

            c += 1

        finishTime = time.perf_counter()

        print(f'   => {i} hit results filled from {c} total original '
              f'sentences in {round(finishTime - startTime, 2)} seconds')

        with open(outputDir / f'{pref}.json', 'w') as o:
            print('-> Writing output file...')
            json.dump(hits, o, indent=2)

    print('Finished processing all corresponding json and conll files.')


def parseArgs():
    parser = argparse.ArgumentParser(
        description=(
            'This is a script to loop over all \'.raw.json\' (grew-match '
            'result) files in a given directory and output new json files with '
            'info filled in from the corresponding .conllu (corpus info) files'))

    parser.add_argument('-c', '--conllu_dir', required=True, type=Path,
                        help='path to directory containing sentences .conllu '
                             'files. e.g. Nyt1.conll')

    parser.add_argument('-r', '--raw_dir', type=Path, required=True,
                        help='path to directory containing unprocessed/raw '
                             '.json search result files to be processed of '
                             'form \'<sentenceSetID>.raw.json\'. e.g. Nyt1.if')

    parser.add_argument('-o', '--output_dir', type=Path, default=None,
                        help='path to directory to write filled output json '
                             'files to. If not specified, the raw_dir path will'
                             ' be used (output/filled json files lose the '
                             '\'.raw\' in the filename.)')

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

    rawJsonSet = set(j.with_suffix('').stem for j in jsonDir.iterdir()
                     if '.raw' in j.suffixes)
    conlluSet = set(c.stem for c in conllDir.iterdir()
                    if c.suffix == '.conllu')

    return rawJsonSet.intersection(conlluSet)


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
    print(
        f'Time elapsed: {round((absFinish - absStart)/60, 2)} minutes')
