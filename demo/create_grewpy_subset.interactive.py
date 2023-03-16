# %%
"""developed from https://github.com/grew-nlp/grewpy/blob/master/examples/test_corpus.py"""
import enum
import os
import sys
from collections import namedtuple
from pathlib import Path
from pprint import pprint

import pandas as pd
from grewpy import Corpus, Request
from grewpy.grew import GrewError as GrewError

# sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

# TODO: add input argument processing for: `conllu_path`, `pat_path`, and `(out)label`

# %%[markdown]

# ## Define functions

_META_TUP = namedtuple(
    'meta_info',
    ['sent_id', 'doc_id', 'sent_int', 'sent_text', 'prev_id', 'prev_text', 'next_id', 'next_text'])


def corpus_from_path(path):
    return Corpus(str(path))


def grewpize_pat(raw_text):
    return ''.join(line.strip() for line in raw_text.split('{', 1)[1].split('}', 1)[0].strip().splitlines())

def parse_sent(sent_id):
    doc_id, ordinal_str = sent_id.rsplit('_', 1)
    ordinal_int = int(ordinal_str)

    row = (sent_id, doc_id, ordinal_int, co.get(sent_id).meta['text'])
    for context_ix in (ordinal_int + i for i in (-1, 1)):
        c_text = ''
        c_id = ''
        # > conllu doc sentence numbering starts at 1
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


def pprint_pat(request):
    print(str(request).replace(';', ';\n\t '))

def table_by_1(corpus: Corpus, pattern_request: Request, cluster: list, total_hits):

    df = pd.Series(corpus.count(pattern_request, cluster)).to_frame().rename(
        columns={0: 'total'})
    df = df.assign(percent=(df.total / total_hits * 100).round(1))
    df = df.sort_values('total', ascending=False)

    return df

def table_by_2(corpus, request, cluster, total_hits):
    df = pd.json_normalize(corpus.count(request, cluster), sep='_').transpose(
    ).rename(columns={0: 'total'})
    df = df.assign(percent=(df.total / total_hits * 100).round(1))
    df = df.sort_values('total', ascending=False)
    
    return df


# %%
# Program to Get file size in human-readable units like KB, MB, GB, TB

class sizeUnit(enum.Enum):
    # class to store the various units
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def unitConvertor(sizeInBytes, unit):
    # Cinverts the file unit
    if unit == sizeUnit.KB:
        return sizeInBytes/1024
    elif unit == sizeUnit.MB:
        return sizeInBytes/(1024*1024)
    elif unit == sizeUnit.GB:
        return sizeInBytes/(1024*1024*1024)
    else:
        return sizeInBytes


def fileSize(filePath, size_type, decimals=1):
    """File size in KB, MB and GB"""
    size = os.path.getsize(filePath)
    return round(unitConvertor(size, size_type), decimals)


# %% [markdown]
# Should be able to set this up to have `conllu_path` (and `pat_path`?)
#       as input, and run it in parallel on a list of files,
#       even files from different directories

# %%
# TODO: add argument parsing (at least `argv` if not `argparse`)
pat_path = Path('Pat/advadj/all-RB-JJs.pat')

# pat_paths = Path.cwd().glob('Pat/[acsr]*/*.pat')
# for pat_path in pat_paths:
#     print(str(pat_path))

conllu_path = Path(
    # "/home/arh234/data/puddin/PccVa.conll/pcc_eng_val-03.conllu"
    # "/home/arh234/projects/sanpi/demo/data/corpora/gitrepo_puddin/2smallest.conll/apw_eng_199911.conllu"
    # "data/corpora/gitrepo_puddin/2smallest.conll/apw_eng_199911.conllu"
    "./data/corpora/gitrepo_puddin/2smallest.conll/nyt_eng_200405.conllu"
)
file_size = fileSize(conllu_path,sizeUnit.MB)
print(f'Loading corpus from {conllu_path} ({file_size} MB)...')
co = corpus_from_path(conllu_path)

# %% [markdown]
# # Describing the corpus input

#  %%
counts_df = pd.DataFrame(index=['total'], columns=[
                         'file_size', 'sentences', 'tokens', 'ADV', 'ADJ', 'NEG'])
counts_df['file_size'] = f'{file_size} MB'
counts_df['sentences'] = len(co)
counts_df['tokens'] = sum(len(s) for s in co)

# %%
for name, spec in (
    ('ADV', 'xpos=re"RB.*"'),
    ('ADJ', 'xpos=re"JJ.*"'),
    ('NEG', ('lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|'
             '"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"'),
     # TODO: add neg raising lemma node
     #  'N-R', ()
     )):

    req = Request(f'X[{spec}]')
    total_count = co.count(req)
    counts_df[name] = total_count

    print(f"\nTotal {name} in {conllu_path.name} by exact POS:\n")
    print(table_by_1(co, req, ["X.xpos"], total_count).to_markdown(), '\n')

    print(f"\nTop 10 {name} lemma in {conllu_path.name}\n")
    print(table_by_1(co, req, ["X.lemma"], total_count).nlargest(
        10, 'total').to_markdown(), '\n')

print(f"# {conllu_path.name} overview\n")
print(counts_df.transpose().to_markdown())


# %%[markdown]
# ## `ADV ADJ` bigrams/collocations
# %%
req = Request(grewpize_pat(pat_path.read_text(encoding='utf8')))
pprint_pat(req)

# %%
total_hits = co.count(req)
print("\n## `ADV ADJ` bigrams in", conllu_path.name)
print(f"total `ADV ADJ` bigrams in {conllu_path.name}: {total_hits}")

# %%
print(f"\n## Count bigrams in {conllu_path.name} with clustering")
print(f"Bigrams by ADV lemma: Top 10")
print(table_by_1(co, req, ["ADV.lemma"], total_hits).nlargest(
    10, 'total').to_markdown())

# %%
print(f"Top 5 `ADV ADJ` bigrams in {conllu_path.name}")
print(table_by_2(co, req, ["ADV.lemma", "ADJ.lemma"],
      total_hits).nlargest(5, 'total').to_markdown())

# %% [markdown]
# ### Collect context info

#%%
context_info = pd.concat(pd.DataFrame(parse_sent(
                         match['sent_id'])) for match in co.search(req))
context_info = context_info.assign(conllu_id=conllu_path.stem).set_index('sent_id')

context_info = context_info[['conllu_id', 'doc_id', 'sent_int',
                       'prev_id', 'next_id', 'prev_text', 'sent_text', 'next_text']]

# %%[markdown]
# ### Save `context_info` dataframe as .psv

# Example row: 
# |           | apw_eng_19991101_0021_10                                                                                                                                                                                                                                     |
# |:----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
# | conllu_id | apw_eng_199911                                                                                                                                                                                                                                               |
# | doc_id    | apw_eng_19991101_0021                                                                                                                                                                                                                                        |
# | sent_int  | 10                                                                                                                                                                                                                                                           |
# | prev_id   | apw_eng_19991101_0021_9                                                                                                                                                                                                                                      |
# | next_id   | apw_eng_19991101_0021_11                                                                                                                                                                                                                                     |
# | prev_text | -LBQ-  That 's called logical , consistent thinking , which unfortunately is not the way of Washington , D.C. , right now ,  -RDQ-  said A. Michael Noll , a University of Southern California communications professor and a former AT & employee .         |
# | sent_text | AT & claims that limiting the number of access providers may not be so bad , because a company that can plan its investment in all the equipment it requires to run the Internet through TV cables can offer service faster , cheaper and more efficiently . |
# | next_text | -LBQ-  We 're moving into an information-based economy .                                                                                                                                                                                                     |

# %%
subset_dir = conllu_path.parent.joinpath(f'subset_{pat_path.parent.stem}')
if not subset_dir.is_dir():
    subset_dir.mkdir()
label = pat_path.stem
# TODO: make `label` an input option
context_path = subset_dir.joinpath(
    f'{label}:{conllu_path.stem}.context.psv')
context_info.to_csv(context_path, sep='|')
print(f'✔️ context info for {label} subset of {conllu_path.name} saved as:\n'
      f'     {context_path}')

# %%[markdown]
# ## Create subset conllu and save to file
# %%
subset_path = subset_dir.joinpath(f'{label}:{conllu_path.name}')
subset_path.write_text('\n'.join(co.get(id).to_conll() for id in context_info.index), encoding='utf8')

print(f'✔️ {label} subset of {conllu_path.name} saved as:\n'
      f'     {subset_path}')

