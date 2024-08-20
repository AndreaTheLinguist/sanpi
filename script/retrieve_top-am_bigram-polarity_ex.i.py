# %%
import pandas as pd
from source.utils.am_notebooks import *

from source.utils.associate import TOP_AM_DIR
from source.utils.associate import adjust_am_names as adjust_assoc_columns
from source.utils.general import HIT_TABLES_DIR, timestamp_today
from source.utils.sample import sample_pickle as sp
from sys import argv

try:
    TAG = argv[1]
except IndexError:
    TAG = 'ALL'

try:

    VERBOSE = argv[2] == '-v'
except IndexError:
    VERBOSE = False  # ! MAKE SURE THIS IS WHAT YOU WANT

# TAG = 'ALL'
# VERBOSE = False  # ! MAKE SURE THIS IS WHAT YOU WANT

REFILTER_NEG = False
K = 8
BK = max(K+2, 10)
N_EX_PER_BIGRAM = 99
BIGRAM_F_FLOOR = 50
ADV_F_FLOOR = 5000
DATE = timestamp_today()

METRIC_PRIORITY = METRIC_PRIORITY_DICT[TAG]
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
TAG_TOP_STR = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / TAG_TOP_STR

FOCUS = adjust_am_names(FOCUS_DICT[TAG]['polar'])
FOCUS_MEANS = [f'mean_{c}' for c in FOCUS]
SET_FOCUS = [f'{c}_SET' for c in FOCUS]
MIR_FOCUS = [f'{c}_MIR' for c in FOCUS]
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 70)

# %%
# * parquet paths
NEG_HITS_PATH = HIT_TABLES_DIR / 'RBdirect'/'ALL-RBdirect_final.parq'
PRESAMPLED_PARQ = find_most_recent_top_am(
    date_str=DATE, data_dir=OUT_DIR, suffix='.parq',
    undated_stem=f'{TAG_TOP_STR}adv_sample-hits_')

# %%
adv_am = seek_top_adv_am(
    date_str=DATE, adv_floor=ADV_F_FLOOR, tag_top_dir=OUT_DIR)
adv_am = adjust_assoc_columns(adv_am).convert_dtypes()
if VERBOSE:

    md_frame_code(r"""for selector, selection in (('*_SET', SET_FOCUS), 
                            ('*_MIR', MIR_FOCUS), 
                            ('mean_*', FOCUS_MEANS)):
    nb_show_table(adv_am.filter(selection[:-3]), 
                  title=f'### `{selector}` columns for loaded top adverbs')""")

    for selector, selection in (('*_SET', SET_FOCUS),
                                ('*_MIR', MIR_FOCUS),
                                ('mean_*', FOCUS_MEANS)):

        nb_show_table(adv_am.filter(selection[:-3]),
                      title=f'### `{selector}` columns for loaded top adverbs')

# %%
if VERBOSE:
    md_frame_code("""print('## Comparing metrics across data selections\n')
for metric_cue in METRIC_PRIORITY + ['^[_%]*f', 'f2', '^exp_', 'unexp']:
    print(f'### Displaying Juxtaposed Values for `{repr(metric_cue)}`')
    md_frame_code(f'compare_datasets(adv_am, {repr(metric_cue)})')
    compare_datasets(adv_am, metric_cue)""")

    print('## Comparing metrics across data selections\n')
    for metric_cue in METRIC_PRIORITY + ['^[_%]*f', 'f2', '^exp_', 'unexp']:
        print(f'### Displaying Juxtaposed Values for `{repr(metric_cue)}`')
        md_frame_code(f'compare_datasets(adv_am, {repr(metric_cue)})')
        compare_datasets(adv_am, metric_cue)

if VERBOSE:
    md_frame_code("""TOP_ADV, adv_am = pin_top_adv(
        adv_am, select_col=(
            adv_am.filter([f'mean_{m}' for m in METRIC_PRIORITY])
            .columns.to_list()
        ))""")
TOP_ADV, adv_am = pin_top_adv(
    adv_am, select_col=(
        adv_am.filter([f'mean_{m}' for m in METRIC_PRIORITY])
        .columns.to_list()
    ))

# %%
undated_stem = f'{TAG_TOP_STR}_NEG-ADV-{ADV_F_FLOOR}_Top{BK}-bigrams-{BIGRAM_F_FLOOR}'
top_polar_bigram_am_csv = find_most_recent_top_am(DATE, OUT_DIR, undated_stem)
if VERBOSE:
    print(f'\n* Loading from `{top_polar_bigram_am_csv}`')

# %%
polar_bigram_am = adjust_assoc_columns(
    pd.read_csv(top_polar_bigram_am_csv)
    .set_index('key')
    # > not strictly necessary (loaded table should already satisfy this) but just in case...
    .filter(regex=r'|'.join([f'~{a}_' for a in TOP_ADV]), axis=0)
).filter(items=FOCUS).convert_dtypes()

# %%
if VERBOSE:
    md_frame_code("""sample = polar_bigram_am.sample(3)
sample.update(sample.select_dtypes(include='float').round(4))
nb_show_table(sample, transpose=True)""")

    sample = polar_bigram_am.sample(3)
    sample.update(sample.select_dtypes(include='float').round(4))
    nb_show_table(sample, transpose=True)

# %%
polar_bigram_am = polar_bigram_am.sort_values(METRIC_PRIORITY, ascending=False)
if VERBOSE:
    md_frame_code(
        '''save_top_bigrams_overall_md(polar_bigram_am, 
                            overall_k=int(BK/2 * (K+1)), 
                            out_dir=OUT_DIR,
                            bigram_floor=BIGRAM_F_FLOOR, 
                            adv_floor=ADV_F_FLOOR, 
                            suppress=not VERBOSE)'''
    )

save_top_bigrams_overall_md(polar_bigram_am,
                            overall_k=int(BK/2 * (K+1)),
                            out_dir=OUT_DIR,
                            bigram_floor=BIGRAM_F_FLOOR,
                            adv_floor=ADV_F_FLOOR,
                            suppress=not VERBOSE)

# %% [markdown]
# ### Load Negated Hit Table

# %%
if NEG_HITS_PATH.suffix.startswith('.parq'):
    neg_hits = pd.read_parquet(NEG_HITS_PATH,
                               filters=[('adv_form_lower', 'in', TOP_ADV)])
elif 'pkl' in NEG_HITS_PATH.suffixes:
    neg_hits = pd.read_pickle(NEG_HITS_PATH)

    neg_hits = neg_hits.loc[(neg_hits.adv_lemma.isin(TOP_ADV))
                            | (neg_hits.adv_form_lower.isin(TOP_ADV)), :]


neg_hits = (
    neg_hits.filter(
        regex=r'^[nab].*lower|text|token|g_head|(adv|neg)_lemma')
    .drop_duplicates(['text_window', 'bigram_lower']))


neg_hits = (
    neg_hits.filter(
        regex=r'^[nab].*lower|text|token|g_head|(adv|neg)_lemma')
    .drop_duplicates(['text_window', 'bigram_lower']))

if VERBOSE:
    print(neg_hits.neg_lemma.value_counts()
          .to_frame('subtotal in loaded negated hits sample')
          .to_markdown(intfmt=','))
    nb_show_table(neg_hits.sample(2), transpose=True)

# %%
neg_hits = clarify_neg_categories(neg_hits, verbose=VERBOSE)
if 'all_forms_lower' not in neg_hits.columns:
    # sourcery skip: use-fstring-for-concatenation
    neg_hits['all_forms_lower'] = (
        neg_hits.neg_form_lower.astype('string')
        + '_'
        + neg_hits.bigram_lower.astype('string')
    ).astype('category')

# %%
if PRESAMPLED_PARQ.exists():
    all_hits = pd.read_parquet(PRESAMPLED_PARQ, engine='pyarrow')
else:
    all_hits = pd.read_parquet(str(NEG_HITS_PATH).replace('RBdirect', 'not-RBdirect'),
                               filters=[('adv_form_lower', 'in', TOP_ADV)])

# %%
pos_hits = all_hits.copy().loc[all_hits.polarity == 'pos', :]
if VERBOSE:
    print('Confirming "Positive" Enforcement Accuracy.... 👀')
    seek_errant_negations(pos_hits)

# %%
if VERBOSE:
    for p, d in all_hits.filter(
        ['polarity', 'all_forms_lower', 'text_window']
    ).assign(
        all_forms_lower=all_hits.all_forms_lower.str.replace('_', ' ')
    ).groupby('polarity', observed=True):

        print(f'\n#### sample of `polarity=={p}` hits\n')
        nb_show_table(d.sample(5).sort_values('all_forms_lower').filter(
            ['all_forms_lower', 'text_window']))

# %%
if VERBOSE:
    nb_show_table(neg_hits.loc[neg_hits.adv_lemma.astype('string')
                               != neg_hits.adv_form_lower.astype('string')
                               ].filter(['adv_lemma', 'adv_form_lower', 'text_window']).sample(4))
    nb_show_table(neg_hits.filter(like='adv_').loc[
        neg_hits.adv_lemma.astype(
            'string') != neg_hits.adv_form_lower.astype('string')
    ].value_counts().to_frame().reset_index())

# %%
if VERBOSE:
    print(neg_hits.adv_form_lower.value_counts()
          .to_frame('Tokens in loaded *negated* sample')
          .to_markdown(floatfmt=',.0f', intfmt=','))
    for pol, pol_hits in all_hits.groupby('polarity', observed=True):
        print(f'\n ### `{pol}` adv subtotals\n')
        print(pol_hits.adv_form_lower.value_counts()
              .to_frame('Tokens in loaded sample')
              .to_markdown(floatfmt=',.0f', intfmt=','))

# %%
if VERBOSE:
    rare_forms = neg_hits.neg_form_lower.value_counts().nsmallest(6).index
    # nb_show_table(neg_hits.loc[neg_hits.neg_form_lower.isin(rare_forms), :].sort_values('neg_form_lower').filter(regex=r'bigram|neg|text'))
    nb_show_table(neg_hits.filter(['all_forms_lower', 'text_window'])
                  .assign(
                      text_window=italic(embolden(
                          neg_hits.text_window,
                          bold_regex=r'\b('+r'|'.join(rare_forms)+r')\b')))
                  .loc[neg_hits.neg_form_lower.isin(rare_forms), :]
                  .sort_values('all_forms_lower')
                  )

# %%
if VERBOSE:
    _sample = neg_hits.loc[
        ((neg_hits.neg_form_lower != "n't")
         & (neg_hits.neg_lemma.astype('string')
            != neg_hits.neg_form_lower.astype('string'))),
        ['neg_lemma', 'neg_form_lower', 'text_window']
    ].sample(10).sort_values('neg_form_lower')

    nb_show_table(
        _sample.assign(
            text_window=italic(embolden(
                _sample.text_window,
                bold_regex=r'(\b'+r'\b|\b'.join(_sample.neg_form_lower)+r')\b'))))

# %%
if VERBOSE:
    _sample = neg_hits.loc[
        ((neg_hits.neg_lemma != "not")
         & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string'))),
        ['neg_lemma', 'neg_form_lower', 'text_window']].sort_values('neg_form_lower')

    nb_show_table(
        _sample.assign(
            text_window=italic(embolden(
                _sample.text_window,
                bold_regex=r'(\b'+r'\b|\b'.join(_sample.neg_form_lower)+r')\b'))))

# %%
print(f'# {BK} Most Negative Bigrams for each of the {K} Most Negative Adverbs\n')

for rank, adverb in enumerate(adv_am.index, start=1):
    print(f'\n## {rank}. *{adverb}*')
    populate_adv_dir(
        adverb,
        bigram_am=polar_bigram_am,
        neg_hits_df=neg_hits,
        pos_hits_df=pos_hits,
        data_dir=TOP_AM_TAG_DIR,
        rank_by=METRIC_PRIORITY,
        n_bigrams=BK, n_ex=N_EX_PER_BIGRAM,
        verbose=True)

# %% [markdown]
# ```python
# print(f'# {BK} Most Negative Bigrams for each of the {K} Most Negative Adverbs\n')
#
# for rank, adverb in enumerate(adv_am.index, start=1):
#     print(f'\n## {rank}. *{adverb}*')
#     populate_adv_dir(
#         adverb,
#         bigram_am=polar_bigram_am,
#         neg_hits_df=neg_hits,
#         pos_hits_df=pos_hits,
#         data_dir=TOP_AM_TAG_DIR,
#         rank_by=METRIC_PRIORITY,
#         n_bigrams=BK, n_ex=N_EX_PER_BIGRAM,
#         verbose=VERBOSE)
# ```
