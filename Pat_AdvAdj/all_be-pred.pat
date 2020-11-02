pattern { 
    QNT [lemma="all"];
    S [xpos="NN"]; 
    e1: S -[det]-> QNT;
    V [lemma="be"];
    ADJ [xpos="JJ"]; 
    e2: ADJ -[cop]-> V; 
    e3: ADJ -[nsubj]-> S;
}