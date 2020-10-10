import argparse
import os
import sys
import time
from pathlib import Path


def __main__():

    args = parseArgs()

    checkArgs(args)

    dirPath = args.dir
    patPath = args.pat
    outputDir = args.output
    testDirStr = f'if [ ! -d {outputDir} ]; then mkdir {outputDir}; fi'
    os.system(testDirStr)

    limit = 1 if args.limit else -1

    for file in os.listdir(dirPath)[0:limit]:

        filePref, _ = file.split('.')
        filePathName = f'{dirPath}/{file}'
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

    elif args.limit:

        print(
            f'File limit is enabled. Only first 2 files in {dirPath.name} will be searched.')

    else:
        print(f'{len(os.listdir(dirPath))} total files to be searched.')

    return


def parseArgs():

    parser = argparse.ArgumentParser(
        description='script to loop over files in given directory with given grew pattern search')

    parser.add_argument('dir', type=Path, default=Path.cwd(),
                        help='path to directory containing conll files to search for grew pattern')

    parser.add_argument(
        'pat', type=Path, help='path to grew pattern to search for')

    parser.add_argument(
        'output', type=str, help='output directory name for. Should correspond to sentence data source and pattern like so: "<data set>.<pattern name>", e.g. "Nyt1.p1"')

    parser.add_argument('-l', '--limit', default=False, action='store_true',
                        help='Option to limit search to only the first 2 files in directory.')

    return parser.parse_args()


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round(absFinish - absStart, 2)} seconds')
