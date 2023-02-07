# coding=utf-8
import argparse
from pathlib import Path
import textwrap

import pandas as pd
from analyze.crosstab_deps import crosstabulate_variants as ct_var
from analyze.get_deps import make_dep_dfs, parallel_process_deps
from analyze.utils import dataframes as udf
from analyze.utils import general as ugen


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
    deps_dir = args.output_dir
    out_label = args.name
    df_sample = None
    sample_tag = ''

    if not deps_dir.parent.is_dir():
        deps_dir = args.input_dir.parent.joinpath('3_dep_info')

    if out_label is None:
        out_label = pd.Timestamp.now().strftime("%Y-%m-%d_%H:%M")
    if n_per_category is not None and args.test:
        sample_tag = f'n{int(n_per_category*2)}'
        out_label = f'{out_label}-{sample_tag}'

        # > used below
        df_sample = int(2*n_per_category)

    # out_dir = deps_dir.joinpath(out_label)
    # if not out_dir.is_dir():
    #     out_dir.mkdir(parents=True)
    # TODO: test this!!
    # *** trying new approach: run get_deps() on individual files
    df_file_suffix = f'_{sample_tag}deps.pkl.gz'
    # all_deps_df_save = out_dir.joinpath(out_label+df_file_suffix)
    in_sdf_paths = tuple(
        p for p in ugen.find_files(data_dir=args.input_dir,
                                   fname_glob=args.glob_expr)
        if '.pkl' in p.suffixes)
    out_sdf_paths = tuple(_get_save_path(p, deps_dir, df_file_suffix)
                          for p in in_sdf_paths)
    if verbose:
        print('Corresponding Paths for dependency processed dataframes:')
        ugen.print_iter(out_sdf_paths)

    # # TODO: employ multiprocessing here
    # for zipped in zip(in_sdf_paths, out_sdf_paths):
    #     _in_path, _out_path = zipped
    #     make_dep_dfs(_in_path, _out_path, df_sample)
    parallel_process_deps(in_sdf_paths, out_sdf_paths, df_sample)
    df = udf.concat_pkls(pickles=out_sdf_paths, verbose=verbose)

    # // # * only run `get_deps()` if no prior output exists
    # // if dep_df_save.is_file():
    # // print('Prior dep processing found. Loading from ',
    # //       f'../{dep_df_save.relative_to(deps_dir.parent)}...')
    # // df = pd.read_pickle(dep_df_save)

    # // # * process dataframe for dependency info
    # // else:
    # // # TODO: modify to process pickles individually, then concatonate. Means changing the `df_save_path` argument maybe?
    # // print('No prior dep processing found. Creating dependency string identifiers...')
    # // df = udf.concat_pkls(args.input_dir,
    # //                      fname_glob=args.glob_expr,
    # //                      verbose=True)

    # // df = get_deps(df,
    # //               df_save_path=dep_df_save,
    # //               sample_size=df_sample,
    # //               verbose=verbose)
    print('## Crosstabulate by `hit_id`')
    ct_var(df, out_label=out_label,
           sample_per_category=n_per_category)

# > moved to get_deps.py
# def make_dep_dfs(zipped):
#     in_path, out_path, df_sample = zipped
#     if out_path.is_file() and out_path.stat().st_size > 0:
#         print('Prior dep processing found:',
#                     f'../{Path(*out_path.parts[-3:])}...')

#     else:
#         sdf = pd.read_pickle(in_path)
#             # * This wil only save processed dataframe to file (no returned df)
#         get_deps(df=sdf,
#                         df_save_path=out_path,
#                         sample_size=df_sample,
#                         return_df=False,
#                         verbose=False)


def _get_save_path(pkl_path, out_dir, fname_suffix):
    sdf_save_path = (
        out_dir
        .joinpath(pkl_path.parent.name)
        .joinpath(
            # exactly_puddin_with-relay_hits.pkl.gz
            # ↪ exactly_puddin_with-relay_hits
            #    ↪ exactly_puddin_with-relay
            #       ↪ exactly_puddin_with-relay_deps.pkl.gz)
            pkl_path.name.split('.')[0].replace('_hits', '')
            + fname_suffix)
    )
    if not sdf_save_path.parent.is_dir():
        sdf_save_path.parent.mkdir()

    return sdf_save_path


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
    if '.pkl' not in args.glob_expr:
        print(
            f'⚠️ Warning: search string (glob expression) {args.glob_expr} not explicitly restricted to ".pkl" formats. May lead to errors.')
    return args


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    _main()
    proc_t1 = pd.Timestamp.now()
    print('## ✔️ Analysis Completed')
    print(pd.Timestamp.now().ctime())
    print('\n   total time elapsed: ',
          ugen.dur_round((proc_t1 - proc_t0).seconds))
