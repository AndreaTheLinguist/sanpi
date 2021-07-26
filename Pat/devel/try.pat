pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma="not"]; 
  S [lemma="one"]; 
  N < S; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE    
}