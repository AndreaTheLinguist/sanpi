pattern {
  V [lemma="be"];
  IF [lemma="if"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];    
  e1: ADJ -[cop]-> V;
  e2: ADJ -[mark]-> IF;
  e3: ADJ -[advmod]-> ADV;
  IF << V;
  V < ADV;
  ADV < ADJ;
}
