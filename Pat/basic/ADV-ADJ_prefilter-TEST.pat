pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
}