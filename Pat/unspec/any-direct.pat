pattern { 
    ADJ [xpos=re"JJ.?"]; 
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    direct: ADJ -[re"[^E].*"]-> X;
    X << ADV;
}

% with follwing, will not match `not uninteresting` where "not" is adverb and "uninteresting" is adjective
% ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];