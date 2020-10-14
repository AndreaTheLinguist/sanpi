pattern {
  V [lemma="be"];
  NOT [lemma="not"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];    
  e1: ADJ -[cop]-> V;
  e2: ADJ -[neg]-> NOT;
  e3: ADJ -[advmod]-> ADV;
}
