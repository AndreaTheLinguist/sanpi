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
from analyze.get_deps import (  # pylint: disable=import-error
    parallel_process_deps)
from analyze.utils import dataframes as udf  # pylint: disable=import-error
from analyze.utils import general as ugen  # pylint: disable=import-error
SAMPLE_LEN_MULTIPLY = 1.5

def _main():
    _t0 = pd.Timestamp.now()
    args = _parse_args()
    verbose = args.verbose

    dep_args_df = _get_dep_args(args)

    #// if any(dep_args_df.by_hit.apply(lambda p: not p.is_file())):
    if args.very_verbose: 
        log_level = 10 
    elif verbose: 
        log_level = 20
    else: 
        log_level = 30
    parallel_process_deps(dep_args_df, log_level)

    # to get debug messages:
    # parallel_process_deps(in_sdf_paths, out_sdf_paths, df_sample, log_level=10)

    # * concatonate dataframes with deps processing
    dfs_with_dep_paths = dep_args_df.by_hit.to_list()
    df = udf.concat_pkls(pickles=dfs_with_dep_paths,
                         verbose=verbose, 
                         convert_dtypes=True)  # pylint: disable=invalid-name
    
    df = _optimize_df(df)

    _t1 = pd.Timestamp.now()
    print(f'\n   total time elapsed: `{udf.get_proc_time(start=_t0, end=_t1)}`')


def _optimize_df(df:pd.DataFrame): 
    
    print('Original Dataframe:')
    df.info(memory_usage='deep')
    
    # * clean up dataframe a bit
    #> drop unneeded string columns
    #// for c in udf.cols_by_str(df, start_str=('context', 'text', 'sent_text', 'token')):
    #//     df.pop(c)
    df.drop(
        udf.cols_by_str(df, start_str=('context', 'text', 'sent_text', 'token')), 
        axis=1, inplace=True)
    
    #> select only non-`object` dtype columns
    relevant_cols = df.columns[~df.dtypes.astype('string').str.endswith(('object'))]
    
    #> limit df to `relevant_cols`
    df = df[relevant_cols]
    
    #> create empty dataframe with `relevant_cols` as index/rows
    df_info = pd.DataFrame(index=relevant_cols)

    df_info = df_info.assign(
        mem0=df.memory_usage(deep=True),
        dtype0=df.dtypes.astype('string'),
        defined_values=df.count(),
        unique_values=df.nunique())
    df_info = df_info.assign(
        ratio_unique = (df_info.unique_values/df_info.defined_values).round(2))

    cat_candidates = df_info.loc[df_info.ratio_unique < 0.8, :].loc[df_info.dtype0!='category'].index.to_list()
    #// catted_df = udf.make_cats(df.copy(), cat_candidates)
    df[cat_candidates] = df[cat_candidates].astype('category')
    
    #// df_info = df_info.assign(dtype1=catted_df.dtypes, mem1=catted_df.memory_usage(deep=True))
    df_info = df_info.assign(dtype1=df.dtypes, mem1=df.memory_usage(deep=True))
    df_info = df_info.assign(mem_change= df_info.mem1-df_info.mem0)
    print(df_info.sort_values(['mem_change', 'ratio_unique', 'dtype0']).to_markdown())
    mem_improved = df_info.loc[df_info.mem_change < 0, :].index.to_list()
    for c in df.columns[~df.columns.isin(mem_improved)]: 
        print(c, '\t', df.loc[:, c].dtype)
    #// df.loc[:, mem_improved] = catted_df.loc[:, mem_improved]
    print('Category Converted dataframe:')
    df.info(memory_usage='deep')
    
    return df


def _get_dep_args(args):
    
    #> identify input paths
    input_paths = _identify_input_paths(args)
    
    #> set `dep_info_dir` (output dataframes with subdir for `crosstab` tables)
    dep_info_dir = _set_dep_info_dir(args)
    
    #> set sample size for (test) dataframe with dependency identifier strings
    n_sample_rows = _set_n_sample_rows(args, input_paths)
    
    # > generate output paths for each input and format as dataframe
    paths_df = _generate_output_paths(input_paths, dep_info_dir, n_sample_rows)
    
    if args.verbose: 
        _print_paths(paths_df)
    
    return paths_df.assign(
        sample_size = pd.to_numeric([n_sample_rows] *len(paths_df),
                                    downcast='unsigned'),
        verbose = args.verbose,
        )


def _identify_input_paths(args):
    input_paths = tuple(
        p.resolve() for p in ugen.find_files(data_dir=args.input_dir,
                                   fname_glob=args.glob_expr)
        if '.pkl' in p.suffixes)
    if not input_paths:
        sys_exit('No input files found. Exiting.')
    return input_paths

def _set_dep_info_dir(args):
    dep_info_dir = args.output_dir
    if not dep_info_dir.relative_to(args.input_dir.parent.parent):
        dep_info_dir = args.input_dir.parent.joinpath('3_dep_info')
    if not dep_info_dir.is_dir():
        dep_info_dir.mkdir()
    return dep_info_dir

def _set_n_sample_rows(args, input_paths):
    n_sample_rows = args.sample_size if args.test else 0
    if n_sample_rows < 0:
        n_sample_rows = min(len(pd.read_pickle(i)) for i in input_paths)
    n_sample_rows = int(SAMPLE_LEN_MULTIPLY * n_sample_rows)
    return n_sample_rows

def _generate_output_paths(input_paths, dep_info_dir, n_sample_rows):
    sample_tag = f'[n{n_sample_rows}]' if n_sample_rows else ''
    return pd.DataFrame(gen_out_paths(input_paths, dep_info_dir, sample_tag))


def _print_paths(args_df):

    args_df.index = [Path(p).name.split('.', 1)[0] for p in args_df.input]
    print_df = args_df.applymap(lambda p: Path(*Path(p).parts[-3:]))
    
    udf.print_md_table(
        print_df.transpose(), 
        title='## Dependency Processing Path Info ##')
    
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
        #     ↪ exactly_puddin_with-relay_hits[n40]
        df_stem_prefix = input_path.name.split('.', 1)[0] + sample_tag

        # exactly_puddin_with-relay_hits[n40]+deps.pkl.gz)
        hit_df_path = df_save_dir.joinpath(df_stem_prefix + '+deps.pkl.gz')

        # exactly_puddin_with-relay_hits[n40]_dep-node-info.pkl.gz
        node_df_path = df_save_dir.joinpath(
            df_stem_prefix + '_dep-node-info.pkl.gz')
        if not df_save_dir.is_dir():
            df_save_dir.mkdir(parents=True)
        yield path_tuple(input_path, hit_df_path, node_df_path)


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
        '-V', '--very_verbose',
        action='store_true',
        default=False,
        help=('print additional info')
    )

    parser.add_argument(
        '-t', '--test',
        action='store_true',
        default=False,
        help=('option to limit dataframe processing as well as crosstab output. '
              'will create sample of dataframe, rather than just using sample for `crosstab()`.'
              '`--sample_size` requires the `--test` option to take effect.')
    )

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
