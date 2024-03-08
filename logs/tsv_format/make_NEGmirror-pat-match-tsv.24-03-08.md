# Reformatting co-occurence data for UCS analysis

* Loading from `results/freq_out/NEGmirror/ALL-WORDS_adj-x-adv_thr0-001p.35f.pkl.gz`

## Input Data

| adj_form_lower   | SUM    | very   | more   | ...   | second-most   | cosmetically   | pointedly   |
|:----------------:|-------:|-------:|-------:|------:|--------------:|---------------:|------------:|
| SUM              | 285435 | 8861   | 77335  | ...   | 0             | 4              | 2           |
| many             | 305    | 7      | 0      | ...   | 0             | 0              | 0           |
| important        | 14968  | 104    | 12396  | ...   | 0             | 0              | 0           |
| ...              | ...    | ...    | ...    | ...   | ...           | ...            | ...         |
| contiguous       | 4      | 0      | 0      | ...   | 0             | 0              | 0           |
| panicked         | 5      | 1      | 3      | ...   | 0             | 0              | 0           |
| oversized        | 3      | 0      | 0      | ...   | 0             | 0              | 0           |

## Stacked

|    | adj_form_lower   | adv_form_lower   |   raw_frq |
|---:|:-----------------|:-----------------|----------:|
|  0 | many             | very             |         7 |
|  1 | many             | more             |         0 |
|  2 | many             | most             |         0 |
|  3 | many             | so               |        97 |
|  4 | many             | not              |         6 |
|  5 | many             | as               |        63 |

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
12396   more    important
11087   too     late
5200    too     early
3471    as      good
2967    quite   sure
2636    so      easy
2365    too     old
1895    more    frustrating
1572    very    good
1521    inherently      wrong
1438    more    exciting
1326    as      bad
1293    too     pleased
1291    more    evident
1259    more    satisfying
1185    too     happy
1089    as      simple
1083    more    beautiful
1062    more    true
1045    as      important
...
```

* Simple tab-delimited counts saved as `.tsv`:
  * path: `results/freq_out/NEGmirror/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv`

* Program Completed ✓
  * current time: Fri Mar  8 17:22:24 2024
  * total time elapsed: 00:00:00.276
