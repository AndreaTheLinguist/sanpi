import json
import argparse
import os
import sys
from pathlib import Path


def __main__():

    args = parseargs()
    json_dir = args.json_dir

    check_dir(json_dir)

    # get list base file names (strings; use set to avoid duplicates)
    file_ids = set([f.split('.')[0] for f in os.listdir(json_dir)])

    # new org will be dict of json obj/lists
    # where key = "[adv]_[adj]" and value = json obj/list (of numbered dicts?)
    reorg_data = {}

    for i, file_id in enumerate(file_ids):

        # load data (json object) from given file
        # json obj (i.e. list)
        data = load_data(json_dir, file_id)

        if data:

            reorg_data = reorg(file_id, data, reorg_data)

        # name files like in ucs tables? adv_adj ?
    #     output_file_name = file_id + '.json'

    #     with open(json_dir / 'by_type' / output_file_name, 'r') as output:

    #         json.dump(data, output, indent=2)

    #     print(
    #         f'Annotations for {file_id} saved to {json_dir.name}/{output_file_name}')
    #     print(f'File {i+1} of {len(files)} completed.')

    #     while i + 1 != len(files):

    #         pause = input('Take a break? y/n\n')

    #         if pause.lower() == 'y':

    #             sys.exit(
    #                 'Quitting program without finishing: Unannotated files remain in directory.')

    #         elif pause.lower() == 'n':

    #             print('Continuing to next file...')
    #             break

    # print('Finished.')


def reorg(file_id, data, reorg_data):

    for i, hit in enumerate(data):

        sentence_id = hit['sent_id']
        index_in_doc = sentence_id.split('_')[-1]
        sentence_text = hit['text']
        adv = hit['matching']['fillers']['ADV']
        adj = hit['matching']['fillers']['ADJ']
        key_name = f'{adv}_{adj}'

        hit_dict = {'file_id': file_id, 'sent_id': sentence_id,
                    'sent_index': index_in_doc,
                    'sent_text': sentence_text, 'adv': adv, 'adj': adj, 'key_name': key_name}

        if key_name not in reorg_data.keys():
            reorg_data[key_name] = []

        reorg_data[key_name].append(hit_dict)

        # print(f'{i} of {len(collocations)}')

        # while True:

        #     decision = input(
        #         f'\n\"{adv} {adj}\" : \"{sentence}\":\nlitotes? y/n\n')

        #     if decision.lower() == 'y':

        #         litotes = True

        #     elif decision.lower() == 'n':

        #         litotes = False
        #         break

        # comment = input('Enter any comment code(s). If other, specify:\n'
        #                 'r = neg-raising verb\n'
        #                 't = unexpected trigger\n'
        #                 's = not in scope\n'
        #                 'o [...] = other\n')

        # c['litotes'] = litotes
        # c['comment'] = comment


def load_data(json_dir, file_id):

    file = file_id + '.json'

    with open(json_dir / file, 'r') as f:

        try:

            return json.load(f)

        except json.decoder.JSONDecodeError:

            print(f'{file} is empty. Skipping.')
            return None


def parseargs():

    parser = argparse.ArgumentParser(
        description='Script to loop through collocation tokens in json files and annotate/and and fill litotes field. Takes in directory and saves new files periodically as <origname>_annot.json'
    )

    parser.add_argument('-d', '--json_dir',
                        required=True, type=Path,
                        help='path to directory containing filled json files (i.e. with tokens and context text added)'
                        )

    parser.add_argument('-r', '--redo_annos', action='store_true',
                        help='option to ignore previous annotation files and redo annotations for all files in directory')

    return parser.parse_args()


def check_dir(dir):

    if not dir.is_dir():
        sys.exit('Error: directory not found. Exiting script.')

    if len(os.listdir(dir)) == 0:
        sys.exit('Error: directory is empty. Exiting script.')


if __name__ == '__main__':

    __main__()
