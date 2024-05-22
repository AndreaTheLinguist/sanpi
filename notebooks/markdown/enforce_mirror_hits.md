```python
import re
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, print_iter
from source.utils.sample import sample_pickle

HIT_EX_COLS = ['WITH::^.[il].*lower', 'WITH::text', 'token_str']

pkl_name = 'trigger-bigrams_thr0-001p.35f.pkl.gz'
path_dict = {p: POST_PROC_DIR / p / pkl_name for  p in ('POSmirror','NEGmirror')}
path_dict
```




    {'POSmirror': PosixPath('/share/compling/data/sanpi/4_post-processed/POSmirror/trigger-bigrams_thr0-001p.35f.pkl.gz'),
     'NEGmirror': PosixPath('/share/compling/data/sanpi/4_post-processed/NEGmirror/trigger-bigrams_thr0-001p.35f.pkl.gz')}




```python
nmir = pd.read_pickle(path_dict['NEGmirror'])
```


```python
pmir = pd.read_pickle(path_dict['POSmirror'])

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
    ▸ adv_form
    ▸ adj_form
    ▸ text_window
    ▸ bigram_id
    ▸ token_str
    ▸ mir_deprel
    ▸ mir_head
    ▸ mir_lemma
    ▸ adv_lemma
    ▸ adj_lemma
    ▸ mir_form
    ▸ mir_form_lower
    ▸ adv_form_lower
    ▸ adj_form_lower
    ▸ bigram_lower
    ▸ all_forms_lower
    ▸ pattern
    ▸ category
    ▸ prev_form_lower
    
    NEGmirror columns:
    ▸ neg_form
    ▸ adv_form
    ▸ adj_form
    ▸ text_window
    ▸ bigram_id
    ▸ token_str
    ▸ neg_deprel
    ▸ neg_head
    ▸ neg_lemma
    ▸ adv_lemma
    ▸ adj_lemma
    ▸ neg_form_lower
    ▸ adv_form_lower
    ▸ adj_form_lower
    ▸ bigram_lower
    ▸ all_forms_lower
    ▸ pattern
    ▸ category
    ▸ prev_form_lower



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
    | pos-mirror-R | 1,313,154 |
    | pos-mirror-L |   362,347 |



```python
show_sample(nmir.pattern.value_counts().to_frame(), limit_cols=False, format='pipe')
```

    | pattern      |   count |
    |:-------------|--------:|
    | neg-mirror-R | 210,404 |
    | neg-mirror-L |  75,031 |



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
      - ✓ Applied filter: `token_str== n[o']t .* exactly `
      - ✓ Applied filter: `adv_form_lower==^exactly$`
      - ✓ Applied filter: `pattern==.*L$`
    
    ### All (5) row(s) matching filter(s) from `input frame`
    
    | hit_id                                    | mir_form_lower   | bigram_lower     | text_window                                                  | token_str                                                                                                                                                                                                                                                                                                                                                                                            |
    |:------------------------------------------|:-----------------|:-----------------|:-------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_25_005.3062_x0070160_19:11-12-13  | many             | exactly_alike    | , there are __`not`__ many __`exactly`__ alike .             | Because the traps were all handmade , there are __`not`__ many __`exactly`__ alike .                                                                                                                                                                                                                                                                                                                 |
    | pcc_eng_03_092.8566_x1487301_15:21-22-23  | something        | exactly_friendly | n't think it was something __`exactly`__ friendly for kids . | The i Pad is a fairly simple device to use for adults , but I did __`n't`__ think it was something __`exactly`__ friendly for kids .                                                                                                                                                                                                                                                                 |
    | pcc_eng_29_085.1202_x1358647_07:4-5-6     | something        | exactly_new      | This is __`n't`__ something __`exactly`__ new .              | This is __`n't`__ something __`exactly`__ new .                                                                                                                                                                                                                                                                                                                                                      |
    | pcc_eng_21_004.3936_x0054774_071:62-63-64 | something        | exactly_new      | so it 's __`not`__ something __`exactly`__ new with him ] )  | It 's also missing some of his earlier stuff , but the " KMD " ( Kurious and another random dude Doom was supposedly gonna make a new KMD album with [ another of the many rumored - but- never- seen Doom projects a la Madvillainy 2 & the Ghost collab - this was from like 2000 so it 's __`not`__ something __`exactly`__ new with him ] ) track Sorcerors is on there , which is really nice . |
    | pcc_eng_08_092.9577_x1488616_29:17-18-19  | something        | exactly_right    | I did __`n't`__ have something __`exactly`__ right .         | " [ My clients ] needed a piece of art , and I did __`n't`__ have something __`exactly`__ right .                                                                                                                                                                                                                                                                                                    |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* exactly `
      - ✓ Applied filter: `adv_form_lower==^exactly$`
      - ✓ Applied filter: `pattern==.*R$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                    | mir_form_lower   | bigram_lower      | text_window                                                                           | token_str                                                                                                                                                                                                                                                                                                                    |
    |:------------------------------------------|:-----------------|:------------------|:--------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_24_028.3166_x0441708_039:20-23-24 | everyone         | exactly_equal     | better " rights unless everyone is also __`exactly`__ equal in all other respects     | It 's simply __`not`__ , in general , true that no one will have " better " rights unless everyone is also __`exactly`__ equal in all other respects .                                                                                                                                                                       |
    | pcc_eng_22_031.0840_x0485714_249:19-24-25 | everything       | exactly_friendly  | he knows that __`not`__ everything in Cool World is __`exactly`__ friendly . " in top | Intrigued at seeing his creating come to life , Jack is nonetheless wary as he knows that __`not`__ everything in Cool World is __`exactly`__ friendly . " in top quality .                                                                                                                                                  |
    | pcc_eng_29_068.6475_x1092799_11:21-22-23  | or               | exactly_immutable | life is necessarily true or __`exactly`__ immutable .                                 | It 's the realization that we can sense that __`not`__ everything we have been taught in life is necessarily true or __`exactly`__ immutable .                                                                                                                                                                               |
    | pcc_eng_02_050.0522_x0793598_106:10-11-12 | or               | exactly_perfect   | does __`n't`__ go well or __`exactly`__ perfect , or when something                   | He 's grown when it does __`n't`__ go well or __`exactly`__ perfect , or when something does __`n't`__ happen our way .                                                                                                                                                                                                      |
    | pcc_eng_22_098.4705_x1575203_17:14-16-17  | or               | exactly_sure      | call it honor , or been __`exactly`__ sure of how to describe                         | But , although I might __`not`__ have known to call it honor , or been __`exactly`__ sure of how to describe the gender , race , and class politics that inflect it , I had a sneaking suspicion that something more than my socioeconomic background or my gender stood in the way of my ever being like Dally or Ponyboy . |
    | pcc_eng_01_019.2732_x0295388_118:01-11-12 | some             | exactly_right     | Some of those calls that did __`n't`__ get called were __`exactly`__ right .          | Some of those calls that did __`n't`__ get called were __`exactly`__ right .                                                                                                                                                                                                                                                 |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* ever `
      - ✓ Applied filter: `adv_form_lower==^ever$`
      - ✓ Applied filter: `pattern==.*L$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                   | mir_form_lower   | bigram_lower     | text_window                                                                        | token_str                                                                                                                                                                                                                                                                                                                                                                                      |
    |:-----------------------------------------|:-----------------|:-----------------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_11_083.0903_x1328650_1:25-26-27  | everyone         | ever_involved    | admittedly __`not`__ familiar with everyone __`ever`__ involved with the Wo W      | There are other items in the patch files that look to be named after certain individuals , but I 'm admittedly __`not`__ familiar with everyone __`ever`__ involved with the Wo W community , so I 'll leave it to you guys to let me know if I missed someone .                                                                                                                               |
    | pcc_eng_24_012.9287_x0192321_19:37-38-39 | everything       | ever_related     | attempt to do absolutely everything __`ever`__ related to desktop publishing all   | I 'm in that set of people who fondly remember Word 5.1 , and miss the days of having a word processor that was actually a word processor , __`not`__ an overblown attempt to do absolutely everything __`ever`__ related to desktop publishing all at once ( even Apple 's Pages , while far preferable to any post - 5.1 version of Word , is far more than just a simple word processor ) . |
    | nyt_eng_19950818_0506_53:14-17-18        | someone          | ever_likely      | liberals and surely __`not`__ someone who is __`ever`__ likely to be labeled a     | she is one of broadcasting 's last remaining flaming liberals and surely __`not`__ someone who is __`ever`__ likely to be labeled a girly-girl .                                                                                                                                                                                                                                               |
    | apw_eng_20080222_0028_15:35-39-40        | something        | ever_comfortable | but this is __`not`__ something the Times is __`ever`__ comfortable doing , '' New | `` From the looks of it , the paper is going to have to fight for its story -- and its ethics -- in the court of public opinion , but this is __`not`__ something the Times is __`ever`__ comfortable doing , '' New York University journalism professor Jay Rosen said in a posting on The Huffington Post , a widely read online forum .                                                    |
    | pcc_eng_14_006.0533_x0081779_21:11-12-13 | something        | ever_palpable    | taught , it is something __`ever`__ palpable , in classrooms throughout            | While love may __`not`__ be overtly taught , it is something __`ever`__ palpable , in classrooms throughout the world .                                                                                                                                                                                                                                                                        |
    | pcc_eng_10_005.9191_x0079566_10:6-7-8    | something        | ever_related     | anyone hates AARP and something __`ever`__ related to it , then                    | If anyone hates AARP and something __`ever`__ related to it , then it 's good to hear that they wo __`n't`__ ever __`ever`__ e-book an OAT journey , as a result of I would take one once more and I 'd hate to journey with somebody toting a grudge .                                                                                                                                        |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* ever `
      - ✓ Applied filter: `adv_form_lower==^ever$`
      - ✓ Applied filter: `pattern==.*R$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                    | mir_form_lower   | bigram_lower   | text_window                                                              | token_str                                                                                                                                                                                                                                                                                                                                                                                           |
    |:------------------------------------------|:-----------------|:---------------|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_12_100.4534_x1607108_11:58-61-62  | or               | ever_able      | market for your passion or that your __`ever`__ able to build a business | A lot of business advice tells you to find your passion and pursue it with the kind of persistence that is usually reserved for romantic relationships , but the truth of the matter is you can be passionate about a variety of different things but that does __`n't`__ mean that there 's a market for your passion or that your __`ever`__ able to build a business with that passion in mind . |
    | pcc_eng_19_040.0188_x0629578_10:36-38-39  | or               | ever_moral     | continue to be moral or were __`ever`__ moral to begin with .            | But I ca __`n't`__ help but feel that the moral thing for the show to do is to never let the viewer stop asking him or herself if Matt 's actions continue to be moral or were __`ever`__ moral to begin with .                                                                                                                                                                                     |
    | pcc_eng_24_055.5103_x0881451_09:37-40-41  | or               | ever_okay      | certain spurious results , or is it __`ever`__ okay ?                    | " This book is about the gray zones , " she says , " like when is a data point worthy of inclusion or __`not`__ , when is it okay to overlook certain spurious results , or is it __`ever`__ okay ?                                                                                                                                                                                                 |
    | pcc_eng_05_050.0374_x0793434_13:40-42-43  | or               | ever_popular   | headed this way " or the __`ever`__ popular " regardless of whether      | The average Joe is busy driving to work , dealing with a petty boss and figuring out how he is going to pay his mortgage this month __`not`__ worrying on " a very rainy mess headed this way " or the __`ever`__ popular " regardless of whether it gets a name we are in for bad weather " sort of soundbites .                                                                                   |
    | pcc_eng_19_030.3108_x0473160_281:33-35-36 | or               | ever_popular   | fit him ? " or the __`ever`__ popular , " that dress                     | I should limit my comments to things like , " where did he get that tie ?!?! " or , " could __`n't`__ he afford a suit that fit him ? " or the __`ever`__ popular , " that dress is horrible ! "                                                                                                                                                                                                    |
    | pcc_eng_29_030.4867_x0475923_21:21-22-23  | or               | ever_vocal     | communication is __`not`__ guttural or __`ever`__ vocal ?                | Why would an alien have a name full of human vowels , when their mode of communication is __`not`__ guttural or __`ever`__ vocal ?                                                                                                                                                                                                                                                                  |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* necessarily `
      - ✓ Applied filter: `adv_form_lower==^necessarily$`
      - ✓ Applied filter: `pattern==.*L$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                    | mir_form_lower   | bigram_lower             | text_window                                                                         | token_str                                                                                                                                                                                                                                                                                                                                                                     |
    |:------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | nyt_eng_20040429_0030_4:10-13-14          | all              | necessarily_congruent    | of ambitions , __`not`__ all of them __`necessarily`__ congruent with one another . | TriBeCa clearly has a number of ambitions , __`not`__ all of them __`necessarily`__ congruent with one another .                                                                                                                                                                                                                                                              |
    | nyt_eng_20030413_0024_28:14-16-17         | someone          | necessarily_pop          | you 're __`not`__ expecting someone to __`necessarily`__ pop out of a window        | `` I think it could be very dangerous because you 're __`not`__ expecting someone to __`necessarily`__ pop out of a window as a sniper or a suicide bomber . ''                                                                                                                                                                                                               |
    | pcc_eng_22_076.0516_x1212971_110:22-23-24 | something        | necessarily_commendable  | as if that was something __`necessarily`__ commendable .                            | It is interesting how Bloom 's behaviour is being interpreted as " __`not`__ politically correct " , as if that was something __`necessarily`__ commendable .                                                                                                                                                                                                                 |
    | pcc_eng_14_043.6120_x0688460_092:11-12-13 | something        | necessarily_involved     | of being , but something __`necessarily`__ involved in all kinds and                | God is __`not`__ a special kind of being , but something __`necessarily`__ involved in all kinds and conditions of being .                                                                                                                                                                                                                                                    |
    | pcc_eng_23_010.0018_x0145294_374:23-24-25 | something        | necessarily_supernatural | does __`n't`__ relay on something __`necessarily`__ supernatural .                  | BEANYWOOD : That 's one of the things that I appreciated most about the movie , that it does __`n't`__ relay on something __`necessarily`__ supernatural .                                                                                                                                                                                                                    |
    | pcc_eng_17_008.1276_x0115288_17:10-11-12  | something        | necessarily_vivid        | , it is __`not`__ something __`necessarily`__ vivid and precise , but               | It is __`not`__ a fantasy , it is __`not`__ something __`necessarily`__ vivid and precise , but it functions as an anxious driver from within that forces attention and focus , that clamps onto your spinal column when you hear your child crying out in the night , makes you spin your head on a swivel when you hear an anonymous cry in the street ; is that my child ? |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* necessarily `
      - ✓ Applied filter: `adv_form_lower==^necessarily$`
      - ✓ Applied filter: `pattern==.*R$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                   | mir_form_lower   | bigram_lower           | text_window                                                                        | token_str                                                                                                                                                                                                                                                                                             |
    |:-----------------------------------------|:-----------------|:-----------------------|:-----------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_04_094.0512_x1503416_38:6-7-8    | or               | necessarily_accurate   | list is __`not`__ comprehensive or __`necessarily`__ accurate but it 's a          | My list is __`not`__ comprehensive or __`necessarily`__ accurate but it 's a good way to keep tabs on whats going on in the world of nanobrewing .                                                                                                                                                    |
    | pcc_eng_08_002.9893_x0032328_089:6-7-8   | or               | necessarily_fun        | methods are __`not`__ popular or __`necessarily`__ fun to enforce , but            | Those methods are __`not`__ popular or __`necessarily`__ fun to enforce , but very close supervision and the decision to remove the option of social media at this age would be a good start .                                                                                                        |
    | pcc_eng_21_029.5917_x0462226_35:29-30-31 | or               | necessarily_predictive | reflected on those tests or __`necessarily`__ predictive of later economic success | Reading and math test scores are predictive of economic success later in life , but __`not`__ everything we teach in reading and math is reflected on those tests or __`necessarily`__ predictive of later economic success .                                                                         |
    | pcc_eng_17_081.6290_x1303004_77:50-51-52 | or               | necessarily_productive | dog is __`not`__ appropriate or __`necessarily`__ productive .                     | While it may use up a lot of space in the book , all that explanation of how dogs and wolves are different ultimately helps us to fully understand why using the " pack mentality " and dominance approach to how one deals with their dog is __`not`__ appropriate or __`necessarily`__ productive . |
    | pcc_eng_07_084.6026_x1350878_12:09-10-11 | or               | necessarily_true       | think it 's fair or __`necessarily`__ true to many I know                          | I do __`n't`__ even think it 's fair or __`necessarily`__ true to many I know to use the phrase " right- wing " to label these ideas , as it 's more like " nut-wing " to me and at any extreme edge along a political compass .                                                                      |
    | pcc_eng_03_106.7755_x1712578_38:22-23-24 | or               | necessarily_untrained  | as you insinuated ) or __`necessarily`__ untrained .                               | I do __`n't`__ see anything in the OP 's post that said the dog was unattended ( as you insinuated ) or __`necessarily`__ untrained .                                                                                                                                                                 |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* yet `
      - ✓ Applied filter: `adv_form_lower==^yet$`
      - ✓ Applied filter: `pattern==.*L$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                    | mir_form_lower   | bigram_lower   | text_window                                                                       | token_str                                                                                                                                                                                                                                                                                                                                                        |
    |:------------------------------------------|:-----------------|:---------------|:----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_00_068.1007_x1084525_32:29-32-33  | something        | yet_appealing  | realm of fairies , something simple and __`yet`__ appealing to a younger audience | For light entertainment it 's okay , but then again the original book itself is __`n't`__ much else than a fantastic journey into the realm of fairies , something simple and __`yet`__ appealing to a younger audience , and if you do __`n't`__ care much for character development or heavy themes , it 's alright .                                          |
    | nyt_eng_20070107_0095_4:39-41-42          | something        | yet_available  | to Phoenix to get something __`not`__ yet available on the West Coast             | when more than a decade ago he moved into his previous home , in Coldwater Canyon , only to learn he could __`not`__ pick up a cable signal , he dispatched a production assistant to Phoenix to get something __`not`__ yet available on the West Coast : DirecTV .                                                                                             |
    | pcc_eng_08_045.0918_x0713586_39:63-65-66  | something        | yet_distinct   | to our reality , something abstract __`yet`__ distinct and relatable .            | I was torn on the gods : on one hand they are __`not`__ as meddling as Liu perhaps would have them be , while on the other they do a wonderful job of making the text epic -- of creating that proper distance from our reality to the reality of the story , and therefore also a mirror to our reality , something abstract __`yet`__ distinct and relatable . |
    | pcc_eng_21_056.6212_x0899253_115:45-47-48 | something        | yet_lovely     | indeed and give you something little __`yet`__ lovely to admire every spring      | If you are an admirer of Australian plants in general but do __`n't`__ have enough sunshine to grow the bigger sun-loving natives , a few pots of these beautiful little native orchids will fit into that semi-shaded spot very nicely indeed and give you something little __`yet`__ lovely to admire every spring .                                           |
    | pcc_eng_15_013.4718_x0201157_030:22-23-24 | something        | yet_unfinished | reason to believe that something __`yet`__ unfinished is coming for me            | Ken 's sticking around me , and he 's __`not`__ the idle type ; I have every reason to believe that something __`yet`__ unfinished is coming for me as a loose end , and Ken is using me as bait to get at it - and both of us know it .                                                                                                                         |
    | pcc_eng_03_097.9630_x1569987_08:07-10-11  | something        | yet_unknown    | not even begin until something ( still __`yet`__ unknown to us ) happens          | Evolution can __`not`__ even begin until something ( still __`yet`__ unknown to us ) happens first .                                                                                                                                                                                                                                                             |
    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `token_str== n[o']t .* yet `
      - ✓ Applied filter: `adv_form_lower==^yet$`
      - ✓ Applied filter: `pattern==.*R$`
    
    ### 6 random rows matching filter(s) from `input frame`
    
    | hit_id                                       | mir_form_lower   | bigram_lower     | text_window                                                                                       | token_str                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    |:---------------------------------------------|:-----------------|:-----------------|:--------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | nyt_eng_20060708_0187_22:05-09-10            | everyone         | yet_comfortable  | that does __`not`__ mean everyone in America is __`yet`__ comfortable with interracial marriage ; | that does __`not`__ mean everyone in America is __`yet`__ comfortable with interracial marriage ; it means the law affords them no remedy for their discomfort .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    | pcc_eng_07_026.0948_x0405987_45:28-30-31     | everyone         | yet_willing      | an investment that __`not`__ everyone is __`yet`__ willing to make .                              | Although those who buy Net Zero homes will never experience the stale home smell or the cold basement feeling again , it is an investment that __`not`__ everyone is __`yet`__ willing to make .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    | pcc_eng_08_027.0334_x0421722_05:10-16-17     | many             | yet_unknown      | for modern makers as many of these modern makers are __`yet`__ unknown to me .                    | I do __`n't`__ give values for modern makers as many of these modern makers are __`yet`__ unknown to me .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    | pcc_eng_16_018.6265_x0285541_08628:07-10-11  | or               | yet_more         | your cruelty contented , or have I __`yet`__ more to suffer ?                                     | Is __`not`__ your cruelty contented , or have I __`yet`__ more to suffer ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    | pcc_eng_04_054.2382_x0859969_308:135-137-138 | or               | yet_undeveloped  | rights ( publically owned or as __`yet`__ undeveloped ) of effective use                          | Obviously , the crisis will be ensuring the stability of long-term and settled use of the land , for the moment that the power of the movement weakens , it is more than possible that the forces of nation -state and capital will take the opportunity to fight back , thus destroying previous gains ; and the critical factor in this respect will be whether or __`not`__ the movement will prove , under particular circumstances when the attributes of the nation ( class or other societies ) are in the movement 's favour , robust and efficacious enough to seize hold of such opportunity and transform itself into a resulting organisational structure and whether , through the process of national and legal legitimisation , the peasants will earn the lands rights ( publically owned or as __`yet`__ undeveloped ) of effective use for the purposes of their livelihoods ; and whether this demand can be extended and become a shared consciousness at the national , local , and global levels , is a question worthy of our further thought . |
    | pcc_eng_19_090.9902_x1454514_30:114-116-117  | or               | yet_unidentified | integrity of any surviving or as __`yet`__ unidentified archaeological remains associated with    | Key elements that contribute to the heritage character of the site include : - the original location of the Elizabeth and Mary wreck in the St. Lawrence River , on the seabed of Anse-aux - Bouleaux , __`not`__ far from Baie-Trinite , in the Cote - Nord region of Quebec ; - the continued association of the site with the collection of more than 4,000 perfectly preserved artifacts found during the dives which relate to the navigation , armament , food , clothing , hygiene and the living conditions of the expedition , removed for research , and in storage and on display to the public ; - the integrity of any surviving or as __`yet`__ unidentified archaeological remains associated with the wreck of the Elizabeth and Mary , which may be found within the site in their original placement and extent .                                                                                                                                                                                                                                    |


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
pmir['adv_index'] = pd.to_numeric(pmir.index.to_series().str.split(':').str.get(-1).apply(lambda i: re.search(r'-(\d+)-', i).group().strip('-')), downcast='unsigned')
pmir['preceding_text'] = pmir.apply(lambda x: ' '.join(x.token_str.split()[:x.adv_index - 1]), axis='columns').astype('string')
```


```python
show_sample(pmir[['preceding_text', 'bigram_lower', 'token_str']].sample(5))
```

    +------------------------+------------------------------------------+----------------------+---------------------------------------------------------+
    | hit_id                 | preceding_text                           | bigram_lower         | token_str                                               |
    +========================+==========================================+======================+=========================================================+
    | pcc_eng_06_009.0943_x0 | There 's just something                  | so_solid             | There 's just something so solid , so comforting about  |
    | 130776_7:4-5-6         |                                          |                      | a piping hot flaky disc which conceals a tender and     |
    |                        |                                          |                      | buttery crumb .                                         |
    +------------------------+------------------------------------------+----------------------+---------------------------------------------------------+
    | nyt_eng_20100804_0062_ | in the Harlem store , popular brands     | conspicuously_absent | in the Harlem store , popular brands like JK Jemma Kidd |
    | 34:24-25-26            | like JK Jemma Kidd , Napoleon Perdis '   |                      | , Napoleon Perdis ' NP Set and Petra Strand 's Pixi     |
    |                        | NP Set and Petra Strand 's Pixi were all |                      | were all conspicuously absent .                         |
    +------------------------+------------------------------------------+----------------------+---------------------------------------------------------+
    | pcc_eng_01_037.2456_x0 | I am suggesting there is something       | vitally_important    | I am suggesting there is something vitally important    |
    | 585508_17:6-7-8        |                                          |                      | about the experience of being in environments where     |
    |                        |                                          |                      | loss and hardship are out in the open , where the need  |
    |                        |                                          |                      | for individual courage and collective solidarity is     |
    |                        |                                          |                      | painfully obvious .                                     |
    +------------------------+------------------------------------------+----------------------+---------------------------------------------------------+
    | pcc_eng_20_087.3033_x1 | It is true that HAL goes on to begin     | more_human           | It is true that HAL goes on to begin murdering the crew |
    | 394229_096:23-25-26    | murdering the crew of Discovery , but on |                      | of Discovery , but on some level this makes him all the |
    |                        | some level this makes him all the        |                      | more human .                                            |
    +------------------------+------------------------------------------+----------------------+---------------------------------------------------------+
    | pcc_eng_18_019.9011_x0 | All                                      | very_nice            | All very nice , you might say , but what about the cost |
    | 305893_19:1-2-3        |                                          |                      | ?                                                       |
    +------------------------+------------------------------------------+----------------------+---------------------------------------------------------+



```python
show_sample(pmir[['preceding_text', 'bigram_lower', 'token_str']].sample(5), format='pipe')
```

    | hit_id                                    | preceding_text                                                                                                                             | bigram_lower     | token_str                                                                                                                                                                     |
    |:------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_15_088.6009_x1415991_30:4-5-6     | Has she done something                                                                                                                     | so_egregious     | Has she done something so egregious that it warrants such venomous comments ?                                                                                                 |
    | pcc_eng_15_006.3691_x0086627_053:16-18-19 | For many locals , it was also the first big trip to this region and everyone was                                                           | very_excited     | For many locals , it was also the first big trip to this region and everyone was very excited and happy .                                                                     |
    | pcc_eng_26_106.7456_x1709931_13:6-7-8     | But something like this -- something                                                                                                       | so_unexpected    | But something like this -- something so unexpected , so final -- makes the reality of the situation a little clearer than the romantic ideal .                                |
    | pcc_eng_26_026.5146_x0412213_11:4-6-7     | These shows are all the                                                                                                                    | more_impressive  | These shows are all the more impressive considering the relative creative constraints under which previous generations of TV writers labored .                                |
    | pcc_eng_21_062.5818_x0995326_21:28-29-30  | When it 's actually art and not just some toy scribbling their initials as fast as they can , I do think it is capable of adding something | really_wonderful | When it 's actually art and not just some toy scribbling their initials as fast as they can , I do think it is capable of adding something really wonderful to public space . |



```python
pmir['after_neg'] = pmir.preceding_text.str.lower().str.contains(r"\b(no|n[o']t|no(body| one|thing|where)|(rare|scarce|bare|hard)ly|without|never)\b", regex=True)
show_sample(pmir.loc[pmir.after_neg, ['preceding_text', 'bigram_lower', 'token_str']].sample(10))
```

    /tmp/ipykernel_28020/1348533305.py:1: UserWarning: This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.
      pmir['after_neg'] = pmir.preceding_text.str.lower().str.contains(r"\b(no|n[o']t|no(body| one|thing|where)|(rare|scarce|bare|hard)ly|without|never)\b", regex=True)


    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | hit_id                 | preceding_text                           | bigram_lower           | token_str                                               |
    +========================+==========================================+========================+=========================================================+
    | pcc_eng_02_104.3362_x1 | I found that the mood on this album was  | too_mournful           | I found that the mood on this album was consistent      |
    | 671023_332:17-18-19    | consistent throughout , never becoming   |                        | throughout , never becoming too uplifting or too        |
    |                        | too uplifting or                         |                        | mournful , but steady and very revealing , almost       |
    |                        |                                          |                        | meditative .                                            |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_14_099.6160_x1 | " We 've competed in Nationals so it 's  | completely_new         | " We 've competed in Nationals so it 's not something   |
    | 594081_09:11-12-13     | not something                            |                        | completely new , but it is weird , especially at a dual |
    |                        |                                          |                        | meet . "                                                |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_17_072.3109_x1 | I 've been working with Guy Viner and    | more_crazy             | I 've been working with Guy Viner and until now I am    |
    | 152357_10:21-22-23     | until now I am not really sure if he is  |                        | not really sure if he is more talented or more crazy .  |
    |                        | more talented or                         |                        |                                                         |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_15_063.7716_x1 | Those who had a supportive work          | more_satisfied         | Those who had a supportive work environment felt they   |
    | 013972_17:22-23-24     | environment felt they did not have to go |                        | did not have to go to work when ill , and were both     |
    |                        | to work when ill , and were both         |                        | more satisfied with their jobs and healthier . "        |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_21_084.9338_x1 | Playing live blackjack all day and       | more_profitable        | Playing live blackjack all day and everyday has never   |
    | 356731_02:12-13-14     | everyday has never been easier or        |                        | been easier or more profitable than it is at Global     |
    |                        |                                          |                        | Live Casino .                                           |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_15_050.8072_x0 | " We did not file any document and we    | not_true               | " We did not file any document and we are not saying    |
    | 805216_14:17-18-19     | are not saying that it 's true or        |                        | that it 's true or not true , " he said .               |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_21_078.0603_x1 | Sekulow referenced when Israeli Prime    | more_heroic            | Sekulow referenced when Israeli Prime Minister Ben      |
    | 245291_14:40-41-42     | Minister Ben Gurion eulogized the        |                        | Gurion eulogized the defenders of Gush Etzion in 1948 , |
    |                        | defenders of Gush Etzion in 1948 , " I   |                        | " I can think of no battle in the annals of the Israel  |
    |                        | can think of no battle in the annals of  |                        | Defense Forces which was more magnificent , more tragic |
    |                        | the Israel Defense Forces which was more |                        | or more heroic than the struggle for Gush Etzion ...    |
    |                        | magnificent , more tragic or             |                        |                                                         |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_14_064.8076_x1 | I guess Orkut is n't a major priority    | more_exciting          | I guess Orkut is n't a major priority for Google but it |
    | 031245_17:34-35-36     | for Google but it has a large user base  |                        | has a large user base and it would be a shame if they   |
    |                        | and it would be a shame if they turned   |                        | turned their backs on Orkut and looked for something    |
    |                        | their backs on Orkut and looked for      |                        | more exciting .                                         |
    |                        | something                                |                        |                                                         |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_11_012.6811_x0 | Dr. Ebbing Lautenbach , chief of the     | actually_inappropriate | Dr. Ebbing Lautenbach , chief of the infectious         |
    | 188835_25:24-29-30     | infectious diseases division at the      |                        | diseases division at the University of Pennsylvania ,   |
    |                        | University of Pennsylvania , agreed the  |                        | agreed the study ca n't show whether all of the         |
    |                        | study ca n't show whether all of the     |                        | prescriptions were actually inappropriate .             |
    |                        | prescriptions were                       |                        |                                                         |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+
    | pcc_eng_00_025.2926_x0 | You never know if it 's a tight race     | completely_nonsensical | You never know if it 's a tight race what 's gonna come |
    | 392803_079:18-19-20    | what 's gonna come out it could be       |                        | out it could be something completely nonsensical but .  |
    |                        | something                                |                        |                                                         |
    +------------------------+------------------------------------------+------------------------+---------------------------------------------------------+



```python
some_neg_ex = pmir.loc[pmir.after_neg, ['preceding_text', 'bigram_lower', 'token_str']].sample(6)
show_sample(some_neg_ex.assign(
    preceding_text=embolden(some_neg_ex.preceding_text, 
                            f' ({REGNOT}|nobody|nothing|never|none|no) ')
    ), format='pipe')
```

    | hit_id                                    | preceding_text                                                                                                                                                                                                                                                                                  | bigram_lower        | token_str                                                                                                                                                                                                                                                                                                                                                                   |
    |:------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_11_013.8090_x0207020_504:12-13-14 | In this middle - of- nowhere land , the Kungsleden is sometimes                                                                                                                                                                                                                                 | hardly_more         | In this middle - of- nowhere land , the Kungsleden is sometimes hardly more than a nervous groove cut through the thin topsoil , or a strip of exposed stones with occasional cairns , like lighthouses in a wide green sea .                                                                                                                                               |
    | pcc_eng_04_004.9211_x0063505_40:25-26-27  | It does __`n't`__ help that the scene where Alex comes to have dinner with the Bravermans is kinda silly , what with him being all                                                                                                                                                              | impossibly_virtuous | It does n't help that the scene where Alex comes to have dinner with the Bravermans is kinda silly , what with him being all impossibly virtuous and Adam always seeming like he 's going to punch the kid , but then looking as if he 's tremendously moved by his plight or something .                                                                                   |
    | pcc_eng_12_069.0750_x1100093_14:08-09-10  | It does __`n't`__ take a great imagination or                                                                                                                                                                                                                                                   | much_more           | It does n't take a great imagination or much more than a B-level technothriller writer to see where that has the potential to go , especially when the neighbors are nations like Turkey ( dealing with a forced secularization of the world 's most militant Islamic nation ) and Saudi Arabia ( where an entire population smolders under a brutal medieval theocracy ) . |
    | pcc_eng_02_004.3866_x0054663_041:61-62-63 | Let us try __`not`__ to snicker over trivia : that the man 's name is also the name of the least stylish of all hair styles , and that in the mug shots we see that , to a man , they would all benefit immensely from the services of a skilled barber , because their hair and beards are all | as_ugly             | Let us try not to snicker over trivia : that the man 's name is also the name of the least stylish of all hair styles , and that in the mug shots we see that , to a man , they would all benefit immensely from the services of a skilled barber , because their hair and beards are all as ugly as so many mud fences .                                                   |
    | nyt_eng_19980223_0317_6:10-20-21          | it 's __`not`__ always like that , but too often the image of a rude and arrogant press is                                                                                                                                                                                                      | more_accurate       | it 's not always like that , but too often the image of a rude and arrogant press is more accurate than many of us would like to admit .                                                                                                                                                                                                                                    |
    | pcc_eng_27_061.3710_x0975760_07:17-18-19  | We also se the latest machinery in the cleaning industry therefore __`no`__ job is too small or                                                                                                                                                                                                 | too_big             | We also se the latest machinery in the cleaning industry therefore no job is too small or too big for us , Abalandi Holdings believes in leaving the client happy and with that its retention and an ongoing relationship , Your pocket is our concern as we will tailor a service that meets your budget .                                                                 |



```python
print(f'* ${pmir.after_neg.value_counts()[False]:,}$ tokens in `POSmirror` hits not preceded by negation')
print('  > - I.e. what would remain if _all_ potential contaminants were excluded')
print(f'  > - _{pmir.after_neg.value_counts()[True]:,}_ potential exclusions')
print(f'* ${len(nmir):,}$ tokens in `NEGmirror` hits')
print(f'* Remaining Sample Size Discrepancy: ${pmir.after_neg.value_counts()[False] - len(nmir):,}$')
```

    * $1,434,420$ tokens in `POSmirror` hits not preceded by negation
      > - I.e. what would remain if _all_ potential contaminants were excluded
      > - _241,081_ potential exclusions
    * $285,435$ tokens in `NEGmirror` hits
    * Remaining Sample Size Discrepancy: $1,148,985$


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



```python
enforced_pos= pmir.loc[~pmir.after_neg, :'preceding_text']
enforced_pos.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 1434420 entries, apw_eng_19941111_0004_1:14-15-16 to pcc_eng_val_3.11253_x52703_07:08-10-11
    Data columns (total 21 columns):
     #   Column           Non-Null Count    Dtype   
    ---  ------           --------------    -----   
     0   adv_form         1434420 non-null  category
     1   adj_form         1434420 non-null  category
     2   text_window      1434420 non-null  string  
     3   bigram_id        1434420 non-null  category
     4   token_str        1434420 non-null  string  
     5   mir_deprel       1434420 non-null  category
     6   mir_head         1434420 non-null  category
     7   mir_lemma        1434420 non-null  category
     8   adv_lemma        1434420 non-null  category
     9   adj_lemma        1434420 non-null  category
     10  mir_form         1434420 non-null  category
     11  mir_form_lower   1434420 non-null  category
     12  adv_form_lower   1434420 non-null  category
     13  adj_form_lower   1434420 non-null  category
     14  bigram_lower     1434420 non-null  category
     15  all_forms_lower  1434420 non-null  category
     16  pattern          1434420 non-null  category
     17  category         1434420 non-null  category
     18  prev_form_lower  1434420 non-null  category
     19  adv_index        1434420 non-null  uint8   
     20  preceding_text   1434420 non-null  string  
    dtypes: category(17), string(3), uint8(1)
    memory usage: 1.0 GB



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
    
    +------------------------+--------------------------+--------------------------------------------------------------+
    | hit_id                 | all_forms_lower          | token_str                                                    |
    +========================+==========================+==============================================================+
    | pcc_eng_09_044.5386_x0 | all_exactly_right        | All that is __`exactly`__ right , because deciding on a      |
    | 704486_15:1-4-5        |                          | university is often the first really major decision of a     |
    |                        |                          | young adult 's life .                                        |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_10_096.0405_x1 | all_exactly_identical    | The doors were evenly spaced from one another , and they     |
    | 536500_662:13-14-15    |                          | were all __`exactly`__ identical .                           |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_11_014.7695_x0 | or_exactly_diligent      | The cloths representing the flag , ' ' palace of governador  |
    | 222721_006:30-31-32    |                          | ' ' , the incorporation of people of positions of the        |
    |                        |                          | governmental apparatus , status in the society or            |
    |                        |                          | __`exactly`__ diligent as they themselves that are           |
    |                        |                          | incorporating for example ' ' driver of caminho ' ' - , the  |
    |                        |                          | egg in the head of the statue representing the hat used for  |
    |                        |                          | the governors , everything following the same ' ' protocolo  |
    |                        |                          | ' ' of the colonizadores .                                   |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_12_107.08000_x | or_exactly_equivalent    | DON'T FENCEMEIN : Nearly the size of Manhattan Island ( or   |
    | 1726258_109:11-12-13   |                          | __`exactly`__ equivalent to the square mileage of the City   |
    |                        |                          | of Santa Barbara ) , the " Hanson Ranch " was pieced         |
    |                        |                          | together slowly by Louise Hanson starting in 1972 and        |
    |                        |                          | eventually grew to include eight previously individual       |
    |                        |                          | properties that span much of the land between Highway 1 and  |
    |                        |                          | Route 246 and Highway 101 .                                  |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_14_100.6183_x1 | all_exactly_alike        | We visited the workrooms at Redwing Pottery in Redwing ,     |
    | 610324_19:40-41-42     |                          | Minnesota once and watched the whole process , but the best  |
    |                        |                          | part was a single potter throwing the same pot , on a wheel  |
    |                        |                          | , one after another , all __`exactly`__ alike except not     |
    |                        |                          | somehow .                                                    |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_16_035.7224_x0 | all_exactly_right        | All of those are __`exactly`__ right !                       |
    | 561972_51:1-5-6        |                          |                                                              |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_23_061.1887_x0 | everything_exactly_right | Recently , I saw the power of open in action -- and it both  |
    | 972433_016:23-29-30    |                          | broke my heart and made me feel like everything our team had |
    |                        |                          | done was __`exactly`__ right .                               |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_24_012.7792_x0 | all_exactly_alike        | how could we all get along if we were all __`exactly`__      |
    | 189980_12:10-11-12     |                          | alike ?                                                      |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_24_013.4738_x0 | both_exactly_alike       | I married a lady , with whom I lived very happily , but ,    |
    | 201045_009:76-78-79    |                          | being obliged to go to Epidamnum , I was detained there by   |
    |                        |                          | my business six months , and then , finding I should be      |
    |                        |                          | obliged to stay some time longer , I sent for my wife , who  |
    |                        |                          | , as soon as she arrived , was brought to bed of two sons ,  |
    |                        |                          | and what was very strange , they were both so __`exactly`__  |
    |                        |                          | alike that it was impossible to distinguish the one from the |
    |                        |                          | other .                                                      |
    +------------------------+--------------------------+--------------------------------------------------------------+
    | pcc_eng_28_074.0381_x1 | or_exactly_identical     | Witnesses ' statements conflict or are __`exactly`__         |
    | 181327_16:5-7-8        |                          | identical to the employee 's ;                               |
    +------------------------+--------------------------+--------------------------------------------------------------+



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
    
    | hit_id                                    | all_forms_lower             | text_window                                                                                                                 | token_str                                                                                                                                                                                                                                                                                                                     |
    |:------------------------------------------|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_07_074.2182_x1183280_143:23-28-29 | everything_exactly_accurate | came across this and everything you have said is __`exactly`__ accurate to what I have                                      | I 'm 3 days into my split and would be in some serious agony at night so I came across this and everything you have said is __`exactly`__ accurate to what I have experienced / am experiencing .                                                                                                                             |
    | pcc_eng_17_017.7709_x0271342_22:53-59-60  | or_exactly_alike            | they came from , or why their genetic structure is __`exactly`__ alike .                                                    | The clones look alike but all have different personalities -- so far there 's a soccer mom , a hippie science nerd , a Russian spitfire , and a cop , all played brilliantly by the Canadian actress Tatiana Maslany - - but none of them know where they came from , or why their genetic structure is __`exactly`__ alike . |
    | pcc_eng_29_041.8913_x0660527_20:09-10-11  | all_exactly_alike           | Man Whose Teeth Were All Exactly Alike I have is hardcover                                                                  | The edition of The Man Whose Teeth Were All Exactly Alike I have is hardcover , published by Tor Books , posthumously by Mr. Dick 's estate in 1984 .                                                                                                                                                                         |
    | pcc_eng_07_002.9468_x0031350_128:19-20-21 | or_exactly_equal            | or less than n or __`exactly`__ equal to n .                                                                                | The total value of all pips in a spell must be greater than n or less than n or __`exactly`__ equal to n .                                                                                                                                                                                                                    |
    | pcc_eng_00_044.4965_x0702889_30:09-12-13  | or_exactly_identical        | now effectively infinite ( or at least __`exactly`__ identical to the entire corpus                                         | My record collection is now effectively infinite ( or at least __`exactly`__ identical to the entire corpus of recorded music ) but that does n't mean I want it all on a hard drive in my house .                                                                                                                            |
    | pcc_eng_21_034.0405_x0534239_002:1-3-4    | or_exactly_more             | Or more __`exactly`__ more of a private ideological                                                                         | Or more __`exactly`__ more of a private ideological ( provided it is the right one ) entrepreneur driven program .                                                                                                                                                                                                            |
    | pcc_eng_01_007.5031_x0105039_16:01-17-18  | everything_exactly_right    | Everything from the frieze boards on the exterior to the window trim on the interior is __`exactly`__ right for the space . | Everything from the frieze boards on the exterior to the window trim on the interior is __`exactly`__ right for the space .                                                                                                                                                                                                   |
    | pcc_eng_15_031.9549_x0500468_154:1-2-3    | all_exactly_wrong           | All __`exactly`__ wrong for the start of                                                                                    | All __`exactly`__ wrong for the start of the mass , I would suggest .                                                                                                                                                                                                                                                         |
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `adv_form_lower==exactly`
      - ✓ Applied filter: `pattern==pos-mirror-L`
    
    ### 8 random rows matching filter(s) from `input frame`
    
    | hit_id                                    | all_forms_lower            | text_window                                                                   | token_str                                                                                                                                                                   |
    |:------------------------------------------|:---------------------------|:------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | pcc_eng_05_069.4747_x1107978_086:1-2-3    | everybody_exactly_alike    | Everybody __`exactly`__ alike . "                                             | Everybody __`exactly`__ alike . "                                                                                                                                           |
    | pcc_eng_06_038.9890_x0614425_107:3-6-7    | all_exactly_alike          | They are all of them __`exactly`__ alike , and there is                       | They are all of them __`exactly`__ alike , and there is not one of them can be eaten .                                                                                      |
    | pcc_eng_01_028.2684_x0440942_22:23-24-25  | everyone_exactly_alike     | keys or surfaces , everyone __`exactly`__ alike .                             | All we have is typewriting : a series of gestures that are always the same - taps on keys or surfaces , everyone __`exactly`__ alike .                                      |
    | pcc_eng_04_104.1453_x1666254_08:20-21-22  | something_exactly_opposite | say that somebody said something __`exactly`__ opposite to what they actually | misrepresentation is the kind of thing you and Goerzen do where you outright lie and say that somebody said something __`exactly`__ opposite to what they actually said . > |
    | pcc_eng_15_106.5980_x1707092_015:16-17-18 | something_exactly_related  | , you offered them something __`exactly`__ related to the post they           | What if , instead of pointing visitors to a semi-related resource , you offered them something __`exactly`__ related to the post they just read ?                           |
    | pcc_eng_01_090.6691_x1449922_24:1-2-3     | everything_exactly_same    | Everything __`exactly`__ same , minimum 290 people                            | Everything __`exactly`__ same , minimum 290 people dead .                                                                                                                   |
    | pcc_eng_11_064.7133_x1031125_24:1-2-3     | everything_exactly_same    | Everything __`exactly`__ same , minimum two hundred                           | Everything __`exactly`__ same , minimum two hundred ninety people dead .                                                                                                    |
    | pcc_eng_08_106.0266_x1700594_12:1-2-3     | everything_exactly_same    | Everything __`exactly`__ same , minimum 290 people                            | Everything __`exactly`__ same , minimum 290 people dead .                                                                                                                   |


# FIXME 
  👇 🪲


```python
enforced_pos['utt_len']= pd.to_numeric(enforced_pos.token_str.apply(lambda x: int(len(x.split()))), downcast='integer')
```


```python
dups = enforced_pos.loc[enforced_pos.duplicated(subset=['token_str', 'all_forms_lower'], keep=False), ['all_forms_lower', 'token_str', 'utt_len']]
show_sample(dups.loc[dups.utt_len>=80, :].sort_values(['utt_len', 'token_str']).head(6))
```

    +------------------------+-----------------------+--------------------------------------------------------------+-----------+
    | hit_id                 | all_forms_lower       | token_str                                                    |   utt_len |
    +========================+=======================+==============================================================+===========+
    | pcc_eng_14_107.06555_x | or_too_little         | All of the types of depression may be accompanied by sighs , |        80 |
    | 1724020_021:25-26-27   |                       | tears , outbursts , impulsivity , disturbances of sleep (    |           |
    |                        |                       | too much or too little ) , eating ( too much or too little ) |           |
    |                        |                       | , stomach problems , random aches and pains , changes in     |           |
    |                        |                       | libido ( too much or too little ) , and often a reluctance   |           |
    |                        |                       | to do anything from taking care of major responsibilities to |           |
    |                        |                       | maintaining activities of daily living such as hygiene .     |           |
    +------------------------+-----------------------+--------------------------------------------------------------+-----------+
    | pcc_eng_14_107.06555_x | or_too_little         | All of the types of depression may be accompanied by sighs , |        80 |
    | 1724020_021:34-35-36   |                       | tears , outbursts , impulsivity , disturbances of sleep (    |           |
    |                        |                       | too much or too little ) , eating ( too much or too little ) |           |
    |                        |                       | , stomach problems , random aches and pains , changes in     |           |
    |                        |                       | libido ( too much or too little ) , and often a reluctance   |           |
    |                        |                       | to do anything from taking care of major responsibilities to |           |
    |                        |                       | maintaining activities of daily living such as hygiene .     |           |
    +------------------------+-----------------------+--------------------------------------------------------------+-----------+
    | pcc_eng_14_107.06555_x | or_too_little         | All of the types of depression may be accompanied by sighs , |        80 |
    | 1724020_021:53-54-55   |                       | tears , outbursts , impulsivity , disturbances of sleep (    |           |
    |                        |                       | too much or too little ) , eating ( too much or too little ) |           |
    |                        |                       | , stomach problems , random aches and pains , changes in     |           |
    |                        |                       | libido ( too much or too little ) , and often a reluctance   |           |
    |                        |                       | to do anything from taking care of major responsibilities to |           |
    |                        |                       | maintaining activities of daily living such as hygiene .     |           |
    +------------------------+-----------------------+--------------------------------------------------------------+-----------+
    | pcc_eng_02_019.3116_x0 | or_otherwise_unlawful | You are solely liable for any unauthorized or otherwise      |        80 |
    | 296430_35:08-09-10     |                       | unlawful use of any log-in information and password we may   |           |
    |                        |                       | make available for you to access any part of this site , and |           |
    |                        |                       | you will indemnify and hold Dayco harmless from any suit ,   |           |
    |                        |                       | claim , loss or damage ( including attorneys ' fees )        |           |
    |                        |                       | arising from or relating to the unauthorized or otherwise    |           |
    |                        |                       | unlawful use of any log-in information or password used to   |           |
    |                        |                       | access any part of this site .                               |           |
    +------------------------+-----------------------+--------------------------------------------------------------+-----------+
    | pcc_eng_02_019.3116_x0 | or_otherwise_unlawful | You are solely liable for any unauthorized or otherwise      |        80 |
    | 296430_35:62-63-64     |                       | unlawful use of any log-in information and password we may   |           |
    |                        |                       | make available for you to access any part of this site , and |           |
    |                        |                       | you will indemnify and hold Dayco harmless from any suit ,   |           |
    |                        |                       | claim , loss or damage ( including attorneys ' fees )        |           |
    |                        |                       | arising from or relating to the unauthorized or otherwise    |           |
    |                        |                       | unlawful use of any log-in information or password used to   |           |
    |                        |                       | access any part of this site .                               |           |
    +------------------------+-----------------------+--------------------------------------------------------------+-----------+
    | pcc_eng_18_108.0672_x1 | or_even_greek         | Great mysteries " ( 1:6S ) , the term , well attested in     |        82 |
    | 734493_32:70-71-72     |                       | apocalyptic parallels , was replaced by " mysteries " in G.  |           |
    |                        |                       | - " ... stirring [ the clay for bricks ] " ( 3:5S ) ,        |           |
    |                        |                       | paralleled in an aggadic account , replaced with " making    |           |
    |                        |                       | bricks " in G. 26 Introduction Some mss of S present angels  |           |
    |                        |                       | ' names in Semitic ( rather than Slavic or even Greek )      |           |
    |                        |                       | rather than Slavic or even Greek ) forms .                   |           |
    +------------------------+-----------------------+--------------------------------------------------------------+-----------+



```python
new_pmir = pd.concat((enforced_pos.loc[enforced_pos.utt_len < 80, :],
                      enforced_pos.loc[enforced_pos.utt_len >= 80, :].drop_duplicates(
                          subset=['token_str', 'all_forms_lower'], keep='first'))
                     )
```


```python
print(f'{len(new_pmir):,} hits remaining in `POSmirror` set after additional filtering')
```

    1,434,380 hits remaining in `POSmirror` set after additional filtering



```python
show_sample(new_pmir.sample(6)[['all_forms_lower', 'text_window']])
```

    +------------------------+-------------------------+-----------------------------------------------+
    | hit_id                 | all_forms_lower         | text_window                                   |
    +========================+=========================+===============================================+
    | pcc_eng_09_069.4170_x1 | all_more_human          | this by making him all the more human         |
    | 106792_109:17-19-20    |                         | emotionally , and filling                     |
    +------------------------+-------------------------+-----------------------------------------------+
    | pcc_eng_19_049.7594_x0 | something_very_wrong    | , I could tell something was very wrong today |
    | 787089_49:6-8-9        |                         | at Mc Donalds                                 |
    +------------------------+-------------------------+-----------------------------------------------+
    | pcc_eng_03_003.4198_x0 | or_not_safe             | lock is unsecure ' or ' your lock is not safe |
    | 038990_3:35-40-41      |                         | '                                             |
    +------------------------+-------------------------+-----------------------------------------------+
    | pcc_eng_19_063.7973_x1 | something_very_personal | because Esposito told him something very      |
    | 013949_18:22-23-24     |                         | personal and inspirational .                  |
    +------------------------+-------------------------+-----------------------------------------------+
    | pcc_eng_23_050.0325_x0 | often_more_stable       | workers and , very often , these day workers  |
    | 792054_23:24-30-31     |                         | are more stable , staying with the            |
    +------------------------+-------------------------+-----------------------------------------------+
    | pcc_eng_20_018.0404_x0 | or_as_detailed          | any time by unsubscribing or as detailed in   |
    | 275207_20:12-13-14     |                         | our terms .                                   |
    +------------------------+-------------------------+-----------------------------------------------+



```python
new_pmir = new_pmir.loc[:, :'category']
new_pmir['trigger_lower'] = new_pmir['mir_form_lower'].astype('category')
new_pmir.columns
```




    Index(['adv_form', 'adj_form', 'text_window', 'bigram_id', 'token_str',
           'mir_deprel', 'mir_head', 'mir_lemma', 'adv_lemma', 'adj_lemma',
           'mir_form', 'mir_form_lower', 'adv_form_lower', 'adj_form_lower',
           'bigram_lower', 'all_forms_lower', 'pattern', 'category',
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
      `/share/compling/data/sanpi/4_post-processed/POSmirror/LimitedPOS-trigger-bigrams_thr0-001p.35f.pkl.gz`



```python
nmir['utt_len']= nmir.token_str.apply(lambda x: len(x.split()))
new_nmir = pd.concat((nmir.loc[nmir.utt_len < 80, :], nmir.loc[nmir.utt_len >= 80, :].drop_duplicates(subset=['token_str', 'all_forms_lower'], keep='first')))
new_nmir = new_nmir.loc[:, :'category']
new_nmir['trigger_lower'] = new_nmir.neg_form_lower.astype('category')
show_sample(new_nmir.sample(6)[['trigger_lower', 'all_forms_lower', 'text_window']])

```

    +------------------------+-----------------+------------------------+----------------------------------------------+
    | hit_id                 | trigger_lower   | all_forms_lower        | text_window                                  |
    +========================+=================+========================+==============================================+
    | pcc_eng_08_055.1052_x0 | nothing         | nothing_more_exciting  | " There 's nothing more exciting than that . |
    | 876088_33:4-5-6        |                 |                        | "                                            |
    +------------------------+-----------------+------------------------+----------------------------------------------+
    | pcc_eng_24_070.1460_x1 | nor             | nor_more_different     | Nor as writers could they have been more     |
    | 118408_21:1-8-9        |                 |                        | different in their talents .                 |
    +------------------------+-----------------+------------------------+----------------------------------------------+
    | pcc_eng_06_057.2967_x0 | never           | never_too_late         | USor Canadabecause it 's never too late !    |
    | 911029_18:15-16-17     |                 |                        |                                              |
    +------------------------+-----------------+------------------------+----------------------------------------------+
    | pcc_eng_23_101.1275_x1 | nothing         | nothing_even_close     | " , mostly because nothing else in the       |
    | 618498_04:30-37-38     |                 |                        | kitchen sections was even close .            |
    +------------------------+-----------------+------------------------+----------------------------------------------+
    | pcc_eng_13_014.9416_x0 | nothing         | nothing_more_promising | There 's nothing more promising than a core  |
    | 225224_08:3-4-5        |                 |                        | rulebook                                     |
    +------------------------+-----------------+------------------------+----------------------------------------------+
    | pcc_eng_02_047.0907_x0 | nor             | nor_as_simple          | Nor is it as simple as just turning the      |
    | 745619_017:1-4-5       |                 |                        |                                              |
    +------------------------+-----------------+------------------------+----------------------------------------------+



```python

print(f'\n* {len(nmir):,} original hits in `NEGmirror` (`{path_dict["NEGmirror"].relative_to(POST_PROC_DIR)}`)')
print(f'\n* {len(new_nmir):,} hits remaining in `NEGmirror` set after additional filtering of duplicate hits')

```

    
    * 285,435 original hits in `NEGmirror` (`NEGmirror/trigger-bigrams_thr0-001p.35f.pkl.gz`)
    
    * 285,430 hits remaining in `NEGmirror` set after additional filtering of duplicate hits



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
      `/share/compling/data/sanpi/4_post-processed/NEGmirror/LimitedNEG-trigger-bigrams_thr0-001p.35f.pkl.gz`

