pattern {
  NO [lemma="no"];
  S [xpos="NN"];
  e1: S -[det]-> NO;
  V [lemma="be"];
  ADV [xpos="RB"];
  ADJ [xpos="JJ"];
  e2: ADJ -[cop]-> V;
  e3: ADJ -[advmod]-> ADV;
  e4: ADJ -[nsubj]-> S;
  V < ADV;
  ADV < ADJ;
  ADV.lemma <> "not"
}
