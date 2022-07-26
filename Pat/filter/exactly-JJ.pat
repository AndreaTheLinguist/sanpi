pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma="exactly"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}