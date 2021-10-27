# prefilter

## `ADV ADJ` prefilter

- this would be used to:
  - create corpora subsets:
    - sentences without adverbial modification of an adjective would be ignored
    - if run once on all corpus chunks, could create a smaller sample to do full searches on
    - would need to consider if preceding and following sentences would need to be accessed for evaluation of interpretation
  - get a more inclusive count of adj adv collocations
    - this may not be wanted if none of the contexts would consider pre-nominal APs

```js
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
}
```
