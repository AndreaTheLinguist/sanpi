"""original copied from https://github.com/grew-nlp/grewpy/blob/master/examples/test_corpus.py"""
import sys, os, json

# sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

from grewpy import Graph, CorpusDraft, Request, Corpus, request_counter
from pathlib import Path

def docs(expr): 
  
  try: 
    print(expr.__doc__)
  except AttributeError: 
    print('None')

pud_file = Path("data/corpora/testing/small/small.conll/apw_eng_199911.conllu")
pud = Corpus(str(pud_file))

print ("\n=============== len ===============")
print(f"sentence count in {pud_file.name} = {len(pud)}")
print (request_counter())

print ("\n=============== Get one graph ===============")
sent_id="apw_eng_19991101_0001_1"
graph = pud[sent_id]
print(f"nb of nodes of {sent_id} = ", len(graph))
print (request_counter())

print(f"len(pud[0]) = {len(pud[0])}")
print(f"len(pud[-1]) = {len(pud[-1])}")
print(f"[len(g) for g in pud[-3:]] = {[len(g) for g in pud[-3:]]}")
#other forms pud[-3:-1], pud[1:7:2], ...


# dprint ("\n=============== Iteration on graphs of a corpus ===============")
# print ("⚠️  generate one request to Grew backend for each graph")
# acc = 0
# for sent_id in pud.get_sent_ids():
#   acc += len(pud[sent_id])
# print(f"nb of nodes in {pud_file} = ", acc)
# print (request_counter())

print ("\n=============== Count request in a corpus ===============")
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
  print(f"nb of {xpos} in {pud_file.name} = ", pud.count(req))

  print (" ----- count with clustering -----")
  print(f"nb of {xpos} in {pud_file.name}, clustered by exact POS:")
  print (json.dumps(pud.count(req, ["X.xpos"]), indent=2))
  print (request_counter())

req = Request('ADJ [xpos=re"JJ.?"];'
              'mod: ADJ -[advmod]-> ADV;'
    'ADV < ADJ;'
    # 'NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];'
    # 'neg: ADJ -[re"[^E].*"]-> NEG;'
    # 'NEG << ADV'
    )

print(" ----- basic count -----")
print(f"nb of ADV in {pud_file.name} = ", pud.count(req))

print (" ----- count with clustering -----")
print(f"nb of ADV in {pud_file.name}, clustered by lemma:")
match_list = pud.search(req)
for sent in match_list: 
    
  parse = pud.get(sent)
  
  
print(json.dumps(pud.count(req, ["ADV.lemma"]), indent=2))
print (request_counter())


# corpus = CorpusDraft(pud)
# print("\n=============== Iteration on graphs of a corpus ===============")
# acc = 0
# for sent_id in corpus:
#   acc += len(corpus[sent_id])
# print(f"nb of nodes in {pud_file} = ", acc)
# print (request_counter())

# def clear_edges(graph):
#     for n in graph:
#         graph.sucs[n] = []

# for sid in corpus:
#   clear_edges(corpus[sid])

# noedge_corpus = Corpus(corpus)
# print(" ----- counting nsubj within corpus -----")
# dep = "nsubj"
# req = Request(f"X[];Y[];X -[{dep}]-> Y")
# print(f"nb of {dep} in {pud_file} = ", pud.count(req))
# print(f"nb of {dep} in noedge_corpus = ", noedge_corpus.count(req))

exit(0)



req = Request(f"X -[fixed]-> Y")
print (" ----- count with clustering -----")
print(f"nb of fixed in {pud_file}, clustered by head.lemma:")
print (json.dumps(pud.count(req, ["X.lemma"]), indent=2))

g = pud[sent_id]
for n in g:
  for (s,e) in g.suc(n):
    if e  == {'1' : 'fixed'}:
      print(f"\n{n} : {g[n]} -[{e}]-> {s} : {g[s]}\n")

clear_edges(g)
#pud[sent_id] = g
# NOTE: the next line does not work properly (not __set_item__ called), have a look to https://stackoverflow.com/questions/26189090/how-to-detect-if-any-element-in-a-dictionary-changes
# clear_edges(pud[sent_id]) ==> WARNING: does not change pud!

