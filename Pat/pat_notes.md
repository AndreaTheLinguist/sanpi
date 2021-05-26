# Grew-match Patterns

## Base Context: base

- 'be' lemma
- predicate adjective
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

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

## VP Context Restrictions 

### Context `not` VP adv: nc0

- negation of predicate adjective
- *John is not extremely happy*
- *John wasn't extremely happy*

```
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  []; 
  subj: ADJ -[nsubj|nsubjpass]-> S;
  S << BE;
  NOT [lemma = "not"];
  neg: ADJ -[neg]-> NOT;
}
```

### Context `never` VP adv

- negative adverb on VP
- `never`
- *John was never extremely happy*

```
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  []; 
  subj: ADJ -[nsubj|nsubjpass]-> S;
  S << BE;
  N [lemma = "never"];
  neg: ADJ -[neg]-> N;
}
```

### Context `doubt` matrix VP

## Subject Restriction Contexts

### Context `nobody` subject: 

- negative subject 
- negated existential
- NN: `nobody`
- *Nobody's extremely happy*

```
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="nobody"]; 
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
```

### Context `no one` subject: nc1

- negative subject 
- negated existential
- DP: `no one`
- *No one was extremely happy*
- more frequent than `nobody`

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma="one"]; 
  N [lemma="no"];
  det: S -[det]-> N;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

### Context `no` determinter on subject N

- negative subject 
- negated existential
- unspecified subject `NOUN` with determiner `no`
- *No teacher was extremely happy*
- ? *No students were extremely happy*

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma <> "one"]; 
  N [lemma="no"];
  det: S -[det]-> N;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

### Context `none` subject

- negative subject
- negated existential
- Pronoun/NN `none` with optional `of` phrase
- *None were extremely happy*
- *None of the students were extremely happy*

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma="none"]; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

### Context `neither` determiner on subject

- negative subject
- negated existential (of set with cardinality of 2)
- Determiner/Quantifier `neither NN`
- *Neither restaurant was incredibly good*

```
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma="neither"]; 
  S [];
  det: S -[det]-> N; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE    
}
```

### Context `neither` subject

- negative subject
- negated existential (of set with cardinality of 2)
- NN `neither` with optional `of` phrase
- *Neither's totally amazing*
- *Neither of the boys is super excited*

```
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma="neither"]; 
  sub: ADJ -[nsubj|nsubjpass]-> N;
  N << BE    
}
```

### Context `not one` determiner on subject

- negated subject
- negated existential
- emphatic?
- `not one` determiner
- ? *Not one option was exactly good.*
- **no hits found while debugging**

```
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE; 
  N [lemma="not"]; 
  O [lemma="one"]; 
  N < O; 
  S -> O
}
```

### Context `not a single` determiner on subject

- negated subject
- negated existential
- emphatic?
- `not a single` determiner
- ? *Not a single option was super enticing.*
- **no hits found while debugging**

```
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE; 
  N [lemma="not"]; 
  A [lemma="a"];
  O [lemma="single"]; 
  N < A;
  A < O; 
  S -> O
}
```

### Context `not one` subject

- negated subject
- negated existential
- emphatic? NPI flavor on its own...
- `not one` NP
- ? *Not one was exactly good.*
- **no hits found while debugging**

```
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma="not"]; 
  S [lemma="one"]; 
  N < S; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE    
}
```

### Context `nothing` subject

- `nothing` subject
- existential negation
- *Nothing was super cheap.*
- *Nothing's entirely certain.*

```
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="nothing"]; 
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
```


## Mitigated Negated Existentials

### Context `few` determiner on subject

- mitigated existential negation
- `few` determiner 
- **need to disambiguate the *very few* cases from the *a few* cases**

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S []; 
  FEW [lemma="few"];
  S -[amod]-> FEW;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

### Context `few` subject

- mitigated existential negation
- `few` as elided subject
- **need to disambiguate the *very few* cases from the *a few* cases**

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  FEW [lemma="few"];
  sub: ADJ -[nsubj|nsubjpass]-> FEW;
  FEW << BE
}
```

### Context `almost nobody` subject

- `almost nobody`
- *Almost nobody was entirely pleased.*
- ought to work but currently gets no hits in sample files

```
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="nobody"]; 
  A [lemma="almost"]; 
  A < NS;
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
```

### Context `almost no one` subject

- `almost no one`
- *Almost no one was entirely pleased.*
- ought to work but currently gets no hits in sample files

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma="one"]; 
  N [lemma="no"];
  det: S -[det]-> N;
  A [lemma="almost"];
  A < N;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

### Context `almost no` determiner on subject

- `almost no` N
- *Almost no member was entirely thrilled.*
- ought to work but currently gets no hits in sample files

```
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma <> "one"]; 
  N [lemma="no"];
  ALMOST [lemma="almost"];
  ALMOST < N;
  det: S -[det]-> N;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

### Context `almost none` subject

- `almost none` with optional `of` PP

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma="none"]; 
  ALMOST [lemma="almost"];
  ALMOST < S;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

## Other Context Restrictions: PP, ?

### Context `without being` PP

- `without being`
- semi-restrictive right now, but not catching things that should be excluded

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  W [lemma="without"];
  B [lemma="be"];
  advmod: ADJ -[advmod]-> ADV; 
  W < B; 
  ADJ -> B
}
```

## Notes and To do list

### ambiguity producing contexts
  - [x] almost nobody
  - [x] almost no one
  - [x] almost no NN
  - [x] almost none
  - [ ] almost never
  - [ ] almost not
  - [x] without being
  - [ ] scarcely any (~very few)
  - [ ] scarcely 
  - [ ] rarely
  - [ ] barely
  - [ ] hardly
  - [ ] seldom
  - [ ] doubt (essentially lexicalized neg-raising conext `not believe`)
  - [ ] deny? --> weak NPI only
  - [ ] prevent? --> weak NPI only
  - [ ] not think 
  - [ ] not believe 
  - [ ] not suppose 
  - [ ] not expect
  - [ ] not imagine
  - [ ] not suppose 
  - [ ] not look like
  - [ ] not seem (like, that)
  - [ ] not appear (that)
  - [ ] not likely (that)
  - [ ] not probable (that)
  - [ ] not want (inf-sub) to
  - [ ] not wish (inf-sub, for inf-sub) to
  - [ ] not wish that? **does this allow for neg-raising?**
  - [ ] not intend (inf-sub, for inf-sub) to
  - [ ] not plan (for inf-sub) to 


- `almost` + any of the negated existentials 
  - `almost` will have `advmod` dependency
  - `neg-quant -[advmod]-> almost`
  - actually, better to just use linear relationship, I think...
  - **also do `nearly`?**
  - `almost` context will be subset of more basic restriction, so should be peeled off first

- neg-raising interveners
  - need to check on whether these cases are included by default in c0 or if the delineation of the copula and subject, etc. prevent it? 
  - list from Horn Neg-Raising chapter in Oxford Handbook of Negation
    - believe, suppose, think
    - expect, imagine    
    - be likely, probable
    - seem, appear, look like
    - intend, choose, plan to
    - want, wish, 
    - suggest, advise

    - advisable, desirable
    - should, ought to, better
    - most
    - usually
  - *__neg raising can be used to hedge__. Scope ambiguity between stronger and weaker meanings, very like negation of scalar predicates, resulting in ambiguity that could be used strategically in context. Different from other kinds of scope ambiguities (e.g. PP attachment) because the available readings are not mutually exclusive. Rather, they have a subset relationship: the low scope reading indicates a subset of the possible worlds which are consistent with the high scope reading. This means that, like the negated universal quantifiers, there is an additional level of pragmatic ambiguity when the embedded clause has an inherent scalar middle ground. (__Has this been written about?__)*

  - Illustrations of Neg Raising/Non-blocking interveners
    - Embedded clause judgements
      - They don't have any money, either.
      - \*They have any money, either.  

    - I don't __ they have any money, either.
      - think
        - I don't think they have any money, either. 
          - [low] ~ I think that they have no money
          - [high] ~ It is not the case that I think they have money.
        - \*I think they have any money, either.
      - believe
        - I don't believe they have any money, either.
        - \*I believe they have any money, either.
      - suppose
        - I don't suppose they have any money, either. 
        - \*I suppose they have any money, either.
      - expect
        - I don't expect they have any money, either. 
        - \*I expect they have any money, either.
      - imagine
        - I don't imagine they have any money, either. 
        - \*I imagine they have any money, either.
    
    - It isn't __ (that) they have any money, either.
      - likely
        - It isn't likely they have any money, either.
        - \*It's likely they have any money (either).
      - probable
        - It isn't probable that they have any money, either.
        - \*It's probable they have any money (either).

    - It doesn't __ they have any money.
      - look like
        - It doesn't look like they have any money, either.
        - \*It looks like they have any money (either).
      - seem {like, that}
        - It doesn't seem ({like,that}) they have any money, either.
        - \*It looks like they have any money (either).
      - appear {that}
        - It doesn't appear (that) they have any money, either.
        - \*It appears (that) they have any money (either).
        - It appears (that) they have some money.

    - I didn't __ to give them any money (either)
      - want
        - I didn't want to give them any money, either.
        - \*I wanted to give them any money (either).
        - I wanted to give them ({the, some}) money, too. 
      - wish
        - I didn't wish to give them any money, either.
        - \*I wished to give them any money (either).
        - I wished to give them money. 
      - intend 
        - I didn't intend to give them any money, either. 
        - I intended to give them money. 
        - \*I intended to give them any money. 
      - plan 
        - I didn't plan to give them any money, either. 
        - I planned to give them money. 
        - I planned to give them some money, too.
        - \*I planned to give them any money (either).
      - choose
        - I didn't choose to give them any money, either. 
        - I chose to give them (some) money (too)
        - \*I chose to give them any money (either)

    - I don't __ (that) you give them any money (either)
      - advise
        - I don't advise that you give them any money, either. 
        - I advise that you give them money. 
        - I advise that you give them some money, too. 
        - *I advise that you give them any money, either.
      - suggest
        - I don't suggest that you give them any money, either. 
        - I suggest that you give them money. 
        - I suggest that you give them some money.
        - *I suggest that you give them any money.
      - recommend
        - I don't recommend that you give them any money, either. 
        - I recommend that you give them money. 
        - I recommend that you give them some money.
        - *I recommend that you give them any money.



- mitigated negative adverbs: scarcely, rarely, barely, hardly, etc.

- negated universal quantifiers:
  - *not all, not every, not everyone*

  - not all
    - [not all NP] Not all (of the X) were ADV ADJ
    - [not all DP] Not all X were ADV ADJ
    - [not all VP] They were not all ADV ADJ
      - **overlap** This should be caught in the not VP context description...

  - not every
    - [not every DP] Not every X was ADV ADJ
  
  - not everyone
    - Not everyone was ADV ADJ

- negative verbs
  - doubt --> strong and weak
    - I doubt they have any money, either.
    - I doubt they have the money, either. (is this worse than with *any*?)
    - \*I suspect they have any money.
  - prevent? --> weak only
    - I prevented them from getting any money.
    - \*I helped them get any money.
    - I didn't prevent them from getting the money, either.
    - \*I prevented them from getting the money, either.
  - deny? --> weak only
    - I denied having any money.
    - \*I acknowledged having any money.

    - \*I denied having the keys, either.
    - \*I acknowledged having the keys, either.

    - I didn't {acknowledge, deny} having the keys, either.


- what to do with conjoined predicates like this? 
  - _**Nothing is more unequivocally useless and irritating** than to listen to someone rattle off his Top 10 anything..._
  - currently only `useless` is recorded as ADJ
  - Is it possible to specify the context such that `irritating` is captured in an additional hit? 
  - Or would it be best to record the ADJ as conjoined `useless and irritating`? 


