import sys
import json
import os
import csv
import argparse
from pathlib import Path


def __main__():

    args = argparser()
    triggerName = args.trigger_name
    triggerPath = args.trigger_counts
    complementPath = args.complement_counts

    with open(triggerPath, newline='') as t, open(complementPath, newline='') as c:

        trig_reader = csv.reader(t)
        comp_reader = csv.reader(c)
        lines = []
        for row in trig_reader:

            # print trigger status TAB adv_adj TAB count
            lines.append(f'{row[2]}\twith_{triggerName}\t{row[0]}_{row[1]}')

        for row in comp_reader:

            # print complement status TAB adv_adj TAB count
            lines.append(f'{row[2]}\twithout_{triggerName}\t{row[0]}_{row[1]}')

        for line in lines:

            if line.startswith(tuple('0123456789')):

                try:

                    print(line)

                except UnicodeError:

                    print(f'Encoding error. {line.encode()} skipped')

    # json_dir = Path.cwd()/sys.argv[1]
    # context = sys.argv[2]

    # if not json_dir.is_dir():

    #     sys.exit('Error: Specified json directory does not '
    #              'exist.')

    # errors = 0

    # for f in os.scandir(json_dir):

    #     if f.name.endswith('json') and not f.name.endswith('raw.json'):

    #         with open(f, 'r') as j:

    #             for hit in json.load(j):

    #                 nodes = hit['matching']['fillers']

    #                 pair = (nodes['ADV'] + '\t' +
    #                         nodes['ADJ'])

    #                 try:

    #                     print(pair)

    #                 except UnicodeError:

    #                     error += 1
    #                     print(f"Encoding error. Pair {pair} skipped.")


def argparser():

    parser = argparse.ArgumentParser(
        description=(
            'Script to run through every hit in json files and output a format that can be run with UCS toolkit\'s ucs-make-tables, which requires a lines of the form [item1]\\t[item2]<\\t precompiled counts for type> (third element is optional and requires the flag --types). For this project, [item1]=context type (either has DE trigger, or does not) and [item2]=(adv,adj) pair. Counts for each pair in context have been tabulated in the freq/ directory, so modifier pair types and their token counts can be pulled from tables corresponding to each of the contexts. This script then creates a system output with the context key (which file it came from) and the pairs and their counts in a format that can be piped into ucs-make-tables.'))

    parser.add_argument('-t', '--trigger_counts', type=Path, required=True,
                        help='path to counts csv file for collocates with given trigger, e.g. "with-<trigger>"')

    parser.add_argument('-c', '--complement_counts', type=Path, required=True,
                        help='path to counts csv file for collocates without given trigger, e.g. "without-<trigger>"')

    parser.add_argument('-n', '--trigger_name', type=str, default='trigger',
                        help='name of trigger relevant to given csv files; e.g. not. If not supplied, filler "trigger" will be used in output.')

    return parser.parse_args()


if __name__ == '__main__':

    __main__()
