# pos-quant


## `either` subj det

- positive subject
- existential (of set with cardinality of 2)
- Determiner/Quantifier `either NN`
- *either restaurant is fairly good*

```js
pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma="either"]; 
  S [];
  det: S -[det]-> N; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```

## `either` subj NP

- positive subject
- existential (of set with cardinality of 2)
- NN `either` with optional `of` phrase
- *either's totally amazing*
- *either of the boys is super excited*

```js
pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma=either"]; 
  sub: ADJ -[nsubj|nsubjpass]-> N;
  N << BE
}
```

## `some` subj det

- positive subject
- existential
- Determiner/Quantifier `some NN`
- *some restaurants are fairly good*
- _Some restaurants don't have any budget options_
- _Some man was super upset._
- _\* some restarants have any budget options_
- ??? Are these degraded??
  - is there an interaction with number here? 
    - _No restaurants have any budget options._
    - _There are no restaurants that have any budget options._
    - _There do not exist restaurants that have any budget options._
    - _There does not exist a restaurant that has any budget options._
  - Is it just *any* that's weird? *ever* seems better...
    - _No restaurant has ever served the grass soup of my childhood._
    - _There are no restaurants that have ever served the grass soup of my childhood._
    - _There do not exist restaurants that have ever served grass soup._
    - _There does not exist a restauarant that has ever served grass soup._

```js
pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  mod: ADJ -[advmod]-> ADV;
  ADV < ADJ;
  B [lemma="be"];
  Q [lemma="some"]; 
  ADJ -[cop]-> B;
  ADJ -[nsubj]-> Q
}
```

## `some` subj NP

- positive subject
- existential quantifier
- `some` as subject (anaphor) with optional `of` phrase
- *some are totally amazing*
- *some of the boys are super excited*

```js
pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  mod: ADJ -[advmod]-> ADV;
  ADV < ADJ;
  B [lemma="be"];
  Q [lemma="some"]; 
  ADJ -[cop]-> B;
  ADJ -[nsubj|nsubjpass]-> Q
}
```
