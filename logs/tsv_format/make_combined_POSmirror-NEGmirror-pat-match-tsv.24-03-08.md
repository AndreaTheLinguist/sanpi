# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/combined_POSmirror-NEGmirror/ALL-WORDS_adj-x-adv_thr0-001p.35f.pkl.gz`

## Input Data

| adj_form_lower   | SUM     | very   | more   | ...   | cosmetically   | second-most   | pointedly   |
|:----------------:|--------:|-------:|-------:|------:|---------------:|--------------:|------------:|
| SUM              | 1960936 | 198047 | 312474 | ...   | 32             | 6             | 27          |
| many             | 4083    | 37     | 3      | ...   | 0              | 0             | 0           |
| important        | 48793   | 6750   | 25121  | ...   | 0              | 4             | 0           |
| ...              | ...     | ...    | ...    | ...   | ...            | ...           | ...         |
| contiguous       | 20      | 0      | 2      | ...   | 0              | 0             | 0           |
| panicked         | 23      | 4      | 5      | ...   | 0              | 0             | 0           |
| oversized        | 21      | 0      | 2      | ...   | 0              | 0             | 0           |

## Stacked

|    | adj_form_lower   | adv_form_lower   |   raw_frq |
|---:|:-----------------|:-----------------|----------:|
|  0 | many             | very             |        37 |
|  1 | many             | more             |         3 |
|  2 | many             | most             |         0 |
|  3 | many             | so               |       206 |
|  4 | many             | not              |       125 |
|  5 | many             | as               |      1752 |

...

|         | adj_form_lower   | adv_form_lower   |   raw_frq |
|--------:|:-----------------|:-----------------|----------:|
| 3913464 | oversized        | on               |         0 |
| 3913465 | oversized        | emphatically     |         0 |
| 3913466 | oversized        | touchingly       |         0 |
| 3913467 | oversized        | cosmetically     |         0 |
| 3913468 | oversized        | second-most      |         0 |
| 3913469 | oversized        | pointedly        |         0 |

## Formatted Output Sample (top 20 bigrams)

```log
25121   more    important
17656   as      simple
13552   too     late
9511    more    likely
9347    completely      different
8045    very    good
8000    too     easy
7564    too     familiar
7408    too     small
6971    even    better
6875    very    different
6795    even    worse
6773    as      good
6750    very    important
6293    more    difficult
5517    too     early
5437    too     common
5231    very    special
5188    more    interesting
5182    too     much
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/combined_POSmirror-NEGmirror/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:22:29 2024
  * total time elapsed: 00:00:00.782
