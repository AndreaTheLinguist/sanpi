# %%
"""original copied from https://github.com/grew-nlp/grewpy/blob/master/examples/test_corpus.py"""
import json
import os
import sys
from pathlib import Path
from pprint import pprint
from collections import namedtuple

import pandas as pd
# from grewpy import Graph, CorpusDraft, Request, Corpus, request_counter
from grewpy import (Corpus, 
                    # CorpusDraft, Graph, 
                    Request, request_counter)
from grewpy.grew import GrewError as GrewError

# sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

_META_TUP = namedtuple(
    'meta_info', 
    ['sent_id', 'doc_id', 'sent_int', 'prev_id', 'prev_text', 'next_id', 'next_text'])

def corpus_from_path(path):
    return Corpus(str(path))

def docs(expr):

    try:
        print(expr.__doc__)
    except AttributeError:
        print('None')

# %%
conllu_path = Path(
    "data/corpora/gitrepo_puddin/2smallest.conll/apw_eng_199911.conllu"
    # "data/corpora/gitrepo_puddin/2smallest.conll/nyt_eng_200405.conllu"
    )
co = corpus_from_path(conllu_path)

# %% [markdown]
# Should be able to set this up to have `conllu_path` (and `pat_path`?) 
# as input, and run it in parallel on a list of files, 
# even files from different directories
# 
# ...did I just rewrite the entire subset code today? 🤦‍♀️

# %%

print("\n=============== len ===============")
print(f"sentence count in {conllu_path.name} = {len(co)}")
print(request_counter())

print(f"len(co[0]) = {len(co[0])}")
print(f"len(co[-1]) = {len(co[-1])}")
print(f"[len(g) for g in co[-3:]] = {[len(g) for g in co[-3:]]}")
# other forms co[-3:-1], co[1:7:2], ...


# %%
print("\n=============== Count request in a corpus ===============")
for xpos in ("RB.*", "JJ.*"):
    # xpos="RB.*"
    if xpos.startswith('RB'):
        print('# ADVERBS')
    elif xpos.startswith('JJ'):
        print('# ADJECTIVES')

    req = Request(f'X[xpos=re"{xpos}"]')

    print(" ----- basic count -----")
    print(f"total {xpos} in {conllu_path.name} = ", co.count(req))

    print(" ----- count with clustering -----")
    print(f"total {xpos} in {conllu_path.name}, clustered by exact POS:")
    # print(request_counter())
    print(pd.Series(co.count(req, ["X.xpos"])).to_frame().rename(columns={0:'total'}).to_markdown(), '\n')

# %%
#* ALL bigrams
req = Request('ADJ [xpos=re"JJ.?"];'
              'mod: ADJ -[advmod]-> ADV;'
              'ADV < ADJ'
              )
print(str(req))

# %%
pat_path = Path('Pat/advadj/all-RB-JJs.pat')
pat_str = pat_path.read_text(encoding='utf8')
print(pat_str)

# %% [markdown]
# ⚠️ Just running the raw pattern file text will result in an error:
#%%
print(str(Request(pat_str)))
try: 
    co.count(Request(pat_str))
except: 
    print('ERROR! Bad request. (handled to prevent cancelation of following cells)')
# %% 
def grewpize_pat(raw_text): 
    return ''.join(line.strip() for line in raw_text.split('{', 1)[1].split('}',1)[0].strip().splitlines())
clean_str = grewpize_pat(pat_str)
print(clean_str.replace(';', ';\n'))
print('# actual form:')
print(clean_str)
# %%
read_req = Request(clean_str)
print(str(read_req))

# %% 
# or, all in one go: 
full_read_req = Request(grewpize_pat(pat_path.read_text(encoding='utf8')))
str(full_read_req) == str(read_req)

#%%
co.count(read_req)

# %%
print("\n=============== Count `ADV ADJ` bigrams ===============")
print(f"total `ADV ADJ` bigrams in {conllu_path.name}: {co.count(req)}")
print("\n----- count with clustering -----")
print(f"`ADV ADJ` bigrams in {conllu_path.name}, clustered by ADV lemma:")
# print(json.dumps(co.count(req, ["ADV.lemma"]), indent=2))
pd.Series(co.count(req, ["ADV.lemma"])).to_frame().reset_index().rename(
    columns={'index':'adverb', 0:'total_bigrams'}
    ).sort_values('total_bigrams', ascending=False)

# %%
print(f"Top 10 `ADV ADJ` bigrams in {conllu_path.name}")
pd.json_normalize(co.count(req, ["ADV.lemma", "ADJ.lemma"]), sep='_').transpose(
    ).rename(columns={0:'total'}).nlargest(10, 'total')

# %%
match_list = co.search(req)

print("\n=============== `ADV ADJ` bigram match info ===============")
pd.json_normalize(match_list, sep='_')
# %%
def gen_conllus(match_list, corpus):
    
    # for sent in match_list:
    for i, sent in enumerate(match_list):
        parse = corpus.get(sent['sent_id'])
        if i < 3:
            print(parse.to_conll())
        yield parse.to_conll()+'\n'

# %%
conllu_gen = gen_conllus(match_list, co)

subset_dir = conllu_path.parent.joinpath(f'subset_{pat_path.parent.stem}')
if not subset_dir.is_dir(): 
    subset_dir.mkdir()
    
subset_path = subset_dir.joinpath(f'{pat_path.stem}+{conllu_path.name}')
subset_path.write_text('\n'.join(conllu_gen), encoding='utf8')

# %%
advadj_subset = corpus_from_path(subset_path)

# %%[markdown]
# ## modifier bigram only

# %%
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"];'
    # 'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'neg: ADJ -> NEG;'
    # 'neg: NEG -> ADJ;'
    # 'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))

# %%[markdown]
# ## `not` somewhere in sentence

# %%
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    'NEG [lemma="not"];'
    # 'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'neg: ADJ -> NEG;'
    # 'neg: NEG -> ADJ;'
    # 'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))

# %%[markdown]
# ## known `NEG` lemma somewhere in sentence

# %%
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"];'
    'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'neg: ADJ -> NEG;'
    # 'neg: NEG -> ADJ;'
    # 'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))

# %%[markdown]
# ## known `NEG` lemma preceding `ADV` token node

# %%
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"];'
    'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'neg: ADJ -> NEG;'
    # 'neg: NEG -> ADJ;'
    'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))


# %%[markdown]
# ## known `NEG` lemma with `ADJ` node as its **target** (in dependency relationship)
# This is not expected. No $NegPol$ patterns cover relationships of this direction.

# %%
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"];'
    'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'neg: ADJ -> NEG;'
    'neg: NEG -> ADJ;'
    'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))

# %%[markdown]
# ## known `NEG` lemma with `ADJ` node as its **head/source** 

# %% 
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"];'
    'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    'neg: ADJ -> NEG;'
    # 'neg: NEG -> ADJ;'
    'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))

# %% [markdown]
# 👆 This pattern, which does not impose any restrictions on the *type* 
# of dependency relationship between `NEG` and `ADJ` yields duplicate results 
# in the case of any "enhanced" parsing

# %%
hits = co.search(neg_req)
pprint(hits[:2])
# %%
pprint({f"{h['sent_id']} ~ hit {i} neg label":h['matching']['edges']['neg']['label'] for i,h in enumerate(hits[:16])})
# %%[markdown]
# ## known `NEG` lemma with `ADJ` node as its *head/source* and the relationship type does not start with "E"
# This is to prevent issue with duplicate records for "Enhanced" versions of the dependency.

# %% 
neg_req = Request(
    'ADJ [xpos=re"JJ.?"];'
    'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"];'
    'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'neg: ADJ -> NEG;'
    # 'neg: NEG -> ADJ;'
    'NEG << ADV;'
    )
print(str(neg_req).replace(';', ';\n\t '))
print('-------------------------\nhits:', co.count(neg_req))

# %%[markdown]
# ...and now the duplicate hits (as well as the output structure unpredictability) have been removed:
#%% 
pprint({f"{h['sent_id']} ~ hit {i} neg label":h['matching']['edges']['neg']['label'] for i,h in enumerate(co.search(neg_req)[:16])})

# %%
pd.json_normalize(co.count(neg_req, ["ADV.lemma", "NEG.lemma"]), sep='_').transpose().rename(columns={0:'total'}).nlargest(10,'total')

# %%
neg_df = pd.json_normalize(co.search(neg_req), sep='_').convert_dtypes()
neg_df.columns = (
    neg_df.columns
    .str.replace('matching_', '')
    .str.replace('nodes_', 'index_')
    .str.replace('edges_', 'dep_'))
neg_df

# %%
for m in neg_df.sample(min(len(neg_df),8)).sent_id.apply(lambda i: co.get(i).meta): 
    print(f"{m['sent_id']}:\t{m['text']}")

#%%[markdown]
# ## Thoughts... 
# Instead of creating new subset `.conllu` files with all matching 
# sentences + their context sentences (preceding and following), 
# it should be possible to take only what is needed for the context sentences 
# (i.e. `sent_id` and `sent_text`, the only things put into the hit table)
# and then pull those directly from the meta info. 
# 
# The next big question, though, is whether to create the subset file at all in that case. 
# **This new module essentially makes the first 2 steps of the pipeline code obsolete.**
# If this functionality had existed 2 years ago... smh 😐
#
# But I'm not going to rework *everything* at this point. 
#
# ## Plan
# I will create the `advadj` subset and then run the pipeline on those. 
# 
# If I remove the context sentences, `fill_match_info` will need to be modified to not collect them
# (since anything it would pull would be incorrect). 
# However, it would not necessarily need to add them at all at that point. 
# I wanted to make sure I had access to what they are, but so far, I haven't used them. 
# If there exists a table where they can be looked up if need be, that should suffice. 
# The sentence IDs are stable and unique identifiers, so any table indexed by `sent_id`
# will be easy to connect with the existing data. 
#
# Mock Table Schematic
#
# > | sent_id | doc_id | conllu_id | sent_text | prev_id | next_id | prev_text | next_text |
# > |:--------|:-------|:----------|:----------|:--------|:--------|:----------|:----------|
# > | ... | ... | ... | ... | ... | ... | ... | ... |

# %%
# hit_meta = pd.json_normalize(neg_df.sent_id.apply(lambda i: co.get(i).meta['text'])
#                              ).convert_dtypes()#.rename(columns={'':'newdoc_id'})
hit_meta = neg_df.sent_id.to_frame()
hit_meta = hit_meta.assign(sent_text = hit_meta.sent_id.apply(lambda i: co.get(i).meta['text']),
                           conllu_id=conllu_path.stem, 
                        #    newdoc_id=hit_meta.newdoc_id.str.replace('# newdoc id = ', '').fillna('')
                        )
hit_meta

# %%
def parse_sent_id(sent_id):
    doc_id, ordinal_str = sent_id.rsplit('_', 1)
    ordinal_int = int(ordinal_str)

    row = (sent_id, doc_id, ordinal_int)
    for context_ix in (ordinal_int + i for i in (-1, 1)): 
        c_text = ''
        c_id = ''
        #> conllu doc sentence numbering starts at 1
        if context_ix > 0:
            c_id = f'{doc_id}_{context_ix}'
            try: 
                c_obj = co.get(c_id)
            except GrewError: 
                c_id = ''
            else: 
                c_text = c_obj.meta['text']
        row += (c_id, c_text)
        
    yield _META_TUP._make(row)

#%% 
sid = hit_meta.sent_id[0]
print(pd.DataFrame(parse_sent_id(sid)).set_index('sent_id').transpose().to_markdown())
#%%
context_info = pd.concat(pd.DataFrame(parse_sent_id(s)) for s in hit_meta.sent_id)
context_info.head()

#%% 
meta_info = hit_meta.set_index('sent_id').join(context_info.set_index('sent_id')).rename(columns={'text':'sent_text'})
meta_info = meta_info[['conllu_id', 'doc_id', 'sent_int', 'prev_id', 'next_id', 'prev_text', 'sent_text', 'next_text']]
print(meta_info.sample(min(len(meta_info),2)).to_markdown())
print("\n---\n")
print(meta_info.iloc[-1, :].squeeze().to_markdown())

# %% 
meta_info.to_csv(subset_dir.joinpath(conllu_path.stem+'+meta.psv'), sep='|')

# %%
neg_df.loc[:, ['sent_text', 'conllu_id', 'doc_id']] =  neg_df.sent_id.apply(
    lambda x: meta_info.loc[x, ['sent_text', 'conllu_id', 'doc_id']])
neg_df.sample(min(len(neg_df),10))


# %%
