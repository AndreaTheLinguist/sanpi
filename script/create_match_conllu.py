# coding=utf-8
# create_match_conllu.py
"""defines function to create (write to file) a subset conllu file containing
all matches in given full conllu file for given pattern file.

Returns:
    None
"""
import argparse
import sys
from pathlib import Path

import grew
import pyconll


def _main():

    # setting example inputs
    conllu_path, pat_path = _parse_args()

    if not conllu_path.is_file():
        sys.exit(f'{conllu_path} does not exist.\n')

    if conllu_path.stat().st_size == 0:
        sys.exit(f'{conllu_path} is empty.\n')

    write_matches_to_conllu(conllu_path, pat_path)


def _parse_args():
    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-c', '--conllu_path',
        type=Path,
        default='/home/arh234/data/devel/quicktest.conll/nyt_eng_199912.conllu',
        help=('path to full `.conllu` corpus file to search')
    )

    parser.add_argument(
        '-p', '--pat_path',
        type=Path,
        default='/home/arh234/projects/sanpi/Pat/contig/sans-relay.pat',
        help=('path to `.pat` pattern file specifying pattern string to create seek')
    )

    args = parser.parse_args()

    return args.conllu_path, args.pat_path


def write_matches_to_conllu(conllu_path: Path, pat_path: Path):
    """
    create subset conllu file consisting of all sentences
    in a given conllu file which match a given pattern file

    Args:
        conllu_path (Path): path to `.conllu` file to be searched
        pat_path (Path): path to `.pat` file specifying pattern to be sought
    """

    # set output path to subdirectory in origin conllu dir:
    #   subset_[PATTERN_DIR]/
    out_dir_name = f'subset_{pat_path.parent.stem}'
    if out_dir_name == conllu_path.parent.name:
        sys.exit(
            'Input conllu is already a subset matching search pattern: '
            f'{pat_path.relative_to(pat_path.parent.parent)}\n')
    out_dir = conllu_path.with_name(out_dir_name)
    if not out_dir.is_dir():
        out_dir.mkdir()
    # and filename to original conllu name plus pat name
    #   [ORIGIN_CONLLU_STEM]_[PAT_STEM].conllu
    out_file = out_dir.joinpath(f'{conllu_path.stem}_{pat_path.stem}.conllu')
    if (out_file.is_file() and out_file.stat().st_size > 0
       and out_file.stat().st_mtime > pat_path.stat().st_mtime):
        sys.exit(
            f'Subset {out_file.relative_to(conllu_path.parent)} already '
            'exists and is more recent than any pattern file modifications.\n')

    print(f'\nSearching {conllu_path.name} for {pat_path.stem} pattern:\n')
    # * grew tool must be started!
    grew.init()
    # load corpus into grew interface
    print('loading corpus file...')
    corpus_ix = grew.corpus(str(conllu_path))

    # collect matches for pattern
    print('collecting matches...')
    matches_found = grew.corpus_search(
        pat_path.read_text(encoding='utf8'), corpus_ix)
    if not matches_found:
        sys.exit(f'No matches for {pat_path.name} in {conllu_path.name}.')
    # pull out sentence id for every match
    match_ids = set(m['sent_id'] for m in matches_found)

    # collect conllu sentence objects for each matching sentence
    #   and put in string output format + line break
    print('generating subset conllu...')
    match_conllus = (f'{sent.conll()}\n'
                     for sent in pyconll.iter_from_file(str(conllu_path))
                     if sent.id in match_ids)

    # create string of conllu formatted strings
    out_str = '\n'.join(match_conllus)

    # write string to new subset file
    out_file.write_text(out_str, encoding='utf8')

    print(f'Subset conllu file saved to {out_file}.\n')


if __name__ == '__main__':

    _main()
