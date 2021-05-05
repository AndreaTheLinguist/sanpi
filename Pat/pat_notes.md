# Grew-match Patterns

## Base Context: c0

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
  sub: ADJ -[nsubj]-> S;
  S << BE
}
```

## Context Restrictions 

### Context 1: c1

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
  subj: ADJ -[nsubj]-> S;
  S << BE;
  NOT [lemma = "not"];
  neg: ADJ -[neg]-> NOT;
}
```

### Context 2: c2

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
  subj: ADJ -[nsubj]-> NS;
  NS << BE;
}
```

### Context 3: c3

- negative subject 
- negated existential
- DP: `no one`
- *No one was extremely happy*

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
  sub: ADJ -[nsubj]-> S;
  S << BE
}
```

### Context 4: c4

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
  sub: ADJ -[nsubj]-> S;
  S << BE
}
```

### Context 5: c5

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
  sub: ADJ -[nsubj]-> S;
  S << BE
}
```

### Context 6: c6

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
  sub: ADJ -[nsubj]-> S;
  S << BE    
}
```

### Context 7: c7

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
  sub: ADJ -[nsubj]-> N;
  N << BE    
}
```

### Context 8: c8

- negated (emphatic?) subject
- negated existential
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
  sub: ADJ -[nsubj]-> S;
  S << BE; 
  N [lemma="not"]; 
  O [lemma="one"]; 
  O -[neg|quantmod]-> N; 
  num: S -[nummod]-> O
}
```

### Context 9: c9

- negated (emphatic?) subject
- negated existential
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
  neg: S -[neg]-> N; 
  sub: ADJ -[nsubj]-> S;
  S << BE    
}
```


### Context 10: c10

- negative adverb
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
  subj: ADJ -[nsubj]-> S;
  S << BE;
  N [lemma = "never"];
  neg: ADJ -[neg]-> N;
}
```

### Context 11: c11

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
  sub: ADJ -[nsubj]-> S;
  S << BE
}
```

### Context 12: c12

- mitigated existential negation
- `few` as elided subject

```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  FEW [lemma="few"];
  sub: ADJ -[nsubj]-> FEW;
  FEW << BE
}
```

### Context 13: c13

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

### Context ?? 

- `almost` + any of the negated existentials 
  - `almost` will have `advmod` dependency
  - `neg-quant -[advmod]-> almost`

- neg-raising interveners
  - need to check on whether these cases are included by default in c0 or if the delineation of the copula and subject, etc. prevent it? 

- mitigated negative adverbs: scarcely, rarely, barely, hardly, etc.

- negated universal quantifiers:
  - not all, not every, not everyone

