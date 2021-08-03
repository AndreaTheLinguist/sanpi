# Neg Ext Subj

- This document describes `GREW-match` patterns for contexts that have the negation as part of the subject noun phrase. There are 2 formulations of this: 
  1. negative determiners on a noun/noun phrase
  2. inherently negative noun phrases
- *note:* Title heading of this file is used as subdirectory name for organization of generated pattern files.

## `nobody` subj NP

- negative subject
- negated existential
- NN: `nobody`
- *Nobody's extremely happy*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `no one` subj NP

- negative subject
- negated existential
- DP: `no one`
- *No one was extremely happy*
- more frequent than `nobody`
- currenty `nc1.pat`

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `no` subj det

- negative subject
- negated existential
- unspecified subject `NOUN` with determiner `no`
- *No teacher was extremely happy*
- ? *No students were extremely happy*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `none` subj NP

- negative subject
- negated existential
- Pronoun/NN `none` with optional `of` phrase
- *None were extremely happy*
- *None of the students were extremely happy*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `neither` subj det

- negative subject
- negated existential (of set with cardinality of 2)
- Determiner/Quantifier `neither NN`
- *Neither restaurant was incredibly good*

```js
pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `neither` subj NP

- negative subject
- negated existential (of set with cardinality of 2)
- NN `neither` with optional `of` phrase
- *Neither's totally amazing*
- *Neither of the boys is super excited*

```js
pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `not one` subj det

- negated subject
- negated existential
- emphatic?
- `not one` determiner
- ? *Not one option was exactly good.*
- **no hits found while debugging**

```js
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `not a single` subj det

- negated subject
- negated existential
- emphatic?
- `not a single` determiner
- ? *Not a single option was super enticing.*
- **no hits found while debugging**

```js
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `not one` subj NP

- negated subject
- negated existential
- emphatic? NPI flavor on its own...
- `not one` NP
- ? *Not one was exactly good.*
- **no hits found while debugging**

```js
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `nothing` subj NP

- `nothing` subject
- existential negation
- *Nothing was super cheap.*
- *Nothing's entirely certain.*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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
