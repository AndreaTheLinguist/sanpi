pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma="immediately"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}