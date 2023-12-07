pattern { 
    ADJ [xpos=re"JJ.?"]; 
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}

% will match e.g. `not uninteresting`
