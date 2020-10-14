pattern {
  V [lemma="be"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];    
  e1: ADJ -[cop]-> V;
  e3: ADJ -[advmod]-> ADV;
  V < ADV;
  ADV < ADJ;
}
