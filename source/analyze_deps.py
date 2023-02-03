# coding=utf-8
import argparse
from pathlib import Path
import textwrap

import pandas as pd
from analyze.crosstab_deps import crosstabulate_variants as ct_var
from analyze.get_deps import get_deps as get_deps
from analyze.utils import dataframes as udf
from analyze.utils import general as ugen

# TODO: move all this to an argparse function / pull from crosstab_deps?
# _DATA_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
# _FILEGLOB = '*hits.pkl.gz'
# _DF_SAVE_DIR = _DATA_DIR.parent.joinpath('3_dep_info')
# if not _DF_SAVE_DIR.is_dir():
#     _DF_SAVE_DIR.mkdir()
# _DF_SAVE_PATH = _DF_SAVE_DIR.joinpath(
#     f'{_FILEGLOB.split("*")[0]}_deps.pkl.gz')


def _main():
    args = _parse_args()
    n_per_category = args.sample_size
    

    # * if path to processed df given, jump straight to crosstab and pull output info from input path
    if args.dep_df:
        input_path = args.dep_df

        ct_label = input_path.name.split('.')[0].replace('_deps', '')

        if n_per_category is not None:
            ct_label = f'{ct_label}-n{n_per_category}'

        ct_var(df=pd.read_pickle(input_path),
               out_label=ct_label,
               dep_dir=input_path.parent,
               sample_per_category=n_per_category)
        return

    # * otherwise, follow normal processing
    verbose = args.verbose    
    output_dir = args.output_dir
    if not output_dir:
        output_dir = args.input_dir.parent.joinpath('3_dep_info')
    if not output_dir.is_dir():
        output_dir.mkdir()

    out_label = args.name
    if out_label is None:
        out_label = pd.Timestamp.now().strftime("%Y-%m-%d_%H:%M")
    if n_per_category is not None and args.test:
        ct_label = f'{out_label}-n{int(n_per_category*2)}'
        
    dep_df_save = output_dir.joinpath(out_label+'_deps.pkl.gz')

    # > only run `get_deps()` if no prior output exists
    if dep_df_save.is_file():
        print('Prior dep processing found. Loading from ',
              f'../{dep_df_save.relative_to(output_dir.parent)}...')
        df = pd.read_pickle(dep_df_save)
        
    #> process dataframe for dependency info
    else:
        # TODO: modify to process pickles individually, then concatonate. Means changing the `df_save_path` argument maybe?
        print('No prior dep processing found. Creating dependency string identifiers...')
        df = udf.concat_pkls(args.input_dir,
                             fname_glob=args.glob_expr,
                             verbose=True)
        if n_per_category is not None:
            df_sample = int(2*n_per_category)
            df = get_deps(df,
                          df_save_path=dep_df_save,
                          sample_size=df_sample,
                          verbose=verbose)
        else:
            
            df = get_deps(df,
                          df_save_path=dep_df_save,
                          verbose=verbose)

    ct_var(df, out_label=out_label,
           sample_per_category=n_per_category)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(textwrap.dedent('''\
                     For specified directory, find all `.pkl(.gz)` files and create dependency string identifiers for all rows. 
                     Then create crosstabulations for all dependency string variants by `hit_id` (default), or another specified column. 
        ''')),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--input_dir',
        type=Path,
        default='/share/compling/data/sanpi/2_hit_tables',
        help=(
            textwrap.dedent('''\
            path to directory containing pickle files to process for dependency relations
            default: '/share/compling/data/sanpi/2_hit_tables'
            '''))
    )

    parser.add_argument(
        '-d', '--dep_df',
        type=Path,
        default=None,
        help=(
            textwrap.dedent('''\
            path to already processed data (containing "dep_str..." columns
            '''))
    )

    parser.add_argument(
        '-g', '--glob_expr',
        type=str,
        default='*hits.pkl.gz',
        help=(textwrap.dedent('''\
              glob expression (str) for selecting files from given directory.
              ** HINT: 
                  to exclude `advadj` pattern matches, start glob expression with:
                    '*[!j]/' or '*[gd]/'
                  to only analyze `advadj` matches, start with: 
                    'advadj/' or '*j/'
              default: '*hits.pkl.gz'
              '''))
    )

    parser.add_argument(
        '-s', '--sample_size',
        type=int,
        default=None,
        help=(textwrap.dedent('''\
              option to produce sample crosstabulation with at most this number of hits per category.
              * When combined with `--test` option, will limit dataframe output to at most 2x this number.'''))
    )

    parser.add_argument(
        '-o', '--output_dir',
        type=Path,
        default='/share/compling/data/sanpi/3_dep_info',
        help=(
            textwrap.dedent('''\
            path to directory for output files
            default: '/share/compling/data/sanpi/3_dep_info'
            ''')),
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        default=None,
        help=(
            'option to give output data a specific name. if not supplied, date will be used')
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help=('print additional info')
    )

    parser.add_argument(
        '-t', '--test',
        action='store_true',
        default=False,
        help=('option to limit dataframe processing as well as crosstab output. will create sample of dataframe, rather than just giving a sample output for crosstabulation.')
    )
    # TODO: add argument for "cross column" in crosstabulate step
    # TODO: (?) add argument to run only dependency processing? or modify `get_deps` to run dataframes separately, then concatonate *after* adding dep_str columns?

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    _main()
    proc_t1 = pd.Timestamp.now()
    print('✔️ Analysis Completed --', pd.Timestamp.now().ctime())
    print(f'   total time elapsed: {ugen.dur_round ((proc_t1 - proc_t0).seconds)}')
