pattern {
	V [lemma="be"];
	ADV [xpos="RB"];
	ADJ [xpos="JJ"];
	e1: ADJ -[cop]-> V;
	e2: ADJ -[advmod]-> ADV;
	V < ADV;
	ADV < ADJ;
	ADV.lemma <> "not"} 
