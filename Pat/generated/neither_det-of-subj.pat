pattern{
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  N [lemma="neither"]; 
  S [];
  det: S -[det]-> N; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
