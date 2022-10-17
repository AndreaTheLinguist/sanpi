pattern { 
	ADJ [xpos=re"JJ.?", form=re"non.*\|un.*\|[md]is.*\|i[lmnr].*\|de.*"];   
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}

% not (non\w+\b|un\w+\b|[md]is\w+\b|i[lmnr]\w+\b|de\w+\b)