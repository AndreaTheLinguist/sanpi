# Comparing Bigram Frequencies by Polarity

- for `35` corpus input `.conll` directories containing source `.conllu` files
- with word types limited to only those that account for at least $0.001\%$ of the cleaned dataset (as sourced from 35 corpus file inputs)
- file identifier = `thr0-001p.35f`
- pattern matches restricted to only token word types with at least `868` total tokens across all combinations

- Selected Paths
  - `/share/compling/projects/sanpi/results/freq_out/RBdirect/all-frq_adj-x-adv_thr0-001p.35f.pkl.gz`
  - `/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## _`RBdirect`_ Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for`stats_all-frq_adj-x-adv_thr0-001p.35f` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBdirect/descriptive_stats/ADV-stats_all-frq_adj-x-adv_thr0-001p.35f.csv`
  - time elapsed: 00:00:00.14
  
Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| specifically     | 3,886 |    0 |   3 |   0 |   0 |   0 |   0 | 192 |   898 |        14 |   192 |        0 |           0 |           0 |              1 |              1 |
| seemingly        | 3,886 |    0 |   0 |   0 |   0 |   0 |   0 |  17 |   163 |         9 |    17 |        0 |           0 |           0 |              1 |              1 |
| blandly          | 3,886 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |    11 |        19 |     1 |        0 |           0 |           0 |              1 |              1 |
| wondrously       | 3,886 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     1 |        62 |     1 |        0 |           0 |           0 |              1 |              1 |
| blissfully       | 3,886 |    0 |   0 |   0 |   0 |   0 |   0 |  14 |    42 |        28 |    14 |        0 |           0 |           0 |              1 |              1 |
| blazingly        | 3,886 |    0 |   0 |   0 |   0 |   0 |   0 |  18 |    31 |        38 |    18 |        0 |           0 |           0 |              1 |              1 |
  
|             | `RBdirect`: `adv_form_lower` totals |
|:------------|------------------------------------:|
| count       |                               3,886 |
| mean        |                                 810 |
| std         |                               4,753 |
| min         |                                   1 |
| 25%         |                                  35 |
| 50%         |                                  88 |
| 75%         |                                 298 |
| max         |                             132,226 |
| total       |                           3,148,010 |
| var_coeff   |                                   6 |
| range       |                             132,225 |
| IQ_range    |                                 263 |
| upper_fence |                                 692 |
| lower_fence |                                -359 |

### Descriptive Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for`stats_all-frq_adj-x-adv_thr0-001p.35f` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBdirect/descriptive_stats/ADJ-stats_all-frq_adj-x-adv_thr0-001p.35f.csv`
  - time elapsed: 00:00:00.99

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| underwater       | 1,001 |    0 |   0 |   0 |   0 |   0 |   0 |   5 |    45 |         7 |     5 |        0 |           0 |           0 |              1 |              1 |
| overdue          | 1,001 |    0 |   2 |   0 |   0 |   0 |   0 |  60 |   115 |        17 |    60 |        0 |           0 |           0 |              1 |              1 |
| universal        | 1,001 |    0 |   5 |   0 |   0 |   0 |   0 | 122 |   489 |        10 |   122 |        0 |           0 |           0 |              1 |              1 |
| kinky            | 1,001 |    0 |   1 |   0 |   0 |   0 |   0 |  26 |   102 |        12 |    26 |        0 |           0 |           0 |              1 |              1 |
| free             | 1,001 |    6 |  44 |   0 |   0 |   0 |   0 | 617 | 5,837 |         7 |   617 |        0 |           0 |           0 |              1 |              1 |
| stingy           | 1,001 |    0 |   2 |   0 |   0 |   0 |   0 |  42 |   144 |        14 |    42 |        0 |           0 |           0 |              1 |              1 |

|             | `RBdirect`: `adj_form_lower` totals |
|:------------|------------------------------------:|
| count       |                               1,001 |
| mean        |                               3,145 |
| std         |                              25,328 |
| min         |                                   1 |
| 25%         |                                  16 |
| 50%         |                                  49 |
| 75%         |                                 205 |
| max         |                             526,827 |
| total       |                           3,148,010 |
| var_coeff   |                                   8 |
| range       |                             526,826 |
| IQ_range    |                                 189 |
| upper_fence |                                 488 |
| lower_fence |                                -268 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/RBdirect/images/sample-heatmap_all-frq_adj-x-adv_thr0-001p.35f.pkl.png`

### Full Table Preview of _`RBdirect`_ Frequencies

| `adj_form_lower` | `SUM`   | as     | so     | too    | very   | more   | ... | unseasonably | doubtless | wondrously | preferably | seductively | fewer |
|:-----------------|:--------|:-------|:-------|:-------|:-------|:-------|:----|:-------------|:----------|:-----------|:-----------|:------------|:------|
| `SUM`            | 3148010 | 526827 | 341050 | 307870 | 191043 | 166176 | ... | 1            | 1         | 1          | 1          | 1           | 1     |
| good             | 132226  | 44885  | 18002  | 3623   | 30349  | 32     | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| sure             | 128741  | 714    | 26584  | 8093   | 675    | 141    | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| bad              | 105134  | 27740  | 21352  | 19520  | 316    | 8      | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| easy             | 87499   | 23376  | 17596  | 1207   | 2736   | 147    | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| clear            | 72836   | 3456   | 3255   | 473    | 2641   | 1369   | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| ...              | ...     | ...    | ...    | ...    | ...    | ...    | ... | ...          | ...       | ...        | ...        | ...         | ...   |
| trusted          | 1       | 0      | 0      | 0      | 1      | 0      | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| personalised     | 1       | 0      | 0      | 0      | 0      | 0      | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| immigrant        | 1       | 0      | 0      | 0      | 0      | 0      | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| undetected       | 1       | 0      | 0      | 0      | 0      | 0      | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| menial           | 1       | 0      | 0      | 0      | 0      | 0      | ... | 0            | 0         | 0          | 0          | 0           | 0     |
| undisturbed      | 1       | 0      | 0      | 0      | 0      | 0      | ... | 0            | 0         | 0          | 0          | 0           | 0     |

### (Semi-)Random Sample of _`RBdirect`_ Frequencies

| `adj_form_lower` |     `SUM` |    any | nearly |   not | wildly | humanly | noticeably | academically |
|:-----------------|----------:|-------:|-------:|------:|-------:|--------:|-----------:|-------------:|
| `SUM`            | 3,148,010 | 15,342 |  8,707 | 7,740 |    995 |     384 |        371 |          362 |
| right            |    15,727 |      0 |     13 |    61 |      1 |       1 |          0 |            0 |
| scary            |     5,090 |      0 |      6 |    12 |      0 |       0 |          0 |            0 |
| dissimilar       |     2,524 |      0 |      0 |     1 |     16 |       0 |          0 |            0 |
| wonderful        |     2,003 |      0 |      0 |     2 |      0 |       0 |          0 |            0 |
| grateful         |     1,888 |      0 |      0 |    27 |      0 |       0 |          0 |            0 |
| precise          |     1,835 |      0 |      4 |     0 |      0 |       0 |          0 |            0 |
| weird            |     1,716 |      0 |      2 |     6 |      0 |       0 |          1 |            0 |

## _ALL_ (`RBdirect` and non-`RBdirect`) Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for`stats_all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADV-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.530

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% |   max |  total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|------:|-------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| therefore        | 3,894 |   13 |  88 |   0 |   0 |   1 |   5 | 3,676 | 51,275 |         7 | 3,676 |        5 |          12 |          -8 |              3 |              2 |
| ordinarily       | 3,894 |    1 |   3 |   0 |   0 |   0 |   0 |   154 |  2,015 |         6 |   154 |        0 |           0 |           0 |              1 |              1 |
| enough           | 3,894 |    5 |  33 |   0 |   0 |   0 |   2 | 1,508 | 20,156 |         6 | 1,508 |        2 |           5 |          -3 |              2 |              2 |
| musically        | 3,894 |    2 |  14 |   0 |   0 |   0 |   0 |   630 |  6,111 |         9 |   630 |        0 |           0 |           0 |              1 |              1 |
| eminently        | 3,894 |    3 |  27 |   0 |   0 |   0 |   0 |   909 | 11,180 |         9 |   909 |        0 |           0 |           0 |              1 |              1 |
| outright         | 3,894 |    2 |  12 |   0 |   0 |   0 |   1 |   322 |  7,573 |         6 |   322 |        1 |           2 |          -2 |              1 |              1 |

|             | ALL: `adv_form_lower` totals |
|:------------|-----------------------------:|
| count       |                        3,894 |
| mean        |                       21,388 |
| std         |                       91,460 |
| min         |                          870 |
| 25%         |                        1,637 |
| 50%         |                        3,466 |
| 75%         |                       10,673 |
| max         |                    2,210,387 |
| total       |                   83,284,343 |
| var_coeff   |                            4 |
| range       |                    2,209,517 |
| IQ_range    |                        9,036 |
| upper_fence |                       24,227 |
| lower_fence |                      -11,917 |

### Descriptive Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for`stats_all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADJ-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.959

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean | std | min | 25% | 50% | 75% |   max |  total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|------:|-------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| bustling         | 1,005 |    1 |  13 |   0 |   0 |   0 |   0 |   271 |  1,273 |        10 |   271 |        0 |           0 |           0 |              1 |              1 |
| shit             | 1,005 |    1 |   7 |   0 |   0 |   0 |   0 |   121 |    891 |         8 |   121 |        0 |           0 |           0 |              1 |              1 |
| frightening      | 1,005 |   26 | 230 |   0 |   0 |   0 |   2 | 4,724 | 26,624 |         9 | 4,724 |        2 |           5 |          -3 |              2 |              1 |
| desolate         | 1,005 |    3 |  22 |   0 |   0 |   0 |   0 |   487 |  2,940 |         8 |   487 |        0 |           0 |           0 |              1 |              1 |
| pro              | 1,005 |    1 |  12 |   0 |   0 |   0 |   0 |   259 |  1,299 |         9 |   259 |        0 |           0 |           0 |              1 |              1 |
| predominant      | 1,005 |    2 |  24 |   0 |   0 |   0 |   0 |   612 |  1,913 |        13 |   612 |        0 |           0 |           0 |              1 |              1 |

|             | ALL: `adj_form_lower` totals |
|:------------|-----------------------------:|
| count       |                        1,005 |
| mean        |                       82,870 |
| std         |                      581,924 |
| min         |                          868 |
| 25%         |                        1,705 |
| 50%         |                        4,049 |
| 75%         |                       15,767 |
| max         |                    9,913,432 |
| total       |                   83,284,343 |
| var_coeff   |                            7 |
| range       |                    9,912,564 |
| IQ_range    |                       14,062 |
| upper_fence |                       36,860 |
| lower_fence |                      -19,388 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/RBXadj/images/sample-heatmap_all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.png`

### Full Table Preview of _All_ Frequencies

| `adv_form_lower` |    `SUM` |    very |    more | ... | second-most | cosmetically | pointedly |
|:-----------------|---------:|--------:|--------:|:---:|------------:|-------------:|----------:|
| `SUM`            | 83284343 | 9913432 | 9320997 | ... |         869 |          869 |       868 |
| many             |  2210387 |   21237 |     373 | ... |           0 |            0 |         0 |
| important        |  2199447 |  359610 |  306604 | ... |         105 |            9 |         0 |
| good             |  2030480 |  507499 |   18902 | ... |           0 |            7 |         0 |
| much             |  1776924 |   42365 |     102 | ... |           0 |            0 |         1 |
| likely           |  1048364 |   35899 |  498401 | ... |          12 |            0 |         0 |
| ...              |      ... |     ... |     ... | ... |         ... |          ... |       ... |
| intermittent     |      872 |      84 |     171 | ... |           0 |            0 |         0 |
| untrained        |      872 |       9 |      10 | ... |           0 |            0 |         0 |
| carnal           |      872 |      34 |     150 | ... |           0 |            0 |         0 |
| contiguous       |      871 |       4 |     106 | ... |           0 |            0 |         0 |
| panicked         |      871 |      54 |     159 | ... |           0 |            0 |         0 |
| oversized        |      870 |      32 |      45 | ... |           0 |            0 |         0 |

[13 rows x 13 columns]

### (Semi-)Random Sample of _ALL_ Frequencies

| `adj_form_lower` |      `SUM` | enough | roughly | freely | shockingly | overtly | understandably |
|:-----------------|-----------:|-------:|--------:|-------:|-----------:|--------:|---------------:|
| `SUM`            | 83,284,343 | 20,156 |  18,829 | 17,275 |     14,999 |  13,876 |         12,719 |
| willing          |    141,652 |     33 |       0 |     30 |          4 |       0 |              7 |
| bigger           |    130,089 |     13 |       3 |      0 |          2 |       0 |              3 |
| lucky            |     96,258 |      6 |       0 |      0 |          3 |       0 |              0 |
| convenient       |     94,621 |      9 |       1 |      0 |          2 |       0 |              1 |
| tired            |     81,827 |      6 |       0 |      0 |          0 |       0 |             75 |
| quick            |     78,299 |      9 |       0 |      0 |         46 |       0 |             10 |

👀 sanity dimension checks

|       dataframe | # rows | # columns |
|----------------:|-------:|----------:|
| only `RBdirect` |   3887 |      1002 |
|             ALL |   3895 |      1006 |
|    adjusted NEG |   3895 |      1006 |

## Words with 0 tokens in the `RBdirect` results

### Adjectives

| `adj_form_lower` | SUM_RBdirect | `SUM` |
|:-----------------|-------------:|------:|
| evolving         |            0 | 3,141 |
| earliest         |            0 | 2,199 |
| northerly        |            0 | 1,890 |
| southerly        |            0 | 1,426 |
| chopped          |            0 | 1,293 |
| away             |            0 | 1,291 |
| marrow           |            0 | 1,168 |
| null             |            0 | 1,063 |
| worldwide        |            0 |   963 |

### Adverbs

| `adv_form_lower` | SUM_RBdirect | `SUM` |
|:-----------------|-------------:|------:|
| yearly           |            0 | 2,218 |
| sparsely         |            0 | 1,281 |
| legendarily      |            0 |   981 |
| second-most      |            0 |   869 |

## The Difference

| `adj_form_lower` | `SUM`    | very    | more    | ... | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:----|:------------|:-------------|:----------|
| `SUM`            | 80136333 | 9722389 | 9154821 | ... | 869         | 815          | 853       |
| many             | 2196242  | 19312   | 371     | ... | 0           | 0            | 0         |
| important        | 2149576  | 357754  | 291396  | ... | 105         | 9            | 0         |
| ...              | ...      | ...     | ...     | ... | ...         | ...          | ...       |
| contiguous       | 814      | 3       | 106     | ... | 0           | 0            | 0         |
| panicked         | 832      | 53      | 153     | ... | 0           | 0            | 0         |
| oversized        | 854      | 32      | 45      | ... | 0           | 0            | 0         |

### Descriptive _Complement_ Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for`stats_diff_RBdirect-all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBdirect/complement/descriptive_stats/ADV-stats_diff_RBdirect-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.234

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% |    max |  total | var_coeff |  range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|-------:|-------:|----------:|-------:|---------:|------------:|------------:|---------------:|---------------:|
| environmentally  | 3,894 |   21 | 688 |   0 |   0 |   0 |   0 | 41,258 | 81,914 |        33 | 41,258 |        0 |           0 |           0 |              1 |              1 |
| ethically        | 3,894 |    2 |  17 |   0 |   0 |   0 |   0 |    712 |  6,569 |        10 |    712 |        0 |           0 |           0 |              1 |              1 |
| terrifically     | 3,894 |    1 |   4 |   0 |   0 |   0 |   0 |    130 |  2,863 |         5 |    130 |        0 |           0 |           0 |              1 |              1 |
| tremendously     | 3,894 |    6 |  49 |   0 |   0 |   0 |   2 |  1,640 | 25,202 |         8 |  1,640 |        2 |           5 |          -3 |              2 |              1 |
| momentarily      | 3,894 |    1 |   3 |   0 |   0 |   0 |   0 |    128 |  2,058 |         6 |    128 |        0 |           0 |           0 |              1 |              1 |
| therefore        | 3,894 |   13 |  87 |   0 |   0 |   1 |   5 |  3,674 | 50,873 |         7 |  3,674 |        5 |          12 |          -8 |              3 |              2 |

|             | _not `RBdirect`_: `adv_form_lower` totals |
|:------------|------------------------------------------:|
| count       |                                     3,894 |
| mean        |                                    20,579 |
| std         |                                    88,045 |
| min         |                                       801 |
| 25%         |                                     1,600 |
| 50%         |                                     3,368 |
| 75%         |                                    10,266 |
| max         |                                 2,196,242 |
| total       |                                80,136,344 |
| var_coeff   |                                         4 |
| range       |                                 2,195,441 |
| IQ_range    |                                     8,666 |
| upper_fence |                                    23,264 |
| lower_fence |                                   -11,400 |

### Descriptive _Complement_ Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for`stats_diff_RBdirect-all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBdirect/complement/descriptive_stats/ADJ-stats_diff_RBdirect-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.535

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean | std | min | 25% | 50% | 75% |   max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|------:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| melancholy       | 1,005 |    3 |  23 |   0 |   0 |   0 |   1 |   558 | 3,139 |         7 |   558 |        1 |           2 |          -2 |              2 |              1 |
| prime            | 1,005 |    2 |  14 |   0 |   0 |   0 |   0 |   324 | 1,685 |         8 |   324 |        0 |           0 |           0 |              1 |              1 |
| maternal         | 1,005 |    1 |   7 |   0 |   0 |   0 |   0 |   155 |   891 |         8 |   155 |        0 |           0 |           0 |              1 |              1 |
| expert           | 1,005 |    4 |  30 |   0 |   0 |   0 |   0 |   602 | 3,598 |         8 |   602 |        0 |           0 |           0 |              1 |              1 |
| inconvenient     | 1,005 |    9 |  65 |   0 |   0 |   0 |   1 | 1,310 | 8,651 |         8 | 1,310 |        1 |           2 |          -2 |              2 |              1 |
| rosy             | 1,005 |    5 |  36 |   0 |   0 |   0 |   0 |   688 | 4,590 |         8 |   688 |        0 |           0 |           0 |              1 |              1 |

|             | _not `RBdirect`_: `adj_form_lower` totals |
|:------------|------------------------------------------:|
| count       |                                     1,005 |
| mean        |                                    79,738 |
| std         |                                   566,480 |
| min         |                                       757 |
| 25%         |                                     1,661 |
| 50%         |                                     3,969 |
| 75%         |                                    15,230 |
| max         |                                 9,722,389 |
| total       |                                80,136,333 |
| var_coeff   |                                         7 |
| range       |                                 9,721,632 |
| IQ_range    |                                    13,569 |
| upper_fence |                                    35,584 |
| lower_fence |                                   -18,692 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/RBdirect/complement/images/sample-heatmap_diff_RBdirect-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.png`

✅ complement frequency table saved as `/share/compling/projects/sanpi/results/freq_out/RBdirect/complement/diff_RBdirect-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

### Adverb stats for complement

|       | non-`RBdirect` ADJ totals |
|:------|--------------------------:|
| count |                  3,895.00 |
| mean  |                 41,148.31 |
| std   |              1,286,716.97 |
| min   |                    801.00 |
| 25%   |                  1,600.00 |
| 50%   |                  3,369.00 |
| 75%   |                 10,268.50 |
| max   |             80,136,333.00 |

### Adverb stats for complement

|       | non-`RBdirect` ADV totals |
|:------|--------------------------:|
| count |                  1,006.00 |
| mean  |                159,316.77 |
| std   |              2,586,776.64 |
| min   |                    757.00 |
| 25%   |                  1,666.75 |
| 50%   |                  3,969.00 |
| 75%   |                 15,486.50 |
| max   |             80,136,333.00 |

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

### `RBdirect`

| `adj_form_lower` | `SUM`   | very   | more   | most  | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:--------|:-------|:-------|:------|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 3148010 | 191043 | 166176 | 19665 | ... | 10           | 0           | 54           | 15        |
| many             | 14145   | 1925   | 2      | 0     | ... | 0            | 0           | 0            | 0         |
| important        | 49871   | 1856   | 15208  | 963   | ... | 0            | 0           | 0            | 0         |
| good             | 132226  | 30349  | 32     | 5     | ... | 0            | 0           | 1            | 0         |
| ...              | ...     | ...    | ...    | ...   | ... | ...          | ...         | ...          | ...       |
| carnal           | 15      | 0      | 0      | 1     | ... | 0            | 0           | 0            | 0         |
| contiguous       | 57      | 1      | 0      | 0     | ... | 0            | 0           | 0            | 0         |
| panicked         | 39      | 1      | 6      | 0     | ... | 0            | 0           | 0            | 0         |
| oversized        | 16      | 0      | 0      | 0     | ... | 0            | 0           | 0            | 0         |

### _Complement_

| `adj_form_lower` | `SUM`    | very    | more    | most    | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:--------|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 80136333 | 9722389 | 9154821 | 7549147 | ... | 862          | 869         | 815          | 853       |
| many             | 2196242  | 19312   | 371     | 140     | ... | 3            | 0           | 0            | 0         |
| important        | 2149576  | 357754  | 291396  | 747570  | ... | 2            | 105         | 9            | 0         |
| good             | 1898254  | 477150  | 18870   | 5202    | ... | 6            | 0           | 6            | 0         |
| ...              | ...      | ...     | ...     | ...     | ... | ...          | ...         | ...          | ...       |
| carnal           | 857      | 34      | 150     | 61      | ... | 0            | 0           | 0            | 0         |
| contiguous       | 814      | 3       | 106     | 8       | ... | 0            | 0           | 0            | 0         |
| panicked         | 832      | 53      | 153     | 31      | ... | 0            | 0           | 0            | 0         |
| oversized        | 854      | 32      | 45      | 16      | ... | 0            | 0           | 0            | 0         |

| `adj_form_lower`     |  that | particularly | exactly | necessarily | fully |  ever | absolutely | remotely | extremely | slightly | utterly | somewhat | fairly | definitely |
|:---------------------|------:|-------------:|--------:|------------:|------:|------:|-----------:|---------:|----------:|---------:|--------:|---------:|-------:|-----------:|
| ancient              |  1.00 |         6.08 |    1.41 |        1.41 |  1.00 |  8.49 |       5.20 |     1.41 |     13.42 |     1.73 |    1.73 |     5.20 |   6.48 |       2.24 |
| ancient-`NEG`        |  1.73 |         3.00 |    4.12 |        1.00 |  0.00 |  0.00 |       0.00 |     0.00 |      0.00 |     0.00 |    0.00 |     0.00 |   0.00 |       0.00 |
| bullish              |  2.24 |        12.33 |    0.00 |        2.00 |  3.00 |  1.41 |       2.65 |     0.00 |     19.65 |    10.63 |    1.00 |     6.78 |  10.49 |       4.36 |
| bullish-`NEG`        |  4.80 |         5.10 |    4.36 |        3.16 |  0.00 |  0.00 |       0.00 |     0.00 |      2.00 |     0.00 |    0.00 |     0.00 |   1.00 |       0.00 |
| challenging          |  2.45 |        64.10 |    1.73 |        2.65 |  2.00 | 10.95 |       6.00 |     4.80 |     69.34 |    13.34 |    2.83 |    26.81 |  19.82 |      17.78 |
| challenging-`NEG`    |  9.85 |        14.28 |    4.12 |        3.61 |  0.00 |  2.45 |       0.00 |     3.74 |      4.36 |     1.00 |    0.00 |     1.41 |   0.00 |       0.00 |
| deep                 |  9.85 |        25.96 |    2.45 |        2.83 |  2.83 |  5.00 |       2.65 |     1.41 |     32.16 |     4.80 |    1.73 |     9.49 |  31.08 |       4.36 |
| deep-`NEG`           | 14.87 |        15.52 |    6.71 |        5.57 |  0.00 |  0.00 |       0.00 |     1.41 |      3.87 |     0.00 |    0.00 |     0.00 |   1.00 |       0.00 |
| enough               |  4.58 |         2.83 |   15.52 |        5.83 |  6.08 | 15.23 |       8.25 |     6.48 |      2.65 |     2.45 |    1.00 |     2.00 |   5.48 |      19.36 |
| enough-`NEG`         |  6.32 |         0.00 |    6.48 |       16.73 |  3.00 | 13.15 |       0.00 |     6.86 |      0.00 |     0.00 |    0.00 |     0.00 |   0.00 |       1.41 |
| explicit             |  2.24 |         7.35 |    0.00 |        2.83 |  6.86 |  2.24 |       6.24 |     1.00 |     11.79 |     2.83 |    2.24 |     4.69 |  13.93 |       1.41 |
| explicit-`NEG`       |  1.73 |         4.36 |    2.00 |        3.87 |  2.45 |  1.41 |       0.00 |     0.00 |      2.24 |     0.00 |    0.00 |     0.00 |   0.00 |       0.00 |
| faint                |  1.41 |         2.00 |    0.00 |        0.00 |  0.00 |  2.65 |       1.00 |     0.00 |     14.53 |     4.80 |    0.00 |     5.29 |   5.92 |       1.00 |
| faint-`NEG`          |  0.00 |         0.00 |    1.00 |        0.00 |  0.00 |  0.00 |       0.00 |     0.00 |      0.00 |     0.00 |    0.00 |     0.00 |   0.00 |       1.00 |
| instructive          |  1.00 |        16.19 |    0.00 |        0.00 |  1.41 |  0.00 |       1.41 |     0.00 |      7.07 |     1.41 |    0.00 |     4.69 |   3.16 |       2.00 |
| instructive-`NEG`    |  1.00 |         3.32 |    0.00 |        1.00 |  0.00 |  1.00 |       0.00 |     0.00 |      0.00 |     0.00 |    0.00 |     0.00 |   0.00 |       0.00 |
| persuasive           |  2.24 |        11.96 |    0.00 |        1.41 |  4.12 |  1.41 |       1.73 |     3.46 |     12.69 |     1.41 |    7.14 |     4.47 |   8.89 |       2.83 |
| persuasive-`NEG`     |  3.46 |         5.74 |    1.00 |        2.24 |  3.46 |  1.00 |       1.00 |     1.41 |      0.00 |     1.00 |    1.00 |     0.00 |   0.00 |       0.00 |
| phenomenal           |  2.65 |         3.61 |    1.00 |        0.00 |  0.00 |  2.00 |      36.10 |     0.00 |      2.45 |     1.00 |    5.48 |     2.45 |   2.65 |       2.45 |
| phenomenal-`NEG`     |  2.65 |         0.00 |    2.00 |        1.00 |  0.00 |  0.00 |       2.24 |     0.00 |      1.00 |     0.00 |    0.00 |     0.00 |   0.00 |       0.00 |
| rational             |  1.73 |         4.58 |    1.41 |        3.61 | 14.83 |  3.74 |       5.57 |     5.48 |      8.37 |     2.65 |    5.74 |     6.63 |   9.06 |       1.41 |
| rational-`NEG`       |  4.12 |         5.92 |    4.36 |        6.24 |  6.40 |  1.41 |       0.00 |     2.65 |      1.00 |     0.00 |    0.00 |     0.00 |   0.00 |       0.00 |
| representative       |  1.00 |         8.06 |    3.16 |        5.29 | 18.57 |  3.32 |       3.32 |     3.00 |      4.00 |     1.73 |    2.83 |     7.68 |  19.39 |       3.87 |
| representative-`NEG` |  0.00 |         5.74 |    7.42 |       22.27 | 12.00 |  1.00 |       1.41 |     4.12 |      0.00 |     0.00 |    0.00 |     0.00 |   1.73 |       0.00 |
| secular              |  0.00 |         1.73 |    0.00 |        2.00 |  7.35 |  0.00 |       3.61 |     1.00 |      5.39 |     0.00 |    4.47 |     5.10 |   7.00 |       2.00 |
| secular-`NEG`        |  0.00 |         1.00 |    1.41 |        3.00 |  1.41 |  0.00 |       0.00 |     1.00 |      0.00 |     0.00 |    0.00 |     0.00 |   0.00 |       0.00 |

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

### Top (15 x 10) collocations in `RBdirect` frequencies (+ `SUM`)

| `adj_form_lower` |     `SUM` |      as |      so |     too |    very |    more |    that |    only |  always | really |  quite |
|:-----------------|----------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|-------:|-------:|
| `SUM`            | 3,148,010 | 526,827 | 341,050 | 307,870 | 191,043 | 166,176 | 165,061 | 109,955 | 103,441 | 95,459 | 77,813 |
| good             |   132,226 |  44,885 |  18,002 |   3,623 |  30,349 |      32 |  10,655 |   3,332 |   1,709 |  2,521 |  1,332 |
| sure             |   128,741 |     714 |  26,584 |   8,093 |     675 |     141 |     300 |      24 |   1,168 | 17,898 | 26,156 |
| bad              |   105,134 |  27,740 |  21,352 |  19,520 |     316 |       8 |  16,535 |     678 |     916 |    718 |    101 |
| easy             |    87,499 |  23,376 |  17,596 |   1,207 |   2,736 |     147 |  10,158 |   1,349 |  24,574 |    543 |    189 |
| clear            |    72,836 |   3,456 |   3,255 |     473 |   2,641 |   1,369 |     516 |     111 |   4,012 |  1,497 |  2,307 |
| available        |    55,828 |     320 |      62 |      34 |      27 |      92 |      11 |     569 |   2,359 |    252 |     52 |
| important        |    49,871 |  12,280 |   3,408 |     683 |   1,856 |  15,208 |   5,532 |   2,764 |     136 |  1,309 |     37 |
| much             |    48,629 |   5,898 |  21,925 |  12,638 |   1,175 |       1 |   4,743 |      38 |      12 |  1,243 |      3 |
| different        |    45,646 |     616 |   5,785 |   2,363 |   3,241 |   6,797 |   6,574 |     299 |      14 |    366 |     68 |
| great            |    33,022 |   5,728 |   9,594 |   1,294 |     396 |       5 |  11,075 |   1,075 |     613 |    389 |     81 |
| big              |    30,852 |  10,764 |   2,113 |   6,441 |   2,462 |       3 |   6,269 |     168 |      57 |    579 |    349 |
| hard             |    30,836 |   1,217 |   4,597 |  10,108 |   1,682 |       9 |   9,966 |     314 |      58 |    548 |     41 |
| simple           |    30,616 |  14,753 |   6,613 |     236 |     264 |     456 |   6,163 |     263 |     629 |    107 |     77 |
| difficult        |    29,884 |   4,635 |   2,608 |   7,446 |   2,439 |   1,699 |   5,577 |     534 |      41 |    304 |     38 |
| close            |    29,405 |   2,854 |   1,537 |   1,833 |   1,025 |      14 |     582 |     101 |      56 |    552 |    130 |

### Top (15 x 10) collocations in DIFF frequencies (+ `SUM`)

| `adj_form_lower` |      `SUM` |      very |      more |      most |        so |       not |       too |        as |    really |      much |    pretty |
|:-----------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| `SUM`            | 80,136,333 | 9,722,389 | 9,154,821 | 7,549,147 | 5,394,914 | 4,408,045 | 3,249,570 | 3,183,087 | 2,000,598 | 1,933,545 | 1,619,519 |
| many             |  2,196,242 |    19,312 |       371 |       140 | 1,189,736 |    58,428 |   444,021 |   431,385 |       498 |       199 |        54 |
| important        |  2,149,576 |   357,754 |   291,396 |   747,570 |   102,101 |    17,182 |    12,196 |    90,543 |    70,866 |     1,739 |     6,585 |
| good             |  1,898,254 |   477,150 |    18,870 |     5,202 |   135,194 |    95,800 |    56,060 |   190,463 |   257,760 |    12,879 |   243,512 |
| much             |  1,728,295 |    41,190 |       101 |        22 |   592,727 |    66,385 |   570,546 |   349,470 |     1,823 |       280 |    57,867 |
| likely           |  1,037,857 |    33,569 |   495,783 |   192,118 |       575 |    46,814 |       899 |    29,733 |       340 |       249 |     1,310 |
| more             |  1,019,626 |        69 |     2,277 |        90 |     2,941 |    17,630 |        51 |     2,841 |     4,466 |   349,076 |        13 |
| different        |    860,954 |   229,767 |     5,440 |     1,363 |    33,561 |     4,017 |     2,835 |     8,680 |     6,179 |    33,360 |     2,138 |
| popular          |    810,253 |    86,889 |    69,048 |   398,297 |    41,443 |     4,546 |     1,699 |     9,989 |     4,868 |     1,233 |     3,209 |
| available        |    807,114 |       376 |     9,647 |     1,379 |       428 |   132,250 |       243 |     1,559 |       300 |       939 |        31 |
| difficult        |    803,104 |   185,754 |   218,516 |    76,506 |    23,934 |    19,817 |    20,492 |    11,406 |    18,475 |       464 |     5,635 |
| better           |    716,836 |        93 |     1,737 |        66 |       860 |    13,514 |        29 |     1,973 |     1,619 |   283,999 |        15 |
| sure             |    715,325 |     4,016 |     2,183 |       314 |     9,092 |   466,983 |       621 |     3,186 |     2,227 |       319 |    84,250 |
| easy             |    680,953 |   122,808 |     5,420 |     1,201 |    71,043 |    95,375 |    39,258 |    49,857 |    29,040 |       727 |    31,745 |
| high             |    566,531 |   135,495 |     5,211 |    10,389 |    33,618 |     5,762 |    74,787 |    60,951 |    10,869 |       549 |    12,988 |
| common           |    544,248 |    43,469 |    85,255 |   272,621 |    13,573 |     7,171 |     9,972 |     7,689 |     1,432 |       901 |     7,176 |

## Totals

### Total Tokens per Frequency Group

|            |     totals |
|:-----------|-----------:|
| ALL        | 83,284,343 |
| `RBdirect` |  3,148,010 |
| DIFF       | 80,136,333 |

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

### Marginal Frequencies for `RBdirect` Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                   808 |                 3,132 |
| std   |                 4,748 |                25,278 |
| min   |                     0 |                     0 |
| 25%   |                    34 |                    16 |
| 50%   |                    87 |                    49 |
| 75%   |                   297 |                   205 |
| max   |               132,226 |               526,827 |

### Marginal Frequencies for DIFF Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                20,579 |                79,738 |
| std   |                88,045 |               566,480 |
| min   |                   801 |                   757 |
| 25%   |                 1,600 |                 1,661 |
| 50%   |                 3,368 |                 3,969 |
| 75%   |                10,266 |                15,230 |
| max   |             2,196,242 |             9,722,389 |

#### Top 30 ADV totals comparison

| `adv_form_lower` | RBdirect/ALL | DIFF/ALL | RBdirect_RAW |     DIFF_RAW |
|:-----------------|-------------:|---------:|-------------:|-------------:|
| necessarily      |         0.76 |     0.24 |    41,009.00 |    13,072.00 |
| exactly          |         0.71 |     0.29 |    41,973.00 |    17,501.00 |
| that             |         0.66 |     0.34 |   165,061.00 |    84,460.00 |
| immediately      |         0.56 |     0.44 |    57,132.00 |    44,031.00 |
| yet              |         0.53 |     0.47 |    51,866.00 |    45,127.00 |
| terribly         |         0.26 |     0.74 |    17,854.00 |    50,286.00 |
| remotely         |         0.26 |     0.74 |     5,504.00 |    15,904.00 |
| only             |         0.25 |     0.75 |   109,955.00 |   335,962.00 |
| consciously      |         0.22 |     0.78 |       914.00 |     3,154.00 |
| altogether       |         0.22 |     0.78 |     4,413.00 |    15,230.00 |
| anymore          |         0.22 |     0.78 |       414.00 |     1,450.00 |
| entirely         |         0.21 |     0.79 |    62,400.00 |   229,439.00 |
| overly           |         0.20 |     0.80 |    24,028.00 |    93,559.00 |
| precisely        |         0.20 |     0.80 |       764.00 |     3,079.00 |
| anywhere         |         0.18 |     0.82 |       212.00 |       939.00 |
| mobile           |         0.18 |     0.82 |       484.00 |     2,200.00 |
| in               |         0.18 |     0.82 |       162.00 |       757.00 |
| appreciably      |         0.17 |     0.83 |       232.00 |     1,124.00 |
| merely           |         0.17 |     0.83 |     5,320.00 |    26,365.00 |
| any              |         0.16 |     0.84 |    15,342.00 |    78,244.00 |
| always           |         0.16 |     0.84 |   103,441.00 |   535,793.00 |
| unduly           |         0.16 |     0.84 |       899.00 |     4,659.00 |
| outright         |         0.16 |     0.84 |     1,189.00 |     6,384.00 |
| directly         |         0.15 |     0.85 |     8,065.00 |    44,776.00 |
| lawfully         |         0.15 |     0.85 |       145.00 |       825.00 |
| overtly          |         0.15 |     0.85 |     2,037.00 |    11,839.00 |
| as               |         0.14 |     0.86 |   526,827.00 | 3,183,087.00 |
| adequately       |         0.14 |     0.86 |       308.00 |     1,896.00 |
| automatically    |         0.14 |     0.86 |       775.00 |     4,885.00 |
| mutually         |         0.13 |     0.87 |     5,928.00 |    38,595.00 |

#### Top 30 ADJ totals comparison

| `adj_form_lower` | RBdirect/ALL | DIFF/ALL | RBdirect_RAW |   DIFF_RAW |
|:-----------------|-------------:|---------:|-------------:|-----------:|
| shabby           |         0.69 |     0.31 |     5,533.00 |   2,430.00 |
| farfetched       |         0.32 |     0.68 |       568.00 |   1,202.00 |
| clear-cut        |         0.31 |     0.69 |     1,367.00 |   3,020.00 |
| rosy             |         0.31 |     0.69 |     2,075.00 |   4,590.00 |
| dissimilar       |         0.29 |     0.71 |     2,524.00 |   6,251.00 |
| far-fetched      |         0.29 |     0.71 |     1,964.00 |   4,865.00 |
| cut              |         0.25 |     0.75 |       385.00 |   1,163.00 |
| binding          |         0.24 |     0.76 |       683.00 |   2,124.00 |
| hasty            |         0.23 |     0.77 |       588.00 |   1,915.00 |
| flashy           |         0.23 |     0.77 |     1,611.00 |   5,326.00 |
| distant          |         0.21 |     0.79 |     8,180.00 |  30,231.00 |
| bad              |         0.19 |     0.81 |   105,134.00 | 449,564.00 |
| forthcoming      |         0.18 |     0.82 |     2,016.00 |   9,206.00 |
| unsightly        |         0.18 |     0.82 |       273.00 |   1,280.00 |
| enthused         |         0.17 |     0.83 |       437.00 |   2,066.00 |
| altruistic       |         0.17 |     0.83 |       490.00 |   2,375.00 |
| fond             |         0.17 |     0.83 |     6,667.00 |  32,900.00 |
| thrilled         |         0.16 |     0.84 |     4,804.00 |  24,408.00 |
| keen             |         0.16 |     0.84 |     9,131.00 |  46,424.00 |
| indicative       |         0.16 |     0.84 |     2,071.00 |  10,634.00 |
| late             |         0.16 |     0.84 |    26,301.00 | 136,200.00 |
| fancy            |         0.16 |     0.84 |     1,905.00 |  10,300.00 |
| quantifiable     |         0.16 |     0.84 |       243.00 |   1,315.00 |
| greener          |         0.16 |     0.84 |       523.00 |   2,849.00 |
| sure             |         0.15 |     0.85 |   128,741.00 | 715,325.00 |
| fussy            |         0.15 |     0.85 |       779.00 |   4,337.00 |
| exclusive        |         0.15 |     0.85 |     6,191.00 |  34,817.00 |
| clear            |         0.15 |     0.85 |    72,836.00 | 416,469.00 |
| nostalgia        |         0.15 |     0.85 |       163.00 |     945.00 |
| glamorous        |         0.14 |     0.86 |     2,497.00 |  14,926.00 |
