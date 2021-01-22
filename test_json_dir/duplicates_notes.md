# notes on duplicate hits

- duplicate due to erroneous parsing of "what" as subject of "happy": 
*"And **what** of the Colts teammates **who** were not too **happy** with him ?"*

  ```text 
    "fillers": {
        "S": "what",
        "NOT": "not",
        "BE": "be",
        "ADV": "too",
        "ADJ": "happy"
    ...

    "fillers": {
        "S": "who",
        "NOT": "not",
        "BE": "be",
        "ADV": "too",
        "ADJ": "happy"}

    "text": "And what of the Colts teammates who were not too happy with him ?"
  },
  ```
---
  - another subject parse error: ***Mjeanwhile** , second-quarter **earnings**, while disappointing , were not as **bad** as had been expected , fueling the Bolsa 's slight rebound .*

  ```text
        "fillers": {
        "S": "Mjeanwhile",
        "NOT": "not",
        "BE": "be",
        "ADV": "as",
        "ADJ": "bad"
      }
      ...

        "fillers": {
        "S": "earnings",
        "NOT": "not",
        "BE": "be",
        "ADV": "as",
        "ADJ": "bad"
      }
    },
    "text": "Mjeanwhile , second-quarter earnings , while disappointing , were not as bad as had been expected , fueling the Bolsa 's slight rebound ."
  ```
---
- again due to `nsubj` relation
- but an accurate parse actually, because of resumptive pronoun. Sentence actually has 2 subjects. Still, isn't cause for concern in regards to predicate/trigger data.
- *He argued [...] The dramatic **changes** they 're touting , **they** 're not that **dramatic** .*

  ```text
      "fillers": {
        "S": "change",
        "NOT": "not",
        "BE": "be",
        "ADV": "that",
        "ADJ": "dramatic"
      }
      ...
      "fillers": {
        "S": "they",
        "NOT": "not",
        "BE": "be",
        "ADV": "that",
        "ADJ": "dramatic"
      }
    },
    "text": "He argued  -COL-   -LBQ-  The dramatic changes they 're touting , they 're not that dramatic ."
  ```
---
- parsing error again. 
- *it* and *she* both marked as subject of *welcome* : 
*U.S. diplomats in London , responsible for the North , made **it** clear that **she** was not really **welcome** , that she was interfering*
  ```text
      "fillers": {
        "S": "it",
        "NOT": "not",
        "BE": "be",
        "ADV": "really",
        "ADJ": "welcome"
      }
    ...
        "fillers": {
        "S": "she",
        "NOT": "not",
        "BE": "be",
        "ADV": "really",
        "ADJ": "welcome"
      }
    },
    "text": "U.S. diplomats in London , responsible for the North , made it clear that she was not really welcome , that she was interfering ."
  ```
---
- another misparse of `nsubj`, though another "resumptive" like case
- *People* marked as subject, due to confusing movement
- ***People** who want to help you -- **it** 's not necessarily **smart** to spit in their face*

  ```text
      "fillers": {
        "S": "people",
        "NOT": "not",
        "BE": "be",
        "ADV": "necessarily",
        "ADJ": "smart"
      }
    ...
      "fillers": {
        "S": "it",
        "NOT": "not",
        "BE": "be",
        "ADV": "necessarily",
        "ADJ": "smart"
      }
    },
    "text": "-LBQ-  People who want to help you -- it 's not necessarily smart to spit in their face ,  -RDQ-  he said .
  ```
---
- Another correct parse due to resumptive pronoun, but will not have any bearing on predicate/trigger data
- *The **way** I am playing , **it** 's not too **bad** for a 44-year-old has-been*

  ```text
    "fillers": {
        "S": "way",
        "NOT": "not",
        "BE": "be",
        "ADV": "too",
        "ADJ": "bad"
      }
      ...
    "fillers": {
        "S": "it",
        "NOT": "not",
        "BE": "be",
        "ADV": "too",
        "ADJ": "bad"
      }
    },
    "text": "The way I am playing , it 's not too bad for a 44-year-old has-been .  -RDQ-"
  },
  ```
---
- more resumptives, still a duplicate subject
- *The **city** , **it** is not so **complicated***
  ```text
    "fillers": {
        "S": "city",
        "NOT": "not",
        "BE": "be",
        "ADV": "so",
        "ADJ": "complicated"
      }
      ...
    "fillers": {
        "S": "it",
        "NOT": "not",
        "BE": "be",
        "ADV": "so",
        "ADJ": "complicated"
      }
    },
    "text": "-LBQ-  The city , it is not so complicated ,  -RDQ-  said Macsuara ."
  ```
---
- another `make it x that y is (trigger) [adv] [adj]` case, where *it* is marked as `nsubj`
- *...whose peace-loving brotherhood of residents make **it** amply clear **he** 's not very **welcome** , anyway*

  ```text
    "fillers": {
        "S": "it",
        "NOT": "not",
        "BE": "be",
        "ADV": "very",
        "ADJ": "welcome"
      }
    ...
    "fillers": {
        "S": "he",
        "NOT": "not",
        "BE": "be",
        "ADV": "very",
        "ADJ": "welcome"
      }
    },
    "text": "He ca n't wait , for example , to get out of that silly desert commune -- whose peace-loving brotherhood of residents make it amply clear he 's not very welcome , anyway ."
  ```

---

- `nsubj` error, this time due to sentential adverb
- has no bearing on target data, provided correct is still being caught
- ***Technically** , **that** 's not totally **accurate***

  ```text
    "fillers": {
        "S": "Technically",
        "NOT": "not",
        "BE": "be",
        "ADV": "totally",
        "ADJ": "accurate"
    ...
    "fillers": {
        "S": "that",
        "NOT": "not",
        "BE": "be",
        "ADV": "totally",
        "ADJ": "accurate"
      }
    },
    "text": "Technically , that 's not totally accurate ."
  ```
  
---

- another subject parsing error/duplicate, this one due to *matter* being incorrectly parsed as a noun (and an assumption of a resumptive pronoun?)
- *In most of the ways that **matter** , **he** is not that **different** from many other top-level Wells Fargo employees*

  ```text
    "fillers": {
      "S": "matter",
      "NOT": "not",
      "BE": "be",
      "ADV": "that",
      "ADJ": "different"
    ...
    "fillers": {
        "S": "he",
        "NOT": "not",
        "BE": "be",
        "ADV": "that",
        "ADJ": "different"
      }
    },
    "text": "In most of the ways that matter , he is not that different from many other top-level Wells Fargo employees ."
  ```

---

- 
- 

  ```text


  ```


---

- 
- 

  ```text


  ```


---

- 
- 

  ```text


  ```