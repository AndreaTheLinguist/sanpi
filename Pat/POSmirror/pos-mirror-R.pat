pattern { 
    ADJ [xpos=re"JJ.?"]; 
    ADV [xpos=re"RB.?"]; 
    ADV < ADJ;
    mod: ADJ -[advmod]-> ADV;  
    MIR [lemma="somebody"|"someone"|"everyone"|"everybody"|"something"|"everything"|
          "all"|"many"|"some"|"every"|"always"|"sometimes"|"often"|"either"|"both"|"or"];     
    mir: ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod|parataxis|dislocated|rel
                |nsubjpass|attr|punct|csubj|ccomp|reparandum|obj 
                |compound|expl|partmod|dep|conj]-> MIR; 
    MIR << ADV
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|
                "nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod|parataxis|dislocated|rel]-> NEG;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|
                "nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];
    NEG -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];   
    NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
    NR -[re"[^E].*"]-> ADJ;
    NR -[re"[^E].*"]-> NEG;
    NEG << ADV;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];    
    NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
    NR -[re"[^E].*"]-> ADJ;
    NR -[re"[^E].*"]-> RELAY; 
    RELAY -[re"[^E].*"]-> NEG;
    NEG << RELAY;
    NEG << ADV;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|
            "nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    ADJ -[re"[^E].*"]-> RELAY; 
    RELAY -[re"[^E].*"]-> NEG;
    NEG << ADV;
}