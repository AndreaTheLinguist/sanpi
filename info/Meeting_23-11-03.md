# Meeting: ~~Thursday, Nov 2~~ _Friday, Nov 3_, 2023

## Updates

### Data

#### pattern specifications

- finalized new `.pat` files for negative environments with a direct dependency
  relation between the `NEG` and `ADJ` nodes
  (`ADJ` necessarily has a direct dependency with `ADV`).
  Both of the following now reside in
  `Pat/RBdirect/`---`RB` indicates the added `xpos` limitation for `ADV`,
  and I decided _direct_ is a much clearer descriptor than _contig_)
  1. essentially the original with added relation restrictions:
     - `direct-adj-head.pat`
     - `neg: ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod]-> NEG;`

     > ```js
     > pattern { 
     >     ADJ [xpos=re"JJ.?"]; 
     >     ADV [xpos=re"RB.?"]; 
     >     NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"
     >               |"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
     >     mod: ADJ -[advmod]-> ADV;  
     >     neg: ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod]-> NEG; 
     >     ADV < ADJ;
     >     NEG << ADV
     > }
     > ```
     > 
     > fyi, WILL match negative adverbs to `ADV` node,
     > provided there is an additional negative token matching NEG specs;
     > e.g.:
     > 
     > neg_form | adv_form | adj_form    | text_window                                                | neg_deprel
     > ---------|----------|-------------|------------------------------------------------------------|-----------
     > not      | not      | funny       | July 31 , and not only is it not funny , it totally seemed | advmod
     > Not      | not      | responsible | Not only is christianity not responsible for science , but | advmod
     > not      | not      | possible    | , however it 's not not possible .                         | advmod
     > not      | not      | patriotic   | It 's not that I 'm not patriotic ; it 's just             | advmod
     > Not      | not      | important   | Not that it 's not important to understand and explain     | advmod
     > Not      | not      | sure        | Not to mention , I am not sure if they like Winnie         | advmod
     > n't      | not      | true        | But is n't that just specifically not true ?               | advmod
 
     -------------------------

  2. inverted dominance/governance: `NEG` as the head:
     - `direct-neg-head.pat`
     - `neg: NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;`

     > ```js
     > pattern {
     >     ADJ [xpos=re"JJ.?"];
     >     ADV [xpos=re"RB.?"];
     >     mod: ADJ -[advmod]-> ADV;
     >     ADV < ADJ;
     >     NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"
     >                 |"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];
     >     neg: NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;
     >     NEG << ADV
     > }
     > ```
     > 
     > fyi, WILL match negative adverbs to `ADV` node,
     > provided there is an additional negative token matching NEG specs;
     > e.g.:
     > | neg_form | adv_form | adj_form | text_window                                         | neg_deprel |
     > |----------|----------|----------|-----------------------------------------------------|------------|
     > | Not      | not      | excited  | ( Not that I 'm not excited about those things --   | ccomp      |
     > | nothing  | not      | awkward  | "yeah , there 's nothing not awkward about it , """ | amod       |
     > | nothing  | not      | safe     | There 's nothing not safe about it , nothing        | amod       |
     > | nobody   | not      | good     | There 's nobody not good in the West .              | amod       |
     -------------------------

- ran these on the full corpora set
  - had only tested the dependency relations that showed up in a sample
  - I can can see there are additional problem cases to be dealt with for the full dataset

#### composite dependency "identifiers" for each pattern match/hit

- working on creating a `dep_path` identifier
  - initially assumed it had to be a `str` type, but then considered `tuple` types, esp. `namedtuple`,
    since these are also hashable, and, therefore, can be compared/evaluated by `pandas`
  - then realized (a) I had already had this same reasoning before and \
    (b) since the size (i.e. number of nodes and ties) varies as a result of the pattern type, 
    a `namedtuple` on the highest level has the problem of what to set as a field
  - so currently, each "tie" in the composite dependency between the `NEG` and `ADJ` nodes is 
    defined as a `dep_tuple`
  - but to analyze the composite dependency as a whole, all ties need to be combined into a single object
    - currently, this is done as `str` type objects, 
      with several different variations, depending on which kinds of info are included

      |                    | combined dependency strings                                               |
      |:-------------------|:--------------------------------------------------------------------------|
      | `dep_str`          | existential>more[=mod];none>existential[=neg]                             |
      | `dep_str_ix`       | 29:existential>28:more[=mod];27:none>29:existential[=neg]                 |
      | `dep_str_full`     | 29:existential>[advmod]>28:more[=mod];27:none>[amod]>29:existential[=neg] |
      | `dep_str_rel`      | existential>[advmod]>more[=mod];none>[amod]>existential[=neg]             |
      | `dep_str_mask`     | JJ>RBR;NN>existential                                                     |
      | `dep_str_mask_rel` | JJ>[advmod]>RBR;NN>[amod]>existential                                     |
      
      - info of a _single_ tie (the _mod_ tie `ADJ --> ADV` in this case)
        |                    | mod (of "_none more existential_")                                                                                                                                                                                              |
        |:-------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
        | `contiguous`       | True                                                                                                                                                                                                                            |
        | `relation`         | advmod                                                                                                                                                                                                                          |
        | `head_lemma`       | existential                                                                                                                                                                                                                     |
        | `head_ix`          | 29                                                                                                                                                                                                                              |
        | `head_xpos`        | JJ                                                                                                                                                                                                                              |
        | `target_lemma`     | more                                                                                                                                                                                                                            |
        | `target_ix`        | 28                                                                                                                                                                                                                              |
        | `target_xpos`      | RBR                                                                                                                                                                                                                             |
        | `head_node`        | ADJ                                                                                                                                                                                                                             |
        | `target_node`      | ADV                                                                                                                                                                                                                             |
        | `head_form`        | existential                                                                                                                                                                                                                     |
        | `target_form`      | more                                                                                                                                                                                                                            |
        | `hit_id`           | pcc_eng_29_109.0205_x1740618_22:28-29-30                                                                                                                                                                                        |
        | `pattern`          | direct-neg-head                                                                                                                                                                                                                 |
        | `dep_tuple`        | dep_info(tie='mod', pattern='direct-neg-head', relation='advmod', head_node='ADJ', head_ix='29', head_form='existential', head_lemma='existential', target_node='ADV', target_ix='28', target_form='more', target_lemma='more') |
        | `dep_str`          | existential>more[=mod]                                                                                                                                                                                                          |
        | `dep_str_ix`       | 29:existential>28:more[=mod]                                                                                                                                                                                                    |
        | `dep_str_full`     | 29:existential>[advmod]>28:more[=mod]                                                                                                                                                                                           |
        | `dep_str_rel`      | existential>[advmod]>more[=mod]                                                                                                                                                                                                 |
        | `dep_str_mask`     | JJ>RBR                                                                                                                                                                                                                          |
        | `dep_str_mask_rel` | JJ>[advmod]>RBR                                                                                                                                                                                                                 |

- can view more of this information via new script: `../sanpi/script/sample_pickle.py`

  ```log
  python sample_pickle.py -m -s 10 \
    -c text_window -c dep_str_rel \
    /share/compling/projects/sanpi/demo/data/3_dep_info/RBdirect/bigram_smallest_direct-adj-head_hits[n34]+deps.pkl.gz
  ```

  > ## 10 random rows from `bigram_smallest_direct-adj-head_hits[n34]+deps.pkl.gz`
  >
  > | hit_id                                    | text_window                                                     | dep_str_rel                                                          |
  > |:------------------------------------------|:----------------------------------------------------------------|:---------------------------------------------------------------------|
  > | pcc_eng_29_109.3220_x1745422_14:29-30-31  | , but that 's not entirely accurate .                           | accurate>[advmod]>not[=neg]; accurate>[advmod]>entirely[=mod]        |
  > | pcc_eng_29_109.3185_x1745367_11:18-19-20  | as it clearly is not as dangerous as the others and             | dangerous>[advmod]>not[=neg]; dangerous>[advmod]>as[=mod]            |
  > | apw_eng_20040626_0225_7:38-39-40          | that the president was not seriously ill .                      | ill>[neg]>not[=neg]; ill>[advmod]>seriously[=mod]                    |
  > | pcc_eng_29_109.4425_x1747387_58:11-12-13  | Roth IRA , though not directly related to this particular topic | related>[advmod]>not[=neg]; related>[advmod]>directly[=mod]          |
  > | apw_eng_20040622_0117_23:4-5-6            | `` It 's not so important if I get into                         | important>[neg]>not[=neg]; important>[advmod]>so[=mod]               |
  > | pcc_eng_29_109.3034_x1745107_35:4-5-6     | " It 's never too late for accountability and justice           | late>[advmod]>never[=neg]; late>[advmod]>too[=mod]                   |
  > | pcc_eng_29_109.2489_x1744272_005:4-5-6    | An orgasm is n't just pleasurable -- it also makes              | pleasurable>[advmod]>not[=neg]; pleasurable>[advmod]>just[=mod]      |
  > | pcc_eng_29_109.4390_x1747329_05:3-4-5     | They are n't immediately accessible , and draw you              | accessible>[advmod]>not[=neg]; accessible>[advmod]>immediately[=mod] |
  > | pcc_eng_29_109.0236_x1740673_174:21-22-23 | - that we 're not even cognizant that something has taken       | cognizant>[advmod]>not[=neg]; cognizant>[advmod]>even[=mod]          |
  > | apw_eng_20040626_0040_7:14-15-16          | lap he acknowledged was n't very pretty .                       | pretty>[neg]>not[=neg]; pretty>[advmod]>very[=mod]                   |

#### dependency terminology

- also went down a bit of a rabbit hole last night with terminology dependencies and their parts:
  - `grew` calls each token (e.g. word with a form, index, lemma, etc.) identified in the pattern a `node`
  - it calls the _connection_ between them, an `edge`
    - 🙅‍♀️ I really dislike this term
    - proposal for replacement: `tie`,
      - supported by the definition in construction/engineering: \
        a beam that resists _tension_ (not compression or lateral/perpendicular force)
      - corresponds with the general metaphor
      - also conveniently short
      - isn't used by anything else currently
      - and doesn't start with an `l` (visually ambiguous; first replacement idea was "leg", as in "leg of a trip/journey(path)")
  - didn't want to use `dependency` to refer to the connection object because
    - it's more of a concept and/or the whole structure of nodes + their "connector"
    - makes it harder to talk about "complex" dependencies that build on one another
    - this way a `dependency` is composed
      - 2 `node`s:
        1. `head`
        2. `target`
      - 1 `tie` between them
      - 1 `relation` type (e.g. `advmod`, `amod`, `nsubj`, etc.)
  - 🤔 considering referring to "complex dependencies",
    i.e. more than 1 dependency ({head, target, tie, relation}), a `truss` or something

### Theory

#### negative pronoun post-modification

1. _It's **nothing too serious**._,
2. _**Nobody very interesting** is scheduled to talk today._
3. _She thought he had **nothing especially interesting** to say._

- created new document: [`neg-pronoun_post-mod.md`](../../../Documents/dissertex/justwriting/neg-pronoun_post-mod.md)
- potential equivalence with more transparent cases, i.e.:
  - under sentential negation
  - in predicate following negative subject
- potential caveats
  - not all bigrams are as acceptable in this construction:
    - _nothing_ and _nobody_ select different adjective types
    - and when they do occur with the same bigram, the meaning isn't necessarily the same\
      (but this is more of a global issue of different senses depending on
       the semantic class of the entity being modified; e.g. person vs. event vs. object vs. concept)
  - pragmatic inferences affected by premise of existence; \
    potentially supplied by
    - local linguistic context
      - existence necessitated by other words in the sentence
        - _the_ vs. _a_ vs. no determiner
        - _any_ vs. _some_ vs. _no_
    - anaphoric linguistic context
      - previous updates to common ground indicate existence
    - contextual/situational context
      - assumptions of existence given the topic, setting, etc.
- comparison with strong NPI licensing
  - punctual _until_ behaves differently than _in years/months/days/etc._ and additive _either_
    - but is it due to polarity sensitivity or some other difference in semantic and/or syntactic selection requirements?
    - _in years_ and _either_ appear able to occur in modifier of _nothing_/_nobody_
      - > _Nothing in years has so impressed me with the swiftness of time's flight._[^1]
      - > _That is nothing new, either, because that is exactly what happens when you recover a database._[^2]
      - (_assuming, of course, that these are valid examples_)
    - _until_ does not
  - preliminary hunch of an idea: \
    [_and this is probably not novel---people have been talking about "until" for some time now_]
    - _in years_ and _either_ have simple and/or corroborating semantic contributions
    - so negating them is clearer
    - punctual _until_ has 2 contributions with opposite polarities
      - _until $T$_ = _**at** $T$_ **&** _**$\neg$before** $T$_
      - so it can't move around/isn't as flexible in where it can be interpreted
- attempted to create a very thorough list of examples:
  - [The burglary](../../../Documents/dissertex/justwriting/neg-pronoun_post-mod.md#the-burglary)

[^1]: from Google Ngrams; p.370:
      Literature and Aging: An Anthology. (1992). United States: Kent State University Press.
[^2]: from Google Ngrams; p. 500:
      Bach, M., Arao, K., Colvin, A., Osborne, K., Arao, K., Johnson, R., Hoogland, F., Poder, T.
        (2015). Expert Oracle Exadata. United States: Apress.
