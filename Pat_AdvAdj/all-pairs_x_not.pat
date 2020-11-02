pattern { 
  ADV [xpos=RB];
  ADJ [xpos=JJ]; 
  ADV < ADJ; 
  e: ADJ -[advmod]-> ADV; 
  ADV.lemma <> "not"
}