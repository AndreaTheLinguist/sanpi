pattern { 
    EVERY [lemma="every"];
    ADV [xpos=RB];
    ADJ [xpos=JJ];
    N [xpos=NN]; 
    e1: N -[det]-> EVERY;
    e2: N -[amod]-> ADJ;
    e3: ADJ -[advmod]-> ADV;
    }