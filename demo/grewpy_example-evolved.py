# %%
"""original copied from https://github.com/grew-nlp/grewpy/blob/master/examples/test_corpus.py"""
import json
import os
import sys
from pathlib import Path
from pprint import pprint

import pandas as pd
# from grewpy import Graph, CorpusDraft, Request, Corpus, request_counter
from grewpy import (Corpus, 
                    # CorpusDraft, Graph, 
                    Request, request_counter)

# sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib


def grewpy_corpus(path):
    return Corpus(str(path))

def docs(expr):

    try:
        print(expr.__doc__)
    except AttributeError:
        print('None')

# %%
pud_file = Path(
    # "data/corpora/gitrepo_puddin/2smallest.conll/apw_eng_199911.conllu"
    "data/corpora/gitrepo_puddin/2smallest.conll/nyt_eng_200405.conllu"
    )
pud = grewpy_corpus(str(pud_file))

print("\n=============== len ===============")
print(f"sentence count in {pud_file.name} = {len(pud)}")
print(request_counter())

# print("\n=============== Get one graph ===============")
# sent_id = "apw_eng_19991101_0001_1"
# graph = pud[sent_id]
# print(f"nb of nodes of {sent_id} = ", len(graph))
# print(request_counter())

print(f"len(pud[0]) = {len(pud[0])}")
print(f"len(pud[-1]) = {len(pud[-1])}")
print(f"[len(g) for g in pud[-3:]] = {[len(g) for g in pud[-3:]]}")
# other forms pud[-3:-1], pud[1:7:2], ...


# dprint ("\n=============== Iteration on graphs of a corpus ===============")
# print ("⚠️  generate one request to Grew backend for each graph")
# acc = 0
# for sent_id in pud.get_sent_ids():
#   acc += len(pud[sent_id])
# print(f"nb of nodes in {pud_file} = ", acc)
# print (request_counter())

# %%
print("\n=============== Count request in a corpus ===============")
# upos="ADV"
# req = Request(f"X[upos={upos}]")
for xpos in ("RB.*", "JJ.*"):
    # xpos="RB.*"
    if xpos.startswith('RB'):
        print('# ADVERBS')
    elif xpos.startswith('JJ'):
        print('# ADJECTIVES')

    req = Request(f'X[xpos=re"{xpos}"]')

    print(" ----- basic count -----")
    print(f"total {xpos} in {pud_file.name} = ", pud.count(req))

    print(" ----- count with clustering -----")
    print(f"total {xpos} in {pud_file.name}, clustered by exact POS:")
    # print(request_counter())
    print(pd.Series(pud.count(req, ["X.xpos"])).to_frame().rename(columns={0:'total'}).to_markdown(), '\n')

# %%
#* ALL bigrams
req = Request('ADJ [xpos=re"JJ.?"];'
              'mod: ADJ -[advmod]-> ADV;'
              'ADV < ADJ'
              )

# %%
print("\n=============== Count `ADV ADJ` bigrams ===============")
print(f"total `ADV ADJ` bigrams in {pud_file.name}: {pud.count(req)}")
print("\n----- count with clustering -----")
print(f"`ADV ADJ` bigrams in {pud_file.name}, clustered by ADV lemma:")
# print(json.dumps(pud.count(req, ["ADV.lemma"]), indent=2))
pd.Series(pud.count(req, ["ADV.lemma"])).to_frame().reset_index().rename(
    columns={'index':'adverb', 0:'total_bigrams'}
    ).sort_values('total_bigrams', ascending=False)

# %%
print(f"Top 10 `ADV ADJ` bigrams in {pud_file.name}")
pd.json_normalize(pud.count(req, ["ADV.lemma", "ADJ.lemma"]), sep='_').transpose(
    ).rename(columns={0:'total'}).nlargest(10, 'total')

# %%
match_list = pud.search(req)

print("\n=============== `ADV ADJ` bigram match info ===============")
pd.json_normalize(match_list, sep='_')#.transpose().rename(columns={0:'total'}).nlargest(10, 'total')

# %%
def gen_conllus(match_list, corpus):
    
    # for sent in match_list:
    for i, sent in enumerate(match_list):
        parse = corpus.get(sent['sent_id'])
        if i < 3:
            print(parse.to_conll())
        yield parse.to_conll()+'\n'

# %%
conllu_gen = gen_conllus(match_list, pud)

test_out_conllu_path = pud_file.with_name(f'pat-match_{pud_file.name}')
test_out_conllu_path.write_text('\n'.join(conllu_gen), encoding='utf8')

# %%
advadj_subset = grewpy_corpus(str(test_out_conllu_path))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
#* Negated
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
print('-------------------------\nhits:', pud.count(neg_req))

# %%
pd.json_normalize(pud.count(neg_req, ["ADV.lemma", "NEG.lemma"]), sep='_')

# %%
pd.json_normalize(pud.count(neg_req, ["ADV.lemma", "NEG.lemma"]), sep='_').transpose().rename(columns={0:'total'})

# %%
pd.json_normalize(pud.search(neg_req), sep='_')

# %%
neg_df = pd.json_normalize(pud.search(neg_req), sep='_')
neg_df

# %%
neg_df.sent_id.apply(lambda i: pud.get(i).meta['text'])

# %%
for m in neg_df.sent_id.apply(lambda i: pud.get(i).meta): 
    pprint(m)

# %%
pd.json_normalize(neg_df.sent_id.apply(lambda i: pud.get(i).meta), sep='_')

# %%
pd.DataFrame(neg_df.sent_id.apply(lambda i: pud.get(i).meta))

# %%
hit_meta = pd.json_normalize(neg_df.sent_id.apply(lambda i: pud.get(i).meta)).convert_dtypes()
hit_meta

# %%
neg_df = neg_df.assign(sent_text=hit_meta.text, 
                    #    new_doc_id=hit_meta['']
                       )
neg_df

# %%
neg_df = pd.json_normalize(pud.search(neg_req), sep='_').convert_dtypes()
neg_df.columns = neg_df.columns.str.replace('matching_', '')
neg_df

# %%
hit_meta = pd.json_normalize(neg_df.sent_id.apply(lambda i: pud.get(i).meta)).convert_dtypes()
hit_meta

# %%
neg_df = neg_df.assign(sent_text=hit_meta.text, 
                       doc_id=neg_df.sent_id.str.rsplit('_', 1).str.get(0), 
                       conllu_id=pud_file.stem
                    #    new_doc_id=hit_meta['']
                       )
neg_df


