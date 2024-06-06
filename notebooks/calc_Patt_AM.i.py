# %%
import pandas as pd

from source.utils import FREQ_DIR, RESULT_DIR, UCS_DIR, confirm_dir
from source.utils.associate import (BINARY_ASSOC_ARGS, add_extra_am,
                                    associate_ucs, confirm_basic_ucs)
from source.utils.associate import convert_ucs_to_csv as ucs2csv
from source.utils.associate import get_associations_csv as init_am, AM_DF_DIR
from source.utils.associate import manipulate_ucs, seek_readable_ucs, adjust_assoc_columns
pd.set_option('display.float_format', '{:,.2f}'.format)

# %% [markdown]
# set parameters:
# - `UNIT` options:
#   - `'Bigr'`
#   - `'Adv'`
#   - `'Adj'`
# - `PAT_DIR` options:
#   - any directory in `results/freq_out/` containing a `ucs_format/` subdir with a `Trig*.tsv` frequency table
#   - developed with the following in mind:
#     - `POSmirror`
#     - `NEGmirror`
#     - `ANYmirror` (which has been populated by simple concatenation in the shell)

UNIT = 'All'
# UNIT = 'Adj'
# UNIT = 'Adv'
# UNIT = 'Bigr'
# PAT_DIR = 'POSmirror'
PAT_DIR = 'NEGmirror'
# PAT_DIR = 'ANYmirror'
# FRQ_FLOOR = 3
# FRQ_FLOOR = 10
# FRQ_FLOOR = 20
# FRQ_FLOOR = 50
FRQ_FLOOR = 100
TRIG_TSV = FREQ_DIR.joinpath(
    f'{PAT_DIR}/ucs_format/Patt{UNIT}_frq-thrMIN-7.35f.tsv')
FOCUS = ['f', 'unexpected_f',
         'conservative_log_ratio',
         'am_p1_given2', 'am_p2_given1',
         'am_p1_given2_simple', 'am_p2_given1_simple',
         'am_log_likelihood',
         #  'mutual_information', 'am_odds_ratio_disc', 't_score',
         'N', 'f1', 'f2', 'E11',
         'l1', 'l2']

# %%
TRIGGER_POLARITY = {
    'positive': {'all',
                 'always',
                 'both',
                 'either',
                 'every',
                 'everybody',
                 'everyone',
                 'everything',
                 'many',
                 'often',
                 'or',
                 'some',
                 'somebody',
                 'someone',
                 'something',
                 'somethings',
                 'sometimes'},
    'negative': {'barely',
                 'hardly',
                 'neither',
                 'never',
                 'no',
                 'nobody',
                 'none',
                 'nor',
                 'nothing',
                 'seldom',
                 'rarely',
                 'scarcely'},

}
# %%
TRIGGER_QUANT = {
    'existential': {
        'some',
        'somebody',
        'someone',
        'something',
        'somethings',
        'either',
        'or',
        'sometimes'
    },
    'universal': {
        'all', 'every',
        'always',
        'everybody',
        'everyone',
        'both',
        'everything',
    },
    'not_exist': {
        'neither',
        'never',
        'no',
        'nobody',
        'none',
        'nor',
        'nothing',
    },
    'hedged_not_exist': {
        'barely',
        'hardly',
        'rarely',
        'scarcely',
        'seldom',
        'few'
    },
    'hedged_universal': {
        'many',
        'often',
    }
}

# %%


def invert_set_dict(d: dict):
    return {v: k for k in d for v in d[k]}


# %% [markdown]
# 1. Run `seek_readable_ucs()` to generate consistent output path
readable = seek_readable_ucs(min_freq=FRQ_FLOOR,
                             ucs_subdir='pattern_eval',
                             contained_counts_path=TRIG_TSV)
print(readable.relative_to(RESULT_DIR))

# %% [markdown]
# Snippet of starting frequency data (`TRIG_TSV`)
! head -5 {TRIG_TSV} | column -t

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
        contained_counts_path=TRIG_TSV)

# %% [markdown]
# Excerpt of initial UCS table
init_readable = UCS_DIR.joinpath(
    f'pattern_eval/{PAT_DIR}/readable'
).joinpath(f'{TRIG_TSV.name.replace(".tsv","")}_min{FRQ_FLOOR}x.init.txt')
! head -7 {init_readable}


# %% [markdown]
# 3. Run `associate_ucs()` (if needed)

if not readable.is_file():
    associate_ucs(basic_ucs_path)

transform_ucs_log = f'/share/compling/projects/sanpi/logs/associate/ucs//ucs-{PAT_DIR}_Patt{UNIT}_frq-thrMIN-7-35f_min{FRQ_FLOOR}x*.log'
! head -15 `ls -t1 {transform_ucs_log} | head -1`
! echo '...'
! tail -2 `ls -t1 {transform_ucs_log} | head -1`

# %% [markdown]
# Define dictionary containing relevant vocab sizes
# !!! Warning This is a `#HACK`: \
#     Rather than developing a command/code to retrieve the vocab sizes programmatically,
#     I simply copied the values given in the log output of `transform_usc.sh`
#     for each `PAT_DIR`+`UNIT` combination
#
# |      |   ANYmirror |   NEGmirror |   POSmirror |
# |:-----|------------:|------------:|------------:|
# | Bigr |     395,338 |      64,644 |     330,694 |
# | Adv  |      23,125 |       5,004 |      18,121 |
# | Adj  |      83,422 |      21,562 |      61,860 |

#> _trigger_ vocabs, not pattern
#// VOCABS = {'ANYmirror': {'Adv': 23125, 'Bigr': 395338, 'Adj': 83422},
#//           'NEGmirror': {'Adv': 5004, 'Bigr': 64644, 'Adj': 21562},
#//           'POSmirror': {'Adv': 18121, 'Bigr': 330694, 'Adj': 61860}
#//           }  # HACK
#// VOCAB = VOCABS[PAT_DIR][UNIT]
VOCAB = None
pd.DataFrame(VOCABS)

# %% [markdown]
# 4. Run `ucs_to_csv()` to convert `ucs/[PAT_DIR]/readable/*.txt` to format that `pandas` can parse as a dataframe

! head -5 {readable}
csv_path = ucs2csv(readable)
print(f'CSV: `{csv_path.relative_to(RESULT_DIR)}`')

# %% [markdown]
###
patt_amdf = pd.read_csv(csv_path).convert_dtypes()
patt_amdf

# %%
patt_amdf['key'] = (patt_amdf.l1 + '~' +
                    patt_amdf.l2).astype('string')
patt_amdf = patt_amdf.set_index('key')
patt_amdf
# %% [markdown]
# 6. Save to `./results/assoc_df/`

df_csv_path = AM_DF_DIR.joinpath(
    str(csv_path.relative_to(UCS_DIR))
    .replace('/readable', '')
    .replace('.rsort-view_am-only', ''))

if not df_csv_path.is_file():
    confirm_dir(df_csv_path.parent)
    patt_amdf.to_csv(df_csv_path)

df_pkl_path = df_csv_path.with_suffix('.pkl.gz')
if not df_pkl_path.is_file():
    patt_amdf.to_pickle(df_csv_path.with_suffix('.pkl.gz'))
# %% [markdown]
# 7. Add additional AM via `add_extra_am()`
ex_patt_amdf = add_extra_am(df=patt_amdf,
                            verbose=True,
                            vocab=VOCAB,
                            metrics=['t_score', 'mutual_information']
                            ).convert_dtypes()

# %% [markdown]
# Add pattern features as columns: polarity and quantification type
# def add_feature(patterns:pd.Series,
#                 group_dict: dict) -> pd.Series:
#     assign_dict = invert_set_dict(group_dict)
#     return patterns.apply(lambda x: assign_dict[x] if x in assign_dict.keys() else '')

# ex_patt_amdf['polarity'] = add_feature(ex_patt_amdf.l1, TRIGGER_POLARITY)
# ex_patt_amdf['quant'] = add_feature(ex_patt_amdf.l1, TRIGGER_QUANT)
# %% [markdown]
# Save extended AM tables to `extra/` subdirectory if not already saved
df_extra_csv = df_csv_path.parent / 'extra' / \
    df_csv_path.name.replace('.csv', '_extra.csv')
print(df_extra_csv)
if not df_extra_csv.is_file():
    confirm_dir(df_extra_csv.parent)
    ex_patt_amdf.to_csv(df_extra_csv)

df_extra_pkl = df_extra_csv.with_suffix('.pkl.gz')
if not df_extra_pkl.is_file():
    ex_patt_amdf.to_pickle(df_extra_pkl)

# %%
ex_patt_full = ex_patt_amdf.copy()
ex_patt_abbr = adjust_assoc_columns(
    ex_patt_amdf[[c for c in ['polarity', 'quant'] + FOCUS if c in ex_patt_amdf.columns]]).sort_values('LRC', ascending=False)
cols = ex_patt_abbr.columns

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


pos_prone[UNIT] = sort_prone_by_f2(pos_prone[UNIT], ex_patt_abbr)
neg_prone[UNIT] = sort_prone_by_f2(neg_prone[UNIT], ex_patt_abbr)
pos_prone[UNIT]
# %% [markdown]
# Strongest associations for each polarity by metric


def show_metric_top(amdf: pd.DataFrame,
                    metric: str,
                    k=5, cols=[None]):
    if not any(cols):
        cols = amdf.columns
    return (pd.concat((polar_df.nlargest(k, metric)
                       for pol, polar_df in amdf.groupby('polarity')))
            .loc[:, [metric] + cols[cols != metric].to_list()]
            .reset_index(drop=True).set_index(['polarity', 'l1', 'l2'])
            )


def update_prone(exdf, pos_prone, neg_prone) -> dict:
    prone_dict = {'positive': pos_prone,
                  'negative': neg_prone}
    for polarity, prone in prone_dict.items():
        try:
            polar_ex = exdf.loc[polarity, :]
        except KeyError:
            continue
        else:

            for topw in polar_ex.reset_index().l2.head(2).squeeze():
                if topw not in prone[UNIT]:
                    prone[UNIT].append(topw)
            prone_dict[polarity] = prone
    return prone_dict['positive'], prone_dict['negative']


# %% [markdown]
# Top consevative log ratio $LRC$ values
exdf = show_metric_top(ex_patt_abbr, "LRC")
pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top $\Delta P(\texttt{pattern}|\texttt{adv})$ values
exdf = show_metric_top(ex_patt_abbr, 'dP1')
pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top conditional probability $P(\texttt{pattern}|\texttt{adv})$ values
exdf = show_metric_top(ex_patt_abbr, 'dP1_simple')
pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top $\Delta P(\texttt{adv}|\texttt{pattern})$ values
exdf = show_metric_top(ex_patt_abbr, 'dP2')
pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top conditional probability $P(\texttt{adv}|\texttt{pattern})$ values
exdf = show_metric_top(ex_patt_abbr, 'dP2_simple')
pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf
# %% [markdown]
# Top log-likelihood $G^2$ values
exdf = show_metric_top(ex_patt_abbr, 'G2')
pos_prone, neg_prone = update_prone(exdf, pos_prone, neg_prone)
exdf

# %%
sig_patt_abbr = ex_patt_abbr.loc[ex_patt_abbr.LRC.abs() > 1, :]


def show_prone_ex(amdf, prone_list, list_index: int = 0):
    try:
        example = prone_list[list_index]

    except IndexError:
        return list_index + 1, f'No {list_index}th entry'
    else:
        print(f'>> {example} <<')
        return list_index + 1, amdf.filter(regex=f'~{example}$', axis=0).iloc[:10, :]


# %% [markdown]
# ---
# Significant Examples for Items demonstrated positive polarity environment lean overall (Top 10 by $|LRC|>1$)
prone = pos_prone[UNIT]
prone
# %%
ix = 0
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf


# %% [markdown]
# ---
# Examples for Items demonstrating *Negative* polarity environment lean overall (Top 10 by $|LRC|>1$)

prone_list = neg_prone[UNIT]
prone = sig_patt_abbr.copy().loc[sig_patt_abbr.l2.isin(prone_list), ['f2', 'l2']].drop_duplicates(
).reset_index(drop=True).set_index('l2').round(1).sort_values(['f2'], ascending=False).index.to_list()
prone
# %%
ix = 0
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf

# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(sig_patt_abbr, prone, ix)
exdf
# %%
ix, exdf = show_prone_ex(
    sig_patt_abbr, [r'exactly\w*'] if UNIT != 'Adj' else [r'un\w+'])
exdf
