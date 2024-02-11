# Meeting: Thursday, November 16, 2023

## Agenda

- [plan for finishing](#planning)
- [updates](#updates)
- 
  
## Planning

- Crafted a new working outline [here](PlanPotential_2023-11-15.md)
- Would very much like to finish by summer

### Goal for the next 2 weeks

- [ ] 🌟 Write draft of [Chapters 2 & 3](../../Documents/dissertex/justwriting/PlanPotential_2023-11-15.md#2-the-why-problems-and-proposal-research-questionstheory-informed-motivations-for-corpus-creation) & send it to _all_ committee members.
  - [ ] Chapter 2: The **why**
    - _theory informed motivations for creating corpus/corpus methodology_
    - have started this in one form or other in several different place (find them!)

  - [ ] Chapter 3: The **what**
    - _describe it---how I created it, what it is, and how to use it, etc._
    - already have a partial draft of this, completed August 2022

## Updates

### Full Bigram Dataset has been counted!!! 🎉 🍾 ✨

- **Total Remaining Bigrams = `83,284,343`**
- for all case normalized word forms with at least `868` tokens across all combinations remaining in the dataset
- most tokens seen for a single adj: \
    `2,210,387` tokens of _many_
- most tokens seen for a single adv: \
    `9,913,432` tokens of _very_
- `3,894` unique adjectives in the dataset
- `1,005` unique adverbs in the dataset
- `4,415,785` tokens of _not_ in the `ADV` node position
    (e.g. _Bob was **not** happy_ or _a **not** unpleasant experience_)
- `1,206,294` tokens of _-n't_ in the `ADV` node position
    (e.g. _Bob was**n't** happy_)

- #### 👀 An example of a change directly resulting from using `ad*_form_lower` instead of `ad*_lemma`

     \#validated

    There seems to be an **obvious** difference in the shape of the distributions
    (per adverb form) for the base and comparative forms,
    if _good_ and _better_ can be taken as a representative example.
    The most telling examples here are those adverbs where _better_ has far more tokens,
    despite the sum being less than half that of _good_'s: **_much_** & **_even_**.
    Additionally, the disparity for the classic "degree diagnostic" adverbs is,
    in my estimation, evidence that _better_ (and the comparative form in general)
    is not itself **scalar**, despite being evidence that its stem, _good_, **is**.
    With the prior processing, these vectors would have appeared only as the sum,
    and the differences would have been completely obscured.

    | `adj_form_lower` |     `SUM` |  _very_ | _more_ | _most_ |    _so_ |  _not_ |    _as_ |  _too_ | _really_ | ↕️ _much_ | _pretty_ | _less_ |  _n't_ | ↕️ _even_ | _also_ | _quite_ |
    |:-----------------|----------:|--------:|-------:|-------:|--------:|-------:|--------:|-------:|---------:|----------:|---------:|-------:|-------:|----------:|-------:|--------:|
    | _good_           | 2,030,480 | 507,499 | 18,902 |  5,207 | 153,196 | 96,143 | 235,348 | 59,683 |  260,281 |    14,343 |  243,692 |  2,544 | 34,203 |     2,334 | 20,518 |  27,613 |
    | _better_         |   740,721 |      93 |  1,756 |     66 |     872 | 13,540 |   1,990 |     30 |    1,770 |   295,224 |       16 |     92 |  1,819 |   138,886 |  2,807 |     171 |

  - [ ] examine this same difference with transformed/normalized values
  - [ ] examine difference in association metrics as well

  - Descriptive stats from log
    > Frequency Filtered Hits Summary
    > |                |      count |   unique | top   |      freq |
    > |:---------------|-----------:|---------:|:------|----------:|
    > | adv_form_lower | 83,284,343 |     1005 | very  | 9,913,432 |
    > | adj_form_lower | 83,284,343 |     3894 | many  | 2,210,387 |

    > Frequency Filtered Word Type Distributions
    > |       |   `adv_form_lower` |   `adj_form_lower` |
    > |:------|-----------------:|-----------------:|
    > | count |            1,005 |            3,894 |
    > | mean  |           82,870 |           21,388 |
    > | std   |          581,924 |           91,460 |
    > | min   |              868 |              870 |
    > | 25%   |            1,705 |            1,637 |
    > | 50%   |            4,049 |            3,466 |
    > | 75%   |           15,767 |           10,673 |
    > | max   |        9,913,432 |        2,210,387 |

  ```log
  (base) arh234@g2-login-03:~$ sainfo
  JobID           JobName      State               Start                 End    Elapsed     ReqMem     MaxRSS   TotalCPU
  ------------ ---------- ---------- ------------------- ------------------- ---------- ---------- ---------- ----------
  1152527      115g35f~0+  COMPLETED 2023-11-15T00:00:00 2023-11-15T00:42:35   00:42:35       115G              02:20:46
  1152527.bat+      batch  COMPLETED 2023-11-15T00:00:00 2023-11-15T00:42:35   00:42:35                99.70G   02:20:46
  1152527.ext+     extern  COMPLETED 2023-11-15T00:00:00 2023-11-15T00:42:35   00:42:35                 0.00G   00:00:00
  ```

  ```shell
  tail -80 logs/count_RBgrams/115g35f~001-RBgrams_23-11-14_1152527.out
  ```

  ```log
  >>> 83,284,343 total remaining hits <<<
    95.97% of 86780216 total valid hits.
  * Saving list of all 83284343 bigram hit_id values retained after frequency filtering as
    + /share/compling/data/sanpi/4_post-processed/RBXadj/bigram-index_frq-thr0-001p.35f.txt
  ~ Saving frequency restrictred bigrams (868+ frequency threshold) as pickle...
    >> successfully saved as /share/compling/data/sanpi/4_post-processed/RBXadj/bigrams_frq-thr0-001p.35f.pkl.gz
        (time elapsed: 00:30:28.590)
  ✓ time: 02:15:59.601
      ⇟ minimum hits/word type in data: 868

    Frequency Filtered Hits Summary
    |                |      count | unique | top  |      freq |
    |:---------------|-----------:|-------:|:-----|----------:|
    | adv_form_lower | 83,284,343 |   1005 | very | 9,913,432 |
    | adj_form_lower | 83,284,343 |   3894 | many | 2,210,387 |

    Frequency Filtered Word Type Distributions
    |       | adv_form_lower | adj_form_lower |
    |:------|---------------:|---------------:|
    | count |          1,005 |          3,894 |
    | mean  |         82,870 |         21,388 |
    | std   |        581,924 |         91,460 |
    | min   |            868 |            870 |
    | 25%   |          1,705 |          1,637 |
    | 50%   |          4,049 |          3,466 |
    | 75%   |         15,767 |         10,673 |
    | max   |      9,913,432 |      2,210,387 |

  ## Processing Frequency data for all word types.
  [ Time to crosstabulate adj-x-adv frequencies: 00:04:28.586 ]
  ~ Saving all adj_form_lower ✕ adv_form_lower frequency table as pickle...
    >> successfully saved as /share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz
        (time elapsed: 00:00:09.540)
  ~ Saving all adj_form_lower ✕ adv_form_lower frequency table as csv...
    >> successfully saved as /share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.csv
        (time elapsed: 00:00:00.24)
  [ Time to process frequencies: 00:04:54.405 ]
  ~ Note: full descriptive statistics not calculated. To retrieve, simply rerun with same arguments + `-s` or `--get_stats` ~

  ### Summary Statistics for Marginal Frequencies ###
  |       | adjective totals | adverb totals |
  |:------|-----------------:|--------------:|
  | count |            1,005 |         3,894 |
  | mean  |           82,870 |        21,388 |
  | std   |          581,924 |        91,460 |
  | min   |              868 |           870 |
  | 25%   |            1,705 |         1,637 |
  | 50%   |            4,049 |         3,466 |
  | 75%   |           15,767 |        10,673 |
  | max   |        9,913,432 |     2,210,387 |

  ### Top 20 Adjectives by Top 15 Adverbs ###
  | adj_form_lower |        SUM |      very |      more |      most |        so |       not |        as |       too |    really |      much |    pretty |      less |       n't |      even |      also |     quite |
  |:---------------|-----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
  | SUM            | 83,284,343 | 9,913,432 | 9,320,997 | 7,568,812 | 5,735,964 | 4,415,785 | 3,709,914 | 3,557,440 | 2,096,057 | 1,986,728 | 1,621,748 | 1,256,870 | 1,206,294 | 1,120,205 | 1,108,517 | 1,065,022 |
  | many           |  2,210,387 |    21,237 |       373 |       140 | 1,191,864 |    58,442 |   434,631 |   450,194 |       518 |       201 |        54 |        54 |       580 |     5,310 |     1,132 |       230 |
  | important      |  2,199,447 |   359,610 |   306,604 |   748,533 |   105,509 |    17,351 |   102,823 |    12,879 |    72,175 |     1,826 |     6,594 |    25,152 |     7,071 |       658 |    67,118 |     5,670 |
  | good           |  2,030,480 |   507,499 |    18,902 |     5,207 |   153,196 |    96,143 |   235,348 |    59,683 |   260,281 |    14,343 |   243,692 |     2,544 |    34,203 |     2,334 |    20,518 |    27,613 |
  | much           |  1,776,924 |    42,365 |       102 |        22 |   614,652 |    66,410 |   355,368 |   583,184 |     3,066 |       284 |    57,884 |        15 |    13,683 |       999 |       407 |        87 |
  | likely         |  1,048,364 |    35,899 |   498,401 |   192,635 |       847 |    46,858 |    31,820 |     1,196 |       466 |       259 |     1,312 |   139,538 |    17,793 |       846 |    16,795 |     7,419 |
  | more           |  1,028,133 |        69 |     2,280 |        90 |     2,953 |    17,641 |     2,851 |        52 |     4,561 |   355,655 |        14 |       939 |       696 |   199,527 |     2,643 |        69 |
  | different      |    906,600 |   233,008 |    12,237 |     1,364 |    39,346 |     4,024 |     9,296 |     5,198 |     6,545 |    44,251 |     2,140 |       198 |       792 |       349 |     3,712 |    43,184 |
  | available      |    862,942 |       403 |     9,739 |     1,384 |       490 |   132,371 |     1,879 |       277 |       552 |       979 |        32 |     1,978 |    20,868 |     2,227 |   114,567 |       117 |
  | sure           |    844,066 |     4,691 |     2,324 |       315 |    35,676 |   467,213 |     3,900 |     8,714 |    20,125 |       341 |    84,366 |     2,358 |    92,560 |    14,871 |     2,043 |    36,320 |
  | difficult      |    832,988 |   188,193 |   220,215 |    76,638 |    26,542 |    19,841 |    16,041 |    27,938 |    18,779 |       638 |     5,649 |     5,467 |     5,778 |       784 |     4,195 |    15,489 |
  | popular        |    827,608 |    89,434 |    70,577 |   398,955 |    42,950 |     4,558 |    15,226 |     2,153 |     5,022 |     1,305 |     3,214 |     8,844 |     1,788 |       298 |     7,180 |    11,716 |
  | easy           |    768,452 |   125,544 |     5,567 |     1,215 |    88,639 |    95,490 |    73,233 |    40,465 |    29,583 |       816 |    31,788 |     1,832 |    37,638 |       520 |     9,937 |    18,250 |
  | better         |    740,721 |        93 |     1,756 |        66 |       872 |    13,540 |     1,990 |        30 |     1,770 |   295,224 |        16 |        92 |     1,819 |   138,886 |     2,807 |       171 |
  | high           |    586,188 |   138,155 |     5,218 |    10,402 |    35,697 |     5,769 |    68,042 |    78,087 |    11,041 |       576 |    13,002 |       528 |     2,392 |       284 |     5,023 |    10,239 |
  | common         |    555,893 |    45,763 |    85,760 |   272,787 |    15,145 |     7,175 |    11,388 |    10,439 |     1,531 |       916 |     7,186 |    16,523 |     1,347 |       222 |     6,225 |    14,326 |
  | bad            |    554,698 |    50,586 |     8,470 |       703 |    89,547 |    45,132 |    70,769 |    82,159 |    49,477 |     1,675 |    20,388 |     1,743 |    19,968 |       509 |     1,520 |     1,849 |
  | effective      |    530,361 |    50,857 |   141,978 |   148,925 |    11,156 |     7,561 |    27,812 |       591 |     4,532 |       508 |     2,078 |    17,454 |     2,100 |       303 |     3,941 |     4,780 |
  | happy          |    526,217 |   143,139 |     5,770 |     2,767 |    79,756 |    47,886 |    11,816 |    16,447 |    37,939 |       547 |    12,490 |     3,130 |    20,152 |       602 |     6,716 |    14,214 |
  | interesting    |    494,389 |   107,352 |   110,201 |    84,601 |    13,760 |     2,894 |     7,990 |     1,121 |    42,588 |       809 |    11,926 |     6,631 |     1,528 |       462 |     9,552 |    12,682 |
  | clear          |    489,305 |    93,435 |    15,101 |     1,491 |    12,170 |    91,591 |    13,449 |     2,575 |     5,766 |       538 |    29,902 |    10,241 |    19,228 |     1,774 |     7,346 |    20,270 |

  ................................
  ✓ Finished @ 2023-11-15 12:42AM
  == Total Run Time ==
      02:21:50.776
  ```

### Notebooks

- [comparison of `adj-x-adv` frequencies: all vs. direct NEG vs. difference (ALL - NEG)](../notebooks/compare_bigram-directNEG.ipynb)
- [transformed frequencies](../results/transform_freqs.ipynb)