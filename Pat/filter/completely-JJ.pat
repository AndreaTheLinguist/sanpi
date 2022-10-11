pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma="completely"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}