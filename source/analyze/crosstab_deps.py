# coding=utf-8

# %%
import argparse
import io
from pathlib import Path

import pandas as pd
from analyze.utils.dataframes import (  # pylint: disable=import-error
    balance_sample, cols_by_str)
from analyze.utils.general import ( # pylint: disable=import-error
                                   dur_round)

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
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-p', '--full_path',
        type=Path, default=None,
        help=('full path to `.pkl` file storing hits dataframe '
              'with dependency string identifiers (starting with `dep_str`)')
    )

    parser.add_argument(
        '-n', '--filename',
        type=str,
        default='exactly_nyt_deps.pkl.gz',
        help=('''
              name (only) of data file relative to `/share/compling/data/sanpi/3_dep_info/`.
              **Will be ignored if `-f`/`--full_path` is specified.**
              Note: If string does not end in `.pkl(.[compression_suffix])`, 
                    program will attempt to find the file by appending `.pkl` or `.pkl.gz`.
              ''')
    )

    args = parser.parse_args()

    if args.full_path:
        path = args.full_path

    else:
        dir_path = Path('/share/compling/data/sanpi/3_dep_info/')
        if dir_path.is_dir():
            fpath = dir_path.joinpath(args.filename)
        else:
            exit(f'Default directory {dir_path} not found.')

        if '.pkl' in fpath.suffixes:
            if fpath.is_file():
                path = fpath
            else:
                gzpath = fpath.with_name(fpath.name + '.gz')
                if gzpath.is_file():
                    path = gzpath
                else:
                    exit(f'Pickled dataframe {fpath} not found.')
        elif not fpath.suffixes:
            if fpath.with_suffix('.pkl.gz').is_file():
                path = fpath.with_suffix('.pkl.gz')
            elif fpath.with_suffix('.pkl').is_file():
                path = fpath.with_suffix('.pkl')
            else:
                exit(
                    f'Name {args.filename} does not point to existing pickled dataframe.')
        else:
            exit(
                f'Input data must be in pickle format. Invalid input: {fpath}')

    return path


def _select_columns(_df, extra: bool = True):
    _col_list = _df.columns[_df.columns.str.endswith(
        ('category', 'corpus', 'bigram_id', 'colloc', 'hit_text', 'lemma'))
    ].to_list() + _depstr_cols(_df) if extra else _depstr_cols(_df)

    return _col_list


def _depstr_cols(_df):
    return cols_by_str(_df, 'dep_str')


def crosstabulate_variants(df: pd.DataFrame,
                           cross: str = 'hit_id',
                           out_label: str = None,
                           dep_dir=Path(
                               '/share/compling/data/sanpi/3_dep_info'),
                           n_per_category: int = None,
                           include_extra: bool = True,
                           n_largest: int = 5):

    # TODO: add argument for "cross" column (to crosstabulate by more than just `hit_id`)
    if out_label is None:
        out_label = pd.Timestamp.now().strftime("%Y-%m-%d_%H%M")

    lines = [
        # TODO: change this line as well once it's not just `hit_id`
        f'# All dependency string identifier variants crosstabulated by `{cross}`\n',
        pd.Timestamp.now().strftime("%Y-%m-%d %I:%M%p")
        # pd.Timestamp.now().ctime()
    ]

    crosstab_dir = dep_dir.joinpath('crosstab', cross)
    if not crosstab_dir.is_dir():
        crosstab_dir.mkdir(parents=True)

    ct_out_fstem = f'{out_label}_X-{cross}'

    if n_per_category:
        ct_out_fstem += f'[n{n_per_category}]'

        df, sample_info = balance_sample(df, column_name='category',
                                         sample_per_value=n_per_category,
                                         verbose=True)
        lines.append(sample_info)

    _ct_cols = _select_columns(df, include_extra)
    # > to avoid "crosstab by self"
    if cross in _ct_cols:
        _ct_cols.pop(_ct_cols.index(cross))
    _ct_cols.sort()
    
    ct_generator = gen_crosstabs(df, ct_out_fstem, crosstab_dir, _ct_cols, cross)

    for ct_col, ctdf in ct_generator:
        csv_path = crosstab_dir.joinpath(
            f'{ct_out_fstem}_{ct_col.replace("_", "-")}.csv')
        ctdf.to_csv(csv_path)
        
        pkl_path = csv_path.with_suffix('.pkl.gz')
        ctdf.to_pickle(pkl_path)

        lines.append(f'\n\n## `{cross}` x `{ct_col}`')
        lines.append(
            f"\n- *both values defined for {ctdf.pop('SUM').loc['SUM']} rows*")
        lines.append(
            f"\n- Full crosstabulation dataframe saved to\n  `{csv_path}`")
        lines.append(f'\n### {n_largest} most common `{ct_col}` values\n')
        lines.append(ctdf.transpose().SUM.nlargest(n_largest).to_markdown())

    md_info_path = crosstab_dir.joinpath(f'{ct_out_fstem}_info.md')
    print('- Depencency crosstab info overview saved to:\\')
    print(f'  `{md_info_path}`')
    md_info_path.write_text('\n'.join(lines), encoding='utf8')


def gen_crosstabs(df: pd.DataFrame,
                  out_stem: Path,
                  out_dir: Path,
                  columns: list = None,
                  cross: str = 'hit_id', 
                  ):
    
    df = df.reset_index()
    if not columns:
        columns = _depstr_cols(df)
    print('|  column   |  time  |  rows  |  columns  |  memory  |')
    print('|:----------|-------:|-------:|----------:|---------:|')
    for c in columns:
        csv_path = out_dir.joinpath(
            f'{out_stem}_{c.replace("_", "-")}.csv')
        if csv_path.is_file(): 
            print(f'{csv_path} already exists. Skipping.')
            continue
        #\\ print(f'\ncolumn: `{c}`')
        # ! Hack to avoid "performance error" in crosstab unstack step; may or may not work...
        if c.endswith('id') and cross.endswith('id'):
            continue
        
        proc_t0 = pd.Timestamp.now()
        df[c] = df[c].str.replace(';', '; ').str.replace(';  ', '; ')
        ctdf = pd.crosstab(
                   index=df[cross], columns=df[c],
                   rownames=[cross], margins=True, margins_name='SUM')

        proc_t1 = pd.Timestamp.now()
        iobuf = io.StringIO()
        ctdf.info(buf=iobuf)
        mem_info = iobuf.getvalue().rsplit('\n',2)[1].split(': ')[1]
        print(f"| {c} | {dur_round((proc_t1 - proc_t0).seconds)} | {len(ctdf)} | {ctdf.shape[1]} | {mem_info} |")
        
        yield (c, ctdf)

if __name__ == '__main__':
    # _READ_PATH = _get_read_path()
    dep_df = pd.read_pickle(_READ_PATH)

    # FIXME: These calls are obsolete
    crosstabulate_variants(dep_df, n_per_category=5)
    crosstabulate_variants(dep_df)
