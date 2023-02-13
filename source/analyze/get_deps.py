# coding=utf-8
import multiprocessing as mp
import textwrap
from collections import namedtuple
from pathlib import Path

import pandas as pd
from analyze.utils.dataframes import (  # pylint: disable=import-error
    balance_sample, cols_by_str)
from analyze.utils.general import (  # pylint: disable=import-error
    display_message, dur_round, find_files, print_iter)

# pd.set_option('display.max_colwidth', 40)
# pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 100)

_DEP = namedtuple('dep_info', ['node', 'head_ix', 'head_lemma',
                               'target_ix', 'target_lemma', 'relation'])
_DATA_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
_FILEGLOB = 'exactly_nyt*hits.pkl.gz'
_DF_SAVE_DIR = _DATA_DIR.parent.joinpath('3_dep_info')
if not _DF_SAVE_DIR.is_dir():
    _DF_SAVE_DIR.mkdir()
_DF_SAVE_PATH = _DF_SAVE_DIR.joinpath(
    f'{_FILEGLOB.split("*",1)[0]}_deps.pkl.gz')

_TIE_STR = '>'
_BULLET = '+'

_LOGGER = mp.log_to_stderr()
_LOG_LEVEL = 30
# _LOGGER.setLevel(30)  # warning
# _LOGGER.setLevel(20)  # info
# _LOGGER.setLevel(10) # debug


def parallel_process_deps(args_df: pd.DataFrame,
                          log_level: int = _LOG_LEVEL):
    """process selected dataframes in parallel to add `dep_str...` columns.
       * does NOT return a dataframe object--only writes new dataframes to corresponding "out_path"

    Args:
        #// in_paths (iterable): paths for pickled hits dataframes in need of dependency processing
        #// out_paths (iterable): paths to save new dataframes to (with "dep_str(...)" columns added)
        paths_info (pd.DataFrame): dataframe with columns `input`, `by_hit`, and `by_node` indicating paths
        df_sample (int, optional): sample size (per pattern category) for dataframe (if any). Defaults to None.
        log_level (int, optional): integer indicating log level for multiprocessing log.
            Options are: 10 = DEBUG;
                         20 = INFO;
                         30 = WARNING;
                         40 = ERROR;
            Defaults to _LOG_LEVEL(=30=WARNING).
    """
    log_level = round(log_level, -1)
    mp.set_start_method('forkserver')
    _LOGGER.setLevel(log_level)

    # in order to pass the same value for each different input dataframe,
    #   create list of `df_sample` variable repeated to  match # of paths
    # // zip_sample = [df_sample] * len(in_paths)
    # // inputs = tuple(zip(in_paths, out_paths, zip_sample))
    input_count = len(args_df)
    # > set pool `processes` argument to
    # > (a) 1 less than the number of cpus
    # > OR
    # > (b) number of inputs to be processed
    # > OR
    # > (c) 15 cpus (don't want to be too ridiculous)
    # > whichever is less
    cpus = min(mp.cpu_count()-1, input_count, 15)
    print(f'\n## processing {input_count} inputs with {cpus} CPUs...')
    t0 = pd.Timestamp.now()

    with mp.Pool(processes=cpus) as pool:

        # NOTE: if process function takes more than 1 argument:
        #       use (a) snippet "expand_argument_inputs" and `imap(_unordered)`
        #       or  (b) `starmap` -> does not require printing step after, but slower
        results = tuple(
            pool.imap_unordered(
                _make_dep_dfs,
                (args_df.loc[i, :].squeeze() for i in args_df.index))
        )

        # zfill_len = len(str(file_count))
        # in_sz_w = 7
        # out_sz_w = 8
        # in_name_w = len(list(corpus_dir.glob('*conllu'))[0].stem)+1
        # print(('  task  |  time  \tin size\tout size\t'
        #         f'{"in data".ljust(in_name_w)}\t'
        #         ' out data\n'
        #         f' ------ | ------ \t'
        #         f'{"-"*in_sz_w}\t'
        #         f'{"-"*out_sz_w}\t'
        #         f'{"-"*in_name_w}\t'
        #         f'{"-"*40}'
        #         ).expandtabs(3))

        #! this is required to actually get the processes to run
        # ? Is there a better way to do this?
        # ^ Like, some "run" or "start" or "join" method?
        i = 0
        for result in results:
            i += 1
            input_header = f'## Input {i}'
            # dur, in_name, in_size, out_name, out_size = result
            # print((f'{str(i).zfill(zfill_len).center(8)}|{dur.rjust(7)} \t'
            #         f'{in_size.center(in_sz_w)}\t'
            #         f'{out_size.center(out_sz_w)}\t'
            #         f'{in_name.ljust(in_name_w)}\t'
            #         f'{out_name}').expandtabs(3))
            if not isinstance(result, (int, str, float)):
                try:
                    print_iter(iter_obj=result,
                               bullet=_BULLET,
                               header=input_header,
                               logger=_LOGGER)
                except TypeError:
                    display_message(result, _LOGGER)
                else:
                    continue

        # total_inputs_processed = i
        # print(total_inputs_processed, 'inputs processed')

    t1 = pd.Timestamp.now()
    dep_processing_info_lines = (
        f'Timestamp:{t1.strftime("%Y-%m-%d @ %I:%M%p")}',
        f'Total time elapsed: {dur_round((t1 - t0).seconds)}',
        f'Total dataframes processed: {input_count}',
        f'Total CPUs: {cpus}')
    print_iter(dep_processing_info_lines, bullet=_BULLET,
               header='## Parallel Processing Complete')
    print('----------------')

    return results


# // def _star_make_dep_dfs(zipped_args):
# //     return _make_dep_dfs(zipped_args)


def _make_dep_dfs(arg_series):
    _t0 = pd.Timestamp.now()
    dep_result = []
    # proc_t0 = time.perf_counter()
    # print(f'Time to perform process: {dur_round(proc_t1 - proc_t0)}')
    out_path = arg_series.by_hit
    if out_path.is_file() and out_path.stat().st_size > 0:
        dep_result.append('Prior dep processing found:'
                          + f'../{Path(*out_path.parts[-3:])}...',)

    else:
        sdf = pd.read_pickle(arg_series.input).assign(
            hits_df_path=arg_series.input)
        # * This wil only save processed dataframe to file (no returned df)
        dep_result = list(get_deps(hits_df=sdf,
                                   dep_hits_path=out_path,
                                   dep_node_path=arg_series.by_node,
                                   sample_size=arg_series.sample_size,
                                   run_in_parallel=True,
                                   verbose=False))

    _t1 = pd.Timestamp.now()
    # proc_t1 = time.perf_counter()
    dep_result.append(f'Total Time: {dur_round((_t1 - _t0).seconds)}')
    return dep_result


def get_deps(hits_df: pd.DataFrame,
             dep_hits_path: Path = None,
             dep_node_path: Path = None,
             sample_size: int = None,
             verbose: bool = False,
             run_in_parallel: bool = False):

    logger = _LOGGER if run_in_parallel else None
    _t0 = pd.Timestamp.now()
    input_path = hits_df.hits_df_path[0]
    if not dep_hits_path:
        no_save_warning = f'⚠️ Warning: No output path given. Processing for {input_path} will not be saved.'
        display_message(no_save_warning, logger, level=30)
    new_hits_df, all_nodes_df = _process_dep_info(
        hits_df, sample_size, verbose, run_in_parallel)
    _t1 = pd.Timestamp.now()

    dep_proc_time = dur_round((_t1 - _t0).seconds)
    if new_hits_df is None:

        overview_str = f"❗ERROR: Unparsable input data. No dependency processing completed for `{input_path}`"

    else:
        counts_md_table = (
            new_hits_df.loc[:, new_hits_df.columns.isin(
                ('dep_str', 'dep_str_mask', 'neg_lemma', 'colloc'))]
            #  ('hit_text', 'dep_str', 'dep_str_mask', 'neg_lemma', 'colloc'))]
            .value_counts().to_frame().rename(columns={0: 'count'})
            .sort_values('colloc').nlargest(5, 'count').reset_index()
            .to_markdown())
        input_name = input_path.name.rsplit("_", 1)[0]
        overview_str = f'\n### `{input_name}` Top 5\n{counts_md_table}'

        if verbose or run_in_parallel:
            print_df = new_hits_df.sample(5) if len(
                new_hits_df) > 5 else new_hits_df
            table_str = '\n' + print_df.loc[~print_df.dep_str.isna(),
                                            ['category', 'hit_text'] + cols_by_str(print_df, start_str='dep_str')].to_markdown()
            display_message(
                f'Time to create dep_str cols: {dep_proc_time}\n{table_str}', logger)

        if not dep_hits_path:
            no_save_warning = (f'No output path given for {input_name} data.' +
                               'Dataframe with dependency string identifiers for not saved.')
            display_message(no_save_warning, logger, 30)

        else:
            message = (f'writing `{input_name}` hits dataframe with added dependency string identifiers '
                       + f'to `{dep_hits_path}`...')
            display_message(message, logger)
            new_hits_df.to_pickle(dep_hits_path)

            message = (f'writing `{input_name}` dependency info indexed by individual node '
                       + f'to `{dep_node_path}`...')
            display_message(message, logger)
            all_nodes_df.to_pickle(dep_node_path)

            message_done = f'✔️ `{input_name}` dataframes saved. {pd.Timestamp.now().ctime()}'
            display_message(message_done, logger)

    display_message(f'`{input_name}` returning from processing...', logger)
    if run_in_parallel:
        return input_name, dep_proc_time, dep_hits_path, dep_node_path, overview_str
    else:
        display_message(overview_str, logger)
        return new_hits_df


def _process_dep_info(hits_df: pd.DataFrame,
                      sample_size: int = None,
                      verbose=False,
                      in_parallel=False):

    logger = _LOGGER if in_parallel else None
    input_path = hits_df.hits_df_path[0]
    if sample_size is not None:
        if len(hits_df) < sample_size:
            display_message(f'No sampling needed. Only 2 rows in ../{Path(*input_path.parts[-2:])} dataframe.',
                            logger, level=30)
        else:
            hits_df, sampling_info = balance_sample(
                hits_df, column_name='category',
                sample_per_value=sample_size, verbose=True)
            display_message((f'`{input_path.name}` dataframe limited '
                            + f'to at most {sample_size} per (pattern) category'),
                            logger, level=30)
            if verbose and not in_parallel:
                # if in_parallel, sampling_info will be uninformative
                # e.g.
                #   ## category representation in exactly_apw_with-relay_hits.pkl sample
                #   | category   |   count |   percentage |
                #   |:-----------|--------:|-------------:|
                #   | scoped     |       8 |          100 |
                display_message(sampling_info)

    dep_cols = cols_by_str(hits_df, start_str='dep_')
    too_flat = bool(cols_by_str(hits_df[dep_cols],
                                end_str=('node', 'contiguous', 'relation', 'head', 'target')))
    if too_flat:
        display_message(
            textwrap.dedent(f'''\
            ❗ Input dataframe `{input_path}` has wrong structure:
                Each node in hit should have only 1 column (e.g. `dep_mod`) in hits dataframe.
                Rerun pipeline on raw data, then try again.'''),
            logger, level=40)

        return None

    # labels = (c.split('_')[1] for c in dep_cols)
    logger = _LOGGER if in_parallel else None
    if verbose or in_parallel:
        print_iter(dep_cols,
                   bullet=_BULLET, logger=logger,
                   header=f'## original `{input_path.name}` dependency info columns')

    all_nodes_df = pd.DataFrame()
    # %%
    for hit_id in hits_df.index:
        row = hits_df.loc[hit_id, dep_cols]
        deps_in_hit = _process_deps_in_hit(row, verbose, in_parallel)
        # if error in processing hit, return None
        if deps_in_hit is None:
            return None
        # %%
        # > add string identifiers, with & without index, but sorted by index
        str_deps_df = _add_dep_strs(deps_in_hit)

        all_nodes_df = pd.concat(
            [all_nodes_df, str_deps_df.reset_index().set_index(['hit_id', 'index'])])
        # ^ alternatively, it can be turned into a dictionary and set as a column (below approach)
        # full_deps_info[ix] = hit_deps.transpose().to_dict()
        # by_hit_dep_df = pd.DataFrame().assign(
        #     # dep_info=pd.Series(full_deps_info),
        #     # dep_str_indexed=pd.Series(dep_ix_str).astype('string'),
        #     # dep_str=pd.Series(dep_str).astype('string'),
        #     dep_str_mask=pd.Series(dep_mask_str).astype('string'),
        #     # dep_tuple=pd.Series(dep_tuples)
        # )

        # * create series of all the dep strings combined (with `; `) for a hit.
        str_cols = cols_by_str(str_deps_df, start_str='dep_str')
        joined_strs = str_deps_df[str_cols].apply(
            lambda c: '; '.join(c), axis=0)  # pylint: disable=unnecessary-lambda
        hits_df.loc[hit_id, str_cols] = joined_strs

        if verbose and not in_parallel:
            print_iter(
                iter_obj=(
                    f'{x} ↣ {joined_strs[x]}' for x in joined_strs.index),
                bullet=_BULLET,
                header=f'⁂ Combined string representations of dependencies for match {hit_id}')
    if verbose or in_parallel:
        display_message(message=f'## New columns added to `{input_path.name}`\n'
                        + hits_df.loc[:, 'hits_df_path':].iloc[0,
                                                               :].to_markdown(),
                        logger=logger)

    #! namedtuple `dep_info` can't be pickled, so convert `dep_tuple` to dict type
    all_nodes_df = all_nodes_df.assign(
        dep_dict=all_nodes_df.dep_tuple.apply(lambda t: t._asdict()))
    all_nodes_df.pop('dep_tuple')
    return hits_df, all_nodes_df


def _process_deps_in_hit(row: pd.Series(dtype='object'),
                         verbose: bool = False,
                         in_parallel: bool = False):
    # ? is `fillna('n/a') necessary?`
    row = row.fillna('n/a')
    logger = _LOGGER if in_parallel else None
    if verbose or (in_parallel and logger.getEffectiveLevel() == 10):
        # log level for this info set to DEBUG
        print_iter((f'{x}\n    {row[x]}'
                   for x in row.index
                   if not isinstance(row[x], dict)),
                   bullet=_BULLET, logger=logger, level=10,
                   header=f'\n## row {row.name} non-dictionary values'
                   )
        print_iter((f'{x}\n{pd.Series(row[x])}\n'
                   for x in row.index
                   if isinstance(row[x], dict)),
                   bullet=_BULLET, logger=logger, level=10,
                   header=f'\n## row {row.name} non-dictionary values')
        display_message(row.to_markdown(), logger, level=10)

    deps_for_hit = pd.DataFrame()
    # ^ with multiple patterns concatenated, there will be NaN values for some "target" cols.
    # ? Is it better to simply skip those, or include them with empty values?
    for dep_col in row.index:
        # label = dep_col.split('_')[1]

        # > first trying it with a simple `continue`... 🤞
        if row[dep_col] == 'n/a':
            continue
        try:
            dep_df = pd.json_normalize(row[dep_col], sep='_')
        except NotImplementedError:
            display_message(('❗ `pd.json_normalize()` in `get_deps._process_deps_in_hit()` failed on:\n'
                            + row[[dep_col]].to_markdown()),
                            logger, level=40)
            return None

        deps_for_hit = pd.concat([deps_for_hit, dep_df], ignore_index=True)

    deps_for_hit = deps_for_hit.assign(hit_id=row.name).convert_dtypes()

    deps_for_hit = deps_for_hit.assign(
        dep_tuple=deps_for_hit.apply(_get_dep_tuples, axis=1))

    return deps_for_hit


def _get_dep_tuples(_df):
    row = _df[['node', 'head_ix', 'head_lemma',
               'target_ix', 'target_lemma', 'relation']].squeeze()
    ix_cols = ['head_ix', 'target_ix']
    row[ix_cols] = row[ix_cols].astype('string').str.zfill(2)
    return _DEP._make(row)


def _add_dep_strs(deps_in_hit: pd.DataFrame,
                  verbose: bool = False):

    str_deps_df = deps_in_hit.assign(

        dep_str=deps_in_hit.dep_tuple.apply(
            lambda x: (f"{x.head_lemma}{_TIE_STR}"
                       f"{x.target_lemma}[={x.node}]")
        ).fillna('').astype('string'),

        dep_str_ix=deps_in_hit.dep_tuple.apply(
            lambda x: (f"{x.head_ix}:{x.head_lemma}{_TIE_STR}"
                       f"{x.target_ix}:{x.target_lemma}[={x.node}]")
        ).fillna('').astype('string')
    )

    str_deps_df = str_deps_df.assign(
        dep_str_full=str_deps_df[
            ['dep_str_ix', 'relation']].apply(_add_relation, axis=1),
        dep_str_rel=str_deps_df[
            ['dep_str', 'relation']].apply(_add_relation, axis=1)
    )

    str_deps_df.iloc[:, -6:].squeeze()

    # %%
    index_cols = ['target_ix', 'head_ix']

    str_deps_df[index_cols] = str_deps_df[
        index_cols].apply(pd.to_numeric, downcast='unsigned')

    str_deps_df = str_deps_df.sort_values(index_cols).reset_index(drop=True)

    str_deps_df = str_deps_df.assign(dep_str_mask=_mask_dep_str(str_deps_df))

    str_deps_df = str_deps_df.assign(
        dep_str_mask_rel=str_deps_df[
            ['dep_str_mask', 'relation']].apply(_add_relation, axis=1))

    try:
        debug = _LOGGER.getEffectiveLevel() == 10
    except AttributeError:
        logger = None
        debug = False
    else:
        logger = _LOGGER

    if verbose or debug:
        dep_str_table = (
            str_deps_df[cols_by_str(str_deps_df, start_str='dep_str')]
            .to_markdown())
        display_message(
            f'`{str_deps_df.hit_id[0]}`\n{dep_str_table}', logger, level=10)

    return str_deps_df


def _mask_dep_str(str_df: pd.DataFrame):

    # * for mod, use both xpos
    # * for relay, use both xpos
    if 'node' not in str_df.columns:
        print('Error: "node" column is not set.')
        return str_df.assign(dep_str_mask='').dep_str_mask

    # > this one doesn't need an existence check because `mod` always exists
    # > but doing it anyway, in case that changes 🤷‍♀️
    is_mod_or_relay = str_df.node.isin(('mod', 'relay'))
    if any(is_mod_or_relay):
        str_df.loc[is_mod_or_relay, 'dep_str_mask'] = (
            str_df.loc[is_mod_or_relay, 'head_xpos']
            + _TIE_STR
            + str_df.loc[is_mod_or_relay, 'target_xpos'])

    # * for neg, use target_lemma and head_xpos (keep neg token)
    is_neg = str_df.node == 'neg'
    if any(is_neg):
        str_df.loc[is_neg, 'dep_str_mask'] = (
            str_df.loc[is_neg, 'head_xpos']
            + _TIE_STR
            + str_df.loc[is_neg, 'target_lemma'])

    # * for negraise, use target_xpos and head_lemma (keep NR token)
    is_raised = str_df.node == 'negraise'
    if any(is_raised):
        str_df.loc[is_raised, 'dep_str_mask'] = (
            str_df.loc[is_raised, 'head_lemma']
            + _TIE_STR
            + str_df.loc[is_raised, 'target_xpos'])

    return str_df.dep_str_mask


def _add_relation(_row):
    _str = _row.fillna('').iloc[0]
    if not (_str and isinstance(_str, str)):
        return ''

    _relation = _row.iloc[1]
    # opt_hyphen = '-' if '-' in _TIE_STR else ''
    # return _str.replace(_TIE_STR, f'{opt_hyphen}[{_relation}]{_TIE_STR}')
    return _str.replace(_TIE_STR, f'{_TIE_STR}[{_relation}]{_TIE_STR}')


# %%
if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    df = pd.concat(find_files(_DATA_DIR, _FILEGLOB, True))
    df = get_deps(df, _DF_SAVE_PATH)
    proc_t1 = pd.Timestamp.now()
    print(
        f'Time to get dependency identifier strings: {dur_round((proc_t1 - proc_t0).seconds)}')


#################################################################
# # %%
# # can save this here, or call crosstab method directly
# # df.to_pickle(f'/share/compling/data/sanpi/2_hit_tables/{_FILEGLOB.split("*")[0]}_dep.pkl.gz')
# # df = pd.read_pickle(
# #     f'{_DATA_DIR}{_FILEGLOB.split("*")[0]}_dep.pkl.gz')

# # * Crosstabulate Dependency Strings
# # * (1) `hit_id`
# # TODO: add arg for cross-column to crosstabulate method
# ct_hit_id = ct_var(df)
# boolean_hits = ct_hit_dep.loc[ct_hit_dep.index != 'All',
#                               ct_hit_dep.columns != 'All'].astype('boolean')

# # %% [markdown]
# # I think it may be interesting to see a crosstabulation of the dependency paths with the exact lemmas collapsed.
# # For example, instead of `'standard>not_neg; standard>exactly_mod'`, have a series of `'ADJ>not_neg; ADJ>ADV_mod'`
# # and crosstabulate that with the collocations (i.e. the `ADJ` and `ADV` token lemmas)
# #
# # - [x] added this as `dep_str_mask`

# # %%
# ct_colloc_mask = pd.crosstab(df.colloc, df.dep_str_mask, margins=True)
# ct_colloc_mask
# # %%
# df = df.assign(neg_lemma=df.neg_lemma.str.lower()
#                ).loc[df.adv_lemma == 'exactly', :]
# df.groupby('dep_str_mask')['colloc', 'dep_str'].value_counts()

# # %%
# ct_mask_colloc = pd.crosstab(df.dep_str_mask, df.colloc,  margins=True)
# ct_mask_colloc
# # %%
