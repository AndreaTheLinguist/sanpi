pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="nobody"]; 
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
