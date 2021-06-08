import argparse
import os
import sys
import time
from pathlib import Path


def __main__():

    args = parseArgs()

    dirPath = args.dir
    patPath = args.pat
    outputDir = args.output

    print(f'\nRunning grew search on conll files in {dirPath.name}...\n')

    checkArgs(args)

    testDirStr = f'if [ ! -d {outputDir} ]; then mkdir {outputDir}; fi'
    os.system(testDirStr)

    for f in os.listdir(dirPath):

        filePref, ext = f.split('.')
        if ext != 'conllu':
            continue
        filePathName = f'{dirPath}/{f}'
        outputFilename = f'{filePref}.raw.json'

        # do not run grew search if output (raw) json file already exists
        if args.skip_files and outputFilename in os.listdir(outputDir):
            print(
                f'Output file {outputFilename} already exists for {filePathName}. Grew search will not be re-run.')
            continue

        grew_cmd_str = f'grew grep -pattern {patPath} -i {filePathName} > {outputDir}/{filePref}.raw.json'
        print(f'searching {filePathName}...')
        print('grew command: ', grew_cmd_str)

        os.system(grew_cmd_str)

    return


def checkArgs(args):

    dirPath = args.dir

    if not dirPath.is_dir():
        sys.exit('Error: path specified for directory to search is not a directory.')

    if args.pat.is_dir():
        sys.exit('Error: path specifed for pattern file is a directory.')

    if len(os.listdir(dirPath)) < 1:
        sys.exit('Error: specified search directory is empty.')

    print(f'{len(os.listdir(dirPath))} total files to be searched.')

    return


def parseArgs():

    parser = argparse.ArgumentParser(
        description='script to loop over files in given directory with given grew pattern search')

    parser.add_argument('dir', type=Path, default=Path.cwd(),
                        help='path to directory containing conll files to search for grew pattern')

    parser.add_argument('pat', type=Path,
                        help='path to grew pattern to search for')

    parser.add_argument('output', type=str,
                        help='output directory name for. Should correspond to sentence data source and pattern like so: "<data set>.<pattern name>", e.g. "Nyt1.p1"')

    parser.add_argument('-s', '--skip_files', action='store_true',
                        default=False,
                        help='option to skip corpus files that already have a corresponding output in the given json directory. Grew search will not be rerun and pre-existing raw json file will be preserved.')

    return parser.parse_args()


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round((absFinish - absStart)/60, 2)} minutes')
