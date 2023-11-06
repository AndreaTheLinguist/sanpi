pattern {
    ADJ [xpos=re"JJ.?"];
    ADV [xpos=re"RB.?"];
    mod: ADJ -[advmod]-> ADV;
    ADV < ADJ;
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];
    neg: NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;
    NEG << ADV
}

% fyi, WILL match negative adverbs to `ADV` node, 
%   provided there is an additional negative token matching NEG specs; 
%   e.g.: 
%   | neg_form | adv_form | adj_form | text_window                                         | neg_deprel |
%   |----------|----------|----------|-----------------------------------------------------|------------|
%   | Not      | not      | excited  | ( Not that I 'm not excited about those things --   | ccomp      |
%   | nothing  | not      | awkward  | "yeah , there 's nothing not awkward about it , """ | amod       |
%   | nothing  | not      | safe     | There 's nothing not safe about it , nothing        | amod       |
%   | nobody   | not      | good     | There 's nobody not good in the West .              | amod       |