# %%
# Install `transformers` from master
# ! 👇 apparently this isn't really python code. It only works on jupyter kernal
!pip install transformers
!pip list | grep -E 'transformers|tokenizers'
# transformers version at notebook update --- 4.32.1 #//2.11.0
# tokenizers version at notebook update ---  0.13.3 #//0.8.0rc1

import csv
from pathlib import Path
from pprint import pprint

import pandas as pd
import torch
from transformers import (AutoModel, AutoModelForMaskedLM, AutoTokenizer,
                          pipeline)
from utils.LexicalCategories import ADJ_BY_SCALE as ADJ_SETS
from utils.LexicalCategories import ADV_OF_INTEREST as ADV_SETS

pd.set_option('display.max_colwidth', 70)

MASK_POS = 'adv'
MODEL = 'distilbert-base-uncased'
UNMASK = pipeline('fill-mask', model=MODEL, tokenizer=MODEL, framework='pt')
HITS_PATH = Path(
    '/share/compling/projects/sanpi/demo/data/2_hit_tables/RBXadj/bigram_X2puddin_all-RB-JJs_hits.csv')
FRQ_FILTER = Path(
    '/share/compling/projects/sanpi/demo/data/4_post-processed/RBxpos/hit-index_thr0-001p.1f.txt')
# %% [markdown]
# ## Load sample hit table as data
# %%


def _load_hits(dpath=HITS_PATH):

    if '.csv' in dpath.suffixes:
        data = pd.read_csv(dpath)
        data = data.set_index('hit_id').convert_dtypes()

    elif dpath.endswith('pkl.gz'):
        data = pd.read_pickle(dpath)

    print('data loaded')
    pprint(data.columns)
    print(data.sample(3))

    return data

data = _load_hits()

# %% [markdown] 
# Apply filters to loaded data, based on frequency as well as manual criteria

# %%
def _filter_hits(hits_data):
    # trim data
    filter_hi = pd.read_csv(FRQ_FILTER).squeeze()
    df = hits_data.loc[filter_hi,
                       ['adv_form', 'adj_form', 'adv_lemma', 'adj_lemma',
                        'adv_index', 'adj_index', 'token_str', 'text_window']]
    df = df.assign(
        prev_prev_word=df.index.to_series().apply(
            lambda ix: df.token_str[ix].split()[max(-1,df.adv_index[ix] - 2)]),
        prev_word=df.index.to_series().apply(
            lambda ix: df.token_str[ix].split()[max(-1,df.adv_index[ix] - 1)]),
        next_word=df.index.to_series().apply(
            lambda ix: df.token_str[ix].split()[min(len(df.token_str[ix].split())-1, df.adj_index[ix] + 1)]),
        next_next_word=df.index.to_series().apply(
            lambda ix: df.token_str[ix].split()[min(len(df.token_str[ix].split())-1, df.adj_index[ix] + 2)])
        )
    df.loc[df.prev_word == df.prev_prev_word, 'prev_prev_word'] = ''
    df.loc[df.prev_word == df.adv_form, 'prev_word'] = ''
    df.loc[df.next_word == df.next_next_word, 'next_next_word'] = ''
    df.loc[df.next_word == df.adj_form, 'next_word'] = ''
    manual_criteria = (
        # limit to `token_str` values with no more than 14 spaces ≈ max 15 words
        (df.token_str.str.count(' ') <= 14)
        # NOTE: 'many', 'much' & 'enough' have abnormal syntactic patterns
        & (~df.adv_lemma.str.lower().isin(('enough', 'how', 'much', 'most')))
        & (~df.adj_lemma.str.lower().isin(('many', 'more', 'much')))
        # have issues filling position following "much" and "more"--they don't wind up being adverbs but comparative adjectives
        & (~df.prev_word.isin(['more', 'much', 'as']))
        & (~df.next_word.str.lower().isin(['as']))
    )
    df = df.loc[manual_criteria, :]

    return df

data = _filter_hits(data)
# %%
data.sample(5).reset_index(drop=True).loc[:, data.columns.str.endswith(('word', 'form', 'str', 'window'))]

# %% [markdown]
# ## Mask tokens
# In this version, the data is not pre-masked.
# It consists of sentence strings and target information, including the index of token nodes in the `token_str` values.
# Should be able to use the `adv_index` and/or `adj_index` to create the corresponding masked version of `token_str`
#
# _Note: for some reason, the initial filter series, `filter_hi`, gets reshaped as the index of `data`, so it cannot be used in place of `data.index.to_series()`_


# %%
def pre_mask(df, mask_pos='adv'):
    # df.info()
    mask_ix = df.loc[:, f'{mask_pos}_index']
    # print(mask_ix)
    # #! end index is not included in the returned value! [:mask_ix[h]-1] cuts out the word preceding the adv as well

    return df.index.to_series().apply(
        lambda h: ' '.join(df.token_str[h].split()[:mask_ix[h]]))


def post_mask(df, mask_pos='adv'):
    mask_ix = df.loc[:, f'{mask_pos}_index']

    return mask_ix.index.to_series().apply(
        lambda h: ' '.join(df.token_str[h].split()[mask_ix[h]+1:]))


def mask(df: pd.DataFrame, pos='adv'):
    pre_col = pre_mask(df, pos)
    post_col = post_mask(df, pos)
    return df.assign(masked=pre_col + ' [MASK] ' + post_col)


data = mask(data, MASK_POS)
# %%
pd.set_option('display.max_colwidth', 90)
# %%
data.sample(9).reset_index()[['masked']]
# %%
pd.set_option('display.max_colwidth', 70)

# %% [markdown]
# ## *Unmask* Tokens
# Data is loaded and now _masked_ sentences are a column in the dataframe. 
# Can use `UNMASK` pipeline to get probabilities of tokens at masked position.
# 
# ## For just 1 input
# 
# Select sample sentence and run pipeline
# %%
selected_data = data.loc[:, ['adv_form', 'adj_form', 'text_window', 'masked', 'prev_word', 'next_word']]
sent_row = selected_data.sample(1)
sent = sent_row.masked.squeeze()
sent_row.transpose()

# %% [markdown]
# get top 10 predictions for masked position
# %%
results = UNMASK(sent, top_k=10)
rdf = pd.DataFrame(results).sort_values('score', ascending=False)

# %% [markdown]
# load lexical categories and compare

# %%
def add_lexcats(results, lex_dict,
                original_forms
                ):

    cat_start_index = len(results.columns)
    for lex_type, lex_set in lex_dict.items():
        results.loc[:, lex_type] = results.token_str.isin(lex_set)
    return (results
            .assign(lexcat_defined=rdf.iloc[:, cat_start_index:].apply(any, axis=1),
                    match_masked_POS=results.token_str.isin(original_forms))
            )


orig_form = data[f'{MASK_POS}_form']

if MASK_POS == 'adj':
    lexcat_dict = ADJ_SETS
elif MASK_POS == 'adv':
    # for adv_type, adv_set in ADV_SETS.items():
    #     rdf.loc[:, adv_type] = rdf.token_str.isin(adv_set)
    # rdf = rdf.assign(match_masked_POS=rdf.token_str.isin(data.adv_form))
    lexcat_dict = ADV_SETS

rdf = add_lexcats(rdf, lexcat_dict, orig_form)
print(rdf.to_markdown(floatfmt='.4f'))

# %% [markdown]
# ## Across multiple inputs
# 
# Apply across all masked sentences and collect results

# %%
selected_data = selected_data.sample(300) # HACK: #! temporary. REMOVE


def get_scores(masked, top_k=10):
    return {word_fill['token_str']: word_fill['score'] for word_fill in UNMASK(masked, top_k=top_k)}


def sum_lexcats(scores: dict, lex_dict: dict):
    results = pd.Series(scores).to_frame('score')
    # results.index.name = 'filler_str'
    # results = results.reset_index()
    lexcat_sums = pd.Series(dtype='float')
    for lex_type, lex_set in lex_dict.items():
        # return results.loc[results.index.isin(lex_set), 'score'].sum()
        lexcat_sums.loc[f'{lex_type}_total'] = results.loc[results.index.isin(
            lex_set), 'score'].sum().round(5)
    return lexcat_sums
# %%
pprint([{'hit_id': i,
         f'original_{MASK_POS}': selected_data.loc[i, f'{MASK_POS}_form'],
         'text_window': selected_data.text_window[i],
         'masked_str': selected_data.masked[i],
         'scores': UNMASK(selected_data.masked[i], top_k=3)}
        for i in selected_data.sample(3).index])

# %%
score_df = selected_data.assign(scores=selected_data.masked.apply(get_scores, top_k=30))
score_df = score_df.join(score_df.scores.apply(sum_lexcats, lex_dict=ADV_SETS))
score_df.info()
# %%
score_df.describe().round(4).T
#%%
score_df.sample(15)

