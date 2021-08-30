# Unknown Polarity

## `everyone` subj

- `everyone is ADV ADJ` subject position
- Positive context
- does not licencse NPIs
  - __\*__ *Everyone has any money.*

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
  - __\*__ *Everybody has any money.*

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
- __\*__ *Every student has any money.*

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

## `if` antecedent

- within if antecedent clause
- `If N BE ADV ADJ`:
  - *If Bill is incredibly smart, he will invest now.*
  - *If they were really interested, they would have replied.*
- **does** license weak NPIs
  - *If you have any ideas, I'd love to hear them.*
  - *If I ever go back to France, it won't be to Paris.*
- **does not** license strong NPIs
  - *If she is departing __at__ noon, she won't arrive before 2 pm.*
  - __\*__ *If she is departing __until__ noon, she won't arrive before 2 pm.*
  - *If she is departing __at__ noon, she will arrive after 2 pm.*
  - __\*__ *If she is departing __until__ noon, she will arrive after 2 pm.*  
vs.
  - *If she is**n't** departing __until__ noon, she won't arrive before 2 pm.*
  - _She is**n't** depart __until__ noon, so she will arrive after 2 pm._

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE; 

  IF [lemma="if"]; 
  ADJ -[mark|dep|prep|advmod]-> IF
}
```

## `if` consequent

- CP following `if` clause
- even weak NPIs are not licensed in the consequent.
- _If John is enrolled, then he is likely prepared._
- \* _If John is enrolled, then he is exactly prepared._
- _If John is enrolled, then he has some money._
- \* _If John is enrolled, then he has any money._

pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ];
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  [];
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE;

  IF [lemma="if"];
  ADJ -[mark|dep|prep|advmod]-> IF
}

## `before` clause

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE; 

  BEFORE [lemma="before"]; 
  ADJ -[mark|dep|prep|advmod]-> BEFORE
}
```
