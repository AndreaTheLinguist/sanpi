#!/usr/bin/env python3

import argparse
import os
import sys
import time
from io import open
from pprint import pprint

try:
    import conllu
except:
    print('conllu module required. installing...')
    os.system("pip3 install conllu")


def __main__():

    args = parseArgs()
    conll_dir = args.orig_dir
    output_dir = conll_dir.rstrip(
        '/') + '_clean/' if not args.output_dir else args.output_dir
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    print(
        f'Files without duplicates will be saved to a new directory, {output_dir}, with the original file name.')

    # necessary to track repeats across files
    all_sentences_dict = {}

    prev1repeated = False
    prev2repeated = False
    prev3repeated = False
    prev_doc_id = None

    discarded = []

    for conll_file in os.scandir(conll_dir):

        # ignore anything without .conllu extension
        if not conll_file.name.endswith('.conllu'):
            continue

        # save generator object for iterating over conllu file
        data = open(conll_file, 'r')
        parser = conllu.parse_incr(data)

        # initialize dict to keep same-doc sentences together
        # and not add sentences prematurely
        doc_dict = {}
        discard = False

        print(f'...processing {conll_file.name}')

        # write conll files: keep same file divisions, only with repeats removed.
        # put in new dir: "[orig dir]_clean/" (set above before looping thru files)
        new_conll_file = output_dir + '/' + conll_file.name
        with open(new_conll_file, 'w') as output:

            for sent_obj in parser:

                doc_id, __ = sent_obj.metadata['sent_id'].rsplit('_', 1)

                # if not first sentence in file
                if prev_doc_id:

                    # if same doc as prev sentence and doc marked for discard
                    if doc_id == prev_doc_id and discard:

                        continue

                    # if starting new doc
                    elif doc_id != prev_doc_id:

                        # add previous doc's senteces to sentence dict
                        all_sentences_dict.update(doc_dict)

                        # write novel doc to clean file
                        for s in doc_dict.values():

                            try:
                                output.write(s.serialize())
                            except UnicodeDecodeError:
                                stext = s.metadata['text']
                                print(
                                    f'Warning: Unicode decoding error. Skipping {stext}')

                        if args.verbose:
                            print(
                                f'...Doc {prev_doc_id} successfully written to file.')

                        # new doc --> clean slate
                        discard = False
                        prev1repeated = False
                        prev2repeated = False
                        prev3repeated = False

                        # reset doc dictionary
                        doc_dict = {}

                sent_text = sent_obj.metadata['text'].encode()

                # if novel, do nothing
                if sent_text not in all_sentences_dict.keys():

                    pass

                # if previous 3 already repeated (now 4), discard doc
                elif prev3repeated:
                    discard = True
                    discarded.append(doc_id)
                    if args.verbose:
                        print(f'!!! Duplicate! discarding doc {doc_id}.')

                # if 3 now repeated
                elif prev2repeated:
                    prev3repeated = True

                # if 2 now repeated
                elif prev1repeated:
                    prev2repeated = True

                # if this is the first repeat
                else:
                    prev1repeated = True

                # if discard threshold has not been reached
                # (putting this last is to catch valid one or two-off sentence repeats)
                if not discard:

                    doc_dict[sent_text] = sent_obj

                # set current id to previous before restarting loop
                prev_doc_id = doc_id

        print('finished.')
        if args.verbose:
            print(
                f'New file does not contain following documents from {conll_file.name}:')
            pprint(discarded)

    discard_log = output_dir + '/' + 'discard_log.txt'
    print(f'Saving discard log to {discard_log}.')
    with open(output_dir + '/' + 'discard_log.txt', 'w') as log:

        log.writelines(discarded)


def parseArgs():

    parser = argparse.ArgumentParser(
        description='Script to remove duplicated documents from corpus conllu files. Run on entire directory, and outputs new (smaller) files to different directory with same names as in original directory. Requires conllu package.'
    )

    parser.add_argument("orig_dir", type=str,
                        help='path to directory containing sentences .conllu files. e.g. Nyt1.conll')

    parser.add_argument('-o', '--output_dir', type=str,
                        help='optional argument to specify output directory. Default will be original directory name + _clean')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    return parser.parse_args()


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round((absFinish - absStart)/60, 2)} minutes')
