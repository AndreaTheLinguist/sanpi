# special cases

## `few` as function on subject

```{js}
    pattern {
        ADJ [xpos=JJ|JJR|JJS];
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"
             |"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"
             |"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;
        NEG [lemma="few"];  
        relay: ADJ -> S;
        neg: S -> NEG;
        NEG << ADV;
    }

    without {
        S -[det|poss]-> det;
        S -[amod]-> NEG;
    }
```

## `few` as subject

```{js}

    pattern { 
        ADJ [xpos=JJ|JJR|JJS]; 
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"
             |"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"
             |"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;

        NEG [lemma="few"];  
        neg: NEG -> ADJ;
        NEG << ADV; 
    }

```

## positive `few`?

```{js}
    pattern { 
        ADJ [xpos=JJ|JJR|JJS]; 
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;
        NEG [lemma="few"];  
        relay: ADJ -> S; 
        neg: S -> NEG;
        det: S -[det]-> DET;
        NEG << ADV
    }
```