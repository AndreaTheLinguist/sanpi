import argparse
import os
import sys
import time
from pathlib import Path

# TODO: make default to not overwrite existing (non-empty) raw.json files;
#   otherwise need to have new pat directories for any added patterns
#   (to avoid needing to redo all the searches already run)


def grew_search():
    absStart = time.perf_counter()
    args = parseArgs()

    dirPath = args.corpus_dir
    patPath = args.pat_file
    outputDir = args.output

    print(f'```\n### Running grew search on `{dirPath.name}`...\n```')

    checkArgs(args)

    if not outputDir.exists():
        outputDir.mkdir(parents=True)

    # testDirStr = f'if [ ! -d {outputDir} ]; then mkdir {outputDir}; fi'
    # os.system(testDirStr)

    # iterate over items in dirPath ending with ".conllu"
    # TODO: make this a parallel loop? 
    for f in dirPath.glob('*.conllu'):

        fstart = time.perf_counter()
        # skip any subdirectories in corpus/conllu files directory
        if f.is_dir():
            continue

        outPath = outputDir.joinpath(f.stem + '.raw.json')

        # do not run grew search if output (raw) json file already exists
        if args.skip_files and outPath.exists():
            print(
                f'Output file {outPath.name} already exists in '
                f'{outPath.parent.relative_to(outPath.home())}.\n'
                f'  -> Grew search will not be re-run.')
            continue

        grew_cmd_str = (f'grew grep -pattern {patPath} -i {f} > {outPath}')
        print(f'-> searching {f.relative_to(dirPath.parent)}:\n{grew_cmd_str}')

        os.system(grew_cmd_str)

        fend = time.perf_counter()
        print(f'{round((fend - fstart)/60, 2)} minutes on {f.name}')

    absFinish = time.perf_counter()
    print(f'\nTotal grew search time: '
          f'{round((absFinish - absStart)/60, 2)} minutes\n'
          '==============================================\n')


def checkArgs(args):

    dirPath = args.corpus_dir

    if not dirPath.is_dir():
        sys.exit('Error: specified corpus path is not a directory.')

    corpus_files = tuple(dirPath.glob('*.conllu'))
    if not corpus_files:
        sys.exit(
            'Error: specified corpus directory does not contain any conllu '
            'formatted files.')

    if args.pat_file.is_dir():
        sys.exit(
            'Error: path specifed for pattern file is a directory.')

    print(f'{len(corpus_files)} total file(s) to be searched.')

    return


def parseArgs():

    parser = argparse.ArgumentParser(
        description='script to loop over files in given directory with given '
                    'grew pattern search')

    parser.add_argument('corpus_dir', type=Path, default=Path.cwd(),
                        help='path to directory containing conll files to '
                             'search for grew pattern')

    parser.add_argument('pat_file', type=Path,
                        help='path to grew pattern to search for')

    # arguement to specify subdirectory?
    # parser.add_argument('-c', type=Path,
    #                     help='')

    parser.add_argument('output', type=Path,
                        help='output directory name. Should correspond to '
                             'sentence data source and pattern like so: '
                             '"<data set>.<pattern name>", e.g. "Nyt1.p1"')

    parser.add_argument('-s', '--skip_files', action='store_true',
                        default=False,
                        help='option to skip corpus files that already have '
                             'a corresponding output in the given json '
                             'directory. Grew search will not be rerun and '
                             'pre-existing raw json file will be preserved.')

    return parser.parse_args()


if __name__ == '__main__':

    grew_search()
