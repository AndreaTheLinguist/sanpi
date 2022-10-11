pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma="entirely"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}
