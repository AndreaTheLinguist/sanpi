pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [xpos=re"RB.?"]; 
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    mod: ADJ -[advmod]-> ADV;  
    neg: ADJ -[re"[^E].*"]-> NEG;
    ADV < ADJ;
    NEG << ADV
}

% with following, will not match `not uninteresting` where "not" is adverb and "uninteresting" is adjective
% ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];