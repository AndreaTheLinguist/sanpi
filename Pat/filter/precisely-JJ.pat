pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma="precisely"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}
