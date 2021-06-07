# coding=utf-8

'''
script to read pat_notes.md and pull out all literal blocks specifying a pattern then write each pattern to a .pat file and create a reference file connecting the heading label for a given pattern and its filename. 

to be run from dir containing both Pat/ and script/
'''

import os
import re
from pprint import pprint
from collections import namedtuple
from pathlib import Path

pat_tup = namedtuple('pat_info', ['word', 'type', 'pat'])

with open(f'{Path.cwd()}/Pat/pat_notes.md', 'r') as N:
    notes = N.read().strip()
    heading = re.compile(r'### Context (`[\w ]*`) ([ \w`]*)')
    # info = heading.findall(notes)
    heading_iter = heading.finditer(notes)

    headings = [(f'{h.groups()[0]}_{h.groups()[1]}'
                 ).replace(' ', '-').replace('`', '')
                for h in heading_iter]
    # pprint(headings)

    pat = re.compile(r'```\s+(pattern \{[^`]*\s+\})\s+```')
    pattern_iter = pat.finditer(notes)
    patterns = [(p.groups()[0],) for p in pattern_iter]
    # pprint(patterns)

pattern_info = zip(headings, patterns)

for p in pattern_info:
    fname = f'{p[0]}.pat'

    try:
        os.mkdir(Path.cwd() / 'Pat' / 'generated')
    except OSError:
        pass
    outputDir = Path.cwd() / 'Pat' / 'generated'

    with open(outputDir/fname, 'w') as out:

        out.writelines(p[1])
