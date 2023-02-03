# coding=utf-8
# %%
from collections import namedtuple
from json import dumps
from pathlib import Path
from pprint import pprint

import pandas as pd

from analyze.crosstab_deps import crosstabulate_variants as ct_var
from analyze.utils.dataframes import balance_sample, cols_by_str
from analyze.utils.general import print_iter, dur_round

# pd.set_option('display.max_colwidth', 40)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 100)

_DEP = namedtuple('dep_info', ['node', 'head_ix', 'head_lemma',
                               'target_ix', 'target_lemma', 'relation'])

_DATA_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
_FILEGLOB = 'exactly_nyt*hits.pkl.gz'
_DF_SAVE_DIR = _DATA_DIR.parent.joinpath('3_dep_info')
if not _DF_SAVE_DIR.is_dir():
    _DF_SAVE_DIR.mkdir()
_DF_SAVE_PATH = _DF_SAVE_DIR.joinpath(
    f'{_FILEGLOB.split("*")[0]}_deps.pkl.gz')

_TIE_STR = '>'
_VERBOSE = False

# ! moved to utils/dataframes
# // def concat_pkls(data_dir: Path(), fname_glob: str):
# //     pickles = tuple(data_dir.rglob(fname_glob))
# //     print(f'{len(pickles)} paths matching {fname_glob} found.')
# //     print_iter([f'../{Path(*p.parts[-3:])}' for p in pickles])
# //     df = pd.concat((pd.read_pickle(p) for p in pickles))
# //     return df


def get_deps(df: pd.DataFrame(),
             df_save_path: Path() = None,
             sample_size: int = None,
             verbose: bool = False):

    proc_t0 = pd.Timestamp.now()
    if not df_save_path:
        print('⚠️ Warning: No output path given. Resultant dataframe will not be saved to file.')
    df = process_dep_info(df, sample_size=sample_size, verbose=verbose)
    proc_t1 = pd.Timestamp.now()
    print(
        f'\nTime to process dep info: {dur_round((proc_t1 - proc_t0).seconds)}')

    if verbose:
        print_df = df.sample(15) if len(df) > 15 else df
        print(print_df.loc[~print_df.dep_str.isna(),
                           ['category', 'hit_text'] + cols_by_str(print_df, 'dep_str')].to_markdown())

    print(df[['hit_text', 'dep_str', 'dep_str_mask', 'neg_lemma', 'colloc']]
            .value_counts().to_frame().rename(columns={0: 'count'}).sort_values('colloc').nlargest(10, 'count').reset_index().to_markdown())
        
    # TODO: modify to process pickles individually, then concatonate. Means changing the `df_save_path` argument maybe?
    if not df_save_path:
        print('\nNo output path given. Dataframe with dependency string identifiers not saved to file.')
    else:
        print('\nwriting dataframe with added dependency string variants',
              f'to {df_save_path}...')
        df.to_pickle(df_save_path)
        print(' ✔️ finished saving file')

    return df


def process_dep_info(df: pd.DataFrame(), sample_size: int = None, verbose=False):

    # * Testing Options
    # > for testing loop
    if sample_size is not None:
        df, sampling_info = balance_sample(
            df, column_name='category',
            sample_per_value=sample_size, verbose=True)
        if verbose:
            print(sampling_info)
        else: 
            print(f'data limited to at most {sample_size} per (pattern)category')

    # > for testing outside of loop
    # ix = df.sample(1).index[0]
    # while not isinstance(df.loc[ix, 'dep_neg'], dict):
    #     ix = df.sample(1).index[0]
    # print('Testing Single Random Hit:',ix)
    # pprint(df.dep_neg[ix])

    dep_cols = cols_by_str(df, start_str='dep_')
    labels = (c.split('_')[1] for c in dep_cols)

    if verbose:

        print('## dependency info columns')
        print_iter(dep_cols)

        print('## labels')
        print_iter(labels)

    # TODO: currently, nothing is done with this. Either use it or remove it
    all_hits_df = pd.DataFrame()
    # %%
    for hit_id in df.index:
        row = df.loc[hit_id, dep_cols]
        deps_in_hit = _process_deps_in_hit(row, verbose)

        # %%
        # > add string identifiers, with & without index, but sorted by index
        str_deps_df = _add_dep_strs(deps_in_hit)

        # TODO: this might work to record all info, but must add `node` to index (to make it unique)
        all_hits_df = pd.concat([all_hits_df, str_deps_df])
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
            lambda c: ';'.join(c), axis=0)
        df.loc[hit_id, str_cols] = joined_strs

        if verbose:
            print('\n⁂ Combined string representations of dependencies for match', hit_id)
            print_iter(f'{x} ↣ {joined_strs[x]}' for x in joined_strs.index)

    return df


def _process_deps_in_hit(row: pd.Series(dtype='object'),
                         verbose: bool = False):
    # ? is `fillna('n/a') necessary?`
    row = row.fillna('n/a')

    if verbose:
        print(f'\n## row {row.name} values')
        print_iter(f'{x}\n    {row[x]}'
                   for x in row.index
                   if not isinstance(row[x], dict))
        print_iter(f'{x}\n{pd.Series(row[x])}\n'
                   for x in row.index
                   if isinstance(row[x], dict))
        print(row.to_markdown())

    deps_for_hit = pd.DataFrame()
    # ^ with multiple patterns concatenated, there will be NaN values for some "target" cols.
    # ? Is it better to simply skip those, or include them with empty values?
    for dep_col in row.index:
        label = dep_col.split('_')[1]

        # > first trying it with a simple `continue`... 🤞
        if row[dep_col] == 'n/a':
            continue

        dep_df = pd.json_normalize(row[dep_col], sep='_')

        deps_for_hit = pd.concat([deps_for_hit, dep_df])

    deps_for_hit = deps_for_hit.assign(hit_id=row.name).convert_dtypes()

    deps_for_hit = deps_for_hit.assign(
        dep_tuple=deps_for_hit.apply(_get_dep_tuples, axis=1))

    return deps_for_hit


def _get_dep_tuples(df):
    row = df[['node', 'head_ix', 'head_lemma',
              'target_ix', 'target_lemma', 'relation']].squeeze()
    ix_cols = ['head_ix', 'target_ix']
    row[ix_cols] = row[ix_cols].astype('string').str.zfill(2)
    return _DEP._make(row)


def _add_dep_strs(deps_in_hit: pd.DataFrame(),
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

    # %%
    str_deps_df = str_deps_df.assign(
        dep_str_mask=_mask_dep_str(str_deps_df))

    str_deps_df = str_deps_df.assign(
        dep_str_mask_rel=str_deps_df[
            ['dep_str_mask', 'relation']].apply(_add_relation, axis=1))

    if verbose:
        print(str_deps_df.squeeze())

    return str_deps_df


def _mask_dep_str(df: pd.DataFrame()):

    # * for mod, use both xpos
    # * for relay, use both xpos
    if 'node' not in df.columns:
        print('Error: "node" column is not set.')
        return df.assign(dep_str_mask='').dep_str_mask

    # > this one doesn't need an existence check because `mod` always exists
    # > but doing it anyway, in case that changes 🤷‍♀️
    is_mod_or_relay = df.node.isin(('mod', 'relay'))
    if any(is_mod_or_relay):
        df.loc[is_mod_or_relay, 'dep_str_mask'] = (
            df.loc[is_mod_or_relay, 'head_xpos']
            + _TIE_STR
            + df.loc[is_mod_or_relay, 'target_xpos'])

    # * for neg, use target_lemma and head_xpos (keep neg token)
    is_neg = df.node == 'neg'
    if any(is_neg):
        df.loc[is_neg, 'dep_str_mask'] = (
            df.loc[is_neg, 'head_xpos']
            + _TIE_STR
            + df.loc[is_neg, 'target_lemma'])

    # * for negraise, use target_xpos and head_lemma (keep NR token)
    is_raised = df.node == 'negraise'
    if any(is_raised):
        df.loc[is_raised, 'dep_str_mask'] = (
            df.loc[is_raised, 'head_lemma']
            + _TIE_STR
            + df.loc[is_raised, 'target_xpos'])

    return df.dep_str_mask


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
    df = concat_pkls(_DATA_DIR, _FILEGLOB, True)
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
