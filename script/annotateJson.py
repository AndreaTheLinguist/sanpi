import json
import argparse
import os
import sys
from pathlib import Path


def __main__():

    args = parseargs()
    json_dir = args.json_dir

    check_dir(json_dir)

    # get list base file names (strings) to be annotated
    files = prep_file_list(args)

    for i, file in enumerate(files):

        # load data (json object) from given file
        data = load_data(json_dir, file)

        if data:

            annotate(data)

        file_id = file.split('.')[0]
        output_file_name = file_id + '.anno.json'

        with open(json_dir / output_file_name, 'r') as output:

            json.dump(data, output, indent=2)

        print(
            f'Annotations for {file_id} saved to {json_dir.name}/{output_file_name}')
        print(f'File {i+1} of {len(files)} completed.')

        while i + 1 != len(files):

            pause = input('Take a break? y/n\n')

            if pause.lower() == 'y':

                sys.exit(
                    'Quitting program without finishing: Unannotated files remain in directory.')

            elif pause.lower() == 'n':

                print('Continuing to next file...')
                break

    print('Finished.')


def annotate(collocations):

    # colloc_gen = (entry for entry in data)

    # for c in colloc_gen:
    for i, c in enumerate(collocations):

        sentence = c['text']
        adv = c['matching']['fillers']['ADV']
        adj = c['matching']['fillers']['ADJ']
        print(f'{i} of {len(collocations)}')

        while True:

            decision = input(f'\n\"{adv} {adj}\" : \"{sentence}\":\nlitotes? y/n\n')

            if decision.lower() == 'y':

                litotes = True

            elif decision.lower() == 'n':

                litotes = False
                break

        comment = input('Enter any comment code(s). If other, specify:\n'
                        'r = neg-raising verb\n'
                        't = unexpected trigger\n'
                        's = not in scope\n'
                        'o [...] = other\n')

        c['litotes'] = litotes
        c['comment'] = comment

    
        

def load_data(json_dir, file):

    with open(json_dir / file, 'r') as f:

        try:

            return json.load(f)

        except json.decoder.JSONDecodeError:

            print('json file is empty. Skipping.')
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


def prep_file_list(args):

    json_dir = args.json_dir
    base_files = [f for f in os.listdir(json_dir)
                  if not f.endswith(('.raw.json', '.anno.json'))]
    base_cnt = len(base_files)

    if args.redo_annos:

        while True:

            response = input(
                f'Redo annotations option selected: all {base_cnt} files in directory queued for processing, regardless of previous annotations. Any pre-existing annotated json files will be overwritten. Continue? y/n\n')

            if response.lower() == 'y':

                break

            elif response.lower() == 'n':

                sys.exit('Quitting script.')

            else:

                print('Invalid response.')

        files = base_files

    else:

        annot_files = [f for f in os.listdir(json_dir)
                       if f.endswith('.anno.json')]
        annot_cnt = len(annot_files)
        unann_cnt = base_cnt - annot_cnt

        print(f'{base_cnt} total base json files in directory.')

        if unann_cnt == 0:

            sys.exit(
                'All files have been annotated. Quitting script with no changes to directory.')

        print(
            f'{annot_cnt} already annotated. {unann_cnt} remaining unannotated files.')

        annot_names = [f.split('.')[0] for f in annot_files]
        base_names = [f.split('.')[0] for f in base_files]

        files = [n + '.json' for n in base_names if n not in annot_names]

    return files


if __name__ == '__main__':

    __main__()
