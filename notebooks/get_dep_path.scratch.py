# %%
from collections import namedtuple
from json import dumps
from pathlib import Path
from pprint import pprint

from source.utils.dataframes import balance_sample

import pandas as pd

# pd.set_option('display.max_colwidth', 40)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 100)

_TIE_STR = '>'
_FILEGLOB = 'exactly_[pna]*hits.pkl.gz'
_DEP = namedtuple('dep_info', ['node', 'head_ix', 'head_lemma',
                               'target_ix', 'target_lemma', 'relation'])


# %%
def balance_sample(_df, column_name: str, sample_per_value: int = 5):
    '''
    create sample with n rows satisfying each unique value of the given column (or the )
    '''
    return [
        _df.loc[_df.loc[:, 'category'] == c, :].sample(min(_df.category.value_counts()[c], 8)) for c in _df.loc[:, 'category'].unique()]


def print_iter(iter_obj):
    print(' ▸ '+'\n ▸ '.join(iter_obj))


def get_dep_tuples(df):
    _row = df[['node', 'head_ix', 'head_lemma',
               'target_ix', 'target_lemma', 'relation']].squeeze()
    _index_cols = ['head_ix', 'target_ix']
    _row[['head_ix', 'target_ix']] = _row[[
        'head_ix', 'target_ix']].astype('string').str.zfill(2)
    return _DEP._make(_row)


def _add_relation(_row):
    _str = _row.fillna('').iloc[0]
    if not (_str and isinstance(_str, str)):
        return ''

    _relation = _row.iloc[1]
    # opt_hyphen = '-' if '-' in _TIE_STR else ''
    # return _str.replace(_TIE_STR, f'{opt_hyphen}[{_relation}]{_TIE_STR}')
    return _str.replace(_TIE_STR, f'{_TIE_STR}[{_relation}]{_TIE_STR}')


def _mask_dep_str(_df: pd.DataFrame()):

    # for mod, use both xpos
    # for relay, use both xpos
    if 'node' not in _df.columns:
        print('Error: "node" column is not set.')
        return _df.assign(dep_str_mask='').dep_str_mask

    # this one doesn't need an existence check because `mod` always exists
    # but doing it anyway, in case that changes 🤷‍♀️
    is_mod_or_relay = _df.node.isin(('mod', 'relay'))
    if any(is_mod_or_relay):
        _df.loc[is_mod_or_relay, 'dep_str_mask'] = (
            _df.loc[is_mod_or_relay, 'head_xpos']
            + _TIE_STR
            + _df.loc[is_mod_or_relay, 'target_xpos'])

    # for neg, use target_lemma and head_xpos (keep neg token)
    is_neg = _df.node == 'neg'
    if any(is_neg):
        _df.loc[is_neg, 'dep_str_mask'] = (
            _df.loc[is_neg, 'head_xpos']
            + _TIE_STR
            + _df.loc[is_neg, 'target_lemma'])

    # for negraise, use target_xpos and head_lemma (keep NR token)
    is_raised = _df.node == 'negraise'
    if any(is_raised):
        _df.loc[is_raised, 'dep_str_mask'] = (
            _df.loc[is_raised, 'head_lemma']
            + _TIE_STR
            + _df.loc[is_raised, 'target_xpos'])

    return _df.dep_str_mask

# %% [markdown]
# Select dataframes to be crosstabulated
#
# ```{python}
# * one pickled dataframe only (i.e. no NaN values)
# # > scoped sample
# # df_path = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits/'
# #               'scoped/exactly_test_with-relay_hits.pkl.gz')
# # > negraised sample
# # df_path = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits/'
# #               'raised/exactly_test_neg-raised_hits.pkl.gz')
# # > contig sample
# #df_path = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits/'
# #               'contig/exactly_test_sans-relay_hits.pkl.gz')
# #df = pd.read_pickle(df_path)
# # * multiple pickled dataframes concatenated into a single frame
# # > hits for more than 1 pattern type ==> NaN values in optional columns
# # pickles_from_paths = (Path('/share/compling/data/sanpi/demo/data/2_hit_tables').joinpath(dataset_path)
# #            for dataset_path
# #            in ('contig/exactly_test_sans-relay_hits.pkl.gz',
# #                'scoped/exactly_test_with-relay_hits.pkl.gz',
# #                'raised/exactly_test_neg-raised_hits.pkl.gz')
# #            )
# ```


# %%
# > data inputs could also be a glob expression for a directory
pickles_from_dir = Path(
    '/share/compling/data/sanpi/2_hit_tables').rglob(_FILEGLOB)

pickles = tuple(pickles_from_dir)
print(f'{len(pickles)} paths matching {_FILEGLOB} found.')
print_iter([f'../{Path(*p.parts[-3:])}' for p in pickles])
# pickles = pickles_from_paths

# %% [markdown]
# Read in all indicated dataframes and concatonate

# %%
df = pd.concat((pd.read_pickle(p) for p in pickles))

# %% [markdown]
# ## Retrieve head index from `dep_[label]_source` column
# Almost everything needed for dep path is in in the `dep_[label]_target` columns but the index of the head token is not. This can be retrieved from the `source` columns though, and then everything is contained in a single set of dictionaries

# %%
# // all_dep_fields = ['head_ix', 'head_lemma', 'head_xpos',
# //                   'target_ix', 'target_lemma', 'target_xpos',
# //                   'relation', 'node']
# // dep_info = namedtuple('dependency_ix', all_dep_fields)
# // dep_identifiers = ['node', 'target_lemma', 'head_lemma']
# // final_dep = namedtuple('dependency', dep_identifiers)
dep_cols = df.columns[df.columns.str.startswith('dep')].to_list()
print('## dependency info columns')
print_iter(dep_cols)
# // target_cols = df.columns[df.columns.str.endswith('target')].to_list()
# // print('## dep TARGET columns')
# // print_iter(target_cols)

labels = [c.split('_')[1] for c in dep_cols]
print('## labels')
print_iter(labels)

# no longer necessary with new structure
# // head_cols = [f"dep_{L}_head" for L in labels]
# // print('## dep HEAD columns')
# // print_iter(head_cols)

# // full_deps_info = {}
# // dep_ix_str = {}
# // dep_str = {}
# // dep_mask_str = {}
# // dep_dicts = {}
# // dep_dict_values = {}
# // dep_tuples = {}

all_hits_df = pd.DataFrame()

# > for testing loop
# df = balance_sample(df, column_name='category', sample_per_value=8)

# %%
# > for testing outside of loop
# ix = df.sample(1).index[0]
# while not isinstance(df.loc[ix, 'dep_neg'], dict):
#     ix = df.sample(1).index[0]
# pprint(df.dep_neg[ix])
# %%
# TODO: make this a method
for ix in df.index:

    # ? is `fillna('n/a') necessary?`
    row = df.loc[ix, ['category'] + dep_cols].fillna('n/a')

    # print(f'## row {ix} values')
    # print_iter(f'{x}\n    {row[x]}'
    #            for x in row.index
    #            if not isinstance(row[x], dict))
    # print_iter(f'{x}\n{pd.Series(row[x])}\n'
    #            for x in row.index
    #            if isinstance(row[x], dict))
    # print(row.to_markdown())

    deps_for_hit = pd.DataFrame()
    # ^ with multiple patterns concatenated, there will be NaN values for some "target" cols.
    # ? Is it better to simply skip those, or include them with empty values?
    # dep_col = 'dep_mod'
    # label = 'mod'
    for dep_col, label in zip(dep_cols, labels):

        # > first trying it with a simple `continue`... 🤞
        if row.at[dep_col] == 'n/a':
            continue
        # // dep = None

        # already in dep_col value dict
        # // adds = {'node': label}
        # t_dict = row[dep_col]['target']
        # h_dict = row[dep_col]['head']
        # // s_dict = row[s_col]
        # // if not (s_dict != 'n/a' and t_dict['head'] == s_dict['lemma']):
        # //     print(
        # //         f'ERROR: mismatch between target and source info for {label} node dependency for hit {ix}')
        # //     continue

        # //# fields = ['head_ix', 'head_lemma', 'head_xpos',
        # //#           'target_ix', 'target_lemma', 'target_xpos',
        # //#           'relation', 'node']
        # // dep = dep_info(head_ix=h_dict['ix'],
        # //    head_lemma=h_dict['lemma'],
        # //    head_xpos=s_dict.get('xpos', '_'),
        # //    target_ix=t_dict['ix'],
        # //    target_lemma=t_dict['lemma'],
        # //    target_xpos=t_dict['xpos'],
        # //    relation=t_dict['deprel'],
        # //    node=label)

        dep_df = pd.json_normalize(row[dep_col], sep='_')
        # dep_ix_str = (f"{str(dep_df.head_ix[0]).zfill(2)}:{hit_deps.head_lemma[0]}-{label}{_TIE_STR}"
        #               f"{str(dep_df.target_ix[0]).zfill(2)}:{dep_df.target_lemma[0]}")
        # dep_str = (f"{hit_deps.head_lemma[0]}-{label}{_TIE_STR}"
        #            f"{dep_df.target_lemma[0]}")

        # dep_dict = dep_df.to_dict('index')[0]

        # deps_df.loc[ix, label + '_dep_dict'] = dep_dict
        # // deps_df.loc[ix, label + '_dep_frame'] = dep_df
        deps_for_hit = pd.concat([deps_for_hit, dep_df])

    deps_for_hit = deps_for_hit.assign(hit_id=ix).convert_dtypes()

    deps_for_hit = deps_for_hit.assign(
        dep_tuple=deps_for_hit.apply(get_dep_tuples, axis=1))

    # %%
    # > add string identifiers, with & without index, but sorted by index
    str_deps_df = deps_for_hit.assign(
        dep_str=deps_for_hit.dep_tuple.apply(
            lambda x: (f"{x.head_lemma}{_TIE_STR}"
                       f"{x.target_lemma}[={x.node}]")).fillna('').astype('string'),
        dep_str_ix=deps_for_hit.dep_tuple.apply(
            lambda x: (f"{x.head_ix}:{x.head_lemma}{_TIE_STR}"
                       f"{x.target_ix}:{x.target_lemma}[={x.node}]")).fillna('').astype('string'),
    )
    # %%
    str_deps_df = str_deps_df.assign(
        dep_str_full=str_deps_df[['dep_str_ix', 'relation']].apply(
            _add_relation, axis=1),
        dep_str_rel=str_deps_df[['dep_str', 'relation']].apply(
            _add_relation, axis=1)
    )
    str_deps_df.iloc[:, -6:].squeeze()

    # %%
    # already a dataframe
    # //hit_deps = pd.DataFrame(deps, index=all_dep_fields
    # //                         ).transpose().convert_dtypes()
    index_cols = ['target_ix', 'head_ix']

    str_deps_df[index_cols] = str_deps_df[index_cols].apply(
        pd.to_numeric, downcast='unsigned')
    str_deps_df = str_deps_df.sort_values(
        index_cols).reset_index(drop=True)

    # print(str_deps_df.squeeze())

    # contiguous already in table
    # // hit_deps = hit_deps.assign(
    # //     contiguous=abs(hit_deps.head_ix - hit_deps.target_ix) == 1)

    # %% [markdown]
    # ## Collapsing to index by `hit_index`
    # At this point, all unmasked strings are defined for each individual dependency within a hit.
    #
    # So the remaining steps are:
    # - [x] add POS-masked strings (started this with `gen_masked_str()` below)
    # - [ ] somehow get the information for each hit (multiple dependencies) into a single dataframe
    #   - this could be by having a multilevel index, or by collapsing columns

    # %%
    # dep_ix_str = '; '.join(
    # (f"{str(this_hit_deps.head_ix[i]).zfill(2)}:{this_hit_deps.head_lemma[i]}{_TIE_STR}"
    #     f"{str(this_hit_deps.target_ix[i]).zfill(2)}:{this_hit_deps.target_lemma[i]}"
    #     f"_{this_hit_deps.node[i]}"
    #     for i in this_hit_deps.index))

    # dep_str[ix] = '; '.join(
    #     (f"{this_hit_deps.head_lemma[i]}{_TIE_STR}{this_hit_deps.target_lemma[i]}_{this_hit_deps.node[i]}"
    #         for i in this_hit_deps.index))

    # %%
    str_deps_df = str_deps_df.assign(
        dep_str_mask=_mask_dep_str(str_deps_df))
    str_deps_df = str_deps_df.assign(
        dep_str_mask_rel=str_deps_df[['dep_str_mask', 'relation']].apply(_add_relation, axis=1))

    # ? no longer necessary?
    # // # create named tuples
    # // dep_id_df = hit_deps[dep_identifiers]
    # // dep_tuples[ix] = tuple(final_dep._make(dep_id_df.loc[i, :].squeeze())
    # //                        for i in dep_id_df.index)

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

    # %% [markdown]
    # The following creates a series of all the dep strings combined (with `; `) for a hit.

    str_cols = str_deps_df.columns[str_deps_df.columns.str.startswith(
        'dep_str')].to_list()
    # print('\n⁂ Combined string representations of dependencies for match', ix)
    joined_strs = str_deps_df[str_cols].apply(lambda c: ';'.join(c), axis=0)
    # print_iter(f'{x} ↣ {joined_strs[x]}' for x in joined_strs.index)
    df.loc[ix, str_cols] = joined_strs
    # df = df.join(by_hit_dep_df)

# %%
print_df = df.sample(15) if len(df) > 15 else df
print(print_df.loc[~print_df.dep_str.isna(), [
      'category', 'colloc', 'hit_text'] + str_cols].to_markdown())

print(df[['dep_str_mask', 'colloc', 'dep_str', 'hit_text']]
      .value_counts().to_frame().rename(columns={0: 'count'})
      .reset_index().head(10).to_markdown())

# %%

df.to_pickle(f'/share/compling/data/sanpi/2_hit_tables/{_FILEGLOB.split("*")[0]}_dependencies.pkl.gz')

# %% [markdown]
# ## Construct boolean table for dep_str

# %%
ct_hit_dep = pd.crosstab(index=df.index, columns=df.dep_str,
                         rownames=['hit_id'], margins=True)
ct_hit_dep
# %% [markdown]
# `crosstab()` creates a frequency table.
#
# It is possible for the `dep_str` frequencies to sum to greater than 1,
# since the same dependency path can be repeated in different hits

# %%
print(ct_hit_dep.sum(axis=0).nlargest(5))

# %% [markdown]
# However, the sum of frequencies of `dep_str` by hit must be == 1
# since there is exactly 1 dependency path for each hit.

# %%
print(ct_hit_dep.sum(axis=1).nlargest(3))

# %% [markdown]
# Since the frequencies will always be either $1$ or $0$,
# they can be directly converted to boolean `dtypes` using `astype('boolean')`

# %%
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
