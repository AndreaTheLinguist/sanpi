pattern { 
    EVERY [lemma="every"];
    S [xpos="NN"]; 
    e1: S -[det]-> EVERY;
    V [lemma="be"];
    ADJ [xpos="JJ"]; 
    e2: ADJ -[cop]-> V; 
    e3: ADJ -[nsubj]-> S;
}