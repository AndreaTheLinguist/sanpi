# %% [markdown]
# # Compilation of All Counts for <font color=DodgerBlue><u>*Original Corpora*</u></font> & <font color=Brown><u>***BiRC***</u></font>
# ___`BiRC`___ $=\text{``bigram restricted corpus'' or }\texttt{bigram\_subset}$
# %% [markdown]
# ### *imports*
from pathlib import Path
import pandas as pd
from am_notebooks import *

#! Toggle TESTING
TESTING = False
if TESTING:
    print(
        '🚨⚠️ WARNING!\n  This is a **TEST** run!'
        'Full count data will not be loaded or saved\n'
    )

# // from utils import file_size_round
SUBSET_DATA_DIR = Path('/share/compling/data/sanpi/subsets')
print(
    '==============================\n'
    f'Date: {pd.Timestamp.now().ctime()}\n'
    '=============================='
)

BIRC_INFO_DIR = SANPI_HOME.joinpath('info/BiRC')
confirm_dir(BIRC_INFO_DIR)
BIRC_META_CSV = BIRC_INFO_DIR.joinpath('meta-info-full.csv')
REL_BIRC_TEX_DIR = 'ch6/BiRC'
BIRC_TEX_DIR = LATEX_TABLES.joinpath(REL_BIRC_TEX_DIR)
confirm_dir(BIRC_TEX_DIR)
# %% [markdown]
# ## **Define functions** to compile all the disparate meta info...


def collect_subset_path_index():
    """Collect subset path index information.

    This function gathers information about subset paths, including parent directory,
    name, full path, source path (from symlink), BiRC subcorpus, size, and other
    relevant details. It then processes this information to create a DataFrame with
    additional derived columns, such as 'init_conllu', 'data_key', 'corpus_part',
    'corpus', 'subset_info_dir', and 'path_index_csv'.

    Returns:
        pd.DataFrame: A DataFrame containing the collected subset path index info.
    """
    data = {p.stem:
            {
                'parent': p.parent.name,
                'name': p.name,
                'path': p,
                'source_path': p.readlink(),
                'birc_subcorpus': p.parent.parent.stem,
                'is_link': p.is_symlink(),
                # 'size': file_size_round(p.stat().st_size),
                'size': p.stat().st_size,  # ! no longer forcing into different units
            }
            for p in SUBSET_DATA_DIR.rglob('*.conllu')
            #! to prevent *DEMO* files being included:
            if not p.parent.name.startswith('bigram-DEMO')
            }
    bp_df = pd.DataFrame.from_dict(data, orient='index').convert_dtypes()
    bp_df
    bp_df['init_conllu'] = bp_df.name.str.replace('BIGRAM.', '', regex=False)
    bp_df['data_key'] = bp_df.index.str.replace('BIGRAM.', '', regex=False)

    bp_df['corpus_part'], bp_df['corpus'], bp_df['subset_info_dir'] = zip(
        *bp_df.source_path.apply(
            lambda sp: (sp.parent.parent.stem,
                        sp.parent.parent.parent.stem,
                        sp.parent.joinpath('info')))
    )
    bp_df = bp_df.convert_dtypes()

    set_my_style(bp_df.sample(1).T)

    bp_df['path_index_csv'] = bp_df.subset_info_dir.apply(
        lambda i: max(i.glob('subset-bigram_path-index*csv'),
                      key=lambda file: file.stat().st_ctime))

    try:
        path_info = pd.read_csv(X.path_index_csv,
                                usecols=['STEM', ' INPUT_COUNTS',
                                         ' SUBSET_COUNTS']
                                ).set_index('STEM')
    except ValueError:
        path_info = pd.read_csv(X.path_index_csv,
                                usecols=['STEM', 'INPUT_COUNTS',
                                         'SUBSET_COUNTS']
                                ).set_index('STEM')

    path_info.columns = path_info.columns.str.strip().str.lower()
    path_info.columns

    for stem in path_info.sample(3).T:
        print(f'- {stem}')
        print(f'  - input_counts = {path_info.input_counts[stem]}')
        print(f'  - subset_counts = {path_info.subset_counts[stem]}')

    bp_df.index.name = 'subset_stem'
    return bp_df.reset_index().set_index('data_key')


def collect_meta_info(_bp_df):
    """Collect metadata information from various sources.

    This function groups the input DataFrame by 'path_index_csv', reads data from
    corresponding CSV files, joins the data with the original DataFrame, and
    concatenates the results into a single DataFrame. It also performs some
    string cleaning on the resulting DataFrame's columns.

    Args:
        _bp_df (pd.DataFrame): DataFrame containing file paths and other info.

    Returns:
        pd.DataFrame: A DataFrame containing the combined metadata information.
    """
    subframes = []
    for path_ix, df in _bp_df.groupby('path_index_csv'):
        print(path_ix)
        if 'DEMO' in str(path_ix):
            continue
        try:
            path_info = pd.read_csv(
                path_ix,
                usecols=['STEM', ' INPUT_COUNTS', ' SUBSET_COUNTS']
            ).set_index('STEM')
        except ValueError:
            path_info = pd.read_csv(
                path_ix,
                usecols=['STEM', 'INPUT_COUNTS', 'SUBSET_COUNTS']
            ).set_index('STEM')
        nb_display(set_my_style(df.head(1).T, caption=str(
            path_ix.relative_to('/share/compling/data'))))
        subframes.append(df.join(path_info))

    meta_df = pd.concat(subframes)
    meta_df.iloc[:, -2:] = meta_df.iloc[:, -2:].apply(lambda x: x.str.strip())
    meta_df.columns = meta_df.columns.str.strip().str.lower()
    return meta_df
#  %% [markdown]
# ## **Create or read meta info**


if BIRC_META_CSV.is_file():
    meta_df = pd.read_csv(BIRC_META_CSV, index_col='data_key').convert_dtypes()
    print(f'Meta Info DataFrame loaded from "{BIRC_META_CSV}"')
else:
    bp_df = collect_subset_path_index()
    meta_df = collect_meta_info(bp_df)
    meta_df.to_csv(BIRC_META_CSV)

set_my_style(
    meta_df.head(1).T,
    caption='First Line of Meta DataFrame')

# %% [markdown]
# ## *Define functions* to retrieve count data


def load_totals(counts_path):
    """Load total counts from a JSON file.

    This function reads a JSON file containing counts data, extracts the 'total'
    column, drops any missing values (NaN), and returns the result as a dictionary.
    If the provided path is not absolute, it prepends the sanpi data directory.

    Args:
        counts_path (str or Path): Path to the JSON file.

    Returns:
        dict: A dictionary containing the total counts, with keys corresponding to
            the original index of the 'total' column.
    """

    if not Path(counts_path).is_absolute():
        counts_path = f"/share/compling/data/sanpi/{counts_path}"
    counts_df = pd.read_json(counts_path)
    return counts_df.loc[:, 'total'].dropna().to_dict()


def generate_counts(_meta_df, retrieval_key='input'):
    """Generate counts for each data key.

    This generator iterates through the index of the input DataFrame, retrieves the
    counts path based on the retrieval key, and yields the data key along with its
    corresponding counts.

    Args:
        _meta_df (pd.DataFrame): DataFrame containing metadata information.
        retrieval_key (str, optional): Key used to retrieve the counts path.
            Defaults to 'input'.

    Yields:
        tuple: A tuple containing the data key and its corresponding counts.
    """
    for data_key in _meta_df.index:
        counts_path = _meta_df.at[data_key, f'{retrieval_key}_counts']
        yield data_key, load_totals(counts_path)


def retrieve_count_data(_counts_csv_path, _meta_df, test=False):
    seek_birc = "birc" in _counts_csv_path.name.lower()
    _counts_label = "BiRC" if seek_birc else "Original"
    if _counts_csv_path.is_file():
        try:
            _counts_df = pd.read_csv(_counts_csv_path,
                                     index_col='corpus_slice').convert_dtypes()
        except ValueError:
            _counts_df = pd.read_csv(_counts_csv_path).convert_dtypes()

        print(
            f'**{_counts_label} Counts** read from csv',
            f'> Path: {_counts_csv_path.relative_to(SANPI_HOME)}',
            sep='\n')
    else:
        _meta_selection = _meta_df.copy().sample(100) if test else _meta_df.copy()
        _counts_df = pd.DataFrame.from_dict(
            {k: c for k, c in generate_counts(
                _meta_df=_meta_selection,
                retrieval_key='subset' if seek_birc else 'input')},
            orient='index')
        _counts_df.index.name = 'corpus_slice'
        _counts_df = _counts_df.reset_index().convert_dtypes().set_index('corpus_slice')
        print(
            f'**{_counts_label} Counts** saved as csv',
            f'> Path: {_counts_csv_path.relative_to(SANPI_HOME)}',
            sep='\n')
        if test:
            print('TESTING (so, not really)')
        else:
            _counts_df.to_csv(_counts_csv_path)
    return _counts_df.loc[:, ~_counts_df.columns.str.startswith('NR_')]


# %% [markdown]
# ## **Load <font color=DodgerBlue><u>Original</u></font> counts** (if not previously collected)
orig_counts_df = retrieve_count_data(
    _counts_csv_path=BIRC_INFO_DIR.joinpath('original-count-data.csv'),
    _meta_df=meta_df,
    test=TESTING
)

orig_counts_df.info()

# %% [markdown]
# ## **...and <font color=Brown><u>BiRC</u></font> counts** (likewise)
birc_counts_df = retrieve_count_data(
    _counts_csv_path=BIRC_INFO_DIR.joinpath('birc-count-data.csv'),
    _meta_df=meta_df,
    test=TESTING
)

birc_counts_df.info()
# if birc_counts_composite_csv.is_file():
#     birc_counts_df = pd.read_csv(birc_counts_composite_csv).convert_dtypes()
#     print(
#         f'**BiRC Counts** read from csv\n> Path: {birc_counts_composite_csv.relative_to(SANPI_HOME)}')
# else:
#     birc_counts_df = pd.DataFrame.from_dict(
#         # {k:c for k,c in generate_counts(meta_df.head(500), 'subset')}, orient='index')
#         {k: c for k, c in generate_counts(meta_df, 'subset')}, orient='index')
#     pd.to_csv(birc_counts_composite_csv)
#     print(
#         f'**BiRC Counts** saved as csv\n> Path: {birc_counts_composite_csv.relative_to(SANPI_HOME)}')

# %% [markdown]
# ## *Describe Count Collections*

save_latex_table(orig_counts_df.describe().T.iloc[:, 1:].assign(Total=orig_counts_df.sum()).convert_dtypes(),
                 caption='Original Corpora: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='init-descrip-stats-orig')

save_latex_table(birc_counts_df.describe().T.iloc[:, 1:].assign(Total=birc_counts_df.sum()).convert_dtypes(),
                 caption='BiRC: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='init-descrip-stats-birc')
# %%


def add_rate_cols(_df):
    return _df.assign(
        tok_per_sent=_df.tokens / _df.sentences,
        ADV_tok_per_sent=_df.ADV_tokens / _df.sentences,
        ADJ_tok_per_sent=_df.ADJ_tokens / _df.sentences,
        NEG_tok_per_sent=_df.NEG_tokens / _df.sentences,
        NEG_tok_per_mill=(_df.NEG_tokens / _df.tokens)*(10**6),
        ADV_tok_per_mill=(_df.ADV_tokens / _df.tokens)*(10**6),
        ADJ_tok_per_mill=(_df.ADJ_tokens / _df.tokens)*(10**6),
        ADV_form_per_lemma=_df.ADV_forms / _df.ADV_lemmas,
        # ADV_lemma_per_form= _df.ADV_lemmas / _df.ADV_forms,
        ADV_tok_per_lemma=_df.ADV_tokens / _df.ADV_lemmas,
        ADV_tok_per_form=_df.ADV_tokens / _df.ADV_forms,
        ADJ_form_per_lemma=_df.ADJ_forms / _df.ADJ_lemmas,
        # ADJ_lemma_per_form= _df.ADJ_lemmas / _df.ADJ_forms,
        ADJ_tok_per_lemma=_df.ADJ_tokens / _df.ADJ_lemmas,
        ADJ_tok_per_form=_df.ADJ_tokens / _df.ADJ_forms,
        # NEG_lemma_per_form= _df.NEG_lemmas / _df.NEG_forms,
        NEG_form_per_lemma=_df.NEG_forms / _df.NEG_lemmas,
    )


orig_counts_df = add_rate_cols(orig_counts_df)
birc_counts_df = add_rate_cols(birc_counts_df)
samix = orig_counts_df.sample(4).sort_index().index
nb_display(set_my_style(orig_counts_df.filter(
    like='per').loc[samix, :].T, caption='"Rate" columns for Original Counts'))
nb_display(set_my_style(birc_counts_df.filter(
    like='per').loc[samix, :].T, caption='"Rate" columns for BiRC Counts'))
# %%
save_latex_table(orig_counts_df.describe().T.iloc[:, 1:].assign(Total=orig_counts_df.sum()).convert_dtypes(),
                 caption='Original Corpora Counts & Rates: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='plus-rates-descrip-stats-orig')

save_latex_table(birc_counts_df.describe().T.iloc[:, 1:].assign(Total=birc_counts_df.sum()).convert_dtypes(),
                 caption='BiRC Counts & Rates: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='plus-rates-descrip-stats-birc')

save_latex_table(orig_counts_df.filter(like='per').describe().T.iloc[:, 1:].assign(Total=orig_counts_df.sum()).convert_dtypes(),
                 caption='Original Corpora Rates: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='only-rates-descrip-stats-orig')

save_latex_table(birc_counts_df.filter(like='per').describe().T.iloc[:, 1:].assign(Total=birc_counts_df.sum()).convert_dtypes(),
                 caption='BiRC Rates: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='only-rates-descrip-stats-birc')
# %% [markdown]
# ## *Calculate **Reduction*** (<code>BiRC - Full</code>)
reduction_df = birc_counts_df - orig_counts_df
# iloc[:, 1:] drops the uninformtative `count` column
save_latex_table(reduction_df.describe().T.iloc[:, 1:].assign(Total=reduction_df.sum()).convert_dtypes(),
                 caption='Reduction (BiRC -- Full) Counts & Rates: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='plus-rates-birc-minus-full-descrip-stats')
save_latex_table(reduction_df.filter(like='per').describe().T.iloc[:, 1:].assign(Total=reduction_df.sum()).convert_dtypes(),
                 caption='Reduction (BiRC -- Full) Rates: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='only-rates-birc-minus-full-descrip-stats')
# nb_display(set_my_style(reduction_df.describe().T.assign(Total=reduction_df.sum()).convert_dtypes(),
#                         caption='BiRC <i>Reduction</i>: Descriptive Stats', precision=1))
nb_display(set_my_style(reduction_df.filter(
    like='per').loc[samix, :].T, caption='"Rate" columns for <code>BiRC - Full</code> counts'))
# %%


def reconfigure_counts(_counts_df, count_kind: str):
    return _counts_df.assign(
        kind=count_kind
    ).reset_index().set_index(['kind', 'corpus_slice']).unstack('kind')


orig_s = reconfigure_counts(orig_counts_df, count_kind='Full')
birc_s = reconfigure_counts(birc_counts_df, 'BiRC')
diff_s = reconfigure_counts(reduction_df, 'diff')
juxta = orig_s.join(birc_s).join(diff_s).convert_dtypes().sort_index(axis=1)

# juxta = orig_counts_df.join(birc_counts_df, rsuffix=':BiRC', lsuffix=':Full').join(reduction_df.add_suffix(':diff')).convert_dtypes()
juxta_desc = juxta.describe().iloc[1:, :]
juxta_desc.loc['TOTAL', :] = juxta.sum()
juxta_desc.index = juxta_desc.index.str.upper()
juxta_desc.loc['CV%', :] = (
    (juxta_desc.T.STD / juxta_desc.T.MEAN).fillna(0) * 100)
save_latex_table(juxta_desc.T.convert_dtypes(),
                 caption='Juxtaposed BiRC: Descriptive Stats', verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='birc-juxtaposed-descrip-stats-complete')

# juxta = pd.concat([juxta, juxta_desc])
# juxtaT = juxta.T.assign(TOTAL=juxta.sum(), MEAN=juxta.mean(), MEDIAN=juxta.median(),
#                         MAX=juxta.max(), MIN=juxta.min(),
#                         STD=juxta.std())
# juxta = juxtaT.sort_index().T.sort_index()
juxta = juxta.assign(
    corpus=juxta.index.to_series().str[:3].map(
        {'apw': 'News', 'nyt': 'News', 'pcc': 'Puddin'}).astype('category'))
juxta = juxta.reset_index().set_index(['corpus']+juxta.index.names)
juxta = juxta.sort_index().sort_index(axis=1)

# %%
full_juxta_csv = BIRC_INFO_DIR.joinpath('juxtaposed-counts-and-rates.csv')
if not full_juxta_csv.is_file():
    juxta.stack().reset_index().to_csv(full_juxta_csv)

# %%
save_latex_table(
    pd.concat([
        juxta.filter(like='apw', axis=0).sample(1),
        juxta.filter(like='nyt', axis=0).sample(1),
        # 👆 to ensure at least one sample of apw  and news are included
        juxta.sample(8)
    ]).drop_duplicates().sort_index().T,
    caption=('Sample of Juxtaposed Counts'),
    verbose=True,
    latex_subdir=REL_BIRC_TEX_DIR,
    latex_stem='birc-juxtaposed-sample')

# %%
sent_tok_summary = juxta_desc.filter(
    [(c, o) for c, o in it.product(['sentences', 'tokens'], ['BiRC', 'Full'])])

# sent_tok_summary.columns = sent_tok_summary.columns.reorder_levels([1,0])
save_latex_table(sent_tok_summary.sort_index().sort_index(axis=1),
                 caption=('Comparing BiRC to Full Corpora: sentences & tokens'),
                 verbose=True,
                 latex_subdir=REL_BIRC_TEX_DIR,
                 latex_stem='birc-juxtaposed-sent-tok-summary')
# %% [ markdown ] ## By Corpus **Part** (rather than *slice*)


def describe_and_total(_df):
    return _df.describe().T.assign(total=_df.sum()).T


by_corpus_descrip = juxta.groupby(
    'corpus', observed=True).apply(describe_and_total)
by_corpus_descrip.index.names = ['corpus', 'stat']
by_corpus_descrip.columns.names = ['obs', 'kind']

by_corpus_descrip = (
    by_corpus_descrip
    .stack(['obs', 'kind'])
    .unstack(['corpus', 'kind', 'stat'])
    .stack('stat')
    .rename(index={
            'count': '# files',
            '50%': 'median'}))
save_latex_table(
    by_corpus_descrip.xs('file_MB').style,
    caption=('BiRC Storare Size (MB) Comparison by Corpus '),
    verbose=True,
    latex_subdir=REL_BIRC_TEX_DIR,
    latex_stem='birc-by-corpus-size-compare-summary'
)
# %%
save_latex_table(
    by_corpus_descrip.xs('tokens').style,
    caption=('BiRC Token Comparison by Corpus '),
    verbose=True,
    latex_subdir=REL_BIRC_TEX_DIR,
    latex_stem='birc-by-corpus-token-compare-summary'
)
# %%
save_latex_table(
    by_corpus_descrip.xs('sentences').style,
    caption=('BiRC Sentence Comparison by Corpus '),
    verbose=True,
    latex_subdir=REL_BIRC_TEX_DIR,
    latex_stem='birc-by-corpus-sentence-compare-summary'
)


# %%
for cue in ['ADV_tok', 'ADJ_tok', 
            'ADV_lemma', 'ADJ_lemma', 
            'ADV_form', 'ADJ_form', 
            'NEG_tok']:
    save_latex_table(by_corpus_descrip.filter(like=cue, axis=0),
                     caption=f'BiRC {cue} Comparisons: By Corpus', verbose=True,
                     latex_subdir=REL_BIRC_TEX_DIR,
                     latex_stem=f'birc-by-corpus-summary-{cue}')
    save_latex_table(juxta_desc.filter(like=cue),
                     caption=f'BiRC {cue} Comparisons', verbose=True,
                     latex_subdir=REL_BIRC_TEX_DIR,
                     latex_stem=f'birc-juxta-summary-{cue}')
    # save_latex_table(by_corpus_descrip.filter(like=cue, axis=0).iloc[:9, :],
    #                  caption=f'BiRC {cue} Comparison Summary', verbose=True,
    #                  latex_subdir=REL_BIRC_TEX_DIR,
    #                  latex_stem=f'birc-juxtaposed-{cue}-summary')

# %%
