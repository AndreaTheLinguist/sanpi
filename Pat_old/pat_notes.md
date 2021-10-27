# Pattern Notes and TODOs

## Unambiguous contexts

- [ ] simple sentence with no elements included in the next to sections...
- [ ] context above a "blocking" verb (or whatever it's called), e.g. *know*, *discover* (factives?)
- [ ] positive polarity subject/quantifiers: `some`, `either` (without predicate negation)

## Ambiguity producing contexts

- [x] almost nobody
- [x] almost no one
- [x] almost no NN
- [x] almost none
- [ ] almost never
- [ ] almost not
- [x] without being
- [ ] scarcely any (~very few)
- [ ] scarcely
- [ ] rarely
- [ ] barely
- [ ] hardly
- [ ] seldom
- [ ] doubt (essentially lexicalized neg-raising conext `not believe`)
- [ ] deny? --> weak NPI only
- [ ] prevent? --> weak NPI only
- [ ] not think
- [ ] not believe
- [ ] not suppose
- [ ] not expect
- [ ] not imagine
- [ ] not suppose
- [ ] not look like
- [ ] not seem (like, that)
- [ ] not appear (that)
- [ ] not likely (that)
- [ ] not probable (that)
- [ ] not want (inf-sub) to
- [ ] not wish (inf-sub, for inf-sub) to
- [ ] not wish that? **does this allow for neg-raising?**
- [ ] not intend (inf-sub, for inf-sub) to
- [ ] not plan (for inf-sub) to

## Questionable contexts

- [x] every N subj
- [x] everyone subj
- [x] everything subj
- [x] if antecedent
- [x] if consequent
- [ ] questions
- [ ] all N subj
- [ ] none restriction
- [ ] no restriction

- `almost` + any of the negated existentials
  - `almost` will have `advmod` dependency
  - `neg-quant -[advmod]-> almost`
  - actually, better to just use linear relationship, I think...
  - **also do `nearly`?**
  - `almost` context will be subset of more basic restriction, so should be peeled off first

- neg-raising interveners
  - need to check on whether these cases are included by default in c0 or if the delineation of the copula and subject, etc. prevent it?
  - list from Horn Neg-Raising chapter in Oxford Handbook of Negation
    - believe, suppose, think
    - expect, imagine
    - be likely, probable
    - seem, appear, look like
    - intend, choose, plan to
    - want, wish,
    - suggest, advise

    - advisable, desirable
    - should, ought to, better
    - most
    - usually

  - *__neg raising can be used to hedge__. Scope ambiguity between stronger and weaker meanings,
    very like negation of scalar predicates, resulting in ambiguity that could be used strategically
    in context. Different from other kinds of scope ambiguities (e.g. PP attachment) because the
    available readings are not mutually exclusive. Rather, they have a subset relationship: the low
    scope reading indicates a subset of the possible worlds which are consistent with the high scope
    reading. This means that, like the negated universal quantifiers, there is an additional level
    of pragmatic ambiguity when the embedded clause has an inherent scalar middle ground.
    (__Has this been written about?__)*

  - Illustrations of Neg Raising/Non-blocking interveners
    - Embedded clause judgements
      - They don't have any money, either.
      - \*They have any money, either.  

    - I don't __ they have any money, either.
      - think
        - I don't think they have any money, either.
          - [low] ~ I think that they have no money
          - [high] ~ It is not the case that I think they have money.
        - \*I think they have any money, either.
      - believe
        - I don't believe they have any money, either.
        - \*I believe they have any money, either.
      - suppose
        - I don't suppose they have any money, either.
        - \*I suppose they have any money, either.
      - expect
        - I don't expect they have any money, either.
        - \*I expect they have any money, either.
      - imagine
        - I don't imagine they have any money, either.
        - \*I imagine they have any money, either.

    - It isn't __ (that) they have any money, either.
      - likely
        - It isn't likely they have any money, either.
        - \*It's likely they have any money (either).
      - probable
        - It isn't probable that they have any money, either.
        - \*It's probable they have any money (either).

    - It doesn't __ they have any money.
      - look like
        - It doesn't look like they have any money, either.
        - \*It looks like they have any money (either).
      - seem {like, that}
        - It doesn't seem ({like,that}) they have any money, either.
        - \*It looks like they have any money (either).
      - appear {that}
        - It doesn't appear (that) they have any money, either.
        - \*It appears (that) they have any money (either).
        - It appears (that) they have some money.

    - I didn't __ to give them any money (either)
      - want
        - I didn't want to give them any money, either.
        - \*I wanted to give them any money (either).
        - I wanted to give them ({the, some}) money, too.
      - wish
        - I didn't wish to give them any money, either.
        - \*I wished to give them any money (either).
        - I wished to give them money.
      - intend
        - I didn't intend to give them any money, either.
        - I intended to give them money.
        - \*I intended to give them any money.
      - plan
        - I didn't plan to give them any money, either.
        - I planned to give them money.
        - I planned to give them some money, too.
        - \*I planned to give them any money (either).
      - choose
        - I didn't choose to give them any money, either.
        - I chose to give them (some) money (too)
        - \*I chose to give them any money (either)

    - I don't __ (that) you give them any money (either)
      - advise
        - I don't advise that you give them any money, either.
        - I advise that you give them money.
        - I advise that you give them some money, too.
        - *I advise that you give them any money, either.
      - suggest
        - I don't suggest that you give them any money, either.
        - I suggest that you give them money.
        - I suggest that you give them some money.
        - *I suggest that you give them any money.
      - recommend
        - I don't recommend that you give them any money, either.
        - I recommend that you give them money.
        - I recommend that you give them some money.
        - *I recommend that you give them any money.

- mitigated negative adverbs: scarcely, rarely, barely, hardly, etc.

- negated universal quantifiers:
  - *not all, not every, not everyone*

  - not all
    - [not all NP] Not all (of the X) were ADV ADJ
    - [not all DP] Not all X were ADV ADJ
    - [not all VP] They were not all ADV ADJ
      - **overlap** This should be caught in the not VP context description...

  - not every
    - [not every DP] Not every X was ADV ADJ
  
  - not everyone
    - Not everyone was ADV ADJ

- negative verbs
  - doubt --> strong and weak
    - I doubt they have any money, either.
    - I doubt they have the money, either. (is this worse than with *any*?)
    - \*I suspect they have any money.
  - prevent? --> weak only
    - I prevented them from getting any money.
    - \*I helped them get any money.
    - I didn't prevent them from getting the money, either.
    - \*I prevented them from getting the money, either.
  - deny? --> weak only
    - I denied having any money.
    - \*I acknowledged having any money.

    - \*I denied having the keys, either.
    - \*I acknowledged having the keys, either.

    - I didn't {acknowledge, deny} having the keys, either.

- what to do with conjoined predicates like this?
  - _**Nothing is more unequivocally useless and irritating** than to listen to someone rattle off his Top 10 anything..._
  - currently only `useless` is recorded as ADJ
  - Is it possible to specify the context such that `irritating` is captured in an additional hit?
  - Or would it be best to record the ADJ as conjoined `useless and irritating`?
  - cases with `no` as determiner on modified noun, e.g `no small thing`, `no big deal`

- May want to remove subject match restrictions from patterns unless required to ensure the right structure: relative clauses vs. matrix clause
  
- What's going on with `because` here?
  - *He didn't leave because he was particularly upset*
  - does this license NPIs?
  - Is it litotes?
  - does `because` block negation?

- difference between these cases/what's going on?:
  - _nothing too exciting is going on_
    - There does not exist a thing that is too exciting and that is also happening
    - ~ not[exists(x) & too_excitg(x) & going_on(x)]
  - _no too exciting thing is going on_
    - There does not exist a [too exciting thing ]
    - ~ not
  - _There is nothing exciting_
  - _There are no exciting things_
  - ...**Is** there a difference?? Does senntence position matter?
  
- problem cases:
  - conjunctions
    - _..., and it is even more uncertain..._

      ```conllu
        12 and         and       _ CC _ 2   cc     2:cc _
        13 it         it        _ PRP _ 17 nsubj   17:nsubj _
        14 is         be        _ VBZ _ 17 cop     17:cop _
        15 even        even      _ RB _ 17 advmod 17:advmod _
        16 more        more      _ RBR _ 17 advmod 17:advmod _
        17 uncertain   uncertain _ JJ _ 2   conj   2:conj _
      ```

    - *Nothing is more unequivocally useless and irritating*

      ```conllu
        1 nothing       nothing       _ NN _ 5 nsubj   5:nsubj _
        2 is           be           _ VBZ _ 5 cop     5:cop _
        3 more         more         _ RBR _ 4 advmod 4:advmod _
        4 unequivocally unequivocally _ RB _ 5 advmod 5:advmod _
        5 useless       useless       _ JJ _ 0 root   0:root _
        6 and           and           _ CC _ 5 cc     5:cc _
        7 irritating   irritating   _ JJ _ 5 conj   5:conj _
      ```

  - comparitives and superlatives:
    - different xpos codes for these:
      - JJR/RBR
      - JJS/RBS

## New Patterns: to be categorized

Trying a revised more minimal/unified approach to the patterns: Instead of
having a separate one for every single case, the same template pattern can
be used, and the value of the "NEG" marker can be pulled out along with ADV-ADJ pairs.

This may not work entirely, and maybe keeping the original framework would be a better idea.
(i.e. maybe I shouldn't re-invent the wheel? But it is helpful in seeing what types of
combinations actually _are_)

### Pat: with "relay" intervener (neg-det> subject > adj?)

With a "relay" (i.e. something scoping between the neg element and the adjective) "not" cannot
be included, because it catches things like:

- _Last week , in perhaps the most striking departure , Egypt 's Mubarak said that if the_
  _Palestinians could **not** achieve progress in Sharon 's time , it would be **very difficult** afterward ._
- This might be avoidable if additional specifications are made.

Further narrowing/splitting of this grouping may be helpful as well.

NEG must precede ADV as well, though it doesn't not have to be immediate.
ADV and ADJ pairs are restricted to contiguous tokens.

```js
pattern { 
    ADJ [xpos=JJ|JJR|JJS]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    NEG [lemma="hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
    relay: ADJ -> S; 
    neg: S -> NEG;
    NEG << ADV;
}
```

### Pat: without "relay" intervener (neg-subject > adj | neg-adverb > adj)

Without a relay, "not" can and should be included:

```js
pattern { 
    ADJ [xpos=JJ|JJR|JJS]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
    neg: ADJ -> NEG;
    NEG << ADV;
}
```

### Pat permissible nonlocal/negraising

Attempting to get a neg-raising template. Not sure if this is right yet--needs further exploration
--> check out data in sdf3 from pat_debug notebook

```js
pattern { 
    ADJ [xpos=JJ|JJR|JJS]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];  
    NR [lemma="think"|"believe"|"want"|"seem"];
    negraise: NR -> ADJ;
    neg: NR -> NEG;
    NEG << ADV;
}
```

- "negraise" labels corresponding to valid cases:

  - `ccomp`
    - _We do **n't think** this is **fundamentally new** or different_
    - _But many did **not think** that Sunday morning sports and Sunday morning spirituality were **mutually exclusive**_
    - _...she did **not believe** Ford 's current position was **much different** from the coalition 's_
    - _I do **n't believe** that any great art form , any part of the history of man 's accomplishments and civilization , is **as discardable** as a used tissue_
    - _I did **n't think** racism was **so high** or rampant_

    - **! problematic `ccomp`**:
      - _I did **n't want** to show my face , I was **so disappointed** in my performance_
      - _The role of money does **n't seem** to bother anyone other than the owner-handlers , perhaps because campaigns have been **extremely pricey** since the '70s_

  - `acomp`
    - _The Knicks , despite John Starks ' guarantee that there would be a Game 6 in New York , **never seemed mentally prepared** to match the Pacers_

- maybe work?:  
  - `xcomp` but not `be` verb
    - _We do **n't want** to get **too bullish** and push the horses too far_
    - _federal officials do **n't want** to appear **too reliant** on information from companies locked in battle with Microsoft_
    - _I do **n't want** to get **too excited**..._
    - _You do **n't want** it **too soupy**_
    - _And **nobody seems** to be **more bullish** at the moment than Everett_
    - _You want to play aggressively , but you do **n't want** to be **too aggressive**_
    - _But I do **n't want** to get **too excited**_
    - _I do **n't want** to be **too negative** because there 's good and bad , but I have to agree with my husband_
    - _I do **n't want** to stay **too long**_
    - _some Afghans did **not want** to be **overly critical** of efforts to give Afghans the powerful roles previously filled by Westerners_
    - _he was criticized as a Kremlin pawn who did **not want** Ukraine to become **more democratic** and pro-Western_
    - _You do **n't want** it **too thin**_
    - _You do **n't want** it **too thick**_

- labels that do **not** work:

  - `advcl`
    - _Magazines did **n't want** to do a story on a child because it is n't **very marketable**_
    - _universities and companies might **not want** to run the risk of opening Web forums if they would be **criminally liable** for their contents_

  - `conj`
    - _I do **n't want** to make a blanket statement , but the importance of instant gratification is **much higher** than four years ago_
    - _I did **n't think** I 'd ever get another Silver Charm , but this horse is **very close**_
    - _Scott did **n't want** to know his golf clubs and was **more interested** in surfing in the ocean..._
    - _Eli ... wo **n't  -LBQ-  think** as well on his feet ... and is **more likely**  -LBQ-  to short-circuit in the biggest of pressures and the biggest of games_
    - _He and much of his circle do **not want** the U.S. to leave and are only **too happy** to see us invest further_
    - _I would **never** have **thought** that , but it 's kind **of neat** ._ [! `of` as adverb????]
    - _The rules ... can **not seem** to contain the tumult of politics in the new Iraq , where religious symbolism fuses seamlessly with political messages , and campaigning is **as colorful** and unruly as the nation itself ._
    - _I do **n't think** Alex walked home , but that was **all real**_

  - `parataxis`
    - _**Nobody believed** in this movie ; we could n't get backing from the usual sources_ the characters were **too raw**_
    - _In the exam room , he **seemed without** normal communication skills ; I was **increasingly sure** that he was on the autistic spectrum ._

  - `dep`
    - _If health costs were killing businesses , do **n't** you **think** businesses would have lobbied for measures to reduce costs ? Instead , they have been silent or **even opposed**_
    - _I ca **n't believe** nine months ago I was **no different** than you guys and now I 'm playing in the Super Bowl_

### with different neg-raisers

```js
  pattern { 
      ADJ [xpos=JJ|JJR|JJS]; 
      mod: ADJ -[advmod]-> ADV;  
      ADV < ADJ;
      NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];  
      NR [lemma="suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"|"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"|"desirable"|"should"|"ought"|"better"|"most"|"usually"];
      negraise: NR -> ADJ;
      neg: NR -> NEG;
      NEG << ADV;
}
```

#### examples (from Feb 2010 NYT)

- Good

  - `acomp`
    - _the political landscape does **n't look too promising** right now_
    - _your triple axel does **n't look very good** these days_
    - _things still do **n't look so good** for Tibet_
    - _Miller did **not look as comfortable**..._
    - _The golden days of postwar American letters **never looked** quite **so good** as in this collection of snapshots_
    - _...it 's safe to say Claire **never** has **looked so angry** in public , or had reason to look so defeated_
    - _Redford **never** has **looked more haggard** or been more sympathetic and convincing_
      - and working `conj` case! -> Redford never has looked more haggard or been **more sympathetic** and convincing
    - _Scott Fraser... threw a wrist shot at Belfour that did **n't look particularly special** until it hit the inside of the right post and ricocheted into the net ._

  - `dobj`
    - _If you were **n't expecting too much** from a show based on a cheesy 1980s miniseries about an alien invasion_ (??? `much` as adj?? more like a noun here)
    - _I ca **n't expect much more**_
  
  - `xcomp`
    - _Scientists were **not expecting** 2002 to be **any different**_
    - _Do **n't expect** to get too much **more creative** with the format than that_
    - _The Dodgers probably ca**n't expect** to be **too formidable **offensively..._
    - _Rupert Murdoch 's Fox Group is **n't likely** to be **so magnanimous**_
    - _...the killing did **n't appear** to be **politically motivated**..._

- maybe??
  - `acomp`
    - _... Bridges , as an ex-con struggling to be the father he never had , has **rarely looked more beautiful** or been more devastatingly touching ._

  - `dobj`
    - _he does **n't look too much** like a football coach_

  - `dep`
    - _...I could **n't** have **imagined** it being **much better**_

- Bad
  
  - `conj`
    - _**None** of the analysts in CNN 's stable are **likely** to run for office in 2010 or 2012 , and the same is **generally true** for the broadcast networks ._
    - _... that study ... found homes with guns , compared to homes **without** , are five times more **likely** to experience a suicide and three times **more likely** to have a member of the household killed by another member or by an acquaintance ._
    - _Maybe **not better** , but life 's still been **pretty good** for a long time for McKay_

  - `ccomp` case
    - _I am **not suggesting** that Streisand 's sponsoring of the film is in any way traitorous , **just mistaken**_

### pat with all neg-blockers

```js
  pattern { 
      ADJ [xpos=JJ|JJR|JJS]; 
      ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
      mod: ADJ -[advmod]-> ADV;  
      ADV < ADJ;
      NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
      NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"|"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"|"desirable"|"should"|"ought"|"better"|"most"|"usually"];
      negraise: NR -> ADJ;
      neg: NR -> NEG;
      NEG << ADV;
}
```

### pat with neg-blockers

~~_i.e. interveners that are not neg-raisers_~~
**This does not work**

```js
  pattern { 
      ADJ [xpos=JJ|JJR|JJS]; 
      ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
      mod: ADJ -[advmod]-> ADV;  
      ADV < ADJ;
      NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];  
      BLOCK [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"|"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"|"desirable"|"should"|"ought"|"better"|"most"|"usually"];
      block: BLOCK -> ADJ;
      neg: BLOCK -> NEG;
      NEG << ADV;
}
```

## Adjust pattern templates

Tasks to do this (*tentative*):

- [x] add `nor`   
  - This got more complicated than expected. Some cases will be caught just by adding "nor" to the NEG lemma list, but the following structure is not captured with those:

    ```js
      pattern { 
        ADJ [xpos="JJ"|"JJR"|"JJS"]; 
        ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
            |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
        mod: ADJ -[advmod]-> ADV;  
        ADV < ADJ;
        NEG [lemma="nor"];  
        NEG << ADV;
        C [xpos<>VB];
        neg: C -> NEG;
        relay: C -> ADJ; 
      }
    ```
    
- [ ] exclude `a few` and `the few` (allow `(the) very few`? )
- [ ] restrict allowances on "relay" action
  - [ ] dependency relation label 
  - [ ] part of speech tag
- [ ] look at the odd cases (`...look-into-these.csv`)
- [ ] fix `without` cases: 
  - may not be able to be lumped in with the others
  - does not work with the alternate structure for `nor` above either.
- [ ] assess restriction cases
    - [ ] look at few_sample for how to structure restriction pattern   
      &rarr; [<sub>S</sub> [<sub>NP</sub> `few` ADV ADJ NOUN ] [<sub>VP</sub> ... ] ]    
      (use `quickview.py`)
- [ ] deal with conjunction cases?
---
possible additional steps? 
- [ ] Create new categorization scheme for patterns?
- [ ] create new fields/info categories for sentence text split at key points: e.g. `pre-NEG`, `post-NEG`, `NEG-to-ADV`, `post-ADJ` ...
- [ ] specify permitted (or prohibited) dependency labels and/or xpos values for "relayed" negation cases. 
- [ ] mark prenominal vs. predicate adjectives 
- [ ] mark adjunct clauses?? (Is this possible?)