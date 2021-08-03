# Neg Mit

- This document describes `grew-match` patterns for mitigated negation contexts. 
  - The mitigated negation can be in any position (i.e. subject N, subject D, predicate Adv, etc.). 
  - mainly mitigating adverbs (e.g. `almost`, `nearly`, ...?) modifying the **negation** in a given context
  - but also inherent mitigation in the form of `few`
- **IMPORTANT** 

    __This does not refer to negated objects **with mitigation elsewhere**__: The migigation must be on the negation/negated element itself.
- *Note!*
    
    It's likely this mitgating of negation can __only__ occur with negated existentials. This is because negated universals do not have a set point of reference (i.e. they are already "ambiguous") and thus adding a mitigator to the negation---and thereby increasing the acceptable margin around the indicated threshold---is nonsensical (because there *is no* defined threshold to extend the accuracy margin around). 

## `few` det of subj

- mitigated existential negation
- `few` determiner
- **need to disambiguate the *very few* cases from the *a few* cases**

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `few` subj

- mitigated existential negation
- `few` as elided subject
- **need to disambiguate the *very few* cases from the *a few* cases**

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `almost nobody` subj

- `almost nobody`
- *Almost nobody was entirely pleased.*
- ought to work but currently gets no hits in sample files

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `almost no one` subj

- `almost no one`
- *Almost no one was entirely pleased.*
- ought to work but currently gets no hits in sample files
- currently `nc2.pat`

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `almost no` det of subj

- `almost no` N
- *Almost no member was entirely thrilled.*
- ought to work but currently gets no hits in sample files

```js
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

## `almost none` subj

- `almost none` with optional `of` PP

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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
