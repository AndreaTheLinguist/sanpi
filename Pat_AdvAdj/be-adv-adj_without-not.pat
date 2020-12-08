pattern {
  ADV [xpos=RB, lemma <> "not"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  BE.xpos = re"VB.";
  ADV < ADJ;
  e1: ADJ -[advmod]-> ADV;
  e2: ADJ -[cop]-> BE;
  S  []; 
  e3: ADJ -[nsubj]-> S;
  S << BE
}

without {
  NEG [lemma = "not"];
  e4: ADJ -[advmod]-> NEG;
}