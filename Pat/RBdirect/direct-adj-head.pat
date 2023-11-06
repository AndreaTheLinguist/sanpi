pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [xpos=re"RB.?"]; 
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    mod: ADJ -[advmod]-> ADV;  
    neg: ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod]-> NEG; 
    ADV < ADJ;
    NEG << ADV
}

% fyi, WILL match negative adverbs to `ADV` node, 
%   provided there is an additional negative token matching NEG specs; 
%   e.g.: 
%   neg_form | adv_form | adj_form    | text_window                                                | neg_deprel
%   ---------|----------|-------------|------------------------------------------------------------|-----------
%   not      | not      | funny       | July 31 , and not only is it not funny , it totally seemed | advmod
%   Not      | not      | responsible | Not only is christianity not responsible for science , but | advmod
%   not      | not      | possible    | , however it 's not not possible .                         | advmod
%   not      | not      | patriotic   | It 's not that I 'm not patriotic ; it 's just             | advmod
%   Not      | not      | important   | Not that it 's not important to understand and explain     | advmod
%   Not      | not      | sure        | Not to mention , I am not sure if they like Winnie         | advmod
%   n't      | not      | true        | But is n't that just specifically not true ?               | advmod
