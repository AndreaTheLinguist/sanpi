import argparse
import multiprocessing
import logging
import os
import sys
import time
from pathlib import Path

_LOGGER = multiprocessing.log_to_stderr()
_LOGGER.setLevel(logging.WARNING)

# TODO : make default to not overwrite existing (non-empty) raw.json files; otherwise need to have new pat directories for any added patterns (to avoid needing to redo all the searches already run)


def grew_search(corpus_dir: Path,
                pat_file: Path,
                match_dir: Path,
                skip_files=False):
    multiprocessing.set_start_method('forkserver')

    if not match_dir.is_dir():
        match_dir.mkdir(parents=True)

    file_count = len(tuple(corpus_dir.glob('*.conllu')))

    #: set pool `processes` argument to number of _available_ cpus
    # OR number of files to be searched, whichever is smaller
    cpus = min(len(os.sched_getaffinity(0)), file_count)
    print(f'\n> {file_count} files total in ../'
          f'{Path(*corpus_dir.parts[-3:])}/ to be searched with {cpus} CPUs...')
    _start = time.perf_counter()

    with multiprocessing.Pool(processes=cpus) as pool:

        # NOTE: if `starmap` method used instead, call `_seek_pat_in_file` directly (and no need to print)
        results = pool.imap_unordered(
            _star_seek_pat,
            _arg_paths_generator(corpus_dir.glob('*.conllu'),
                                 match_dir, pat_file, skip_files))

        zfill_len = len(str(file_count))
        gap = max(4, zfill_len)+2
        print(f'  task{" " * (gap -2 )}|  time\tinput data\n'
              f'{"-" * (gap + 4 -2)}  |  {"-" * 8}\t---------------')
        #! this is required to actually get the processes to run
        for i, result in enumerate(results):
            print(
                f'   {str(i+1).zfill(zfill_len)}{" " * (gap+1-zfill_len)}|  {result}')
        # ? Is there a better way to do this? ^^ Like, some "run" or "start" or "join" method?

        _end = time.perf_counter()

    print(f'\n{file_count} files searched'
          f'\nacross \t{cpus} cpus'
          f'\nin {round((_end - _start)/60, 2):.2f} minutes\n'
          f'Raw pattern match json files saved to:\n'
          f'  ../{Path(*match_dir.parts[-5:])}/\n'
          '============================')


def _arg_paths_generator(file_glob,
                         match_dir_path: Path,
                         pat_file: Path,
                         skip_files: bool):

    for input_path in file_glob:
        #: skip any subdirectories in corpus/conllu files directory
        # ? isn't this redundant given the glob expression? ^^
        if not input_path.is_file():
            continue
        output_path = match_dir_path.joinpath(
            input_path.stem + '.raw.json')

        # if skip flag given, see which if any files should be skipped
        if skip_files:
            try:
                size = output_path.stat().st_size

            # if file does not exist, still include file in generator
            except FileNotFoundError:
                pass

            # if file does exist already
            else:
                # if empty and predates pattern file changes
                if size < 100 and output_path.stat().st_mtime < pat_file.stat().st_mtime:
                    _LOGGER.warning(msg='File exists but is empty and older than last pattern modification. '
                                    'Grew search will be re-run.')
                # if nonempty or pattern has not changed since output last modified
                #  =>> SKIP
                else:
                    _LOGGER.warning(msg=f'{output_path.resolve()}\n'
                                    '  >> {input_path.stem} matches will not be updated.\n'
                                    f'     (Output path is non-empty '
                                    'and pattern has not changed.)')
                    continue

        yield input_path, pat_file, output_path


def _seek_pat_in_file(corpus, pat, out):

    f_start = time.perf_counter()

    # append ' 2>/dev/null' for debugging
    grew_cmd_str = (
        f'grew grep -pattern {pat} -i {corpus} > {out}')

    # TODO : update this to use `subprocess` module instead, so that grew warnings/errors can be handled better
    os.system(grew_cmd_str)

    dur = time.perf_counter() - f_start
    if dur < 60:
        dur = f'{_dur_round(dur)}s'
    else:
        dur = f'{_dur_round(dur/60)}m'

    return (f'{dur}\t{corpus.stem}')


def _dur_round(dur):
    if dur < 10:
        return f'{round(dur, 2):.2f}'
    else:
        return f'{round(dur, 1):.1f}'


def _star_seek_pat(args):
    return _seek_pat_in_file(*args)


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
                        help='upper level output directory name. Should correspond to '
                             'sentence data source and pattern like so: '
                             '"<data set>.<pattern name>", e.g. "Nyt1."')

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
        print(f'{name}\t: {value}')
    print(f'[Logging Level\t: {_LOGGER.getEffectiveLevel()}]')
    
    return [a[1] for a in args._get_kwargs()]


if __name__ == '__main__':
    start_time = time.perf_counter()
    print('>>> Running `grew_search` with:')
    grew_search(*_parse_args())
    end_time = time.perf_counter()
    print(f'time elapsed:\t{round((end_time-start_time)/60, 2):.2f} minutes\n')
