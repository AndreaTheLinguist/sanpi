# %%
import pandas as pd

from source.utils import SANPI_HOME, FREQ_DIR, RESULT_DIR, UCS_DIR, confirm_dir
from source.utils.associate import (BINARY_ASSOC_ARGS, add_extra_am,
                                    associate_ucs, confirm_basic_ucs)
from source.utils.associate import convert_ucs_to_csv as ucs2csv
from source.utils.associate import get_associations_csv as init_am, AM_DF_DIR
from source.utils.associate import manipulate_ucs, seek_readable_ucs, adjust_am_names
pd.set_option('display.float_format', '{:,.2f}'.format)

# %% [markdown]
# 🧮 set parameters

# %%
UNIT = 'Adj'
TAG = 'ALL'
# PAT_DIR = 'POSmirror'
# PAT_DIR = 'NEGmirror'
# PAT_DIR = 'ANYmirror'
PAT_DIR_NAME = 'RBdirect'
# PAT_DIR = 'RBXadj'
# FRQ_FLOOR = 3
# FRQ_FLOOR = 10
# FRQ_FLOOR = 20
# FRQ_FLOOR = 50
FRQ_FLOOR = 100  # BUG 100 will be used regardless, so set it to this to at least keep the naming accurate
ADVADJ_TSV = FREQ_DIR.joinpath(
    # // f'{PAT_DIR}/ucs_format/Adv{UNIT}_frq-thrMIN-7.35f.tsv')
    f'{PAT_DIR_NAME}/Adv{UNIT}_{TAG}_{PAT_DIR_NAME}_final-freq.tsv')
FOCUS = ['f', 'unexpected_f',
         'conservative_log_ratio',
         'am_p1_given2', 'am_p2_given1',
         'am_p1_given2_simple', 'am_p2_given1_simple',
         'am_log_likelihood',
         #  'mutual_information', 'am_odds_ratio_disc', 't_score',
         'N', 'f1', 'f2', 'E11',
         'l1', 'l2']

# %%
def invert_set_dict(d: dict):
    return {v: k for k in d for v in d[k]}


# %% [markdown]
# 1. Run `seek_readable_ucs()` to generate consistent output path

# %%
readable = seek_readable_ucs(min_freq=FRQ_FLOOR,
                             ucs_subdir='adv_adj',
                             contained_counts_path=ADVADJ_TSV)
print(readable.relative_to(RESULT_DIR))

# %% [markdown]
# Snippet of starting frequency data (`ADVADJ_TSV`)

# %%
! head '-5' "{ADVADJ_TSV}" | column '-t'

# %% [markdown]
# 2. Run `confirm_basic_ucs()` (if needed)
if not readable.is_file():
    basic_ucs_path = readable.parent.parent.joinpath(
        readable.name.replace('.rsort-view_am-only.txt', '.ds.gz'))
    print(
        f'Creating initial UCS table: `{basic_ucs_path.relative_to(RESULT_DIR)}')

    basic_ucs_path = confirm_basic_ucs(
        basic_ucs_path,
        freq_floor=FRQ_FLOOR,
        contained_counts_path=ADVADJ_TSV)

# %% [markdown]
# Excerpt of initial UCS table
init_readable = UCS_DIR.joinpath(
    f'adv_adj/{PAT_DIR_NAME}/readable'
).joinpath(f'{ADVADJ_TSV.name.replace(".tsv","")}_min{FRQ_FLOOR}x.init.txt')
! head '-7' "{init_readable}"


# %% [markdown]
# 3. Run `associate_ucs()` (if needed)

if not readable.is_file():
    associate_ucs(basic_ucs_path)
# /ucs-RBdirect_AdvAdj_ALL_RBdirect_final-freq_min100x-ds.2024-08-11_2314.log
transform_ucs_log = f'/share/compling/projects/sanpi/logs/associate/ucs/ucs-{PAT_DIR_NAME}_Adv{UNIT}_{TAG}_{PAT_DIR_NAME}_final-freq_min{FRQ_FLOOR}x*.log'
print(transform_ucs_log)
# %%
#// ! head '-15' `ls '-t1' {transform_ucs_log} | head '-1'`
#// ! echo '...'
#// ! tail '-2' `ls '-t1' {transform_ucs_log} | head '-1'`
! grep '# Sample size' {transform_ucs_log} | tail '-1'

# %% [markdown]
# 4. Run `ucs_to_csv()` to convert `ucs/[PAT_DIR]/readable/*.txt` to format that `pandas` can parse as a dataframe

! head '-5' "{readable}"
csv_path = ucs2csv(readable)
print(f'CSV: `{csv_path.relative_to(RESULT_DIR)}`')

# %% [markdown]
###
adx_amdf = pd.read_csv(csv_path).convert_dtypes()
adx_amdf

# %%
adx_amdf['key'] = (adx_amdf.l1 + '~' +
                   adx_amdf.l2).astype('string')
adx_amdf = adx_amdf.set_index('key')
adx_amdf
# %% [markdown]
# 6. Save to `./results/assoc_df/`

df_csv_path = AM_DF_DIR.joinpath(
    str(csv_path.relative_to(UCS_DIR))
    .replace('/readable', '')
    .replace('.rsort-view_am-only', ''))

if not df_csv_path.is_file():
    confirm_dir(df_csv_path.parent)
    adx_amdf.to_csv(df_csv_path)

df_pkl_path = df_csv_path.with_suffix('.pkl.gz')
if not df_pkl_path.is_file():
    adx_amdf.to_pickle(df_csv_path.with_suffix('.pkl.gz'))
# %% [markdown]
# 7. Add additional AM via `add_extra_am()`
# Define dictionary containing relevant vocab sizes
# !!! Warning This is a `#HACK`: \
#     Rather than developing a command/code to retrieve the vocab sizes programmatically,
#     I simply copied the values given in the log output of `transform_usc.sh`
#     for each `PAT_DIR`+`UNIT` combination


VOCABS = {
    'old!NEGmirror': {'Adj': 40004}, #! old
    'old!POSmirror': {'Adj': 178159}, #! old
    'old!ANYmirror': {'Adj': 195059}, #! old
    'RBdirect':  {'Adj': 187831}, # updated! ✅
    'old!RBXadj':  {'Adj': 1940305} #! old
}  # ! #HACK
VOCAB = VOCABS[PAT_DIR_NAME][UNIT]

print(pd.DataFrame(VOCABS).convert_dtypes().to_markdown(intfmt=','))

# %%
# import association_measures as assom
# # %%
# assom.measures.list_measures()
# # %%

# assom.measures.conservative_log_ratio(assom.frequencies.observed_frequencies(adx_amdf), vocab=VOCAB)


VOCAB = None
ex_adx_amdf = add_extra_am(df=adx_amdf,
                           verbose=True,
                           vocab=VOCAB,
                           metrics=['t_score', 'mutual_information']
                           ).convert_dtypes()

# %% [markdown]
# Save extended AM tables to `extra/` subdirectory if not already saved
df_extra_csv = df_csv_path.parent / 'extra' / \
    df_csv_path.name.replace('.csv', '_extra.csv')
print(df_extra_csv)
if not df_extra_csv.is_file():
    confirm_dir(df_extra_csv.parent)
    ex_adx_amdf.to_csv(df_extra_csv)

df_extra_pkl = df_extra_csv.with_suffix('.pkl.gz')
if not df_extra_pkl.is_file():
    ex_adx_amdf.to_pickle(df_extra_pkl)

# %%
ex_adx_full = ex_adx_amdf.copy()
ex_adx_abbr = adjust_am_names(
    ex_adx_amdf[[c for c in ['polarity', 'quant'] + FOCUS if c in ex_adx_amdf.columns]]).sort_values('LRC', ascending=False)
cols = ex_adx_abbr.columns

# %% [markdown]
# Define lexical items with given lean shown in binary environment evaluation
pos_prone = {
    'Adj': [
        'unrelated',
        'unable',
        'akin',
        'larger',
        'different',
        'familiar',
        'similar',
        'likely',
        'brief',
        'unaware'
    ],
    'Adv': [
        'slightly',
        'definitely',
        'utterly',
        # LRC top
        'pretty',
        'rather',
        'plain',
        'fairly',
        'somewhat',
        'otherwise',
        'downright',
        'relatively',
        # G2 top
        # 'very',
        # 'even',
        # 'just',
        # dP1 top (and odds ratio disc)
        'plain',
        'maybe'
    ],
    'Bigr': [
        # G2 top
        'completely_different',
        'too_familiar',
        'even_better',
        # dP1 top
        'quite_different',
        'too_real',
        'well_aware',
        # LRC top
        'too_common',
        'entirely_different'
    ]}
neg_prone = {
    'Bigr': [
        # LRC top
        'quite_sure',
        'really_sure',
        'too_early',
        'too_pleased',
        'too_fancy',
        # dP1 top
        'entirely_sure',
        'ever_easy',
        'ever_perfect',
        'particularly_surprising',
        'particularly_new',
        # G2 top
        'too_late',
        'more_important',
        'so_easy',
        'as_good',
        'too_old'
    ],
    'Adv': [
        'yet',
        # LRC top
        'ever',
        'any',
        'longer',
        'necessarily',
        'that',
        # dP1 top
        'before',
        'wise',  # ? How is this used as an adverb?
        'earthly',
        'remotely',
        'exactly',
        # G2 top
        'particularly',
        'too',
        # 'inherently'
    ],
    'Adj': [
        # LRC top
        'early',
        'late',
        'fancy',
        'alone',
        'sure',
        # dP1 top
        'shabby',
        'demoralizing',
        'alone',
        'aggravating',
        'groundbreaking',
        'eventful',
        # G2 top
        'important',
        'frustrating',
        'evident',
        'certain'
    ]
}


def sort_prone_by_f2(prone_list, amdf):
    return amdf.copy().loc[amdf.l2.isin(prone_list), ['f2', 'l2']].drop_duplicates().reset_index(drop=True).set_index('l2').round(1).sort_values(['f2'], ascending=False).index.to_list()


pos_prone[UNIT] = sort_prone_by_f2(pos_prone[UNIT], ex_adx_abbr)
neg_prone[UNIT] = sort_prone_by_f2(neg_prone[UNIT], ex_adx_abbr)
pos_prone[UNIT]
# %% [markdown]
# Strongest associations for each polarity by metric


def show_metric_top(amdf: pd.DataFrame,
                    metric: str,
                    k=5,
                    cols=[None]):
    if not any(cols):
        cols = amdf.columns
    return (amdf.nlargest(k, metric)
            .loc[:, [metric] + cols[cols != metric].to_list()]
            .reset_index(drop=True).set_index(['l1', 'l2'])
            )


# %% [markdown]
# Top consevative log ratio $LRC$ values
exdf = show_metric_top(ex_adx_abbr, "LRC", k=8)
# pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top $\Delta P(\texttt{adv}|\texttt{adj})$ values
exdf = show_metric_top(ex_adx_abbr, 'dP1', k=8)
# pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top conditional probability $P(\texttt{adv}|\texttt{adj})$ values
exdf = show_metric_top(ex_adx_abbr, 'dP1_simple', k=8)
# pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top $\Delta P(\texttt{adj}|\texttt{adv})$ values
exdf = show_metric_top(ex_adx_abbr, 'dP2', k=8)
# pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top conditional probability $P(\texttt{adj}|\texttt{adv})$ values
exdf = show_metric_top(ex_adx_abbr, 'dP2_simple', k=8)
# pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top log-likelihood $G^2$ values
exdf = show_metric_top(ex_adx_abbr, 'G2', k=8)
# pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf

# %%
sig_adx_abbr = ex_adx_abbr.loc[ex_adx_abbr.LRC.abs() > 1, :]
sig_adx_abbr
# %% [markdown]
# Positive Prone Adverbs with significant LRC
sig_adx_abbr.loc[sig_adx_abbr.l1.isin(pos_prone['Adv'])]
# %% [markdown]
# Negative Prone Adverbs with significant LRC
sig_adx_abbr.loc[sig_adx_abbr.l1.isin(neg_prone['Adv'])]
# %% [markdown]
# Positive Prone Adjectives with significant LRC
sig_adx_abbr.loc[sig_adx_abbr.l2.isin(pos_prone['Adj'])]
# %% [markdown]
# Negative Prone Adjectives with significant LRC
sig_adx_abbr.loc[sig_adx_abbr.l2.isin(neg_prone['Adj'])]
