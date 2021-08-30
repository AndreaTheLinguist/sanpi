pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  mod: ADJ -[advmod]-> ADV;
  ADV < ADJ;
  B [lemma="be"];
  ADJ -[cop]-> B;
  QD [lemma="either"];
  S []; 
  S -[det]-> QD;
  B -[nsubj|nsubjpass]-> S
}