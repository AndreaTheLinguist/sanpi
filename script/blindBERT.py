##// %% [markdown]
##// <a href="https://colab.research.google.com/gist/AndreaTheLinguist/67c76e226c22a62dc0bc796e4f279ba7/get_bert_scores.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

##// %% [markdown]
##// Mount Google Drive, install transformers, import packages

##// %%
##// from google.colab import drive
##// drive.mount('/content/drive/')

# %%
# Install `transformers` from master
!pip install transformers
!pip list | grep -E 'transformers|tokenizers'
# transformers version at notebook update --- 2.11.0
# tokenizers version at notebook update --- 0.8.0rc1

from transformers import AutoTokenizer, AutoModel
from transformers import AutoModelForMaskedLM
from transformers import pipeline
from pprint import pprint
import csv
import pandas as pd
import torch

##// %% [markdown]
##// get data from google sheet
#//
##// %%
##// from google.colab import auth
##// auth.authenticate_user()
#//
##// import gspread
##// from oauth2client.client import GoogleCredentials
#//
##// gc = gspread.authorize(GoogleCredentials.get_application_default())
#//
##// worksheet = gc.open('generated_adj_masked_both').sheet1
#//
##// get_all_values gives a list of rows.
##// rows = worksheet.get_all_values()
##//print(rows)
#//
##// Convert to a DataFrame and render.
#//
##// data = pd.DataFrame.from_records(rows)
##// header = data.iloc[0]
##// data = data[1:]
##// data.columns = header
# %% [markdown]
# ## Load sample hit table as data
# %%
dpath = '/share/compling/projects/sanpi/demo/data/2_hit_tables/RBXadj/bigram_X2puddin_all-RB-JJs_hits.csv'
if dpath.endswith('csv'): 
  data = pd.read_csv(dpath)
  data = data.set_index('hit_id')

elif dpath.endswith('pkl.gz'): 
  data = pd.read_pickle(dpath)

print('data loaded')
pprint(data.columns)
data.head()

# %%
#trim data
filter_hi = pd.read_csv(
    '/share/compling/projects/sanpi/demo/data/4_post-processed/RBxpos/hit-index_thr0-001p.1f.txt').squeeze()
data = data.loc[filter_hi, ['adv_form', 'adj_form',
                                      'adv_lemma', 'adj_lemma', 'adv_index', 'adj_index', 'token_str']]
data
# %% 
#Get the column sent and put it into a list
# sents = data['sentences'].tolist()
sents = data.token_str.to_list()
pprint(sents)

# %% [markdown]
# ## Mask tokens
# In this version, the data is not pre-masked.
# It consists of sentence strings and target information, including the index of token nodes in the `token_str` values.
# Should be able to use the `adv_index` and/or `adj_index` to create the corresponding masked version of `token_str`
#
# _Note: for some reason, the initial filter series, `filiter_hi`, gets reshaped as the index of `data`, so it cannot be used in place of `data.index.to_series()`_
#%%
data = data.assign(
  pre_adv = data.index.to_series().apply(lambda h: ' '.join(data.token_str[h].split()[:data.adv_index[h]-1])), 
  post_adv=data.index.to_series().apply(lambda h: ' '.join(data.token_str[h].split()[data.adv_index[h]+1:])))
data
#%%
data = data.assign(
  masked=data.pre_adv + ' [MASK] ' + data.post_adv)


# %% [markdown]
# Data is loaded and now _masked_ sentences are a column in the dataframe. Now use unmasker to get probabilities of tokens at masked position:

# %%
model = 'bert-base-uncased'

#Create pipeline that will do the unmasking
unmasker = pipeline('fill-mask', model=model, tokenizer=model, framework='pt')

#%%
#let's try this on an example sentence
# sent = sents[0]
sent = data.masked[0]
print(sent)
# sent_n = "There was a feeling out there that it wasn't [MASK] religious"
# sent_p = "There was a feeling out there that it was [MASK] religious"

# %%
#get top 5 predictions
results = unmasker(sent, top_k=20)
pprint(results)

# %% [markdown]
# Loop through every sentence/sentence pair in list and record scores.

# %%
pprint(sents)

scores = []
col = data.columns
print(type(col))


for i in data.index:

  sent = data['sentences'][i]
  results = unmasker(sent, top_k=20)
  # print(type(results))
  # pprint(results)

  for r in results:

    r['input'] = sent
    r['mask_type'] = data['mask_type'][i]
    r['pred_pos'] = data['pred_pos'][i]
    r['scale_type'] = data['scale_type'][i]

    scores.append(r)

  # pprint(results)

# for i, s in enumerate(sents[:2]):

#   print(s)
#   # get results (as list of dictionaries)
#   results = unmasker(s, top_k=20)
#   results['mask_type'] = mask_type[i]
#   results['pred_pos'] = mask

#   # save results to dict
#   scores[s] = results

print('\nScores:')
for s in scores:

  pprint(s)

with open('/content/drive/MyDrive/ColabNotebooks/scores.csv', 'w') as output:

    csv_dictwriter = csv.DictWriter(output, fieldnames=scores[0].keys())

    csv_dictwriter.writeheader()

    csv_dictwriter.writerows(scores)

  # scores.to_csv('/content/drive/MyDrive/ColabNotebooks/scores.csv', index=False)

# %%



