import json
import argparse
import os
import sys
from pathlib import Path


def __main__():

    args = parseargs()
    json_dir = args.json_dir

    check_dir(json_dir)

    # get list base file names (strings; use set to avoid duplicates/ignore 'raw')
    file_ids = set([f.split('.')[0]
                    for f in os.listdir(json_dir) if f.split('.')[-1] == 'json' and f.split('.')[0] != 'duplicates'])

    # new org will be dict of json obj/lists
    # where key = "[adv]_[adj]" and value = json obj/list (of numbered dicts?)
    reorg_data = {}

    for file_id in file_ids:

        # load data (json object) from given file
        # json obj (i.e. list)
        data = load_data(json_dir, file_id)

        if data:

            reorg_data = reorg(file_id, data, reorg_data, json_dir)

    

    output_dir_path = json_dir / 'by_adverb'
    os.system(
        f'if [ ! -d {output_dir_path} ]; then mkdir {output_dir_path}; fi')

    print(f'data successfully reorganized by modification pairs.\nWriting files to adverb subdirectories in {output_dir_path}...')

    x = 0
    total_files = len(reorg_data)
    print(f'{total_files} total files to be written...')
    for type_label, tokens_list in reorg_data.items():

        # type_label goes into new json filename
        # tokens_dict becomes content of json file

        # sort by adverb (first half of label)
        subdir_path = output_dir_path / type_label.split('_')[0]
        os.system(f'if [ ! -d {subdir_path} ]; then mkdir {subdir_path}; fi')

        output_file_name = type_label + '.json'
        with open(subdir_path / output_file_name, 'w') as output:

            json.dump(tokens_list, output, indent=2)

        x += 1
        if x in [round(total_files*y) for y in [0.25, 0.5, 0.75, .9]]:

            print(
                f'{x} ({round(x / total_files * 100)}%) completed...')

    print('finished.')


def reorg(file_id, data, reorg_data, json_dir):

    duplicates = []
    print(f'reorganizing hits in {file_id}.json')
    for i, hit in enumerate(data):

        sentence_id = hit['sent_id']
        doc_id, index_in_doc = sentence_id.rsplit('_', 1)
        sentence_text = hit['text']
        adv = hit['matching']['fillers']['ADV'].split(
            '\\')[0].strip('\'\"').replace('.', '')
        adj = hit['matching']['fillers']['ADJ'].split(
            '\\')[0].strip('\'\"').replace('.', '')
        key_name = f'{adv}_{adj}'
        token_index = (int(hit['matching']['nodes']['ADV']),
                       int(hit['matching']['nodes']['ADJ']))

        new_dict = {'orig_file': {'file_id': file_id, 'file_index': i - 1},
                    'sent_id': sentence_id, 'doc_id': doc_id,
                    'sent_index': index_in_doc, 'sent_text': sentence_text,
                    'adv': adv, 'adj': adj, 'token_index': token_index, 'key_name': key_name}

        if key_name not in reorg_data.keys():

            reorg_data[key_name] = []

        elif sentence_id in [t['sent_id'] for t in reorg_data[key_name]]:

            if token_index in [t['token_index'] for t in reorg_data[key_name]]:

                print(
                    f'Duplicate: {key_name} at {i-1} in sentence {sentence_id}')

                duplicates.append({'mod_pair': key_name,
                                   'orig_file': file_id,
                                   'orig_index': i-1,
                                   'sentence_id': sentence_id,
                                   'sentence': sentence_text})
                continue

        reorg_data[key_name].append(new_dict)

    print(f'\n{len(duplicates)} duplicated hits found in {file_id}')
    if len(duplicates) > 0:
        with open(json_dir / 'duplicates.json', 'a') as d:
            json.dump(duplicates, d, indent=2)
        print(
            f'Duplicates were excluded from reorganized data. Additional info saved to {json_dir}/duplicates.json\n')

    return reorg_data


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
