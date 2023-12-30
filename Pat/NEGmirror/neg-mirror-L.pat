pattern {
    ADJ [xpos=re"JJ.?"];
    ADV [xpos=re"RB.?"];
    ADV < ADJ;
    mod: ADJ -[advmod]-> ADV;
    NEG [lemma="nobody"|"nothing"|"no"|"none"|"never"|"rarely"|"seldom"|"hardly"|"scarcely"|"barely"|"neither"|"nor"];  
    neg: NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis|acl|obl|advmod|acomp|nsubj|attr|dobj|list|partmod|prep]-> ADJ;
    NEG << ADV
}

% without direct ADJ head
without {
    NEG [lemma="not"|"without"|"few"|"ain't"|"aint"];  
    ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod|parataxis]-> NEG; 
}

% without direct NEG head
without {
    NEG [lemma="not"|"without"|"few"|"ain't"|"aint"];  
    NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;
}

% without neg-raised negation
without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];   
    NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
    negraise: NR -[re"[^E].*"]-> ADJ;
    NR -[re"[^E].*"]-> NEG;
    NEG << ADV;
}

% without 
without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];    
    NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
    negraise: NR -[re"[^E].*"]-> ADJ;
    relay: NR -[re"[^E].*"]-> RELAY; 
    RELAY -[re"[^E].*"]-> NEG;
    NEG << RELAY;
    NEG << ADV;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|
            "nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    relay: ADJ -[re"[^E].*"]-> RELAY; 
    RELAY -[re"[^E].*"]-> NEG;
    NEG << ADV;
}