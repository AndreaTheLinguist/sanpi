# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/RBdirect/complement/diff_all-RBdirect_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## Input Data

| adj_form_lower |      SUM |    very |    more | ... | second-most | cosmetically | pointedly |
|:--------------:|---------:|--------:|--------:|----:|------------:|-------------:|----------:|
|      SUM       | 80136333 | 9722389 | 9154821 | ... |         869 |          815 |       853 |
|      many      |  2196242 |   19312 |     371 | ... |           0 |            0 |         0 |
|   important    |  2149576 |  357754 |  291396 | ... |         105 |            9 |         0 |
|      ...       |      ... |     ... |     ... | ... |         ... |          ... |       ... |
|   contiguous   |      814 |       3 |     106 | ... |           0 |            0 |         0 |
|    panicked    |      832 |      53 |     153 | ... |           0 |            0 |         0 |
|   oversized    |      854 |      32 |      45 | ... |           0 |            0 |         0 |

## Stacked

|   | adj_form_lower | adv_form_lower | raw_frq |
|--:|:---------------|:---------------|--------:|
| 0 | many           | very           |   19312 |
| 1 | many           | more           |     371 |
| 2 | many           | most           |     140 |
| 3 | many           | so             | 1189736 |
| 4 | many           | not            |   58428 |
| 5 | many           | as             |  431385 |

...

|         | adj_form_lower | adv_form_lower | raw_frq |
|--------:|:---------------|:---------------|--------:|
| 3913464 | oversized      | touchingly     |       0 |
| 3913465 | oversized      | on             |       0 |
| 3913466 | oversized      | emphatically   |       0 |
| 3913467 | oversized      | second-most    |       0 |
| 3913468 | oversized      | cosmetically   |       0 |
| 3913469 | oversized      | pointedly      |       0 |

## Formatted Output Sample (top 20 bigrams)

```log
1189736 so      many
747570  most    important
592727  so      much
570546  too     much
495783  more    likely
477150  very    good
466983  not     sure
444021  too     many
431385  as      many
398297  most    popular
357754  very    important
349470  as      much
349076  much    more
313107  most    recent
291396  more    important
283999  much    better
272621  most    common
257760  really  good
243512  pretty  good
241660  very    little
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/RBdirect/complement/ucs_format/diff_all-RBdirect_adj-x-adv_frq-thr0-001p.35f=868+.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:17:13 2024
  * total time elapsed: 00:00:02.297
