# coding=utf-8
# %%
from collections import namedtuple
from json import dumps
from pathlib import Path
from pprint import pprint

import pandas as pd

from crosstab_deps import crosstabulate_variants as ct_var
from utils.dataframes import balance_sample, cols_by_str
from utils.general import print_iter, dur_round

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


def concat_pkls():
    # TODO: change path and glob to arguments
    pickles = tuple(_DATA_DIR.rglob(_FILEGLOB))
    print(f'{len(pickles)} paths matching {_FILEGLOB} found.')
    print_iter([f'../{Path(*p.parts[-3:])}' for p in pickles])

    df = pd.concat((pd.read_pickle(p) for p in pickles))

    return df


def get_deps(df: pd.DataFrame()):
    df = process_dep_info(df)

    print_df = df.sample(15) if len(df) > 15 else df
    print(print_df.loc[~print_df.dep_str.isna(),
                       ['category', 'colloc', 'hit_text'] + cols_by_str(print_df, 'dep_str')].to_markdown())

    print(df[['dep_str_mask', 'colloc', 'dep_str', 'hit_text']]
          .value_counts().to_frame().rename(columns={0: 'count'})
          .reset_index().head(10).to_markdown())

    df.to_pickle(_DF_SAVE_PATH)

    return df


def process_dep_info(df: pd.DataFrame()):

    dep_cols = cols_by_str(df, start_str='dep_')
    labels = (c.split('_')[1] for c in dep_cols)

    if _VERBOSE:

        print('## dependency info columns')
        print_iter(dep_cols)

        print('## labels')
        print_iter(labels)

    all_hits_df = pd.DataFrame()

    # * Testing Options
    # > for testing loop
    df, sampling_info = balance_sample(df, column_name='category',
                                       sample_per_value=8, verbose=True)
    print(sampling_info)

    # > for testing outside of loop
    # ix = df.sample(1).index[0]
    # while not isinstance(df.loc[ix, 'dep_neg'], dict):
    #     ix = df.sample(1).index[0]
    # print('Testing Single Random Hit:',ix)
    # pprint(df.dep_neg[ix])

    # %%
    for hit_id in df.index:
        row = df.loc[hit_id, dep_cols]
        deps_in_hit = _process_deps_in_hit(row)

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

        if _VERBOSE:
            print('\n⁂ Combined string representations of dependencies for match', hit_id)
            print_iter(f'{x} ↣ {joined_strs[x]}' for x in joined_strs.index)

    return df


def _process_deps_in_hit(row):
    # ? is `fillna('n/a') necessary?`
    row = row.fillna('n/a')

    if _VERBOSE:
        print(f'## row {row.name} values')
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


def _add_dep_strs(deps_in_hit: pd.DataFrame()):

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

    if _VERBOSE:
        print(str_deps_df.squeeze())

    return str_deps_df


def _mask_dep_str(_df: pd.DataFrame()):

    # * for mod, use both xpos
    # * for relay, use both xpos
    if 'node' not in _df.columns:
        print('Error: "node" column is not set.')
        return _df.assign(dep_str_mask='').dep_str_mask

    # > this one doesn't need an existence check because `mod` always exists
    # > but doing it anyway, in case that changes 🤷‍♀️
    is_mod_or_relay = _df.node.isin(('mod', 'relay'))
    if any(is_mod_or_relay):
        _df.loc[is_mod_or_relay, 'dep_str_mask'] = (
            _df.loc[is_mod_or_relay, 'head_xpos']
            + _TIE_STR
            + _df.loc[is_mod_or_relay, 'target_xpos'])

    # * for neg, use target_lemma and head_xpos (keep neg token)
    is_neg = _df.node == 'neg'
    if any(is_neg):
        _df.loc[is_neg, 'dep_str_mask'] = (
            _df.loc[is_neg, 'head_xpos']
            + _TIE_STR
            + _df.loc[is_neg, 'target_lemma'])

    # * for negraise, use target_xpos and head_lemma (keep NR token)
    is_raised = _df.node == 'negraise'
    if any(is_raised):
        _df.loc[is_raised, 'dep_str_mask'] = (
            _df.loc[is_raised, 'head_lemma']
            + _TIE_STR
            + _df.loc[is_raised, 'target_xpos'])

    return _df.dep_str_mask


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
    df = concat_pkls()
    df = get_deps(df)
    proc_t1 = pd.Timestamp.now()
    print(
        f'Time to get dependency identifier strings: {dur_round((proc_t1 - proc_t0).seconds)}')


# %%
# can save this here, or call crosstab method directly
# df.to_pickle(f'/share/compling/data/sanpi/2_hit_tables/{_FILEGLOB.split("*")[0]}_dep.pkl.gz')
# df = pd.read_pickle(
#     f'{_DATA_DIR}{_FILEGLOB.split("*")[0]}_dep.pkl.gz')

# * Crosstabulate Dependency Strings
# * (1) `hit_id`
# TODO: add arg for cross-column to crosstabulate method
ct_hit_id = ct_var(df)
boolean_hits = ct_hit_dep.loc[ct_hit_dep.index != 'All',
                              ct_hit_dep.columns != 'All'].astype('boolean')

# %% [markdown]
# I think it may be interesting to see a crosstabulation of the dependency paths with the exact lemmas collapsed.
# For example, instead of `'standard>not_neg; standard>exactly_mod'`, have a series of `'ADJ>not_neg; ADJ>ADV_mod'`
# and crosstabulate that with the collocations (i.e. the `ADJ` and `ADV` token lemmas)
#
# - [x] added this as `dep_str_mask`

# %%
ct_colloc_mask = pd.crosstab(df.colloc, df.dep_str_mask, margins=True)
ct_colloc_mask
# %%
df = df.assign(neg_lemma=df.neg_lemma.str.lower()
               ).loc[df.adv_lemma == 'exactly', :]
df.groupby('dep_str_mask')['colloc', 'dep_str'].value_counts()

# %%
ct_mask_colloc = pd.crosstab(df.dep_str_mask, df.colloc,  margins=True)
ct_mask_colloc
# %%
