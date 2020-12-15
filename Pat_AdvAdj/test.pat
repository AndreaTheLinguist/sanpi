pattern{
	NO [lemma="no"];
	S [];
	B [lemma="be"];
    ADV [xpos=RB, lemma<>"not"];
    ADJ [xpos=JJ];
    ADJ -[cop]-> B;
    ADJ -[nsubj]-> S;
    ADJ -> ADV;
    ADV < ADJ;
    S << ADJ;
    S -[det]-> NO;
}
 
without{
	NOT [lemma="not"];
    ADJ -> NOT
}
