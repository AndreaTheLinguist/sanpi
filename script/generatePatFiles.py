# coding=utf-8

'''
script to read pat_notes.md and pull out all literal blocks specifying a pattern then write each pattern to a .pat file and create a reference file connecting the heading label for a given pattern and its filename. 

to be run from dir containing both Pat/ and script/
'''

import os
import re
import shutil
from pprint import pprint
from collections import namedtuple
from pathlib import Path

pat_tup = namedtuple('pat_info', ['text', 'start', 'end'])

with open(f'{Path.cwd()}/Pat/pat_notes.md', 'r') as N:
    notes = N.read().strip()
    heading = re.compile(r'### Context (`[\w ]*`) ([ \w`]*)')
    # pprint(heading.findall(notes))
    heading_iter = heading.finditer(notes)

    pat = re.compile(r'```\s+(pattern[^`]+)```')
    # pprint(pat.findall(notes))
    pattern_iter = pat.finditer(notes)

headings = []
for h in heading_iter:
    heading = (f'{h.groups()[0]}_{h.groups()[1]}'
               ).replace(' ', '-').replace('`', '')

    headings.append(pat_tup(heading, h.start(), h.end()))

# pprint(headings)
patterns = []
for p in pattern_iter:

    pattern = p.groups()[0]

    patterns.append(pat_tup(pattern, p.start(), p.end()))

headings = sorted(headings, key=lambda x: x.start)
patterns = sorted(patterns, key=lambda y: y.start)

# specs = []
# for i, h in enumerate(headings):

#     for p in patterns:

#         if h.end < p.start:

#             try:
#                 next_h = headings[i+1]

#             except IndexError:

#                 specs.append((h.text, p.text))
#                 break

#             else:

#                 if p.end < headings[i+1].start:

#                     specs.append((h.text, p.text))
#                     break

#     # patterns = [(p.groups()[0],) for p in pattern_iter]
#     # pprint(patterns)

patinfo_gen = zip((h.text for h in headings), (p.text for p in patterns))

try:
    shutil.rmtree(Path.cwd() / 'Pat' / 'generated')

except OSError:
    pass

os.mkdir(Path.cwd() / 'Pat' / 'generated')

outputDir = Path.cwd() / 'Pat' / 'generated'

for p in patinfo_gen:
    fname = f'{p[0]}.pat'

    with open(outputDir/fname, 'w') as out:

        out.writelines(p[1])
