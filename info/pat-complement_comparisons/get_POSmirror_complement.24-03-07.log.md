# Comparing Bigram Frequencies by Polarity

- for `35` corpus input `.conll` directories containing source `.conllu` files
- with word types limited to only those that account for at least $0.001\%$ of the cleaned dataset (as sourced from 35 corpus file inputs)
- file identifier = `thr0-001p.35f`
- pattern matches restricted to only token word types with at least `868` total tokens across all combinations

- Selected Paths
  - `/share/compling/projects/sanpi/results/freq_out/POSmirror/all-frq_adj-x-adv_thr0-001p.35f.pkl.gz`
  - `/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## _`POSmirror`_ Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for`stats_all-frq_adj-x-adv_thr0-001p.35f` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/POSmirror/descriptive_stats/ADV-stats_all-frq_adj-x-adv_thr0-001p.35f.csv`
  - time elapsed: 00:00:00.838

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| electrically     | 3,890 |    0 |   0 |   0 |   0 |   0 |   0 |   7 |    22 |        24 |     7 |        0 |           0 |           0 |              1 |              1 |
| crystal          | 3,890 |    0 |   2 |   0 |   0 |   0 |   0 | 148 |   148 |        62 |   148 |        0 |           0 |           0 |              1 |              1 |
| admirably        | 3,890 |    0 |   0 |   0 |   0 |   0 |   0 |   4 |    56 |        11 |     4 |        0 |           0 |           0 |              1 |              1 |
| deathly          | 3,890 |    0 |   1 |   0 |   0 |   0 |   0 |  44 |   120 |        27 |    44 |        0 |           0 |           0 |              1 |              1 |
| daily            | 3,890 |    0 |   0 |   0 |   0 |   0 |   0 |   2 |     8 |        27 |     2 |        0 |           0 |           0 |              1 |              1 |
| secretly         | 3,890 |    0 |   1 |   0 |   0 |   0 |   0 |  20 |   201 |        10 |    20 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adv_form_lowers |
|:------------|------------------------------:|
| count       |                         3,890 |
| mean        |                           431 |
| std         |                         1,620 |
| min         |                             1 |
| 25%         |                            31 |
| 50%         |                            73 |
| 75%         |                           230 |
| max         |                        38,602 |
| total       |                     1,675,501 |
| var_coeff   |                             4 |
| range       |                        38,601 |
| IQ_range    |                           199 |
| upper_fence |                           528 |
| lower_fence |                          -268 |

### Descriptive Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for`stats_all-frq_adj-x-adv_thr0-001p.35f` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/POSmirror/descriptive_stats/ADJ-stats_all-frq_adj-x-adv_thr0-001p.35f.csv`
  - time elapsed: 00:00:00.351

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| peaceful         | 1,005 |    1 |   6 |   0 |   0 |   0 |   0 | 139 |   566 |        11 |   139 |        0 |           0 |           0 |              1 |              1 |
| organic          | 1,005 |    0 |   4 |   0 |   0 |   0 |   0 |  93 |   385 |        10 |    93 |        0 |           0 |           0 |              1 |              1 |
| creative         | 1,005 |    2 |  26 |   0 |   0 |   0 |   0 | 739 | 2,114 |        12 |   739 |        0 |           0 |           0 |              1 |              1 |
| heterosexual     | 1,005 |    0 |   0 |   0 |   0 |   0 |   0 |   7 |    46 |         9 |     7 |        0 |           0 |           0 |              1 |              1 |
| veiled           | 1,005 |    0 |   0 |   0 |   0 |   0 |   0 |   3 |    11 |        14 |     3 |        0 |           0 |           0 |              1 |              1 |
| macho            | 1,005 |    0 |   1 |   0 |   0 |   0 |   0 |  12 |    62 |        10 |    12 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adj_form_lowers |
|:------------|------------------------------:|
| count       |                         1,005 |
| mean        |                         1,667 |
| std         |                        12,315 |
| min         |                             1 |
| 25%         |                            33 |
| 50%         |                            81 |
| 75%         |                           291 |
| max         |                       235,139 |
| total       |                     1,675,501 |
| var_coeff   |                             7 |
| range       |                       235,138 |
| IQ_range    |                           258 |
| upper_fence |                           678 |
| lower_fence |                          -354 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/POSmirror/images/sample-heatmap_all-frq_adj-x-adv_thr0-001p.35f.pkl.png`

### Full Table Preview of _`POSmirror`_ Frequencies

| `adj_form_lower` | `SUM`   | more   | very   | too    | so     | as    | ... | anywhere | chock | unseasonably | farther | namely | lot |
|:-----------------|:--------|:-------|:-------|:-------|:-------|:------|:----|:---------|:------|:-------------|:--------|:-------|:----|
| `SUM`            | 1675501 | 235139 | 189186 | 140198 | 118563 | 94706 | ... | 3        | 3     | 2            | 2       | 1      | 1   |
| different        | 38602   | 155    | 6824   | 135    | 2049   | 155   | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| important        | 33825   | 12725  | 6646   | 235    | 1475   | 3007  | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| good             | 29290   | 76     | 6473   | 1451   | 2482   | 3302  | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| simple           | 24954   | 430    | 1917   | 383    | 2431   | 16567 | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| wrong            | 18435   | 64     | 3091   | 10     | 398    | 67    | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| ...              | ...     | ...    | ...    | ...    | ...    | ...   | ... | ...      | ...   | ...          | ...     | ...    | ... |
| storied          | 1       | 0      | 0      | 0      | 1      | 0     | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| aging            | 1       | 0      | 0      | 0      | 0      | 0     | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| booming          | 1       | 0      | 0      | 0      | 0      | 0     | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| marrow           | 1       | 0      | 0      | 0      | 0      | 0     | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| southerly        | 1       | 1      | 0      | 0      | 0      | 0     | ... | 0        | 0     | 0            | 0       | 0      | 0   |
| away             | 1       | 0      | 0      | 0      | 0      | 0     | ... | 0        | 0     | 0            | 0       | 0      | 0   |

### (Semi-)Random Sample of _`POSmirror`_ Frequencies

| `adj_form_lower` |     `SUM` |      so | highly | plain | particularly | definitely | financially | over |
|:-----------------|----------:|--------:|-------:|------:|-------------:|-----------:|------------:|-----:|
| `SUM`            | 1,675,501 | 118,563 |  9,715 | 5,880 |        5,533 |      1,610 |         961 |  495 |
| satisfied        |     2,342 |      12 |     51 |     1 |            2 |          1 |           0 |    0 |
| affordable       |     1,797 |      26 |     18 |     0 |            0 |          1 |           3 |    0 |
| involved         |     1,755 |     134 |     13 |     0 |            3 |          0 |           1 |    0 |
| clean            |     1,685 |     194 |      0 |     0 |            2 |          2 |           0 |    1 |
| less             |     1,651 |      16 |      0 |     0 |            0 |          1 |           0 |    1 |
| dependent        |     1,399 |      80 |     99 |     0 |            5 |          0 |          54 |    3 |
| tender           |     1,174 |      49 |      1 |     1 |            4 |          0 |           0 |    0 |

## _ALL_ (`POSmirror` and non-`POSmirror`) Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for stats_all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADV-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.526

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% |   max |  total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|------:|-------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| exponentially    | 3,894 |    1 |  22 |   0 |   0 |   0 |   0 |   798 |  5,208 |        17 |   798 |        0 |           0 |           0 |              1 |              1 |
| impressively     | 3,894 |    2 |  15 |   0 |   0 |   0 |   1 |   594 |  8,925 |         6 |   594 |        1 |           2 |          -2 |              2 |              1 |
| cosmetically     | 3,894 |    0 |   3 |   0 |   0 |   0 |   0 |   118 |    869 |        14 |   118 |        0 |           0 |           0 |              1 |              1 |
| otherwise        | 3,894 |   25 | 104 |   0 |   1 |   4 |  14 | 4,243 | 98,248 |         4 | 4,243 |       13 |          34 |         -18 |              6 |              3 |
| cheerfully       | 3,894 |    0 |   1 |   0 |   0 |   0 |   0 |    27 |  1,371 |         4 |    27 |        0 |           0 |           0 |              1 |              1 |
| home             | 3,894 |    1 |   9 |   0 |   0 |   0 |   0 |   442 |  2,088 |        17 |   442 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adv_form_lowers |
|:------------|------------------------------:|
| count       |                         3,894 |
| mean        |                        21,388 |
| std         |                        91,460 |
| min         |                           870 |
| 25%         |                         1,637 |
| 50%         |                         3,466 |
| 75%         |                        10,673 |
| max         |                     2,210,387 |
| total       |                    83,284,343 |
| var_coeff   |                             4 |
| range       |                     2,209,517 |
| IQ_range    |                         9,036 |
| upper_fence |                        24,227 |
| lower_fence |                       -11,917 |

### Descriptive Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for stats_all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADJ-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.492

Sample `adj_form_lower` Stats

| `adj_form_lower` | count |  mean |    std | min | 25% | 50% | 75% |     max |     total | var_coeff |   range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|------:|-------:|----:|----:|----:|----:|--------:|----------:|----------:|--------:|---------:|------------:|------------:|---------------:|---------------:|
| original         | 1,005 |    45 |    345 |   0 |   0 |   1 |   5 |   7,624 |    45,226 |         8 |   7,624 |        5 |          12 |          -8 |              3 |              2 |
| compelling       | 1,005 |    71 |    759 |   0 |   0 |   1 |   6 |  17,062 |    71,698 |        11 |  17,062 |        6 |          15 |          -9 |              4 |              2 |
| prominent        | 1,005 |   106 |  2,132 |   0 |   0 |   0 |   2 |  64,329 |   106,697 |        20 |  64,329 |        2 |           5 |          -3 |              2 |              1 |
| important        | 1,005 | 2,188 | 28,559 |   0 |   0 |   4 |  32 | 748,533 | 2,199,447 |        13 | 748,533 |       32 |          80 |         -48 |             10 |              3 |
| untapped         | 1,005 |     4 |     53 |   0 |   0 |   0 |   0 |   1,446 |     4,406 |        12 |   1,446 |        0 |           0 |           0 |              1 |              1 |
| communicative    | 1,005 |     2 |     24 |   0 |   0 |   0 |   0 |     582 |     2,065 |        12 |     582 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adj_form_lowers |
|:------------|------------------------------:|
| count       |                         1,005 |
| mean        |                        82,870 |
| std         |                       581,924 |
| min         |                           868 |
| 25%         |                         1,705 |
| 50%         |                         4,049 |
| 75%         |                        15,767 |
| max         |                     9,913,432 |
| total       |                    83,284,343 |
| var_coeff   |                             7 |
| range       |                     9,912,564 |
| IQ_range    |                        14,062 |
| upper_fence |                        36,860 |
| lower_fence |                       -19,388 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/RBXadj/images/sample-heatmap_all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.png`

### Full Table Preview of _All_ Frequencies

|              |    `SUM` |    very |    more | ... | second-most | cosmetically | pointedly |
|:-------------|---------:|--------:|--------:|----:|------------:|-------------:|----------:|
| `SUM`        | 83284343 | 9913432 | 9320997 | ... |         869 |          869 |       868 |
| many         |  2210387 |   21237 |     373 | ... |           0 |            0 |         0 |
| important    |  2199447 |  359610 |  306604 | ... |         105 |            9 |         0 |
| good         |  2030480 |  507499 |   18902 | ... |           0 |            7 |         0 |
| much         |  1776924 |   42365 |     102 | ... |           0 |            0 |         1 |
| likely       |  1048364 |   35899 |  498401 | ... |          12 |            0 |         0 |
| ...          |      ... |     ... |     ... | ... |         ... |          ... |       ... |
| intermittent |      872 |      84 |     171 | ... |           0 |            0 |         0 |
| untrained    |      872 |       9 |      10 | ... |           0 |            0 |         0 |
| carnal       |      872 |      34 |     150 | ... |           0 |            0 |         0 |
| contiguous   |      871 |       4 |     106 | ... |           0 |            0 |         0 |
| panicked     |      871 |      54 |     159 | ... |           0 |            0 |         0 |
| oversized    |      870 |      32 |      45 | ... |           0 |            0 |         0 |

[13 rows x 13 columns]

### (Semi-)Random Sample of _ALL_ Frequencies

| `adj_form_lower` |      `SUM` | completely |   never | surprisingly | indeed |   over | horribly |
|:-----------------|-----------:|-----------:|--------:|-------------:|-------:|-------:|---------:|
| `SUM`            | 83,284,343 |    619,769 | 129,653 |      119,814 | 41,540 | 24,419 |   20,539 |
| wrong            |    185,695 |      9,525 |   1,531 |           15 |    139 |     20 |    7,500 |
| positive         |    184,198 |        462 |      75 |          523 |     43 |      4 |        0 |
| pleased          |    169,709 |        247 |     120 |           47 |     51 |     21 |        1 |
| sensitive        |    143,415 |         18 |       5 |          136 |     30 |    202 |        1 |
| present          |    125,577 |        435 |     299 |           16 |    220 |      4 |        0 |
| skilled          |     75,095 |         38 |       6 |           37 |      7 |      2 |        0 |

👀 sanity dimension checks

|            dataframe | # rows | # columns |
|---------------------:|-------:|----------:|
|     only `POSmirror` |   3891 |      1006 |
|                  ALL |   3895 |      1006 |
| adjusted `POSmirror` |   3895 |      1006 |

## Words with 0 tokens in the `POSmirror` results

### Adjectives

| `adj_form_lower` | SUM_POSmirror | `SUM` |
|:-----------------|--------------:|------:|
| wanted           |             0 | 3,416 |
| halfway          |             0 | 1,721 |
| bustling         |             0 | 1,273 |
| famed            |             0 |   879 |

### Adverbs

| `adv_form_lower` | SUM_POSmirror | `SUM` |
|------------------|---------------|-------|
| n/a              |               |       |

## The Difference

| `adj_form_lower` | `SUM`    | very    | more    | ... | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:----|:------------|:-------------|:----------|
| `SUM`            | 81608842 | 9724246 | 9085858 | ... | 863         | 841          | 843       |
| many             | 2206609  | 21207   | 370     | ... | 0           | 0            | 0         |
| important        | 2165622  | 352964  | 293879  | ... | 101         | 9            | 0         |
| ...              | ...      | ...     | ...     | ... | ...         | ...          | ...       |
| contiguous       | 855      | 4       | 104     | ... | 0           | 0            | 0         |
| panicked         | 853      | 51      | 157     | ... | 0           | 0            | 0         |
| oversized        | 852      | 32      | 43      | ... | 0           | 0            | 0         |

### Descriptive _Complement_ Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for stats_diff_POSmirror-all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/POSmirror/complement/descriptive_stats/ADV-stats_diff_POSmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.625

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean |   std | min | 25% | 50% | 75% |     max |     total | var_coeff |   range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|------:|----:|----:|----:|----:|--------:|----------:|----------:|--------:|---------:|------------:|------------:|---------------:|---------------:|
| commonly         | 3,894 |    2 |    48 |   0 |   0 |   0 |   1 |   2,943 |     7,812 |        24 |   2,943 |        1 |           2 |          -2 |              1 |              1 |
| less             | 3,894 |  317 | 2,591 |   0 |  11 |  41 | 136 | 138,199 | 1,232,558 |         8 | 138,199 |      125 |         324 |        -176 |             43 |             10 |
| mathematically   | 3,894 |    1 |    16 |   0 |   0 |   0 |   0 |     802 |     4,585 |        14 |     802 |        0 |           0 |           0 |              1 |              1 |
| sometime         | 3,894 |    0 |     1 |   0 |   0 |   0 |   0 |      34 |     1,475 |         4 |      34 |        0 |           0 |           0 |              1 |              1 |
| deeply           | 3,894 |   43 |   371 |   0 |   0 |   1 |   9 |  14,624 |   167,811 |         9 |  14,624 |        9 |          22 |         -14 |              4 |              2 |
| timelessly       | 3,894 |    0 |     4 |   0 |   0 |   0 |   0 |     198 |       995 |        16 |     198 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adv_form_lowers |
|:------------|------------------------------:|
| count       |                         3,894 |
| mean        |                        20,958 |
| std         |                        90,196 |
| min         |                           567 |
| 25%         |                         1,603 |
| 50%         |                         3,392 |
| 75%         |                        10,429 |
| max         |                     2,206,609 |
| total       |                    81,608,842 |
| var_coeff   |                             4 |
| range       |                     2,206,042 |
| IQ_range    |                         8,826 |
| upper_fence |                        23,668 |
| lower_fence |                       -11,636 |

### Descriptive _Complement_ Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for stats_diff_POSmirror-all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/POSmirror/complement/descriptive_stats/ADJ-stats_diff_POSmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.158

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean |   std | min | 25% | 50% | 75% |     max |   total | var_coeff |   range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|------:|----:|----:|----:|----:|--------:|--------:|----------:|--------:|---------:|------------:|------------:|---------------:|---------------:|
| northern         | 1,005 |    3 |    53 |   0 |   0 |   0 |   0 |   1,319 |   3,503 |        15 |   1,319 |        0 |           0 |           0 |              1 |              1 |
| hot              | 1,005 |  164 | 1,550 |   0 |   0 |   2 |  14 |  30,515 | 165,129 |         9 |  30,515 |       14 |          35 |         -21 |              6 |              2 |
| beautiful        | 1,005 |  309 | 3,664 |   0 |   1 |   5 |  27 | 104,352 | 310,051 |        12 | 104,352 |       26 |          66 |         -38 |              9 |              3 |
| gigantic         | 1,005 |    2 |    15 |   0 |   0 |   0 |   0 |     257 |   2,051 |         7 |     257 |        0 |           0 |           0 |              1 |              1 |
| threatening      | 1,005 |   13 |   139 |   0 |   0 |   0 |   1 |   3,217 |  13,325 |        11 |   3,217 |        1 |           2 |          -2 |              2 |              1 |
| crazier          | 1,005 |    3 |    67 |   0 |   0 |   0 |   0 |   2,097 |   2,966 |        23 |   2,097 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adj_form_lowers |
|:------------|------------------------------:|
| count       |                         1,005 |
| mean        |                        81,203 |
| std         |                       570,895 |
| min         |                           788 |
| 25%         |                         1,667 |
| 50%         |                         3,969 |
| 75%         |                        15,438 |
| max         |                     9,724,246 |
| total       |                    81,608,842 |
| var_coeff   |                             7 |
| range       |                     9,723,458 |
| IQ_range    |                        13,771 |
| upper_fence |                        36,094 |
| lower_fence |                       -18,990 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/POSmirror/complement/images/sample-heatmap_diff_POSmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.png`

✅ complement frequency table saved as `/share/compling/projects/sanpi/results/freq_out/POSmirror/complement/diff_POSmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

### Adverb stats for complement

|       | non-`POSmirror` ADJ totals |
|:------|---------------------------:|
| count |                   3,895.00 |
| mean  |                  41,904.41 |
| std   |               1,310,397.02 |
| min   |                     567.00 |
| 25%   |                   1,603.50 |
| 50%   |                   3,394.00 |
| 75%   |                  10,434.50 |
| max   |              81,608,842.00 |

### Adverb stats for complement

|       | non-`POSmirror` ADV totals |
|:------|---------------------------:|
| count |                   1,006.00 |
| mean  |                 162,244.22 |
| std   |               2,633,003.96 |
| min   |                     788.00 |
| 25%   |                   1,668.00 |
| 50%   |                   3,971.00 |
| 75%   |                  15,551.25 |
| max   |              81,608,842.00 |

## Frequency Table Corners

### ALL

| `adj_form_lower` | `SUM`    | very    | more    | most    | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:--------|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 83284343 | 9913432 | 9320997 | 7568812 | ... | 872          | 869         | 869          | 868       |
| many             | 2210387  | 21237   | 373     | 140     | ... | 3            | 0           | 0            | 0         |
| important        | 2199447  | 359610  | 306604  | 748533  | ... | 2            | 105         | 9            | 0         |
| good             | 2030480  | 507499  | 18902   | 5207    | ... | 6            | 0           | 7            | 0         |
| ...              | ...      | ...     | ...     | ...     | ... | ...          | ...         | ...          | ...       |
| carnal           | 872      | 34      | 150     | 62      | ... | 0            | 0           | 0            | 0         |
| contiguous       | 871      | 4       | 106     | 8       | ... | 0            | 0           | 0            | 0         |
| panicked         | 871      | 54      | 159     | 31      | ... | 0            | 0           | 0            | 0         |
| oversized        | 870      | 32      | 45      | 16      | ... | 0            | 0           | 0            | 0         |

### `POSmirror`

| `adj_form_lower` | `SUM`   | very   | more   | most  | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:--------|:-------|:-------|:------|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 1675501 | 189186 | 235139 | 19494 | ... | 22           | 6           | 28           | 25        |
| many             | 3778    | 30     | 3      | 0     | ... | 0            | 0           | 0            | 0         |
| important        | 33825   | 6646   | 12725  | 1193  | ... | 0            | 4           | 0            | 0         |
| good             | 29290   | 6473   | 76     | 5     | ... | 0            | 0           | 0            | 0         |
| ...              | ...     | ...    | ...    | ...   | ... | ...          | ...         | ...          | ...       |
| carnal           | 23      | 2      | 9      | 1     | ... | 0            | 0           | 0            | 0         |
| contiguous       | 16      | 0      | 2      | 0     | ... | 0            | 0           | 0            | 0         |
| panicked         | 18      | 3      | 2      | 0     | ... | 0            | 0           | 0            | 0         |
| oversized        | 18      | 0      | 2      | 0     | ... | 0            | 0           | 0            | 0         |

### _Complement_

| `adj_form_lower` | `SUM`    | very    | more    | most    | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:--------|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 81608842 | 9724246 | 9085858 | 7549318 | ... | 850          | 863         | 841          | 843       |
| many             | 2206609  | 21207   | 370     | 140     | ... | 3            | 0           | 0            | 0         |
| important        | 2165622  | 352964  | 293879  | 747340  | ... | 2            | 101         | 9            | 0         |
| good             | 2001190  | 501026  | 18826   | 5202    | ... | 6            | 0           | 7            | 0         |
| ...              | ...      | ...     | ...     | ...     | ... | ...          | ...         | ...          | ...       |
| carnal           | 849      | 32      | 141     | 61      | ... | 0            | 0           | 0            | 0         |
| contiguous       | 855      | 4       | 104     | 8       | ... | 0            | 0           | 0            | 0         |
| panicked         | 853      | 51      | 157     | 31      | ... | 0            | 0           | 0            | 0         |
| oversized        | 852      | 32      | 43      | 16      | ... | 0            | 0           | 0            | 0         |

## Juxtaposed Sample (√ frequencies)

| `adj_form_lower`         | extremely | slightly | fairly | absolutely | particularly | somewhat | fully |  that | utterly | definitely | remotely | necessarily |  ever | exactly |
|:-------------------------|----------:|---------:|-------:|-----------:|-------------:|---------:|------:|------:|--------:|-----------:|---------:|------------:|------:|--------:|
| adult                    |      5.10 |     3.32 |   5.00 |       1.73 |         3.16 |     4.12 | 11.53 |  0.00 |    1.73 |       4.00 |     1.73 |        1.41 |  5.92 |    1.00 |
| adult-`POSmirror`        |      1.00 |     0.00 |   1.73 |       0.00 |         0.00 |     0.00 |  1.41 |  0.00 |    0.00 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| ashamed                  |      7.21 |    14.53 |   1.73 |       8.37 |         5.48 |    13.38 |  2.00 |  2.83 |   10.05 |       1.73 |     3.87 |        2.45 |  3.74 |    2.45 |
| ashamed-`POSmirror`      |      1.00 |     2.65 |   0.00 |       1.00 |         0.00 |     1.73 |  0.00 |  0.00 |    1.00 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| blunt                    |      9.49 |     3.74 |  11.05 |       3.87 |         9.27 |     7.07 |  0.00 |  3.16 |    2.45 |       1.41 |     0.00 |        1.41 |  3.00 |    0.00 |
| blunt-`POSmirror`        |      1.73 |     1.00 |   0.00 |       0.00 |         0.00 |     1.00 |  0.00 |  0.00 |    0.00 |       0.00 |     0.00 |        1.00 |  0.00 |    0.00 |
| concerned                |     65.14 |    24.62 |   7.07 |       9.54 |        86.43 |    30.59 |  4.00 | 31.16 |    3.61 |      15.75 |     9.85 |       12.12 | 16.64 |    4.80 |
| concerned-`POSmirror`    |      9.49 |     3.61 |   1.41 |       1.00 |         7.55 |     8.54 |  1.41 |  3.46 |    0.00 |       1.73 |     0.00 |        1.00 |  1.00 |    0.00 |
| confusing                |     22.96 |    24.54 |   9.33 |       4.69 |        15.00 |    36.55 |  1.00 |  7.14 |   12.69 |       5.00 |     1.73 |        1.73 |  4.90 |    1.73 |
| confusing-`POSmirror`    |      4.24 |     3.61 |   1.73 |       0.00 |         1.41 |     5.20 |  0.00 |  0.00 |    2.45 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| dissimilar               |      4.69 |     3.46 |   3.46 |       2.45 |         2.00 |     4.36 |  0.00 | 17.83 |    6.40 |       1.00 |     0.00 |        2.00 |  0.00 |    0.00 |
| dissimilar-`POSmirror`   |      1.41 |     0.00 |   0.00 |       0.00 |         0.00 |     0.00 |  0.00 |  1.73 |    1.00 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| enticing                 |     11.09 |     1.41 |   3.74 |       3.61 |        15.78 |     4.69 |  0.00 |  4.58 |    3.32 |       3.61 |     1.73 |        1.73 |  3.46 |    4.69 |
| enticing-`POSmirror`     |      1.41 |     0.00 |   1.41 |       0.00 |         1.73 |     0.00 |  0.00 |  0.00 |    0.00 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| forgettable              |      6.48 |     4.36 |  12.45 |       3.61 |         2.65 |    11.36 |  1.73 |  2.00 |   17.44 |       2.83 |     0.00 |        0.00 |  1.00 |    1.00 |
| forgettable-`POSmirror`  |      0.00 |     1.00 |   1.41 |       0.00 |         0.00 |     1.41 |  0.00 |  0.00 |    2.65 |       1.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| inconsistent             |     15.03 |     9.49 |   9.70 |       6.56 |         4.00 |    20.88 |  2.00 |  3.87 |    9.90 |       3.46 |     2.45 |        8.72 |  2.45 |    1.73 |
| inconsistent-`POSmirror` |      2.24 |     1.00 |   2.00 |       1.00 |         0.00 |     1.73 |  0.00 |  0.00 |    0.00 |       0.00 |     0.00 |        1.00 |  0.00 |    0.00 |
| insistent                |      3.74 |     1.73 |   5.39 |       6.40 |         9.95 |     2.00 |  1.41 |  2.24 |    1.73 |       1.00 |     0.00 |        0.00 |  3.61 |    0.00 |
| insistent-`POSmirror`    |      0.00 |     0.00 |   0.00 |       0.00 |         1.41 |     0.00 |  0.00 |  0.00 |    0.00 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| overrated                |      8.19 |     9.17 |   2.00 |       3.32 |         1.41 |    10.54 |  1.00 |  1.00 |    2.00 |       5.57 |     0.00 |        1.41 |  1.00 |    0.00 |
| overrated-`POSmirror`    |      2.45 |     1.00 |   0.00 |       0.00 |         0.00 |     1.00 |  0.00 |  0.00 |    0.00 |       1.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| stuck                    |      2.83 |     4.80 |   2.24 |       6.48 |         5.39 |     9.27 |  1.73 |  1.00 |    4.12 |       2.24 |     0.00 |        2.24 |  3.00 |    1.00 |
| stuck-`POSmirror`        |      0.00 |     1.00 |   0.00 |       0.00 |         0.00 |     1.41 |  0.00 |  0.00 |    0.00 |       0.00 |     0.00 |        0.00 |  0.00 |    0.00 |
| tense                    |     26.08 |     9.06 |   7.42 |       2.24 |        21.02 |    11.31 |  2.45 |  2.65 |    1.00 |       4.69 |     1.41 |        0.00 |  2.65 |    2.00 |
| tense-`POSmirror`        |      2.65 |     0.00 |   1.00 |       0.00 |         1.00 |     1.41 |  0.00 |  0.00 |    0.00 |       0.00 |     0.00 |        0.00 |  1.00 |    0.00 |

## Top Values

### Top (15 x 10) collocations in ALL frequencies (+ `SUM`)

| `adj_form_lower` |      `SUM` |      very |      more |      most |        so |       not |        as |       too |    really |      much |    pretty |
|:-----------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| `SUM`            | 83,284,343 | 9,913,432 | 9,320,997 | 7,568,812 | 5,735,964 | 4,415,785 | 3,709,914 | 3,557,440 | 2,096,057 | 1,986,728 | 1,621,748 |
| many             |  2,210,387 |    21,237 |       373 |       140 | 1,191,864 |    58,442 |   434,631 |   450,194 |       518 |       201 |        54 |
| important        |  2,199,447 |   359,610 |   306,604 |   748,533 |   105,509 |    17,351 |   102,823 |    12,879 |    72,175 |     1,826 |     6,594 |
| good             |  2,030,480 |   507,499 |    18,902 |     5,207 |   153,196 |    96,143 |   235,348 |    59,683 |   260,281 |    14,343 |   243,692 |
| much             |  1,776,924 |    42,365 |       102 |        22 |   614,652 |    66,410 |   355,368 |   583,184 |     3,066 |       284 |    57,884 |
| likely           |  1,048,364 |    35,899 |   498,401 |   192,635 |       847 |    46,858 |    31,820 |     1,196 |       466 |       259 |     1,312 |
| more             |  1,028,133 |        69 |     2,280 |        90 |     2,953 |    17,641 |     2,851 |        52 |     4,561 |   355,655 |        14 |
| different        |    906,600 |   233,008 |    12,237 |     1,364 |    39,346 |     4,024 |     9,296 |     5,198 |     6,545 |    44,251 |     2,140 |
| available        |    862,942 |       403 |     9,739 |     1,384 |       490 |   132,371 |     1,879 |       277 |       552 |       979 |        32 |
| sure             |    844,066 |     4,691 |     2,324 |       315 |    35,676 |   467,213 |     3,900 |     8,714 |    20,125 |       341 |    84,366 |
| difficult        |    832,988 |   188,193 |   220,215 |    76,638 |    26,542 |    19,841 |    16,041 |    27,938 |    18,779 |       638 |     5,649 |
| popular          |    827,608 |    89,434 |    70,577 |   398,955 |    42,950 |     4,558 |    15,226 |     2,153 |     5,022 |     1,305 |     3,214 |
| easy             |    768,452 |   125,544 |     5,567 |     1,215 |    88,639 |    95,490 |    73,233 |    40,465 |    29,583 |       816 |    31,788 |
| better           |    740,721 |        93 |     1,756 |        66 |       872 |    13,540 |     1,990 |        30 |     1,770 |   295,224 |        16 |
| high             |    586,188 |   138,155 |     5,218 |    10,402 |    35,697 |     5,769 |    68,042 |    78,087 |    11,041 |       576 |    13,002 |
| common           |    555,893 |    45,763 |    85,760 |   272,787 |    15,145 |     7,175 |    11,388 |    10,439 |     1,531 |       916 |     7,186 |

### Top (15 x 10) collocations in `POSmirror` frequencies (+ `SUM`)

| `adj_form_lower` |     `SUM` |    more |    very |     too |      so |     as |   even |    not | really |  quite |   just |
|:-----------------|----------:|--------:|--------:|--------:|--------:|-------:|-------:|-------:|-------:|-------:|-------:|
| `SUM`            | 1,675,501 | 235,139 | 189,186 | 140,198 | 118,563 | 94,706 | 72,792 | 70,667 | 52,399 | 36,925 | 30,182 |
| different        |    38,602 |     155 |   6,824 |     135 |   2,049 |    155 |     66 |     39 |    608 |  3,504 |    291 |
| important        |    33,825 |  12,725 |   6,646 |     235 |   1,475 |  3,007 |     57 |    475 |  1,755 |    159 |     21 |
| good             |    29,290 |      76 |   6,473 |   1,451 |   2,482 |  3,302 |    433 |  2,025 |  3,840 |  1,083 |    283 |
| simple           |    24,954 |     430 |   1,917 |     383 |   2,431 | 16,567 |     30 |     51 |    342 |    501 |     40 |
| wrong            |    18,435 |      64 |   3,091 |      10 |     398 |     67 |    135 |    126 |    894 |     89 |    377 |
| easy             |    16,645 |     240 |   1,481 |   7,879 |   1,215 |  1,082 |     44 |  1,198 |    387 |    254 |     49 |
| difficult        |    16,063 |   5,518 |   3,758 |   1,130 |     584 |    358 |    119 |     78 |    381 |    575 |     65 |
| better           |    15,066 |     134 |       0 |       1 |      11 |     17 |  6,959 |    102 |     29 |      3 |    470 |
| special          |    14,888 |   1,746 |   5,141 |      34 |   1,032 |    199 |     22 |     20 |  2,929 |    483 |     30 |
| likely           |    14,632 |   9,179 |     525 |     335 |      11 |    269 |    169 |    362 |      7 |     57 |      6 |
| right            |    14,280 |      48 |      83 |      18 |     112 |      9 |     44 |  4,688 |     27 |     54 |    741 |
| small            |    14,135 |      48 |   1,388 |   6,670 |   1,473 |  2,519 |    103 |     23 |    229 |    363 |     20 |
| familiar         |    14,054 |     639 |     960 |   7,533 |     524 |    118 |     33 |    616 |     42 |    220 |     15 |
| available        |    13,620 |     131 |      16 |      13 |      38 |     19 |    198 |  2,631 |      7 |      4 |     19 |
| close            |    13,344 |      52 |   4,290 |   1,288 |   1,425 |  2,032 |    771 |    136 |    473 |    205 |     29 |

### Top (15 x 10) collocations in DIFF frequencies (+ `SUM`)

| `adj_form_lower` |      `SUM` |      very |      more |      most |        so |       not |        as |       too |    really |      much |    pretty |
|:-----------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| `SUM`            | 81,608,842 | 9,724,246 | 9,085,858 | 7,549,318 | 5,617,401 | 4,345,118 | 3,615,208 | 3,417,242 | 2,043,658 | 1,962,059 | 1,595,511 |
| many             |  2,206,609 |    21,207 |       370 |       140 | 1,191,755 |    58,323 |   432,942 |   449,022 |       517 |       201 |        54 |
| important        |  2,165,622 |   352,964 |   293,879 |   747,340 |   104,034 |    16,876 |    99,816 |    12,644 |    70,420 |     1,815 |     6,444 |
| good             |  2,001,190 |   501,026 |    18,826 |     5,202 |   150,714 |    94,118 |   232,046 |    58,232 |   256,441 |    14,304 |   241,427 |
| much             |  1,770,282 |    42,124 |        97 |        22 |   614,339 |    66,207 |   354,710 |   578,747 |     3,031 |       283 |    57,739 |
| likely           |  1,033,732 |    35,374 |   489,222 |   191,428 |       836 |    46,496 |    31,551 |       861 |       459 |       257 |     1,305 |
| more             |  1,019,589 |        69 |     2,265 |        90 |     2,866 |    17,547 |     2,842 |        52 |     4,518 |   353,819 |        14 |
| different        |    867,998 |   226,184 |    12,082 |     1,362 |    37,297 |     3,985 |     9,141 |     5,063 |     5,937 |    43,597 |     2,047 |
| available        |    849,322 |       387 |     9,608 |     1,375 |       452 |   129,740 |     1,860 |       264 |       545 |       965 |        32 |
| sure             |    838,595 |     4,629 |     2,257 |       314 |    35,380 |   464,291 |     3,870 |     8,690 |    20,106 |       338 |    84,000 |
| popular          |    823,309 |    88,585 |    69,758 |   398,412 |    42,704 |     4,465 |    15,035 |     2,089 |     4,939 |     1,302 |     3,177 |
| difficult        |    816,925 |   184,435 |   214,697 |    76,016 |    25,958 |    19,763 |    15,683 |    26,808 |    18,398 |       631 |     5,547 |
| easy             |    751,807 |   124,063 |     5,327 |     1,211 |    87,424 |    94,292 |    72,151 |    32,586 |    29,196 |       811 |    31,327 |
| better           |    725,655 |        93 |     1,622 |        66 |       861 |    13,438 |     1,973 |        29 |     1,741 |   292,240 |        16 |
| high             |    579,650 |   136,871 |     5,172 |    10,386 |    35,268 |     5,690 |    67,005 |    76,146 |    10,937 |       573 |    12,889 |
| common           |    547,709 |    45,348 |    85,023 |   272,634 |    14,951 |     7,108 |    11,089 |     5,016 |     1,506 |       916 |     7,124 |

## Totals

### Total Tokens per Frequency Group

|             |     totals |
|:------------|-----------:|
| ALL         | 83,284,343 |
| `POSmirror` |  1,675,501 |
| DIFF        | 81,608,842 |

### Marginal Frequencies for ALL Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                21,388 |                82,870 |
| std   |                91,460 |               581,924 |
| min   |                   870 |                   868 |
| 25%   |                 1,637 |                 1,705 |
| 50%   |                 3,466 |                 4,049 |
| 75%   |                10,673 |                15,767 |
| max   |             2,210,387 |             9,913,432 |

### Marginal Frequencies for `POSmirror` Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                   430 |                 1,667 |
| std   |                 1,619 |                12,315 |
| min   |                     0 |                     1 |
| 25%   |                    31 |                    33 |
| 50%   |                    73 |                    81 |
| 75%   |                   230 |                   291 |
| max   |                38,602 |               235,139 |

### Marginal Frequencies for DIFF Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                20,958 |                81,203 |
| std   |                90,196 |               570,895 |
| min   |                   567 |                   788 |
| 25%   |                 1,603 |                 1,667 |
| 50%   |                 3,392 |                 3,969 |
| 75%   |                10,429 |                15,438 |
| max   |             2,206,609 |             9,724,246 |

#### Top 30 ADV totals comparison

| `adv_form_lower` | POSmirror/ALL | DIFF/ALL | POSmirror_RAW |     DIFF_RAW |
|:-----------------|--------------:|---------:|--------------:|-------------:|
| else             |          0.27 |     0.73 |        934.00 |     2,498.00 |
| plain            |          0.17 |     0.83 |      5,880.00 |    28,646.00 |
| outright         |          0.15 |     0.85 |      1,137.00 |     6,436.00 |
| together         |          0.14 |     0.86 |        303.00 |     1,885.00 |
| maybe            |          0.13 |     0.87 |      2,777.00 |    18,114.00 |
| around           |          0.12 |     0.88 |      1,065.00 |     8,081.00 |
| downright        |          0.11 |     0.89 |      5,240.00 |    43,892.00 |
| on               |          0.10 |     0.90 |         84.00 |       788.00 |
| otherwise        |          0.09 |     0.91 |      8,575.00 |    89,673.00 |
| confusingly      |          0.08 |     0.92 |         90.00 |       971.00 |
| altogether       |          0.08 |     0.92 |      1,660.00 |    17,983.00 |
| willfully        |          0.08 |     0.92 |        301.00 |     3,270.00 |
| innately         |          0.08 |     0.92 |        280.00 |     3,310.00 |
| tangentially     |          0.08 |     0.92 |        102.00 |     1,244.00 |
| simply           |          0.07 |     0.93 |      8,408.00 |   110,322.00 |
| early            |          0.07 |     0.93 |        218.00 |     2,947.00 |
| indirectly       |          0.07 |     0.93 |        124.00 |     1,694.00 |
| unpleasantly     |          0.07 |     0.93 |         91.00 |     1,254.00 |
| unintentionally  |          0.07 |     0.93 |        233.00 |     3,228.00 |
| indescribably    |          0.07 |     0.93 |        123.00 |     1,761.00 |
| even             |          0.06 |     0.94 |     72,792.00 | 1,047,413.00 |
| perversely       |          0.06 |     0.94 |         90.00 |     1,308.00 |
| perhaps          |          0.06 |     0.94 |      3,649.00 |    53,618.00 |
| dreadfully       |          0.06 |     0.94 |        204.00 |     3,097.00 |
| someplace        |          0.06 |     0.94 |         85.00 |     1,320.00 |
| vaguely          |          0.06 |     0.94 |      1,112.00 |    17,393.00 |
| at               |          0.06 |     0.94 |        182.00 |     2,877.00 |
| there            |          0.06 |     0.94 |        257.00 |     4,099.00 |
| seriously        |          0.06 |     0.94 |      3,922.00 |    63,590.00 |
| hyper            |          0.06 |     0.94 |         71.00 |     1,178.00 |

#### Top 30 ADJ totals comparison

| `adj_form_lower` | POSmirror/ALL | DIFF/ALL | POSmirror_RAW |   DIFF_RAW |
|:-----------------|--------------:|---------:|--------------:|-----------:|
| amiss            |          0.53 |     0.47 |        628.00 |     567.00 |
| sinister         |          0.18 |     0.82 |      3,087.00 |  14,429.00 |
| unenforceable    |          0.14 |     0.86 |        155.00 |     921.00 |
| triple           |          0.14 |     0.86 |        139.00 |     874.00 |
| fishy            |          0.13 |     0.87 |        211.00 |   1,403.00 |
| peachy           |          0.12 |     0.88 |        127.00 |     906.00 |
| objectionable    |          0.12 |     0.88 |        656.00 |   4,711.00 |
| medium           |          0.12 |     0.88 |        180.00 |   1,328.00 |
| third            |          0.12 |     0.88 |        580.00 |   4,387.00 |
| nefarious        |          0.10 |     0.90 |        298.00 |   2,616.00 |
| intangible       |          0.10 |     0.90 |        181.00 |   1,598.00 |
| fourth           |          0.10 |     0.90 |        256.00 |   2,272.00 |
| missing          |          0.10 |     0.90 |        289.00 |   2,607.00 |
| wrong            |          0.10 |     0.90 |     18,435.00 | 167,260.00 |
| trivial          |          0.10 |     0.90 |      1,368.00 |  12,436.00 |
| primal           |          0.09 |     0.91 |        308.00 |   3,132.00 |
| akin             |          0.09 |     0.91 |      1,268.00 |  13,603.00 |
| wishful          |          0.08 |     0.92 |        198.00 |   2,224.00 |
| foolhardy        |          0.08 |     0.92 |         88.00 |     990.00 |
| misinformed      |          0.08 |     0.92 |        109.00 |   1,247.00 |
| special          |          0.08 |     0.92 |     14,888.00 | 181,391.00 |
| petty            |          0.08 |     0.92 |        262.00 |   3,206.00 |
| mundane          |          0.07 |     0.93 |      1,425.00 |  17,646.00 |
| askew            |          0.07 |     0.93 |         84.00 |   1,065.00 |
| tangible         |          0.07 |     0.93 |        976.00 |  12,623.00 |
| rotten           |          0.07 |     0.93 |        234.00 |   3,037.00 |
| elemental        |          0.07 |     0.93 |        138.00 |   1,797.00 |
| fifth            |          0.07 |     0.93 |         95.00 |   1,242.00 |
| galling          |          0.07 |     0.93 |        165.00 |   2,160.00 |
| grander          |          0.07 |     0.93 |        203.00 |   2,665.00 |
