import os
import time
import argparse
from collections import namedtuple
from json import loads as parse_json
from pathlib import Path
from pprint import pprint
from shutil import rmtree

import pandas as pd
from pypandoc import convert_file


def __main__():

    top_dir_path = parseargs()

    # top_dir_path = Path.cwd() / "Pat"

    specs_file_gen = (f for f in top_dir_path.iterdir()
                      if f.name.startswith('specs_'))

    for specs_file in specs_file_gen:

        block_list = parse_md(specs_file)

        # check if file met minimum blocks threshold:
        #   need at least 2 headers and 1 codeblock for 1 .pat file
        if len(block_list) < 3:
            print(f'\nWARNING! Pat/{specs_file.name} is incomplete. Skipping.')
            continue

        info_df = parse_pat_specs(block_list)

        dir_stem = info_df.loc[info_df.level == 1, 'keep'].iat[0].lower()
        output_dir = top_dir_path / dir_stem
        prep_output_dir(output_dir)

        specs = info_df.loc[info_df.level == 2, ['type', 'ix', 'keep']]
        print(f'\n==> Writing files to {output_dir} for the following '
              f'contexts:\n')
        pprint(specs.loc[specs.type == 'Header', :].reset_index().keep)

        write_files(specs, output_dir)


def parseargs():

    parser = argparse.ArgumentParser(
        description=('script to read all "specs..." files in a given '
                     'directory and convert them to individual ".pat" '
                     'files with labels corresponding to the file '
                     'names and headers.'))

    parser.add_argument('pat_dir_path', type=Path,
                        help=('path to directory where pattern specification '
                              '.md files are located. Output files will be '
                              'saved to the same location.'))
    args = parser.parse_args()

    return args.pat_dir_path


def parse_md(specs_path: str):

    with open(specs_path, "r") as specs_file:

        json_str = convert_file(specs_file.name, 'json', format='md')

        pat_spec_dict = parse_json(json_str)

    blocktup = namedtuple('block', ['type', 'content', 'ix', 'level', 'keep'])

    blocks = [blocktup(b['t'], b['c'], '', '', '')
              for b in pat_spec_dict['blocks']
              if b['t'].lower() in ('header', 'codeblock')]

    return blocks


def parse_pat_specs(blocks: list):

    headix = 0
    level = 0
    for i, b in enumerate(blocks):
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

        blocks[i] = b._replace(ix=headix,
                               level=level,
                               keep=keep)

    df = pd.DataFrame(blocks)
    df.loc[:, 'type'] = df.type.astype('category')
    df.loc[:, 'keep'] = df.keep.astype('string')
    df.loc[:, ['ix', 'level']] = (
        df.loc[:, ['ix', 'level']].apply(pd.to_numeric, downcast='unsigned'))

    return df


def prep_output_dir(outputdir):

    try:
        rmtree(outputdir)

    except OSError:
        pass

    os.mkdir(outputdir)


def write_files(specs: pd.DataFrame, output_dir):

    for i in specs.ix.unique():

        spec_orig = specs.loc[specs.ix == i, ['type', 'keep']]
        spec = spec_orig.set_index('type')
        label = spec.at['Header', 'keep']

        if spec_orig.value_counts('type').CodeBlock > 1:
            pprint(
                f'Warning: Too many pattern strings found for {label}. Pattern '
                f'file will not be written.\n(Hint: make sure each pattern in '
                f'specs markdown file has its own level 2/## header)')

        fpath = output_dir / f'{label}.pat'

        with open(fpath, 'w') as pat_file:
            pat_file.write(spec.loc['CodeBlock', 'keep'])


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round((absFinish - absStart), 2)} s')
