# %%
import pandas as pd
from pathlib import Path
from collections import namedtuple
from pprint import pprint
pd.set_option('display.width', 120, 'display.max_colwidth', 40)
_TIE_STR = '->'
# %%
# * one pickled dataframe only (i.e. no NaN values)
# # > scoped sample
# # df_path = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits/'
# #               'scoped/exactly_test_with-relay_hits.pkl.gz')
# # > negraised sample
# # df_path = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits/'
# #               'raised/exactly_test_neg-raised_hits.pkl.gz')
# # > contig sample
# df_path = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits/'
#                'contig/exactly_test_sans-relay_hits.pkl.gz')

# df = pd.read_pickle(df_path)

# %%
# * multiple pickled dataframes concatenated into a single frame
# > hits for more than 1 pattern type ==> NaN values in optional columns
pickles_from_paths = (Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits').joinpath(dataset_path)
           for dataset_path
           in ('contig/exactly_test_sans-relay_hits.pkl.gz',
               'scoped/exactly_test_with-relay_hits.pkl.gz',
               'raised/exactly_test_neg-raised_hits.pkl.gz')
           )
# %% 
#> data inputs could also be a glob expression for a directory
pickles_from_dir = Path('/home/arh234/projects/sanpi/demo/data/2_csv_hits').rglob('exactly*hits.pkl.gz')

pickles = pickles_from_dir
# pickles = pickles_from_paths
df = pd.concat((pd.read_pickle(p) for p in pickles))

# %% [markdown]
# ## Retrieve head index from `dep_[label]_source` column
# Almost everything needed for dep path is in in the `dep_[label]_target` columns but the index of the head token is not. This can be retrieved from the `source` columns though, and then everything is contained in a single set of dictionaries

# %%
all_dep_fields = ['head_ix', 'head_lemma', 'head_xpos',
                  'target_ix', 'target_lemma', 'target_xpos',
                  'relation', 'node']
dep_info = namedtuple('dependency_ix', all_dep_fields)
dep_identifiers = ['node', 'target_lemma', 'head_lemma']
final_dep = namedtuple('dependency', dep_identifiers)
target_cols = df.columns[df.columns.str.endswith('target')].to_list()
print('TARGET columns')
pprint(target_cols)
labels = [c.split('_')[1] for c in target_cols]
print('labels')
pprint(labels)
source_cols = [f"dep_{L}_source" for L in labels]
print('SOURCE columns')
pprint(source_cols)

# %%
full_deps_info = {}
dep_ix_str = {}
dep_str = {}
dep_mask_str = {}
dep_dicts = {}
dep_dict_values = {}
dep_tuples = {}
for ix in df.index:
    # for c, ix in enumerate(df.index):
    # if c > 1:
    #     break
    row = df.loc[ix, ['category'] + target_cols + source_cols].fillna('n/a')
    # print(row.to_markdown())
    deps = {}
    # ^ with multiple patterns concatenated, there will be NaN values for some "target" cols.
    # ? Is it better to simply skip those, or include them with empty values?
    for t_col, s_col, label in zip(target_cols, source_cols, labels):
        # > first trying it with a simple `continue`... 🤞
        if row[t_col] == 'n/a':
            continue

        dep = None
        adds = {'node': label}
        t_dict = row[t_col]
        s_dict = row[s_col]
        if not (s_dict != 'n/a' and t_dict['head'] == s_dict['lemma']):
            print(
                f'ERROR: mismatch between target and source info for {label} node dependency for hit {ix}')
            continue
        # fields = ['head_ix', 'head_lemma', 'head_xpos',
        #           'target_ix', 'target_lemma', 'target_xpos',
        #           'relation', 'node']
        dep = dep_info(head_ix=s_dict.get('ix', -1),
                       head_lemma=t_dict['head'],
                       head_xpos=s_dict.get('xpos', '_'),
                       target_ix=t_dict['ix'],
                       target_lemma=t_dict['lemma'],
                       target_xpos=t_dict['xpos'],
                       relation=t_dict['deprel'],
                       node=label)

        deps['dep_info_' + label] = dep

    hit_deps = pd.DataFrame(deps, index=all_dep_fields
                            ).transpose().convert_dtypes()
    indexer_cols = hit_deps.columns.str.endswith('ix')
    hit_deps.loc[:, indexer_cols] = hit_deps.loc[:, indexer_cols].apply(
        pd.to_numeric, downcast='unsigned')
    hit_deps = hit_deps.sort_values(['head_ix', 'target_ix']).assign(
        contiguous=abs(hit_deps.head_ix - hit_deps.target_ix) == 1)

    full_deps_info[ix] = hit_deps.transpose().to_dict()

    # > add string identifiers, with and without index, but sorted by index
    dep_ix_str[ix] = '; '.join(
        (f"{str(hit_deps.head_ix[i]).zfill(2)}:{hit_deps.head_lemma[i]}{_TIE_STR}"
         f"{str(hit_deps.target_ix[i]).zfill(2)}:{hit_deps.target_lemma[i]}"
         f"_{hit_deps.node[i]}"
         for i in hit_deps.index))
    dep_str[ix] = '; '.join(
        (f"{hit_deps.head_lemma[i]}{_TIE_STR}{hit_deps.target_lemma[i]}_{hit_deps.node[i]}"
         for i in hit_deps.index))

    dep_x_node = hit_deps.copy().set_index('node')

    # for mod, use both xpos
    # for relay, use both xpos
    dep_x_node.loc[dep_x_node.index.isin(('mod', 'relay')), 'dep_str_masked'] = (
        dep_x_node.loc[dep_x_node.index.isin(('mod', 'relay')), 'head_xpos']
        + _TIE_STR
        + dep_x_node.loc[dep_x_node.index.isin(('mod', 'relay')), 'target_xpos'])

    # for neg, use target_lemma and head_xpos (keep neg token)
    dep_x_node.loc['neg', 'dep_str_masked'] = (
        dep_x_node.loc['neg', 'head_xpos']
        + _TIE_STR
        + dep_x_node.loc['neg', 'target_lemma'])

    # for negraise, use target_xpos and head_lemma (keep NR token)
    if 'negraise' in dep_x_node.index:
        dep_x_node.loc['negraise', 'dep_str_masked'] = (
            dep_x_node.loc['negraise', 'head_lemma']
            + _TIE_STR
            + dep_x_node.loc['negraise', 'target_xpos'])
    dep_mask_str[ix] = '; '.join(dep_x_node.dep_str_masked)

    # create named tuples
    dep_id_df = hit_deps[dep_identifiers]
    dep_tuples[ix] = tuple(final_dep._make(dep_id_df.loc[i, :].squeeze())
                           for i in dep_id_df.index)
# %%
dep_df = pd.DataFrame().assign(
    dep_info=pd.Series(full_deps_info),
    dep_str_indexed=pd.Series(dep_ix_str).astype('string'),
    dep_str=pd.Series(dep_str).astype('string'),
    dep_str_masked=pd.Series(dep_mask_str).astype('string'),
    dep_tuple=pd.Series(dep_tuples))

df = df.join(dep_df)

print(df[['dep_str_masked', 'colloc', 'dep_str', 'hit_text']].value_counts().to_frame().rename(
    columns={0: 'count'}).reset_index().to_markdown())

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
boolean_hits = ct_hit_dep.loc[ct_hit_dep.index !='All', 
                              ct_hit_dep.columns != 'All'].astype('boolean')

# %% [markdown]
# I think it may be interesting to see a crosstabulation of the dependency paths with the exact lemmas collapsed.
# For example, instead of `'standard>not_neg; standard>exactly_mod'`, have a series of `'ADJ>not_neg; ADJ>ADV_mod'`
# and crosstabulate that with the collocations (i.e. the `ADJ` and `ADV` token lemmas)
#
# - [x] added this as `dep_str_masked`

# %%
ct_colloc_mask = pd.crosstab(df.colloc, df.dep_str_masked, margins=True)
ct_colloc_mask
# %%
df = df.assign(neg_lemma=df.neg_lemma.str.lower()).loc[df.adv_lemma=='exactly', :]
df.groupby('dep_str_masked')['colloc', 'dep_str'].value_counts()

# %% 
ct_mask_colloc = pd.crosstab(df.dep_str_masked, df.colloc,  margins=True)
ct_mask_colloc
# %%
