pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma="particularly"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}