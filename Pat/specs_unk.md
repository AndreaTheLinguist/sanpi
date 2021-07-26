# Unknown Polarity

## `everyone` subj

- `everyone is ADV ADJ` subject position
- Positive context
- does not licencse NPIs
  - **Everyone has any money.*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="everyone"]; 
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
```

## `everybody` subj

- `everybody is ADV ADJ` subject position
- Positive context
- does not licencse NPIs
  - **Everybody has any money.*

```js
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="everybody"]; 
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
```

## `every` det of subj

- `every` as determinter of subj noun
- positive context
- does not license NPIs
- **Every student has any money.*

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma <> "one"]; 
  E [lemma="every"];
  det: S -[det]-> E;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```