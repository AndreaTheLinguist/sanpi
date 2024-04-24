# Comparing Bigram Frequencies by Polarity

- for `35` corpus input `.conll` directories containing source `.conllu` files
- with word types limited to only those that account for at least $0.001\%$ of the cleaned dataset (as sourced from 35 corpus file inputs)
- file identifier = `thr0-001p.35f`
- pattern matches restricted to only token word types with at least `868` total tokens across all combinations

- Selected Paths
  - `/share/compling/projects/sanpi/results/freq_out/NEGmirror/all-frq_adj-x-adv_thr0-001p.35f.pkl.gz`
  - `/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

## _`NEGmirror`_ Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for `stats_all-frq_adj-x-adv_thr0-001p.35f` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/NEGmirror/descriptive_stats/ADV-stats_all-frq_adj-x-adv_thr0-001p.35f.csv`
  - time elapsed: 00:00:00.283

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| shockingly       | 3,572 |    0 |   0 |   0 |   0 |   0 |   0 |   2 |    17 |        16 |     2 |        0 |           0 |           0 |              1 |              1 |
| brightly         | 3,572 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     1 |        60 |     1 |        0 |           0 |           0 |              1 |              1 |
| satisfyingly     | 3,572 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     2 |        42 |     1 |        0 |           0 |           0 |              1 |              1 |
| tragically       | 3,572 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     6 |        24 |     1 |        0 |           0 |           0 |              1 |              1 |
| overall          | 3,572 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     3 |        34 |     1 |        0 |           0 |           0 |              1 |              1 |
| interminably     | 3,572 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     1 |        60 |     1 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across `adv_form_lower`s |
|:------------|--------------------------------:|
| count       |                           3,572 |
| mean        |                              80 |
| std         |                             444 |
| min         |                               1 |
| 25%         |                               4 |
| 50%         |                              10 |
| 75%         |                              34 |
| max         |                          14,968 |
| total       |                         285,435 |
| var_coeff   |                               6 |
| range       |                          14,967 |
| IQ_range    |                              30 |
| upper_fence |                              80 |
| lower_fence |                             -41 |

### Descriptive Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for`stats_all-frq_adj-x-adv_thr0-001p.35f` as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/NEGmirror/descriptive_stats/ADJ-stats_all-frq_adj-x-adv_thr0-001p.35f.csv`
  - time elapsed: 00:00:00.846

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| homey            |   876 |    0 |   0 |   0 |   0 |   0 |   0 |   7 |    11 |        20 |     7 |        0 |           0 |           0 |              1 |              1 |
| unruly           |   876 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     3 |        17 |     1 |        0 |           0 |           0 |              1 |              1 |
| melodic          |   876 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     7 |        11 |     1 |        0 |           0 |           0 |              1 |              1 |
| hygienic         |   876 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     3 |        17 |     1 |        0 |           0 |           0 |              1 |              1 |
| dizzy            |   876 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     1 |        30 |     1 |        0 |           0 |           0 |              1 |              1 |
| lacklustre       |   876 |    0 |   0 |   0 |   0 |   0 |   0 |   1 |     1 |        30 |     1 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across `adj_form_lower`s |
|:------------|--------------------------------:|
| count       |                             876 |
| mean        |                             326 |
| std         |                           3,393 |
| min         |                               1 |
| 25%         |                               2 |
| 50%         |                               7 |
| 75%         |                              26 |
| max         |                          77,335 |
| total       |                         285,435 |
| var_coeff   |                              10 |
| range       |                          77,334 |
| IQ_range    |                              24 |
| upper_fence |                              62 |
| lower_fence |                             -34 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/NEGmirror/images/sample-heatmap_all-frq_adj-x-adv_thr0-001p.35f.pkl.png`

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

| `adj_form_lower` |   `SUM` | incredibly | however | wildly | also | apparently | scientifically | critically |
|:-----------------|--------:|-----------:|--------:|-------:|-----:|-----------:|---------------:|-----------:|
| `SUM`            | 285,435 |        166 |     103 |    103 |  101 |         71 |             40 |         34 |
| unique           |     452 |          1 |       0 |      0 |    0 |          0 |              0 |          0 |
| confident        |     416 |          0 |       0 |      0 |    0 |          0 |              0 |          0 |
| personal         |     329 |          1 |       1 |      0 |    0 |          0 |              0 |          0 |
| frightening      |     326 |          0 |       0 |      0 |    0 |          0 |              0 |          0 |
| violent          |     225 |          1 |       0 |      0 |    0 |          0 |              0 |          0 |
| pleasing         |     189 |          0 |       0 |      0 |    0 |          0 |              0 |          0 |
| apt              |     171 |          0 |       0 |      0 |    0 |          0 |              0 |          0 |

## _ALL_ (`NEGmirror` and non-`NEGmirror`) Frequencies Overview

### Descriptive Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for stats_all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADV-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.262

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% | max | total | var_coeff | range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|----:|------:|----------:|------:|---------:|------------:|------------:|---------------:|---------------:|
| momentarily      | 3,894 |    1 |   3 |   0 |   0 |   0 |   0 | 128 | 2,065 |         6 |   128 |        0 |           0 |           0 |              1 |              1 |
| democratically   | 3,894 |    0 |   5 |   0 |   0 |   0 |   0 | 286 |   948 |        21 |   286 |        0 |           0 |           0 |              1 |              1 |
| someplace        | 3,894 |    0 |   4 |   0 |   0 |   0 |   0 | 127 | 1,405 |        11 |   127 |        0 |           0 |           0 |              1 |              1 |
| dynamically      | 3,894 |    0 |   2 |   0 |   0 |   0 |   0 |  62 | 1,086 |         7 |    62 |        0 |           0 |           0 |              1 |              1 |
| jaw-droppingly   | 3,894 |    0 |   4 |   0 |   0 |   0 |   0 | 160 | 1,175 |        12 |   160 |        0 |           0 |           0 |              1 |              1 |
| monstrously      | 3,894 |    1 |   4 |   0 |   0 |   0 |   0 | 156 | 1,983 |         8 |   156 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across `adv_form_lower`s |
|:------------|--------------------------------:|
| count       |                           3,894 |
| mean        |                          21,388 |
| std         |                          91,460 |
| min         |                             870 |
| 25%         |                           1,637 |
| 50%         |                           3,466 |
| 75%         |                          10,673 |
| max         |                       2,210,387 |
| total       |                      83,284,343 |
| var_coeff   |                               4 |
| range       |                       2,209,517 |
| IQ_range    |                           9,036 |
| upper_fence |                          24,227 |
| lower_fence |                         -11,917 |

### Descriptive Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for stats_all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/RBXadj/descriptive_stats/ADJ-stats_all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.428

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean |   std | min | 25% | 50% | 75% |    max |   total | var_coeff |  range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|------:|----:|----:|----:|----:|-------:|--------:|----------:|-------:|---------:|------------:|------------:|---------------:|---------------:|
| prohibitive      | 1,005 |    2 |    13 |   0 |   0 |   0 |   0 |    215 |   2,259 |         6 |    215 |        0 |           0 |           0 |              1 |              1 |
| horrifying       | 1,005 |    9 |    82 |   0 |   0 |   0 |   1 |  1,824 |   8,917 |         9 |  1,824 |        1 |           2 |          -2 |              2 |              1 |
| renowned         | 1,005 |    3 |    58 |   0 |   0 |   0 |   0 |  1,693 |   3,318 |        18 |  1,693 |        0 |           0 |           0 |              1 |              1 |
| dangerous        | 1,005 |  291 | 2,923 |   0 |   0 |   3 |  15 | 60,599 | 292,335 |        10 | 60,599 |       15 |          38 |         -22 |              6 |              2 |
| foreign          | 1,005 |   18 |   147 |   0 |   0 |   0 |   1 |  3,085 |  17,887 |         8 |  3,085 |        1 |           2 |          -2 |              2 |              1 |
| nerve-racking    | 1,005 |    1 |    12 |   0 |   0 |   0 |   0 |    215 |   1,430 |         9 |    215 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across `adj_form_lower`s |
|:------------|--------------------------------:|
| count       |                           1,005 |
| mean        |                          82,870 |
| std         |                         581,924 |
| min         |                             868 |
| 25%         |                           1,705 |
| 50%         |                           4,049 |
| 75%         |                          15,767 |
| max         |                       9,913,432 |
| total       |                      83,284,343 |
| var_coeff   |                               7 |
| range       |                       9,912,564 |
| IQ_range    |                          14,062 |
| upper_fence |                          36,860 |
| lower_fence |                         -19,388 |

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

| `adj_form_lower` |      `SUM` |      less | politically | pleasantly | noticeably | chronically | disproportionately |
|:-----------------|-----------:|----------:|------------:|-----------:|-----------:|------------:|-------------------:|
| `SUM`            | 83,284,343 | 1,256,870 |     131,810 |     23,351 |     18,064 |      14,999 |             11,541 |
| sad              |    109,543 |       390 |           1 |          4 |          8 |          11 |                  2 |
| certain          |    104,145 |     6,039 |           3 |          0 |          0 |           0 |                  0 |
| influential      |     99,566 |       976 |       1,288 |          0 |          1 |           0 |                 52 |
| thin             |     68,395 |        57 |           2 |         10 |         63 |           5 |                  2 |
| viable           |     43,007 |       642 |         745 |          0 |          0 |           0 |                  0 |
| underway         |     41,641 |         1 |           0 |          0 |          4 |           0 |                  0 |

👀 sanity dimension checks

|            dataframe | # rows | # columns |
|---------------------:|-------:|----------:|
|     only `NEGmirr`or |   3573 |       877 |
|                  ALL |   3895 |      1006 |
| adjusted `NEGmirror` |   3895 |      1006 |

## Words with 0 tokens in the `NEGmirror` results

### Adjectives

| `adj_form_lower` | SUM_NEGmirror |  `SUM` |
|:-----------------|--------------:|-------:|
| fewer            |             0 | 47,307 |
| ongoing          |             0 | 12,939 |
| daily            |             0 | 11,213 |
| defunct          |             0 |  9,510 |
| latest           |             0 |  7,883 |
| highest          |             0 |  7,246 |
| softer           |             0 |  6,236 |
| cost             |             0 |  5,926 |
| residential      |             0 |  5,720 |
| adjacent         |             0 |  5,216 |
| inconceivable    |             0 |  4,970 |
| shiite           |             0 |  4,656 |
| narrower         |             0 |  4,485 |
| earlier          |             0 |  4,451 |
| untapped         |             0 |  4,406 |
| rudimentary      |             0 |  4,367 |
| breathable       |             0 |  4,366 |
| unexplored       |             0 |  4,300 |
| sunni            |             0 |  4,067 |
| overall          |             0 |  4,054 |
| underserved      |             0 |  3,625 |
| unused           |             0 |  3,576 |
| steeper          |             0 |  3,269 |
| unresolved       |             0 |  3,246 |
| stricter         |             0 |  3,244 |
| unpublished      |             0 |  3,163 |
| evolving         |             0 |  3,141 |
| bureaucratic     |             0 |  3,127 |
| unfinished       |             0 |  2,969 |
| trickier         |             0 |  2,917 |
| underdeveloped   |             0 |  2,914 |
| calmer           |             0 |  2,900 |
| themed           |             0 |  2,895 |
| quality          |             0 |  2,883 |
| untested         |             0 |  2,856 |
| secluded         |             0 |  2,830 |
| unbeaten         |             0 |  2,805 |
| imperceptible    |             0 |  2,770 |
| inseparable      |             0 |  2,694 |
| underrepresented |             0 |  2,688 |
| undisclosed      |             0 |  2,666 |
| milder           |             0 |  2,659 |
| finest           |             0 |  2,641 |
| former           |             0 |  2,631 |
| later            |             0 |  2,627 |
| hindu            |             0 |  2,565 |
| drab             |             0 |  2,548 |
| consecutive      |             0 |  2,443 |
| opportunistic    |             0 |  2,430 |
| indirect         |             0 |  2,423 |
| protestant       |             0 |  2,422 |
| unrecognized     |             0 |  2,403 |
| unanswered       |             0 |  2,402 |
| developed        |             0 |  2,388 |
| priced           |             0 |  2,372 |
| future           |             0 |  2,331 |
| unreported       |             0 |  2,292 |
| moot             |             0 |  2,289 |
| intent           |             0 |  2,284 |
| uphill           |             0 |  2,258 |
| unaccounted      |             0 |  2,256 |
| unmatched        |             0 |  2,227 |
| darn             |             0 |  2,227 |
| never-ending     |             0 |  2,223 |
| earliest         |             0 |  2,199 |
| underfunded      |             0 |  2,185 |
| outdoor          |             0 |  2,145 |
| non-stop         |             0 |  2,128 |
| individualized   |             0 |  2,123 |
| foggy            |             0 |  2,113 |
| unnamed          |             0 |  2,110 |
| stretchy         |             0 |  2,108 |
| unparalleled     |             0 |  2,064 |
| acoustic         |             0 |  2,047 |
| slimmer          |             0 |  2,045 |
| concentrated     |             0 |  2,035 |
| customisable     |             0 |  2,027 |
| petite           |             0 |  2,024 |
| multiple         |             0 |  2,023 |
| annual           |             0 |  2,008 |
| monthly          |             0 |  2,001 |
| wealthier        |             0 |  1,994 |
| reusable         |             0 |  1,974 |
| underpaid        |             0 |  1,952 |
| unexplained      |             0 |  1,950 |
| knit             |             0 |  1,942 |
| unharmed         |             0 |  1,932 |
| unintentional    |             0 |  1,929 |
| administrative   |             0 |  1,914 |
| northerly        |             0 |  1,890 |
| nil              |             0 |  1,885 |
| unresponsive     |             0 |  1,878 |
| editable         |             0 |  1,869 |
| stormy           |             0 |  1,866 |
| firmer           |             0 |  1,859 |
| fictitious       |             0 |  1,816 |
| spotty           |             0 |  1,794 |
| gothic           |             0 |  1,784 |
| greatest         |             0 |  1,781 |
| established      |             0 |  1,777 |
| conflicting      |             0 |  1,775 |
| sizeable         |             0 |  1,759 |
| tastier          |             0 |  1,749 |
| veteran          |             0 |  1,747 |
| prospective      |             0 |  1,742 |
| initial          |             0 |  1,734 |
| self-reliant     |             0 |  1,734 |
| male-dominated   |             0 |  1,728 |
| proportionate    |             0 |  1,726 |
| breathless       |             0 |  1,715 |
| unprotected      |             0 |  1,711 |
| looser           |             0 |  1,666 |
| nominal          |             0 |  1,656 |
| industrialized   |             0 |  1,649 |
| affable          |             0 |  1,629 |
| inexcusable      |             0 |  1,627 |
| returnable       |             0 |  1,612 |
| peripheral       |             0 |  1,609 |
| unobtrusive      |             0 |  1,593 |
| indecisive       |             0 |  1,570 |
| electrical       |             0 |  1,567 |
| top-notch        |             0 |  1,566 |
| punishable       |             0 |  1,560 |
| freer            |             0 |  1,544 |
| luxury           |             0 |  1,533 |
| rectangular      |             0 |  1,532 |
| medium           |             0 |  1,508 |
| unnoticeable     |             0 |  1,497 |
| marginalised     |             0 |  1,476 |
| south            |             0 |  1,467 |
| nascent          |             0 |  1,467 |
| qualitative      |             0 |  1,464 |
| african-american |             0 |  1,460 |
| insolvent        |             0 |  1,458 |
| rougher          |             0 |  1,442 |
| unsupported      |             0 |  1,436 |
| expired          |             0 |  1,429 |
| southerly        |             0 |  1,426 |
| fucking          |             0 |  1,419 |
| woven            |             0 |  1,418 |
| testy            |             0 |  1,416 |
| uncharted        |             0 |  1,416 |
| closest          |             0 |  1,415 |
| gentler          |             0 |  1,409 |
| verbatim         |             0 |  1,386 |
| concerted        |             0 |  1,384 |
| deadlier         |             0 |  1,373 |
| lead             |             0 |  1,373 |
| clingy           |             0 |  1,371 |
| toothless        |             0 |  1,368 |
| gooey            |             0 |  1,368 |
| reproducible     |             0 |  1,367 |
| unending         |             0 |  1,367 |
| personalised     |             0 |  1,366 |
| unfulfilled      |             0 |  1,366 |
| uninterrupted    |             0 |  1,365 |
| par              |             0 |  1,354 |
| giant            |             0 |  1,351 |
| indescribable    |             0 |  1,349 |
| angrier          |             0 |  1,348 |
| fifth            |             0 |  1,337 |
| run              |             0 |  1,333 |
| countless        |             0 |  1,332 |
| biggest          |             0 |  1,326 |
| unsolved         |             0 |  1,318 |
| leaner           |             0 |  1,316 |
| unintended       |             0 |  1,314 |
| recommendable    |             0 |  1,312 |
| undetected       |             0 |  1,312 |
| patchy           |             0 |  1,302 |
| elliptical       |             0 |  1,302 |
| hyperbole        |             0 |  1,298 |
| chopped          |             0 |  1,293 |
| away             |             0 |  1,291 |
| unspoken         |             0 |  1,288 |
| cartoony         |             0 |  1,285 |
| inner            |             0 |  1,272 |
| mere             |             0 |  1,270 |
| payable          |             0 |  1,264 |
| inexhaustible    |             0 |  1,263 |
| fiscal           |             0 |  1,258 |
| good-natured     |             0 |  1,254 |
| amorphous        |             0 |  1,252 |
| rambunctious     |             0 |  1,245 |
| inaudible        |             0 |  1,245 |
| moribund         |             0 |  1,241 |
| unheralded       |             0 |  1,232 |
| outpacing        |             0 |  1,231 |
| underused        |             0 |  1,226 |
| unconvinced      |             0 |  1,221 |
| air-conditioned  |             0 |  1,215 |
| flavourful       |             0 |  1,215 |
| unconscionable   |             0 |  1,203 |
| hued             |             0 |  1,201 |
| unsubstantiated  |             0 |  1,199 |
| ailing           |             0 |  1,198 |
| libelous         |             0 |  1,198 |
| sassy            |             0 |  1,186 |
| north            |             0 |  1,185 |
| nonpartisan      |             0 |  1,173 |
| front            |             0 |  1,172 |
| statistical      |             0 |  1,171 |
| solar            |             0 |  1,171 |
| known            |             0 |  1,169 |
| marrow           |             0 |  1,168 |
| advantaged       |             0 |  1,165 |
| wavy             |             0 |  1,150 |
| armored          |             0 |  1,147 |
| moreso           |             0 |  1,146 |
| unassailable     |             0 |  1,137 |
| impregnable      |             0 |  1,135 |
| situational      |             0 |  1,132 |
| protracted       |             0 |  1,130 |
| uncalled         |             0 |  1,129 |
| year-round       |             0 |  1,119 |
| wetter           |             0 |  1,118 |
| state-owned      |             0 |  1,118 |
| pluralistic      |             0 |  1,117 |
| baroque          |             0 |  1,116 |
| pricier          |             0 |  1,115 |
| strongest        |             0 |  1,113 |
| fallible         |             0 |  1,113 |
| resident         |             0 |  1,111 |
| unconfirmed      |             0 |  1,110 |
| upmarket         |             0 |  1,107 |
| undetermined     |             0 |  1,101 |
| ill-equipped     |             0 |  1,101 |
| unfocused        |             0 |  1,100 |
| caucasian        |             0 |  1,097 |
| unbroken         |             0 |  1,093 |
| sayin            |             0 |  1,093 |
| shrinking        |             0 |  1,089 |
| untold           |             0 |  1,086 |
| experiential     |             0 |  1,086 |
| sandy            |             0 |  1,085 |
| undisturbed      |             0 |  1,084 |
| luckier          |             0 |  1,078 |
| unenforceable    |             0 |  1,076 |
| non              |             0 |  1,073 |
| indie            |             0 |  1,072 |
| unflappable      |             0 |  1,072 |
| upward           |             0 |  1,068 |
| angled           |             0 |  1,068 |
| deployable       |             0 |  1,066 |
| null             |             0 |  1,063 |
| washable         |             0 |  1,060 |
| sixth            |             0 |  1,053 |
| blond            |             0 |  1,052 |
| balmy            |             0 |  1,052 |
| contextual       |             0 |  1,047 |
| inconsiderable   |             0 |  1,043 |
| flatter          |             0 |  1,042 |
| immigrant        |             0 |  1,040 |
| dental           |             0 |  1,037 |
| unsteady         |             0 |  1,037 |
| unappreciated    |             0 |  1,033 |
| overcooked       |             0 |  1,029 |
| mass             |             0 |  1,027 |
| groggy           |             0 |  1,024 |
| disheveled       |             0 |  1,016 |
| triple           |             0 |  1,013 |
| full-time        |             0 |  1,010 |
| downward         |             0 |  1,010 |
| tantamount       |             0 |  1,009 |
| frazzled         |             0 |  1,004 |
| coachable        |             0 |    998 |
| beatable         |             0 |    996 |
| unrecognisable   |             0 |    989 |
| afloat           |             0 |    988 |
| menial           |             0 |    988 |
| trusted          |             0 |    988 |
| real-time        |             0 |    987 |
| architectural    |             0 |    986 |
| leeway           |             0 |    983 |
| unskilled        |             0 |    980 |
| upper            |             0 |    978 |
| colorless        |             0 |    974 |
| uncooperative    |             0 |    973 |
| microscopic      |             0 |    972 |
| genial           |             0 |    970 |
| collegial        |             0 |    969 |
| nationwide       |             0 |    967 |
| sculptural       |             0 |    964 |
| fatter           |             0 |    964 |
| worldwide        |             0 |    963 |
| asymmetrical     |             0 |    962 |
| low-risk         |             0 |    959 |
| inebriated       |             0 |    957 |
| inflated         |             0 |    955 |
| asymptomatic     |             0 |    952 |
| skewed           |             0 |    950 |
| tangential       |             0 |    947 |
| under-reported   |             0 |    944 |
| unannounced      |             0 |    942 |
| illiquid         |             0 |    941 |
| hybrid           |             0 |    941 |
| novice           |             0 |    938 |
| jobless          |             0 |    934 |
| unorganized      |             0 |    932 |
| prevailing       |             0 |    931 |
| seminal          |             0 |    930 |
| compelled        |             0 |    928 |
| afoot            |             0 |    925 |
| androgynous      |             0 |    922 |
| homegrown        |             0 |    921 |
| apocryphal       |             0 |    918 |
| non-traditional  |             0 |    916 |
| subtler          |             0 |    914 |
| gluten-free      |             0 |    910 |
| substandard      |             0 |    907 |
| personalized     |             0 |    898 |
| so-called        |             0 |    897 |
| non-toxic        |             0 |    890 |
| expandable       |             0 |    885 |
| subconscious     |             0 |    881 |
| simplest         |             0 |    880 |
| argumentative    |             0 |    880 |
| famed            |             0 |    879 |
| directional      |             0 |    874 |
| drowsy           |             0 |    873 |
| intermittent     |             0 |    872 |
| untrained        |             0 |    872 |

### Adverbs

| `adv_form_lower` | SUM_NEGmirror |  `SUM` |
|:-----------------|--------------:|-------:|
| formerly         |             0 | 16,931 |
| least            |             0 | 14,530 |
| admittedly       |             0 | 13,066 |
| cautiously       |             0 | 11,204 |
| worst            |             0 |  9,594 |
| lightly          |             0 |  7,913 |
| presumably       |             0 |  7,190 |
| nicely           |             0 |  5,826 |
| exponentially    |             0 |  5,208 |
| persistently     |             0 |  5,163 |
| approximately    |             0 |  4,617 |
| perilously       |             0 |  4,597 |
| sorely           |             0 |  4,549 |
| earlier          |             0 |  4,547 |
| finely           |             0 |  4,273 |
| uncommonly       |             0 |  4,220 |
| slowly           |             0 |  4,212 |
| hitherto         |             0 |  4,185 |
| insufficiently   |             0 |  4,167 |
| preferably       |             0 |  4,111 |
| elegantly        |             0 |  3,737 |
| alternately      |             0 |  3,589 |
| instead          |             0 |  3,534 |
| unimaginably     |             0 |  3,423 |
| inexplicably     |             0 |  3,297 |
| carefully        |             0 |  3,190 |
| gorgeously       |             0 |  3,121 |
| dang             |             0 |  3,026 |
| third            |             0 |  2,834 |
| decently         |             0 |  2,667 |
| oftentimes       |             0 |  2,620 |
| chiefly          |             0 |  2,561 |
| collectively     |             0 |  2,491 |
| rightfully       |             0 |  2,474 |
| gradually        |             0 |  2,462 |
| admirably        |             0 |  2,429 |
| counter          |             0 |  2,428 |
| immeasurably     |             0 |  2,404 |
| electrically     |             0 |  2,398 |
| dead             |             0 |  2,390 |
| briefly          |             0 |  2,346 |
| lot              |             0 |  2,328 |
| unspeakably      |             0 |  2,320 |
| consequently     |             0 |  2,309 |
| delicately       |             0 |  2,289 |
| disarmingly      |             0 |  2,264 |
| infamously       |             0 |  2,241 |
| yearly           |             0 |  2,218 |
| computationally  |             0 |  2,194 |
| upwardly         |             0 |  2,184 |
| appallingly      |             0 |  2,093 |
| daily            |             0 |  2,074 |
| nowadays         |             0 |  2,070 |
| meticulously     |             0 |  2,044 |
| heartbreakingly  |             0 |  2,040 |
| unseasonably     |             0 |  2,039 |
| respectfully     |             0 |  2,026 |
| plenty           |             0 |  2,005 |
| chillingly       |             0 |  2,000 |
| incomparably     |             0 |  1,997 |
| geologically     |             0 |  1,995 |
| scarily          |             0 |  1,954 |
| indescribably    |             0 |  1,884 |
| vanishingly      |             0 |  1,880 |
| purportedly      |             0 |  1,854 |
| mercifully       |             0 |  1,832 |
| scrupulously     |             0 |  1,768 |
| defensively      |             0 |  1,733 |
| semi             |             0 |  1,712 |
| thinly           |             0 |  1,705 |
| thereby          |             0 |  1,705 |
| everywhere       |             0 |  1,616 |
| spotlessly       |             0 |  1,614 |
| fewer            |             0 |  1,596 |
| deep             |             0 |  1,559 |
| dazzlingly       |             0 |  1,554 |
| soooooo          |             0 |  1,517 |
| intermittently   |             0 |  1,505 |
| vibrantly        |             0 |  1,498 |
| next             |             0 |  1,495 |
| kindly           |             0 |  1,486 |
| freshly          |             0 |  1,480 |
| mightily         |             0 |  1,443 |
| someplace        |             0 |  1,405 |
| obsessively      |             0 |  1,403 |
| fascinatingly    |             0 |  1,358 |
| doubtless        |             0 |  1,319 |
| enduringly       |             0 |  1,309 |
| metabolically    |             0 |  1,303 |
| everyday         |             0 |  1,292 |
| repeatedly       |             0 |  1,289 |
| chock            |             0 |  1,288 |
| sparsely         |             0 |  1,281 |
| jointly          |             0 |  1,274 |
| worldwide        |             0 |  1,263 |
| arbitrarily      |             0 |  1,250 |
| faster           |             0 |  1,185 |
| pearly           |             0 |  1,165 |
| softly           |             0 |  1,142 |
| seductively      |             0 |  1,136 |
| virulently       |             0 |  1,125 |
| privately        |             0 |  1,100 |
| amply            |             0 |  1,096 |
| tonally          |             0 |  1,077 |
| fortunately      |             0 |  1,071 |
| infinitesimally  |             0 |  1,069 |
| precariously     |             0 |  1,061 |
| flatly           |             0 |  1,059 |
| ergonomically    |             0 |  1,057 |
| dizzyingly       |             0 |  1,047 |
| timelessly       |             0 |  1,033 |
| unflinchingly    |             0 |  1,001 |
| unnervingly      |             0 |    999 |
| differently      |             0 |    985 |
| savagely         |             0 |    985 |
| legendarily      |             0 |    981 |
| unsurprisingly   |             0 |    980 |
| foremost         |             0 |    964 |
| incrementally    |             0 |    945 |
| stupendously     |             0 |    941 |
| unavoidably      |             0 |    940 |
| wondrously       |             0 |    939 |
| preposterously   |             0 |    934 |
| institutionally  |             0 |    931 |
| north            |             0 |    906 |
| absolute         |             0 |    898 |
| questionably     |             0 |    891 |
| touchingly       |             0 |    872 |
| second-most      |             0 |    869 |

## The Difference

| `adj_form_lower` | `SUM`    | very    | more    | ... | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:----|:------------|:-------------|:----------|
| `SUM`            | 82998908 | 9904571 | 9243662 | ... | 869         | 865          | 866       |
| many             | 2210082  | 21230   | 373     | ... | 0           | 0            | 0         |
| important        | 2184479  | 359506  | 294208  | ... | 105         | 9            | 0         |
| ...              | ...      | ...     | ...     | ... | ...         | ...          | ...       |
| contiguous       | 867      | 4       | 106     | ... | 0           | 0            | 0         |
| panicked         | 866      | 53      | 156     | ... | 0           | 0            | 0         |
| oversized        | 867      | 32      | 45      | ... | 0           | 0            | 0         |

### Descriptive _Complement_ Statistics for `adj_form_lower` by `adv_form_lower`

- Saving `adv_form_lower` descriptive statististics for stats_diff_NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/NEGmirror/complement/descriptive_stats/ADV-stats_diff_NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.879

Sample `adv_form_lower` Stats

| `adv_form_lower` | count | mean | std | min | 25% | 50% | 75% |    max |   total | var_coeff |  range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|----:|----:|----:|----:|----:|-------:|--------:|----------:|-------:|---------:|------------:|------------:|---------------:|---------------:|
| originally       | 3,894 |    2 |  13 |   0 |   0 |   0 |   1 |    552 |   6,803 |         8 |    552 |        1 |           2 |          -2 |              1 |              1 |
| chock            | 3,894 |    0 |  21 |   0 |   0 |   0 |   0 |  1,288 |   1,288 |        62 |  1,288 |        0 |           0 |           0 |              1 |              1 |
| insanely         | 3,894 |    7 |  48 |   0 |   0 |   0 |   2 |  1,207 |  27,350 |         7 |  1,207 |        2 |           5 |          -3 |              2 |              1 |
| positively       | 3,894 |    3 |  16 |   0 |   0 |   1 |   2 |    733 |  13,268 |         5 |    733 |        2 |           5 |          -3 |              2 |              2 |
| once             | 3,894 |   26 | 279 |   0 |   1 |   4 |  13 | 16,346 | 101,274 |        11 | 16,346 |       12 |          31 |         -17 |              6 |              3 |
| roughly          | 3,894 |    5 | 114 |   0 |   0 |   0 |   0 |  5,401 |  18,827 |        24 |  5,401 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across `adv_form_lower`s |
|:------------|--------------------------------:|
| count       |                           3,894 |
| mean        |                          21,315 |
| std         |                          91,177 |
| min         |                             866 |
| 25%         |                           1,633 |
| 50%         |                           3,459 |
| 75%         |                          10,628 |
| max         |                       2,210,082 |
| total       |                      82,998,908 |
| var_coeff   |                               4 |
| range       |                       2,209,216 |
| IQ_range    |                           8,994 |
| upper_fence |                          24,119 |
| lower_fence |                         -11,858 |

### Descriptive _Complement_ Statistics for `adv_form_lower` by `adj_form_lower`

- Saving `adj_form_lower` descriptive statististics for stats_diff_NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+ as csv...
  - successfully saved as `/share/compling/projects/sanpi/results/freq_out/NEGmirror/complement/descriptive_stats/ADJ-stats_diff_NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.csv`
  - time elapsed: 00:00:00.773

Sample `adj_form_lower` Stats

| `adj_form_lower` | count | mean |    std | min | 25% | 50% | 75% |     max |   total | var_coeff |   range | IQ_range | upper_fence | lower_fence | plus1_geo_mean | plus1_har_mean |
|:-----------------|------:|-----:|-------:|----:|----:|----:|----:|--------:|--------:|----------:|--------:|---------:|------------:|------------:|---------------:|---------------:|
| hypothetical     | 1,005 |    3 |     22 |   0 |   0 |   0 |   0 |     481 |   2,985 |         8 |     481 |        0 |           0 |           0 |              1 |              1 |
| better           | 1,005 |  736 | 10,561 |   0 |   0 |   3 |  24 | 294,900 | 739,603 |        14 | 294,900 |       24 |          60 |         -36 |              8 |              2 |
| matte            | 1,005 |    1 |     11 |   0 |   0 |   0 |   0 |     272 |   1,350 |         8 |     272 |        0 |           0 |           0 |              1 |              1 |
| deceitful        | 1,005 |    1 |      7 |   0 |   0 |   0 |   0 |     134 |   1,130 |         6 |     134 |        0 |           0 |           0 |              1 |              1 |
| tender           | 1,005 |   23 |    208 |   0 |   0 |   0 |   2 |   4,617 |  23,451 |         9 |   4,617 |        2 |           5 |          -3 |              2 |              1 |
| trans            | 1,005 |    1 |     11 |   0 |   0 |   0 |   0 |     223 |   1,103 |        10 |     223 |        0 |           0 |           0 |              1 |              1 |

|             | Summed Across `adj_form_lower`s |
|:------------|--------------------------------:|
| count       |                           1,005 |
| mean        |                          82,586 |
| std         |                         579,733 |
| min         |                             864 |
| 25%         |                           1,704 |
| 50%         |                           4,024 |
| 75%         |                          15,765 |
| max         |                       9,904,571 |
| total       |                      82,998,908 |
| var_coeff   |                               7 |
| range       |                       9,903,707 |
| IQ_range    |                          14,061 |
| upper_fence |                          36,856 |
| lower_fence |                         -19,388 |

Heatmap saved to:

  `/share/compling/projects/sanpi/results/freq_out/NEGmirror/complement/images/sample-heatmap_diff_NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.png`

✅ complement frequency table saved as `/share/compling/projects/sanpi/results/freq_out/NEGmirror/complement/diff_NEGmirror-all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz`

### Adverb stats for complement

|       | non-`NEGmirror` ADJ totals |
|:------|---------------------------:|
| count |                   3,895.00 |
| mean  |                  42,618.18 |
| std   |               1,332,679.27 |
| min   |                     866.00 |
| 25%   |                   1,633.50 |
| 50%   |                   3,459.00 |
| 75%   |                  10,651.00 |
| max   |              82,998,908.00 |

### Adverb stats for complement

|       | non-`NEGmirror` ADV totals |
|:------|---------------------------:|
| count |                   1,006.00 |
| mean  |                 165,007.77 |
| std   |               2,677,660.85 |
| min   |                     864.00 |
| 25%   |                   1,704.25 |
| 50%   |                   4,035.00 |
| 75%   |                  15,771.00 |
| max   |              82,998,908.00 |

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

### `NEGmirror`

| `adj_form_lower` | `SUM`  | very | more  | most | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:-------|:-----|:------|:-----|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 285435 | 8861 | 77335 | 1300 | ... | 1            | 0           | 4            | 2         |
| many             | 305    | 7    | 0     | 0    | ... | 0            | 0           | 0            | 0         |
| important        | 14968  | 104  | 12396 | 61   | ... | 0            | 0           | 0            | 0         |
| good             | 8697   | 1572 | 12    | 0    | ... | 0            | 0           | 0            | 0         |
| ...              | ...    | ...  | ...   | ...  | ... | ...          | ...         | ...          | ...       |
| carnal           | 2      | 0    | 0     | 1    | ... | 0            | 0           | 0            | 0         |
| contiguous       | 4      | 0    | 0     | 0    | ... | 0            | 0           | 0            | 0         |
| panicked         | 5      | 1    | 3     | 0    | ... | 0            | 0           | 0            | 0         |
| oversized        | 3      | 0    | 0     | 0    | ... | 0            | 0           | 0            | 0         |

### _Complement_

| `adj_form_lower` | `SUM`    | very    | more    | most    | ... | emphatically | second-most | cosmetically | pointedly |
|:-----------------|:---------|:--------|:--------|:--------|:----|:-------------|:------------|:-------------|:----------|
| `SUM`            | 82998908 | 9904571 | 9243662 | 7567512 | ... | 871          | 869         | 865          | 866       |
| many             | 2210082  | 21230   | 373     | 140     | ... | 3            | 0           | 0            | 0         |
| important        | 2184479  | 359506  | 294208  | 748472  | ... | 2            | 105         | 9            | 0         |
| good             | 2021783  | 505927  | 18890   | 5207    | ... | 6            | 0           | 7            | 0         |
| ...              | ...      | ...     | ...     | ...     | ... | ...          | ...         | ...          | ...       |
| carnal           | 870      | 34      | 150     | 61      | ... | 0            | 0           | 0            | 0         |
| contiguous       | 867      | 4       | 106     | 8       | ... | 0            | 0           | 0            | 0         |
| panicked         | 866      | 53      | 156     | 31      | ... | 0            | 0           | 0            | 0         |
| oversized        | 867      | 32      | 45      | 16      | ... | 0            | 0           | 0            | 0         |

## Juxtaposed Sample (√ frequencies)

| `adj_form_lower`        | particularly |  ever |  that | remotely | fully | necessarily | exactly | absolutely | extremely | slightly | utterly | definitely | fairly | somewhat |
|:------------------------|-------------:|------:|------:|---------:|------:|------------:|--------:|-----------:|----------:|---------:|--------:|-----------:|-------:|---------:|
| comfortable             |        26.12 |  7.94 | 25.90 |     7.75 | 25.63 |       13.15 |   14.39 |      21.31 |     70.19 |     4.90 |   10.49 |      13.19 |  36.89 |    18.84 |
| comfortable-`NEGmirror` |         6.63 |  3.46 |  4.80 |     1.00 |  7.55 |        0.00 |    2.00 |       1.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| famous                  |        25.87 | 14.32 | 14.32 |     5.66 |  1.00 |        6.63 |   11.40 |       4.00 |     22.89 |     7.21 |    3.46 |       3.61 |  14.56 |    18.30 |
| famous-`NEGmirror`      |         3.00 |  1.00 |  1.41 |     0.00 |  0.00 |        0.00 |    1.73 |       0.00 |      1.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| flavorful               |         7.55 |  0.00 |  4.12 |     1.00 |  1.41 |        0.00 |    0.00 |       2.45 |     15.17 |     0.00 |    1.00 |       2.00 |   2.83 |     1.00 |
| flavorful-`NEGmirror`   |         1.41 |  0.00 |  0.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| fond                    |        65.83 |  4.58 | 17.80 |     2.00 |  1.00 |        5.10 |    9.33 |       3.16 |     23.83 |     2.45 |    1.41 |       3.74 |   5.10 |     6.32 |
| fond-`NEGmirror`        |        10.54 |  0.00 |  4.90 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| forgiving               |         6.40 |  6.08 |  5.83 |     1.00 |  1.73 |        1.41 |    2.24 |       1.73 |     11.49 |     1.73 |    2.00 |       1.00 |  10.95 |     8.37 |
| forgiving-`NEGmirror`   |         1.41 |  0.00 |  1.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| inept                   |         8.25 |  1.00 |  4.47 |     0.00 |  1.00 |        0.00 |    1.00 |       4.24 |      4.36 |     4.80 |    9.59 |       0.00 |   5.83 |     7.68 |
| inept-`NEGmirror`       |         0.00 |  0.00 |  0.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| lopsided                |         4.36 |  0.00 |  3.87 |     0.00 |  0.00 |        1.00 |    0.00 |       1.00 |      7.55 |     9.38 |    1.00 |       2.00 |   5.10 |     9.00 |
| lopsided-`NEGmirror`    |         0.00 |  0.00 |  1.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| manageable              |         1.00 |  0.00 |  2.65 |     3.74 |  7.14 |        1.00 |    0.00 |       4.80 |      6.93 |     2.00 |    1.00 |       8.49 |   9.90 |     9.85 |
| manageable-`NEGmirror`  |         0.00 |  0.00 |  0.00 |     1.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| muslim                  |         5.39 |  6.00 |  0.00 |     0.00 |  4.90 |        3.46 |    0.00 |       1.00 |      1.00 |     1.41 |    0.00 |       2.24 |   1.00 |     0.00 |
| muslim-`NEGmirror`      |         1.00 |  0.00 |  0.00 |     0.00 |  0.00 |        1.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| older                   |        10.34 |  7.87 |  2.00 |     0.00 |  0.00 |        3.32 |    1.00 |       0.00 |      4.24 |    66.23 |    1.00 |       9.49 |   4.00 |    25.88 |
| older-`NEGmirror`       |         0.00 |  0.00 |  0.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| preferable              |         2.83 |  1.41 |  2.45 |     1.00 |  0.00 |        3.46 |    1.73 |       2.45 |      3.00 |     4.69 |    0.00 |      12.45 |   2.45 |     2.65 |
| preferable-`NEGmirror`  |         0.00 |  0.00 |  0.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| relatable               |         5.66 |  1.41 |  2.83 |     2.24 |  3.87 |        2.00 |    3.46 |       3.16 |     13.67 |     1.00 |    6.48 |       4.80 |   3.87 |     7.87 |
| relatable-`NEGmirror`   |         1.00 |  0.00 |  0.00 |     1.00 |  1.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |
| sensual                 |         4.12 |  2.83 |  0.00 |     1.73 |  2.24 |        2.00 |    0.00 |       3.32 |     11.49 |     3.46 |    2.83 |       2.00 |   1.73 |     3.32 |
| sensual-`NEGmirror`     |         1.00 |  0.00 |  0.00 |     0.00 |  0.00 |        0.00 |    0.00 |       0.00 |      0.00 |     0.00 |    0.00 |       0.00 |   0.00 |     0.00 |

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

### Top (15 x 10) collocations in `NEGmirror` frequencies (+ `SUM`)

| `adj_form_lower` |   `SUM` |   more |    too |     as |     so | really | particularly |  very | quite |  less |  ever |
|:-----------------|--------:|-------:|-------:|-------:|-------:|-------:|-------------:|------:|------:|------:|------:|
| `SUM`            | 285,435 | 77,335 | 46,567 | 30,872 | 24,760 | 11,124 |        9,079 | 8,861 | 6,203 | 4,718 | 4,613 |
| important        |  14,968 | 12,396 |     70 |  1,045 |    532 |    114 |           42 |   104 |     3 |   272 |     3 |
| late             |  11,139 |      0 | 11,087 |      5 |      5 |      1 |            0 |     3 |     0 |     0 |    21 |
| good             |   8,697 |     12 |    519 |  3,471 |    432 |    301 |          392 | 1,572 |   125 |     5 |   300 |
| sure             |   5,814 |     94 |    539 |     22 |    170 |    912 |            4 |    29 | 2,967 |     9 |    30 |
| wrong            |   5,329 |    224 |     14 |     13 |     99 |    529 |          212 |    12 |     3 |     3 |   102 |
| early            |   5,218 |      0 |  5,200 |      1 |      4 |      0 |            1 |     1 |     0 |     0 |     1 |
| easy             |   5,090 |     97 |    121 |    889 |  2,636 |     55 |           98 |   100 |    15 |     4 |   368 |
| happy            |   3,449 |     97 |  1,185 |    183 |    830 |    238 |           74 |   151 |    78 |     9 |    48 |
| bad              |   3,444 |      4 |    460 |  1,326 |    362 |    228 |           92 |    53 |     4 |     4 |    16 |
| exciting         |   2,904 |  1,438 |    431 |    260 |    137 |    118 |          114 |    97 |     0 |    31 |     2 |
| simple           |   2,813 |    180 |     30 |  1,089 |    683 |     18 |            7 |    28 |     7 |     6 |   207 |
| close            |   2,579 |     10 |     96 |    263 |    390 |    173 |          138 |   129 |    11 |     1 |    13 |
| old              |   2,534 |      1 |  2,365 |     58 |     30 |      4 |            7 |    18 |     3 |     0 |     3 |
| clear            |   2,454 |    460 |     57 |    146 |    152 |    194 |           26 |   147 |   427 |    17 |    21 |
| serious          |   2,126 |    647 |    781 |    144 |     83 |    106 |           24 |    82 |     2 |    32 |    11 |

### Top (15 x 10) collocations in DIFF frequencies (+ `SUM`)

| `adj_form_lower` |      `SUM` |      very |      more |      most |        so |       not |        as |       too |    really |      much |    pretty |
|:-----------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| `SUM`            | 82,998,908 | 9,904,571 | 9,243,662 | 7,567,512 | 5,711,204 | 4,414,394 | 3,679,042 | 3,510,873 | 2,084,933 | 1,984,505 | 1,621,622 |
| many             |  2,210,082 |    21,230 |       373 |       140 | 1,191,767 |    58,436 |   434,568 |   450,081 |       518 |       201 |        54 |
| important        |  2,184,479 |   359,506 |   294,208 |   748,472 |   104,977 |    17,342 |   101,778 |    12,809 |    72,061 |     1,818 |     6,594 |
| good             |  2,021,783 |   505,927 |    18,890 |     5,207 |   152,764 |    96,099 |   231,877 |    59,164 |   259,980 |    14,149 |   243,680 |
| much             |  1,775,552 |    42,329 |       102 |        22 |   614,433 |    66,405 |   355,242 |   582,439 |     3,022 |       284 |    57,881 |
| likely           |  1,047,568 |    35,805 |   498,069 |   192,580 |       820 |    46,854 |    31,787 |     1,191 |       456 |       259 |     1,312 |
| more             |  1,027,402 |        69 |     2,278 |        90 |     2,943 |    17,639 |     2,849 |        52 |     4,509 |   355,204 |        13 |
| different        |    905,106 |   232,957 |    11,623 |     1,364 |    39,307 |     4,021 |     9,288 |     5,147 |     6,451 |    44,159 |     2,140 |
| available        |    861,908 |       403 |     9,707 |     1,384 |       487 |   132,343 |     1,875 |       275 |       534 |       977 |        32 |
| sure             |    838,252 |     4,662 |     2,230 |       315 |    35,506 |   467,185 |     3,878 |     8,175 |    19,213 |       341 |    84,358 |
| difficult        |    831,007 |   188,124 |   219,440 |    76,629 |    26,395 |    19,839 |    15,925 |    27,513 |    18,754 |       636 |     5,649 |
| popular          |    825,522 |    89,282 |    69,779 |   398,904 |    42,791 |     4,555 |    14,787 |     2,094 |     4,994 |     1,304 |     3,214 |
| easy             |    763,362 |   125,444 |     5,470 |     1,215 |    86,003 |    95,470 |    72,344 |    40,344 |    29,528 |       809 |    31,786 |
| better           |    739,603 |        93 |     1,749 |        66 |       869 |    13,534 |     1,985 |        30 |     1,751 |   294,900 |        16 |
| high             |    585,126 |   138,047 |     5,215 |    10,402 |    35,452 |     5,767 |    67,780 |    77,808 |    11,022 |       576 |    12,999 |
| common           |    555,534 |    45,718 |    85,584 |   272,784 |    15,119 |     7,175 |    11,351 |    10,425 |     1,528 |       915 |     7,186 |

## Totals

### Total Tokens per Frequency Group

|             |     totals |
|:------------|-----------:|
| ALL         | 83,284,343 |
| `NEGmirror` |    285,435 |
| DIFF        | 82,998,908 |

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

### Marginal Frequencies for `NEGmirror` Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                    73 |                   284 |
| std   |                   426 |                 3,169 |
| min   |                     0 |                     0 |
| 25%   |                     3 |                     2 |
| 50%   |                     8 |                     5 |
| 75%   |                    30 |                    19 |
| max   |                14,968 |                77,335 |

### Marginal Frequencies for DIFF Bigram Tokens

|       | individual adj totals | individual adv totals |
|:------|----------------------:|----------------------:|
| count |                 3,894 |                 1,005 |
| mean  |                21,315 |                82,586 |
| std   |                91,177 |               579,733 |
| min   |                   866 |                   864 |
| 25%   |                 1,633 |                 1,704 |
| 50%   |                 3,459 |                 4,024 |
| 75%   |                10,628 |                15,765 |
| max   |             2,210,082 |             9,904,571 |

#### Top 30 ADV totals comparison

| `adv_form_lower` | NEGmirror/ALL | DIFF/ALL | NEGmirror_RAW |     DIFF_RAW |
|:-----------------|--------------:|---------:|--------------:|-------------:|
| remotely         |          0.08 |     0.92 |      1,758.00 |    19,650.00 |
| inherently       |          0.05 |     0.95 |      2,814.00 |    48,788.00 |
| intrinsically    |          0.04 |     0.96 |        419.00 |     8,980.00 |
| ever             |          0.04 |     0.96 |      4,613.00 |   113,082.00 |
| this             |          0.03 |     0.97 |         28.00 |       864.00 |
| anywhere         |          0.03 |     0.97 |         36.00 |     1,115.00 |
| overtly          |          0.03 |     0.97 |        370.00 |    13,506.00 |
| knowingly        |          0.03 |     0.97 |         30.00 |     1,156.00 |
| majorly          |          0.02 |     0.98 |         48.00 |     1,943.00 |
| terribly         |          0.02 |     0.98 |      1,557.00 |    66,583.00 |
| else             |          0.02 |     0.98 |         72.00 |     3,360.00 |
| innately         |          0.02 |     0.98 |         63.00 |     3,527.00 |
| necessarily      |          0.02 |     0.98 |        936.00 |    53,145.00 |
| that             |          0.02 |     0.98 |      4,318.00 |   245,203.00 |
| substantively    |          0.02 |     0.98 |         16.00 |       914.00 |
| particularly     |          0.02 |     0.98 |      9,079.00 |   554,545.00 |
| outwardly        |          0.01 |     0.99 |         63.00 |     4,243.00 |
| there            |          0.01 |     0.99 |         62.00 |     4,294.00 |
| egregiously      |          0.01 |     0.99 |         22.00 |     1,585.00 |
| offensively      |          0.01 |     0.99 |         27.00 |     2,001.00 |
| exactly          |          0.01 |     0.99 |        787.00 |    58,687.00 |
| definitively     |          0.01 |     0.99 |         15.00 |     1,128.00 |
| objectively      |          0.01 |     0.99 |         80.00 |     6,023.00 |
| too              |          0.01 |     0.99 |     46,567.00 | 3,510,873.00 |
| precisely        |          0.01 |     0.99 |         48.00 |     3,795.00 |
| explicitly       |          0.01 |     0.99 |         83.00 |     7,020.00 |
| mechanically     |          0.01 |     0.99 |         35.00 |     2,971.00 |
| overly           |          0.01 |     0.99 |      1,364.00 |   116,223.00 |
| any              |          0.01 |     0.99 |      1,068.00 |    92,518.00 |
| implicitly       |          0.01 |     0.99 |         10.00 |       891.00 |

#### Top 30 ADJ totals comparison

| `adj_form_lower` | NEGmirror/ALL | DIFF/ALL | NEGmirror_RAW |   DIFF_RAW |
|:-----------------|--------------:|---------:|--------------:|-----------:|
| late             |          0.07 |     0.93 |     11,139.00 | 151,362.00 |
| fancy            |          0.06 |     0.94 |        780.00 |  11,425.00 |
| demoralizing     |          0.06 |     0.94 |         70.00 |   1,162.00 |
| aggravating      |          0.04 |     0.96 |        112.00 |   2,407.00 |
| early            |          0.04 |     0.96 |      5,218.00 | 114,205.00 |
| revelatory       |          0.04 |     0.96 |         62.00 |   1,638.00 |
| frustrating      |          0.03 |     0.97 |      2,062.00 |  61,303.00 |
| amiss            |          0.03 |     0.97 |         38.00 |   1,157.00 |
| motivating       |          0.03 |     0.97 |        128.00 |   4,130.00 |
| wrong            |          0.03 |     0.97 |      5,329.00 | 180,366.00 |
| infuriating      |          0.03 |     0.97 |        111.00 |   3,802.00 |
| comforting       |          0.03 |     0.97 |        404.00 |  14,006.00 |
| exhilarating     |          0.03 |     0.97 |        186.00 |   6,468.00 |
| invigorating     |          0.03 |     0.97 |         64.00 |   2,242.00 |
| dispiriting      |          0.03 |     0.97 |         33.00 |   1,169.00 |
| satisfying       |          0.03 |     0.97 |      1,805.00 |  64,248.00 |
| groundbreaking   |          0.03 |     0.97 |         76.00 |   2,746.00 |
| strenuous        |          0.03 |     0.97 |        196.00 |   7,214.00 |
| off-putting      |          0.03 |     0.97 |         72.00 |   2,743.00 |
| hurt             |          0.03 |     0.97 |         99.00 |   3,808.00 |
| discouraging     |          0.02 |     0.98 |        122.00 |   4,803.00 |
| empowering       |          0.02 |     0.98 |         78.00 |   3,139.00 |
| evident          |          0.02 |     0.98 |      1,469.00 |  59,131.00 |
| flashy           |          0.02 |     0.98 |        164.00 |   6,773.00 |
| frightful        |          0.02 |     0.98 |         26.00 |   1,095.00 |
| disheartening    |          0.02 |     0.98 |        128.00 |   5,404.00 |
| gratifying       |          0.02 |     0.98 |        295.00 |  13,320.00 |
| contemptible     |          0.02 |     0.98 |         22.00 |     996.00 |
| relaxing         |          0.02 |     0.98 |        409.00 |  19,465.00 |
| crass            |          0.02 |     0.98 |         49.00 |   2,340.00 |
