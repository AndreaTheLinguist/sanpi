pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [xpos=re"RB.?"]; 
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}

% will match e.g. `not uninteresting`
% ! restricts the `xpos` of the ADV node to "RB*" forms only, 
% instead of merely relying on `advmod` dependency relationship