# coding=utf-8

# %%
import argparse
from pathlib import Path

import pandas as pd
from analyze.utils.dataframes import (  # pylint: disable=import-error
    balance_sample, cols_by_str)

_DATA_DIR = Path('/share/compling/data/sanpi')
_READ_PATH = _DATA_DIR.joinpath('3_dep_info/exactly_nyt_deps.pkl.gz')
# %%


def _get_read_path():

    parser = argparse.ArgumentParser(
        description=(
            '''
                Create crosstabulations for all dependency string variants by `hit_id` (default), or another specified column.

                Note: Data file is specified either by full path
                OR by just a filename interpeted as relative to `/share/compling/data/sanpi/2_hit_tables/`.
                ** If both are given, filename argument will be ignored.
            '''
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--full_path',
        type=Path, default=None,
        help=('full path to `.pkl` file storing hits dataframe with dependency string identifiers (starting with `dep_str`)')
    )

    parser.add_argument(
        '-n', '--filename',
        type=str,
        default='exactly_nyt_deps.pkl.gz',
        help=('''
              name (only) of data file relative to `/share/compling/data/sanpi/3_dep_info/`.
              **Will be ignored if `-f`/`--full_path` is specified.**
              Note: If string does not end in `.pkl(.[compression_suffix])`, program will attempt to find the file by appending `.pkl` or `.pkl.gz`.
              ''')
    )

    args = parser.parse_args()

    if args.full_path:
        return args.full_path

    else:
        dir_path = Path('/share/compling/data/sanpi/3_dep_info/')
        if dir_path.is_dir():
            fpath = dir_path.joinpath(args.filename)
        else:
            exit(f'Default directory {dir_path} not found.')

        if '.pkl' in fpath.suffixes:
            if fpath.is_file():
                return fpath
            else:
                gzpath = fpath.with_name(fpath.name + '.gz')
                if gzpath.is_file():
                    return gzpath
                else:
                    exit(f'Pickled dataframe {fpath} not found.')
        elif not fpath.suffixes:
            if fpath.with_suffix('.pkl.gz').is_file():
                return fpath.with_suffix('.pkl.gz')
            elif fpath.with_suffix('.pkl').is_file():
                return fpath.with_suffix('.pkl')
            else:
                exit(
                    f'Name {args.filename} does not point to existing pickled dataframe.')
        else:
            exit(
                f'Input data must be in pickle format. Invalid input: {fpath}')

    return parser.parse_args()


def _select_columns(_df, extra: bool = True):
    _col_list = _df.columns[_df.columns.str.endswith(
        ('category', 'corpus', 'colloc_id', 'colloc', 'hit_text', 'lemma'))
    ].to_list() + _depstr_cols(_df) if extra else _depstr_cols(_df)

    return _col_list


def _depstr_cols(_df):
    return cols_by_str(_df, 'dep_str')

# TODO: add argument for "cross" column (to crosstabulate dep strings with more than just `hit_id`)
def crosstabulate_variants(df: pd.DataFrame,
                           cross_col: str = 'hit_id',
                           out_label: str = None,
                           dep_dir=Path(
                               '/share/compling/data/sanpi/3_dep_info'),
                           n_per_category: int = None,
                           include_extra: bool = True,
                           n_largest: int = 5):
    if out_label is None:
        out_label = pd.Timestamp.now().strftime("%Y-%m-%d_%H%M")

    lines = [
        # TODO: change this line as well once it's not just `hit_id`
        f'# All dependency string identifier variants crosstabulated with `{cross_col}`\n',
        pd.Timestamp.now().strftime("%Y-%m-%d %I:%M%p")
        # pd.Timestamp.now().ctime()
    ]

    crosstab_dir = dep_dir.joinpath('crosstab')
    if not crosstab_dir.is_dir():
        crosstab_dir.mkdir(parents=True)

    ct_out_fstem = f'{out_label}_ct'

    if n_per_category is not None:
        ct_out_fstem += '-sample'

        df, sample_info = balance_sample(df, column_name='category',
                                         sample_per_value=n_per_category,
                                         verbose=True)
        lines.append(sample_info)

    _ct_cols = _select_columns(df, include_extra)
    _ct_cols.sort()
    ct_tables = get_crosstabs(df, _ct_cols)

    for ct_col, ctdf in ct_tables.items():
        #TODO: change paths to include info on "cross" column once added
        csv_path = crosstab_dir.joinpath(
            f'{ct_out_fstem}_{ct_col.replace("_", "-")}.csv')
        ctdf.to_csv(csv_path)

        lines.append(f'\n\n## `{ct_col}`')
        lines.append(f"\n- *Defined for {ctdf.pop('SUM').loc['SUM']} hits*")
        lines.append(
            f"\n- Full crosstabulation dataframe saved to\n  `{csv_path}`")
        lines.append(f'\n### {n_largest} most common `{ct_col}` values\n')
        lines.append(ctdf.transpose().SUM.nlargest(n_largest).to_markdown())

    md_info_path = crosstab_dir.joinpath(f'{ct_out_fstem}_info.md')
    print('- Depencency crosstab info overview saved to:\\')
    print(f'  `{md_info_path}`')
    md_info_path.write_text('\n'.join(lines), encoding='utf8')


def get_crosstabs(df: pd.DataFrame,
                  columns: list = None,
                  cross: str = 'hit_id'):
    crosstab_dict = {}
    df = df.reset_index()
    if not columns:
        columns = _depstr_cols(df)
    for c in columns:
        df[c] = df[c].str.replace(';', '; ').str.replace(';  ', '; ')
        crosstab_dict[c] = pd.crosstab(
            index=df[cross], columns=df[c],
            rownames=[cross], margins=True, margins_name='SUM')
    return crosstab_dict


# %%
if __name__ == '__main__':
    # _READ_PATH = _get_read_path()
    dep_df = pd.read_pickle(_READ_PATH)

    crosstabulate_variants(dep_df, n_per_category=5)

    crosstabulate_variants(dep_df)
