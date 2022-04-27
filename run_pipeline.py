# coding=utf-8
"""
    simple "glue" script to initiate multiple pipes in one go.
            If no arguments are given, every corpus dir and pattern subdir
            in the current working directory will be run.

    usage: run_pipeline.py [-h] [-c CORPORA_DIR] [-p PATTERN_DIR] [-R]
    Returns:
        panas.DataFrame formatted into a csv file for every combination of
        corpus directory and pattern file
"""

import argparse
import os
import time
from sys import argv
from pathlib import Path

# TODO : ? turn scripts into utilities and import
# from script.grewSearchDir import grew_search
# from script.FillJson import fill_json
# from script.

THIS_DIR = Path(argv[0]).parent
DATA_DIR = Path.home().joinpath('data')
CODE_DIR = THIS_DIR.joinpath('source/gather')


def _main():

    args = _parse_input_args()

    # check requirements
    if args.env_check:
        os.system(f'bash {THIS_DIR.joinpath("condacheck.sh")}')
    patdirs = ((p.resolve() for p in args.patterndirs) if args.patterndirs
               else list(CODE_DIR.parent.glob('Pat/*')))

    corpora = ((c for c in args.corpora) if args.corpora
               else (DATA_DIR.glob('devel/*.conll')))

    for patdir in patdirs:
        # skip any directories without at least one .pat file
        if not list(patdir.glob('*.pat')):
            continue

        for corpus in corpora:

            print(
                f'>> searching `{corpus}` for '
                f'patterns specified in `{patdir}`...')

            # run grew search
            for pat in patdir.iterdir():
                corpus_name = corpus.stem.split('.')[0]
                output_label = '.'.join([corpus_name, pat.stem])
                output_dir = DATA_DIR.joinpath(
                    f'sanpi/1_json_grew-matches/{patdir.stem}/{output_label}')
                if not output_dir.is_dir():
                    output_dir.mkdir(parents=True)

                _run_grew(pat, corpus, output_dir, args.replace_raw_data)

                # add language info to raw jsons from conllus
                # args: fill_match_info.py [-h] CONLLU_DIR RAW_DIR
                #                   ([-o OUTPUT_DIR] [-w {yes,no,check}] [-t {lemma,form}])
                #       (OUTPUT_DIR defaults to same dir as .raw.json files=RAW_DIR)
                fill_info_cmd = (f'python {CODE_DIR}/fill_match_info.py '
                                 f'{corpus}/ {output_dir}/')
                print('\n' + fill_info_cmd)
                os.system(fill_info_cmd)

                # run tabulate
                # usage: tabulate_hits.py [-h] PAT_JSON_DIR OUTPUTPREFIX [-v]
                tabulate_cmd = (f'python {CODE_DIR}/tabulate_hits.py '
                                f'{output_dir} {corpus_name}_{pat.stem}')

                print('\n'+tabulate_cmd)
                os.system(tabulate_cmd)


def _run_grew(pat, corpus_dir, match_dir, replace):

    if not replace:
        # if all grew output files already exist in data_dir
        prev_grew_run = (set(d.stem.split('.')[0]
                             for d in match_dir.glob('*raw*'))
                         == set(c.stem for c in corpus_dir.iterdir()))

        if prev_grew_run:
            print(f'\n{match_dir.relative_to(DATA_DIR)} '
                  'is already fully populated from previous run. Skipping.')
            return

    grew_cmd = f'python {CODE_DIR}/grew_search.py {corpus_dir}/ {pat} {match_dir}'
    print('\n'+grew_cmd)
    os.system(grew_cmd)


def _parse_input_args():

    parser = argparse.ArgumentParser(
        description=(
            'simple "glue" script to initiate multiple pipes in one go. '
            'If no arguments are given, every corpus dir and pattern subdir '
            'in the current working directory will be run.'))

    parser.add_argument('-c', '--corpus', action='append', dest='corpora', type=Path,
                        help=('specify any corpus directory to be searched for pattern(s). '
                              'Can include as many as desired, but each one needs a flag. '
                              'If none specified, all `.conll` directories will be searched.')
                        )

    parser.add_argument('-p', '--patterns', action='append', dest='patterndirs', type=Path,
                        help=('specify pattern directory containing patterns to search for. '
                              'Can include as many as desired, but each one needs a flag. '
                              'If none specified, all patterns (`.pat` files) '
                              'will be sought.')
                        )

    parser.add_argument('-R', '--replace_raw_data', action='store_true',
                        help=('option to replace existing raw grew json output '
                              '(`...raw.json` files) from a previous run. If not included, '
                              'previous data will not be overwritten and grew search step '
                              'will only be performed for data directories that are '
                              'incompletely populated. '
                              'Raw data processing scripts will still be run regardless '
                              '(on existing `.raw.json` files).'))

    parser.add_argument('-E', '--env_check', action='store_true',
                        help=('option to confirm environment satisfies requirements '
                              'before running programs.'))

    return parser.parse_args()


if __name__ == '__main__':
    t0 = time.perf_counter()
    _main()
    t1 = time.perf_counter()
    print(f'total time: {round((t1-t0)/60, 2)} minutes')
