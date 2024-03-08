# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/POSmirror/complement/diff_all-POSmirror_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## Input Data

| adj_form_lower |      SUM |    very |    more | ... | second-most | cosmetically | pointedly |
|:--------------:|---------:|--------:|--------:|----:|------------:|-------------:|----------:|
|      SUM       | 81608842 | 9724246 | 9085858 | ... |         863 |          841 |       843 |
|      many      |  2206609 |   21207 |     370 | ... |           0 |            0 |         0 |
|   important    |  2165622 |  352964 |  293879 | ... |         101 |            9 |         0 |
|      ...       |      ... |     ... |     ... | ... |         ... |          ... |       ... |
|   contiguous   |      855 |       4 |     104 | ... |           0 |            0 |         0 |
|    panicked    |      853 |      51 |     157 | ... |           0 |            0 |         0 |
|   oversized    |      852 |      32 |      43 | ... |           0 |            0 |         0 |

## Stacked

|   | adj_form_lower | adv_form_lower | raw_frq |
|--:|:---------------|:---------------|--------:|
| 0 | many           | very           |   21207 |
| 1 | many           | more           |     370 |
| 2 | many           | most           |     140 |
| 3 | many           | so             | 1191755 |
| 4 | many           | not            |   58323 |
| 5 | many           | as             |  432942 |

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
1191755 so      many
747340  most    important
614339  so      much
578747  too     much
501026  very    good
489222  more    likely
464291  not     sure
449022  too     many
432942  as      many
398412  most    popular
354710  as      much
353819  much    more
352964  very    important
312901  most    recent
293879  more    important
292240  much    better
272634  most    common
256441  really  good
241427  pretty  good
240469  very    little
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/POSmirror/complement/ucs_format/diff_all-POSmirror_adj-x-adv_frq-thr0-001p.35f=868+.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:17:10 2024
  * total time elapsed: 00:00:02.627
