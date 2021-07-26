pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  BE [lemma="be"];
  cop: ADJ -[cop]-> BE;
  S  []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}