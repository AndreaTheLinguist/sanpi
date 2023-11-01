pattern {
    ADJ [xpos=re"JJ.?"];
    ADV [xpos=re"RB.?"];
    mod: ADJ -[advmod]-> ADV;
    ADV < ADJ;
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];
    neg: NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;
    NEG << ADV
}

% with following, will not match `not uninteresting` where "not" is adverb and "uninteresting" is adjective
% ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];