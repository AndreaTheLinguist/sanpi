# %%
import stanza
from pprint import pprint
from pathlib import Path
from sys import argv
_DOC2CONLL_TEXT = stanza.utils.conll.CoNLL.doc2conll_text

# %%
try:
    # print('Loading dependency parsing pipeline...')
    NLP = stanza.Pipeline(
            lang='en',
            processors='tokenize,pos,lemma,depparse')
except stanza.pipeline.core.ResourcesFileNotFoundError:
    # print('Language model not found. Downloading...')
    stanza.download('en')
    # print('Loading dependency parsing pipeline...\n')
    NLP = stanza.Pipeline(
            lang='en',
            processors='tokenize,pos,lemma,depparse')

# %%
sentence = argv[1]

# %%
doc = NLP(sentence)
conllu = _DOC2CONLL_TEXT(doc)
print(conllu[:-1])
# with open(Path('/home/arh234/projects/sanpi/sandbox/examples.conllu'), mode='append') as o: 
#     o.write(conllu + '\n')


