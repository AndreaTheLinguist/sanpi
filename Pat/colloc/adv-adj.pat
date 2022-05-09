pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ
}