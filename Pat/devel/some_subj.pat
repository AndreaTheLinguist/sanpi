pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  mod: ADJ -[advmod]-> ADV;
  ADV < ADJ;
  B [lemma="be"];
  ADJ -[cop]-> B;
  QS [lemma="some"]; 
  B -[nsubj|nsubjpass]-> QS
}