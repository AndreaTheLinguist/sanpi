from json import loads as load_json_str
from shutil import rmtree
from os import mkdir
from collections import namedtuple as ntup
from pathlib import Path
from pprint import pprint

import pandas as pd
from pypandoc import convert_file

Patdirpath = Path.cwd() / "Pat"
blocktup = ntup('block', ['type', 'content', 'ix', 'level', 'keep'])

# TODO add loop to scan `Pat/` for all `specs_`... files
with open(Patdirpath / "specs_mit-neg.md", "r") as pat_spec_file:

    json_str = convert_file(pat_spec_file.name, 'json', format='md')
    pat_spec_dict = load_json_str(json_str)

blocks = [blocktup(b['t'], b['c'], '', '', '')
          for b in pat_spec_dict['blocks']
          if b['t'].lower() in ('header', 'codeblock')]

headix = 0
level = 0
for i, b in enumerate(blocks):

    if b.type.lower() == 'bulletlist':
        continue

    keep = ''

    if b.type.lower() == 'header':
        level = b.content[0]

        keep_list = []
        str_list = []
        for e in b.content[2]:

            if e['t'] == 'Code':
                keep_list.append(e['c'][1])

            elif e['t'] == 'Str':
                str_list.append(e['c'])

        keep_list.append('-'.join(str_list))
        keep = '_'.join(keep_list).replace(' ', '-')

        if i != 0:
            headix += 1

    elif b.type.lower() == 'codeblock':
        keep = b.content[1]

    blocks[i] = b._replace(ix=headix, level=level, keep=keep)

df = pd.DataFrame(blocks)
df = df.loc[df.type != 'BulletList']
df.loc[:, 'type'] = df.type.astype('category')
df.loc[:, 'keep'] = df.keep.astype('string')
df.loc[:, ['ix', 'level']] = df.loc[:, ['ix', 'level']].apply(
    pd.to_numeric, downcast='unsigned')

dirstem = df.loc[df.level == 1, 'keep'].iat[0].lower()

outputDir = Patdirpath / dirstem

try:
    rmtree(outputDir)

except OSError:
    pass

mkdir(outputDir)

specs = df.loc[df.level == 2, ['type', 'ix', 'keep']]

for i in specs.ix.unique():

    spec_df = specs.loc[specs.ix == i, ['type', 'keep']].set_index('type')
    fname = spec_df.at['Header', 'keep']
    fpath = outputDir / f'{fname}.pat'

    with open(fpath, 'w') as pat_file:

        pat_file.write(spec_df.at['CodeBlock', 'keep'])
