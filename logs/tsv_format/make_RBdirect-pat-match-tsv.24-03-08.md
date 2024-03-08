# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/RBdirect/ALL-WORDS_adj-x-adv_thr0-001p.35f.pkl.gz`

## Input Data

| adj_form_lower   | SUM     | very   | more   | ...   | second-most   | cosmetically   | pointedly   |
|:----------------:|--------:|-------:|-------:|------:|--------------:|---------------:|------------:|
| SUM              | 3148010 | 191043 | 166176 | ...   | 0             | 54             | 15          |
| many             | 14145   | 1925   | 2      | ...   | 0             | 0              | 0           |
| important        | 49871   | 1856   | 15208  | ...   | 0             | 0              | 0           |
| ...              | ...     | ...    | ...    | ...   | ...           | ...            | ...         |
| contiguous       | 57      | 1      | 0      | ...   | 0             | 0              | 0           |
| panicked         | 39      | 1      | 6      | ...   | 0             | 0              | 0           |
| oversized        | 16      | 0      | 0      | ...   | 0             | 0              | 0           |

## Stacked

|    | adj_form_lower   | adv_form_lower   |   raw_frq |
|---:|:-----------------|:-----------------|----------:|
|  0 | many             | very             |      1925 |
|  1 | many             | more             |         2 |
|  2 | many             | most             |         0 |
|  3 | many             | so               |      2128 |
|  4 | many             | not              |        14 |
|  5 | many             | as               |      3246 |

...

|         | adj_form_lower   | adv_form_lower   |   raw_frq |
|--------:|:-----------------|:-----------------|----------:|
| 3913464 | oversized        | touchingly       |         0 |
| 3913465 | oversized        | on               |         0 |
| 3913466 | oversized        | emphatically     |         0 |
| 3913467 | oversized        | second-most      |         0 |
| 3913468 | oversized        | cosmetically     |         0 |
| 3913469 | oversized        | pointedly        |         0 |

## Formatted Output Sample (top 20 bigrams)

```log
44885   as      good
30349   very    good
27740   as      bad
26584   so      sure
26156   quite   sure
25854   too     late
25276   immediately     clear
24574   always  easy
23376   as      easy
21925   so      much
21352   so      bad
21297   immediately     available
19520   too     bad
18002   so      good
17898   really  sure
17701   even    close
17596   so      easy
16535   that    bad
15208   more    important
14753   as      simple
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/RBdirect/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:22:27 2024
  * total time elapsed: 00:00:00.739
