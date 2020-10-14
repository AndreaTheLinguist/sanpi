pattern {
  NONE [lemma="none"];
  V [lemma="be"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];
  e1: ADJ -[cop]-> V;
  e3: ADJ -[advmod]-> ADV;
  NONE << V;
  V < ADV;
  ADV < ADJ;
  ADV.lemma <> "not"
}
