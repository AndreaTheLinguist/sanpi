pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [xpos=re"RB.?"]; 
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    mod: ADJ -[advmod]-> ADV;  
    neg: ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod]-> NEG; 
    ADV < ADJ;
    NEG << ADV
}
    % neg: ADJ -[nsubj|case|cop|det|cc|cc:preconj]-> NEG; 