import sys
import json
import os
from pathlib import Path

json_dir = Path.cwd()/sys.argv[1]

if not json_dir.is_dir():

    sys.exit('Error: Specified json directory does not '
             'exist.')

errors = 0

for f in os.scandir(json_dir):

    if f.name.endswith('json') and not f.name.endswith('raw.json'):

        with open(f, 'r') as j:

            for hit in json.load(j):

                nodes = hit['matching']['fillers']

                pair = (nodes['ADV'] + '\t' +
                        nodes['ADJ'])

                try:

                    print(pair)

                except UnicodeError:

                    error += 1
                    print(f"Encoding error. Pair {pair} skipped.")

            # print(f'{errors} errors in {f.name}')
