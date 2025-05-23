# coding=utf-8
# make_subset_conllus.py
"""defines function to create (write to file) a subset conllu file containing
all matches in given full conllu file for given pattern file.

Returns:
    None
"""
import argparse
import sys
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from types import GeneratorType

import grew
import pyconll


def _main():

    # setting example inputs
    conllu_path, pat_path = _parse_args()

    if not (conllu_path.is_file() or conllu_path.suffix != '.conllu'):
        sys.exit(f'{conllu_path} is not a .conllu file.\n')

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
        default='/share/compling/data/puddin/Pcc00.conll/pcc_eng_00-001.conllu',
        help=('path to full `.conllu` corpus file to search')
    )

    parser.add_argument(
        '-p', '--pat_path',
        type=Path,
        default='share/compling/projects/sanpi/Pat/advadj/all-RB-JJs.pat',
        help=('path to `.pat` pattern file specifying pattern string to create seek. '
              '*note* If run from top level of project sanpi/, this must be specified.')
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
        print('Input conllu is already a subset matching search pattern: '
              f'{pat_path.relative_to(pat_path.parent.parent)}\n')
        # successful termination
        sys.exit(0)
    out_dir = conllu_path.with_name(out_dir_name)
    try:
        out_dir.mkdir()
    except FileExistsError:
        pass
    # and filename to original conllu name plus pat name
    #   [ORIGIN_CONLLU_STEM]_[PAT_STEM].conllu
    out_file = out_dir.joinpath(f'{conllu_path.stem}_{pat_path.stem}.conllu')
    if (out_file.is_file() and out_file.stat().st_size > 0
        and out_file.stat().st_mtime > pat_path.stat().st_mtime
            and out_file.stat().st_mtime > conllu_path.stat().st_mtime):

        #! print(message_string) and exit() because exit(message_string) indicates error:
        #   exit([anything but 0 or None]) gets exit code of 1, which indicates error.
        #   exit()(exit(0), exit(None)) indicates successful termination
        print(f'Subset {out_file.relative_to(conllu_path.parent)} already '
              'exists and is more recent than any pattern file modifications.\n')
        sys.exit(0)

    print(f'\nSearching {conllu_path.name} for {pat_path.stem} pattern:\n')
    # * grew tool must be started!
    # with socket() as s:
    #     s.bind(('', 0))
    #     portnum=s.getsockname()[1]
    # print('trying port', portnum)
    # not_started = True
    # portnum=8888

    # while not_started:
    #     try:
    #         print(portnum)
    #         grew.init(port=portnum)
    #     except:
    #         print('grew failed to start')
    #         portnum+=1
    #         # sys.exit('ERROR: Grew could not be initialized. Subset not created.')
    #     else:
    #         print('yay! grew started!')
    #         not_started = False
    c = 0
    while c < 5:
        try:
            grew.init()
            c = 100
        except:
            c += 1

    if c < 10:
        sys.exit('ERROR: Grew could not be initialized. Subset not created.')

    # load corpus into grew interface
    print('loading corpus file...')
    corpus_ix = grew.corpus(str(conllu_path))

    # collect matches for pattern
    print('collecting matches...')
    matches_found = grew.corpus_search(
        pat_path.read_text(encoding='utf8'), corpus_ix)
    
# Andrea Hummel on Oct 11, 2022 at 12:40 PM
# TODO: Need to modify the python script to create an **empty** subset conllu for
#   cases with no match, so that there is a record of processing having already been
#   completed. 
#       - otherwise, code will never mark subset as "complete" and loop over the
#   files endlessly
    if not matches_found:
        print(f'No matches for {pat_path.name} in {conllu_path.name}.')
        # successful exit
        sys.exit(0)
    print(len(matches_found), 'pattern matches found.')
    # pull out sentence id for every match
    match_ids_set = {m['sent_id'] for m in matches_found}
    extended_ids_iter = _add_context(match_ids_set)

    # collect conllu sentence objects for each matching sentence
    #   and put in string output format + line break
    print('generating subset conllu...')
    conllu_subset_str_gen = _generate_conllu_strings(
        pyconll.iter_from_file(str(conllu_path)),
        extended_ids_iter, match_ids_set,
        f'{pat_path.parent.name}_{pat_path.stem}')

    # create string of conllu formatted strings
    out_str = '\n'.join(conllu_subset_str_gen)

    # write string to new subset file
    #! grew complains when conllu file does not end with a blank line
    out_file.write_text(out_str+'\n', encoding='utf8')

    print(f'Subset conllu file saved to {out_file}.\n')
    print(f'  ~ completed at {datetime.now().ctime()}')


def _add_context(match_ids):
    match_context_tuples = _generate_match_tuples(match_ids)
    extended_ids_tuple = tuple(sent_id
                               for match_context in match_context_tuples
                               for sent_id in match_context)
    return extended_ids_tuple


def _generate_match_tuples(match_ids):
    match_info = namedtuple(
        'MatchContext', ['prev_sent', 'match_sent', 'next_sent'])

    for m_id in match_ids:
        doc, match = m_id.rsplit('_', 1)
        zf_len = len(match)
        sent_int = int(match)
        prev_sent = str(sent_int-1).zfill(zf_len)
        next_sent = str(sent_int+1).zfill(zf_len)
        match_tuple = match_info(f'{doc}_{prev_sent}',
                                 m_id,
                                 f'{doc}_{next_sent}')

        yield match_tuple


def _generate_conllu_strings(conll_iter: GeneratorType,
                             subset_ids,
                             match_set: set,
                             pattern: str):

    added_docs = []
    for sent in conll_iter:
        preface = ''
        sent_id = sent.id
        if sent_id in subset_ids:
            sent_meta = sent._meta
            doc_id = sent_id.rsplit('_', 1)[0]
            if doc_id not in added_docs and 'newdoc id' not in sent_meta.keys():
                sent_meta['newdoc id'] = doc_id
            if sent_id in match_set:
                try:
                    prev_pattern_match = sent_meta['pattern_match']
                except KeyError:
                    pattern_match = pattern
                else:
                    pattern_match = '; '.join((prev_pattern_match, pattern))
                sent_meta['pattern_match'] = pattern_match

            yield f'{preface}{sent.conll()}\n'


if __name__ == '__main__':

    _main()
