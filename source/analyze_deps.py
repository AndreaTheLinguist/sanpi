"""generate crosstabulations of hit dependencies by hit_id or other attributes
    #TODO: finish description?
    Returns:
        _type_: _description_
    """
# coding=utf-8
import argparse
import textwrap
from collections import namedtuple
from pathlib import Path
from sys import exit as sys_exit

import pandas as pd
from analyze.crosstab_deps import (  # pylint: disable=import-error
    crosstabulate_variants)
from analyze.get_deps import (  # pylint: disable=import-error
    parallel_process_deps)
from analyze.utils import dataframes as udf  # pylint: disable=import-error
from analyze.utils import general as ugen  # pylint: disable=import-error


def _main():
    args = _parse_args()
    n_per_category = args.sample_size
    # * if path to processed df given, jump straight to crosstab and pull output info from input path
    if args.dep_df:
        input_path = args.dep_df

        # > should drop "_deps.pkl.gz" and keep whatever precedes it
        ct_label = input_path.name.rsplit('_', 1)[-1]
        # > default is now `0`, so will always be defined
        if n_per_category > 0:
            ct_label = f'{ct_label}-n{n_per_category}'
        elif n_per_category < -1:
            ct_label = f'{ct_label}-min'

        crosstabulate_variants(df=pd.read_pickle(input_path),
                               out_label=ct_label,
                               dep_dir=input_path.parent,
                               n_per_category=n_per_category)
        return

    # * otherwise, follow normal processing
    verbose = args.verbose

    # *** trying new approach: run get_deps() on individual files
    # all_deps_df_save = out_dir.joinpath(out_label+df_file_suffix)
    # if verbose:
    #     print('## File Processing Info')

    dep_args_df = _get_dep_args(args)
    # _gen_path_info yields _PATH_INFO namedtuple
    # create dataframe from generator of these namedtuples for each input path

    if any(dep_args_df.by_hit.apply(lambda p: not p.is_file())):
        log_level = 20 if verbose else 30
        parallel_process_deps(dep_args_df, log_level)

    # to get debug messages:
    # parallel_process_deps(in_sdf_paths, out_sdf_paths, df_sample, log_level=10)

    # * concatonate dataframes with deps processing
    dfs_with_dep_paths = dep_args_df.by_hit.to_list()
    df = udf.concat_pkls(pickles=dfs_with_dep_paths,
                         verbose=verbose, 
                         convert_dtypes=True)  # pylint: disable=invalid-name
    
    df = _optimize_df(df)
    
    # * run crosstabulation code
    df_fname = dfs_with_dep_paths[0].name
    if '[' in df_fname:
        df_sample_tag = f"[{df_fname.split('[', 1)[1].split(']',1)[0]}]"
    else:
        df_sample_tag = ''
    ct_out_label = _get_crosstab_label(args.name, df_sample_tag)

    crosses = ('hit_id', 'colloc_id', 'colloc', 'category',
               'dep_str_mask', 'neg_lemma', 'adj_lemma')
    for cross_col in crosses:
        print(f'## Crosstabulating by `{cross_col}`')
        proc_t0 = pd.Timestamp.now()

        crosstabulate_variants(
            df=df,
            cross=cross_col,
            out_label=ct_out_label,
            n_per_category=n_per_category,
            dep_dir=dfs_with_dep_paths[0].parent.parent)

        proc_t1 = pd.Timestamp.now()
        print(
            f'\n   total time elapsed: `{ugen.dur_round((proc_t1 - proc_t0).seconds)}`')


def _optimize_df(df:pd.DataFrame): 
    
    print('Original Dataframe:')
    df.info(memory_usage='deep')
    
    # * clean up dataframe a bit
    # drop unneeded string columns
    for c in udf.cols_by_str(df, start_str=('context', 'text', 'sent_text', 'token')):
        df.pop(c)
    # select only non-`object` dtype columns
    relevant_cols = df.columns[~df.dtypes.astype(
        'string').str.endswith(('object'))]
    # limit df to `relevant_cols`
    df = df[relevant_cols]
    # create empty dataframe with `relevant_cols` as index/rows
    df_info = pd.DataFrame(index=relevant_cols)

    df_info = df_info.assign(
        mem0=df.memory_usage(deep=True),
        dtype0=df.dtypes.astype('string'),
        defined_values=df.count(),
        unique_values=df.apply(pd.unique, axis=0).apply(len))
    df_info = df_info.assign(
        ratio_unique = (df_info.unique_values/df_info.defined_values).round(2))

    cat_candidates = df_info.loc[df_info.ratio_unique < 0.8, :].loc[df_info.dtype0!='category'].index.to_list()
    catted_df = udf.make_cats(df.copy(), cat_candidates)
    
    df_info = df_info.assign(dtype1=catted_df.dtypes, mem1=catted_df.memory_usage(deep=True))
    df_info = df_info.assign(mem_change= df_info.mem1-df_info.mem0)
    print(df_info.sort_values(['mem_change', 'ratio_unique', 'dtype0']).to_markdown())
    mem_improved = df_info.loc[df_info.mem_change < 0, :].index.to_list()
    for c in df.columns[~df.columns.isin(mem_improved)]: 
        print(c, '\t', df.loc[:, c].dtype)
    df.loc[:, mem_improved] = catted_df.loc[:, mem_improved]
    print('Category Converted dataframe:')
    df.info(memory_usage='deep')
    
    return df


def _get_dep_args(args):

    # * identify input paths
    input_paths = tuple(
        p for p in ugen.find_files(data_dir=args.input_dir,
                                   fname_glob=args.glob_expr)
        if '.pkl' in p.suffixes)
    if not input_paths:
        sys_exit('No input files found. Exiting.')

    # * set `dep_info_dir` (output dataframes with subdir for `crosstab` tables)
    dep_info_dir = args.output_dir
    if not dep_info_dir.relative_to(args.input_dir.parent.parent):
        dep_info_dir = args.input_dir.parent.joinpath('3_dep_info')
    if not dep_info_dir.is_dir():
        dep_info_dir.mkdir()

    # * set sample size for (test) dataframe with dependency identifier strings
    # > if test dataframe is to be created, use given sample size
    df_sample = args.sample_size if args.test else 0
    # > if sample size is negative, get minimum length across all selected input dataframes
    if df_sample < 0:
        df_sample = min(len(pd.read_pickle(i)) for i in input_paths)
    # > multiply by 2 for sample size of test dataframe
    df_sample = int(2 * df_sample)

    sample_tag = f'[n{df_sample}]' if df_sample else ''

    # * generate output paths for input paths and convert to dataframe
    paths_df = pd.DataFrame(gen_out_paths(
        input_paths, dep_info_dir, sample_tag))

    if args.verbose:
        print_paths = paths_df.assign(
            dataset=paths_df.input.apply(lambda p: Path(p).name.split('.', 1)[0]))
        print_paths = print_paths.set_index('dataset')
        for i in print_paths.index:
            row = print_paths.loc[i, :]
            row = row.apply(lambda p: Path(*p.parts[-3:])) # type: ignore
            print_paths.loc[i, :] = row
        print('\n## Dependency Processing Path Info\n'
              + print_paths.transpose().to_markdown())

    args_df = paths_df.assign(sample_size=df_sample)
    return args_df


def gen_out_paths(input_paths, dep_info_dir, sample_tag):

    path_tuple = namedtuple('path_info', ['input', 'by_hit', 'by_node'])

    for input_path in input_paths:
        df_save_dir = (
            # ../3_dep_info/
            dep_info_dir
            # ../2_hit_tables/scoped/exactly_puddin_with-relay_hits.pkl.gz
            # ↪ scoped
            #     ↪ ../3_dep_info/scoped
            .joinpath(input_path.parent.name))
        # exactly_puddin_with-relay_hits.pkl.gz
        # ↪ exactly_puddin_with-relay_hits
        #   ↪ exactly_puddin_with-relay_hits[n40]
        df_stem_prefix = input_path.name.split('.', 1)[0] + sample_tag

        # exactly_puddin_with-relay_hits[n40]+deps.pkl.gz)
        hit_df_path = df_save_dir.joinpath(df_stem_prefix + '+deps.pkl.gz')

        # exactly_puddin_with-relay_hits[n40]_dep-node-info.pkl.gz
        node_df_path = df_save_dir.joinpath(
            df_stem_prefix + '_dep-node-info.pkl.gz')
        if not df_save_dir.is_dir():
            df_save_dir.mkdir(parents=True)
        yield path_tuple(input_path, hit_df_path, node_df_path)


def _get_crosstab_label(name, df_sample_label=None):
    ct_out_label = (name if name
                    else pd.Timestamp.now().strftime("%Y-%m-%d_%H:%M"))
    sample_tag = df_sample_label if df_sample_label else ''
    ct_out_label += sample_tag

    return ct_out_label


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
        # Note: changed from None to 0 to make tests easier
        default=0,
        help=(
            textwrap.dedent('''\
                Option to produce sample crosstabulation with at most this number of hits per category.
                * When combined with `--test` option, 
                  this will limit dataframe output to at most **2x** this number.
                '''))
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
        help=('option to limit dataframe processing as well as crosstab output. '
              'will create sample of dataframe, rather than just using sample for `crosstab()`.')
    )
    # TODO: add argument for "cross column" in crosstabulate step
    # ^ (?) add argument to run only dependency processing?
    # ^ or modify `get_deps` to run dataframes separately,
    # ^     then concatonate *after* adding dep_str columns?

    args = parser.parse_args()
    if '.pkl' not in args.glob_expr:
        print(f'⚠️ Warning: search string (glob expression) {args.glob_expr}',
              'not explicitly restricted to ".pkl" formats. May lead to errors.')
    return args


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    _main()
    proc_t1 = pd.Timestamp.now()
    print('## ✔️ Analysis Completed')
    print(pd.Timestamp.now().ctime())
    print('\n   total time elapsed: ',
          ugen.dur_round((proc_t1 - proc_t0).seconds))
