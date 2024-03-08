# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/POSmirror/ALL-WORDS_adj-x-adv_thr0-001p.35f.pkl.gz`

## Input Data

| adj_form_lower   | SUM     | very   | more   | ...   | second-most   | cosmetically   | pointedly   |
|:----------------:|--------:|-------:|-------:|------:|--------------:|---------------:|------------:|
| SUM              | 1675501 | 189186 | 235139 | ...   | 6             | 28             | 25          |
| many             | 3778    | 30     | 3      | ...   | 0             | 0              | 0           |
| important        | 33825   | 6646   | 12725  | ...   | 4             | 0              | 0           |
| ...              | ...     | ...    | ...    | ...   | ...           | ...            | ...         |
| contiguous       | 16      | 0      | 2      | ...   | 0             | 0              | 0           |
| panicked         | 18      | 3      | 2      | ...   | 0             | 0              | 0           |
| oversized        | 18      | 0      | 2      | ...   | 0             | 0              | 0           |

## Stacked

|    | adj_form_lower   | adv_form_lower   |   raw_frq |
|---:|:-----------------|:-----------------|----------:|
|  0 | many             | very             |        30 |
|  1 | many             | more             |         3 |
|  2 | many             | most             |         0 |
|  3 | many             | so               |       109 |
|  4 | many             | not              |       119 |
|  5 | many             | as               |      1689 |

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
16567   as      simple
12725   more    important
9322    completely      different
9179    more    likely
7879    too     easy
7533    too     familiar
6959    even    better
6824    very    different
6687    even    worse
6670    too     small
6646    very    important
6473    very    good
5518    more    difficult
5423    too     common
5141    very    special
4861    more    interesting
4688    not     right
4437    too     much
4361    n't     right
4290    very    close
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/POSmirror/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:22:26 2024
  * total time elapsed: 00:00:00.445
