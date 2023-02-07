# coding=utf-8

import argparse
import multiprocessing
import os
import sys
import time
from pathlib import Path

_LOGGER = multiprocessing.log_to_stderr()
_LOGGER.setLevel(30)  # warning
# _LOGGER.setLevel(20)  # info
# _LOGGER.setLevel(10) # debug

def grew_search(corpus_dir: Path,
                pat_file: Path,
                match_dir: Path,
                skip_files=True):
    multiprocessing.set_start_method('forkserver')
    if not match_dir.is_dir():
        match_dir.mkdir(parents=True)

    file_count = len(tuple(corpus_dir.glob('*.conllu')))

    # > set pool `processes` argument to number of _available_ cpus
    # > OR number of files to be searched, whichever is smaller
    cpus = min(len(os.sched_getaffinity(0)), file_count, 15)
    print(f'\n> searching {file_count} files in ../'
          f'{Path(*corpus_dir.parts[-3:])}/ with {cpus} CPUs...')
    _start = time.perf_counter()

    with multiprocessing.Pool(processes=cpus) as pool:

        # NOTE: if `starmap` method used instead, call `_seek_pat_in_file` directly (and no need to print)
        results = pool.imap_unordered(
            _star_seek_pat,
            _arg_paths_generator(corpus_dir.glob('*.conllu'),
                                 match_dir, pat_file, skip_files))

        zfill_len = len(str(file_count))
        in_sz_w = 7
        out_sz_w = 8
        in_name_w = len(list(corpus_dir.glob('*conllu'))[0].stem)+1
        print(('  task  |  time  \tin size\tout size\t'
               f'{"in data".ljust(in_name_w)}\t'
               ' out data\n'
               f' ------ | ------ \t'
               f'{"-"*in_sz_w}\t'
               f'{"-"*out_sz_w}\t'
               f'{"-"*in_name_w}\t'
               f'{"-"*40}'
               ).expandtabs(3))
        #! this is required to actually get the processes to run
        i = 0
        for result in results:
            i += 1
            dur, in_name, in_size, out_name, out_size = result
            print((f'{str(i).zfill(zfill_len).center(8)}|{dur.rjust(7)} \t'
                   f'{in_size.center(in_sz_w)}\t'
                   f'{out_size.center(out_sz_w)}\t'
                   f'{in_name.ljust(in_name_w)}\t'
                   f'{out_name}').expandtabs(3))
        search_count = i
        # ? Is there a better way to do this? ^^ Like, some "run" or "start" or "join" method?
        _end = time.perf_counter()

    print(f'\n{search_count} files searched'
          f'\nacross {cpus} cpus'
          f'\nin {round((_end - _start)/60, 2):.2f} minutes\n'
          f'Raw pattern match json files saved to:\n'
          f'  ../{Path(*match_dir.parts[-5:])}/\n'
          '============================')


def _star_seek_pat(args):
    return _seek_pat_in_file(*args)


def _seek_pat_in_file(corpus, pat, out):

    f_start = time.perf_counter()
    # > append ' 2>/dev/null' for debugging
    # NOTE: -pattern changed to -request 
    #   per WARNING: -pattern and -patterns comman line args are deprecated, replaced by -request and -requests
    grew_cmd_str = (f'grew grep -request {pat} -i {corpus} > {out}')

    #TODO: update this to use `subprocess` module instead,
    #   so that grew warnings/errors can be handled better
    os.system(grew_cmd_str)

    dur = dur_round(time.perf_counter() - f_start)

    return (dur,
            corpus.stem, _size_round(corpus.stat().st_size),
            Path(*out.parts[-2:]), _size_round(out.stat().st_size))


def dur_round(dur: float):
    """take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits 

    Args:
        dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = 's'
    if dur >= 60:
        dur = dur/60
        unit = 'm'

        if dur >= 60:
            dur = dur/60
            unit = 'h'

    if dur < 10:
        dur_str = f'{round(dur, 2):.2f}{unit}'
    else:
        dur_str = f'{round(dur, 1):.1f}{unit}'

    return dur_str


def _size_round(size: int):

    if size >= 10**8:
        unit = 'G'
        power = 9
    elif size >= 10**5:
        unit = 'M'
        power = 6
    elif size >= 10**2:
        unit = 'K'
        power = 3
    else:
        unit = ''
        power = 0

    return f'{round(size / (10**power), 1):.1f} {unit}B'


def _arg_paths_generator(file_glob,
                         match_dir_path: Path,
                         pat_file: Path,
                         skip_files: bool):

    for input_path in file_glob:
        # > skip any subdirectories in corpus/conllu files directory
        # ? isn't this redundant given the glob expression? ^^
        if not input_path.is_file():
            continue
        corpus = input_path.stem
        output_path = match_dir_path.joinpath(
            f'{corpus}.raw.json')

        try:
            size = output_path.stat().st_size

        # if file does not exist, include file in generator
        except FileNotFoundError:
            pass

        # if file does exist already
        else:
            # if skip flag given, see which if any files should be skipped
            if skip_files:

                # if file size is exactly 0 bytes (nothing in it at all)
                # NOTE: a "no hits found" file consists of "[]" (3 bytes; "[\n]\n" is 5 bytes)
                if size == 0:
                    _LOGGER.warning(
                        'Results file %s exists for but is completely empty, suggesting a previous out-of-memory crash. '
                        'Grew search will be re-attempted on for %s data', output_path.name, corpus
                    )
                # if no hits and predates pattern file changes
                elif size < 10 and output_path.stat().st_mtime < pat_file.stat().st_mtime:
                    _LOGGER.warning(
                        f'Results file {output_path} exists but is empty and older than last pattern modification. '
                        'Grew search will be re-attempted for %s', corpus)
                # if nonempty or pattern has not changed since output last modified
                #  =>> SKIP
                else:
                    _LOGGER.warning(
                        '%s\n  >> %s matches will not be updated.\n'
                        '     (Output path is non-empty and pattern has not changed.)',
                        output_path.resolve(), corpus)
                    continue

        yield input_path, pat_file, output_path


def _validate_args(args):

    corpus_dir = args.corpus_dir

    if not corpus_dir.is_dir():
        sys.exit('Error: specified corpus path is not an existing directory.')

    conllu_files = tuple(corpus_dir.glob('*.conllu'))
    if not conllu_files:
        sys.exit(
            'Error: specified corpus directory does not contain any conllu '
            'formatted files.')

    if not (args.pat_file.is_file() and args.pat_file.suffix == '.pat'):
        sys.exit('Error: path specifed for pattern is not a .pat file.')


def _parse_args():

    parser = argparse.ArgumentParser(
        description='script to loop over files in given directory with given '
                    'grew pattern search')

    parser.add_argument('corpus_dir', type=Path, default=Path.cwd(),
                        help='path to directory containing conll files to '
                             'search for grew pattern')

    parser.add_argument('pat_file', type=Path,
                        help='path to grew pattern to search for')

    parser.add_argument('output_dir', type=Path,
                        default='/share/compling/data/sanpi/1_json_grew-matches',
                        help='upper level output directory name for grew match data. '
                        'Will be populated with subdir corresponding to pattern dir, '
                        'with filenames patterned like so: '
                             '"[conll dirname].[pat filename]", e.g. "Nyt1.sans-relay"')

    parser.add_argument('-s', '--skip_files', action='store_true',
                        default=False,
                        help='option to skip corpus files that already have '
                             'a corresponding output in the given json '
                             'directory. Grew search will not be rerun and '
                             'pre-existing raw json file will be preserved.'
                             '* Empty output files that predate pattern changes '
                             'will be overwritten.')

    args = parser.parse_args()
    _validate_args(args)
    pat_path = args.pat_file
    args.output_dir = args.output_dir.joinpath(
        pat_path.parent.name, f'{args.corpus_dir.stem}.{pat_path.stem}')

    for name, value in args._get_kwargs():
        print(f'{name.rjust(15)} : {value}')
    print(f'{"[Logging Level".rjust(15)} : {_LOGGER.getEffectiveLevel()}]')

    return [a[1] for a in args._get_kwargs()]


if __name__ == '__main__':
    start_time = time.perf_counter()
    print('>>> Running `grew_search` with:')
    grew_search(*_parse_args())
    end_time = time.perf_counter()
    print(f'time elapsed:\t{round((end_time-start_time)/60, 2):.2f} minutes\n')
