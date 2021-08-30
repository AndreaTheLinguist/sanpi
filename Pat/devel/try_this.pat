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