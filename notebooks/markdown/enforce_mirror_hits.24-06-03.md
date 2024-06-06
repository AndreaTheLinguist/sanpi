```python
import re
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, print_iter
from source.utils.sample import sample_pickle

HIT_EX_COLS = ['WITH::^.[il].*lower', 'WITH::text', 'token_str']
# sanpi/4_post-processed/POSmirror/trigger-bigrams_frq-thrMIN-7.35f.pkl.gz
pkl_name = 'trigger-bigrams_frq-thrMIN-7.35f.pkl.gz'
path_dict = {p: POST_PROC_DIR / p / pkl_name for  p in ('POSmirror','NEGmirror')}
path_dict
```

    {'POSmirror': PosixPath('/share/compling/data/sanpi/4_post-processed/POSmirror/trigger-bigrams_frq-thrMIN-7.35f.pkl.gz'),
     'NEGmirror': PosixPath('/share/compling/data/sanpi/4_post-processed/NEGmirror/trigger-bigrams_frq-thrMIN-7.35f.pkl.gz')}




```python
nmir = pd.read_pickle(path_dict['NEGmirror'])
```


```python
pmir = pd.read_pickle(path_dict['POSmirror'])
```


```python
pmir[pmir.bigram_lower.str.contains(r"[^\w'-]", regex=True)].bigram_lower.value_counts().nlargest(15)
```




    bigram_lower
    v._good           2
    not_o.k           2
    even_1\/4-inch    1
    v._expensive      1
    fun._amoral       1
    v._religious      1
    too*_ironic       1
    is*_remarkable    1
    v._profound       1
    def._wrong        1
    just_o.k.         1
    so*_expensive     1
    probably_no.      1
    c._ecstatic       1
    b)_impossible     1
    Name: count, dtype: Int64




```python
def update_form_combos(df): 
    
    return df.assign(
        all_forms_lower = df.filter(regex=r'^[nma][^l]\w+lower$').apply(lambda x: '_'.join(x), axis=1),
        bigram_lower = df.filter(['adv_form_lower', 'adj_form_lower']).apply(lambda x: '_'.join(x), axis=1)
                     )


def remove_odd_orth_forms(df):

    df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
           ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
                      ].astype('string')

    def adv_is_very(df):
        return df.adv_form_lower.str.contains(r'^v\.?$|^ve+r+y+$', regex=True)

    def adv_is_def(df):
        return df.adv_form_lower.str.contains(r'^def\.?$', regex=True)

    def adj_is_ok(df):
        return df.adj_form_lower.str.contains(r'^o*\.?k+\.?a*y*$', regex=True)

    print('Dropping most bizarre...')
    print(df.loc[df.bigram_lower.str.contains(r'[\[\\\/)]', regex=True),
          ['adv_form_lower', 'adj_form_lower']].astype('string').value_counts()
          .nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df = df.loc[~df.bigram_lower.str.contains(r'[\[\\\/)]', regex=True), :]

    print('Dropping plain numerals as adjectives')
    print(df.loc[df.adj_form_lower.astype('string').str.contains(r'^\d+$'), ['adv_form_lower', 'adj_form_lower', 'text_window']]
          .astype('string').value_counts().nlargest(10).to_frame().reset_index().to_markdown(floatfmt=',.0f')
          )
    df = df.loc[~df.adj_form_lower.astype('string').str.contains(r'^\d+$'), :]

    print('Translating some known orthographic quirks...')
    # > variations on "very"
    print('\n==== very ====')
    print(df.loc[adv_is_very(df), 'adv_form_lower']
          .astype('string').value_counts().nlargest(10).to_frame()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df.loc[adv_is_very(df), :] = df.loc[adv_is_very(df), :].assign(
        adv_lemma='very',
        adv_form_lower='very')

    # > variations on "ok"
    print('\n==== ok ====')
    print(df.loc[adj_is_ok(df), 'adj_form_lower']
          .astype('string').value_counts().nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df.loc[adj_is_ok(df), :] = df.loc[adj_is_ok(df), :].assign(
        adj_form_lower='ok',
        adj_lemma='ok')

    # > variations on "definitely"
    print('\n==== definitely ====')
    print(df.loc[adv_is_def(df), 'adv_form_lower']
          .astype('string').value_counts().nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df.loc[adv_is_def(df), :] = df.loc[adv_is_def(df), :].assign(adv_form_lower='definitely',
                                                                 adv_lemma='definitely')

    # > drop any single character "words"
    print(df.loc[df.adv_form_lower.str.contains(
        r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
        .astype('string').value_counts().nlargest(10).to_frame().reset_index()
        .to_markdown(floatfmt=',.0f', intfmt=','))
    print(df.loc[df.adj_form_lower.str.contains(
        r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
        .astype('string').value_counts().nlargest(10).to_frame().reset_index()
        .to_markdown())
    df = df.loc[~((df.adv_form_lower.str.contains(r'^\w\W*$'))
                  | (df.adj_form_lower.str.contains(r'^\w\W*$'))), :]

    # > delete remaining non-word characters (esp. `.` & `*`)
    df = df.assign(
        adv_form_lower=df.adv_form_lower.str.strip(
            '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
        adv_lemma=df.adv_lemma.str.strip(
            '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True),
        adj_form_lower=df.adj_form_lower.str.strip(
            '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
        adj_lemma=df.adj_lemma.str.strip(
            '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True)
    )
    df = df.loc[~df.adv_form_lower.isin({'is', 'ie'}), :]
    print('**** **** ****')

    print(df.loc[(df.adv_form_lower.str.contains(r"[^\w'-]", regex=True))
                 | (df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)),
                 ['adv_form_lower', 'adj_form_lower']]
          .astype('string').value_counts()
          .nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=',')
          )
    # print(df[df.adv_form_lower.str.contains(r"[^\w'-]", regex=True)].value_counts(['adv_lemma', 'adv_form_lower','adj_form_lower']))
    # print()
    # print(df[df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)].value_counts(['adj_lemma', 'adj_form_lower','adv_form_lower']))
    df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
           ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
                      ].astype('category')
    return df.convert_dtypes()

```


```python
pmir = remove_odd_orth_forms(pmir)
```

Dropping most bizarre...

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | 1/3rd            | smaller          |       1 |
|  1 | a)               | sick             |       1 |
|  2 | b)               | better           |       1 |
|  3 | b)               | impossible       |       1 |
|  4 | even             | 1\/4-inch        |       1 |

Dropping plain numerals as adjectives

|    | adv_form_lower   |   adj_form_lower | text_window                                              |   count |
|---:|:-----------------|-----------------:|:---------------------------------------------------------|--------:|
|  0 | more             |              401 | be popping up in many more 401 -LRB- k -RRB- plans       |       1 |
|  1 | mostly           |              401 | workers retire on all or mostly 401 -LRB- k -RRB- assets |       1 |

Translating some known orthographic quirks...

==== very ====

| adv_form_lower   |   count |
|:-----------------|--------:|
| very             | 191,968 |
| v                |      13 |
| v.               |       8 |
| verrrry          |       5 |
| verrry           |       4 |
| veeeery          |       3 |
| verry            |       2 |
| veeeeeery        |       2 |
| veeery           |       1 |
| veryyy           |       1 |

==== ok ====

|    | adj_form_lower   |   count |
|---:|:-----------------|--------:|
|  0 | okay             |     807 |
|  1 | ok               |     801 |
|  2 | ooky             |       8 |
|  3 | o.k              |       4 |
|  4 | o.k.             |       3 |
    
==== definitely ====

|    | adv_form_lower   |   count |
|---:|:-----------------|--------:|
|  0 | def.             |       1 |
|  1 | def              |       1 |

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | a-               | ok               |       2 |
|  1 | t                | interested       |       2 |
|  2 | t                | lazy             |       1 |
|  3 | n                | unreal           |       1 |
|  4 | n                | worse            |       1 |
|  5 | o                | dear             |       1 |
|  6 | o                | negative         |       1 |
|  7 | o                | nice             |       1 |
|  8 | o                | unpleasant       |       1 |
|  9 | t                | concerned        |       1 |

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | not              | b                |       2 |
|  1 | so               | e                |       2 |
|  2 | just             | b                |       1 |
|  3 | relatively       | g                |       1 |
|  4 | too              | h                |       1 |
|  5 | so               | r                |       1 |
|  6 | so               | q                |       1 |
|  7 | so               | m                |       1 |
|  8 | so               | h                |       1 |
|  9 | so               | f                |       1 |

****

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | faintly          | s&m              |       1 |
|  1 | more             | r&b              |       1 |
|  2 | more             | r&b-oriented     |       1 |



```python
nmir = remove_odd_orth_forms(nmir)
```

Dropping most bizarre...

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | more             | [...]            |       1 |

Dropping plain numerals as adjectives

|    | adv_form_lower   |   adj_form_lower | text_window                       |   count |
|---:|:-----------------|-----------------:|:----------------------------------|--------:|
|  0 | out              |                0 | Shanthakumaran Sreesanth no out 0 |       1 |

Translating some known orthographic quirks...

==== very ====

| adv_form_lower   |   count |
|:-----------------|--------:|
| very             |   8,956 |

==== ok ====

|    | adj_form_lower   |   count |
|---:|:-----------------|--------:|
|  0 | ok               |      58 |
|  1 | okay             |      51 |

==== definitely ====

| adv_form_lower   | count   |
|------------------|---------|

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | c.               | bad              |       1 |
|  1 | e                | detailed         |       1 |
|  2 | i.               | many             |       1 |
|  3 | l                | great            |       1 |
|  4 | l                | impressed        |       1 |
|  5 | n                | submissive       |       1 |
|  6 | t                | conducive        |       1 |
|  7 | t                | possible         |       1 |
|  8 | t                | worthy           |       1 |
|  9 | u                | equal            |       1 |

|    | adv_form_lower   | adj_form_lower   |   count |
|---:|:-----------------|:-----------------|--------:|
|  0 | far              | f                |       1 |
|  1 | not              | m                |       1 |
|  2 | really           | a-               |       1 |
|  3 | there            | m                |       1 |
|  4 | too              | b                |       1 |

**** 

| adv_form_lower   | adj_form_lower   | count   |
|------------------|------------------|---------|



```python
pmir.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>bigram_id</th>
      <th>token_str</th>
      <th>pattern</th>
      <th>category</th>
      <th>adv_form</th>
      <th>adj_form</th>
      <th>text_window</th>
      <th>mir_deprel</th>
      <th>mir_lemma</th>
      <th>adv_lemma</th>
      <th>...</th>
      <th>mir_form</th>
      <th>mir_index</th>
      <th>adv_index</th>
      <th>adj_index</th>
      <th>mir_form_lower</th>
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>bigram_lower</th>
      <th>all_forms_lower</th>
      <th>prev_form_lower</th>
    </tr>
    <tr>
      <th>hit_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>apw_eng_19941111_0004_1:14-15-16</th>
      <td>apw_eng_19941111_0004_1:15-16</td>
      <td>after being locked out for 41 days , National ...</td>
      <td>pos-mirror-R</td>
      <td>POSmirror</td>
      <td>too</td>
      <td>happy</td>
      <td>Hockey League players were all too happy Thurs...</td>
      <td>advmod</td>
      <td>all</td>
      <td>too</td>
      <td>...</td>
      <td>all</td>
      <td>13</td>
      <td>14</td>
      <td>15</td>
      <td>all</td>
      <td>too</td>
      <td>happy</td>
      <td>too_happy</td>
      <td>all_too_happy</td>
      <td>all</td>
    </tr>
    <tr>
      <th>apw_eng_19941111_0011_5:27-29-30</th>
      <td>apw_eng_19941111_0011_5:29-30</td>
      <td>Volpe and Poland were the only two of the 13 w...</td>
      <td>pos-mirror-R</td>
      <td>POSmirror</td>
      <td>too</td>
      <td>dangerous</td>
      <td>government 's claim that both were too dangero...</td>
      <td>nsubj</td>
      <td>both</td>
      <td>too</td>
      <td>...</td>
      <td>both</td>
      <td>26</td>
      <td>28</td>
      <td>29</td>
      <td>both</td>
      <td>too</td>
      <td>dangerous</td>
      <td>too_dangerous</td>
      <td>both_too_dangerous</td>
      <td>were</td>
    </tr>
    <tr>
      <th>apw_eng_19941111_0090_14:09-12-13</th>
      <td>apw_eng_19941111_0090_14:12-13</td>
      <td>`` It seems like the next meeting could always...</td>
      <td>pos-mirror-R</td>
      <td>POSmirror</td>
      <td>most</td>
      <td>important</td>
      <td>the next meeting could always be the most impo...</td>
      <td>advmod</td>
      <td>always</td>
      <td>most</td>
      <td>...</td>
      <td>always</td>
      <td>8</td>
      <td>11</td>
      <td>12</td>
      <td>always</td>
      <td>most</td>
      <td>important</td>
      <td>most_important</td>
      <td>always_most_important</td>
      <td>the</td>
    </tr>
    <tr>
      <th>apw_eng_19941112_0323_28:08-16-17</th>
      <td>apw_eng_19941112_0323_28:16-17</td>
      <td>that was a big concern , for all of us -- that...</td>
      <td>pos-mirror-L</td>
      <td>POSmirror</td>
      <td>so</td>
      <td>appalling</td>
      <td>big concern , for all of us -- that he would b...</td>
      <td>dep</td>
      <td>all</td>
      <td>so</td>
      <td>...</td>
      <td>all</td>
      <td>7</td>
      <td>15</td>
      <td>16</td>
      <td>all</td>
      <td>so</td>
      <td>appalling</td>
      <td>so_appalling</td>
      <td>all_so_appalling</td>
      <td>be</td>
    </tr>
    <tr>
      <th>apw_eng_19941113_0019_21:2-8-9</th>
      <td>apw_eng_19941113_0019_21:8-9</td>
      <td>Handling all of the egos involved was surprisi...</td>
      <td>pos-mirror-R</td>
      <td>POSmirror</td>
      <td>surprisingly</td>
      <td>easy</td>
      <td>Handling all of the egos involved was surprisi...</td>
      <td>advmod</td>
      <td>all</td>
      <td>surprisingly</td>
      <td>...</td>
      <td>all</td>
      <td>1</td>
      <td>7</td>
      <td>8</td>
      <td>all</td>
      <td>surprisingly</td>
      <td>easy</td>
      <td>surprisingly_easy</td>
      <td>all_surprisingly_easy</td>
      <td>was</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>




```python
nmir.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 293947 entries, pcc_eng_11_001.0326_x0000513_088:14-15-16 to pcc_eng_10_108.10108_x1747378_18:7-8-9
    Data columns (total 21 columns):
     #   Column           Non-Null Count   Dtype   
    ---  ------           --------------   -----   
     0   bigram_id        293947 non-null  string  
     1   token_str        293947 non-null  string  
     2   pattern          293947 non-null  category
     3   category         293947 non-null  category
     4   neg_form         293947 non-null  string  
     5   adv_form         293947 non-null  string  
     6   adj_form         293947 non-null  string  
     7   text_window      293947 non-null  string  
     8   neg_deprel       293947 non-null  string  
     9   neg_lemma        293947 non-null  string  
     10  adv_lemma        293947 non-null  category
     11  adj_lemma        293947 non-null  category
     12  neg_index        293947 non-null  UInt16  
     13  adv_index        293947 non-null  UInt16  
     14  adj_index        293947 non-null  UInt16  
     15  neg_form_lower   293947 non-null  string  
     16  adv_form_lower   293947 non-null  category
     17  adj_form_lower   293947 non-null  category
     18  bigram_lower     293947 non-null  string  
     19  all_forms_lower  293947 non-null  string  
     20  prev_form_lower  293947 non-null  string  
    dtypes: UInt16(3), category(6), string(12)
    memory usage: 35.2 MB



```python
pmir.loc[:, ['bigram_lower','all_forms_lower']] = update_form_combos(pmir.filter(like='lower')).loc[:, ['bigram_lower','all_forms_lower']]

```


```python
nmir.loc[:, ['bigram_lower','all_forms_lower']] = update_form_combos(nmir.filter(like='lower')).loc[:, ['bigram_lower','all_forms_lower']]
```


```python
def str_to_cat(df):
    cat_cols = df.filter(regex=r'form|bigram|lemma|deprel|head').columns
    df[cat_cols] = df[cat_cols].astype('category')
    # df.info()
    return df
```


```python
pmir = str_to_cat(pmir)
```


```python
nmir = str_to_cat(nmir)
```


```python
def set_col_widths(df):
    cols = df.copy().reset_index().columns
    width_dict = (
        {c: None for c in cols}
        | {c: 22 for c in cols[cols.str.contains('_id')]}
        | {c: 45 for c in cols[cols.str.contains('text')]}
        | {c: 30 for c in cols[cols.str.contains('forms')]}
        | {c: 60 for c in cols[cols.str.contains('_str')]})
    return list(width_dict.values())
```


```python
print_iter(header = 'POSmirror columns:', iter_obj= pmir.columns.to_list())
print_iter(header = 'NEGmirror columns:', iter_obj= nmir.columns.to_list())
```

    
POSmirror columns:
- `bigram_id`
- `token_str`
- `pattern`
- `category`
- `adv_form`
- `adj_form`
- `text_window`
- `mir_deprel`
- `mir_lemma`
- `adv_lemma`
- `adj_lemma`
- `mir_form`
- `mir_index`
- `adv_index`
- `adj_index`
- `mir_form_lower`
- `adv_form_lower`
- `adj_form_lower`
- `bigram_lower`
- `all_forms_lower`
- `prev_form_lower`

NEGmirror columns:
- `bigram_id`
- `token_str`
- `pattern`
- `category`
- `neg_form`
- `adv_form`
- `adj_form`
- `text_window`
- `neg_deprel`
- `neg_lemma`
- `adv_lemma`
- `adj_lemma`
- `neg_index`
- `adv_index`
- `adj_index`
- `neg_form_lower`
- `adv_form_lower`
- `adj_form_lower`
- `bigram_lower`
- `all_forms_lower`
- `prev_form_lower`



```python
def show_sample(df: pd.DataFrame,
                format: str = 'grid',
                limit_cols: bool = True):
    if limit_cols and format != 'pipe':
        col_widths_list = set_col_widths(df)
    else:
        col_widths_list = [None] * len(df.columns)
    print(df.to_markdown(
        floatfmt=',.0f', intfmt=',',
        maxcolwidths=col_widths_list, 
        tablefmt=format
        ))
```


```python
show_sample(pmir.pattern.value_counts().to_frame(), limit_cols=False, format='pipe')
```

| pattern      |     count |
|:-------------|----------:|
| pos-mirror-R | 1,364,547 |
| pos-mirror-L |   373,490 |



```python
show_sample(nmir.pattern.value_counts().to_frame(), limit_cols=False, format='pipe')
```

| pattern      |   count |
|:-------------|--------:|
| neg-mirror-R | 216,886 |
| neg-mirror-L |  77,061 |



```python
REGNOT=r" (n[o']t) "
def embolden(series,
            bold_regex=None):
    bold_regex = re.compile(bold_regex) if bold_regex else REGNOT
    return series.apply(
        lambda x: bold_regex.sub(r' __`\1`__ ', x))
```

## Problem Sentences

The following examples are all from the `POSmirror` data set which should not include any negative triggers. 
I believe the issue may be due to unexpected parses or cases where the negative trigger dependency is indirect or scopes over the identified positive trigger. 


```python
for adv in ['exactly', 'ever', 'necessarily', 'yet']:
    for pat_suff in ['L', 'R']:
        problems = sample_pickle(
            data=pmir, sample_size=6, regex=True, print_sample=False,
            filters=[f'token_str== {REGNOT} .* {adv} ',
                    f'adv_form_lower==^{adv}$', 
                    f'pattern==.*{pat_suff}$'],
            columns=['mir_form_lower', 'bigram_lower', 'text_window', 'token_str'],
            sort_by='all_forms_lower')

        show_sample(
            problems.loc[problems.token_str.str.contains(f'{REGNOT}.*{adv}')].assign(
                token_str=embolden(problems.token_str, f' ({REGNOT}|{adv}) '),
                text_window=embolden(problems.text_window, f' ({REGNOT}|{adv}) ')
            ),
            format='pipe', limit_cols=False)
```


- *filtering rows...*
  - regex parsing = True
  - Filter expression `token_str==  (n[o']t)  .* exactly ` matched zero rows. Filter not applied.
  - ✓ Applied filter: `adv_form_lower==^exactly$`
  - ✓ Applied filter: `pattern==.*L$`

### 6 random rows matching filter(s) from `input frame`

| hit_id                                    | mir_form_lower   | bigram_lower      | text_window                                                             | token_str                                                                                                                                                                                                                                                                                                                                                                                      |
|:------------------------------------------|:-----------------|:------------------|:------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19990108_0419_27:5-8-9            | someone          | exactly_simpatico | and he is not someone who was __`exactly`__ simpatico with the Gramm of | and he is not someone who was __`exactly`__ simpatico with the Gramm of old .                                                                                                                                                                                                                                                                                                                  |
| apw_eng_20070219_0931_10:22-24-25         | something        | exactly_alien     | of the dictum -- something not __`exactly`__ alien to him .             | Bellamy , who has a history of losing his temper , looks to be the first casualty of the dictum -- something not __`exactly`__ alien to him .                                                                                                                                                                                                                                                  |
| pcc_eng_21_004.3936_x0054774_071:62-63-64 | something        | exactly_new       | so it 's not something __`exactly`__ new with him ] )                   | It 's also missing some of his earlier stuff , but the " KMD " ( Kurious and another random dude Doom was supposedly gonna make a new KMD album with [ another of the many rumored - but- never- seen Doom projects a la Madvillainy 2 & the Ghost collab - this was from like 2000 so it 's not something __`exactly`__ new with him ] ) track Sorcerors is on there , which is really nice . |


- *filtering rows...*
  - regex parsing = True
  - Filter expression `token_str==  (n[o']t)  .* exactly ` matched zero rows. Filter not applied.
  - ✓ Applied filter: `adv_form_lower==^exactly$`
  - ✓ Applied filter: `pattern==.*R$`

### 6 random rows matching filter(s) from `input frame`

| hit_id                                   | mir_form_lower   | bigram_lower   | text_window                                             | token_str                                               |
|:-----------------------------------------|:-----------------|:---------------|:--------------------------------------------------------|:--------------------------------------------------------|
| pcc_eng_22_098.7323_x1579436_44:04-09-10 | all              | exactly_true   | Well , not all of these things are __`exactly`__ true . | Well , not all of these things are __`exactly`__ true . |



- *filtering rows...*
  - regex parsing = True
  - Filter expression `token_str==  (n[o']t)  .* ever ` matched zero rows. Filter not applied.
  - ✓ Applied filter: `adv_form_lower==^ever$`
  - ✓ Applied filter: `pattern==.*L$`

### 6 random rows matching filter(s) from `input frame`

| hit_id                                  | mir_form_lower   | bigram_lower   | text_window                                                             | token_str                                                                                                                                                                                                                                                  |
|:----------------------------------------|:-----------------|:---------------|:------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pcc_eng_11_083.0903_x1328650_1:25-26-27 | everyone         | ever_involved  | admittedly not familiar with everyone __`ever`__ involved with the Wo W | There are other items in the patch files that look to be named after certain individuals , but I 'm admittedly not familiar with everyone __`ever`__ involved with the Wo W community , so I 'll leave it to you guys to let me know if I missed someone . |

---

- This could be dealt with by modifying the patterns (i.e. the `WITHOUT` clauses specifically) and rerunning everything, but
  1. There's no telling how long that would take 
  2. verifying its accuracy is difficult
  3. even with 100% accurate patterns for *correct* parses, there is no way to prevent or really even predict all possible *mis*parses
- So there is a better way: 
  
  The preponderance of positive data provides a large margin for additional data exclusions without unbalancing the samples---in fact, 
  it actually brings `[POSMIR,f1]` _closer_ to the negative sample size, `[NEGMIR, f1]`.

  Therefore, it is possible to simply drop anything with a likely negation preceding the bigram, 
  regardless of the polarity environment the particular syntactic configuration creates, and call it a day.



```python
# pmir['adv_index'] = pd.to_numeric(pmir.index.to_series().str.split(':').str.get(-1).apply(lambda i: re.search(r'-(\d+)-', i).group().strip('-')), downcast='unsigned')
pmir['preceding_text'] = pmir.apply(lambda x: x.token_str.split()[:x.adv_index - 1], axis='columns').astype('string').str.join(' ')
```


```python
show_sample(pmir[['preceding_text', 'bigram_lower', 'token_str']].sample(5))
```

    +------------------------+-----------------------------------------------+----------------+--------------------------------------------------------------+
    | hit_id                 | preceding_text                                | bigram_lower   | token_str                                                    |
    +========================+===============================================+================+==============================================================+
    | pcc_eng_23_038.1062_x0 | As can be seen , Lian and Brian 's episode    | too_familiar   | As can be seen , Lian and Brian 's episode will focus on the |
    | 599468_38:24-25-26     | will focus on the topic of autism , a subject |                | topic of autism , a subject Ler himself is all too familiar  |
    |                        | Ler himself is                                |                | with as he has family members afflicted with autism and he   |
    |                        |                                               |                | explains that it is partly because of this that he feels a   |
    |                        |                                               |                | strong need to raise awareness of the issue in Singapore .   |
    +------------------------+-----------------------------------------------+----------------+--------------------------------------------------------------+
    | pcc_eng_24_108.05817_x | Tosh was always                               | most_militant  | Tosh was always the most militant of the original Wailers    |
    | 1741307_08:3-5-6       |                                               |                | and this album reflects that outlook .                       |
    +------------------------+-----------------------------------------------+----------------+--------------------------------------------------------------+
    | pcc_eng_19_013.6113_x0 | So even                                       | as_simple      | So even something as simple as reminding a tenant what to do |
    | 203717_51:3-4-5        |                                               |                | and reporting any unusual - coloured water or temperatures   |
    |                        |                                               |                | to a landlord can help .                                     |
    +------------------------+-----------------------------------------------+----------------+--------------------------------------------------------------+
    | pcc_eng_28_018.9428_x0 | If surgery is necessary , Bushnell said , the | very_good      | If surgery is necessary , Bushnell said , the technology is  |
    | 290042_162:26-27-28    | technology is so advanced , and the surgery   |                | so advanced , and the surgery is so common , that the        |
    |                        | is so common , that the outcome is            |                | outcome is often very good , giving people like the Johnsons |
    |                        |                                               |                | and the Woznickis a chance to further enjoy the hearts they  |
    |                        |                                               |                | gave to one another more than half a century ago .           |
    +------------------------+-----------------------------------------------+----------------+--------------------------------------------------------------+
    | pcc_eng_22_048.9377_x0 | If someone would                              | so_kind        | If someone would be so kind as to link me to a Google Doc    |
    | 774719_5:2-5-6         |                                               |                | containing , IDK , maybe a .zip file with a Pokemon Platinum |
    |                        |                                               |                | rom inside , that would be just plain amazing and I 'd love  |
    |                        |                                               |                | it .                                                         |
    +------------------------+-----------------------------------------------+----------------+--------------------------------------------------------------+



```python
show_sample(pmir[['preceding_text', 'bigram_lower', 'token_str']].sample(5), format='pipe')
```

| hit_id                                   | preceding_text                                                                                                                                                                                                              | bigram_lower             | token_str                                                                                                                                                                                                                                                 |
|:-----------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pcc_eng_11_072.9334_x1164379_04:30-32-33 | This pierces ( but does not completely shatter ) what I believe has been a six-decade embargo by prison administrators to hold back information on how many prisoners are or                                                | nt_religious             | This pierces ( but does not completely shatter ) what I believe has been a six-decade embargo by prison administrators to hold back information on how many prisoners are or are n't religious .                                                          |
| pcc_eng_20_036.2341_x0569583_6:37-38-39  | I recently completed a collection of poems based on Old Testament stories called ' Ichabod and Other Voices ' and am interested in the way in which the mundane and inconsequential co-exists alongside the deeply profound | historically_significant | I recently completed a collection of poems based on Old Testament stories called ' Ichabod and Other Voices ' and am interested in the way in which the mundane and inconsequential co-exists alongside the deeply profound or historically significant . |
| pcc_eng_00_012.3002_x0182514_19:6-7-8    | I 'm glad you 're                                                                                                                                                                                                           | equally_prosperous       | I 'm glad you 're both equally prosperous in your careers .                                                                                                                                                                                               |
| pcc_eng_16_078.3949_x1252557_31:13-14-15 | There are many ways of refining coconut oil made from copra ,                                                                                                                                                               | more_healthy             | There are many ways of refining coconut oil made from copra , some more healthy than others .                                                                                                                                                             |
| pcc_eng_16_042.5589_x0672568_30:26-28-29 | The loss of use coverages of homeowners policies issued by insurers that do not use the standard ISO HO 2 or HO 3 policy forms often                                                                                        | substantially_similar    | The loss of use coverages of homeowners policies issued by insurers that do not use the standard ISO HO 2 or HO 3 policy forms often are substantially similar to the standard form policies .                                                            |



```python
pmir['after_neg'] = pmir.preceding_text.str.lower().str.contains(r"\b(no|n[o']t|no(body| one|thing|where)|(rare|scarce|bare|hard)ly|seldom|without|never)\b", regex=True)
show_sample(pmir.loc[pmir.after_neg, ['preceding_text', 'bigram_lower', 'token_str']].sample(10))
```

    /tmp/ipykernel_28876/3396796712.py:1: UserWarning: This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.
      pmir['after_neg'] = pmir.preceding_text.str.lower().str.contains(r"\b(no|n[o']t|no(body| one|thing|where)|(rare|scarce|bare|hard)ly|seldom|without|never)\b", regex=True)


    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | hit_id                 | preceding_text                                | bigram_lower         | token_str                                                    |
    +========================+===============================================+======================+==============================================================+
    | pcc_eng_01_026.0198_x0 | Sitting around in 95 degree weather just      | necessarily_fun      | Sitting around in 95 degree weather just waiting on some     |
    | 404751_13:22-23-24     | waiting on some sweaty dudes to show up all   |                      | sweaty dudes to show up all at once is not easy or           |
    |                        | at once is not easy                           |                      | necessarily fun .                                            |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_25_047.4015_x0 | I may not have much of a social life , but I  | even_better          | I may not have much of a social life , but I have something  |
    | 751293_059:14-15-16    | have                                          |                      | even better .                                                |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_26_051.2414_x0 | It 's not comical to assume someone would     | more_productive      | It 's not comical to assume someone would be more productive |
    | 812297_37:07-10-11     |                                               |                      | at something when doing a thing they 're historically good   |
    |                        |                                               |                      | at than something they have no experience in .               |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_04_031.9275_x0 | This is not to be confused with wheel         | completely_different | This is not to be confused with wheel balancing , which is   |
    | 499730_07:13-14-15     | balancing , which is                          |                      | something completely different , though they both affect the |
    |                        |                                               |                      | ride and handling of a motor vehicle .                       |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_02_053.0154_x0 | But once this practical possibility no longer | purely_philosophical | But once this practical possibility no longer seems feasible |
    | 841379_26:15-17-18     | seems feasible , then this approach would     |                      | , then this approach would either be purely philosophical or |
    |                        | either                                        |                      | it would turn against the potentialities of the present An   |
    |                        |                                               |                      | Aging India : Perspectives , Prospects , and Policies .      |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | apw_eng_20000228_0098_ | `` Some were not for something that           | medically_necessary  | `` Some were not for something that was medically necessary  |
    | 11:06-09-10            |                                               |                      | , '' Klimmerman .                                            |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_14_090.1559_x1 | Some who remain without coverage simply       | nt_eligible          | Some who remain without coverage simply are n't eligible     |
    | 441113_69:1-8-9        |                                               |                      | under the new law : undocumented immigrants and people who   |
    |                        |                                               |                      | live in states that opt out of the Medicaid expansion .      |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_27_084.2710_x1 | Rarely a person is so traumatized , or so     | so_stuck             | Rarely a person is so traumatized , or so full of entities , |
    | 346849_177:14-15-16    | full of entities ,                            |                      | or so stuck for some other reason , that it is difficult to  |
    |                        |                                               |                      | work with him or her .                                       |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_04_020.3016_x0 | When a basic U-lock wo n't do , riders have   | most_convenient      | When a basic U-lock wo n't do , riders have been turning to  |
    | 311689_02:29-30-31     | been turning to chain - based locks that      |                      | chain - based locks that protect your bike , but are n't     |
    |                        | protect your bike , but are n't exactly the   |                      | exactly the easiest or most convenient thing to carry around |
    |                        | easiest                                       |                      | .                                                            |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+
    | pcc_eng_23_040.4716_x0 | " When I said people who look like me -- I    | necessarily_smart    | " When I said people who look like me -- I meant the people  |
    | 637758_21:20-21-22     | meant the people who do n't look strong       |                      | who do n't look strong or necessarily smart , or like they   |
    |                        |                                               |                      | 're in control etc.                                          |
    +------------------------+-----------------------------------------------+----------------------+--------------------------------------------------------------+



```python
some_neg_ex = pmir.loc[pmir.after_neg, ['preceding_text', 'bigram_lower', 'token_str']].sample(6)
show_sample(some_neg_ex.assign(
    preceding_text=embolden(some_neg_ex.preceding_text, 
                            f' ({REGNOT}|nobody|nothing|never|none|no) ')
    ), format='pipe')
```

| hit_id                                    | preceding_text                                                                                                                                   | bigram_lower       | token_str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pcc_eng_13_095.7120_x1530725_085:17-19-20 | I promise you , the followers of the dark were __`never`__ stronger , more numerous , or                                                         | openly_influential | I promise you , the followers of the dark were never stronger , more numerous , or more openly influential than in the early decades of the 20th century .                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| pcc_eng_28_001.2565_x0004261_3:10-11-12   | " I do n't think there 's ever been                                                                                                              | so_qualified       | " I do n't think there 's ever been someone so qualified to hold this office . "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| pcc_eng_14_016.3271_x0247591_48:28-30-31  | I owe my salvation to __`nothing`__ more than a sudden change of heart on the part of the pack which , having spotted an even more detestable or | more_edible        | I owe my salvation to nothing more than a sudden change of heart on the part of the pack which , having spotted an even more detestable or apparently more edible figure on the sidewalk on Teatinos , left off attacking me and threw themselves upon him with even greater fury , so that the unfortunate man was forced to fight them off like the hapless prey he was , signalling his distress with much waving of arms and loud cries , attracting no more assistance on my part than he himself had demonstrated just a few moments before , with myself in the role of the helpless victim . |
| pcc_eng_15_056.4401_x0896152_040:08-12-13 | If you ca n't take it anymore or you 're                                                                                                         | not_able           | If you ca n't take it anymore or you 're simply not able to physically , hire a landscaper or a contractor .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| pcc_eng_24_028.3067_x0441558_23:11-12-13  | You open it if it does n't seem too big                                                                                                          | too_overwhelming   | You open it if it does n't seem too big or too overwhelming .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| nyt_eng_20010925_0328_126:05-11-12        | you may not need all of the flour-butter mixture                                                                                                 | only_enough        | you may not need all of the flour-butter mixture ; only enough to thickened the broth slightly .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |



```python
print(f'* ${pmir.after_neg.value_counts()[False]:,}$ tokens in `POSmirror` hits not preceded by negation')
print('  > - I.e. what would remain if _all_ potential contaminants were excluded')
print(f'  > - _{pmir.after_neg.value_counts()[True]:,}_ potential exclusions')
print(f'* ${len(nmir):,}$ tokens in `NEGmirror` hits')
print(f'* Remaining Sample Size Discrepancy: ${pmir.after_neg.value_counts()[False] - len(nmir):,}$')
```

    * $1,490,579$ tokens in `POSmirror` hits not preceded by negation
      > - I.e. what would remain if _all_ potential contaminants were excluded
      > - _247,458_ potential exclusions
    * $293,947$ tokens in `NEGmirror` hits
    * Remaining Sample Size Discrepancy: $1,196,632$


## Effect of Negation Removals



### For 868+ frequency filtered ad* forms 
  
_Without considering any upper case_
* ~~__1,457,913__ tokens in `POSmirror` hits not preceded by negation~~
    * ~~I.e. what would remain if _all_ potential contaminants were excluded~~
    * ~~_217,588_ potential exclusions~~
---
_Without considering fully upper case triggers_
* ~~__1,460,126__ tokens in `POSmirror` hits not preceded by negation~~
* ~~I.e. what would remain if _all_ potential contaminants were excluded~~
* ~~_215,375_ potential exclusions~~
---
_Normalized for case first, but not catching negation at very end of preceding text (no whitespace following)_
* ~~**1,459,568** tokens in `POSmirror` hits not preceded by negation~~
> - ~~I.e. what would remain if _all_ potential contaminants were excluded~~
> - ~~_215,933_ potential exclusions~~
* ~~Updated difference in hit subtotals: **1,174,133**~~
* $285,435$ tokens in `NEGmirror` hits
---
**_Fixed to catch even `preceding_text` final negative triggers_**
* ~~**1,455,547** tokens in `POSmirror` hits not preceded by negation~~
> - ~~I.e. what would remain if _all_ potential contaminants were excluded~~
> - ~~_219,954_ potential exclusions~~
* $285,435$ tokens in `NEGmirror` hits
* ~~Remaining Sample Size Discrepancy: **1,170,112**~~
---
**Strengthened even furthre to catch negative adverbs and "without" and triggers at the _beginning_ of the `preceding_text`**
* $1,434,420$ tokens in `POSmirror` hits not preceded by negation
> - I.e. what would remain if _all_ potential contaminants were excluded
> - _241,081_ potential exclusions
* $285,435$ tokens in `NEGmirror` hits
* Remaining Sample Size Discrepancy: $1,148,985$


### For 7+ frequency filtered ad\* forms

_Without orthography adjustments_
* ~~**1,487,458** tokens in `POSmirror` hits not preceded by negation~~
    > - ~~I.e. what would remain if _all_ potential contaminants were excluded~~
    > - ~~_250,661_ potential exclusions~~
* ~~**293,964** tokens in `NEGmirror` hits~~
* ~~Remaining Sample Size Discrepancy: **1,193,494**~~

_**With** orthography adjustments/filtering_
* $1,490,579$ tokens in `POSmirror` hits not preceded by negation
  > - I.e. what would remain if _all_ potential contaminants were excluded
  > - _247,458_ potential exclusions
* $293,947$ tokens in `NEGmirror` hits
* Remaining Sample Size Discrepancy: $1,196,632$





```python
enforced_pos= pmir.loc[~pmir.after_neg, :'preceding_text']
enforced_pos.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 1490579 entries, apw_eng_19941111_0004_1:14-15-16 to pcc_eng_26_108.10246_x1747457_06:6-8-9
    Data columns (total 22 columns):
     #   Column           Non-Null Count    Dtype   
    ---  ------           --------------    -----   
     0   bigram_id        1490579 non-null  category
     1   token_str        1490579 non-null  string  
     2   pattern          1490579 non-null  category
     3   category         1490579 non-null  category
     4   adv_form         1490579 non-null  category
     5   adj_form         1490579 non-null  category
     6   text_window      1490579 non-null  string  
     7   mir_deprel       1490579 non-null  category
     8   mir_lemma        1490579 non-null  category
     9   adv_lemma        1490579 non-null  category
     10  adj_lemma        1490579 non-null  category
     11  mir_form         1490579 non-null  category
     12  mir_index        1490579 non-null  UInt16  
     13  adv_index        1490579 non-null  UInt16  
     14  adj_index        1490579 non-null  UInt16  
     15  mir_form_lower   1490579 non-null  category
     16  adv_form_lower   1490579 non-null  category
     17  adj_form_lower   1490579 non-null  category
     18  bigram_lower     1490579 non-null  category
     19  all_forms_lower  1490579 non-null  category
     20  prev_form_lower  1490579 non-null  category
     21  preceding_text   1490579 non-null  string  
    dtypes: UInt16(3), category(16), string(3)
    memory usage: 1.1 GB



```python
adv = 'exactly'
new_exactly_ex = sample_pickle(
    data=enforced_pos,
    print_sample=False, sample_size=10,
    columns=['all_forms_lower', 'token_str'],
    filters=[f'adv_form_lower=={adv}'],
)

show_sample(new_exactly_ex.assign(token_str=embolden(new_exactly_ex.token_str, r' (exactly) ')))
```

    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `adv_form_lower==exactly`
    
    ### 10 random rows matching filter(s) from `input frame`
    
    +------------------------+----------------------------+--------------------------------------------------------------+
    | hit_id                 | all_forms_lower            | token_str                                                    |
    +========================+============================+==============================================================+
    | pcc_eng_04_104.1453_x1 | something_exactly_opposite | misrepresentation is the kind of thing you and Goerzen do    |
    | 666254_08:20-21-22     |                            | where you outright lie and say that somebody said something  |
    |                        |                            | __`exactly`__ opposite to what they actually said . >        |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_07_101.4447_x1 | all_exactly_alike          | The Man Whose Teeth Were All Exactly Alike                   |
    | 623411_110:6-7-8       |                            |                                                              |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_12_044.6593_x0 | or_exactly_enough          | The cabbage that accompanied a Muscovy duck breast was       |
    | 705786_21:19-20-21     |                            | braised with too much cinnamon , some thought , or           |
    |                        |                            | __`exactly`__ enough , thought others .                      |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_12_098.6128_x1 | or_exactly_alike           | 3 . sameness : the fact or condition of being the same or    |
    | 577474_138:13-14-15    |                            | __`exactly`__ alike                                          |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_14_021.3253_x0 | many_exactly_alike         | We will advance all reasonable errors , spelling mistakes ,  |
    | 328325_67:43-47-48     |                            | run-on facilities , receive your personal , we will send you |
    |                        |                            | a good link where you can say clip awkward sentences and     |
    |                        |                            | omit any unfamiliar words , phrases , per day , many of      |
    |                        |                            | which nigeria __`exactly`__ alike .                          |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_19_078.5861_x1 | all_exactly_opposite       | All are __`exactly`__ opposite of the best strategies for    |
    | 253458_06:1-3-4        |                            | learning .                                                   |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_20_063.3872_x1 | all_exactly_alike          | " Communism , the New Deal , Fascism , Nazism , " he wrote   |
    | 007929_21:37-38-39     |                            | in his Memoirs , " are merely so-many trade-names for        |
    |                        |                            | collectivist Statism , like the trade-names for tooth -      |
    |                        |                            | pastes which are all __`exactly`__ alike except for the      |
    |                        |                            | flavouring . " ...                                           |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_22_049.7992_x0 | all_exactly_right          | If you 're an online supplier and you want to win a customer |
    | 788588_32:29-30-31     |                            | 's repeat business , you need to make sure prices , products |
    |                        |                            | and service are all __`exactly`__ right .                    |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_25_078.3454_x1 | or_exactly_music-related   | This may be tangentially music-related or __`exactly`__      |
    | 252325_2:6-7-8         |                            | music-related , depending on where you 're sitting :         |
    +------------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_25_097.4853_x1 | everything_exactly_perfect | And , it 's time - aware enough ( by stating " every day " ) |
    | 561507_25:34-37-38     |                            | that your mind can accept and acknowledge linear progress    |
    |                        |                            | while your internal vibration reorients to trust that        |
    |                        |                            | everything IS already __`exactly`__ perfect in this moment , |
    |                        |                            | even if it feels like it 's not - because , again , change   |
    |                        |                            | takes time , and lasting change does n't always appear in    |
    |                        |                            | the external world right away .                              |
    +------------------------+----------------------------+--------------------------------------------------------------+



```python
for pat_suff in ['R', 'L']:
    new_exactly_ex = sample_pickle(
        data=enforced_pos, sample_size=8,
        print_sample=False, sort_by='adj_form_lower',
        columns=['all_forms_lower', 'text_window', 'token_str'],
        filters=[f'adv_form_lower=={adv}', 
                f'pattern==pos-mirror-{pat_suff}'],
    )

    show_sample(new_exactly_ex.assign(
        text_window=embolden(new_exactly_ex.text_window, f' ({adv}) '),
        token_str=embolden(new_exactly_ex.token_str, f' ({adv}) ')
    ), format='pipe')
```

    
- *filtering rows...*
  - regex parsing = False
  - ✓ Applied filter: `adv_form_lower==exactly`
  - ✓ Applied filter: `pattern==pos-mirror-R`

### 8 random rows matching filter(s) from `input frame`

| hit_id                                    | all_forms_lower          | text_window                                                                 | token_str                                                                                                                                                                         |
|:------------------------------------------|:-------------------------|:----------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pcc_eng_03_074.5040_x1190619_26:1-6-7     | or_exactly_correct       | Or maybe the result wasnt __`exactly`__ correct because he was n't          | Or maybe the result wasnt __`exactly`__ correct because he was n't where he thought he was .                                                                                      |
| pcc_eng_14_008.0840_x0114338_03:08-09-10  | or_exactly_false         | is either __`exactly`__ true or __`exactly`__ false is called a statement   | A sentence which is either __`exactly`__ true or __`exactly`__ false is called a statement .                                                                                      |
| pcc_eng_13_079.2956_x1265427_12:10-12-13  | or_exactly_funny         | suposed to be fun or more __`exactly`__ funny .                             | This is MLS it is suposed to be fun or more __`exactly`__ funny .                                                                                                                 |
| pcc_eng_14_047.8465_x0756834_55:4-5-6     | both_exactly_right       | Representative Murphy is both __`exactly`__ right and spectacularly wrong . | Representative Murphy is both __`exactly`__ right and spectacularly wrong .                                                                                                       |
| pcc_eng_22_073.0874_x1165093_82:13-15-16  | everything_exactly_right | to make sure that everything is __`exactly`__ right , especially with our   | He works closely with our nurses and doctors to make sure that everything is __`exactly`__ right , especially with our children .                                                 |
| pcc_eng_23_094.7577_x1515449_43:32-33-34  | all_exactly_right        | vigilante killer " are all __`exactly`__ right .                            | The emphasis on " unlawful use of violence , " the evocation of " vigilantism , " and the description of Tiller 's killer as a " vigilante killer " are all __`exactly`__ right . |
| pcc_eng_03_019.3127_x0296060_12:12-13-14  | always_exactly_right     | - THE CHURCH IS ALWAYS EXACTLY RIGHT .                                      | Let people get it through their heads - THE CHURCH IS ALWAYS EXACTLY RIGHT .                                                                                                      |
| pcc_eng_20_092.6565_x1480742_101:24-25-26 | all_exactly_same         | are messaging it are all __`exactly`__ same as their last time              | The product mix they chose and the level of price increase , the markets they chose and how they are messaging it are all __`exactly`__ same as their last time .                 |

- *filtering rows...*
  - regex parsing = False
  - ✓ Applied filter: `adv_form_lower==exactly`
  - ✓ Applied filter: `pattern==pos-mirror-L`

### 8 random rows matching filter(s) from `input frame`

| hit_id                                    | all_forms_lower            | text_window                                                                   | token_str                                                                                                                                                                   |
|:------------------------------------------|:---------------------------|:------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| apw_eng_20070219_0931_10:22-24-25         | something_exactly_alien    | of the dictum -- something not __`exactly`__ alien to him .                   | Bellamy , who has a history of losing his temper , looks to be the first casualty of the dictum -- something not __`exactly`__ alien to him .                               |
| pcc_eng_02_048.1298_x0762484_04:1-2-3     | everybody_exactly_alike    | Everybody __`exactly`__ alike . "                                             | Everybody __`exactly`__ alike . "                                                                                                                                           |
| pcc_eng_05_069.4747_x1107978_086:1-2-3    | everybody_exactly_alike    | Everybody __`exactly`__ alike . "                                             | Everybody __`exactly`__ alike . "                                                                                                                                           |
| pcc_eng_06_038.9890_x0614425_107:3-6-7    | all_exactly_alike          | They are all of them __`exactly`__ alike , and there is                       | They are all of them __`exactly`__ alike , and there is not one of them can be eaten .                                                                                      |
| pcc_eng_04_104.1453_x1666254_08:20-21-22  | something_exactly_opposite | say that somebody said something __`exactly`__ opposite to what they actually | misrepresentation is the kind of thing you and Goerzen do where you outright lie and say that somebody said something __`exactly`__ opposite to what they actually said . > |
| pcc_eng_15_106.5980_x1707092_015:16-17-18 | something_exactly_related  | , you offered them something __`exactly`__ related to the post they           | What if , instead of pointing visitors to a semi-related resource , you offered them something __`exactly`__ related to the post they just read ?                           |
| pcc_eng_08_106.0266_x1700594_12:1-2-3     | everything_exactly_same    | Everything __`exactly`__ same , minimum 290 people                            | Everything __`exactly`__ same , minimum 290 people dead .                                                                                                                   |
| pcc_eng_11_064.7133_x1031125_24:1-2-3     | everything_exactly_same    | Everything __`exactly`__ same , minimum two hundred                           | Everything __`exactly`__ same , minimum two hundred ninety people dead .                                                                                                    |


## Remove Duplicated `text_window`+`all_forms_lower`


```python
enforced_pos['utt_len']= pd.to_numeric(enforced_pos.token_str.apply(lambda x: int(len(x.split()))), downcast='integer')
```


```python
dups_token_str = enforced_pos.loc[enforced_pos.duplicated(subset=['token_str', 'all_forms_lower']), ['all_forms_lower', 'token_str','text_window', 'utt_len']]
dups_text_window = enforced_pos.loc[enforced_pos.duplicated(subset=['text_window', 'all_forms_lower']), ['all_forms_lower', 'token_str', 'text_window','utt_len']]
dups_both = enforced_pos.loc[enforced_pos.duplicated(subset=['text_window', 'token_str', 'all_forms_lower']), ['all_forms_lower', 'token_str','text_window', 'utt_len']]
# show_sample(dups.loc[dups.utt_len>=80, :].sort_values(['utt_len', 'token_str']).head(6))
print_iter([f'token_str:   {len(dups_token_str):,}', 
            f'text_window: {len(dups_text_window):,}',
            f'both:        {len(dups_both):,}'], header='Potental Removals (no `utt_len` filter applied)')
```

    
Potental Removals (no `utt_len` filter applied)
- `token_str`:   15,394
- `text_window`: 36,885
- both:          14,861



```python
print(f'`text_window` duplicates when restricted to 20+ tokens in `token_str`: {len(dups_text_window.loc[dups_text_window.utt_len>=20, :]):,}')
```

    `text_window` duplicates when restricted to 20+ tokens in `token_str`: 16,570


These duplicates are retained since it's too messy to separate the clearly carbon copy utterances from plausible genuine production. 

Highly Suspicious

|     | text_window                                               | \#tokens in sentence | \#duplications |
|----:|:----------------------------------------------------------|---------------------:|---------------:|
|   7 | _Everything you see here is absolutely FREE to watch ._   |                   10 |             60 |
|  17 | _All of Swedenborg 's works are well worth reading ._     |                   10 |             43 |
|  60 | _2 fig Something quintessentially Canadian ._             |                    6 |             20 |
|  65 | _Everybody is Super Heady in our sandbox ._               |                    8 |             19 |
| 119 | _Because sometimes , 140 characters just is n't enough ._ |                   10 |             13 |
| 143 | _" Or maybe stupid , " Ebenezar countered_                |                    9 |             11 |
| 188 | _Because Sometimes 140 Characters Just Is n't Enough_     |                    8 |              9 |
| 283 | _There 's something very wrong with our pterosaurs ._     |                    9 |              7 |
| 290 | _The plaid decoration is all very good ._                 |                    8 |              7 |
| 482 | _wrap up something as special as she is [...]_            |                    9 |              5 |

Plausible Production

|    | text_window                                    | \#tokens in sentence | \#duplications |
|---:|:-----------------------------------------------|---------------------:|---------------:|
|  2 | _Something was n't right ._                    |                    5 |            118 |
|  3 | _But I 'm sure everything will be just fine ._ |                   10 |            102 |
|  8 | _It 's all very confusing ._                   |                    6 |             56 |
|  6 | _We should all be so lucky ._                  |                    7 |             69 |
| 10 | _It 's all very exciting ._                    |                    6 |             54 |
| 19 | _Something is definitely wrong ._              |                    5 |             41 |
| 20 | _Looking for something more specific ?_        |                    6 |             40 |
| 25 | _Both are equally important ._                 |                    5 |             33 |
| 31 | _My cup is always half full ._                 |                    7 |             30 |
| 39 | _If only it were all so simple !_              |                    9 |             24 |
| 48 | _Everything is not awesome ._                  |                    5 |             23 |


```python
dups_text_window.loc[(dups_text_window.utt_len < 20), :].value_counts(['text_window', 'utt_len']).to_frame().reset_index().sort_values(['count','text_window', ], ascending=False)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>text_window</th>
      <th>utt_len</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Some of your changes are now live .</td>
      <td>8</td>
      <td>384</td>
    </tr>
    <tr>
      <th>1</th>
      <td>And now for something completely different .</td>
      <td>7</td>
      <td>122</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Something was n't right .</td>
      <td>5</td>
      <td>118</td>
    </tr>
    <tr>
      <th>3</th>
      <td>But I 'm sure everything will be just fine .</td>
      <td>10</td>
      <td>102</td>
    </tr>
    <tr>
      <th>4</th>
      <td>And now for something completely different ...</td>
      <td>7</td>
      <td>75</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>7968</th>
      <td>" And now for something completely different . "</td>
      <td>17</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7965</th>
      <td>" All of us at Whataburger are so happy to get...</td>
      <td>16</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7964</th>
      <td>" All along I have been completely consistent ...</td>
      <td>18</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8972</th>
      <td>" Abusers are often very adept at identifying ...</td>
      <td>10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3034</th>
      <td>" ... something truly special . "</td>
      <td>7</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>11125 rows × 3 columns</p>
</div>




```python
def weed_windows(df):
    return pd.concat(
        [df.loc[df.utt_len < 20, :],
         df.loc[df.utt_len >= 20, :].drop_duplicates(
            subset=['text_window', 'all_forms_lower'])]
    )
```


```python
enforced_pos.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 1490579 entries, apw_eng_19941111_0004_1:14-15-16 to pcc_eng_26_108.10246_x1747457_06:6-8-9
    Data columns (total 23 columns):
     #   Column           Non-Null Count    Dtype   
    ---  ------           --------------    -----   
     0   bigram_id        1490579 non-null  category
     1   token_str        1490579 non-null  string  
     2   pattern          1490579 non-null  category
     3   category         1490579 non-null  category
     4   adv_form         1490579 non-null  category
     5   adj_form         1490579 non-null  category
     6   text_window      1490579 non-null  string  
     7   mir_deprel       1490579 non-null  category
     8   mir_lemma        1490579 non-null  category
     9   adv_lemma        1490579 non-null  category
     10  adj_lemma        1490579 non-null  category
     11  mir_form         1490579 non-null  category
     12  mir_index        1490579 non-null  UInt16  
     13  adv_index        1490579 non-null  UInt16  
     14  adj_index        1490579 non-null  UInt16  
     15  mir_form_lower   1490579 non-null  category
     16  adv_form_lower   1490579 non-null  category
     17  adj_form_lower   1490579 non-null  category
     18  bigram_lower     1490579 non-null  category
     19  all_forms_lower  1490579 non-null  category
     20  prev_form_lower  1490579 non-null  category
     21  preceding_text   1490579 non-null  string  
     22  utt_len          1490579 non-null  int16   
    dtypes: UInt16(3), category(16), int16(1), string(3)
    memory usage: 1.1 GB



```python
new_pmir = weed_windows(enforced_pos)
print(f'{len(new_pmir):,} hits remaining in `POSmirror` set after additional filtering', 
      f'({len(enforced_pos) - len(new_pmir):,} hits removed as duplicates.)', 
      sep='\n')
# show_sample(new_pmir.sample(6)[['all_forms_lower', 'text_window']])
```

- $1,475,109$ hits remaining in `POSmirror` set after additional filtering
- (15,470 hits removed as duplicates.)



```python
new_pmir.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 1475109 entries, apw_eng_19941111_0090_14:09-12-13 to pcc_eng_26_108.10246_x1747457_06:6-8-9
    Data columns (total 23 columns):
     #   Column           Non-Null Count    Dtype   
    ---  ------           --------------    -----   
     0   bigram_id        1475109 non-null  category
     1   token_str        1475109 non-null  string  
     2   pattern          1475109 non-null  category
     3   category         1475109 non-null  category
     4   adv_form         1475109 non-null  category
     5   adj_form         1475109 non-null  category
     6   text_window      1475109 non-null  string  
     7   mir_deprel       1475109 non-null  category
     8   mir_lemma        1475109 non-null  category
     9   adv_lemma        1475109 non-null  category
     10  adj_lemma        1475109 non-null  category
     11  mir_form         1475109 non-null  category
     12  mir_index        1475109 non-null  UInt16  
     13  adv_index        1475109 non-null  UInt16  
     14  adj_index        1475109 non-null  UInt16  
     15  mir_form_lower   1475109 non-null  category
     16  adv_form_lower   1475109 non-null  category
     17  adj_form_lower   1475109 non-null  category
     18  bigram_lower     1475109 non-null  category
     19  all_forms_lower  1475109 non-null  category
     20  prev_form_lower  1475109 non-null  category
     21  preceding_text   1475109 non-null  string  
     22  utt_len          1475109 non-null  int16   
    dtypes: UInt16(3), category(16), int16(1), string(3)
    memory usage: 1.1 GB


### Add `trigger_lower` column to `POSmirror` table


```python
new_pmir = new_pmir.loc[:, :'all_forms_lower']
new_pmir['trigger_lower'] = new_pmir['mir_form_lower'].astype('category')
new_pmir.columns
```




    Index(['bigram_id', 'token_str', 'pattern', 'category', 'adv_form', 'adj_form',
           'text_window', 'mir_deprel', 'mir_lemma', 'adv_lemma', 'adj_lemma',
           'mir_form', 'mir_index', 'adv_index', 'adj_index', 'mir_form_lower',
           'adv_form_lower', 'adj_form_lower', 'bigram_lower', 'all_forms_lower',
           'trigger_lower'],
          dtype='object')




```python
new_path = path_dict['POSmirror'].with_name('LimitedPOS-'+path_dict['POSmirror'].name)

if not new_path.is_file():
    
    new_pmir.loc[:, ].to_pickle(new_path)
    print(f'Updated `POSmirror` hits dataframe saved as:\ \n  `{new_path}`')
else: 
    print(f'Updated `POSmirror` hits dataframe already exists:\ \n  `{new_path}`')
    print('\n```shell')
    !ls -ho {new_path}
    print('```')
    
```

Updated `POSmirror` hits dataframe saved as:\ 
  `/share/compling/data/sanpi/4_post-processed/POSmirror/LimitedPOS-trigger-bigrams_frq-thrMIN-7.35f.pkl.gz`


## Remove Duplication from `NEGmirror` as well


```python
nmir.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 293947 entries, pcc_eng_11_001.0326_x0000513_088:14-15-16 to pcc_eng_10_108.10108_x1747378_18:7-8-9
    Data columns (total 21 columns):
     #   Column           Non-Null Count   Dtype   
    ---  ------           --------------   -----   
     0   bigram_id        293947 non-null  category
     1   token_str        293947 non-null  string  
     2   pattern          293947 non-null  category
     3   category         293947 non-null  category
     4   neg_form         293947 non-null  category
     5   adv_form         293947 non-null  category
     6   adj_form         293947 non-null  category
     7   text_window      293947 non-null  string  
     8   neg_deprel       293947 non-null  category
     9   neg_lemma        293947 non-null  category
     10  adv_lemma        293947 non-null  category
     11  adj_lemma        293947 non-null  category
     12  neg_index        293947 non-null  UInt16  
     13  adv_index        293947 non-null  UInt16  
     14  adj_index        293947 non-null  UInt16  
     15  neg_form_lower   293947 non-null  category
     16  adv_form_lower   293947 non-null  category
     17  adj_form_lower   293947 non-null  category
     18  bigram_lower     293947 non-null  category
     19  all_forms_lower  293947 non-null  category
     20  prev_form_lower  293947 non-null  category
    dtypes: UInt16(3), category(16), string(2)
    memory usage: 169.5 MB



```python
nmir['utt_len']= nmir.token_str.apply(lambda x: len(x.split()))
new_nmir = weed_windows(nmir)
new_nmir = new_nmir.loc[:, :'all_forms_lower']
new_nmir['trigger_lower'] = new_nmir.neg_form_lower.astype('category')
show_sample(new_nmir.sample(4)[['trigger_lower', 'all_forms_lower', 'text_window']])
```

    +------------------------+-----------------+-------------------------------+-----------------------------------------------+
    | hit_id                 | trigger_lower   | all_forms_lower               | text_window                                   |
    +========================+=================+===============================+===============================================+
    | pcc_eng_15_002.5425_x0 | never           | never_entirely_separate       | the two worlds can never be entirely separate |
    | 024650_37:6-8-9        |                 |                               | , the overlap in                              |
    +------------------------+-----------------+-------------------------------+-----------------------------------------------+
    | pcc_eng_10_038.8129_x0 | nor             | nor_epistemically_transparent | constrained in its options nor epistemically  |
    | 611668_40:13-14-15     |                 |                               | transparent , as the examples                 |
    +------------------------+-----------------+-------------------------------+-----------------------------------------------+
    | pcc_eng_07_023.7148_x0 | never           | never_so_cold                 | bitterly that they had never been so cold . [ |
    | 367258_118:33-35-36    |                 |                               | 1 ]                                           |
    +------------------------+-----------------+-------------------------------+-----------------------------------------------+
    | nyt_eng_19990830_0387_ | no              | no_more_accurate              | garbage '' and `` no more accurate than       |
    | 4:42-43-44             |                 |                               | information from Web                          |
    +------------------------+-----------------+-------------------------------+-----------------------------------------------+



```python
print(f'\n* {len(nmir):,} original hits in `NEGmirror` (`{path_dict["NEGmirror"].relative_to(POST_PROC_DIR)}`)')
print(f'* {len(new_nmir):,} hits remaining in `NEGmirror` set after additional filtering of duplicate hits')
print(f'  ({len(nmir) - len(new_nmir):,} hits removed as duplicates.)', 
      sep='\n')
```

    
* 293,947 original hits in `NEGmirror` (`NEGmirror/trigger-bigrams_frq-thrMIN-7.35f.pkl.gz`)
* 289,759 hits remaining in `NEGmirror` set after additional filtering of duplicate hits
  (4,188 hits removed as duplicates.)



```python
new_path = path_dict['NEGmirror'].with_name('LimitedNEG-'+path_dict['NEGmirror'].name)
if not new_path.is_file():
    
    new_nmir.to_pickle(new_path)
    print(f'Updated `NEGmirror` hits dataframe saved as:\ \n  `{new_path}`')
else: 
    print(f'Updated `NEGmirror` hits dataframe already exists:\ \n  `{new_path}`')
    print('\n```shell')
    !ls -ho {new_path}
    print('```')
```

Updated `NEGmirror` hits dataframe saved as:\ 
  `/share/compling/data/sanpi/4_post-processed/NEGmirror/LimitedNEG-trigger-bigrams_frq-thrMIN-7.35f.pkl.gz`


## After Removing Additional Duplication

* ~~1,472,077~~ $1,475,109$ hits remaining in `POSmirror` set after additional filtering\
  (~~15,381~~ **15,470** hits removed as duplicates.)

* $289,759$ hits remaining in `NEGmirror` set after additional filtering of duplicate hits\
  (4,188 hits removed as duplicates.)

