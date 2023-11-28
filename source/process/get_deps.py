# coding=utf-8
import multiprocessing as mp
import textwrap
from collections import namedtuple
from pathlib import Path

import pandas as pd
from utils.dataframes import (  # pylint: disable=import-error
    balance_sample, cols_by_str, print_md_table)
from utils.general import (  # pylint: disable=import-error
    display_message, dur_round, find_files, print_iter)

# pd.set_option('display.max_colwidth', 40)
# pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 100)

_DEP = namedtuple('dep_info',
                  ['tie', 'pattern', 'relation',
                   'head_node', 'head_ix', 'head_form', 'head_lemma',
                   'target_node', 'target_ix', 'target_form', 'target_lemma'])
_DATA_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
_FILEGLOB = 'bigram*hits.pkl.gz'
_DF_SAVE_DIR = _DATA_DIR.parent.joinpath('3_dep_info')
if not _DF_SAVE_DIR.is_dir():
    _DF_SAVE_DIR.mkdir()
_DF_SAVE_PATH = _DF_SAVE_DIR.joinpath(
    f'{_FILEGLOB.split("*",1)[0]}_deps.pkl.gz')

_DELIM_STR = '>'
_BULLET = '+'

_DEBUG = 10
_INFO = 20
_WARNING = 30
_ERROR = 40

_LOGGER = mp.log_to_stderr()
_LOG_LEVEL = _WARNING
# _LOGGER.setLevel(30)  # warning
# _LOGGER.setLevel(20)  # info
# _LOGGER.setLevel(10) # debug


def parallel_process_deps(args_df: pd.DataFrame,
                          log_level: int = _LOG_LEVEL):
    """process selected dataframes in parallel to add `dep_str...` columns.
       * does NOT return a dataframe object--only writes new dataframes to corresponding "out_path"

    Args:
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

    input_count = len(args_df)
    # > set pool `processes` argument to
    # > (a) 1 less than the number of cpus
    # > OR
    # > (b) number of inputs to be processed
    # > OR
    # > (c) 15 cpus (don't want to be too ridiculous)
    # > whichever is less
    cpus = min(mp.cpu_count()-1, input_count, 15)
    #// #!#HACK the slurm requests don't seem to be working....
    #// cpus=2
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


def _make_dep_dfs(arg_series):
    _t0 = pd.Timestamp.now()
    out_path = arg_series.by_hit
    dep_result = []
    if out_path.is_file() and out_path.stat().st_size > 0:
        dep_result.append(
            f'Prior dep processing found:../{Path(*out_path.parts[-3:])}...'
        )

    else:
        sdf = pd.read_pickle(arg_series.input)
        sdf['hits_df_path'] = arg_series.input
        # * This wil only save processed dataframe to file (no returned df)
        dep_result = list(get_deps(hits_df=sdf,
                                   dep_hits_path=out_path,
                                   dep_tie_path=arg_series.by_node,
                                   sample_size=arg_series.sample_size,
                                   run_in_parallel=True,
                                   verbose=arg_series.verbose))

    _t1 = pd.Timestamp.now()
    dep_result.append(f'Total Time: {dur_round((_t1 - _t0).seconds)}')
    return dep_result


def _save_outputs(input_name, dep_hits_path, new_hits_df, dep_tie_path, all_ties_df):
    def save_df(_df, path, description):
        message = f'writing `{input_name}` {description} to `{path}`...'
        display_message(
            message, _LOGGER if _LOGGER.getEffectiveLevel == _INFO else None)
        _df.to_pickle(path)

    save_df(new_hits_df, dep_hits_path,
            'hits dataframe with added dependency string identifiers')
    save_df(all_ties_df, dep_tie_path,
            'dependency info indexed by individual tie')


def get_deps(hits_df: pd.DataFrame,
             dep_hits_path: Path = None,
             dep_tie_path: Path = None,
             sample_size: int = 0,
             verbose: bool = False,
             run_in_parallel: bool = False):

    logger = _LOGGER if run_in_parallel else None
    _t0 = pd.Timestamp.now()
    input_path = hits_df.hits_df_path[0]
    if not dep_hits_path:
        no_save_warning = f'⚠️ Warning: No output path given. Processing for {input_path} will not be saved.'
        display_message(no_save_warning, logger, level=_WARNING)
    new_hits_df, all_ties_df = _process_dep_info(
        hits_df, sample_size, verbose, run_in_parallel)
    _t1 = pd.Timestamp.now()

    dep_proc_time = dur_round((_t1 - _t0).seconds)
    input_name = input_path.name.rsplit("_", 1)[0]
    display_message(f'`{input_name}` returning from processing...', logger)
    if new_hits_df is None:

        overview_str = f"❗ERROR: Unparsable input data. No dependency processing completed for `{input_path}`"
        display_message(overview_str, logger, _ERROR)

    else:
        counts_md_table = print_md_table(
            new_hits_df.loc[:, new_hits_df.columns.isin(
                ('dep_str', 'dep_str_mask', 'neg_lemma', 'colloc'))]
            # ('hit_text', 'dep_str', 'dep_str_mask'))]
            .value_counts().to_frame().rename(columns={0: 'count'})
            .sort_values('colloc').nlargest(5, 'count').reset_index(),
            suppress=True)
        overview_str = f'\n### `{input_name}` Top 5\n{counts_md_table}'

        if verbose or run_in_parallel:
            print_df = new_hits_df.sample(5) if len(
                new_hits_df) > 5 else new_hits_df
            table_str = '\n' + print_df.loc[~print_df.dep_str.isna(),
                                            ['category', 'hit_text'] + cols_by_str(print_df, start_str='dep_str')].to_markdown()
            display_message(
                f'Time to create dep_str cols: {dep_proc_time}\n{table_str}', logger)

        if not dep_hits_path:
            no_save_warning = f'No output path given for {input_name} data.Dataframe with dependency string identifiers for not saved.'
            display_message(no_save_warning, logger, 30)

        else:
            _save_outputs(input_name, dep_hits_path,
                          new_hits_df, dep_tie_path, all_ties_df)

            message_done = f'✓ `{input_name}` dataframes saved. {pd.Timestamp.now().ctime()}'
            display_message(message_done, logger)

    if run_in_parallel:
        return input_name, dep_proc_time, dep_hits_path, dep_tie_path, overview_str

    display_message(overview_str, logger)
    return new_hits_df


def _process_dep_info(hits_df: pd.DataFrame,
                      sample_size: int = 0,
                      verbose=False,
                      in_parallel=False):

    logger = _LOGGER if in_parallel else None
    input_path = hits_df.hits_df_path[0]
    if sample_size:
        sample_size = max(sample_size, 2)
        if len(hits_df) < sample_size > 0:
            display_message(
                f'No sampling needed (N={sample_size}). Only {len(hits_df)} rows in ../{Path(*input_path.parts[-2:])} dataframe.',
                logger,
                level=_WARNING,
            )
        else:
            hits_df, sampling_info = balance_sample(
                hits_df, column_name='pattern',
                sample_per_value=sample_size, verbose=True)
            display_message((f'`{input_path.name}` dataframe limited '
                            + f'to at most {sample_size} per (pattern) pattern'),
                            logger, level=_WARNING)
            if verbose and not in_parallel:
                # > if in_parallel, sampling_info will be uninformative
                #   e.g.
                #       ## category representation in exactly_apw_with-relay_hits.pkl sample
                #       | category   |   count |   percentage |
                #       |:-----------|--------:|-------------:|
                #       | scoped     |       8 |          100 |
                display_message(sampling_info)

    dep_cols = cols_by_str(hits_df, start_str='dep_')
    too_flat = bool(cols_by_str(hits_df[dep_cols],
                                end_str=('node', 'contiguous', 'relation', 'head', 'target')))
    if too_flat:
        display_message(
            textwrap.dedent(f'''\
            ❗ Input dataframe `{input_path}` has wrong structure:
                Each tie in hit should have only 1 column (e.g. `dep_mod`) in hits dataframe.
                Rerun pipeline on raw data, then try again.'''),
            logger, level=_ERROR)

        return None

    dep_cats = cols_by_str(hits_df, end_str=(
        'deprel', '_head', 'pattern', 'form', 'x'))
    hits_df[dep_cats] = hits_df[dep_cats].astype('category')
    dep_cols += dep_cats

    logger = _LOGGER if in_parallel else None
    if verbose or in_parallel:
        print_iter(
            dep_cols,
            bullet=_BULLET,
            logger=logger,
            header=f'## original `{input_path.name}` dependency info columns')
        print('')

    tie_dfs = []

    for hit_id in hits_df.index:
        row = hits_df.loc[hit_id, dep_cols]
        deps_in_hit = _process_deps_in_hit(row, verbose, in_parallel)
        # if error in processing hit, return None
        if deps_in_hit is None:
            display_message(f'ERROR: {row.name} processing failed.')
            return (None, None)

        # > add string identifiers, with & without index, but sorted by index
        str_deps_df = _add_dep_strs(deps_in_hit)
        tie_dfs.append(str_deps_df.reset_index()
                       .set_index(['hit_id', 'index']))

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
            print('')

    all_ties_df = pd.concat(tie_dfs)

    if verbose or in_parallel:
        display_message(
            message=f'## New columns added to `{input_path.name}`\n{hits_df.loc[:, "hits_df_path":].iloc[0,:].to_markdown()}',
            logger=logger)

    #! namedtuple `dep_info` can't be pickled, so convert `dep_tuple` to dict type
    all_ties_df = all_ties_df.assign(
        dep_dict=all_ties_df.dep_tuple.apply(lambda t: t._asdict()))
    all_ties_df.pop('dep_tuple')
    return hits_df, all_ties_df


def _identify_dict_vals(row: pd.Series):
    is_dict_val = row.apply(lambda val: isinstance(val, dict))
    dict_vals = row.loc[is_dict_val]
    other_vals = row.loc[~is_dict_val]
    return other_vals, dict_vals


def _show_deps_info(row):
    logger = _LOGGER if _LOGGER.getEffectiveLevel == _DEBUG else None
    other_vals, dict_vals = _identify_dict_vals(row)

    print_iter(
        (f'{x}:\t{other_vals[x]}'
         for x in other_vals.index),
        bullet=_BULLET, logger=logger, level=_DEBUG,
        header=f'\n## `hit_id` = `{row.name}`'
    )

    #! if json processing of "edges" is updated to use 'tie' in place of 'node',
    #!      this will also have to be updated
    display_message('+ dependency features\n' +
                    print_md_table(pd.json_normalize(dict_vals).set_index('node').T,
                                   indent=2, suppress=True)
                    )
    print('')

    # display_message(row.to_markdown(), logger, level=_DEBUG)


def _process_deps_in_hit(row: pd.Series(dtype='object'),
                         verbose: bool = False,
                         in_parallel: bool = False):
    # ? is `fillna('n/a') necessary?`
    row = row.fillna('n/a')
    logger = _LOGGER if in_parallel else None
    display_message(
        f"processing {row.pattern} ~ {row.name}", logger, level=_INFO)

    # > log level for this info set to DEBUG
    # if verbose or (in_parallel and logger.getEffectiveLevel() == _DEBUG):
    # if verbose and ((not in_parallel) or logger.getEffectiveLevel() == _DEBUG):
    if logger.getEffectiveLevel() == _DEBUG and not in_parallel:
        _show_deps_info(row)
    #HACK
    # if 'pcc_eng_06_096.6489' in row.name: 
    #     print('found stupid long problem sentence')
    node_by_ix = view_nodes_by_index(row, extras=['form'])

    dep_dfs = []
    for dep_col in cols_by_str(row.to_frame().T, start_str='dep_'):

        tie = dep_col.replace('dep_', '')

        # ^ with multiple patterns concatenated, there will be NaN values for some "target" cols.
        # ? Is it better to simply skip those, or include them with empty values?
        # > first trying it with a simple `continue`... 🤞
        if row[dep_col] == 'n/a':
            continue
        try:
            dep_df = pd.json_normalize(row[dep_col], sep='_')
        except NotImplementedError:
            display_message(
                ('ERROR: `pd.json_normalize()` in `get_deps._process_deps_in_hit()` failed on:\n'
                 + print_md_table(row[[dep_col]], indent=2, suppress=True)),
                logger, level=_ERROR)
            return None
        else:
            dep_df['head_node'] = row[f'{tie}_head']
            dep_df['target_node'] = node_by_ix.node[dep_df.target_ix.squeeze()]
            dep_df['head_form'] = node_by_ix.form[dep_df.head_ix.squeeze()]
            # if verbose:
            #     print_dep = print_md_table(dep_df, suppress=True, indent=4)
            #     print_row = print_md_table(row.to_frame(), suppress=True, indent=4)
            #     print_nodeix = print_md_table(node_by_ix, suppress=True, indent=4)
            #     display_message(
            #         '\n'.join(
            #             (f'\n* `dep_df` for {row.name}',
            #              print_dep,
            #              f'\n* `row` for {row.name}',
            #              print_row, 
            #              f'\n* `node_by_ix` for {row.name}',
            #              print_nodeix, 
            #              )
            #         ), 
            #         logger
            #     )
            dep_df['target_form'] = node_by_ix.form[dep_df.target_ix.squeeze()]
            # try:
            #     dep_df['target_form'] = node_by_ix.form[dep_df.target_ix.squeeze()]
            # except:
            #     show_deps_info(row)
            #     display_message(
            #         '\n'.join(
            #             (f'\n## KeyError: `dep_df.target_ix`(={dep_df.target_ix.squeeze()}) not found in `node_by_ix` index\n',
            #              '* Offending `dep_df`',
            #              print_md_table(dep_df, indent=2, suppress=True),
            #              '* Offending `node_by_ix`',
            #              print_md_table(node_by_ix, indent=2, suppress=True),
            #              f'* `type(dep_df.target_ix.squeeze())` >> {type(dep_df.target_ix.squeeze())}',
            #              '* Offending `row`',
            #              print_md_table(
            #                  row.to_frame(), indent=2, suppress=True),
            #              ''
            #              )
            #         ),
            #         logger=logger, level=_ERROR
            #     )
            #     return None
            # HACK temp -- remove
            # print(dep_df.T.to_markdown())
            dep_dfs.append(dep_df)

    deps_for_hit = pd.concat(dep_dfs, ignore_index=True)

    index_cols = ['target_ix', 'head_ix']
    deps_for_hit[index_cols] = deps_for_hit[
        index_cols].apply(pd.to_numeric, downcast='unsigned')

    # #! renaming `'node'` column to `'tie'`:
    # # > it's the _connection_ not the joint/vertex,
    # # > and 'node' is already used to refer to the token/words (in grew output)
    # # <https://en.wikipedia.org/wiki/Structural_element>
    if 'node' in deps_for_hit.columns:
        deps_for_hit = deps_for_hit.rename(columns={'node': 'tie'})
    deps_for_hit['hit_id'] = row.name
    deps_for_hit['pattern'] = row.pattern

    # This doesn't save any memory at this point, but it might add up.
    #   In case there are type errors later,
    #   this does change the index columns from 'int64' to 'Int64'
    #! convert_dtypes is liable to totally fuck up the values 🙅‍♀️ DO NOT USE
    # deps_for_hit = deps_for_hit.convert_dtypes()

    deps_for_hit = deps_for_hit.assign(
        dep_tuple=deps_for_hit.apply(_get_dep_tuples, axis=1))

    return deps_for_hit


def view_nodes_by_index(hit_dep_info, extras=None):
    if isinstance(extras, str):
        extras = [extras] if extras != 'all' else ['lemma', 'form', 'xpos']
    try:
        frame = hit_dep_info.to_frame('ix_info')
    except AttributeError:
        frame = hit_dep_info

    ix_cols = cols_by_str(frame, end_str='x')
    if not ix_cols:
        frame = frame.T
        ix_cols = cols_by_str(frame, end_str='x')
        # frame = frame.T
    # ix_cols = list(set(ix_cols)
    #                - set(cols_by_str(frame, start_str='dep_str')))
    _by_ix = frame[ix_cols].T.apply(pd.to_numeric, downcast='unsigned')
    _by_ix['node'] = (_by_ix.index.to_series().astype('string')
                      .str.split('_').str.get(0).str.upper())
    _by_ix = _by_ix.set_index('ix_info')
    _by_ix.index.name = 'ix'
    if extras:
        for extra_col in extras:

            init_names = _by_ix.node.str.lower() + '_' + extra_col
            values = []
            for ix in init_names.index:
                init_col = init_names[ix]
                try:
                    val = frame[init_col].squeeze()
                except KeyError:
                    val = None
                    try:
                        display_message(
                            f'⚠️   ERROR: {init_col} not found', _LOGGER, _ERROR)
                    except NameError:
                        display_message(f'⚠️   ERROR: {init_col} not found')

                values.append(val)
            _by_ix[extra_col] = values
            _by_ix[extra_col] = _by_ix[extra_col].astype('string')
    return _by_ix


def _get_dep_tuples(_df):
    ix_cols = ['head_ix', 'target_ix']
    # pre_cols = ['node', 'head_lemma']
    # post_cols = ['target_lemma', 'relation']
    _df[ix_cols] = _df[ix_cols].astype('string').str.zfill(2)
    row = _df[list(_DEP._fields)].squeeze()
    # > fields:
    # ['tie', 'pattern', 'relation',
    #  'head_node', 'head_ix', 'head_form', 'head_lemma',
    #  'target_node', 'target_ix', 'target_form', 'target_lemma']
    return _DEP._make(row)


def _add_dep_strs(deps_in_hit: pd.DataFrame, verbose: bool = False):

    str_deps_df = deps_in_hit.copy()
    # ! changed the default value to `form` instead of `lemma` @ 2023-11-03
    str_deps_df['dep_str'] = [
        f"{x.head_form.lower()}{_DELIM_STR}{x.target_form.lower()}[={x.tie}]"
        if x is not None else ''
        for x in str_deps_df['dep_tuple']]

    str_deps_df['dep_str_lemma'] = [
        f"{x.head_lemma}{_DELIM_STR}{x.target_lemma}[={x.tie}]"
        if x is not None else ''
        for x in str_deps_df['dep_tuple']]

    str_deps_df['dep_str_struct'] = [
        f"{x.head_node}{_DELIM_STR}{x.target_node}[={x.tie}]"
        if x is not None else ''
        for x in str_deps_df['dep_tuple']]

    str_deps_df['dep_str_ix'] = [
        f"{x.head_ix}:{x.head_form.lower()}{_DELIM_STR}{x.target_ix}:{x.target_form.lower()}[={x.tie}]" if x is not None else ''
        for x in str_deps_df['dep_tuple']
    ]

    str_deps_df['dep_str_node'] = [
        f"{x.head_node}:{x.head_form.lower()}{_DELIM_STR}{x.target_node}:{x.target_form.lower()}[={x.tie}]" if x is not None else ''
        for x in str_deps_df['dep_tuple']
    ]

    str_deps_df = str_deps_df.assign(
        dep_str_full=str_deps_df[
            ['dep_str_ix', 'relation']].apply(_add_relation, axis=1),
        dep_str_rel=str_deps_df[
            ['dep_str', 'relation']].apply(_add_relation, axis=1),
        dep_str_node_rel=str_deps_df[
            ['dep_str_node', 'relation']].apply(_add_relation, axis=1)
    )
    try:
        debug = _LOGGER.getEffectiveLevel() == 10
    except AttributeError:
        logger = None
        debug = False
    else:
        logger = _LOGGER
    # HACK temp -- remove
    # dep_str_cols = cols_by_str(str_deps_df, start_str='dep_str')
    # print(str_deps_df.set_index('tie').loc[:, dep_str_cols].T.to_markdown())

    str_deps_df = str_deps_df.sort_values(
        ['target_ix', 'head_ix']).reset_index(drop=True)

    str_deps_df = str_deps_df.assign(dep_str_mask=_mask_dep_str(str_deps_df))
    # ? #TODO: mask `str_deps_df.dep_str_node_rel` as well?

    str_deps_df = str_deps_df.assign(
        dep_str_mask_rel=str_deps_df[
            ['dep_str_mask', 'relation']].apply(_add_relation, axis=1))

    if verbose or debug:
        dep_str_table = (print_md_table(
            str_deps_df[cols_by_str(str_deps_df, start_str='dep_str')],
            indent=2, suppress=True)
        )
        display_message(
            f'`{str_deps_df.hit_id[0]}`\n{dep_str_table}', logger, level=_DEBUG)

    return str_deps_df


def _mask_dep_str(str_df: pd.DataFrame):
    try:
        debug = _LOGGER.getEffectiveLevel() == 10
    except AttributeError:
        logger = None
        debug = False
    else:
        logger = _LOGGER

    def _assign_dep_str_mask(_df, condition, col1, col2):
        if any(condition):
            _df.loc[condition, 'dep_str_mask'] = (
                _df.loc[condition, col1] + _DELIM_STR + _df.loc[condition, col2])

    # * for mod, use both xpos
    # * for relay, use both xpos
    if 'tie' not in str_df.columns:
        display_message('Error: "tie" column is not set.',
                        logger, level=_ERROR)
        return str_df.assign(dep_str_mask='').dep_str_mask

    # > this one doesn't need an existence check because `mod` always exists
    # > but doing it anyway, in case that changes 🤷‍♀️
    is_mod_or_relay = str_df.tie.isin(('mod', 'relay'))
    _assign_dep_str_mask(str_df, is_mod_or_relay, 'head_xpos', 'target_xpos')

    # * for neg, use target_lemma and head_xpos (keep neg token)
    is_neg = str_df.tie == 'neg'
    _assign_dep_str_mask(str_df, is_neg, 'head_xpos', 'target_lemma')

    # * for negraise, use target_xpos and head_lemma (keep NR token)
    is_raised = str_df.tie == 'negraise'
    _assign_dep_str_mask(str_df, is_raised, 'head_lemma', 'target_xpos')

    return str_df.dep_str_mask


def _add_relation(_row):
    _str = _row.get(0, '')
    if not (_str and isinstance(_str, str)):
        return ''

    _relation = _row.get(1)
    return _str.replace(_DELIM_STR, f'{_DELIM_STR}[{_relation}]{_DELIM_STR}')


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    df = pd.concat(find_files(_DATA_DIR, _FILEGLOB, True))
    df = get_deps(df, _DF_SAVE_PATH)
    proc_t1 = pd.Timestamp.now()
    print(
        f'Time to get dependency identifier strings: {dur_round((proc_t1 - proc_t0).seconds)}')
