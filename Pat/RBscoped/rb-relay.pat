pattern { 
    ADJ [xpos=JJ|JJR|JJS]; 
    ADV [xpos=re"RB.?"]; 
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    relay: ADJ -[re"[^E].*"]-> RELAY; 
    neg: RELAY -[re"[^E].*"]-> NEG;
    NEG << ADV;
}

% with follwing, will not match `not uninteresting` where "not" is adverb and "uninteresting" is adjective
% ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];