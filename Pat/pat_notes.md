# Pattern Notes and TODOs

## ambiguity producing contexts

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

## Questionable Contexts

- [x] every N subj
- [x] everyone subj
- [x] everything subj
- [ ] if antecedent
- [ ] if consequent
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
  - *__neg raising can be used to hedge__. Scope ambiguity between stronger and weaker meanings, very like negation of scalar predicates, resulting in ambiguity that could be used strategically in context. Different from other kinds of scope ambiguities (e.g. PP attachment) because the available readings are not mutually exclusive. Rather, they have a subset relationship: the low scope reading indicates a subset of the possible worlds which are consistent with the high scope reading. This means that, like the negated universal quantifiers, there is an additional level of pragmatic ambiguity when the embedded clause has an inherent scalar middle ground. (__Has this been written about?__)*

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
  
- What's going on with `because` here?
  - *He didn't leave because he was particularly upset*
  - does this license NPIs?
  - Is it litotes?
  - does `because` block negation?
  