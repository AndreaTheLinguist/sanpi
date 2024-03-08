# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/NEGmirror/complement/diff_all-NEGmirror_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## Input Data

| adj_form_lower |      SUM |    very |    more | ... | second-most | cosmetically | pointedly |
|:--------------:|---------:|--------:|--------:|----:|------------:|-------------:|----------:|
|      SUM       | 82998908 | 9904571 | 9243662 | ... |         869 |          865 |       866 |
|      many      |  2210082 |   21230 |     373 | ... |           0 |            0 |         0 |
|   important    |  2184479 |  359506 |  294208 | ... |         105 |            9 |         0 |
|      ...       |      ... |     ... |     ... | ... |         ... |          ... |       ... |
|   contiguous   |      867 |       4 |     106 | ... |           0 |            0 |         0 |
|    panicked    |      866 |      53 |     156 | ... |           0 |            0 |         0 |
|   oversized    |      867 |      32 |      45 | ... |           0 |            0 |         0 |

## Stacked

|   | adj_form_lower | adv_form_lower | raw_frq |
|--:|:---------------|:---------------|--------:|
| 0 | many           | very           |   21230 |
| 1 | many           | more           |     373 |
| 2 | many           | most           |     140 |
| 3 | many           | so             | 1191767 |
| 4 | many           | not            |   58436 |
| 5 | many           | as             |  434568 |

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
1191767 so      many
748472  most    important
614433  so      much
582439  too     much
505927  very    good
498069  more    likely
467185  not     sure
450081  too     many
434568  as      many
398904  most    popular
359506  very    important
355242  as      much
355204  much    more
313180  most    recent
294900  much    better
294208  more    important
272784  most    common
259980  really  good
243680  pretty  good
241701  very    little
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/NEGmirror/complement/ucs_format/diff_all-NEGmirror_adj-x-adv_frq-thr0-001p.35f=868+.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:17:07 2024
  * total time elapsed: 00:00:02.397
