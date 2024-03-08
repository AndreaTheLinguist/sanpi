# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/combined_POSmirror-NEGmirror/complement/diff_all-combinedMIRROR_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## Input Data

| adj_form_lower |      SUM |    very |    more | ... | cosmetically | second-most | pointedly |
|:--------------:|---------:|--------:|--------:|----:|-------------:|------------:|----------:|
|      SUM       | 81323407 | 9715385 | 9008523 | ... |          837 |         863 |       841 |
|      many      |  2206304 |   21200 |     370 | ... |            0 |           0 |         0 |
|   important    |  2150654 |  352860 |  281483 | ... |            9 |         101 |         0 |
|      ...       |      ... |     ... |     ... | ... |          ... |         ... |       ... |
|   contiguous   |      851 |       4 |     104 | ... |            0 |           0 |         0 |
|    panicked    |      848 |      50 |     154 | ... |            0 |           0 |         0 |
|   oversized    |      849 |      32 |      43 | ... |            0 |           0 |         0 |

## Stacked

|   | adj_form_lower | adv_form_lower | raw_frq |
|--:|:---------------|:---------------|--------:|
| 0 | many           | very           |   21200 |
| 1 | many           | more           |     370 |
| 2 | many           | most           |     140 |
| 3 | many           | so             | 1191658 |
| 4 | many           | not            |   58317 |
| 5 | many           | as             |  432879 |

...

|         | adj_form_lower | adv_form_lower | raw_frq |
|--------:|:---------------|:---------------|--------:|
| 3913464 | oversized      | on             |       0 |
| 3913465 | oversized      | emphatically   |       0 |
| 3913466 | oversized      | touchingly     |       0 |
| 3913467 | oversized      | cosmetically   |       0 |
| 3913468 | oversized      | second-most    |       0 |
| 3913469 | oversized      | pointedly      |       0 |

## Formatted Output Sample (top 20 bigrams)

```log
1191658 so      many
747279  most    important
614120  so      much
578002  too     much
499454  very    good
488890  more    likely
464263  not     sure
448909  too     many
432879  as      many
398361  most    popular
354584  as      much
353368  much    more
352860  very    important
312896  most    recent
291916  much    better
281483  more    important
272631  most    common
256140  really  good
241415  pretty  good
240439  very    little
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/combined_POSmirror-NEGmirror/complement/ucs_format/diff_all-combinedMIRROR_adj-x-adv_frq-thr0-001p.35f=868+.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:17:16 2024
  * total time elapsed: 00:00:01.329
