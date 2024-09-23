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
import sys
from pathlib import Path

from source.gather.grew_search import grew_search  # pylint: disable=import-error
from source.gather.fill_match_info import fill_json  # pylint: disable=import-error
from source.gather.tabulate_hits import tabulate_hits  # pylint: disable=import-error

THIS_DIR = Path(sys.argv[0]).parent
DATA_DIR = Path('/share/compling/data')
CODE_DIR = THIS_DIR.joinpath('source/gather')


def _main():

    args = _parse_input_args()

    # check requirements
    if args.env_check:
        os.system(f'bash {THIS_DIR.joinpath("setup/condacheck.sh")}')
    patdirs = ((p.resolve() for p in args.patterndirs) if args.patterndirs
               else list(CODE_DIR.parent.glob('Pat/*')))

    corpora = tuple(
        iter(args.corpora)
        if args.corpora
        else (DATA_DIR.glob('devel/*.conll'))
    )
    if not corpora:
        sys.exit('No valid corpora directories indicated. Terminating.')
    tab_only = args.tabulate_only
    rewrite_files = args.rerun_grew_search
    for patdir in patdirs:
        # skip any directories without at least one .pat file
        if not bool(list(patdir.glob('*.pat'))):
            continue

        for corpus in corpora:
            corpus = corpus.resolve()

            verb = 'process' if tab_only else 'search'
            print(
                f'>> {verb}ing `{corpus}` data for '
                f'patterns specified in `{patdir}/`...')

            for pat_path in patdir.glob('*.pat'):
                print(
                    f'. . . . . . . . . . . . . . . . . . . . .\n↯ Processing {pat_path.name} matches...')
                # > can use "corpus.stem" for corpus subset name
                # >     because pathlib treats ".conll" of dir name as suffix
                grew_json_dir = (args.grew_output_dir
                                 .joinpath(pat_path.parent.name, f'{corpus.stem}.{pat_path.stem}')
                                 .resolve())

                if not grew_json_dir.is_dir():
                    if tab_only:
                        print('ERROR: "tabulate_only" option specified, but no hit files',
                              'exist for given pattern and corpus. Run full pipeline.')
                    else:
                        grew_json_dir.mkdir(parents=True)

                if not tab_only:
                    # * run grew search
                    _run_grew(pat_path, corpus, grew_json_dir, rewrite_files)

                    # * add word/token info to raw jsons from conllus
                    fill_json(conllu_dir=corpus,
                              raw_dir=grew_json_dir,
                              rewrite=rewrite_files)

                # * run tabulate
                tabulate_hits(match_dir=grew_json_dir,
                              #   pat_path=pat_path,
                              #   output_prefix=output_prefix
                              redo=rewrite_files
                              )
                print(f'✓✓✓ finished {pat_path.name} search')


def _run_grew(pat: Path,
              corpus_dir: Path,
              match_dir: Path,
              replace: bool):

    if replace:
        # > skips files with exising output by default
        grew_search(corpus_dir=corpus_dir,
                    pat_file=pat,
                    match_dir=match_dir,
                    skip_files=False)

    else:
        # > check if all grew output files already exist in data_dir
        prev_grew_run = {
            d.stem.split('.')[0] for d in match_dir.glob('*raw*')
        } == {c.stem for c in corpus_dir.iterdir()}

        if prev_grew_run:
            print(f'\n{Path(*match_dir.parts[-4:])} '
                  'is already fully populated from previous run. Skipping.')

        else:
            grew_search(corpus_dir=corpus_dir,
                        pat_file=pat,
                        match_dir=match_dir)


def _parse_input_args():
    print('parsing argument inputs...')
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

    parser.add_argument('-g', '--grew_output_dir', type=Path,
                        default=DATA_DIR.joinpath('1_json_grew-matches'),
                        help=('specify location to direct output to other than default supplied by `grew_search.py`: '
                              '/share/compling/data/sanpi/1_json_grew-matches'))

    parser.add_argument('-R', '--rerun_grew_search', action='store_true',
                        help=('option to replace existing raw grew json output '
                              '(`...raw.json` files) from a previous run. If not included, '
                              'previous data will not be overwritten and grew search step '
                              'will only be performed for data directories that are '
                              'incompletely populated. '
                              'Raw data processing scripts will still be run regardless '
                              '(on existing `.raw.json` files).'))
    parser.add_argument(
        '-T', '--tabulate_only', action='store_true', default=False,
        help=('option to jump directly to tabulate step.'
              'Use if previous processing interrupted during tabulation.'),
    )

    parser.add_argument('-E', '--env_check', action='store_true',
                        help=('option to confirm environment satisfies requirements '
                              'before running programs.'))

    return parser.parse_args()


def dur_round(time_dur: float):
    """take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits

    Args:
        dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur /= 60
        unit = "m"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "h"

    return (
        f"{round(time_dur, 2):.2f}{unit}"
        if time_dur < 10
        else f"{round(time_dur, 1):.1f}{unit}"
    )


if __name__ == '__main__':
    proc_t0 = time.perf_counter()
    _main()
    proc_t1 = time.perf_counter()
    print(f'Total time to run pipeline: {dur_round(proc_t1 - proc_t0)}')
