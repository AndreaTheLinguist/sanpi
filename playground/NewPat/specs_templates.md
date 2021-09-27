# template approaches

## all `RB JJ*` cases

pattern {
    ADJ [xpos="JJ"|"JJR"|"JJS"]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
}

## cases with a "relay" between negation and AP

```{js}
    pattern { 
        ADJ [xpos=JJ|JJR|JJS]; 
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
            |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;

        NEG [lemma="hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
            |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"]; 
        RELAY [];
        relay: ADJ -> RELAY; 
        neg: RELAY -> NEG;
        NEG << ADV;
    }
```

## cases with direct dep relation between neg and AP

I.e. without a relay or intervening element to "filter" or "block"

```{js}
    pattern { 
        ADJ [xpos=JJ|JJR|JJS]; 
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
            |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;
        NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|
            "seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
        neg: ADJ -> NEG;
        NEG << ADV;
    }
```

## cases with negraising

```{js}
    pattern { 
        ADJ [xpos=JJ|JJR|JJS]; 
        ADV [
            lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"
        ];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;
        NEG [
            lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"
        ];  
        NR [
            lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"|"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"|"desirable"|"should"|"ought"|"better"|"most"|"usually"];
            
        negraise: NR -> ADJ;
        neg: NR -> NEG;
        NEG << ADV;
    }
```

Negraising?  or transparency? 

- I'm not sure he's exactly happy. 
- I'm not certain he's exactly happy. 
- He didn't make a very strong case. 
