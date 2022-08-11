pattern { 
	ADJ [xpos=re"JJ.?", form=re"non.*\|un.*\|[md]is.*\|i[lmnr].*\|de.*"];   
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}