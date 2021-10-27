# Neg Ext NonSubj

## `not` VP adv

- negation of predicate adjective
- *John is not extremely happy*
- *John wasn't extremely happy*
- currently `nc0.pat`

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

---

## `never` VP adv

- negative adverb on VP
- `never`
- *John was never extremely happy*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

---

## `not` VP adv

- negation of predicate adjective
- *John is not extremely happy*
- *John wasn't extremely happy*
- currently `nc0.pat`

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

---

## `never` VP adv

- negative adverb on VP
- `never`
- *John was never extremely happy*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
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

---

## `without being` PP

- `without being`
- semi-restrictive right now, but not catching things that should be excluded
- currently `nc3.pat`

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  W [lemma="without"];
  B [lemma="be"];
  advmod: ADJ -[advmod]-> ADV; 
  W < B; 
  ADJ -> B
}
```