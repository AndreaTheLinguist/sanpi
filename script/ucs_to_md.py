# coding=utf-8
from pathlib import Path
import argparse


def _main():

    args = _parse_args()
    ucs_path = args.ucs_text_path
    lines = ucs_path.read_text(encoding='utf8').splitlines()
    if args.row_limit:
        lines = lines[:args.row_limit]

    rows = [f'# `{ucs_path.stem}`\n']
    rows.extend(convert_lines(lines))
    write_to_md(rows, ucs_path, args.row_limit)


def convert_lines(lines):
    return (f"| {' | '.join(row_cells)} |"
            for row_cells in (
                row.split()
                for row in lines))


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            'script to convert text output of ucs table to markdown table. If table is not in text format, run `ucs-print -o [file]` first.'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-u', '--ucs_text_path',
        type=Path,
        default=Path(
            '/home/arh234/projects/sanpi/results/ucs_tables/all-frq_thresh8777.35f-min3x.rsort-view_top200.txt'),
        help=('path to text version of UCS table to convert')
    )
    parser.add_argument(
        '-r', '--row_limit',
        type=int, default=0,
        help='optional limit to number of rows to include in output'
    )

    return parser.parse_args()


def write_to_md(rows, ucs_path, n_rows):
    rows = tuple(rows)
    if n_rows and len(rows) >= n_rows:
        md_path = ucs_path.with_name(
            ucs_path.name.replace('.txt', '').split('_top', 1)[0] 
            + '.txt')
        md_path = md_path.with_name(
                md_path.name.replace('.txt', f'_top{n_rows}.md'))
    else:
        md_path = ucs_path.name.replace('.txt', '.md')

    md_path.write_text('\n'.join(rows))
    print(f'✓ converted ucs table plain text to markdown: {md_path}')

if __name__ == '__main__':
    _main()
