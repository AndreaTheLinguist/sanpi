# %% [markdown]
# # Inspecting pickled `bigram` hits

# %% [markdown]
# ## Imports

# %%
import pandas as pd
from pathlib import Path

# %% [markdown]
# ## Define helper functions
# 
# ### Copied from `./source/analyze/utils/`
# jupyter won't import them 🤷‍♀️

# %%
def find_files(data_dir: Path, fname_glob: str, verbose: bool = False):
    path_iter = data_dir.rglob(fname_glob)
    if verbose:
        path_iter = tuple(path_iter)
        print_iter(
            [f'../{p.relative_to(data_dir)}' for p in path_iter], bullet='-',
            header=f'### {len(path_iter)} paths matching {fname_glob} found in {data_dir}')
    return path_iter


def print_iter(iter_obj,
               bullet: str = '▸',
               # //    logger: logging.Logger = None,
               # //    level: int = 20,
               header: str = ''):

    bullet_str = f'\n{bullet} '

    iter_str = bullet_str.join(f'{i}' for i in iter_obj)

    msg_str = f'\n{header}{bullet_str}{iter_str}'
    msg_str = msg_str.replace('\n\n', '\n').strip(f'{bullet} ')

    print(msg_str)


def cols_by_str(df: pd.DataFrame, start_str=None, end_str=None) -> list:
    if end_str:
        cols = df.columns[df.columns.str.endswith(end_str)]
        if start_str:
            cols = cols[cols.str.startswith(start_str)]
    elif start_str:
        cols = df.columns[df.columns.str.startswith(start_str)]
    else:
        cols = df.columns

    return cols.to_list()


def make_cats(orig_df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    df = orig_df.copy()
    if columns is None:
        cat_suff = ("code", "name", "path", "stem")
        columns = df.columns.str.endswith(cat_suff)  # type: ignore
    df.loc[:, columns] = df.loc[:, columns].astype(
        'string').fillna('_').astype('category')

    return df


def balance_sample(full_df: pd.DataFrame,
                   column_name: str = 'category',
                   sample_per_value: int = 5,
                   verbose: bool = False) -> tuple:
    '''
    create sample with no more than n rows satisfying each unique value
    of the given column. A value of -1 for `sample_per_value` will limit
    all values' results to the minimum count per value.
    '''
    info_message = ''
    subsamples = []
    for __, col_val_df in full_df.groupby(column_name):
        # take sample if 1+ and less than length of full dataframe
        if len(col_val_df) > sample_per_value > 0:
            subsample_df = col_val_df.sample(sample_per_value)
            subsamples.append(subsample_df)
        else:
            subsamples.append(col_val_df)

    # > trim all "by column" sub dfs to length of shortest if -1 given
    if sample_per_value == -1:
        trim_len = int(min(len(sdf) for sdf in subsamples))
        subsamples = [sdf.sample(trim_len)
                      for sdf in subsamples]

    b_sample = pd.concat(subsamples)

    if verbose:
        subset_info_table = (
            b_sample
            .value_counts(subset=column_name)
            .to_frame(name='count')
            .assign(percentage=b_sample
                    .value_counts(column_name, normalize=True)
                    .round(2) * 100)
            .to_markdown())
        label = (full_df.hits_df_pkl[0].stem + ' '
                 if 'hits_df_pkl' in full_df.columns
                 else '')
        info_message = (f'\n## {column_name} representation in {label}sample\n'
                        + subset_info_table)

    return b_sample, info_message


def concat_pkls(data_dir: Path = Path('/share/compling/data/sanpi/2_hit_tables'),
                fname_glob: str = '*.pkl.gz',
                pickles=None,
                convert_dtypes=False,
                verbose: bool = True) -> pd.DataFrame:
    if not pickles:
        pickles = find_files(Path(data_dir), fname_glob, verbose)

    # tested and found that it is faster to assign `corpus` intermittently
    sep_dfs = []
    for p in pickles:
        df = (pd.read_pickle(p).assign(corpus=p.stem.rsplit('_', 2)[0]))
        df = df.loc[:, 
                    cols_by_str(
            df, end_str=('lemma', 'id', 'text', 'window', 'category', 'Pol', 'sent')) + cols_by_str(df, start_str=('corpus', 'lemma'))]
        df = df.convert_dtypes()

        dup_check_cols = cols_by_str(df, end_str=('text', 'id', 'sent'))
        df = (df.loc[~df.duplicated(subset=dup_check_cols), :])
        sep_dfs.append(df)
    
    c_df = pd.concat(sep_dfs)    
    dup_check_cols = cols_by_str(c_df, end_str=('text', 'id', 'sent'))
    c_df = (c_df.loc[~c_df.duplicated(subset=dup_check_cols), :])
    c_df = make_cats(c_df, (['corpus'] + cols_by_str(c_df, start_str=('nr', 'neg', 'adv'),
                                                 end_str=('lemma', 'form'))))

    return c_df

# %% [markdown]
# ### copied from `./source/analyze_deps.py`:

# %%
def _optimize_df(df: pd.DataFrame) -> pd.DataFrame:

    # print('Original Dataframe:')
    # df.info(memory_usage='deep')

    # > drop unneeded string columns
    # was:
    #   for c in udf.cols_by_str(df, start_str=('context', 'text', 'sent_text', 'token')):
    for c in cols_by_str(df, start_str=('context', 'token', 'utt')):
        df.pop(c)

    # > select only non-`object` dtype columns
    relevant_cols = df.columns[~df.dtypes.astype(
        'string').str.endswith(('object'))]
    # limit df to `relevant_cols`
    df = df[relevant_cols]

    # > create empty dataframe with `relevant_cols` as index/rows
    df_info = pd.DataFrame(index=relevant_cols)

    df_info = df_info.assign(
        mem0=df.memory_usage(deep=True),
        dtype0=df.dtypes.astype('string'),
        defined_values=df.count(),
        unique_values=df.apply(pd.unique, axis=0).apply(len))
    df_info = df_info.assign(
        ratio_unique=(df_info.unique_values/df_info.defined_values).round(2))

    cat_candidates = df_info.loc[df_info.ratio_unique < 0.8,
                                 :].loc[df_info.dtype0 != 'category'].index.to_list()
    #was: catted_df = udf.make_cats(df.copy(), cat_candidates)
    catted_df = make_cats(df.copy(), cat_candidates)

    df_info = df_info.assign(dtype1=catted_df.dtypes,
                             mem1=catted_df.memory_usage(deep=True))
    df_info = df_info.assign(mem_change=df_info.mem1-df_info.mem0)
    print(df_info.sort_values(
        ['mem_change', 'ratio_unique', 'dtype0']).to_markdown())
    mem_improved = df_info.loc[df_info.mem_change < 0, :].index.to_list()
    for c in df.columns[~df.columns.isin(mem_improved)]:
        print(c, '\t', df.loc[:, c].dtype)
    df.loc[:, mem_improved] = catted_df.loc[:, mem_improved]
    print('Category Converted dataframe:')
    df.info(memory_usage='deep')

    return df

# %% [markdown]
# ### Newly created

# %%
def show_counts(df, columns):
    return df.value_counts(columns).to_frame().rename(columns={0: 'count'})

def summarize_text_cols(text_df: pd.DataFrame):

    summary = text_df.describe().transpose()
    summary = summary.assign(top_percent=(
        ((pd.to_numeric(summary.freq) / len(text_df)))*100).round(2))
    summary = summary.rename(columns={'top': 'top_value', 'freq': 'top_freq'})

    return summary.convert_dtypes().sort_values('unique')

# %% [markdown]
# ## Load Data

# %%
def select_pickles():
    pickle_dir = Path(
        '/share/compling/data/sanpi/2_hit_tables/')
    # > make dataframe to load smallest files first (for testing)
    pickles = pd.DataFrame(pickle_dir.rglob(
        'bigram-*hits.pkl.gz'), columns=['path'])
    pickles = pickles.assign(size=pickles.path.apply(lambda f: f.stat().st_size))
    pickles = pickles.sort_values('size')
    print_pkl_df = pickles.reset_index().astype('string')
    print(pd.concat([print_pkl_df.head(5), print_pkl_df.tail(5)]).to_markdown())
    #HACK : limiter for faster testing
    pkl_paths = pickles.loc[pickles.path.apply(
        lambda x: x.name.startswith(tuple('bigram-'+c for c in ('Apw','Nyt1','PccTe', 'PccVa','Pcc06')))), 'path'].squeeze().to_list()
    print_iter(pkl_paths, header=f'\n※ testing! Hit dataframes limited to: {len(pkl_paths)} files')
    return pkl_paths

hit_pkls = select_pickles()


# %%
ddf = concat_pkls(pickles=hit_pkls, convert_dtypes=True)
# ddf = concat_pkls(pickles=hit_pkls[:50], convert_dtypes=True)

# %% [markdown]
# ### Optimize DataFrame

# %%
odf = _optimize_df(ddf)

# %%
columns = odf.columns[~odf.columns.isin(cols_by_str(
    odf, start_str=('dep_m', 'dep_n', 'dep_r', 'context')))].to_list()
columns.sort()
odf = odf.loc[:, columns]
len(odf) == len(ddf)


# # %% [markdown]
# # ⚠️ remove `any-direct` hits with `x_...` values filled

# # %%
# if 'x_form' in odf.columns: 
#     x_cols = cols_by_str(odf, start_str='x')
#     print(x_cols)

#     odf = odf.loc[odf.x_form == '_', ~odf.columns.isin(x_cols)]

# %%
odf.loc[odf.corpus.str.contains('Pcc'), 'corpus_group'] = 'puddin'
odf.loc[odf.corpus.str.endswith(('Nyt1', 'Nyt2', 'Apw')), 'corpus_group'] = 'news'

general_counts = show_counts(odf, ['category', 'corpus_group'])

general_counts = general_counts.unstack()
general_counts = general_counts.sort_values(('count', 'puddin'), ascending=False)  # type: ignore
print(general_counts)

# %% [markdown]
# ### Add `conllu_id` and drop unused columns

# %%
tdf = odf.assign(conllu_id=odf.sent_id.str.rsplit('_', 2).str.get(0).str.split(
    '.').str.get(0).astype('string').astype('category'))  # type: ignore
print(f'Total hits for all patterns: {len(tdf)}')
#// tdf = odf[cols_by_str(odf, end_str=('lemma', 'id', 'text', 'window',
#//                       'category', 'Pol')) + cols_by_str(odf, start_str=('corpus', 'lemma'))]



# %% [markdown]
# ## Identify $PosPol$ and $NegPol$ contexts

# %% [markdown]
# ### Option A
# bare collocation tokens (`advadj.all-RB-JJs` pattern match) which do not appear as matches for any other pattern match (i.e. $NegPol$ contexts).
# 
# *That is, the `colloc_id` (unique `ADV` & `ADJ` nodes in unique sentence tokens) is not duplicated.*
# 
# ```{python}
# tdfp_a = tdf.loc[(tdf.category=='advadj') & (~tdf.duplicated(subset='colloc_id', keep=False)), :]
# ```
# 
# ### Option B
# categorize $NegPol$ set first (`tdfn`), then compute complement of that (i.e. $ALL - NegPol$)
# 
# ```{python}
# tdfn = tdf.loc[tdf.neg_lemma!='_', :]
# tdfp = tdf.loc[~tdf.colloc_id.isin(tdfn.colloc_id), :]
# ```
# 
# ### Options A and B are identical
# 
# `all(tdfp_a.index == tdfp_b.index)` evaluates as true
# 
# So, since $NegPol$ is more directly defined, and has to be separated out anyway, it's simpler to just get the "complement", (`tdfp_b` method)

# %%
tdfn = tdf.loc[tdf.neg_lemma != '_', :]
tdfp = tdf.loc[~tdf.colloc_id.isin(tdfn.colloc_id), :]


## %%
print(tdfn[['neg_lemma', 'adv_lemma', 'adj_lemma', 'hit_text', 
      'text_window', 
    #   'sent_text'
      ]].sample(25).to_markdown())

#%%
summarize_text_cols(tdf).to_csv('/share/compling/projects/sanpi/notebooks/bigram_out/all_df_summary.csv')
summarize_text_cols(tdfn).to_csv('/share/compling/projects/sanpi/notebooks/bigram_out/neg_df_summary.csv')
summarize_text_cols(tdfp).to_csv('/share/compling/projects/sanpi/notebooks/bigram_out/pos_df_summary.csv')


# %% [markdown]
# ## Assign `polarity` and recombine

# %%
tdfp = tdfp.assign(polarity='positive')
tdfn = tdfn.assign(polarity='negative')
tdfn.to_pickle('/share/compling/projects/sanpi/notebooks/bigram_out/NegPol_ALL.pkl.gz')
tdf_with_overlap = tdf
pol_union_df = pd.concat([tdfp, tdfn]).sort_values('colloc_id')

print(
    f'Total bare collocations: {odf.category.value_counts()["advadj"]}')
print(
    f'Total pattern hits (+ NegPol pattern overlap): {len(pol_union_df)}')
print(f'PosPol: {round(100*len(tdfp)/len(pol_union_df))}% : {len(tdfp)} hits')
print(
    f'NegPol: {str(round(100*len(tdfn)/len(pol_union_df))).zfill(2)}% : {len(tdfn)} hits')


# %% [markdown]
# ### Pickle Pos+Neg Dataframe

# %%
# pol_union_df.to_pickle(
#     '/share/compling/projects/sanpi/notebooks/bigram_out/all-exactly-hits_text+polarity.pkl.gz')


# %% [markdown]
# ## Frequency by Polarity

# %% [markdown]
# ### Simple Frequency Comparison

# %%
try: 
    top_200 = pd.read_csv('/share/compling/projects/sanpi/notebooks/bigram_out_full/top_200.csv')
except: 
    top_200 = show_counts(pol_union_df, ['polarity', 'adj_lemma']).head(200)
    top_200.to_csv('/share/compling/projects/sanpi/notebooks/bigram_out/top_200.csv')
print(top_200.to_markdown())


# %%
try: 
    top_200_neg = pd.read_csv('/share/compling/projects/sanpi/notebooks/bigram_out_full/top_200_neg.csv')
except:
    top_200_neg = show_counts(pol_union_df.loc[pol_union_df.polarity=='negative', :], ['polarity', 'adj_lemma']).head(200)
    top_200_neg.to_csv('/share/compling/projects/sanpi/notebooks/bigram_out/top_200_neg.csv')
top_200_neg


# %%
spread_top_200 = top_200.unstack(level='polarity', fill_value=0)
spread_top_200.sort_values(('count', 'negative'),
                           ascending=False).head(30)  # type: ignore


# %%
spread_top_200.sort_values(('count', 'positive'),
                           ascending=False).head(30)  # type: ignore


# %% [markdown]
# ### Crosstabulate adjective by context polarity


# %%
try: 
    freq_thresh5 = pd.read_csv(
    '/share/compling/projects/sanpi/notebooks/bigram_out_full/freq_thresh5.csv')
except: 
    freq_dist = pd.crosstab(pol_union_df.adj_lemma,
                        pol_union_df.polarity,
                        margins=True, margins_name='TOTAL')

    freq_dist = freq_dist.assign(
        ratio_neg=(freq_dist.negative/freq_dist.TOTAL).round(3),
        ratio_pos=(freq_dist.positive/freq_dist.TOTAL).round(3))

    freq_dist = freq_dist.assign(
        bin_neg=freq_dist.ratio_neg.round(1),
        bin_pos=freq_dist.ratio_pos.round(1))

    cols = freq_dist.columns.to_list()
    cols.pop(cols.index('TOTAL'))
    freq_dist = freq_dist[['TOTAL'] + cols]

    print(freq_dist.sort_values('TOTAL', ascending=False).head(10))
    
    freq_thresh5 = freq_dist.loc[freq_dist.TOTAL >= 5, :]
    freq_thresh5 = freq_thresh5.sort_values(
        ['bin_neg', 'TOTAL', 'ratio_neg'], ascending=False)
    freq_thresh5.to_csv(
        '/share/compling/projects/sanpi/notebooks/bigram_out/freq_thresh5.csv')
freq_thresh5


# %%
try: 
    freq_thresh100 = pd.read_csv(
    '/share/compling/projects/sanpi/notebooks/bigram_out_full/freq_thresh100.csv')
except: 
    freq_thresh100 = freq_dist.loc[freq_dist.TOTAL >= 100, :]
    freq_thresh100 = freq_thresh100.sort_values(
        ['ratio_neg','TOTAL', 'bin_neg', ], ascending=False)
    freq_thresh100.to_csv(
        '/share/compling/projects/sanpi/notebooks/bigram_out/freq_thresh100.csv')
freq_thresh100


# %%
try: 
    freq_thresh200 = pd.read_csv(
    '/share/compling/projects/sanpi/notebooks/bigram_out_full/freq_thresh200.csv')
except: 
    freq_thresh200 = freq_dist.loc[freq_dist.TOTAL >= 200, :]
    freq_thresh200 = freq_thresh200.sort_values(
        ['bin_neg', 'TOTAL', 'ratio_neg'], ascending=False)
    freq_thresh200.to_csv(
        '/share/compling/projects/sanpi/notebooks/bigram_out/freq_thresh200.csv')
freq_thresh200


# %%
freq_dist = freq_thresh5


# %%
freq_dist.ratio_neg.plot(kind='hist')

# %%
freq_dist.loc[freq_dist.index!='TOTAL', ['negative', 'positive']].plot(x='negative', y ='positive', kind='scatter')

## %%
freq_dist.loc[freq_dist.index!='TOTAL', ['negative', 'positive']].plot(x='negative', y ='positive', kind='density')

# %%
freq_dist.ratio_pos.plot(kind='hist')

# %% [markdown]
# ## Save $PosPol$ text data
# 
# Since $PosPol$ is defined as the complement of $NegPol$, accuracy relies on $NegPol$ catching all relevant cases.
# 
# To ensure pattern specifications are sufficiently inclusive, all sentences with supposedly positive polarity
# should be manually inspected for any errant (uncaught) negative lemmas, as identified in the $NegPol$ pattern specifications.
# 
# ```{ocaml}
# NEG [lemma="hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
# ```
# 
# - [x] create simplified output of $PosPol$/`tdfp` sentence text data, with necessary identifiers
# - [x] save as csv
# - [ ] grep `pos_sentences.csv` for each neg lemma:\
#   *There should not be any negative lemmas an `exactly JJ` collocation in its scope.*
# 

# # %%
# select_cols = ['adj_lemma', 'text_window', 'sent_text',
#                'sent_id', 'conllu_id', 'corpus']
# pos_text_info = tdfp.loc[:, select_cols]
# pos_text_info = pos_text_info.assign(
#     adj_neg_ratio=pos_text_info.adj_lemma.apply(lambda a: freq_dist.loc[a, 'ratio_neg'] if a in freq_dist.index else None))  # type: ignore
# pos_text_info.sort_values(['adj_neg_ratio', 'conllu_id'], ascending=False)
# pos_text_info.to_csv(
#     '/share/compling/projects/sanpi/notebooks/bigram_out/pos_sentences.csv')

# tdfp.adj_lemma[~tdfp.adj_lemma.isin(freq_dist.index)].value_counts()
# TODO?? why does it say there is a mismatch between the crosstab and pospol adj set?
# ^ 🤔 probably something to do with categorical dtype


# %%
freq_thresh5.describe().round(2)

# %%
# pol_union_thresh5 = pol_union_df.loc[pol_union_df.adj_lemma]
adj_x_cat = (pd.crosstab(index=pol_union_df.adj_lemma, columns=pol_union_df.category, 
                         margins=True, margins_name='TOTAL', normalize='index')
             .rename(columns={'advadj':'PosPol', 'contig':'contig_NegPol', 
                              'raised': 'raised_NegPol', 'scoped':'scoped_NegPol'})
             .round(3))
adj_x_cat.loc[adj_x_cat.index.isin(freq_thresh200.index), :]

# %%
adj_x_neg = pd.crosstab(index=pol_union_df.adj_lemma,
                        columns=pol_union_df.neg_lemma, margins=True)
adj_x_neg.nlargest(20, columns=['All'])



