# `NEQ`: Identifying Adverbs with Strongest Negative Environment Associations


```python
from source.utils.associate import TOP_AM_DIR
from source.utils.general import confirm_dir

from am_notebooks import *

DATE=timestamp_today()
SET_FLOOR = 5000
MIR_FLOOR = min(round(SET_FLOOR//15, -2), 1000)
K = 8

TAG='NEQ'
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
confirm_dir(TOP_AM_TAG_DIR)

data_top = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / data_top
confirm_dir(OUT_DIR)
METRIC_PRIORITIES = METRIC_PRIORITY_DICT[TAG]
parameters = {
    '`SET_FLOOR`': {
        'value': f'${SET_FLOOR:,}$',
        'description': '_`*direct` superset minimum `env~adv` co-occurence_',
    },
    '`MIR_FLOOR`': {
        'value': f'${MIR_FLOOR:,}$',
        'description': '_`*mirror` subset minimum `env~adv` co-occurence_',
    },
    '`TAG`': {
        'value': f'`"{TAG}"`',
        'description': '_frequency data evaluated_',
    },
    '`K`': {
        'value': f'${K}$',
        'description': '_# top adverbs sought_',
    },
    '`OUT_DIR`': {
        'value': f'`{OUT_DIR}/`',
        'description': '_output directory_',
    },
    '`DATE`': {
        'value': DATE,
        'description': '_date of processing_',
    }
}
nb_show_table(pd.DataFrame(parameters, dtype='string').T)
```


|                 | `value`                                                       | `description`                                       |
|:----------------|:--------------------------------------------------------------|:----------------------------------------------------|
| **`SET_FLOOR`** | $5,000$                                                       | _`*direct` superset minimum `env~adv` co-occurence_ |
| **`MIR_FLOOR`** | $300$                                                         | _`*mirror` subset minimum `env~adv` co-occurence_   |
| **`TAG`**       | `"NEQ"`                                                       | _frequency data evaluated_                          |
| **`K`**         | $8$                                                           | _# top adverbs sought_                              |
| **`OUT_DIR`**   | `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/` | _output directory_                                  |
| **`DATE`**      | 2024-07-30                                                    | _date of processing_                                |


Set columns and diplay settings


```python
FOCUS = FOCUS_DICT[TAG]['polar']
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 90)
pd.set_option("display.precision", 2)
pd.set_option("styler.format.precision", 2)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.2f}'.format)
```

## Set paths and load adverb association tables


```python
try:
    adv_am_paths = locate_polar_am_paths(superset_floor=SET_FLOOR,
                                         mirror_floor=MIR_FLOOR)
except Exception:
    MIR_FLOOR = 100
    adv_am_paths = locate_polar_am_paths(superset_floor=SET_FLOOR,
                                         mirror_floor=MIR_FLOOR)
```

    ╒══════════╤══════════════════════════════════════════════════════════════════════════╕
    │          │ path to selected AM dataframe                                            │
    ╞══════════╪══════════════════════════════════════════════════════════════════════════╡
    │ RBdirect │ /share/compling/projects/sanpi/results/assoc_df/polar/RBdirect/adv/extra │
    │          │ /polarized-adv_ALL-direct_min5000x_extra.parq                            │
    ├──────────┼──────────────────────────────────────────────────────────────────────────┤
    │ mirror   │ /share/compling/projects/sanpi/results/assoc_df/polar/mirror/adv/extra/p │
    │          │ olarized-adv_ALL-mirror_min300x_extra.parq                               │
    ╘══════════╧══════════════════════════════════════════════════════════════════════════╛



```python
setdiff_adv = adjust_am_names(filter_load_adx_am(adv_am_paths['RBdirect'], column_list=FOCUS))
mirror_adv = adjust_am_names(filter_load_adx_am(adv_am_paths['mirror'], column_list=FOCUS))

print(r'### Sample of Superset `RBdirect` $*E\sim\texttt{adv}$ AMs', 
      f'With $f\geq{SET_FLOOR:,}$ (i.e. `adv` occurs at least {SET_FLOOR:,} times)',
      sep='\n\n', end = '\n\n')
nb_show_table(setdiff_adv.sample(min(6,K)).sort_values('unexp_f', ascending=False))
```

### Sample of Superset `RBdirect` $*E\sim\texttt{adv}$ AMs

With $f\geq5,000$ (i.e. `adv` occurs at least 5,000 times)


|                      |     `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`       | `l2`         |       `f1` |    `f2` |        `N` |    `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |
|:---------------------|--------:|--------:|--------:|-------:|----------:|:-----------|:-------------|-----------:|--------:|-----------:|-----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|
| **COM~increasingly** | 374,465 |    0.04 |    7.02 |   1.00 | 32,515.21 | COMPLEMENT | increasingly | 69,665,890 | 374,538 | 72,839,571 | 358,219.07 |   16,245.93 |        0.04 |            2.37 | 26.55 |   0.02 |    0.01 |   0.01 |
| **NEGany~actually**  |  11,860 |    0.04 |    0.92 |   0.08 |  4,343.21 | NEGATED    | actually     |  3,173,681 | 141,962 | 72,839,571 |   6,185.40 |    5,674.60 |        0.48 |            0.30 | 52.11 |   0.28 |    0.00 |   0.00 |
| **COM~longer**       | 144,380 |    0.03 |    2.06 |   0.99 |  5,954.86 | COMPLEMENT | longer       | 69,665,890 | 145,746 | 72,839,571 | 139,395.73 |    4,984.27 |        0.03 |            0.68 | 13.12 |   0.02 |    0.00 |   0.00 |
| **COM~best**         |  50,827 |    0.03 |    1.56 |   0.99 |  1,659.97 | COMPLEMENT | best         | 69,665,890 |  51,464 | 72,839,571 |  49,221.67 |    1,605.33 |        0.03 |            0.56 |  7.12 |   0.01 |    0.00 |   0.00 |
| **COM~frequently**   |  18,298 |    0.04 |    2.24 |   0.99 |    982.03 | COMPLEMENT | frequently   | 69,665,890 |  18,406 | 72,839,571 |  17,604.03 |      693.97 |        0.04 |            0.89 |  5.13 |   0.02 |    0.00 |   0.00 |
| **COM~curiously**    |   6,713 |    0.04 |    2.82 |   1.00 |    497.47 | COMPLEMENT | curiously    | 69,665,890 |   6,725 | 72,839,571 |   6,431.99 |      281.01 |        0.04 |            1.39 |  3.43 |   0.02 |    0.00 |   0.00 |




```python
print(r'### Sample of Subset `mirror` $@E\sim\texttt{adv}$ AMs', 
      f'With $f\geq{MIR_FLOOR:,}$ (i.e. `adv` occurs at least {MIR_FLOOR:,} times)',
      sep='\n\n', end = '\n\n')
nb_show_table(mirror_adv.sample(min(6,K)).sort_values('unexp_f', ascending=False))
```

### Sample of Subset `mirror` $@E\sim\texttt{adv}$ AMs

With $f\geq300$ (i.e. `adv` occurs at least 300 times)


|                         |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`   | `l2`            |      `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |   `dP2` |   `P2` |
|:------------------------|------:|--------:|--------:|-------:|---------:|:-------|:----------------|----------:|-------:|----------:|----------:|------------:|------------:|----------------:|-------:|-------:|--------:|-------:|
| **NEGmir~inherently**   | 2,864 |    0.39 |    2.40 |   0.56 | 3,925.26 | NEGMIR | inherently      |   291,735 |  5,133 | 1,701,929 |    879.87 |    1,984.13 |        0.69 |            0.79 |  37.08 |   0.51 |    0.01 |   0.01 |
| **POS~almost**          | 5,247 |    0.16 |    3.70 |   0.99 | 1,640.80 | POSMIR | almost          | 1,410,194 |  5,288 | 1,701,929 |  4,381.56 |      865.44 |        0.16 |            1.42 |  11.95 |   0.08 |    0.00 |   0.00 |
| **POS~sometimes**       | 1,358 |    0.16 |    2.86 |   0.99 |   421.67 | POSMIR | sometimes       | 1,410,194 |  1,369 | 1,701,929 |  1,134.33 |      223.67 |        0.16 |            1.39 |   6.07 |   0.08 |    0.00 |   0.00 |
| **POS~little**          |   529 |    0.16 |    1.97 |   0.99 |   159.95 | POSMIR | little          | 1,410,194 |    534 | 1,701,929 |    442.46 |       86.54 |        0.16 |            1.30 |   3.76 |   0.08 |    0.00 |   0.00 |
| **POS~environmentally** |   720 |    0.09 |    0.27 |   0.91 |    47.49 | POSMIR | environmentally | 1,410,194 |    788 | 1,701,929 |    652.93 |       67.07 |        0.09 |            0.34 |   2.50 |   0.04 |    0.00 |   0.00 |
| **POS~overly**          | 2,893 |   -0.15 |   -0.98 |   0.68 |  -596.66 | POSMIR | overly          | 1,410,194 |  4,285 | 1,701,929 |  3,550.49 |     -657.49 |       -0.23 |           -0.37 | -12.22 |  -0.09 |   -0.00 |   0.00 |



## Calculate "Most Negative" Adverbs for each Polarity Approximation


```python
METRIC_PRI_2 = METRIC_PRIORITIES[:2]
nb_show_table(
    pd.concat([setdiff_adv.filter(METRIC_PRI_2).sample(5),
               mirror_adv.filter(METRIC_PRI_2).sample(5)])
)
```


|                       |   `LRC` |   `P1` |
|:----------------------|--------:|-------:|
| **COM~unfortunately** |    2.85 |   1.00 |
| **NEGany~absolutely** |   -1.32 |   0.02 |
| **COM~second**        |    1.34 |   0.99 |
| **COM~further**       |    1.95 |   0.99 |
| **COM~grossly**       |    0.80 |   0.98 |
| **POS~apparently**    |    0.01 |   0.90 |
| **POS~brand**         |    1.18 |   0.97 |
| **POS~readily**       |    0.35 |   0.90 |
| **NEGmir~just**       |   -2.68 |   0.03 |
| **POS~suddenly**      |    1.05 |   0.98 |


```python
[setdiff_top15, mirror_top15] = [
    get_top_vals(adjust_am_names(adv_df),
                 k=15,
                 metric_filter=METRIC_PRI_2)
    .assign(adv=adv_df.l2)
    for adv_df in (setdiff_adv, mirror_adv)
]
```


```python
print(f'### 15 Most Negatively Associated Adverbs for {TAG} data superset\n',
      '_Absent Negative_ approximation',
      f'ranked by {" & ".join([f"`{m}`" for m in METRIC_PRI_2])}', 
      sep='\n+ ')
nb_show_table(setdiff_top15.reset_index()
              .filter(items = ['adv'] + adjust_am_names(FOCUS)).filter(regex=r'^[^l]')
              )
```

### 15 Most Negatively Associated Adverbs for NEQ data superset

+ _Absent Negative_ approximation
+ ranked by `LRC` & `P1`

|        | `adv`       |     `f` |   `dP1` |   `LRC` |   `P1` |       `G2` |      `f1` |      `f2` |        `N` |    `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |
|:-------|:------------|--------:|--------:|--------:|-------:|-----------:|----------:|----------:|-----------:|-----------:|------------:|------------:|----------------:|-------:|-------:|
| **1**  | necessarily |  42,595 |    0.83 |    7.10 |   0.87 | 230,256.76 | 3,173,681 |    48,947 | 72,839,571 |   2,132.66 |   40,462.34 |        0.95 |            2.17 | 196.05 |   1.30 |
| **2**  | that        | 164,768 |    0.75 |    6.34 |   0.79 | 831,134.96 | 3,173,681 |   208,262 | 72,839,571 |   9,074.15 |  155,693.85 |        0.94 |            1.94 | 383.56 |   1.26 |
| **3**  | exactly     |  43,813 |    0.70 |    5.94 |   0.75 | 210,126.00 | 3,173,681 |    58,643 | 72,839,571 |   2,555.12 |   41,257.88 |        0.94 |            1.82 | 197.11 |   1.23 |
| **4**  | immediately |  56,099 |    0.54 |    4.86 |   0.58 | 224,058.80 | 3,173,681 |    96,973 | 72,839,571 |   4,225.19 |   51,873.81 |        0.92 |            1.49 | 219.01 |   1.12 |
| **5**  | yet         |  51,867 |    0.50 |    4.65 |   0.54 | 197,610.29 | 3,173,681 |    95,763 | 72,839,571 |   4,172.47 |   47,694.53 |        0.92 |            1.42 | 209.42 |   1.09 |
| **6**  | any         |  15,384 |    0.40 |    4.07 |   0.45 |  50,880.76 | 3,173,681 |    34,382 | 72,839,571 |   1,498.05 |   13,885.95 |        0.90 |            1.25 | 111.95 |   1.01 |
| **7**  | remotely    |   5,661 |    0.30 |    3.40 |   0.34 |  15,284.42 | 3,173,681 |    16,426 | 72,839,571 |     715.70 |    4,945.31 |        0.87 |            1.06 |  65.73 |   0.90 |
| **8**  | terribly    |  17,949 |    0.26 |    3.19 |   0.30 |  43,741.22 | 3,173,681 |    58,964 | 72,839,571 |   2,569.11 |   15,379.89 |        0.86 |            0.98 | 114.80 |   0.84 |
| **9**  | only        | 113,502 |    0.22 |    2.92 |   0.26 | 243,217.76 | 3,173,681 |   435,592 | 72,839,571 |  18,979.11 |   94,522.89 |        0.83 |            0.90 | 280.57 |   0.78 |
| **10** | overly      |  24,613 |    0.20 |    2.77 |   0.24 |  49,095.42 | 3,173,681 |   100,826 | 72,839,571 |   4,393.07 |   20,219.93 |        0.82 |            0.85 | 128.88 |   0.75 |
| **11** | entirely    |  63,321 |    0.19 |    2.70 |   0.23 | 121,161.73 | 3,173,681 |   271,851 | 72,839,571 |  11,844.77 |   51,476.22 |        0.81 |            0.83 | 204.57 |   0.73 |
| **12** | merely      |   5,918 |    0.15 |    2.32 |   0.20 |   9,443.79 | 3,173,681 |    30,000 | 72,839,571 |   1,307.12 |    4,610.88 |        0.78 |            0.73 |  59.94 |   0.66 |
| **13** | always      | 103,883 |    0.13 |    2.15 |   0.17 | 141,897.27 | 3,173,681 |   608,062 | 72,839,571 |  26,493.77 |   77,389.23 |        0.74 |            0.67 | 240.11 |   0.59 |
| **14** | as          | 531,731 |    0.12 |    2.08 |   0.16 | 726,913.93 | 3,173,681 | 3,270,915 | 72,839,571 | 142,516.50 |  389,214.50 |        0.73 |            0.69 | 533.76 |   0.57 |
| **15** | directly    |   8,197 |    0.12 |    2.04 |   0.17 |  10,716.74 | 3,173,681 |    49,169 | 72,839,571 |   2,142.33 |    6,054.67 |        0.74 |            0.64 |  66.87 |   0.58 |




```python
print(f'### 15 Most Negatively Associated Adverbs for {TAG} data subset\n',
      '_Present Positive_ approximation',
      f'ranked by {" & ".join([f"`{m}`" for m in METRIC_PRI_2])}', 
      sep='\n+ ')
nb_show_table(mirror_top15.reset_index()
              .filter(items = ['adv'] + adjust_am_names(FOCUS))
              .filter(regex=r'^[^l]'))
```

### 15 Most Negatively Associated Adverbs for NEQ data subset

+ _Present Positive_ approximation
+ ranked by `LRC` & `P1`

|        | `adv`         |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` |    `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |
|:-------|:--------------|------:|--------:|--------:|-------:|----------:|--------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|
| **1**  | ever          | 4,709 |    0.76 |    5.63 |   0.93 | 14,253.47 | 291,735 |  5,060 | 1,701,929 |    867.36 |    3,841.64 |        0.82 |            1.82 | 55.98 |   0.73 |
| **2**  | any           | 1,066 |    0.72 |    4.65 |   0.89 |  2,985.73 | 291,735 |  1,197 | 1,701,929 |    205.18 |      860.82 |        0.81 |            1.59 | 26.37 |   0.72 |
| **3**  | necessarily   |   963 |    0.70 |    4.39 |   0.87 |  2,597.66 | 291,735 |  1,107 | 1,701,929 |    189.76 |      773.24 |        0.80 |            1.51 | 24.92 |   0.71 |
| **4**  | that          | 4,308 |    0.61 |    3.90 |   0.78 |  9,957.28 | 291,735 |  5,494 | 1,701,929 |    941.75 |    3,366.25 |        0.78 |            1.25 | 51.29 |   0.66 |
| **5**  | remotely      | 1,840 |    0.62 |    3.79 |   0.79 |  4,256.31 | 291,735 |  2,341 | 1,701,929 |    401.28 |    1,438.72 |        0.78 |            1.25 | 33.54 |   0.66 |
| **6**  | exactly       |   813 |    0.61 |    3.57 |   0.78 |  1,860.71 | 291,735 |  1,041 | 1,701,929 |    178.44 |      634.56 |        0.78 |            1.24 | 22.25 |   0.66 |
| **7**  | particularly  | 9,243 |    0.54 |    3.43 |   0.71 | 18,583.63 | 291,735 | 13,003 | 1,701,929 |  2,228.90 |    7,014.10 |        0.76 |            1.09 | 72.96 |   0.62 |
| **8**  | inherently    | 2,864 |    0.39 |    2.40 |   0.56 |  3,925.26 | 291,735 |  5,133 | 1,701,929 |    879.87 |    1,984.13 |        0.69 |            0.79 | 37.08 |   0.51 |
| **9**  | overtly       |   391 |    0.35 |    1.89 |   0.53 |    483.89 | 291,735 |    743 | 1,701,929 |    127.36 |      263.64 |        0.67 |            0.73 | 13.33 |   0.49 |
| **10** | intrinsically |   433 |    0.32 |    1.70 |   0.49 |    466.37 | 291,735 |    890 | 1,701,929 |    152.56 |      280.44 |        0.65 |            0.66 | 13.48 |   0.45 |
| **11** | especially    | 1,569 |    0.23 |    1.45 |   0.40 |  1,140.78 | 291,735 |  3,926 | 1,701,929 |    672.97 |      896.03 |        0.57 |            0.51 | 22.62 |   0.37 |
| **12** | fully         | 1,664 |    0.19 |    1.23 |   0.36 |    957.28 | 291,735 |  4,598 | 1,701,929 |    788.16 |      875.84 |        0.53 |            0.44 | 21.47 |   0.32 |
| **13** | yet           |   320 |    0.22 |    1.11 |   0.39 |    223.08 | 291,735 |    815 | 1,701,929 |    139.70 |      180.30 |        0.56 |            0.50 | 10.08 |   0.36 |
| **14** | terribly      | 1,567 |    0.17 |    1.09 |   0.34 |    764.42 | 291,735 |  4,610 | 1,701,929 |    790.22 |      776.78 |        0.50 |            0.40 | 19.62 |   0.30 |




```python
print(f'* Total unique mirror adv where LRC >= 1 and f > {MIR_FLOOR:,}',
      (mirror_adv.loc[mirror_adv.LRC > 1]
       .value_counts('l1').to_frame('adv subtotal')
       .to_markdown(intfmt=',', tablefmt='simple')),
      (adjust_am_names(
          catify(mirror_adv, reverse=True).filter(like='NEG', axis=0))
       .loc[mirror_adv.LRC >= 1, ['l2', 'f']+METRIC_PRIORITIES]
       .sort_values(METRIC_PRIORITIES[0], ascending=False)
       .to_markdown(intfmt=',', floatfmt=',.2f', tablefmt='simple_outline')),
      sep='\n\n')
```

    * Total unique mirror adv where LRC >= 1 and f > 300
    
    l1        adv subtotal
    ------  --------------
    POSMIR              96
    NEGMIR              15
    
    ┌──────────────────────┬───────────────┬───────┬───────┬──────┬───────────┬──────┐
    │ key                  │ l2            │     f │   LRC │   P1 │        G2 │   P2 │
    ├──────────────────────┼───────────────┼───────┼───────┼──────┼───────────┼──────┤
    │ NEGmir~not           │ not           │ 1,404 │  8.78 │ 1.00 │  4,958.00 │ 0.00 │
    │ NEGmir~ever          │ ever          │ 4,709 │  5.63 │ 0.93 │ 14,253.47 │ 0.02 │
    │ NEGmir~any           │ any           │ 1,066 │  4.65 │ 0.89 │  2,985.73 │ 0.00 │
    │ NEGmir~necessarily   │ necessarily   │   963 │  4.39 │ 0.87 │  2,597.66 │ 0.00 │
    │ NEGmir~that          │ that          │ 4,308 │  3.90 │ 0.78 │  9,957.28 │ 0.01 │
    │ NEGmir~remotely      │ remotely      │ 1,840 │  3.79 │ 0.79 │  4,256.31 │ 0.01 │
    │ NEGmir~exactly       │ exactly       │   813 │  3.57 │ 0.78 │  1,860.71 │ 0.00 │
    │ NEGmir~particularly  │ particularly  │ 9,243 │  3.43 │ 0.71 │ 18,583.63 │ 0.03 │
    │ NEGmir~inherently    │ inherently    │ 2,864 │  2.40 │ 0.56 │  3,925.26 │ 0.01 │
    │ NEGmir~overtly       │ overtly       │   391 │  1.89 │ 0.53 │    483.89 │ 0.00 │
    │ NEGmir~intrinsically │ intrinsically │   433 │  1.70 │ 0.49 │    466.37 │ 0.00 │
    │ NEGmir~especially    │ especially    │ 1,569 │  1.45 │ 0.40 │  1,140.78 │ 0.01 │
    │ NEGmir~fully         │ fully         │ 1,664 │  1.23 │ 0.36 │    957.28 │ 0.01 │
    │ NEGmir~yet           │ yet           │   320 │  1.11 │ 0.39 │    223.08 │ 0.00 │
    │ NEGmir~terribly      │ terribly      │ 1,567 │  1.09 │ 0.34 │    764.42 │ 0.01 │
    └──────────────────────┴───────────────┴───────┴───────┴──────┴───────────┴──────┘


### Or here, the least "negative"/most "non-negative"


```python
show_top_positive(setdiff_adv, k=15, data_tag=TAG, filter_and_sort=METRIC_PRI_2)
```

#### Top 15 Adverbs in *Complement* Polarity Environment (`set_diff`, $*\complement_{N^+}$)

> ranked by `['LRC', 'P1']`

**Total Tokens in dataset**: $N = 72,839,571$

|                    |   `LRC` |   `P1` |       `f` |   `dP1` |       `G2` |       `f1` |      `f2` |      `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |
|:-------------------|--------:|-------:|----------:|--------:|-----------:|-----------:|----------:|-------------:|------------:|------------:|----------------:|------:|-------:|
| **increasingly**   |    7.02 |   1.00 |   374,465 |    0.04 |  32,515.21 | 69,665,890 |   374,538 |   358,219.07 |   16,245.93 |        0.04 |            2.37 | 26.55 |   0.02 |
| **relatively**     |    5.96 |   1.00 |   583,426 |    0.04 |  48,767.89 | 69,665,890 |   583,744 |   558,309.79 |   25,116.21 |        0.04 |            1.93 | 32.88 |   0.02 |
| **almost**         |    5.26 |   1.00 |   434,507 |    0.04 |  34,964.27 | 69,665,890 |   434,904 |   415,954.87 |   18,552.13 |        0.04 |            1.70 | 28.14 |   0.02 |
| **mostly**         |    5.09 |   1.00 |   199,883 |    0.04 |  16,053.14 | 69,665,890 |   200,066 |   191,348.96 |    8,534.04 |        0.04 |            1.70 | 19.09 |   0.02 |
| **seemingly**      |    5.03 |   1.00 |   161,276 |    0.04 |  12,953.82 | 69,665,890 |   161,423 |   154,389.66 |    6,886.33 |        0.04 |            1.70 | 17.15 |   0.02 |
| **fairly**         |    4.97 |   1.00 |   371,923 |    0.04 |  29,332.96 | 69,665,890 |   372,340 |   356,116.84 |   15,806.16 |        0.04 |            1.61 | 25.92 |   0.02 |
| **pretty**         |    4.96 |   1.00 | 1,511,615 |    0.04 | 118,377.54 | 69,665,890 | 1,513,571 | 1,447,623.45 |   63,991.55 |        0.04 |            1.56 | 52.05 |   0.02 |
| **largely**        |    4.87 |   1.00 |   173,667 |    0.04 |  13,747.92 | 69,665,890 |   173,852 |   166,277.12 |    7,389.88 |        0.04 |            1.63 | 17.73 |   0.02 |
| **partly**         |    4.80 |   1.00 |    78,775 |    0.04 |   6,329.57 | 69,665,890 |    78,846 |    75,410.61 |    3,364.39 |        0.04 |            1.70 | 11.99 |   0.02 |
| **albeit**         |    4.80 |   1.00 |    15,742 |    0.04 |   1,364.13 | 69,665,890 |    15,745 |    15,058.98 |      683.02 |        0.04 |            2.31 |  5.44 |   0.02 |
| **rather**         |    4.74 |   1.00 |   363,581 |    0.04 |  28,091.98 | 69,665,890 |   364,070 |   348,207.17 |   15,373.83 |        0.04 |            1.53 | 25.50 |   0.02 |
| **sometimes**      |    4.55 |   1.00 |   141,910 |    0.04 |  10,959.00 | 69,665,890 |   142,099 |   135,907.63 |    6,002.37 |        0.04 |            1.53 | 15.93 |   0.02 |
| **also**           |    4.45 |   1.00 | 1,062,622 |    0.04 |  78,975.91 | 69,665,890 | 1,064,588 | 1,018,203.01 |   44,418.99 |        0.04 |            1.40 | 43.09 |   0.02 |
| **supposedly**     |    4.40 |   1.00 |    27,562 |    0.04 |   2,236.14 | 69,665,890 |    27,584 |    26,382.14 |    1,179.86 |        0.04 |            1.75 |  7.11 |   0.02 |
| **virtually**      |    4.32 |   1.00 |    86,032 |    0.04 |   6,575.98 | 69,665,890 |    86,156 |    82,402.11 |    3,629.89 |        0.04 |            1.50 | 12.38 |   0.02 |
| **allegedly**      |    4.05 |   1.00 |    16,367 |    0.04 |   1,328.28 | 69,665,890 |    16,380 |    15,666.31 |      700.69 |        0.04 |            1.74 |  5.48 |   0.02 |
| **understandably** |    3.96 |   1.00 |    12,295 |    0.04 |   1,012.27 | 69,665,890 |    12,303 |    11,766.95 |      528.05 |        0.04 |            1.82 |  4.76 |   0.02 |
| **beyond**         |    3.87 |   1.00 |    13,836 |    0.04 |   1,114.85 | 69,665,890 |    13,848 |    13,244.63 |      591.37 |        0.04 |            1.70 |  5.03 |   0.02 |
| **admittedly**     |    3.85 |   1.00 |    12,587 |    0.04 |   1,021.46 | 69,665,890 |    12,597 |    12,048.14 |      538.86 |        0.04 |            1.74 |  4.80 |   0.02 |
| **undoubtedly**    |    3.81 |   1.00 |    11,657 |    0.04 |     948.08 | 69,665,890 |    11,666 |    11,157.70 |      499.30 |        0.04 |            1.75 |  4.62 |   0.02 |
| **presumably**     |    3.69 |   1.00 |     7,308 |    0.04 |     617.16 | 69,665,890 |     7,311 |     6,992.45 |      315.55 |        0.04 |            1.98 |  3.69 |   0.02 |
| **hopefully**      |    3.44 |   1.00 |     7,183 |    0.04 |     588.65 | 69,665,890 |     7,188 |     6,874.81 |      308.19 |        0.04 |            1.77 |  3.64 |   0.02 |




```python
# Mirror Data ~ explicitly positive ~ positive trigger present
show_top_positive(mirror_adv, k=15, data_tag=TAG, filter_and_sort=METRIC_PRI_2)
```

#### Top 15 Adverbs in *Posmir* Polarity Environment (`mirror`, $@P$)

> ranked by `['LRC', 'P1']`

**Total Tokens in dataset**: $N = 1,701,929$

|                 |   `LRC` |   `P1` |    `f` |   `dP1` |     `G2` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |
|:----------------|--------:|-------:|-------:|--------:|---------:|----------:|-------:|----------:|------------:|------------:|----------------:|------:|-------:|
| **pretty**      |    4.71 |   0.99 | 24,593 |    0.17 | 8,175.09 | 1,410,194 | 24,720 | 20,482.64 |    4,110.36 |        0.17 |            1.61 | 26.21 |   0.08 |
| **rather**      |    4.62 |   1.00 |  8,383 |    0.17 | 2,853.24 | 1,410,194 |  8,415 |  6,972.55 |    1,410.45 |        0.17 |            1.73 | 15.40 |   0.08 |
| **plain**       |    4.44 |   1.00 |  5,062 |    0.17 | 1,738.92 | 1,410,194 |  5,079 |  4,208.39 |      853.61 |        0.17 |            1.78 | 12.00 |   0.08 |
| **fairly**      |    4.32 |   1.00 |  5,703 |    0.17 | 1,922.49 | 1,410,194 |  5,727 |  4,745.31 |      957.69 |        0.17 |            1.68 | 12.68 |   0.08 |
| **somewhat**    |    4.31 |   1.00 |  4,482 |    0.17 | 1,531.96 | 1,410,194 |  4,498 |  3,726.98 |      755.02 |        0.17 |            1.75 | 11.28 |   0.08 |
| **otherwise**   |    4.06 |   0.99 |  6,857 |    0.17 | 2,219.99 | 1,410,194 |  6,899 |  5,716.41 |    1,140.59 |        0.17 |            1.53 | 13.77 |   0.08 |
| **maybe**       |    3.98 |   1.00 |  2,672 |    0.17 |   916.94 | 1,410,194 |  2,681 |  2,221.44 |      450.56 |        0.17 |            1.77 |  8.72 |   0.08 |
| **downright**   |    3.88 |   0.99 |  4,726 |    0.17 | 1,528.56 | 1,410,194 |  4,755 |  3,939.92 |      786.08 |        0.17 |            1.52 | 11.43 |   0.08 |
| **already**     |    3.80 |   0.99 |  4,275 |    0.17 | 1,377.37 | 1,410,194 |  4,302 |  3,564.58 |      710.42 |        0.17 |            1.51 | 10.87 |   0.08 |
| **relatively**  |    3.79 |   0.99 |  5,307 |    0.16 | 1,681.39 | 1,410,194 |  5,345 |  4,428.79 |      878.21 |        0.17 |            1.46 | 12.06 |   0.08 |
| **almost**      |    3.70 |   0.99 |  5,247 |    0.16 | 1,640.80 | 1,410,194 |  5,288 |  4,381.56 |      865.44 |        0.16 |            1.42 | 11.95 |   0.08 |
| **equally**     |    3.58 |   0.99 |  7,316 |    0.16 | 2,195.34 | 1,410,194 |  7,389 |  6,122.42 |    1,193.58 |        0.16 |            1.32 | 13.95 |   0.08 |
| **perhaps**     |    3.52 |   0.99 |  3,526 |    0.16 | 1,105.37 | 1,410,194 |  3,553 |  2,943.96 |      582.04 |        0.17 |            1.42 |  9.80 |   0.08 |
| **highly**      |    3.25 |   0.99 |  9,134 |    0.16 | 2,534.99 | 1,410,194 |  9,264 |  7,676.02 |    1,457.98 |        0.16 |            1.16 | 15.26 |   0.08 |
| **slightly**    |    3.22 |   0.99 |  7,559 |    0.16 | 2,104.57 | 1,410,194 |  7,665 |  6,351.11 |    1,207.89 |        0.16 |            1.17 | 13.89 |   0.08 |
| **eerily**      |    1.96 |   1.00 |    402 |    0.17 |   133.03 | 1,410,194 |    404 |    334.75 |       67.25 |        0.17 |            1.52 |  3.35 |   0.08 |
| **lightly**     |    1.95 |   1.00 |    399 |    0.17 |   131.93 | 1,410,194 |    401 |    332.26 |       66.74 |        0.17 |            1.52 |  3.34 |   0.08 |
| **darn**        |    1.94 |   0.99 |    439 |    0.16 |   139.76 | 1,410,194 |    442 |    366.23 |       72.77 |        0.17 |            1.41 |  3.47 |   0.08 |
| **chronically** |    1.65 |   0.99 |    325 |    0.17 |   104.91 | 1,410,194 |    327 |    270.95 |       54.05 |        0.17 |            1.43 |  3.00 |   0.08 |



## Compile top NEG~adverb associations across both approximation methods

### Define the functions

[_moved to `./am_notebooks.py`_]

### Run it 🏃‍♀️


```python
C = combine_top_adv(
    df_1=setdiff_adv, name_1='SET',
    df_2=mirror_adv, name_2='MIR',
    adv_am_paths=adv_am_paths,
    data_tag=TAG,
    filter_items=pd.Series(FOCUS + METRIC_PRIORITIES
                           ).drop_duplicates().to_list(),
    set_floor=SET_FLOOR,
    k=K)
```

### `NEQ` Most Negative Adverb Selections

`SET`: union of top 8 adverbs ranked by `['LRC', 'P1']`
1. _necessarily_
1. _that_
1. _exactly_
1. _immediately_
1. _yet_
1. _any_
1. _remotely_
1. _terribly_

`MIR`: union of top 8 adverbs ranked by `['LRC', 'P1']`
1. _ever_
1. _any_
1. _necessarily_
1. _that_
1. _remotely_
1. _exactly_
1. _particularly_
1. _inherently_

Union of top adverbs for `SET` and `MIR`. (Novel `MIR` adverbs listed last)
1. _necessarily_
1. _that_
1. _exactly_
1. _immediately_
1. _yet_
1. _any_
1. _remotely_
1. _terribly_
1. _ever_
1. _particularly_
1. _inherently_

### `SET` Adverb Associations (in initially loaded table)


|                  |     `f` |   `dP1` |   `LRC` |   `P1` |       `G2` |      `f1` |    `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |   `dP2` |   `P2` |
|:-----------------|--------:|--------:|--------:|-------:|-----------:|----------:|--------:|----------:|------------:|------------:|----------------:|-------:|-------:|--------:|-------:|
| **necessarily**  |  42,595 |    0.83 |    7.10 |   0.87 | 230,256.76 | 3,173,681 |  48,947 |  2,132.66 |   40,462.34 |        0.95 |            2.17 | 196.05 |   1.30 |    0.01 |   0.01 |
| **that**         | 164,768 |    0.75 |    6.34 |   0.79 | 831,134.96 | 3,173,681 | 208,262 |  9,074.15 |  155,693.85 |        0.94 |            1.94 | 383.56 |   1.26 |    0.05 |   0.05 |
| **exactly**      |  43,813 |    0.70 |    5.94 |   0.75 | 210,126.00 | 3,173,681 |  58,643 |  2,555.12 |   41,257.88 |        0.94 |            1.82 | 197.11 |   1.23 |    0.01 |   0.01 |
| **immediately**  |  56,099 |    0.54 |    4.86 |   0.58 | 224,058.80 | 3,173,681 |  96,973 |  4,225.20 |   51,873.80 |        0.92 |            1.49 | 219.01 |   1.12 |    0.02 |   0.02 |
| **yet**          |  51,867 |    0.50 |    4.65 |   0.54 | 197,610.29 | 3,173,681 |  95,763 |  4,172.47 |   47,694.53 |        0.92 |            1.42 | 209.42 |   1.09 |    0.02 |   0.02 |
| **any**          |  15,384 |    0.40 |    4.07 |   0.45 |  50,880.76 | 3,173,681 |  34,382 |  1,498.05 |   13,885.95 |        0.90 |            1.25 | 111.95 |   1.01 |    0.00 |   0.00 |
| **remotely**     |   5,661 |    0.30 |    3.40 |   0.34 |  15,284.42 | 3,173,681 |  16,426 |    715.70 |    4,945.30 |        0.87 |            1.06 |  65.73 |   0.90 |    0.00 |   0.00 |
| **terribly**     |  17,949 |    0.26 |    3.19 |   0.30 |  43,741.22 | 3,173,681 |  58,964 |  2,569.11 |   15,379.89 |        0.86 |            0.98 | 114.80 |   0.84 |    0.01 |   0.01 |
| **inherently**   |   6,743 |    0.10 |    1.75 |   0.14 |   7,021.95 | 3,173,681 |  47,803 |  2,082.82 |    4,660.18 |        0.69 |            0.56 |  56.75 |   0.51 |    0.00 |   0.00 |
| **particularly** |  55,527 |    0.06 |    1.38 |   0.11 |  37,272.26 | 3,173,681 | 513,668 | 22,380.94 |   33,146.06 |        0.60 |            0.43 | 140.66 |   0.39 |    0.01 |   0.02 |
| **ever**         |   5,932 |    0.01 |    0.16 |   0.05 |     183.91 | 3,173,681 | 114,075 |  4,970.34 |      961.66 |        0.16 |            0.08 |  12.49 |   0.08 |    0.00 |   0.00 |


### `MIR` Adverb Associations (in initially loaded table)


|                  |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` |    `f1` |   `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |
|:-----------------|------:|--------:|--------:|-------:|----------:|--------:|-------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|
| **ever**         | 4,709 |    0.76 |    5.63 |   0.93 | 14,253.47 | 291,735 |  5,060 |    867.36 |    3,841.64 |        0.82 |            1.82 | 55.98 |   0.73 |    0.02 |   0.02 |
| **any**          | 1,066 |    0.72 |    4.65 |   0.89 |  2,985.73 | 291,735 |  1,197 |    205.18 |      860.82 |        0.81 |            1.59 | 26.37 |   0.72 |    0.00 |   0.00 |
| **necessarily**  |   963 |    0.70 |    4.39 |   0.87 |  2,597.66 | 291,735 |  1,107 |    189.76 |      773.24 |        0.80 |            1.51 | 24.92 |   0.71 |    0.00 |   0.00 |
| **that**         | 4,308 |    0.61 |    3.90 |   0.78 |  9,957.28 | 291,735 |  5,494 |    941.75 |    3,366.25 |        0.78 |            1.25 | 51.29 |   0.66 |    0.01 |   0.01 |
| **remotely**     | 1,840 |    0.62 |    3.79 |   0.79 |  4,256.31 | 291,735 |  2,341 |    401.28 |    1,438.72 |        0.78 |            1.25 | 33.54 |   0.66 |    0.01 |   0.01 |
| **exactly**      |   813 |    0.61 |    3.57 |   0.78 |  1,860.71 | 291,735 |  1,041 |    178.44 |      634.56 |        0.78 |            1.24 | 22.25 |   0.66 |    0.00 |   0.00 |
| **particularly** | 9,243 |    0.54 |    3.43 |   0.71 | 18,583.64 | 291,735 | 13,003 |  2,228.90 |    7,014.10 |        0.76 |            1.09 | 72.96 |   0.62 |    0.03 |   0.03 |
| **inherently**   | 2,864 |    0.39 |    2.40 |   0.56 |  3,925.26 | 291,735 |  5,133 |    879.87 |    1,984.13 |        0.69 |            0.79 | 37.08 |   0.51 |    0.01 |   0.01 |
| **yet**          |   320 |    0.22 |    1.11 |   0.39 |    223.08 | 291,735 |    815 |    139.70 |      180.30 |        0.56 |            0.50 | 10.08 |   0.36 |    0.00 |   0.00 |
| **terribly**     | 1,567 |    0.17 |    1.09 |   0.34 |    764.42 | 291,735 |  4,610 |    790.22 |      776.78 |        0.50 |            0.40 | 19.62 |   0.30 |    0.00 |   0.01 |
| **immediately**  |   403 |    0.17 |    0.84 |   0.34 |    191.87 | 291,735 |  1,195 |    204.84 |      198.16 |        0.49 |            0.39 |  9.87 |   0.29 |    0.00 |   0.00 |




```python
nb_show_table(C.filter(regex=r'^ratio_f2?_')
              .assign(f_minus_f2=C.ratio_f_MIR - C.ratio_f2_MIR)
              .multiply(100).round(1)
              .sort_values(['f_minus_f2', 'ratio_f_MIR'], ascending=False),
              n_dec=1, adjust_columns=False)

```


|                  |   `ratio_f_MIR` |   `ratio_f2_MIR` |   `f_minus_f2` |
|:-----------------|----------------:|-----------------:|---------------:|
| **ever**         |            79.4 |              4.4 |           74.9 |
| **inherently**   |            42.5 |             10.7 |           31.7 |
| **remotely**     |            32.5 |             14.3 |           18.3 |
| **particularly** |            16.6 |              2.5 |           14.1 |
| **any**          |             6.9 |              3.5 |            3.4 |
| **terribly**     |             8.7 |              7.8 |            0.9 |
| **exactly**      |             1.9 |              1.8 |            0.1 |
| **that**         |             2.6 |              2.6 |           -0.0 |
| **necessarily**  |             2.3 |              2.3 |           -0.0 |
| **yet**          |             0.6 |              0.9 |           -0.2 |
| **immediately**  |             0.7 |              1.2 |           -0.5 |




```python
nb_show_table(
    C
    .filter(regex=r'^f_.*[MS]')
    .sort_index(axis=1, ascending=False)
    .assign(f_diff=C.f_SET-C.f_MIR)
    .sort_values('f_diff', ascending=False)
    .rename(columns={'f_SET': 'total negations',
                     'f_MIR': 'mirror subset negations',
                     'f_diff': 'negations not in mirror subset'}), n_dec=0)
```

#### Joint (_Negated_) Frequency Comparison

|                  |   `total negations` |   `mirror subset negations` |   `negations not in mirror subset` |
|:-----------------|--------------------:|----------------------------:|-----------------------------------:|
| **that**         |             164,768 |                       4,308 |                            160,460 |
| **immediately**  |              56,099 |                         403 |                             55,696 |
| **yet**          |              51,867 |                         320 |                             51,547 |
| **particularly** |              55,527 |                       9,243 |                             46,284 |
| **exactly**      |              43,813 |                         813 |                             43,000 |
| **necessarily**  |              42,595 |                         963 |                             41,632 |
| **terribly**     |              17,949 |                       1,567 |                             16,382 |
| **any**          |              15,384 |                       1,066 |                             14,318 |
| **inherently**   |               6,743 |                       2,864 |                              3,879 |
| **remotely**     |               5,661 |                       1,840 |                              3,821 |
| **ever**         |               5,932 |                       4,709 |                              1,223 |




```python
nb_show_table(
    C
    .filter(regex=r'^f2_.*[MS]').sort_index(axis=1, ascending=False)
    .assign(
        f2_diff=C.f2_SET-C.f2_MIR).sort_values('f2_diff', ascending=False)
    .rename(columns={'f2_SET':'total adverb tokens', 
                     'f2_MIR':'mirror subset adverb tokens', 
                     'f2_diff': 'adverb tokens not in mirror subset'}), n_dec=0)
```

#### Marginal (_Adverb Total_) Frequency Comparison

|                  |   `total adverb tokens` |   `mirror subset adverb tokens` |   `adverb tokens not in mirror subset` |
|:-----------------|------------------------:|--------------------------------:|---------------------------------------:|
| **particularly** |                 513,668 |                          13,003 |                                500,665 |
| **that**         |                 208,262 |                           5,494 |                                202,768 |
| **ever**         |                 114,075 |                           5,060 |                                109,015 |
| **immediately**  |                  96,973 |                           1,195 |                                 95,778 |
| **yet**          |                  95,763 |                             815 |                                 94,948 |
| **exactly**      |                  58,643 |                           1,041 |                                 57,602 |
| **terribly**     |                  58,964 |                           4,610 |                                 54,354 |
| **necessarily**  |                  48,947 |                           1,107 |                                 47,840 |
| **inherently**   |                  47,803 |                           5,133 |                                 42,670 |
| **any**          |                  34,382 |                           1,197 |                                 33,185 |
| **remotely**     |                  16,426 |                           2,341 |                                 14,085 |




```python
full_C = C.copy()
main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in METRIC_PRIORITIES],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2'] ]) 
                              ).drop_duplicates().to_list()
main_C = C[[c for c in main_cols_ordered if c in C.columns]]
sorter = f'mean_{METRIC_PRIORITIES[0]}'
print(f'### Main Columns for Top Adverbs, sorted by `{sorter}`')
nb_show_table(main_C.sort_values(sorter, ascending=False))
```

### Main Columns for Top Adverbs, sorted by `mean_LRC`

|                  |   `LRC_SET` |   `LRC_MIR` |   `mean_LRC` |   `dP1_SET` |   `P1_SET` |   `dP1_MIR` |   `P1_MIR` |   `mean_dP1` |   `mean_P1` |   `G2_SET` |   `G2_MIR` |   `mean_G2` |   `dP2_SET` |   `P2_SET` |   `dP2_MIR` |   `P2_MIR` |   `mean_dP2` |   `mean_P2` |   `f_SET` |   `f_MIR` |   `f1_SET` |   `f1_MIR` |   `f2_SET` |   `f2_MIR` |
|:-----------------|------------:|------------:|-------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|-----------:|-----------:|------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|----------:|----------:|-----------:|-----------:|-----------:|-----------:|
| **necessarily**  |        7.10 |        4.39 |         5.74 |        0.83 |       0.87 |        0.70 |       0.87 |         0.76 |        0.87 | 230,256.76 |   2,597.66 |  116,427.21 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    42,595 |       963 |  3,173,681 |    291,735 |     48,947 |      1,107 |
| **that**         |        6.34 |        3.90 |         5.12 |        0.75 |       0.79 |        0.61 |       0.78 |         0.68 |        0.79 | 831,134.96 |   9,957.28 |  420,546.12 |        0.05 |       0.05 |        0.01 |       0.01 |         0.03 |        0.03 |   164,768 |     4,308 |  3,173,681 |    291,735 |    208,262 |      5,494 |
| **exactly**      |        5.94 |        3.57 |         4.76 |        0.70 |       0.75 |        0.61 |       0.78 |         0.66 |        0.76 | 210,126.00 |   1,860.71 |  105,993.36 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    43,813 |       813 |  3,173,681 |    291,735 |     58,643 |      1,041 |
| **any**          |        4.07 |        4.65 |         4.36 |        0.40 |       0.45 |        0.72 |       0.89 |         0.56 |        0.67 |  50,880.76 |   2,985.73 |   26,933.25 |        0.00 |       0.00 |        0.00 |       0.00 |         0.00 |        0.00 |    15,384 |     1,066 |  3,173,681 |    291,735 |     34,382 |      1,197 |
| **remotely**     |        3.40 |        3.79 |         3.59 |        0.30 |       0.34 |        0.62 |       0.79 |         0.46 |        0.57 |  15,284.42 |   4,256.31 |    9,770.36 |        0.00 |       0.00 |        0.01 |       0.01 |         0.00 |        0.00 |     5,661 |     1,840 |  3,173,681 |    291,735 |     16,426 |      2,341 |
| **ever**         |        0.16 |        5.63 |         2.89 |        0.01 |       0.05 |        0.76 |       0.93 |         0.38 |        0.49 |     183.91 |  14,253.47 |    7,218.69 |        0.00 |       0.00 |        0.02 |       0.02 |         0.01 |        0.01 |     5,932 |     4,709 |  3,173,681 |    291,735 |    114,075 |      5,060 |
| **yet**          |        4.65 |        1.11 |         2.88 |        0.50 |       0.54 |        0.22 |       0.39 |         0.36 |        0.47 | 197,610.29 |     223.08 |   98,916.68 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    51,867 |       320 |  3,173,681 |    291,735 |     95,763 |        815 |
| **immediately**  |        4.86 |        0.84 |         2.85 |        0.54 |       0.58 |        0.17 |       0.34 |         0.35 |        0.46 | 224,058.80 |     191.87 |  112,125.34 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    56,099 |       403 |  3,173,681 |    291,735 |     96,973 |      1,195 |
| **particularly** |        1.38 |        3.43 |         2.40 |        0.06 |       0.11 |        0.54 |       0.71 |         0.30 |        0.41 |  37,272.26 |  18,583.63 |   27,927.95 |        0.01 |       0.02 |        0.03 |       0.03 |         0.02 |        0.02 |    55,527 |     9,243 |  3,173,681 |    291,735 |    513,668 |     13,003 |
| **terribly**     |        3.19 |        1.09 |         2.14 |        0.26 |       0.30 |        0.17 |       0.34 |         0.22 |        0.32 |  43,741.22 |     764.42 |   22,252.82 |        0.01 |       0.01 |        0.00 |       0.01 |         0.00 |        0.01 |    17,949 |     1,567 |  3,173,681 |    291,735 |     58,964 |      4,610 |
| **inherently**   |        1.75 |        2.40 |         2.07 |        0.10 |       0.14 |        0.39 |       0.56 |         0.24 |        0.35 |   7,021.95 |   3,925.26 |    5,473.60 |        0.00 |       0.00 |        0.01 |       0.01 |         0.00 |        0.01 |     6,743 |     2,864 |  3,173,681 |    291,735 |     47,803 |      5,133 |



## Save full adverb selection as `.csv`

Saving Combined "Most Negative Adverbs" AM table as csv:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-07-30.csv`



```python
save_prefix=f'{data_top}_NEG-ADV_combined-{SET_FLOOR}'
combined_top_csv_output = OUT_DIR / f'{save_prefix}.{timestamp_today()}.csv'
print('Saving Combined "Most Negative Adverbs" AM table as csv:  '
    f'\n> `{combined_top_csv_output}`')

C.to_csv(combined_top_csv_output, float_format='{:.4f}'.format)

C
```

Save `all-columns`, `means`, and `MAIN` as markdown formatted tables


```python
nb_show_table(C, suppress_printing=True,
    outpath=OUT_DIR.joinpath(
        f'{save_prefix}_all-columns_{timestamp_today()}.md')
)
nb_show_table(C[main_cols_ordered],
    outpath=OUT_DIR.joinpath(
        f'{save_prefix}_MAIN_{timestamp_today()}.md')
)
```


|                  |   `LRC_SET` |   `LRC_MIR` |   `mean_LRC` |   `dP1_SET` |   `P1_SET` |   `dP1_MIR` |   `P1_MIR` |   `mean_dP1` |   `mean_P1` |   `G2_SET` |   `G2_MIR` |   `mean_G2` |   `dP2_SET` |   `P2_SET` |   `dP2_MIR` |   `P2_MIR` |   `mean_dP2` |   `mean_P2` |   `f_SET` |   `f_MIR` |   `f1_SET` |   `f1_MIR` |   `f2_SET` |   `f2_MIR` |
|:-----------------|------------:|------------:|-------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|-----------:|-----------:|------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|----------:|----------:|-----------:|-----------:|-----------:|-----------:|
| **necessarily**  |        7.10 |        4.39 |         5.74 |        0.83 |       0.87 |        0.70 |       0.87 |         0.76 |        0.87 | 230,256.76 |   2,597.66 |  116,427.21 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    42,595 |       963 |  3,173,681 |    291,735 |     48,947 |      1,107 |
| **that**         |        6.34 |        3.90 |         5.12 |        0.75 |       0.79 |        0.61 |       0.78 |         0.68 |        0.79 | 831,134.96 |   9,957.28 |  420,546.12 |        0.05 |       0.05 |        0.01 |       0.01 |         0.03 |        0.03 |   164,768 |     4,308 |  3,173,681 |    291,735 |    208,262 |      5,494 |
| **exactly**      |        5.94 |        3.57 |         4.76 |        0.70 |       0.75 |        0.61 |       0.78 |         0.66 |        0.76 | 210,126.00 |   1,860.71 |  105,993.36 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    43,813 |       813 |  3,173,681 |    291,735 |     58,643 |      1,041 |
| **any**          |        4.07 |        4.65 |         4.36 |        0.40 |       0.45 |        0.72 |       0.89 |         0.56 |        0.67 |  50,880.76 |   2,985.73 |   26,933.25 |        0.00 |       0.00 |        0.00 |       0.00 |         0.00 |        0.00 |    15,384 |     1,066 |  3,173,681 |    291,735 |     34,382 |      1,197 |
| **remotely**     |        3.40 |        3.79 |         3.59 |        0.30 |       0.34 |        0.62 |       0.79 |         0.46 |        0.57 |  15,284.42 |   4,256.31 |    9,770.36 |        0.00 |       0.00 |        0.01 |       0.01 |         0.00 |        0.00 |     5,661 |     1,840 |  3,173,681 |    291,735 |     16,426 |      2,341 |
| **ever**         |        0.16 |        5.63 |         2.89 |        0.01 |       0.05 |        0.76 |       0.93 |         0.38 |        0.49 |     183.91 |  14,253.47 |    7,218.69 |        0.00 |       0.00 |        0.02 |       0.02 |         0.01 |        0.01 |     5,932 |     4,709 |  3,173,681 |    291,735 |    114,075 |      5,060 |
| **yet**          |        4.65 |        1.11 |         2.88 |        0.50 |       0.54 |        0.22 |       0.39 |         0.36 |        0.47 | 197,610.29 |     223.08 |   98,916.68 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    51,867 |       320 |  3,173,681 |    291,735 |     95,763 |        815 |
| **immediately**  |        4.86 |        0.84 |         2.85 |        0.54 |       0.58 |        0.17 |       0.34 |         0.35 |        0.46 | 224,058.80 |     191.87 |  112,125.34 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    56,099 |       403 |  3,173,681 |    291,735 |     96,973 |      1,195 |
| **particularly** |        1.38 |        3.43 |         2.40 |        0.06 |       0.11 |        0.54 |       0.71 |         0.30 |        0.41 |  37,272.26 |  18,583.63 |   27,927.95 |        0.01 |       0.02 |        0.03 |       0.03 |         0.02 |        0.02 |    55,527 |     9,243 |  3,173,681 |    291,735 |    513,668 |     13,003 |
| **terribly**     |        3.19 |        1.09 |         2.14 |        0.26 |       0.30 |        0.17 |       0.34 |         0.22 |        0.32 |  43,741.22 |     764.42 |   22,252.82 |        0.01 |       0.01 |        0.00 |       0.01 |         0.00 |        0.01 |    17,949 |     1,567 |  3,173,681 |    291,735 |     58,964 |      4,610 |
| **inherently**   |        1.75 |        2.40 |         2.07 |        0.10 |       0.14 |        0.39 |       0.56 |         0.24 |        0.35 |   7,021.95 |   3,925.26 |    5,473.60 |        0.00 |       0.00 |        0.01 |       0.01 |         0.00 |        0.01 |     6,743 |     2,864 |  3,173,681 |    291,735 |     47,803 |      5,133 |




```python
nb_show_table(C.filter(like='mean_'),
    outpath=OUT_DIR.joinpath(
        f'{save_prefix}_means_{timestamp_today()}.md')
)
```


|                  |   `mean_f` |   `mean_dP1` |   `mean_LRC` |   `mean_P1` |   `mean_G2` |    `mean_f1` |   `mean_f2` |      `mean_N` |   `mean_expF` |   `mean_unexpF` |   `mean_unexpR` |   `mean_oddsRDisc` |   `mean_t` |   `mean_MI` |   `mean_dP2` |   `mean_P2` |
|:-----------------|-----------:|-------------:|-------------:|------------:|------------:|-------------:|------------:|--------------:|--------------:|----------------:|----------------:|-------------------:|-----------:|------------:|-------------:|------------:|
| **necessarily**  | 593,171.33 |         0.76 |         5.74 |        0.87 |  116,427.21 | 1,732,708.00 |   25,027.00 | 37,270,750.00 |      1,161.21 |       20,617.79 |            0.88 |               1.84 |     110.48 |        1.00 |         0.01 |        0.01 |
| **that**         | 641,374.67 |         0.68 |         5.12 |        0.79 |  420,546.12 | 1,732,708.00 |  106,878.00 | 37,270,750.00 |      5,007.95 |       79,530.05 |            0.86 |               1.60 |     217.42 |        0.96 |         0.03 |        0.03 |
| **exactly**      | 594,954.33 |         0.66 |         4.76 |        0.76 |  105,993.36 | 1,732,708.00 |   29,842.00 | 37,270,750.00 |      1,366.78 |       20,946.22 |            0.86 |               1.53 |     109.68 |        0.95 |         0.01 |        0.01 |
| **any**          | 586,240.83 |         0.56 |         4.36 |        0.67 |   26,933.25 | 1,732,708.00 |   17,789.50 | 37,270,750.00 |        851.62 |        7,373.38 |            0.86 |               1.42 |      69.16 |        0.86 |         0.00 |        0.00 |
| **remotely**     | 581,947.33 |         0.46 |         3.59 |        0.57 |    9,770.36 | 1,732,708.00 |    9,383.50 | 37,270,750.00 |        558.49 |        3,192.01 |            0.83 |               1.16 |      49.63 |        0.78 |         0.00 |        0.00 |
| **ever**         | 599,198.67 |         0.38 |         2.89 |        0.49 |    7,218.69 | 1,732,708.00 |   59,567.50 | 37,270,750.00 |      2,918.85 |        2,401.65 |            0.49 |               0.95 |      34.23 |        0.41 |         0.01 |        0.01 |
| **yet**          | 602,363.50 |         0.36 |         2.88 |        0.47 |   98,916.68 | 1,732,708.00 |   48,289.00 | 37,270,750.00 |      2,156.09 |       23,937.41 |            0.74 |               0.96 |     109.75 |        0.73 |         0.01 |        0.01 |
| **immediately**  | 603,347.67 |         0.35 |         2.85 |        0.46 |  112,125.34 | 1,732,708.00 |   49,084.00 | 37,270,750.00 |      2,215.02 |       26,035.98 |            0.71 |               0.94 |     114.44 |        0.71 |         0.01 |        0.01 |
| **particularly** | 676,142.83 |         0.30 |         2.40 |        0.41 |   27,927.95 | 1,732,708.00 |  263,335.50 | 37,270,750.00 |     12,304.92 |       20,080.08 |            0.68 |               0.76 |     106.81 |        0.51 |         0.02 |        0.02 |
| **terribly**     | 591,417.67 |         0.22 |         2.14 |        0.32 |   22,252.82 | 1,732,708.00 |   31,787.00 | 37,270,750.00 |      1,679.67 |        8,078.33 |            0.68 |               0.69 |      67.21 |        0.57 |         0.00 |        0.01 |
| **inherently**   | 587,993.17 |         0.24 |         2.07 |        0.35 |    5,473.60 | 1,732,708.00 |   26,468.00 | 37,270,750.00 |      1,481.34 |        3,322.16 |            0.69 |               0.67 |      46.91 |        0.51 |         0.00 |        0.01 |


