pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  W [lemma="without"];
  B [lemma="be"];
  advmod: ADJ -[advmod]-> ADV; 
  W < B; 
  ADJ -> B
}
