pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  mod: ADJ -[advmod]-> ADV;
  ADV < ADJ;
  B [lemma="be"];
  ADJ -[cop]-> B;
  Q [lemma="some"];
  S []; 
  S -[det]-> Q;
  B -[nsubj|nsubjpass]-> S
}