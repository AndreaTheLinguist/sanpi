
import argparse
import os
from pathlib import Path


def main():

    parser = argparse.ArgumentParser(
        description='simple glue program to initiate multiple pipes in one go. Default log option will be used.'
        'If no arguments are given, every corpus dir and pattern subdir in the current working directory will be run.')

    parser.add_argument('-c', '--corpus', action='append', dest='corpora',
                        help='specify any corpus directory to be searched with. '
                        'Can include as many as desired, but each one needs a flag.',
                        type=Path)

    parser.add_argument('-p', '--patterns', action='append', dest='patterndirs',
                        help='specify pattern directory to gather data for. '
                        'Can include as many as desired, but each one needs a flag.',
                        type=Path)

    args = parser.parse_args()

    patdirs = ((p.resolve() for p in args.patterndirs) if args.patterndirs
               else list(Path.cwd().glob('Pat/*')))

    corpora = ((c.resolve() for c in args.corpora) if args.corpora
               else list(Path.cwd().glob('*.conll')))

    for patdir in patdirs:

        for corpus in corpora:

            print(
                f'>> searching {corpus} for patterns specified in {patdir}...')
            cmd_str = f'./script/makeTable.sh {corpus}/ {patdir}/ default'
            print(cmd_str)
            os.system(cmd_str)


if __name__ == '__main__':

    main()
