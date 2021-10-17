
import argparse
import os
import time
from pathlib import Path


def main():

    # check requirements
    os.system('bash script/checkRequirements.sh')

    args = parse_input_args()

    patdirs = (args.patterndirs if args.patterndirs
               else list(Path.cwd().glob('Pat/*')))

    corpora = (args.corpora if args.corpora
               else list(Path.cwd().glob('*.conll')))

    for patdir in patdirs:

        for corpus in corpora:

            print(
                f'>> searching _{corpus.relative_to(Path.cwd())}_ for '
                f'patterns specified in _{patdir.relative_to(Path.cwd())}_...')

            # run grew search
            for pat in patdir.iterdir():
                # args: corpus_dir pat_file output
                corpus_name = corpus.stem.split('.')[0]
                output_label = '.'.join([corpus_name, pat.stem])

                grew_cmd = f'python script/grewSearchDir.py {corpus}/ {pat} {output_label}'
                print(grew_cmd)
                os.system(grew_cmd)

                # run fill json
                # args: FillJson.py [-h] -c CONLLU_DIR -r RAW_DIR [-o OUTPUT_DIR] [-w {yes,no,check}] [-t {lemma,form}]
                data_dir = Path(f'data/{patdir.stem}/{output_label}').resolve()
                filljson_cmd = f'python script/FillJson.py -c {corpus}/ -r {data_dir}/'
                print(filljson_cmd)
                os.system(filljson_cmd)

                # run tabulate
                # usage: tabulateHits.py [-h] -p PAT_JSON_DIR -o OUTPUTPREFIX [-m] [-v]
                tabulate_cmd = f'python script/tabulateHits.py -p {data_dir} -o {corpus_name}_{pat.stem}'

                print(tabulate_cmd)
                os.system(tabulate_cmd)


def parse_input_args():

    parser = argparse.ArgumentParser(
        description=(
            'simple glue program to initiate multiple pipes in one go. '
            'Default log option will be used. If no arguments are '
            'given, every corpus dir and pattern subdir in the current '
            'working directory will be run.'))

    parser.add_argument('-c', '--corpus', action='append', dest='corpora',
                        help='specify any corpus directory to be searched with. '
                        'Can include as many as desired, but each one needs a flag.',
                        type=Path)

    parser.add_argument('-p', '--patterns', action='append', dest='patterndirs',
                        help='specify pattern directory to gather data for. '
                        'Can include as many as desired, but each one needs a flag.',
                        type=Path)

    return parser.parse_args()


if __name__ == '__main__':
    t0 = time.perf_counter()
    main()
    t1 = time.perf_counter()
    print(f'total time: {round((t1-t0)/60, 2)} minutes')
