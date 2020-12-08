# bigrams
all instances of Adv Adj bigrams excluding 'not' as adverb
```
pattern { 
  ADV [xpos=RB];
  ADJ [xpos=JJ]; 
  ADV < ADJ; 
  e: ADJ -[advmod]-> ADV; 
  ADV.lemma <> "not"
}
```

# bigrams minus not
```
pattern { 
  ADV [xpos=RB];
  ADJ [xpos=JJ]; 
  ADV < ADJ; 
  e: ADJ -[advmod]-> ADV; 
  ADV.lemma <> "not"
}

without{
  NOT[lemma="not"];
  e1: V -[advmod]-> NOT;
}
```

# be adv adj excluding not and other negative adverbs
This pattern specifies a empty subject, a verb of any form with lemma 'be' (i.e. any inflection), an adverb excluding those of negative quality specified, and a predicate adjective. 
The subject must precede the 'be' form (no inverting/questions), the be-form must be the adjective's copula, and the adverb must modify the adjective and immediately precede it (excludes more "sentential" adverbs, but also adverbs that can come after the adj, as in "He's not happy exactly.") It also excludes any other additional negative adverbs that might be modifying the adjective (It does *not* exclude negative adverbs from modifying the original adverb immediately preceding the adjective.)
```
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  BE.xpos = re"VB.";
  ADV < ADJ;
  e1: ADJ -[advmod]-> ADV;
  e2: ADJ -[cop]-> BE;
  S  []; 
  e3: ADJ -[nsubj]-> S;
  S << BE
}

without {
  NEG [lemma = "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  e4: ADJ -[advmod]-> NEG;
}
```

# be adv adj excluding only not adv (as collocate adv and also preceding)
file name: be-adv-adj_without-not.pat
```
pattern {
  ADV [xpos=RB, lemma <> "not"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  BE.xpos = re"VB.";
  ADV < ADJ;
  e1: ADJ -[advmod]-> ADV;
  e2: ADJ -[cop]-> BE;
  S  []; 
  e3: ADJ -[nsubj]-> S;
  S << BE
}

without {
  NEG [lemma = "not"];
  e4: ADJ -[advmod]-> NEG;
}
```

# be not adv adj
be-adv-adj_with-not.pat
```
pattern {
  ADV [xpos=RB, lemma <> "not"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  BE.xpos = re"VB.";
  ADV < ADJ;
  e1: ADJ -[advmod]-> ADV;
  e2: ADJ -[cop]-> BE;
  S  []; 
  e3: ADJ -[nsubj]-> S;
  S << BE;
  NEG [lemma = "not"];
  e4: ADJ -[advmod]-> NEG;
}
```


# neg -- n1? 
```
pattern {
    V [lemma="be"];
    NOT [lemma="not"]; 
    R [upos="ADV"];  
    A [upos="ADJ"]; 
    e1: A -[cop]-> V;
    e2: A -[advmod]-> R; 
    e3: A -[advmod]-> NOT;
}
```

# neg_be
```
pattern {
  V [lemma="be"];
  NOT [lemma="not"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];    
  e1: ADJ -[cop]-> V;
  e2: ADJ -[neg]-> NOT;
  e3: ADJ -[advmod]-> ADV;
  V < NOT;
  NOT < ADV;
  ADV < ADJ;
}
```

# none_pred
```
pattern {
  NONE [lemma="none"];
  V [lemma="be"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];
  e1: ADJ -[cop]-> V;
  e3: ADJ -[advmod]-> ADV;
  NONE << V;
  V < ADV;
  ADV < ADJ;
  ADV.lemma <> "not"
}
```

# noNN-pred
```
pattern {
  NO [lemma="no"];
  S [xpos="NN"];
  e1: S -[det]-> NO;
  V [lemma="be"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];
  e2: ADJ -[cop]-> V;
  e3: ADJ -[advmod]-> ADV;
  e4: ADJ -[nsubj]-> S;
  V < ADV;
  ADV < ADJ;
  ADV.lemma <> "not"
}
```


# every_predicate: no adv
```
pattern {
  EVERY [lemma="every"];
  S [xpos="NN"];
  e1: S -[det]-> EVERY;
  V [lemma="be"];
  ADJ [xpos="JJ"];
  e2: ADJ -[cop]-> V;
  e3: ADJ -[nsubj]-> S;
}
```

# every_predicate: with adv 
but dets a lot of sentential adv, like _meanwhile_ or _hopefully_
```
pattern {
  EVERY [lemma="every"];
  S [xpos="NN"];
  e1: S -[det]-> EVERY;
  ADV[xpos="RB"];
  V [lemma="be"];
  ADJ [xpos="JJ"];
  e2: ADJ -[cop]-> V;
  e3: ADJ -[nsubj]-> S;
  e4: ADJ -[advmod]-> ADV;
}
```

# every_predicate: with adv excluding sentential

```
pattern {
  EVERY [lemma="every"];
  S [xpos="NN"];
  e1: S -[det]-> EVERY;
  ADV[xpos="RB"];
  V [lemma="be"];
  ADJ [xpos="JJ"];
  e2: ADJ -[cop]-> V;
  e3: ADJ -[nsubj]-> S;
  e4: ADJ -[advmod]-> ADV;
  V << ADV;
}
```

# p1.pat
```
pattern {
  V [lemma="be"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];
  e1: ADJ -[cop]-> V;
  e3: ADJ -[advmod]-> ADV;
  V < ADV;
  ADV < ADJ;
}
```

# pos_be_x_not
```
pattern{
    V[lemma="be"];
    IF [lemma="if"];
    ADV [xpos="RB"];
    ADJ [xpos="JJ"];
    e1: ADJ -[cop]-> V;
    e2: ADJ -[mark]-> IF;
    e3: ADJ -[advmod]-> ADV; 
    IF << V;
    V <ADV; 
    ADV < ADJ;
    ADV.lemma <> "not";}
```

# not-verb-either
_**NOTE** needs additional elements to include neg raising_
```
pattern{
  EITHER[lemma="either"];
  NOT[lemma="not"];
  V[xpos="VB"];
  e1: V -[advmod]-> NOT;
  e2: V -[advmod]-> EITHER;
  NOT << V;
  V << EITHER  
}
```

# positive context with either
_**NOTE** This needs additional constraints to deal with bridging verbs_
```
pattern{
  EITHER[lemma="either"];
  V[xpos="VB"];
  e2: V -[advmod]-> EITHER;
  V << EITHER  
}

without{
  NOT[lemma="not"];
  e1: V -[advmod]-> NOT;
}
```

# all_be-pred
```
pattern { 
    QNT [lemma="all"];
    S [xpos="NN"]; 
    e1: S -[det]-> QNT;
    V [lemma="be"];
    ADJ [xpos="JJ"]; 
    e2: ADJ -[cop]-> V; 
    e3: ADJ -[nsubj]-> S;
}
```

# every_be-pred
```
pattern { 
    EVERY [lemma="every"];
    S [xpos="NN"]; 
    e1: S -[det]-> EVERY;
    V [lemma="be"];
    ADJ [xpos="JJ"]; 
    e2: ADJ -[cop]-> V; 
    e3: ADJ -[nsubj]-> S;
}
```

# every_restrict
```
pattern { 
    EVERY [lemma="every"];
    ADV [xpos=”RB”];
    ADJ [xpos=”JJ”];
    N [xpos="NN"]; 
    e1: N -[det]-> EVERY;
    e2: N -[amod]-> ADJ;
    e3: ADJ -[advmod]-> ADV;
    }
```

# if-ante_Pred
```
pattern {
  V [lemma="be"];
  IF [lemma="if"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];    
  e1: ADJ -[cop]-> V;
  e2: ADJ -[mark]-> IF;
  e3: ADJ -[advmod]-> ADV;
  IF << V;
  V < ADV;
  ADV < ADJ;
}
```

# if-ante_x_not
```
pattern{
  V [lemma="be"];
  IF [lemma="if"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];
  e1: ADJ -[cop]-> V;
  e2: ADJ -[mark]-> IF; 
  e3: ADJ -[advmod]-> ADV;
  IF << V; 
  V < ADV; 
  ADV < ADJ; 
  ADV.lemma <> "not";
}
```

#

