# Running Notes

## Cases to consider

- `ADJ enough`
- irregular/lexicalized? `not` cases:
  - `not so much`

    - cause:  `not so much that...`
    - subject of content: `not so much about ...`
    - categorizing: `not so much a ...`

  - `not [lower threshold], but [higher threshold]`
    - `not just __, but __`
    - `not only __, but __`  
    - ... `simply`, `merely`, etc.

- `no ADV (ADV) ADJ`
  - `no longer ...`
    - `no longer physcially dependent`
  - `no more ...`
    - `no more [ADJ] (than)` vs. `no more [ADJ] [NOUN]`
    - `no more comfortable`
  - `no less ...`
    - `no less [ADJ`_~ e.g important, weighty, etc._`] a [NOUN]`
- `my form is not the best` -> should this be caught? (with adv)
- `nor` and other(?) negative conjunction cases
- `few`
  - `a few`, `the few` vs. `(very) few`
  - **NPI in matrix VP with `few` in subject: disallowed if DP?**

    1. \* A few (strangers) have been here in years.
    1. &rarr; (Very) few (strangers) have been here in years.

    1. \* The few bibliophiles have visited the library in years.
    1. &rarr; (Very) few locals have visited the library in years.

  - **NPI licensed in restriction of _definite_ DP with `few` modifier**

    1. \* A few Americans who have been here in years were (all) students.

    1. &rarr; The (very) few Americans who have been here in years were (all) students._

    1. **? (Very) few Americans who have been here in years were students.**

  - Note: _This is my intuition..._  
    \* A very few...  
    _vs._  
    &rarr; The very few...

- mitigators:
    1. work with determiners: `almost`, `nearly`
    1. work with predicates but not determiners: `sort of`, `kind of`, `possibly`, `maybe`, `perhaps`
    1. auxiliaries (= modals)
  - second 2 here may just be getting into alternate hedge territory (see below)
- superlatives and comparatives (see below)
- need to exclude question answering `no`'s: _No, [explanation]_
- `ADV ADV ADJ` cases (2+ adverbs) need to be considered: both adverbs may need to be captured for accurate representation of the relevant phenomena

---

## Ideas

### tasks?

- [x] update tabulate script: merge `pat_debug.ipynb` code with `tabulateHits.py`
- [ ] **exclude `a few` and `the few`** (allow `(the) very few`? )
- [ ] restrict allowances on "relay" action
  - [ ] dependency relation label
  - [ ] part of speech tag
- [ ] look at the odd cases (`hits/...look-into-these.csv`)
- [ ] fix `without` cases:
  - may not be able to be lumped in with the others
  - does not work with the alternate structure for `nor` above either.
- [ ] assess restriction cases
  - [ ] look at few_sample for how to structure restriction pattern  
      &rarr; <sub>S</sub> [<sub>NP</sub> `few` ADV ADJ NOUN ] [<sub>VP</sub> ... ] ]
      (use `quickviewHits.py`)
- [ ] deal with conjunction cases?

---

### "maybe"s

- [ ] add catch for additional adverbs (post-search processing? or in search pattherns?)
- [ ] Create new categorization scheme for patterns?
- [ ] create new fields/info categories for sentence text split at key points: e.g. `pre-NEG`, `post-NEG`, `NEG-to-ADV`, `post-ADJ` ...
- [ ] specify permitted (or prohibited) dependency labels and/or xpos values for "relayed" negation cases.
- [ ] mark prenominal vs. predicate adjectives
- [ ] mark adjunct clauses?? (Is this possible?)

---

### Thought connections

negation is used in formal languages to include/cover "undefined" cases, e.g. grew pattern specifications with without clauses and "not" definitions

---

could extended mitigators, i.e. cases with modal adverbs and auxiliary verbs, serve as a categorization metric? That is, if these cases are taken to be hedging cases, would that imply that any negated scalars are also likely hedging uses?

---

Having NPI in subject of NR construction does not prevent "negative quality" from reaching (lower) predicate (e.g. _I don't think anyone has been here in years._)

---

Maybe superlative and comparative forms are just a (the most? one of the most?) basic scalar operation. Superlatives are clearly just elemental maximizers, but comparatives differ from intensifiers, minimizers, and maximizers in the sense that they indicate incremental shifts/relative positions, rather than fixed positions. Intensifiers also indicate relative scale positions, but the comparison point in those cases is contextually defined in an implicit sense than an explicit sense. To say something is "extremely expensive" is allowed in a context where no other entity's expense point has been referenced--we just fill in our understanding of what is in the "normal" range of cost. This implicit threshold/range can be tailored to fit the context (i.e. what kind of item are we considering? houses are much more expensive than coats), but we don't have to actually find a specific entity or group of entities to compare the costs of. If we say something is "more expensive" (or "less expensive") though, we need to be able to find something relevant in the context, either specifically introduced item(s), or vaguely referenced items, or a set of items that we can pull from the context via accomodation.

Consider the following:

    A: I heard your remodeling project is finished! How're you liking your new kitchen?

    B: Oh, it's really great! I finally have enough counter space! It's been really helpful because I've been doing more cooking recently--I'm trying this meal subscription service. 
    >>> It's more expensive, but it's so convenient and I've been learning new techniques I'd've never tried on my own.

In this case, the hearer would have to fill in a comparison point, but that's not hard to do since there are relevant options: It could easily be _"more expensive than not using a subsciption service"_ but it could also be _"more expensive than other meal subscription services"_.

Now let's compare to other possible forms the speaker could have uttered:

    ... It's extremely expensive, but totally worth it for the convenience and variety. 

This one feels a bit odd, since there is a social pressure to not be financially responsible. Saying you're buying something that you yourself label as being in the "extreme cost range" almost requires that a "redeeming quality" be offered as a follow up. The options below are more natural to my ears.

    ... It's not cheap, but totally worth it for the convenience and variety. 
    ... It's (somewhat) expensive, but totally worth it for the convenience and variety.

---

## Corpus parsing info

- superlatives & comparatives:
  - adj: `JJR`, `JJS`
  - adv: `RBR`, `RBS`
- subject match causes problems for relative clause versus matrix clause cases (bc subject is different)
- "neg" relation labels:
  - `neg`: regular
  - `advmod`: no less bright
  - `dep`: no less important
- not all "relay" types are equally permissible: need to restrict (see above)
  - `dep` may be bad across the board for this
- POS tagging in corpora is not 100% accurate; some nouns tagged as adj and adj tagged as verbs
- new generalized patterns catch prenominal cases
- `without` does not have the same dependencies/structural configuration in corpus tagging/parsing
