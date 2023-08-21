# coding=utf-8
from pathlib import Path
import argparse
import csv
from collections import namedtuple


def _main():

    args = _parse_args()
    ucs_path = args.ucs_text_path
    lines = ucs_path.read_text(encoding='utf8').splitlines()
    if args.row_limit:
        # > NOTE: `+2` is to account for the header and border rows still included
        lines = lines[:args.row_limit+2]
    row_dict, fields = convert_lines(lines)
    write_to_csv(row_dict, ucs_path, fields, args.row_limit)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'script to convert text output of ucs table to comma separated (csv). '
            'If table is not in text format, run `ucs-print -o [file]` first.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-u', '--ucs_text_path',
        type=Path,
        default=Path(
            '/home/arh234/projects/sanpi/results/ucs_tables/all-frq_thresh8777'
            '.35f-min3x.rsort-view_top200.txt'),
        help=('path to text version of UCS table to convert')
    )
    parser.add_argument(
        '-r', '--row_limit',
        type=int, default=0,
        help='optional limit to number of rows to include in output'
    )

    return parser.parse_args()


def convert_lines(lines):

    # > _retrieve_ header row
    header = lines.pop(0)
    # > _discard_ horizontal border row
    lines.pop(0)
    csv_tuple = namedtuple('ucs_row', header.replace('.', '_').split())
    return ((csv_tuple._make(line.split())._asdict() for line in lines),
            csv_tuple._fields)


def write_to_csv(row_dicts, ucs_path: Path, fields, n_rows):
    row_dicts = tuple(row_dicts)
    if n_rows and len(row_dicts) >= n_rows:
        csv_path = ucs_path.with_name(
            ucs_path.name.replace('.txt', '').split('_top', 1)[0] 
            + '.txt')
        csv_path = csv_path.with_name(
                csv_path.name.replace('.txt', f'_top{n_rows}.csv'))
    else:
        csv_path = ucs_path.with_name(ucs_path.name.replace('.txt', '.csv'))

    with open(csv_path, mode='w') as csv_out:
        writer = csv.DictWriter(csv_out, fields)
        writer.writeheader()
        writer.writerows(row_dicts)
    print(f'✓ converted ucs table .txt to .csv: {csv_path}')


if __name__ == '__main__':
    _main()
