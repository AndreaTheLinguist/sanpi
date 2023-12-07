  pattern { 
      ADJ [xpos=JJ|JJR|JJS]; 
      mod: ADJ -[advmod]-> ADV;  
      ADV < ADJ;
      NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
      NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
      negraise: NR -[re"[^E].*"]-> ADJ;
      neg: NR -[re"[^E].*"]-> NEG;
      NEG << ADV;
}

% with follwing, will not match `not uninteresting` where "not" is adverb and "uninteresting" is adjective
% ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];