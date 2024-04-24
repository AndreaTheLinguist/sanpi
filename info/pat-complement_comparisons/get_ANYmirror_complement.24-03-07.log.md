# Comparing Bigram Frequencies by Polarity

- for `35` corpus input `.conll` directories containing source `.conllu` files
- with word types limited to only those that account for at least $0.001\%$ of the cleaned dataset (as sourced from 35 corpus file inputs)
- file identifier = `thr0-001p.35f`
- pattern matches restricted to only token word types with at least `868` total tokens across all combinations

- Selected Paths
  - `/share/compling/projects/sanpi/results/freq_out/POSmirror/all-frq_adj-x-adv_thr0-001p.35f.pkl.gz`
  - `/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

- Selected Paths
  - `/share/compling/projects/sanpi/results/freq_out/NEGmirror/all-frq_adj-x-adv_thr0-001p.35f.pkl.gz`
  - `/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## _ALL_ (`POSmirror+NEGmirror` and non-`POSmirror+NEGmirror`) Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for`stats_all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADV-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.920

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean |   std | min | 25% | 50% | 75% |    max |   total | var_coeff |  range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|------:|----:|----:|----:|----:|-------:|--------:|----------:|-------:|---------:|------------:|------------:|---------------:|---------------:|
| unfailingly      | 3,894 |    1 |    11 |   0 |   0 |   0 |   0 |    615 |   2,953 |        14 |    615 |        0 |           0 |           0 |              1 |              1 |
| importantly      | 3,894 |    1 |     4 |   0 |   0 |   0 |   0 |    114 |   3,253 |         5 |    114 |        0 |           0 |           0 |              1 |              1 |
| strategically    | 3,894 |    3 |    84 |   0 |   0 |   0 |   0 |  5,178 |  10,089 |        32 |  5,178 |        0 |           0 |           0 |              1 |              1 |
| slightly         | 3,894 |   95 | 1,129 |   0 |   1 |   5 |  27 | 54,601 | 369,929 |        12 | 54,601 |       26 |          66 |         -38 |              8 |              3 |
| devilishly       | 3,894 |    1 |     9 |   0 |   0 |   0 |   0 |    332 |   2,772 |        13 |    332 |        0 |           0 |           0 |              1 |              1 |
| habitually       | 3,894 |    0 |     3 |   0 |   0 |   0 |   0 |    141 |   1,235 |        10 |    141 |        0 |           0 |           0 |              1 |              1 |

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

- Saving `adj_form_lower` descriptive statististics for`stats_all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADJ-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.963

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean | std | min | 25% | 50% | 75% |   max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|------:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| shitty           | 1,005 |    4 |  39 |   0 |   0 |   0 |   1 |   890 | 3,972 |        10 |   890 |        1 |           2 |          -2 |              1 |              1 |
| sly              | 1,005 |    1 |   8 |   0 |   0 |   0 |   0 |   200 |   956 |         8 |   200 |        0 |           0 |           0 |              1 |              1 |
| cognitive        | 1,005 |    1 |  16 |   0 |   0 |   0 |   0 |   466 | 1,306 |        13 |   466 |        0 |           0 |           0 |              1 |              1 |
| fresher          | 1,005 |    2 |  22 |   0 |   0 |   0 |   0 |   671 | 1,655 |        14 |   671 |        0 |           0 |           0 |              1 |              1 |
| discreet         | 1,005 |    7 |  83 |   0 |   0 |   0 |   0 | 2,082 | 6,887 |        12 | 2,082 |        0 |           0 |           0 |              1 |              1 |
| satirical        | 1,005 |    2 |  10 |   0 |   0 |   0 |   1 |   186 | 2,106 |         5 |   186 |        1 |           2 |          -2 |              2 |              1 |

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

| `adj_form_lower` |      `SUM` |  almost | significantly | generally | economically | sharply | disproportionately |
|:-----------------|-----------:|--------:|--------------:|----------:|-------------:|--------:|-------------------:|
| `SUM`            | 83,284,343 | 421,181 |       137,734 |   130,377 |       50,932 |  16,529 |             11,541 |
| bad              |    554,698 |      67 |            44 |       597 |           27 |       0 |                 18 |
| reliable         |    103,318 |      13 |             3 |       368 |            9 |       0 |                  0 |
| apparent         |     63,808 |       8 |             9 |        31 |            1 |      10 |                  0 |
| independent      |     62,940 |     172 |             3 |       146 |          552 |       0 |                  0 |
| fresh            |     57,485 |      71 |             5 |        38 |            0 |       2 |                  0 |
| brilliant        |     45,868 |      63 |             0 |        42 |            8 |       1 |                  0 |

## _`POSmirror`_ Frequencies Overview

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

| `adj_form_lower` |     `SUM` |   all | relatively |  only | easily |  real | directly | remarkably |
|:-----------------|----------:|------:|-----------:|------:|-------:|------:|---------:|-----------:|
| `SUM`            | 1,675,501 | 6,066 |      5,642 | 4,831 |  2,873 | 1,609 |    1,555 |      1,035 |
| new              |    12,530 |    60 |        640 |     7 |      0 |     0 |        0 |          3 |
| real             |     5,780 |    17 |          1 |     6 |      0 |     1 |        0 |          0 |
| free             |     4,666 |    19 |         20 |    17 |      0 |     1 |        0 |          6 |
| valuable         |     4,579 |     2 |          3 |     8 |      0 |     1 |        0 |          1 |
| crazy            |     2,042 |     7 |          1 |     3 |      0 |     7 |        0 |          0 |
| confusing        |     1,975 |     0 |          0 |     0 |      1 |     0 |        0 |          0 |
| reliable         |     1,135 |     1 |          4 |     0 |      0 |     1 |        0 |          0 |

## _`NEGmirror`_ Frequencies Overview

### Full Table Preview of _`NEGmirror`_ Frequencies

| `adj_form_lower`  | `SUM`  | more  | too   | as    | so    | really | ... | palpably | painstakingly | suspiciously | duly | dynamically | proportionally |
|:------------------|:-------|:------|:------|:------|:------|:-------|:----|:---------|:--------------|:-------------|:-----|:------------|:---------------|
| `SUM`             | 285435 | 77335 | 46567 | 30872 | 24760 | 11124  | ... | 1        | 1             | 1            | 1    | 1           | 1              |
| important         | 14968  | 12396 | 70    | 1045  | 532   | 114    | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| late              | 11139  | 0     | 11087 | 5     | 5     | 1      | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| good              | 8697   | 12    | 519   | 3471  | 432   | 301    | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| sure              | 5814   | 94    | 539   | 22    | 170   | 912    | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| wrong             | 5329   | 224   | 14    | 13    | 99    | 529    | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| ...               | ...    | ...   | ...   | ...   | ...   | ...    | ... | ...      | ...           | ...          | ...  | ...         | ...            |
| knowledgable      | 1      | 0     | 0     | 0     | 0     | 0      | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| lacklustre        | 1      | 1     | 0     | 0     | 0     | 0      | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| understaffed      | 1      | 0     | 0     | 0     | 0     | 0      | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| latin             | 1      | 0     | 0     | 0     | 0     | 0      | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| under-appreciated | 1      | 0     | 0     | 0     | 1     | 0      | ... | 0        | 0             | 0            | 0    | 0           | 0              |
| 3d                | 1      | 0     | 0     | 0     | 0     | 1      | ... | 0        | 0             | 0            | 0    | 0           | 0              |

### (Semi-)Random Sample of _`NEGmirror`_ Frequencies

| `adj_form_lower` |   `SUM` | exactly | economically | strictly | widely | environmentally | intellectually | spectacularly |
|:-----------------|--------:|--------:|-------------:|---------:|-------:|----------------:|---------------:|--------------:|
| `SUM`            | 285,435 |     787 |          144 |      131 |     89 |              68 |             62 |            44 |
| successful       |   1,307 |       0 |            3 |        0 |      0 |               0 |              0 |             1 |
| enough           |     985 |       0 |            0 |        0 |      0 |               0 |              0 |             0 |
| appealing        |     495 |       1 |            0 |        0 |      0 |               0 |              0 |             0 |
| straightforward  |     351 |       3 |            0 |        0 |      0 |               0 |              0 |             0 |
| cheap            |     229 |       7 |            0 |        0 |      0 |               0 |              0 |             0 |
| devastating      |     221 |       0 |            1 |        0 |      0 |               1 |              0 |             0 |
| angry            |     193 |       0 |            0 |        0 |      0 |               0 |              0 |             0 |

👀 sanity dimension checks

|                    dataframe | # rows | # columns |
|-----------------------------:|-------:|----------:|
| only `POSmirror`+`NEGmirror` |   3895 |      1006 |
|                          ALL |   3895 |      1006 |
|                 adjusted NEG |   3895 |      1006 |

## Words with 0 tokens in the `POSmirror`+`NEGmirror` results

### Adjectives

| `adj_form_lower` | SUM_`POSmirror`+`NEGmirror` | `SUM` |
|:-----------------|----------------------------:|------:|
| famed            |                           0 |   879 |

### Adverbs

| `adv_form_lower` | SUM_`POSmirror`+`NEGmirror` | `SUM` |
|------------------|-----------------------------|-------|
| n/a              |                             |       |

## The Difference

| `adj_form_lower` | `SUM`    | very    | more    | ... | cosmetically | second-most | pointedly |
|:-----------------|:---------|:--------|:--------|:----|:-------------|:------------|:----------|
| `SUM`            | 81323407 | 9715385 | 9008523 | ... | 837          | 863         | 841       |
| many             | 2206304  | 21200   | 370     | ... | 0            | 0           | 0         |
| important        | 2150654  | 352860  | 281483  | ... | 9            | 101         | 0         |
| ...              | ...      | ...     | ...     | ... | ...          | ...         | ...       |
| contiguous       | 851      | 4       | 104     | ... | 0            | 0           | 0         |
| panicked         | 848      | 50      | 154     | ... | 0            | 0           | 0         |
| oversized        | 849      | 32      | 43      | ... | 0            | 0           | 0         |

### Descriptive _Complement_ Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for`stats_diff_combined_POSmirror-NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/combined_POSmirror-NEGmirror/complement/descriptive_stats/ADV-stats_diff_combined_POSmirror-NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.511

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% |    max |   total | var_coeff |  range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|-------:|--------:|----------:|-------:|---------:|------------:|------------:|---------------:|---------------:|
| often            | 3,894 |   81 | 315 |   0 |   5 |  18 |  54 | 11,713 | 316,104 |         4 | 11,713 |       49 |         128 |         -68 |             20 |              7 |
| mechanically     | 3,894 |    1 |   8 |   0 |   0 |   0 |   0 |    340 |   2,883 |        11 |    340 |        0 |           0 |           0 |              1 |              1 |
| impressively     | 3,894 |    2 |  15 |   0 |   0 |   0 |   1 |    589 |   8,789 |         6 |    589 |        1 |           2 |          -2 |              2 |              1 |
| vocally          | 3,894 |    0 |   3 |   0 |   0 |   0 |   0 |    116 |   1,471 |         7 |    116 |        0 |           0 |           0 |              1 |              1 |
| thoroughly       | 3,894 |   10 |  84 |   0 |   0 |   1 |   4 |  2,977 |  38,151 |         9 |  2,977 |        4 |          10 |          -6 |              3 |              2 |
| scandalously     | 3,894 |    0 |   2 |   0 |   0 |   0 |   0 |     61 |     856 |         8 |     61 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adv_form_lowers |
|:------------|------------------------------:|
| count       |                         3,894 |
| mean        |                        20,884 |
| std         |                        89,914 |
| min         |                           529 |
| 25%         |                         1,600 |
| 50%         |                         3,378 |
| 75%         |                        10,374 |
| max         |                     2,206,304 |
| total       |                    81,323,407 |
| var_coeff   |                             4 |
| range       |                     2,205,775 |
| IQ_range    |                         8,774 |
| upper_fence |                        23,534 |
| lower_fence |                       -11,561 |

### Descriptive _Complement_ Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for`stats_diff_combined_POSmirror-NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/combined_POSmirror-NEGmirror/complement/descriptive_stats/ADJ-stats_diff_combined_POSmirror-NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.789

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean |   std | min | 25% | 50% | 75% |     max |   total | var_coeff |   range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|------:|----:|----:|----:|----:|--------:|--------:|----------:|--------:|---------:|------------:|------------:|---------------:|---------------:|
| brave            | 1,005 |   19 |   195 |   0 |   0 |   0 |   2 |   5,150 |  18,919 |        10 |   5,150 |        2 |           5 |          -3 |              2 |              1 |
| few              | 1,005 |  268 | 5,517 |   0 |   0 |   0 |   2 | 169,681 | 269,540 |        21 | 169,681 |        2 |           5 |          -3 |              2 |              1 |
| busy             | 1,005 |  187 | 2,224 |   0 |   0 |   1 |   6 |  55,379 | 187,745 |        12 |  55,379 |        6 |          15 |          -9 |              4 |              2 |
| fond             | 1,005 |   38 |   361 |   0 |   0 |   0 |   1 |   8,242 |  38,325 |         9 |   8,242 |        1 |           2 |          -2 |              2 |              1 |
| flippant         | 1,005 |    1 |     8 |   0 |   0 |   0 |   0 |     122 |   1,134 |         7 |     122 |        0 |           0 |           0 |              1 |              1 |
| viewable         | 1,005 |    2 |    17 |   0 |   0 |   0 |   0 |     322 |   2,111 |         8 |     322 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across adj_form_lowers |
|:------------|------------------------------:|
| count       |                         1,005 |
| mean        |                        80,919 |
| std         |                       568,719 |
| min         |                           783 |
| 25%         |                         1,664 |
| 50%         |                         3,946 |
| 75%         |                        15,409 |
| max         |                     9,715,385 |
| total       |                    81,323,407 |
| var_coeff   |                             7 |
| range       |                     9,714,602 |
| IQ_range    |                        13,745 |
| upper_fence |                        36,026 |
| lower_fence |                       -18,954 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/combined_POSmirror-NEGmirror/complement/images/sample-heatmap_diff_combined_POSmirror-NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.png`

✅ complement frequency table saved as `/share/compling/projects/sanpi/results/freq_out/combined_POSmirror-NEGmirror/complement/diff_combined_POSmirror-NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

### Adverb stats for complement

|       | non-`POSmirror+NEGmirror` ADJ totals |
|:------|-------------------------------------:|
| count |                             3,895.00 |
| mean  |                            41,757.85 |
| std   |                         1,305,816.09 |
| min   |                               529.00 |
| 25%   |                             1,600.00 |
| 50%   |                             3,378.00 |
| 75%   |                            10,391.50 |
| max   |                        81,323,407.00 |

### Adverb stats for complement

|       | non-`POSmirror+NEGmirror` ADV totals |
|:------|-------------------------------------:|
| count |                             1,006.00 |
| mean  |                           161,676.75 |
| std   |                         2,623,756.09 |
| min   |                               783.00 |
| 25%   |                             1,665.25 |
| 50%   |                             3,950.00 |
| 75%   |                            15,542.50 |
| max   |                        81,323,407.00 |

## Frequency Table Corners

### ALL

| `adj_form_lower` | `SUM`    | very    | more    | most    | ... | touchingly | cosmetically | second-most | pointedly |
|:-----------------|:---------|:--------|:--------|:--------|:----|:-----------|:-------------|:------------|:----------|
| `SUM`            | 83284343 | 9913432 | 9320997 | 7568812 | ... | 872        | 869          | 869         | 868       |
| many             | 2210387  | 21237   | 373     | 140     | ... | 0          | 0            | 0           | 0         |
| important        | 2199447  | 359610  | 306604  | 748533  | ... | 0          | 9            | 105         | 0         |
| good             | 2030480  | 507499  | 18902   | 5207    | ... | 1          | 7            | 0           | 0         |
| ...              | ...      | ...     | ...     | ...     | ... | ...        | ...          | ...         | ...       |
| carnal           | 872      | 34      | 150     | 62      | ... | 0          | 0            | 0           | 0         |
| contiguous       | 871      | 4       | 106     | 8       | ... | 0          | 0            | 0           | 0         |
| panicked         | 871      | 54      | 159     | 31      | ... | 0          | 0            | 0           | 0         |
| oversized        | 870      | 32      | 45      | 16      | ... | 0          | 0            | 0           | 0         |

### `POSmirror+NEGmirror`

| `adj_form_lower` | `SUM`   | very   | more   | most  | ... | touchingly | cosmetically | second-most | pointedly |
|:-----------------|:--------|:-------|:-------|:------|:----|:-----------|:-------------|:------------|:----------|
| `SUM`            | 1960936 | 198047 | 312474 | 20794 | ... | 43         | 32           | 6           | 27        |
| many             | 4083    | 37     | 3      | 0     | ... | 0          | 0            | 0           | 0         |
| important        | 48793   | 6750   | 25121  | 1254  | ... | 0          | 0            | 4           | 0         |
| good             | 37987   | 8045   | 88     | 5     | ... | 1          | 0            | 0           | 0         |
| ...              | ...     | ...    | ...    | ...   | ... | ...        | ...          | ...         | ...       |
| carnal           | 25      | 2      | 9      | 2     | ... | 0          | 0            | 0           | 0         |
| contiguous       | 20      | 0      | 2      | 0     | ... | 0          | 0            | 0           | 0         |
| panicked         | 23      | 4      | 5      | 0     | ... | 0          | 0            | 0           | 0         |
| oversized        | 21      | 0      | 2      | 0     | ... | 0          | 0            | 0           | 0         |

### _Complement_

| `adj_form_lower` | `SUM`    | very    | more    | most    | ... | touchingly | cosmetically | second-most | pointedly |
|:-----------------|:---------|:--------|:--------|:--------|:----|:-----------|:-------------|:------------|:----------|
| `SUM`            | 81323407 | 9715385 | 9008523 | 7548018 | ... | 829        | 837          | 863         | 841       |
| many             | 2206304  | 21200   | 370     | 140     | ... | 0          | 0            | 0           | 0         |
| important        | 2150654  | 352860  | 281483  | 747279  | ... | 0          | 9            | 101         | 0         |
| good             | 1992493  | 499454  | 18814   | 5202    | ... | 0          | 7            | 0           | 0         |
| ...              | ...      | ...     | ...     | ...     | ... | ...        | ...          | ...         | ...       |
| carnal           | 847      | 32      | 141     | 60      | ... | 0          | 0            | 0           | 0         |
| contiguous       | 851      | 4       | 104     | 8       | ... | 0          | 0            | 0           | 0         |
| panicked         | 848      | 50      | 154     | 31      | ... | 0          | 0            | 0           | 0         |
| oversized        | 849      | 32      | 43      | 16      | ... | 0          | 0            | 0           | 0         |

## Juxtaposed Sample (√ frequencies)

| `adj_form_lower`       | extremely | particularly | slightly |  that | absolutely | fairly |  ever | fully | somewhat | remotely | utterly | definitely | necessarily | exactly |
|:-----------------------|----------:|-------------:|---------:|------:|-----------:|-------:|------:|------:|---------:|---------:|--------:|-----------:|------------:|--------:|
| adjustable             |      6.00 |         2.00 |     6.63 |  0.00 |       3.16 |   1.41 |  2.45 | 59.65 |     3.87 |     2.83 |    1.41 |       1.00 |        0.00 |    0.00 |
| adjustable-`MIRROR`    |      0.00 |         0.00 |     0.00 |  0.00 |       1.00 |   0.00 |  0.00 |  4.58 |     1.41 |     0.00 |    0.00 |       0.00 |        0.00 |    0.00 |
| beneficial             |     69.26 |        43.99 |     4.47 |  8.06 |       7.55 |   5.20 |  2.83 |  4.00 |     7.81 |     3.16 |    2.45 |      15.97 |       10.54 |    2.83 |
| beneficial-`MIRROR`    |      8.66 |         4.47 |     1.73 |  0.00 |       1.00 |   1.00 |  2.24 |  1.00 |     0.00 |     1.73 |    1.00 |       1.00 |        2.65 |    1.00 |
| certain                |      6.93 |         5.74 |     3.32 |  8.00 |      75.80 |  87.11 |  7.62 | 10.54 |     7.48 |     2.00 |    8.60 |       8.94 |        8.49 |   13.23 |
| certain-`MIRROR`       |      1.00 |         1.41 |     0.00 |  2.24 |      12.77 |   6.93 | 11.96 |  4.58 |     1.00 |     1.00 |    1.00 |       1.00 |        0.00 |    2.65 |
| competitive            |     75.15 |        17.38 |     7.35 | 12.45 |       6.48 |  19.92 | 14.87 | 18.95 |    16.09 |    11.45 |    1.73 |       8.06 |        4.69 |    3.74 |
| competitive-`MIRROR`   |      8.37 |         3.16 |     0.00 |  2.65 |       0.00 |   2.24 |  2.00 |  1.41 |     1.41 |     2.24 |    0.00 |       1.00 |        0.00 |    0.00 |
| customizable           |     16.61 |         2.24 |     2.24 |  2.24 |       5.00 |   4.24 |  1.73 | 72.57 |     4.36 |     1.41 |    2.24 |       1.73 |        1.00 |    0.00 |
| customizable-`MIRROR`  |      1.41 |         0.00 |     0.00 |  0.00 |       1.00 |   0.00 |  0.00 | 10.05 |     1.00 |     0.00 |    0.00 |       0.00 |        0.00 |    0.00 |
| dim                    |     10.39 |         6.32 |    10.15 |  1.73 |       1.00 |   9.22 |  1.73 |  1.00 |    11.00 |     0.00 |    0.00 |       1.00 |        1.00 |    0.00 |
| dim-`MIRROR`           |      1.00 |         1.41 |     0.00 |  0.00 |       0.00 |   1.73 |  0.00 |  0.00 |     1.00 |     0.00 |    1.00 |       0.00 |        0.00 |    0.00 |
| evocative              |      8.43 |        13.86 |     3.00 |  1.41 |       2.24 |   3.32 |  2.83 |  1.41 |     5.00 |     1.41 |    2.45 |       2.24 |        1.41 |    1.41 |
| evocative-`MIRROR`     |      1.41 |         2.00 |     0.00 |  0.00 |       0.00 |   0.00 |  0.00 |  0.00 |     0.00 |     0.00 |    0.00 |       0.00 |        1.00 |    0.00 |
| heartbreaking          |      6.86 |        13.42 |     4.00 |  1.41 |      20.98 |   1.73 |  1.41 |  1.00 |     5.29 |     0.00 |   12.33 |       3.87 |        1.00 |    1.41 |
| heartbreaking-`MIRROR` |      1.00 |         3.32 |     1.00 |  1.00 |       3.74 |   0.00 |  0.00 |  0.00 |     0.00 |     0.00 |    1.73 |       0.00 |        0.00 |    0.00 |
| horny                  |     21.73 |         6.00 |     2.83 |  1.41 |       3.61 |   1.00 |  6.08 |  2.00 |     2.83 |     2.65 |    2.45 |       4.36 |        1.00 |    1.00 |
| horny-`MIRROR`         |      3.61 |         0.00 |     0.00 |  0.00 |       0.00 |   0.00 |  0.00 |  0.00 |     0.00 |     0.00 |    0.00 |       0.00 |        0.00 |    0.00 |
| internal               |      2.24 |         2.00 |     1.00 |  1.73 |       0.00 |   1.41 |  2.65 |  4.90 |     2.00 |     0.00 |    0.00 |       1.00 |        2.00 |    1.00 |
| internal-`MIRROR`      |      0.00 |         0.00 |     0.00 |  0.00 |       0.00 |   0.00 |  0.00 |  0.00 |     0.00 |     0.00 |    0.00 |       0.00 |        0.00 |    0.00 |
| larger                 |      4.24 |         8.60 |   112.12 |  2.83 |       3.61 |   5.10 | 51.93 |  0.00 |    39.71 |     1.73 |    1.00 |      10.30 |        5.74 |    1.41 |
| larger-`MIRROR`        |      0.00 |         0.00 |    15.91 |  0.00 |       0.00 |   0.00 |  1.41 |  0.00 |     5.74 |     0.00 |    0.00 |       0.00 |        0.00 |    0.00 |
| miserable              |      9.00 |         9.70 |     5.57 |  5.20 |      25.00 |  11.87 |  2.83 |  1.41 |     7.48 |     1.41 |   17.55 |       2.24 |        2.24 |    1.41 |
| miserable-`MIRROR`     |      2.00 |         1.00 |     0.00 |  1.00 |       3.32 |   1.00 |  1.00 |  0.00 |     1.00 |     0.00 |    2.45 |       0.00 |        0.00 |    0.00 |
| quieter                |      1.00 |         1.41 |    14.76 |  0.00 |       0.00 |   0.00 |  3.87 |  0.00 |    10.15 |     0.00 |    0.00 |       6.56 |        1.73 |    1.00 |
| quieter-`MIRROR`       |      0.00 |         0.00 |     0.00 |  0.00 |       0.00 |   0.00 |  0.00 |  0.00 |     0.00 |     0.00 |    0.00 |       0.00 |        0.00 |    0.00 |

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

### Top (15 x 10) collocations in `POSmirror`+`NEGmirror` frequencies (+ `SUM`)

| `adj_form_lower` |     `SUM` |    more |    very |     too |      so |      as |   even |    not | really |  quite |   just |
|:-----------------|----------:|--------:|--------:|--------:|--------:|--------:|-------:|-------:|-------:|-------:|-------:|
| `SUM`            | 1,960,936 | 312,474 | 198,047 | 186,765 | 143,323 | 125,578 | 75,551 | 72,058 | 63,523 | 43,128 | 30,898 |
| important        |    48,793 |  25,121 |   6,750 |     305 |   2,007 |   4,052 |     60 |    484 |  1,869 |    162 |     23 |
| different        |    40,096 |     769 |   6,875 |     186 |   2,088 |     163 |     66 |     42 |    702 |  3,508 |    300 |
| good             |    37,987 |      88 |   8,045 |   1,970 |   2,914 |   6,773 |    450 |  2,069 |  4,141 |  1,208 |    308 |
| simple           |    27,767 |     610 |   1,945 |     413 |   3,114 |  17,656 |     30 |     51 |    360 |    508 |     53 |
| wrong            |    23,764 |     288 |   3,103 |      24 |     497 |      80 |    143 |    129 |  1,423 |     92 |    385 |
| easy             |    21,735 |     337 |   1,581 |   8,000 |   3,851 |   1,971 |     47 |  1,218 |    442 |    269 |     53 |
| difficult        |    18,044 |   6,293 |   3,827 |   1,555 |     731 |     474 |    120 |     80 |    406 |    576 |     65 |
| special          |    16,913 |   2,027 |   5,231 |     487 |   1,122 |     309 |     26 |     21 |  3,294 |    486 |     31 |
| better           |    16,184 |     141 |       0 |       1 |      14 |      22 |  6,971 |    108 |     48 |      9 |    471 |
| close            |    15,923 |      62 |   4,419 |   1,384 |   1,815 |   2,295 |  1,644 |    140 |    646 |    216 |     30 |
| happy            |    15,693 |     199 |   2,931 |   2,930 |   2,603 |     502 |     88 |    984 |    978 |    395 |    613 |
| likely           |    15,428 |   9,511 |     619 |     340 |      38 |     302 |    178 |    366 |     17 |     58 |      7 |
| right            |    15,345 |     121 |      83 |      18 |     130 |      12 |     46 |  4,699 |     68 |    438 |    824 |
| small            |    15,022 |      48 |   1,398 |   7,408 |   1,532 |   2,552 |    104 |     23 |    234 |    363 |     21 |
| available        |    14,654 |     163 |      16 |      15 |      41 |      23 |    220 |  2,659 |     25 |      4 |     19 |

### Top (15 x 10) collocations in DIFF frequencies (+ `SUM`)

| `adj_form_lower` |      `SUM` |      very |      more |      most |        so |       not |        as |       too |    really |      much |    pretty |
|:-----------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| `SUM`            | 81,323,407 | 9,715,385 | 9,008,523 | 7,548,018 | 5,592,641 | 4,343,727 | 3,584,336 | 3,370,675 | 2,032,534 | 1,959,836 | 1,595,385 |
| many             |  2,206,304 |    21,200 |       370 |       140 | 1,191,658 |    58,317 |   432,879 |   448,909 |       517 |       201 |        54 |
| important        |  2,150,654 |   352,860 |   281,483 |   747,279 |   103,502 |    16,867 |    98,771 |    12,574 |    70,306 |     1,807 |     6,444 |
| good             |  1,992,493 |   499,454 |    18,814 |     5,202 |   150,282 |    94,074 |   228,575 |    57,713 |   256,140 |    14,110 |   241,415 |
| much             |  1,768,910 |    42,088 |        97 |        22 |   614,120 |    66,202 |   354,584 |   578,002 |     2,987 |       283 |    57,736 |
| likely           |  1,032,936 |    35,280 |   488,890 |   191,373 |       809 |    46,492 |    31,518 |       856 |       449 |       257 |     1,305 |
| more             |  1,018,858 |        69 |     2,263 |        90 |     2,856 |    17,545 |     2,840 |        52 |     4,466 |   353,368 |        13 |
| different        |    866,504 |   226,133 |    11,468 |     1,362 |    37,258 |     3,982 |     9,133 |     5,012 |     5,843 |    43,505 |     2,047 |
| available        |    848,288 |       387 |     9,576 |     1,375 |       449 |   129,712 |     1,856 |       262 |       527 |       963 |        32 |
| sure             |    832,781 |     4,600 |     2,163 |       314 |    35,210 |   464,263 |     3,848 |     8,151 |    19,194 |       338 |    83,992 |
| popular          |    821,223 |    88,433 |    68,960 |   398,361 |    42,545 |     4,462 |    14,596 |     2,030 |     4,911 |     1,301 |     3,177 |
| difficult        |    814,944 |   184,366 |   213,922 |    76,007 |    25,811 |    19,761 |    15,567 |    26,383 |    18,373 |       629 |     5,547 |
| easy             |    746,717 |   123,963 |     5,230 |     1,211 |    84,788 |    94,272 |    71,262 |    32,465 |    29,141 |       804 |    31,325 |
| better           |    724,537 |        93 |     1,615 |        66 |       858 |    13,432 |     1,968 |        29 |     1,722 |   291,916 |        16 |
| high             |    578,588 |   136,763 |     5,169 |    10,386 |    35,023 |     5,688 |    66,743 |    75,867 |    10,918 |       573 |    12,886 |
| common           |    547,350 |    45,303 |    84,847 |   272,631 |    14,925 |     7,108 |    11,052 |     5,002 |     1,503 |       915 |     7,124 |

## Totals

### Total Tokens per Frequency Group

|                         |     totals |
|:------------------------|-----------:|
| ALL                     | 83,284,343 |
| `POSmirror`+`NEGmirror` |  1,960,936 |
| DIFF                    | 81,323,407 |

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

### Marginal Frequencies for `POSmirror`+`NEGmirror` Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                   504 |                 1,951 |
| std   |                 1,936 |                15,107 |
| min   |                     0 |                     1 |
| 25%   |                    35 |                    38 |
| 50%   |                    84 |                    85 |
| 75%   |                   262 |                   321 |
| max   |                48,793 |               312,474 |

### Marginal Frequencies for DIFF Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                20,884 |                80,919 |
| std   |                89,914 |               568,719 |
| min   |                   529 |                   783 |
| 25%   |                 1,600 |                 1,664 |
| 50%   |                 3,378 |                 3,946 |
| 75%   |                10,374 |                15,409 |
| max   |             2,206,304 |             9,715,385 |

#### Top 30 ADV totals comparison

| `adv_form_lower` | `POSmirror`+NEGmirror/ALL | DIFF/ALL | `POSmirror`+NEGmirror_RAW |     DIFF_RAW |
|:-----------------|--------------------------:|---------:|--------------------------:|-------------:|
| else             |                      0.29 |     0.71 |                  1,006.00 |     2,426.00 |
| plain            |                      0.17 |     0.83 |                  5,895.00 |    28,631.00 |
| outright         |                      0.16 |     0.84 |                  1,219.00 |     6,354.00 |
| together         |                      0.14 |     0.86 |                    305.00 |     1,883.00 |
| maybe            |                      0.13 |     0.87 |                  2,785.00 |    18,106.00 |
| remotely         |                      0.12 |     0.88 |                  2,609.00 |    18,799.00 |
| around           |                      0.12 |     0.88 |                  1,085.00 |     8,061.00 |
| downright        |                      0.11 |     0.89 |                  5,266.00 |    43,866.00 |
| inherently       |                      0.11 |     0.89 |                  5,467.00 |    46,135.00 |
| on               |                      0.10 |     0.90 |                     89.00 |       783.00 |
| intrinsically    |                      0.10 |     0.90 |                    947.00 |     8,452.00 |
| innately         |                      0.10 |     0.90 |                    343.00 |     3,247.00 |
| altogether       |                      0.09 |     0.91 |                  1,769.00 |    17,874.00 |
| otherwise        |                      0.09 |     0.91 |                  8,614.00 |    89,634.00 |
| willfully        |                      0.09 |     0.91 |                    309.00 |     3,262.00 |
| confusingly      |                      0.09 |     0.91 |                     91.00 |       970.00 |
| tangentially     |                      0.08 |     0.92 |                    106.00 |     1,240.00 |
| terribly         |                      0.08 |     0.92 |                  5,119.00 |    63,021.00 |
| there            |                      0.07 |     0.93 |                    319.00 |     4,037.00 |
| simply           |                      0.07 |     0.93 |                  8,529.00 |   110,201.00 |
| unpleasantly     |                      0.07 |     0.93 |                     95.00 |     1,250.00 |
| unintentionally  |                      0.07 |     0.93 |                    242.00 |     3,219.00 |
| early            |                      0.07 |     0.93 |                    220.00 |     2,945.00 |
| indirectly       |                      0.07 |     0.93 |                    126.00 |     1,692.00 |
| knowingly        |                      0.07 |     0.93 |                     80.00 |     1,106.00 |
| even             |                      0.07 |     0.93 |                 75,551.00 | 1,044,654.00 |
| perversely       |                      0.07 |     0.93 |                     94.00 |     1,304.00 |
| indescribably    |                      0.07 |     0.93 |                    123.00 |     1,761.00 |
| seriously        |                      0.06 |     0.94 |                  4,350.00 |    63,162.00 |
| dreadfully       |                      0.06 |     0.94 |                    212.00 |     3,089.00 |

#### Top 30 ADJ totals comparison

| `adj_form_lower` | `POSmirror`+NEGmirror/ALL | DIFF/ALL | `POSmirror`+NEGmirror_RAW |   DIFF_RAW |
|:-----------------|--------------------------:|---------:|--------------------------:|-----------:|
| amiss            |                      0.56 |     0.44 |                    666.00 |     529.00 |
| sinister         |                      0.19 |     0.81 |                  3,330.00 |  14,186.00 |
| unenforceable    |                      0.14 |     0.86 |                    155.00 |     921.00 |
| objectionable    |                      0.14 |     0.86 |                    743.00 |   4,624.00 |
| triple           |                      0.14 |     0.86 |                    139.00 |     874.00 |
| fishy            |                      0.14 |     0.86 |                    218.00 |   1,396.00 |
| wrong            |                      0.13 |     0.87 |                 23,764.00 | 161,931.00 |
| peachy           |                      0.12 |     0.88 |                    128.00 |     905.00 |
| medium           |                      0.12 |     0.88 |                    180.00 |   1,328.00 |
| nefarious        |                      0.12 |     0.88 |                    347.00 |   2,567.00 |
| third            |                      0.12 |     0.88 |                    583.00 |   4,384.00 |
| trivial          |                      0.11 |     0.89 |                  1,466.00 |  12,338.00 |
| intangible       |                      0.10 |     0.90 |                    184.00 |   1,595.00 |
| fourth           |                      0.10 |     0.90 |                    257.00 |   2,271.00 |
| missing          |                      0.10 |     0.90 |                    294.00 |   2,602.00 |
| fancy            |                      0.10 |     0.90 |                  1,184.00 |  11,021.00 |
| primal           |                      0.09 |     0.91 |                    323.00 |   3,117.00 |
| foolhardy        |                      0.09 |     0.91 |                     93.00 |     985.00 |
| special          |                      0.09 |     0.91 |                 16,913.00 | 179,366.00 |
| late             |                      0.09 |     0.91 |                 13,991.00 | 148,510.00 |
| akin             |                      0.09 |     0.91 |                  1,276.00 |  13,595.00 |
| comforting       |                      0.08 |     0.92 |                  1,210.00 |  13,200.00 |
| wishful          |                      0.08 |     0.92 |                    201.00 |   2,221.00 |
| petty            |                      0.08 |     0.92 |                    285.00 |   3,183.00 |
| misinformed      |                      0.08 |     0.92 |                    110.00 |   1,246.00 |
| demoralizing     |                      0.08 |     0.92 |                     99.00 |   1,133.00 |
| galling          |                      0.08 |     0.92 |                    182.00 |   2,143.00 |
| injurious        |                      0.08 |     0.92 |                    125.00 |   1,481.00 |
| mundane          |                      0.08 |     0.92 |                  1,470.00 |  17,601.00 |
| magical          |                      0.08 |     0.92 |                  1,889.00 |  22,805.00 |
