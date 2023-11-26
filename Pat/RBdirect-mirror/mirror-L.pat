pattern {
    ADJ [xpos=re"JJ.?"];
    ADV [xpos=re"RB.?"];
    ADV < ADJ;
    mod: ADJ -[advmod]-> ADV;

    MIR [lemma="somebody"|"everybody"|"something"|"everything"|
                "some"|"every"|"always"|"sometimes"|"often"|"either"|"with"];  
    mir: MIR -[^acl:relcl|advcl|appos|conj|nmod|parataxis]-> ADJ;
    MIR << ADV
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|
                "nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    ADJ -[^advcl|amod|discourse|prep|obl|obl:npmod|parataxis]-> NEG; 
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
    negraise: NR -[re"[^E].*"]-> ADJ;
    neg: NR -[re"[^E].*"]-> NEG;
    NEG << ADV;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];    
    NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
    negraise: NR -[re"[^E].*"]-> ADJ;
    relay: NR -[re"[^E].*"]-> RELAY; 
    neg: RELAY -[re"[^E].*"]-> NEG;
    NEG << RELAY;
    NEG << ADV;
}

without {
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|
            "nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"|"ain't"|"aint"];  
    relay: ADJ -[re"[^E].*"]-> RELAY; 
    neg: RELAY -[re"[^E].*"]-> NEG;
    NEG << ADV;
}