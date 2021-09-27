# Running Notes

## Cases to consider

- `ADJ enough`
- irregular/lexicalized? `not` cases:
  - `not so much`

    - cause:  `not so much that...`
    - subject of content: `not so much about ...`
    - categorizing: `not so much a ...`

  - `not [lower threshold], but [higher threshold]`
    - `not just __, but __`
    - `not only __, but __`  
    - ... `simply`, `merely`, etc.

- `no ADV (ADV) ADJ`
  - `no longer ...`
    - `no longer physcially dependent`
  - `no more ...`
    - `no more [ADJ] (than)` vs. `no more [ADJ] [NOUN]`
    - `no more comfortable`
  - `no less ...`
    - `no less [ADJ`_~ e.g important, weighty, etc._`] a [NOUN]`
- `my form is not the best` -> should this be caught? (with adv)
- `nor` and other(?) negative conjunction cases
- `few`
  - `too few`?
  - `a few`, `the few` vs. `(very) few`
  - **NPI in matrix VP with `few` in subject: disallowed if DP?**

    1. \* A few (strangers) have been here in years.
    1. &rarr; (Very) few (strangers) have been here in years.

    1. \* The few bibliophiles have visited the library in years.
    1. &rarr; (Very) few locals have visited the library in years.

  - **NPI licensed in restriction of _definite_ DP with `few` modifier**

    1. \* A few Americans who have been here in years were (all) students.

    1. &rarr; The (very) few Americans who have been here in years were (all) students._

    1. **? (Very) few Americans who have been here in years were students.**

  - Note: _This is my intuition..._  
    \* A very few...  
    _vs._  
    &rarr; The very few...

- mitigators:
    1. work with determiners: `almost`, `nearly`
    1. work with predicates but not determiners: `sort of`, `kind of`, `possibly`, `maybe`, `perhaps`
    1. auxiliaries (= modals)
  - second 2 here may just be getting into alternate hedge territory (see below)
- superlatives and comparatives (see below)
- need to exclude question answering `no`'s: _No, [explanation]_
- `ADV ADV ADJ` cases (2+ adverbs) need to be considered: both adverbs may need to be captured for accurate representation of the relevant phenomena

---

## Ideas

### tasks?

- [x] update tabulate script: merge `pat_debug.ipynb` code with `tabulateHits.py`
- [ ] **exclude `a few` and `the few`** (allow `(the) very few`? )
- [ ] restrict allowances on "relay" action
  - [ ] dependency relation label
  - [ ] part of speech tag
- [ ] look at the odd cases (`hits/...look-into-these.csv`)
- [ ] fix `without` cases:
  - may not be able to be lumped in with the others
  - does not work with the alternate structure for `nor` above either.
- [ ] assess restriction cases
  - [ ] look at few_sample for how to structure restriction pattern  
      &rarr; <sub>S</sub> [<sub>NP</sub> `few` ADV ADJ NOUN ] [<sub>VP</sub> ... ] ]
      (use `quickviewHits.py`)
- [ ] deal with conjunction cases?

---

### "maybe"s

- [ ] add catch for additional adverbs (post-search processing? or in search pattherns?)
- [ ] Create new categorization scheme for patterns?
- [ ] create new fields/info categories for sentence text split at key points: e.g. `pre-NEG`, `post-NEG`, `NEG-to-ADV`, `post-ADJ` ...
- [ ] specify permitted (or prohibited) dependency labels and/or xpos values for "relayed" negation cases.
- [ ] mark prenominal vs. predicate adjectives
- [ ] mark adjunct clauses?? (Is this possible?)
- [ ] change csv file to pickles and make script to few selection of pickle?

---

### Thought connections
......

negation is used in formal languages to include/cover "undefined" cases, e.g. grew pattern specifications with without clauses and "not" definitions

---

could extended mitigators, i.e. cases with modal adverbs and auxiliary verbs, serve as a categorization metric? That is, if these cases are taken to be hedging cases, would that imply that any negated scalars are also likely hedging uses?

---

Having NPI in subject of NR construction does not prevent "negative quality" from reaching (lower) predicate (e.g. _I don't think anyone has been here in years._)

---

Maybe superlative and comparative forms are just a (the most? one of the most?) basic scalar operation. Superlatives are clearly just elemental maximizers, but comparatives differ from intensifiers, minimizers, and maximizers in the sense that they indicate incremental shifts/relative positions, rather than fixed positions. Intensifiers also indicate relative scale positions, but the comparison point in those cases is contextually defined in an implicit sense than an explicit sense. To say something is "extremely expensive" is allowed in a context where no other entity's expense point has been referenced--we just fill in our understanding of what is in the "normal" range of cost. This implicit threshold/range can be tailored to fit the context (i.e. what kind of item are we considering? houses are much more expensive than coats), but we don't have to actually find a specific entity or group of entities to compare the costs of. If we say something is "more expensive" (or "less expensive") though, we need to be able to find something relevant in the context, either specifically introduced item(s), or vaguely referenced items, or a set of items that we can pull from the context via accomodation.

Consider the following:

    A: I heard your remodeling project is finished! How're you liking your new kitchen?

    B: Oh, it's really great! I finally have enough counter space! It's been really helpful because I've been doing more cooking recently--I'm trying this meal subscription service. 
    >>> It's more expensive, but it's so convenient and I've been learning new techniques I'd've never tried on my own.

In this case, the hearer would have to fill in a comparison point, but that's not hard to do since there are relevant options: It could easily be _"more expensive than not using a subsciption service"_ but it could also be _"more expensive than other meal subscription services"_.

Now let's compare to other possible forms the speaker could have uttered:

    ... It's extremely expensive, but totally worth it for the convenience and variety. 

This one feels a bit odd, since there is a social pressure to not be financially responsible. Saying you're buying something that you yourself label as being in the "extreme cost range" almost requires that a "redeeming quality" be offered as a follow up. The options below are more natural to my ears.

    ... It's not cheap, but totally worth it for the convenience and variety. 
    ... It's (somewhat) expensive, but totally worth it for the convenience and variety.

---

## Corpus parsing info

### Links

[Universal Dependencies Overview](https://direct-mit-edu.proxy.library.cornell.edu/coli/article/47/2/255/98516/Universal-Dependencies)

[ConLL-U online tree viewer](https://universaldependencies.org/conllu_viewer.html)

[CoNLL-U online parse viewer](https://urd2.let.rug.nl/~kleiweg/conllu/)

[UD online manual](https://universaldependencies.org/)

UD github: 
  - [docs dir](https://github.com/UniversalDependencies/docs)
  - [tools dir](https://github.com/UniversalDependencies/tools)
  - [tools readme](https://github.com/UniversalDependencies/docs/blob/pages-source/tools.md)
  - [dependencies](https://github.com/UniversalDependencies/docs/tree/pages-source/_u-dep)

### Notes

- superlatives & comparatives:
  - adj: `JJR`, `JJS`
  - adv: `RBR`, `RBS`
- subject match causes problems for relative clause versus matrix clause cases (bc subject is different)
- "neg" relation labels:
  - `neg`: regular
  - `advmod`: no less bright
  - `dep`: no less important
- not all "relay" types are equally permissible: need to restrict (see above)
  - `dep` may be bad across the board for this
- POS tagging in corpora is not 100% accurate; some nouns tagged as adj and adj tagged as verbs
- new generalized patterns catch prenominal cases
- `without` does not have the same dependencies/structural configuration in corpus tagging/parsing

---

## `few` reconnaissance

The following pattern might work...
might be able to be relaxed to use with other negs?

    pattern { 
        ADJ [xpos=JJ|JJR|JJS]; 
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;
        NEG [lemma="few"];  
        relay: ADJ -> S; 
        neg: S -> NEG;
        %neg: NEG -> ADJ;
        NEG << ADV; 
    }

    without {
        S -[det|poss]-> det; 
        S -[amod]-> NEG; 
        %TEMP [lemma="next"|"last"|"past"|"following"|"first"|"final"|"previous"]; 
        %S -[amod]-> TEMP
    }

The inclusion of the specific adverbs in the without clause definitely lets in things that should not be there.


`few` modifiers:

| polarity | a/the _ adverbs | bare adverbs |
| :------- | :-------------- | :----------- |
| neg | select, paltry, _very?_, | very,  |
| pos | dedicated, | |
---

preceding determiners have to have dependency relations with `few` to count

    [nyt_eng_19980512_0385_14]
    "a" DT          -[det]->        "company" NN
    "company" NN    -[appos]->      "Inc." NNP
    "few" JJ        -[amod]->       "people" NNS

Text:
_MCI Communications Corp. is in the process of being acquired for $ 37 billion by Worldcom Inc. , a company few people who work somewhere other than Wall Street had even heard of a few years ago_

---
what to do with `only a very few`?
  
Text: _only a very few are chosen to join the president in a huge underground vault_

    "a"     DT    -[det]->        "few" JJ
    "very"  RB    -[advmod]->     "few" JJ
    "few"   JJ    -[nsubjpass]->  "chosen" VBN  

---

`few` seems to operate differently when preceding a unit of time

- a busy few months
- a difficult few weeks
- the past few years

---

I have difficulty with `a very few` in a lot of cases, but `only a very few` or `one of a very few` seem much better than, e.g., `a very few people can say they have swum the English channel`. Why is this? This last example seems bad to me because it's like the polarity interpretations of "a few" and "very few" are conflicting with each other... Is it a scope thing fundamentally?

ceiling versus floor?
a small number vs. the smallest number
redefine scale s.t.

    0% ~ [small number] <|| <--- range ---> ||> [large number] ~ 100%

    [a [[very few] [people]] ] vs. [[[a very] [few people]]]

- She is one of a very few who can say that. 
- "Shutter Island became one of the few movies to ever flat-out fool me" (nyt_eng_20100217_0107_42)

- There are a very _few_ people who can say that.
- ~ There is a very _small group/number of_ people who can say that.
- There are only a very few people who can say that.
- There are very few people who can say that.

- Only a very few people can say that. (~ Only a very _small group of_ people can say that.)
- Only a very few people who sculpt daily can say that.
- A very few people who sculpt daily can say that. 
- A very few people can say that.

- Very few people (who sculpt daily) can say that. 

Do certain syntactic positions prevent or encourage certain scopes?

In object position, and these mean the same thing to me, excluding for minute differences in how small the number indicated is:

 &rarr; _`few` as noun? with essentially an elided `of` clause?---Second parse option would cause number mismatch since adjective doesn't change number and `couple` as an adjective is an entirely different meaning. E.g. 'couple ideas' as a stand-alone sounds like a matchmaker brainstorming_

    Jo had a few ideas. 
      [had [[a few] ideas]] ... [had ^[a [few ideas]]]
    Jo had a couple ideas. 
      [had [[a couple] ideas]] ... [had ^[a ?[couple ideas]]]
    ^ number mismatch
    ? different meaning

    **Jo had a some ideas. 
      [had [*[a some] ideas]] ... **[had `[a [some ideas]]] 
    ` type mismatch

    ?Jo had a handful (of) ideas. (maybe works? better with "of")

No alternate scope option in these cases, but these mean different things to me (few case: _Jo had a smaller number of ideas than what may be wanted/expected_.):

&rarr; _`few` as quantifier? or as adjective? As a noun, `few` requires a determiner (count, not mass). The type must be different in this case._

    Jo had some ideas. 
      [had [some [ideas]]
    Jo had some.
    Jo had few ideas.
      [had [few [ideas]]]
    Jo had few.

    ** Jo had couple ideas.
      ** [had [couple [ideas]]]
      - this must be parsed as the "matchmaking" type reading (or similar) where couple is an adj

Insert `of`? _forces noun interpretation of `few` (and `couple`)?

    Jo had a few of them. 
      [had [a [few [of them]]]] ... [had [[a few] [of them]]]
    Jo had a few of ideas. ? more marked I think? why??
    Jo had a couple of ideas.
      [had [a [couple [of ideas]]]] ... [had [[a couple]  [of ideas]]]

when you add `very`: _`very` can be an adjective able to modify nouns, but it selects for nouns which are inherently on a scalar endpoint of which have defined antonyms--middling things don't work. [Merriam-Webseter entry for `very`](https://www.merriam-webster.com/dictionary/very). Therefore, the insertion of `very` breaking the sentence indicates the part of speech it would be modifying has either the wrong semantic properties (midpoint scalar) or is the wrong part of speech_

    **Jo had very some ideas. 
        [had [[very some] ideas]]    
    Jo had very few ideas. 
      [had [[very few] ideas]]

    **Jo had very some. 
    Jo had very few. 

    *Jo had a very couple ideas. 
    ?Jo had a very few ideas. 
      [a [[very_adv few_adj] ideas_n]] -- number mismatch of singular det with plural count NP [... ideas]
      [ a[[very_adj few_n ] ideas_n]] --with covert of??

<!-- Is this^^ a case of adv-adj-noun or adj-nn? The cases above show that when there is a determiner, the few-as-adj parse of very should break due to number mismatch. That suggests this is the more marked usage of `very` as an adj indicating 'in truth'/'actual'/'real' -->
    *Jo had a very few of ideas.
    *Jo had a very few of them. 
    *Jo had a very couple of ideas. 

    *Jo had (very) few of ideas. -- breaks bc "of" forces noun and few-noun is count and cannot be bare?
    *Jo had some of ideas. -- breaks bc "of" needs an explicit (grouping/container?) noun? not anaphoric reference? 
      -> *Jo had them of ideas/things/items/etc.

But then through in `only` or `just`: _... who knows?_

    Jo had only a very few ideas. 
    Jo only had a very few ideas. 
    Jo had just a few ideas. 
    Jo just had a few ideas. 
    Jo merely had a few ideas.
    ? Jo had--merely a few--ideas.

As subject:

    A few _ideas occurred to me._ 
    Few _ideas occurred to me._ 
    Very few _ideas occurred to me. _
    Only a few _ideas occurred to me. _
    A very few _ideas occurred to me._ 
    Only a very few _ideas occurred to me._
