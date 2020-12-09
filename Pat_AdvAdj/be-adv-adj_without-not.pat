pattern {
  ADV [xpos=RB, lemma <> "not"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  []; 
  subj: ADJ -[nsubj]-> S;
  S << BE
}

without {
  NEG [lemma = "not"];
  ADJ -[neg]-> NEG;
}