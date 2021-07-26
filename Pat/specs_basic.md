# Basic

- can have bulleted list here for general info on pattern category

## `ADV ADJ` prefilter

- this would be used to:
  - create corpora subsets:
    - sentences without adverbial modification of an adjective would be ignored
    - if run once on all corpus chunks, could create a smaller sample to do full searches on
    - would need to consider if preceding and following sentences would need to be accessed for evaluation of interpretation
  - get a more inclusive count of adj adv collocations
    - this may not be wanted if none of the contexts would consider pre-nominal APs

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
}
```

## `be ADV ADJ` predicate adj

- adverbial modification of adjective
- adverb restricted to immediately preceding adjective
    to prevent sentential scopes
- must have at least 1 adverb that isn't inherently negative. Excludes (lemmas):
  - not
  - never
  - scarcely
  - hardly
  - barely
  - rarely
  - seldom
- **Note:** _will need to make sure this doesn't return things with the wrong relationships, but should capture the "with(out) being" cases_
  
```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  BE [lemma="be"];
  cop: ADJ -[cop]-> BE;
}
```

## `S be ADV ADJ` subj control

- same as preceding, but requires subject as an insurance of relationship
  
```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  BE [lemma="be"];
  cop: ADJ -[cop]-> BE;
  S  []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```