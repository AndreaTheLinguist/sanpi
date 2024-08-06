# `ALL`: Identifying Adverbs with Strongest Negative Environment Associations


```python
from source.utils.associate import TOP_AM_DIR
from source.utils.general import confirm_dir

from am_notebooks import *

DATE=timestamp_today()
SET_FLOOR = 5000
# MIR_FLOOR = min(round(SET_FLOOR//15, -2), 500)
MIR_FLOOR = 500
K = 8

TAG='NEQ'
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
confirm_dir(TOP_AM_TAG_DIR)

data_top = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / data_top
confirm_dir(OUT_DIR)
METRIC_PRIORITIES = METRIC_PRIORITY_DICT[TAG]
METRIC_PRI_2 = METRIC_PRIORITIES[:2]
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
save_prefix=f'{data_top}_NEG-ADV_combined-{SET_FLOOR}'
combined_top_csv_output = OUT_DIR / f'{save_prefix}.{timestamp_today()}.csv'

# nb_show_table(pd.DataFrame(parameters, dtype='string').T)
```


|                 | `value`                                                       | `description`                                         |
|:----------------|:--------------------------------------------------------------|:------------------------------------------------------|
| **`SET_FLOOR`** | $5,000$                                                       | *_`*direct` superset minimum `env~adv` co-occurence_* |
| **`MIR_FLOOR`** | $500$                                                         | *_`*mirror` subset minimum `env~adv` co-occurence_*   |
| **`TAG`**       | `"NEQ"`                                                       | *_frequency data evaluated_*                          |
| **`K`**         | $8$                                                           | *_# top adverbs sought_*                              |
| **`OUT_DIR`**   | `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/` | *_output directory_*                                  |
| **`DATE`**      | 2024-08-05                                                    | *_date of processing_*                                |



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
                                         mirror_floor=MIR_FLOOR, 
                                         data_tag=TAG)
except Exception:
    MIR_FLOOR = 100
    adv_am_paths = locate_polar_am_paths(superset_floor=SET_FLOOR,
                                         mirror_floor=MIR_FLOOR, 
                                         data_tag=TAG)

setdiff_adv = adjust_am_names(filter_load_adx_am(adv_am_paths['RBdirect'], column_list=FOCUS))
mirror_adv = adjust_am_names(filter_load_adx_am(adv_am_paths['mirror'], column_list=FOCUS))
```

    {'RBdirect': '*NEQ*min5000x*parq', 'mirror': '*NEQ*min500x*parq'}
    ╒══════════╤══════════════════════════════════════════════════════════════════════════╕
    │          │ path to selected AM dataframe                                            │
    ╞══════════╪══════════════════════════════════════════════════════════════════════════╡
    │ RBdirect │ /share/compling/projects/sanpi/results/assoc_df/polar/RBdirect/adv/extra │
    │          │ /polarized-adv_NEQ-direct_min5000x_extra.parq                            │
    ├──────────┼──────────────────────────────────────────────────────────────────────────┤
    │ mirror   │ /share/compling/projects/sanpi/results/assoc_df/polar/mirror/adv/extra/p │
    │          │ olarized-adv_NEQ-mirror_min500x_extra.parq                               │
    ╘══════════╧══════════════════════════════════════════════════════════════════════════╛



```python
# print(r'### Sample of Superset `RBdirect` $*E\sim\texttt{adv}$ AMs', 
#       f'With $f\geq{SET_FLOOR:,}$ (i.e. `adv` occurs in given environment at least {SET_FLOOR:,} times)',
#       sep='\n\n', end = '\n\n')
# nb_show_table(setdiff_adv.sample(min(6,K)).sort_values('unexp_r', ascending=False))
```

### Sample of Superset `RBdirect` $*E\sim\texttt{adv}$ AMs

With $f\geq5,000$ (i.e. `adv` occurs in given environment at least 5,000 times)


|                    |     `f` |   `dP1` |   `LRC` |   `P1` |        `G2` | `l1`       | `l2`       |      `f1` |    `f2` |       `N` |    `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `odds_r_disc` |       `t` |   `MI` |
|:-------------------|--------:|--------:|--------:|-------:|------------:|:-----------|:-----------|----------:|--------:|----------:|-----------:|------------:|------------:|--------:|-------:|----------------:|----------:|-------:|
| **COM~relatively** |  26,629 |    0.49 |    5.98 |   0.99 |   34,010.20 | COMPLEMENT | relatively | 3,173,681 |  26,947 | 6,347,362 |  13,473.50 |   13,155.50 |        0.49 |    0.01 |   0.01 |            1.93 |     80.62 |   0.30 |
| **COM~slightly**   |  17,168 |    0.45 |    3.87 |   0.95 |   17,506.37 | COMPLEMENT | slightly   | 3,173,681 |  18,163 | 6,347,362 |   9,081.50 |    8,086.50 |        0.47 |    0.01 |   0.01 |            1.24 |     61.72 |   0.28 |
| **COM~more**       | 391,566 |    0.23 |    1.25 |   0.71 |  107,332.79 | COMPLEMENT | more       | 3,173,681 | 553,482 | 6,347,362 | 276,741.00 |  114,825.00 |        0.29 |    0.07 |   0.12 |            0.42 |    183.50 |   0.15 |
| **COM~much**       |  78,823 |    0.10 |    0.53 |   0.60 |    5,188.88 | COMPLEMENT | much       | 3,173,681 | 131,845 | 6,347,362 |  65,922.50 |   12,900.50 |        0.16 |    0.01 |   0.02 |            0.18 |     45.95 |   0.08 |
| **NEGany~really**  |  97,510 |    0.03 |    0.16 |   0.53 |      818.00 | NEGATED    | really     | 3,173,681 | 182,968 | 6,347,362 |  91,484.00 |    6,026.00 |        0.06 |    0.00 |   0.03 |            0.06 |     19.30 |   0.03 |
| **NEGany~most**    |  19,204 |   -0.47 |   -4.04 |   0.06 | -348,424.97 | NEGATED    | most       | 3,173,681 | 346,992 | 6,347,362 | 173,496.00 | -154,292.00 |       -8.03 |   -0.10 |   0.01 |           -1.28 | -1,113.39 |  -0.96 |




```python
# print(r'### Sample of Subset `mirror` $@E\sim\texttt{adv}$ AMs', 
#       f'With $f\geq{MIR_FLOOR:,}$ (i.e. `adv` occurs in given environment at least {MIR_FLOOR:,} times)',
#       sep='\n\n', end = '\n\n')
# nb_show_table(mirror_adv.sample(min(6,K)).sort_values('unexp_r', ascending=False))
```

### Sample of Subset `mirror` $@E\sim\texttt{adv}$ AMs

With $f\geq500$ (i.e. `adv` occurs in given environment at least 500 times)


|                         |    `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`   | `l2`         |    `f1` |   `f2` |     `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `odds_r_disc` |   `t` |   `MI` |
|:------------------------|-------:|--------:|--------:|-------:|---------:|:-------|:-------------|--------:|-------:|--------:|----------:|------------:|------------:|--------:|-------:|----------------:|------:|-------:|
| **POS~deeply**          |  1,008 |    0.42 |    2.84 |   0.92 |   926.78 | POSMIR | deeply       | 291,735 |  1,091 | 583,470 |    545.50 |      462.50 |        0.46 |    0.00 |   0.00 |            1.08 | 14.57 |   0.27 |
| **NEGmir~particularly** |  9,243 |    0.43 |    3.31 |   0.92 | 8,550.11 | NEGMIR | particularly | 291,735 | 10,020 | 583,470 |  5,010.00 |    4,233.00 |        0.46 |    0.03 |   0.03 |            1.09 | 44.03 |   0.27 |
| **POS~now**             |  1,157 |    0.38 |    2.29 |   0.88 |   858.88 | POSMIR | now          | 291,735 |  1,315 | 583,470 |    657.50 |      499.50 |        0.43 |    0.00 |   0.00 |            0.86 | 14.68 |   0.25 |
| **NEGmir~too**          | 46,648 |    0.19 |    0.95 |   0.67 | 9,099.99 | NEGMIR | too          | 291,735 | 69,845 | 583,470 | 34,922.50 |   11,725.50 |        0.25 |    0.08 |   0.16 |            0.34 | 54.29 |   0.13 |
| **POS~seriously**       |    695 |    0.12 |    0.26 |   0.62 |    64.22 | POSMIR | seriously    | 291,735 |  1,123 | 583,470 |    561.50 |      133.50 |        0.19 |    0.00 |   0.00 |            0.21 |  5.06 |   0.09 |
| **NEGmir~truly**        |  2,824 |    0.06 |    0.13 |   0.56 |    65.89 | NEGMIR | truly        | 291,735 |  5,073 | 583,470 |  2,536.50 |      287.50 |        0.10 |    0.00 |   0.01 |            0.10 |  5.41 |   0.05 |



## Calculate "Most Negative" Adverbs for each Polarity Approximation


```python
# md_frame_code('''nb_show_table(
#     pd.concat([setdiff_adv.filter(METRIC_PRI_2).sample(5),
#                mirror_adv.filter(METRIC_PRI_2).sample(5)]))''')
# nb_show_table(
#     pd.concat([setdiff_adv.filter(METRIC_PRI_2).sample(5),
#                mirror_adv.filter(METRIC_PRI_2).sample(5)]))
```


```python
nb_show_table(
    pd.concat([setdiff_adv.filter(METRIC_PRI_2).sample(5),
               mirror_adv.filter(METRIC_PRI_2).sample(5)]))
```


|                   |   `LRC` |   `P1` |
|:------------------|--------:|-------:|
| **COM~almost**    |    5.30 |   0.98 |
| **COM~highly**    |    3.64 |   0.93 |
| **NEGany~that**   |    6.26 |   0.99 |
| **NEGany~yet**    |    4.59 |   0.96 |
| **NEGany~super**  |   -0.40 |   0.41 |
| **NEGmir~that**   |    3.76 |   0.95 |
| **POS~seriously** |    0.26 |   0.62 |
| **POS~easily**    |    0.83 |   0.72 |
| **POS~much**      |    0.87 |   0.67 |
| **POS~even**      |    1.95 |   0.81 |




```python
def show_top_any_env(adv_df:pd.DataFrame, save_path:Path, k:int=10) -> None:
    _top = get_top_vals(adjust_am_names(adv_df),
                 k=k, index_like=None, 
                 metric_filter=METRIC_PRI_2)
    
    is_super =  'COMPLEMENT' in adv_df.l1.unique()
    print(f'### {k} Most Strongly Associated Environment~Adverb Pairs for {TAG} _{"superset" if is_super else "mirror subset"}_ data\n',
        ('_Absent Negative_' if is_super else '_Present Positive_')+ ' approximation',
        f'ranked by {" & ".join([f"`{m}`" for m in METRIC_PRI_2])}', 
        sep='\n+ ')
    nb_show_table(_top.reset_index()
              .filter(items = ['key','adv','l1'] + adjust_am_names(FOCUS))
              .sort_values(METRIC_PRI_2, ascending=False), outpath=save_path)
    print(f'\n> saved as:  \n> `{save_path}`\n')
            #   results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_POS-ADV_combined-5000.2024-08-05.csv
    
# for adv_df in (setdiff_adv, mirror_adv):
#     category='super' if 'COMPLEMENT' in adv_df.l1.unique() else 'mirror'
#     show_top_any_env(adjust_am_names(adv_df).filter(adjust_am_names(FOCUS)), 
#                      save_path=combined_top_csv_output.with_name(
#                          combined_top_csv_output.name.replace('NEG', 'ANY')
#                          .replace('combined', category)))
```

### 10 Most Strongly Associated Environment~Adverb Pairs for NEQ _superset_ data

+ _Absent Negative_ approximation
+ ranked by `LRC` & `P1`

|        | `key`              | `l1`       |     `f` |   `dP1` |   `LRC` |   `P1` |       `G2` | `l2`         |      `f1` |    `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |
|:-------|:-------------------|:-----------|--------:|--------:|--------:|-------:|-----------:|:-------------|----------:|--------:|----------:|----------:|------------:|------------:|----------------:|-------:|-------:|
| **1**  | COM~increasingly   | COMPLEMENT |  17,139 |    0.50 |    7.07 |   1.00 |  22,963.63 | increasingly | 3,173,681 |  17,212 | 6,347,362 |  8,606.00 |    8,533.00 |        0.50 |            2.37 |  65.18 |   0.30 |
| **2**  | NEGany~necessarily | NEGATED    |  42,595 |    0.50 |    6.65 |   0.99 |  55,995.13 | necessarily  | 3,173,681 |  42,916 | 6,347,362 | 21,458.00 |   21,137.00 |        0.50 |            2.13 | 102.42 |   0.30 |
| **3**  | NEGany~that        | NEGATED    | 164,768 |    0.50 |    6.26 |   0.99 | 214,471.83 | that         | 3,173,681 | 166,680 | 6,347,362 | 83,340.00 |   81,428.00 |        0.49 |            1.96 | 200.60 |   0.30 |
| **4**  | COM~relatively     | COMPLEMENT |  26,629 |    0.49 |    5.98 |   0.99 |  34,010.20 | relatively   | 3,173,681 |  26,947 | 6,347,362 | 13,473.50 |   13,155.50 |        0.49 |            1.93 |  80.62 |   0.30 |
| **5**  | NEGany~exactly     | NEGATED    |  43,813 |    0.49 |    5.97 |   0.99 |  55,763.99 | exactly      | 3,173,681 |  44,378 | 6,347,362 | 22,189.00 |   21,624.00 |        0.49 |            1.90 | 103.31 |   0.30 |
| **6**  | COM~almost         | COMPLEMENT |  20,201 |    0.48 |    5.30 |   0.98 |  24,695.07 | almost       | 3,173,681 |  20,598 | 6,347,362 | 10,299.00 |    9,902.00 |        0.49 |            1.71 |  69.67 |   0.29 |
| **7**  | COM~mostly         | COMPLEMENT |   9,180 |    0.48 |    5.12 |   0.98 |  11,190.02 | mostly       | 3,173,681 |   9,363 | 6,347,362 |  4,681.50 |    4,498.50 |        0.49 |            1.70 |  46.95 |   0.29 |
| **8**  | COM~seemingly      | COMPLEMENT |   7,422 |    0.48 |    5.07 |   0.98 |   9,051.32 | seemingly    | 3,173,681 |   7,569 | 6,347,362 |  3,784.50 |    3,637.50 |        0.49 |            1.70 |  42.22 |   0.29 |
| **9**  | COM~fairly         | COMPLEMENT |  17,263 |    0.48 |    5.01 |   0.98 |  20,605.35 | fairly       | 3,173,681 |  17,680 | 6,347,362 |  8,840.00 |    8,423.00 |        0.49 |            1.62 |  64.11 |   0.29 |
| **10** | COM~pretty         | COMPLEMENT |  69,603 |    0.48 |    4.98 |   0.97 |  81,991.26 | pretty       | 3,173,681 |  71,559 | 6,347,362 | 35,779.50 |   33,823.50 |        0.49 |            1.56 | 128.20 |   0.29 |
| **11** | COM~largely        | COMPLEMENT |   8,012 |    0.48 |    4.91 |   0.98 |   9,604.59 | largely      | 3,173,681 |   8,197 | 6,347,362 |  4,098.50 |    3,913.50 |        0.49 |            1.64 |  43.72 |   0.29 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_ANY-ADV_super-5000.2024-08-05.csv`

### 10 Most Strongly Associated Environment~Adverb Pairs for NEQ _mirror subset_ data

+ _Present Positive_ approximation
+ ranked by `LRC` & `P1`

|        | `key`         | `l1`   |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l2`      |    `f1` |   `f2` |     `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |
|:-------|:--------------|:-------|------:|--------:|--------:|-------:|---------:|:----------|--------:|-------:|--------:|----------:|------------:|------------:|----------------:|------:|-------:|
| **1**  | NEGmir~ever   | NEGMIR | 4,709 |    0.49 |    5.32 |   0.99 | 5,953.39 | ever      | 291,735 |  4,776 | 583,470 |  2,388.00 |    2,321.00 |        0.49 |            1.85 | 33.82 |   0.29 |
| **2**  | POS~pretty    | POSMIR | 5,123 |    0.48 |    4.73 |   0.98 | 6,124.97 | pretty    | 291,735 |  5,250 | 583,470 |  2,625.00 |    2,498.00 |        0.49 |            1.61 | 34.90 |   0.29 |
| **3**  | POS~rather    | POSMIR | 1,774 |    0.48 |    4.66 |   0.98 | 2,187.31 | rather    | 291,735 |  1,806 | 583,470 |    903.00 |      871.00 |        0.49 |            1.74 | 20.68 |   0.29 |
| **4**  | NEGmir~any    | NEGMIR | 1,066 |    0.49 |    4.48 |   0.98 | 1,328.27 | any       | 291,735 |  1,083 | 583,470 |    541.50 |      524.50 |        0.49 |            1.79 | 16.06 |   0.29 |
| **5**  | POS~plain     | POSMIR | 1,051 |    0.48 |    4.45 |   0.98 | 1,307.90 | plain     | 291,735 |  1,068 | 583,470 |    534.00 |      517.00 |        0.49 |            1.78 | 15.95 |   0.29 |
| **6**  | POS~fairly    | POSMIR | 1,185 |    0.48 |    4.33 |   0.98 | 1,442.69 | fairly    | 291,735 |  1,209 | 583,470 |    604.50 |      580.50 |        0.49 |            1.69 | 16.86 |   0.29 |
| **7**  | POS~somewhat  | POSMIR |   914 |    0.48 |    4.30 |   0.98 | 1,128.91 | somewhat  | 291,735 |    930 | 583,470 |    465.00 |      449.00 |        0.49 |            1.75 | 14.85 |   0.29 |
| **8**  | POS~otherwise | POSMIR | 1,418 |    0.47 |    4.06 |   0.97 | 1,646.39 | otherwise | 291,735 |  1,460 | 583,470 |    730.00 |      688.00 |        0.49 |            1.53 | 18.27 |   0.29 |
| **9**  | POS~maybe     | POSMIR |   546 |    0.48 |    3.97 |   0.98 |   677.84 | maybe     | 291,735 |    555 | 583,470 |    277.50 |      268.50 |        0.49 |            1.76 | 11.49 |   0.29 |
| **10** | NEGmir~longer | NEGMIR |   821 |    0.48 |    3.96 |   0.98 |   977.90 | longer    | 291,735 |    841 | 583,470 |    420.50 |      400.50 |        0.49 |            1.60 | 13.98 |   0.29 |
| **11** | POS~downright | POSMIR |   981 |    0.47 |    3.88 |   0.97 | 1,138.63 | downright | 291,735 |  1,010 | 583,470 |    505.00 |      476.00 |        0.49 |            1.52 | 15.20 |   0.29 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_ANY-ADV_mirror-5000.2024-08-05.csv`




```python
    
[setdiff_top15, mirror_top15] = [
    get_top_vals(adjust_am_names(adv_df),
                 k=15, index_like=None, 
                 metric_filter=METRIC_PRI_2)
    .assign(adv=adv_df.l2)
    for adv_df in (setdiff_adv, mirror_adv)
]
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

|        | `adv`        |     `f` |   `dP1` |   `LRC` |   `P1` |       `G2` |      `f1` |    `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |
|:-------|:-------------|--------:|--------:|--------:|-------:|-----------:|----------:|--------:|----------:|----------:|------------:|------------:|----------------:|-------:|-------:|
| **1**  | increasingly |  17,139 |    0.50 |    7.07 |   1.00 |  22,963.63 | 3,173,681 |  17,212 | 6,347,362 |  8,606.00 |    8,533.00 |        0.50 |            2.37 |  65.18 |   0.30 |
| **2**  | necessarily  |  42,595 |    0.50 |    6.65 |   0.99 |  55,995.13 | 3,173,681 |  42,916 | 6,347,362 | 21,458.00 |   21,137.00 |        0.50 |            2.13 | 102.42 |   0.30 |
| **3**  | that         | 164,768 |    0.50 |    6.26 |   0.99 | 214,471.83 | 3,173,681 | 166,680 | 6,347,362 | 83,340.00 |   81,428.00 |        0.49 |            1.96 | 200.60 |   0.30 |
| **4**  | relatively   |  26,629 |    0.49 |    5.98 |   0.99 |  34,010.20 | 3,173,681 |  26,947 | 6,347,362 | 13,473.50 |   13,155.50 |        0.49 |            1.93 |  80.62 |   0.30 |
| **5**  | exactly      |  43,813 |    0.49 |    5.97 |   0.99 |  55,763.99 | 3,173,681 |  44,378 | 6,347,362 | 22,189.00 |   21,624.00 |        0.49 |            1.90 | 103.31 |   0.30 |
| **6**  | almost       |  20,201 |    0.48 |    5.30 |   0.98 |  24,695.07 | 3,173,681 |  20,598 | 6,347,362 | 10,299.00 |    9,902.00 |        0.49 |            1.71 |  69.67 |   0.29 |
| **7**  | mostly       |   9,180 |    0.48 |    5.12 |   0.98 |  11,190.02 | 3,173,681 |   9,363 | 6,347,362 |  4,681.50 |    4,498.50 |        0.49 |            1.70 |  46.95 |   0.29 |
| **8**  | seemingly    |   7,422 |    0.48 |    5.07 |   0.98 |   9,051.32 | 3,173,681 |   7,569 | 6,347,362 |  3,784.50 |    3,637.50 |        0.49 |            1.70 |  42.22 |   0.29 |
| **9**  | fairly       |  17,263 |    0.48 |    5.01 |   0.98 |  20,605.35 | 3,173,681 |  17,680 | 6,347,362 |  8,840.00 |    8,423.00 |        0.49 |            1.62 |  64.11 |   0.29 |
| **10** | pretty       |  69,603 |    0.48 |    4.98 |   0.97 |  81,991.26 | 3,173,681 |  71,559 | 6,347,362 | 35,779.50 |   33,823.50 |        0.49 |            1.56 | 128.20 |   0.29 |
| **11** | immediately  |  56,099 |    0.48 |    4.92 |   0.97 |  65,652.79 | 3,173,681 |  57,730 | 6,347,362 | 28,865.00 |   27,234.00 |        0.49 |            1.54 | 114.98 |   0.29 |
| **12** | largely      |   8,012 |    0.48 |    4.91 |   0.98 |   9,604.59 | 3,173,681 |   8,197 | 6,347,362 |  4,098.50 |    3,913.50 |        0.49 |            1.64 |  43.72 |   0.29 |
| **13** | rather       |  16,678 |    0.47 |    4.76 |   0.97 |  19,395.88 | 3,173,681 |  17,167 | 6,347,362 |  8,583.50 |    8,094.50 |        0.49 |            1.53 |  62.68 |   0.29 |
| **14** | sometimes    |   6,623 |    0.47 |    4.61 |   0.97 |   7,722.24 | 3,173,681 |   6,812 | 6,347,362 |  3,406.00 |    3,217.00 |        0.49 |            1.54 |  39.53 |   0.29 |
| **15** | yet          |  51,867 |    0.47 |    4.59 |   0.96 |  58,435.17 | 3,173,681 |  53,779 | 6,347,362 | 26,889.50 |   24,977.50 |        0.48 |            1.44 | 109.67 |   0.29 |




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

|        | `adv`       |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` |    `f1` |   `f2` |     `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |
|:-------|:------------|------:|--------:|--------:|-------:|---------:|--------:|-------:|--------:|----------:|------------:|------------:|----------------:|------:|-------:|
| **1**  | ever        | 4,709 |    0.49 |    5.32 |   0.99 | 5,953.39 | 291,735 |  4,776 | 583,470 |  2,388.00 |    2,321.00 |        0.49 |            1.85 | 33.82 |   0.29 |
| **2**  | pretty      | 5,123 |    0.48 |    4.73 |   0.98 | 6,124.97 | 291,735 |  5,250 | 583,470 |  2,625.00 |    2,498.00 |        0.49 |            1.61 | 34.90 |   0.29 |
| **3**  | rather      | 1,774 |    0.48 |    4.66 |   0.98 | 2,187.31 | 291,735 |  1,806 | 583,470 |    903.00 |      871.00 |        0.49 |            1.74 | 20.68 |   0.29 |
| **4**  | any         | 1,066 |    0.49 |    4.48 |   0.98 | 1,328.27 | 291,735 |  1,083 | 583,470 |    541.50 |      524.50 |        0.49 |            1.79 | 16.06 |   0.29 |
| **5**  | plain       | 1,051 |    0.48 |    4.45 |   0.98 | 1,307.90 | 291,735 |  1,068 | 583,470 |    534.00 |      517.00 |        0.49 |            1.78 | 15.95 |   0.29 |
| **6**  | fairly      | 1,185 |    0.48 |    4.33 |   0.98 | 1,442.69 | 291,735 |  1,209 | 583,470 |    604.50 |      580.50 |        0.49 |            1.69 | 16.86 |   0.29 |
| **7**  | somewhat    |   914 |    0.48 |    4.30 |   0.98 | 1,128.91 | 291,735 |    930 | 583,470 |    465.00 |      449.00 |        0.49 |            1.75 | 14.85 |   0.29 |
| **8**  | otherwise   | 1,418 |    0.47 |    4.06 |   0.97 | 1,646.39 | 291,735 |  1,460 | 583,470 |    730.00 |      688.00 |        0.49 |            1.53 | 18.27 |   0.29 |
| **9**  | maybe       |   546 |    0.48 |    3.97 |   0.98 |   677.84 | 291,735 |    555 | 583,470 |    277.50 |      268.50 |        0.49 |            1.76 | 11.49 |   0.29 |
| **10** | longer      |   821 |    0.48 |    3.96 |   0.98 |   977.90 | 291,735 |    841 | 583,470 |    420.50 |      400.50 |        0.49 |            1.60 | 13.98 |   0.29 |
| **11** | downright   |   981 |    0.47 |    3.88 |   0.97 | 1,138.63 | 291,735 |  1,010 | 583,470 |    505.00 |      476.00 |        0.49 |            1.52 | 15.20 |   0.29 |
| **12** | relatively  | 1,142 |    0.47 |    3.85 |   0.97 | 1,302.05 | 291,735 |  1,180 | 583,470 |    590.00 |      552.00 |        0.48 |            1.47 | 16.33 |   0.29 |
| **13** | necessarily |   963 |    0.47 |    3.82 |   0.97 | 1,109.03 | 291,735 |    993 | 583,470 |    496.50 |      466.50 |        0.48 |            1.50 | 15.03 |   0.29 |
| **14** | already     |   885 |    0.47 |    3.80 |   0.97 | 1,022.30 | 291,735 |    912 | 583,470 |    456.00 |      429.00 |        0.48 |            1.51 | 14.42 |   0.29 |
| **15** | that        | 4,308 |    0.45 |    3.76 |   0.95 | 4,499.79 | 291,735 |  4,538 | 583,470 |  2,269.00 |    2,039.00 |        0.47 |            1.28 | 31.07 |   0.28 |
| **16** | perhaps     |   760 |    0.47 |    3.57 |   0.97 |   856.76 | 291,735 |    787 | 583,470 |    393.50 |      366.50 |        0.48 |            1.44 | 13.29 |   0.29 |




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

    * Total unique mirror adv where LRC >= 1 and f > 500
    
    l1        adv subtotal
    ------  --------------
    POSMIR              31
    NEGMIR              12
    
    ┌─────────────────────┬──────────────┬───────┬───────┬──────┬──────────┬──────┐
    │ key                 │ l2           │     f │   LRC │   P1 │       G2 │   P2 │
    ├─────────────────────┼──────────────┼───────┼───────┼──────┼──────────┼──────┤
    │ NEGmir~not          │ not          │ 1,404 │  6.56 │ 1.00 │ 1,949.74 │ 0.00 │
    │ NEGmir~ever         │ ever         │ 4,709 │  5.32 │ 0.99 │ 5,953.39 │ 0.02 │
    │ NEGmir~any          │ any          │ 1,066 │  4.48 │ 0.98 │ 1,328.27 │ 0.00 │
    │ NEGmir~longer       │ longer       │   821 │  3.96 │ 0.98 │   977.90 │ 0.00 │
    │ NEGmir~necessarily  │ necessarily  │   963 │  3.82 │ 0.97 │ 1,109.03 │ 0.00 │
    │ NEGmir~that         │ that         │ 4,308 │  3.76 │ 0.95 │ 4,499.79 │ 0.01 │
    │ NEGmir~particularly │ particularly │ 9,243 │  3.31 │ 0.92 │ 8,550.11 │ 0.03 │
    │ NEGmir~remotely     │ remotely     │ 1,840 │  3.27 │ 0.94 │ 1,806.81 │ 0.01 │
    │ NEGmir~exactly      │ exactly      │   813 │  3.09 │ 0.94 │   819.82 │ 0.00 │
    │ NEGmir~inherently   │ inherently   │ 2,864 │  2.24 │ 0.86 │ 1,897.04 │ 0.01 │
    │ NEGmir~especially   │ especially   │ 1,569 │  1.32 │ 0.76 │   601.15 │ 0.01 │
    │ NEGmir~fully        │ fully        │ 1,664 │  1.06 │ 0.72 │   477.96 │ 0.01 │
    └─────────────────────┴──────────────┴───────┴───────┴──────┴──────────┴──────┘


### Or here, the least "negative"/most "non-negative"


```python
# show_top_positive(setdiff_adv, k=15, data_tag=TAG, filter_and_sort=METRIC_PRI_2, 
#                   save_path =combined_top_csv_output.with_name(
#                          combined_top_csv_output.name.replace('NEG', 'POS')
#                          .replace('combined', 'super')))
```

#### Top 15 Adverbs in *Complement* Polarity Environment (`set_diff`, $*\complement_{N^+}$)

> ranked by `['LRC', 'P1']`

**Total Tokens in dataset**: $N = 6,347,362$

|                  |   `LRC` |   `P1` |    `f` |   `dP1` |      `G2` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |
|:-----------------|--------:|-------:|-------:|--------:|----------:|----------:|-------:|----------:|------------:|------------:|----------------:|-------:|-------:|
| **increasingly** |    7.07 |   1.00 | 17,139 |    0.50 | 22,963.63 | 3,173,681 | 17,212 |  8,606.00 |    8,533.00 |        0.50 |            2.37 |  65.18 |   0.30 |
| **relatively**   |    5.98 |   0.99 | 26,629 |    0.49 | 34,010.20 | 3,173,681 | 26,947 | 13,473.50 |   13,155.50 |        0.49 |            1.93 |  80.62 |   0.30 |
| **almost**       |    5.30 |   0.98 | 20,201 |    0.48 | 24,695.07 | 3,173,681 | 20,598 | 10,299.00 |    9,902.00 |        0.49 |            1.71 |  69.67 |   0.29 |
| **mostly**       |    5.12 |   0.98 |  9,180 |    0.48 | 11,190.02 | 3,173,681 |  9,363 |  4,681.50 |    4,498.50 |        0.49 |            1.70 |  46.95 |   0.29 |
| **seemingly**    |    5.07 |   0.98 |  7,422 |    0.48 |  9,051.32 | 3,173,681 |  7,569 |  3,784.50 |    3,637.50 |        0.49 |            1.70 |  42.22 |   0.29 |
| **fairly**       |    5.01 |   0.98 | 17,263 |    0.48 | 20,605.35 | 3,173,681 | 17,680 |  8,840.00 |    8,423.00 |        0.49 |            1.62 |  64.11 |   0.29 |
| **pretty**       |    4.98 |   0.97 | 69,603 |    0.48 | 81,991.26 | 3,173,681 | 71,559 | 35,779.50 |   33,823.50 |        0.49 |            1.56 | 128.20 |   0.29 |
| **largely**      |    4.91 |   0.98 |  8,012 |    0.48 |  9,604.59 | 3,173,681 |  8,197 |  4,098.50 |    3,913.50 |        0.49 |            1.64 |  43.72 |   0.29 |
| **rather**       |    4.76 |   0.97 | 16,678 |    0.47 | 19,395.88 | 3,173,681 | 17,167 |  8,583.50 |    8,094.50 |        0.49 |            1.53 |  62.68 |   0.29 |
| **sometimes**    |    4.61 |   0.97 |  6,623 |    0.47 |  7,722.24 | 3,173,681 |  6,812 |  3,406.00 |    3,217.00 |        0.49 |            1.54 |  39.53 |   0.29 |
| **also**         |    4.47 |   0.96 | 49,082 |    0.47 | 54,459.24 | 3,173,681 | 51,048 | 25,524.00 |   23,558.00 |        0.48 |            1.40 | 106.34 |   0.28 |
| **now**          |    4.28 |   0.96 | 19,714 |    0.46 | 21,473.35 | 3,173,681 | 20,566 | 10,283.00 |    9,431.00 |        0.48 |            1.37 |  67.17 |   0.28 |
| **probably**     |    4.14 |   0.96 |  5,739 |    0.46 |  6,310.23 | 3,173,681 |  5,973 |  2,986.50 |    2,752.50 |        0.48 |            1.39 |  36.33 |   0.28 |
| **somewhat**     |    4.12 |   0.96 | 13,119 |    0.46 | 14,041.62 | 3,173,681 | 13,734 |  6,867.00 |    6,252.00 |        0.48 |            1.33 |  54.58 |   0.28 |
| **potentially**  |    4.06 |   0.96 |  8,695 |    0.46 |  9,323.27 | 3,173,681 |  9,098 |  4,549.00 |    4,146.00 |        0.48 |            1.33 |  44.46 |   0.28 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_POS-ADV_super-5000.2024-08-05.csv`




```python
# Mirror Data ~ explicitly positive ~ positive trigger present
# show_top_positive(mirror_adv, k=15, data_tag=TAG, filter_and_sort=METRIC_PRI_2, 
#                   save_path =combined_top_csv_output.with_name(
#                          combined_top_csv_output.name.replace('NEG', 'POS')
#                          .replace('combined', 'mirror')))
```

#### Top 15 Adverbs in *Posmir* Polarity Environment (`mirror`, $@P$)

> ranked by `['LRC', 'P1']`

**Total Tokens in dataset**: $N = 583,470$

|                |   `LRC` |   `P1` |   `f` |   `dP1` |     `G2` |    `f1` |   `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |
|:---------------|--------:|-------:|------:|--------:|---------:|--------:|-------:|----------:|------------:|------------:|----------------:|------:|-------:|
| **pretty**     |    4.73 |   0.98 | 5,123 |    0.48 | 6,124.97 | 291,735 |  5,250 |  2,625.00 |    2,498.00 |        0.49 |            1.61 | 34.90 |   0.29 |
| **rather**     |    4.66 |   0.98 | 1,774 |    0.48 | 2,187.31 | 291,735 |  1,806 |    903.00 |      871.00 |        0.49 |            1.74 | 20.68 |   0.29 |
| **plain**      |    4.45 |   0.98 | 1,051 |    0.48 | 1,307.90 | 291,735 |  1,068 |    534.00 |      517.00 |        0.49 |            1.78 | 15.95 |   0.29 |
| **fairly**     |    4.33 |   0.98 | 1,185 |    0.48 | 1,442.69 | 291,735 |  1,209 |    604.50 |      580.50 |        0.49 |            1.69 | 16.86 |   0.29 |
| **somewhat**   |    4.30 |   0.98 |   914 |    0.48 | 1,128.91 | 291,735 |    930 |    465.00 |      449.00 |        0.49 |            1.75 | 14.85 |   0.29 |
| **otherwise**  |    4.06 |   0.97 | 1,418 |    0.47 | 1,646.39 | 291,735 |  1,460 |    730.00 |      688.00 |        0.49 |            1.53 | 18.27 |   0.29 |
| **maybe**      |    3.97 |   0.98 |   546 |    0.48 |   677.84 | 291,735 |    555 |    277.50 |      268.50 |        0.49 |            1.76 | 11.49 |   0.29 |
| **downright**  |    3.88 |   0.97 |   981 |    0.47 | 1,138.63 | 291,735 |  1,010 |    505.00 |      476.00 |        0.49 |            1.52 | 15.20 |   0.29 |
| **relatively** |    3.85 |   0.97 | 1,142 |    0.47 | 1,302.05 | 291,735 |  1,180 |    590.00 |      552.00 |        0.48 |            1.47 | 16.33 |   0.29 |
| **already**    |    3.80 |   0.97 |   885 |    0.47 | 1,022.30 | 291,735 |    912 |    456.00 |      429.00 |        0.48 |            1.51 | 14.42 |   0.29 |
| **almost**     |    3.67 |   0.96 | 1,068 |    0.46 | 1,188.34 | 291,735 |  1,109 |    554.50 |      513.50 |        0.48 |            1.41 | 15.71 |   0.28 |
| **equally**    |    3.58 |   0.95 | 1,512 |    0.46 | 1,608.88 | 291,735 |  1,585 |    792.50 |      719.50 |        0.48 |            1.32 | 18.50 |   0.28 |
| **perhaps**    |    3.57 |   0.97 |   760 |    0.47 |   856.76 | 291,735 |    787 |    393.50 |      366.50 |        0.48 |            1.44 | 13.29 |   0.29 |
| **slightly**   |    3.31 |   0.94 | 1,675 |    0.44 | 1,669.50 | 291,735 |  1,781 |    890.50 |      784.50 |        0.47 |            1.20 | 19.17 |   0.27 |
| **highly**     |    3.27 |   0.94 | 1,915 |    0.44 | 1,872.44 | 291,735 |  2,045 |  1,022.50 |      892.50 |        0.47 |            1.17 | 20.40 |   0.27 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_POS-ADV_mirror-5000.2024-08-05.csv`



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
1. _longer_
1. _necessarily_
1. _that_
1. _particularly_
1. _remotely_
1. _exactly_

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
1. _longer_
1. _particularly_

### `SET` Adverb Associations (in initially loaded table)


|                  |     `f` |   `dP1` |   `LRC` |   `P1` |       `G2` |      `f1` |    `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `odds_r_disc` |    `t` |   `MI` |
|:-----------------|--------:|--------:|--------:|-------:|-----------:|----------:|--------:|----------:|------------:|------------:|--------:|-------:|----------------:|-------:|-------:|
| **necessarily**  |  42,595 |    0.50 |    6.65 |   0.99 |  55,995.13 | 3,173,681 |  42,916 | 21,458.00 |   21,137.00 |        0.50 |    0.01 |   0.01 |            2.13 | 102.42 |   0.30 |
| **that**         | 164,768 |    0.50 |    6.26 |   0.99 | 214,471.83 | 3,173,681 | 166,680 | 83,340.00 |   81,428.00 |        0.49 |    0.05 |   0.05 |            1.96 | 200.60 |   0.30 |
| **exactly**      |  43,813 |    0.49 |    5.97 |   0.99 |  55,763.99 | 3,173,681 |  44,378 | 22,189.00 |   21,624.00 |        0.49 |    0.01 |   0.01 |            1.90 | 103.31 |   0.30 |
| **immediately**  |  56,099 |    0.48 |    4.92 |   0.97 |  65,652.79 | 3,173,681 |  57,730 | 28,865.00 |   27,234.00 |        0.49 |    0.02 |   0.02 |            1.54 | 114.98 |   0.29 |
| **yet**          |  51,867 |    0.47 |    4.59 |   0.96 |  58,435.17 | 3,173,681 |  53,779 | 26,889.50 |   24,977.50 |        0.48 |    0.02 |   0.02 |            1.44 | 109.67 |   0.29 |
| **any**          |  15,384 |    0.45 |    4.01 |   0.95 |  16,135.27 | 3,173,681 |  16,176 |  8,088.00 |    7,296.00 |        0.47 |    0.00 |   0.00 |            1.29 |  58.82 |   0.28 |
| **remotely**     |   5,661 |    0.43 |    3.30 |   0.93 |   5,269.84 | 3,173,681 |   6,109 |  3,054.50 |    2,606.50 |        0.46 |    0.00 |   0.00 |            1.10 |  34.64 |   0.27 |
| **terribly**     |  17,949 |    0.41 |    3.10 |   0.91 |  15,189.35 | 3,173,681 |  19,801 |  9,900.50 |    8,048.50 |        0.45 |    0.01 |   0.01 |            0.99 |  60.08 |   0.26 |
| **particularly** |  55,527 |    0.23 |    1.33 |   0.72 |  16,109.89 | 3,173,681 |  76,722 | 38,361.00 |   17,166.00 |        0.31 |    0.01 |   0.02 |            0.42 |  72.85 |   0.16 |
| **ever**         |   5,932 |    0.05 |    0.13 |   0.55 |      95.26 | 3,173,681 |  10,849 |  5,424.50 |      507.50 |        0.09 |    0.00 |   0.00 |            0.08 |   6.59 |   0.04 |


### `MIR` Adverb Associations (in initially loaded table)


|                  |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` |    `f1` |   `f2` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `odds_r_disc` |   `t` |   `MI` |
|:-----------------|------:|--------:|--------:|-------:|---------:|--------:|-------:|----------:|------------:|------------:|--------:|-------:|----------------:|------:|-------:|
| **ever**         | 4,709 |    0.49 |    5.32 |   0.99 | 5,953.39 | 291,735 |  4,776 |  2,388.00 |    2,321.00 |        0.49 |    0.02 |   0.02 |            1.85 | 33.82 |   0.29 |
| **any**          | 1,066 |    0.49 |    4.48 |   0.98 | 1,328.27 | 291,735 |  1,083 |    541.50 |      524.50 |        0.49 |    0.00 |   0.00 |            1.79 | 16.06 |   0.29 |
| **longer**       |   821 |    0.48 |    3.96 |   0.98 |   977.90 | 291,735 |    841 |    420.50 |      400.50 |        0.49 |    0.00 |   0.00 |            1.60 | 13.98 |   0.29 |
| **necessarily**  |   963 |    0.47 |    3.82 |   0.97 | 1,109.03 | 291,735 |    993 |    496.50 |      466.50 |        0.48 |    0.00 |   0.00 |            1.50 | 15.03 |   0.29 |
| **that**         | 4,308 |    0.45 |    3.76 |   0.95 | 4,499.79 | 291,735 |  4,538 |  2,269.00 |    2,039.00 |        0.47 |    0.01 |   0.01 |            1.28 | 31.07 |   0.28 |
| **particularly** | 9,243 |    0.43 |    3.31 |   0.92 | 8,550.11 | 291,735 | 10,020 |  5,010.00 |    4,233.00 |        0.46 |    0.03 |   0.03 |            1.09 | 44.03 |   0.27 |
| **remotely**     | 1,840 |    0.44 |    3.27 |   0.94 | 1,806.81 | 291,735 |  1,963 |    981.50 |      858.50 |        0.47 |    0.01 |   0.01 |            1.18 | 20.01 |   0.27 |
| **exactly**      |   813 |    0.44 |    3.09 |   0.94 |   819.82 | 291,735 |    862 |    431.00 |      382.00 |        0.47 |    0.00 |   0.00 |            1.22 | 13.40 |   0.28 |
| **terribly**     | 1,567 |    0.21 |    0.98 |   0.71 |   415.34 | 291,735 |  2,196 |  1,098.00 |      469.00 |        0.30 |    0.00 |   0.01 |            0.40 | 11.85 |   0.15 |




```python
# md_frame_code("""nb_show_table(C.filter(regex=r'^ratio_f2?_')
#               .assign(f_minus_f2=C.ratio_f_MIR - C.ratio_f2_MIR)
#               .multiply(100).round(1)
#               .sort_values(['f_minus_f2', 'ratio_f_MIR'], ascending=False),
#               n_dec=1, adjust_columns=False)""")
# nb_show_table(C.filter(regex=r'^ratio_f2?_')
#               .assign(f_minus_f2=C.ratio_f_MIR - C.ratio_f2_MIR)
#               .multiply(100).round(1)
#               .sort_values(['f_minus_f2', 'ratio_f_MIR'], ascending=False),
#               n_dec=1, adjust_columns=False)
```

## Representation of Adverbs in `NEGmirror`

This table illustrates any disproportionate representations: 
- `ratio_f_MIR` is the ratio of negated occurrences accounted for in the `NEGmirror` subset (actually a percentage here)
- `ratio_f2_MIR` likewise indicates the ratio of **all** tokens of the adverb which are found in *either* mirror polarity (`NEGmirror` or `POSmirror`)
- `f_minus_f2` is the difference of these 2 ratios: a larger value in this column indicates a larger percentage of adverb tokens occuring in not-RBdirect


```python
nb_show_table(C.filter(regex=r'^ratio_f2?_')
              .assign(f_minus_f2=C.ratio_f_MIR - C.ratio_f2_MIR)
              .multiply(100).round(1)
              .sort_values(['f_minus_f2', 'ratio_f_MIR'], ascending=False),
              n_dec=1, adjust_columns=False)
```


|                  |   `ratio_f_MIR` |   `ratio_f2_MIR` |   `f_minus_f2` |
|:-----------------|----------------:|-----------------:|---------------:|
| **ever**         |            79.4 |             44.0 |           35.4 |
| **longer**       |            60.1 |             46.6 |           13.5 |
| **particularly** |            16.6 |             13.1 |            3.6 |
| **remotely**     |            32.5 |             32.1 |            0.4 |
| **any**          |             6.9 |              6.7 |            0.2 |
| **that**         |             2.6 |              2.7 |           -0.1 |
| **necessarily**  |             2.3 |              2.3 |           -0.1 |
| **exactly**      |             1.9 |              1.9 |           -0.1 |
| **yet**          |             0.6 |              0.8 |           -0.1 |
| **immediately**  |             0.7 |              1.0 |           -0.3 |
| **terribly**     |             8.7 |             11.1 |           -2.4 |


For example, the adverb _that_ has only 2.6% of its negated tokens appearing in `NEGmirror`---the remaining 93% occur with sentential negation. 
This value is low, but near equal the proportion of tokens seen in `ANYmir` environments, 
  an indication that almost all _that_ tokens occurring in the mirror subset are negated.

- [ ] Finish this explanation 👆

### *that*

|                 |     `f` |      `f1` |    `f2` |
|:----------------|--------:|----------:|--------:|
| **NEGany~that** | 164,768 | 3,173,681 | 166,680 |
| **NEGmir~that** |   4,308 |   291,735 |   4,538 |

### *ever*

|                 |   `f` |      `f1` |   `f2` |
|:----------------|------:|----------:|-------:|
| **NEGany~ever** | 5,932 | 3,173,681 | 10,849 |
| **NEGmir~ever** | 4,709 |   291,735 |  4,776 |

### *terribly*

|                     |    `f` |      `f1` |   `f2` |
|:--------------------|-------:|----------:|-------:|
| **NEGany~terribly** | 17,949 | 3,173,681 | 19,801 |
| **NEGmir~terribly** |  1,567 |   291,735 |  2,196 |
| **POS~terribly**    |    629 |   291,735 |  2,196 |




```python
# print('### *that*')
# nb_show_table(pd.concat((adf.filter(like='that', axis=0) for adf in [setdiff_adv, mirror_adv])).filter(regex=r'^f'))
# print('### *ever*')
# nb_show_table(pd.concat((adf.filter(like='ever', axis=0) for adf in [setdiff_adv, mirror_adv])).filter(regex=r'^f'))
# print('### *terribly*')
# nb_show_table(pd.concat((adf.filter(like='terribly', axis=0) for adf in [setdiff_adv, mirror_adv])).filter(regex=r'^f'))
```


```python
# md_frame_code("""nb_show_table(
#     C
#     .filter(regex=r'^f_.*[MS]').sort_index(axis=1, ascending=False)
#     .assign(
#         f_diff=C.f_SET-C.f_MIR).sort_values('f_diff', ascending=False)
#     .rename(columns={'f_SET': 'total negations',
#                      'f_MIR': 'mirror subset negations',
#                      'f_diff': 'negations not in mirror subset'}), n_dec=0)""")
# nb_show_table(
#     C
#     .filter(regex=r'^f_.*[MS]').sort_index(axis=1, ascending=False)
#     .assign(
#         f_diff=C.f_SET-C.f_MIR).sort_values('f_diff', ascending=False)
#     .rename(columns={'f_SET': 'total negations',
#                      'f_MIR': 'mirror subset negations',
#                      'f_diff': 'negations not in mirror subset'}), n_dec=0)
```

#### Joint (_Negated_) Frequency Comparison

```python
nb_show_table(
    C
    .filter(regex=r'^f_.*[MS]').sort_index(axis=1, ascending=False)
    .assign(
        f_diff=C.f_SET-C.f_MIR).sort_values('f_diff', ascending=False)
    .rename(columns={'f_SET': 'total negations',
                     'f_MIR': 'mirror subset negations',
                     'f_diff': 'negations not in mirror subset'}), n_dec=0)
```


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
| **remotely**     |               5,661 |                       1,840 |                              3,821 |
| **ever**         |               5,932 |                       4,709 |                              1,223 |
| **longer**       |               1,366 |                         821 |                                545 |




```python
# md_frame_code("""nb_show_table(
#     C
#     .filter(regex=r'^f2_.*[MS]').sort_index(axis=1, ascending=False)
#     .assign(
#         f2_diff=C.f2_SET-C.f2_MIR).sort_values('f2_diff', ascending=False)
#     .rename(columns={'f2_SET':'total adverb tokens', 
#                      'f2_MIR':'mirror subset adverb tokens', 
#                      'f2_diff': 'adverb tokens not in mirror subset'}), n_dec=0)""")
# nb_show_table(
#     C
#     .filter(regex=r'^f2_.*[MS]').sort_index(axis=1, ascending=False)
#     .assign(
#         f2_diff=C.f2_SET-C.f2_MIR).sort_values('f2_diff', ascending=False)
#     .rename(columns={'f2_SET':'total adverb tokens', 
#                      'f2_MIR':'mirror subset adverb tokens', 
#                      'f2_diff': 'adverb tokens not in mirror subset'}), n_dec=0)
```

#### Marginal (_Adverb Total_) Frequency Comparison

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


|                  |   `total adverb tokens` |   `mirror subset adverb tokens` |   `adverb tokens not in mirror subset` |
|:-----------------|------------------------:|--------------------------------:|---------------------------------------:|
| **that**         |                 166,680 |                           4,538 |                                162,142 |
| **particularly** |                  76,722 |                          10,020 |                                 66,702 |
| **immediately**  |                  57,730 |                             578 |                                 57,152 |
| **yet**          |                  53,779 |                             411 |                                 53,368 |
| **exactly**      |                  44,378 |                             862 |                                 43,516 |
| **necessarily**  |                  42,916 |                             993 |                                 41,923 |
| **terribly**     |                  19,801 |                           2,196 |                                 17,605 |
| **any**          |                  16,176 |                           1,083 |                                 15,093 |
| **ever**         |                  10,849 |                           4,776 |                                  6,073 |
| **remotely**     |                   6,109 |                           1,963 |                                  4,146 |
| **longer**       |                   1,803 |                             841 |                                    962 |




```python
full_C = C.copy()
main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in METRIC_PRIORITIES],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2'] ]) 
                              ).drop_duplicates().to_list()
main_C = C[[c for c in main_cols_ordered if c in C.columns]]
sorter = f'mean_{METRIC_PRIORITIES[0]}'

# print(f'### Main Columns for Top Adverbs, sorted by `{sorter}`')
# nb_show_table(main_C.sort_values(sorter, ascending=False))
```

### Main Columns for Top Adverbs, sorted by `mean_LRC`

|                  |   `LRC_SET` |   `LRC_MIR` |   `mean_LRC` |   `dP1_SET` |   `P1_SET` |   `dP1_MIR` |   `P1_MIR` |   `mean_dP1` |   `mean_P1` |   `G2_SET` |   `G2_MIR` |   `mean_G2` |   `dP2_SET` |   `P2_SET` |   `dP2_MIR` |   `P2_MIR` |   `mean_dP2` |   `mean_P2` |   `f_SET` |   `f_MIR` |   `f1_SET` |   `f1_MIR` |   `f2_SET` |   `f2_MIR` |
|:-----------------|------------:|------------:|-------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|-----------:|-----------:|------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|----------:|----------:|-----------:|-----------:|-----------:|-----------:|
| **necessarily**  |        6.65 |        3.82 |         5.24 |        0.50 |       0.99 |        0.47 |       0.97 |         0.48 |        0.98 |  55,995.13 |   1,109.03 |   28,552.08 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    42,595 |       963 |  3,173,681 |    291,735 |     42,916 |        993 |
| **that**         |        6.26 |        3.76 |         5.01 |        0.50 |       0.99 |        0.45 |       0.95 |         0.48 |        0.97 | 214,471.83 |   4,499.79 |  109,485.81 |        0.05 |       0.05 |        0.01 |       0.01 |         0.03 |        0.03 |   164,768 |     4,308 |  3,173,681 |    291,735 |    166,680 |      4,538 |
| **exactly**      |        5.97 |        3.09 |         4.53 |        0.49 |       0.99 |        0.44 |       0.94 |         0.47 |        0.97 |  55,763.99 |     819.82 |   28,291.91 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    43,813 |       813 |  3,173,681 |    291,735 |     44,378 |        862 |
| **any**          |        4.01 |        4.48 |         4.24 |        0.45 |       0.95 |        0.49 |       0.98 |         0.47 |        0.97 |  16,135.27 |   1,328.27 |    8,731.77 |        0.00 |       0.00 |        0.00 |       0.00 |         0.00 |        0.00 |    15,384 |     1,066 |  3,173,681 |    291,735 |     16,176 |      1,083 |
| **remotely**     |        3.30 |        3.27 |         3.29 |        0.43 |       0.93 |        0.44 |       0.94 |         0.43 |        0.93 |   5,269.84 |   1,806.81 |    3,538.33 |        0.00 |       0.00 |        0.01 |       0.01 |         0.00 |        0.00 |     5,661 |     1,840 |  3,173,681 |    291,735 |      6,109 |      1,963 |
| **yet**          |        4.59 |        1.00 |         2.79 |        0.47 |       0.96 |        0.28 |       0.78 |         0.37 |        0.87 |  58,435.17 |     135.28 |   29,285.22 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    51,867 |       320 |  3,173,681 |    291,735 |     53,779 |        411 |
| **immediately**  |        4.92 |        0.57 |         2.74 |        0.48 |       0.97 |        0.20 |       0.70 |         0.34 |        0.83 |  65,652.79 |      92.52 |   32,872.66 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    56,099 |       403 |  3,173,681 |    291,735 |     57,730 |        578 |
| **ever**         |        0.13 |        5.32 |         2.73 |        0.05 |       0.55 |        0.49 |       0.99 |         0.27 |        0.77 |      95.26 |   5,953.39 |    3,024.33 |        0.00 |       0.00 |        0.02 |       0.02 |         0.01 |        0.01 |     5,932 |     4,709 |  3,173,681 |    291,735 |     10,849 |      4,776 |
| **longer**       |        1.24 |        3.96 |         2.60 |        0.26 |       0.76 |        0.48 |       0.98 |         0.37 |        0.87 |     502.62 |     977.90 |      740.26 |        0.00 |       0.00 |        0.00 |       0.00 |         0.00 |        0.00 |     1,366 |       821 |  3,173,681 |    291,735 |      1,803 |        841 |
| **particularly** |        1.33 |        3.31 |         2.32 |        0.23 |       0.72 |        0.43 |       0.92 |         0.33 |        0.82 |  16,109.89 |   8,550.11 |   12,330.00 |        0.01 |       0.02 |        0.03 |       0.03 |         0.02 |        0.02 |    55,527 |     9,243 |  3,173,681 |    291,735 |     76,722 |     10,020 |
| **terribly**     |        3.10 |        0.98 |         2.04 |        0.41 |       0.91 |        0.21 |       0.71 |         0.31 |        0.81 |  15,189.35 |     415.34 |    7,802.35 |        0.01 |       0.01 |        0.00 |       0.01 |         0.00 |        0.01 |    17,949 |     1,567 |  3,173,681 |    291,735 |     19,801 |      2,196 |



## Save full adverb selection as `.csv`



```python
print('Saving Combined "Most Negative Adverbs" AM table as csv:  '
    f'\n> `{combined_top_csv_output}`')

# C.to_csv(combined_top_csv_output, float_format='{:.4f}'.format)
```

    Saving Combined "Most Negative Adverbs" AM table as csv:  
    > `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-08-05.csv`


Saving Combined "Most Negative Adverbs" AM table as csv:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-08-05.csv`

Save `all-columns`, `means`, and `MAIN` as markdown formatted tables


```python
# nb_show_table(C, suppress_printing=True,
#     outpath=OUT_DIR.joinpath(
#         f'{save_prefix}_all-columns_{timestamp_today()}.md')
# )

# md_frame_code("""nb_show_table(C[main_cols_ordered],
#     outpath=OUT_DIR.joinpath(
#         f'{save_prefix}_MAIN_{timestamp_today()}.md'))""")
# nb_show_table(C[main_cols_ordered],
#     outpath=OUT_DIR.joinpath(
#         f'{save_prefix}_MAIN_{timestamp_today()}.md')
# )

```


```python
nb_show_table(C[main_cols_ordered],
    outpath=OUT_DIR.joinpath(
        f'{save_prefix}_MAIN_{timestamp_today()}.md'))
```


|                  |   `LRC_SET` |   `LRC_MIR` |   `mean_LRC` |   `dP1_SET` |   `P1_SET` |   `dP1_MIR` |   `P1_MIR` |   `mean_dP1` |   `mean_P1` |   `G2_SET` |   `G2_MIR` |   `mean_G2` |   `dP2_SET` |   `P2_SET` |   `dP2_MIR` |   `P2_MIR` |   `mean_dP2` |   `mean_P2` |   `f_SET` |   `f_MIR` |   `f1_SET` |   `f1_MIR` |   `f2_SET` |   `f2_MIR` |
|:-----------------|------------:|------------:|-------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|-----------:|-----------:|------------:|------------:|-----------:|------------:|-----------:|-------------:|------------:|----------:|----------:|-----------:|-----------:|-----------:|-----------:|
| **necessarily**  |        6.65 |        3.82 |         5.24 |        0.50 |       0.99 |        0.47 |       0.97 |         0.48 |        0.98 |  55,995.13 |   1,109.03 |   28,552.08 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    42,595 |       963 |  3,173,681 |    291,735 |     42,916 |        993 |
| **that**         |        6.26 |        3.76 |         5.01 |        0.50 |       0.99 |        0.45 |       0.95 |         0.48 |        0.97 | 214,471.83 |   4,499.79 |  109,485.81 |        0.05 |       0.05 |        0.01 |       0.01 |         0.03 |        0.03 |   164,768 |     4,308 |  3,173,681 |    291,735 |    166,680 |      4,538 |
| **exactly**      |        5.97 |        3.09 |         4.53 |        0.49 |       0.99 |        0.44 |       0.94 |         0.47 |        0.97 |  55,763.99 |     819.82 |   28,291.91 |        0.01 |       0.01 |        0.00 |       0.00 |         0.01 |        0.01 |    43,813 |       813 |  3,173,681 |    291,735 |     44,378 |        862 |
| **any**          |        4.01 |        4.48 |         4.24 |        0.45 |       0.95 |        0.49 |       0.98 |         0.47 |        0.97 |  16,135.27 |   1,328.27 |    8,731.77 |        0.00 |       0.00 |        0.00 |       0.00 |         0.00 |        0.00 |    15,384 |     1,066 |  3,173,681 |    291,735 |     16,176 |      1,083 |
| **remotely**     |        3.30 |        3.27 |         3.29 |        0.43 |       0.93 |        0.44 |       0.94 |         0.43 |        0.93 |   5,269.84 |   1,806.81 |    3,538.33 |        0.00 |       0.00 |        0.01 |       0.01 |         0.00 |        0.00 |     5,661 |     1,840 |  3,173,681 |    291,735 |      6,109 |      1,963 |
| **yet**          |        4.59 |        1.00 |         2.79 |        0.47 |       0.96 |        0.28 |       0.78 |         0.37 |        0.87 |  58,435.17 |     135.28 |   29,285.22 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    51,867 |       320 |  3,173,681 |    291,735 |     53,779 |        411 |
| **immediately**  |        4.92 |        0.57 |         2.74 |        0.48 |       0.97 |        0.20 |       0.70 |         0.34 |        0.83 |  65,652.79 |      92.52 |   32,872.66 |        0.02 |       0.02 |        0.00 |       0.00 |         0.01 |        0.01 |    56,099 |       403 |  3,173,681 |    291,735 |     57,730 |        578 |
| **ever**         |        0.13 |        5.32 |         2.73 |        0.05 |       0.55 |        0.49 |       0.99 |         0.27 |        0.77 |      95.26 |   5,953.39 |    3,024.33 |        0.00 |       0.00 |        0.02 |       0.02 |         0.01 |        0.01 |     5,932 |     4,709 |  3,173,681 |    291,735 |     10,849 |      4,776 |
| **longer**       |        1.24 |        3.96 |         2.60 |        0.26 |       0.76 |        0.48 |       0.98 |         0.37 |        0.87 |     502.62 |     977.90 |      740.26 |        0.00 |       0.00 |        0.00 |       0.00 |         0.00 |        0.00 |     1,366 |       821 |  3,173,681 |    291,735 |      1,803 |        841 |
| **particularly** |        1.33 |        3.31 |         2.32 |        0.23 |       0.72 |        0.43 |       0.92 |         0.33 |        0.82 |  16,109.89 |   8,550.11 |   12,330.00 |        0.01 |       0.02 |        0.03 |       0.03 |         0.02 |        0.02 |    55,527 |     9,243 |  3,173,681 |    291,735 |     76,722 |     10,020 |
| **terribly**     |        3.10 |        0.98 |         2.04 |        0.41 |       0.91 |        0.21 |       0.71 |         0.31 |        0.81 |  15,189.35 |     415.34 |    7,802.35 |        0.01 |       0.01 |        0.00 |       0.01 |         0.00 |        0.01 |    17,949 |     1,567 |  3,173,681 |    291,735 |     19,801 |      2,196 |




```python
# md_frame_code("""nb_show_table(C.filter(like='mean_'),
#     outpath=OUT_DIR.joinpath(
#         f'{save_prefix}_means_{timestamp_today()}.md'))""")
# nb_show_table(C.filter(like='mean_'),
#     outpath=OUT_DIR.joinpath(
#         f'{save_prefix}_means_{timestamp_today()}.md')
# )
```


```python
nb_show_table(C.filter(like='mean_'),
    outpath=OUT_DIR.joinpath(
        f'{save_prefix}_means_{timestamp_today()}.md'))
```


|                  |   `mean_f` |   `mean_dP1` |   `mean_LRC` |   `mean_P1` |   `mean_G2` |    `mean_f1` |   `mean_f2` |     `mean_N` |   `mean_expF` |   `mean_unexpF` |   `mean_unexpR` |   `mean_dP2` |   `mean_P2` |   `mean_oddsRDisc` |   `mean_t` |   `mean_MI` |
|:-----------------|-----------:|-------------:|-------------:|------------:|------------:|-------------:|------------:|-------------:|--------------:|----------------:|----------------:|-------------:|------------:|-------------------:|-----------:|------------:|
| **necessarily**  | 592,147.17 |         0.48 |         5.24 |        0.98 |   28,552.08 | 1,732,708.00 |   21,954.50 | 3,465,416.00 |     10,977.25 |       10,801.75 |            0.49 |         0.01 |        0.01 |               1.81 |      58.72 |        0.29 |
| **that**         | 634,285.00 |         0.48 |         5.01 |        0.97 |  109,485.81 | 1,732,708.00 |   85,609.00 | 3,465,416.00 |     42,804.50 |       41,733.50 |            0.48 |         0.03 |        0.03 |               1.62 |     115.83 |        0.29 |
| **exactly**      | 592,547.00 |         0.47 |         4.53 |        0.97 |   28,291.91 | 1,732,708.00 |   22,620.00 | 3,465,416.00 |     11,310.00 |       11,003.00 |            0.48 |         0.01 |        0.01 |               1.56 |      58.35 |        0.29 |
| **any**          | 583,187.50 |         0.47 |         4.24 |        0.97 |    8,731.77 | 1,732,708.00 |    8,629.50 | 3,465,416.00 |      4,314.75 |        3,910.25 |            0.48 |         0.00 |        0.00 |               1.54 |      37.44 |        0.29 |
| **remotely**     | 580,164.83 |         0.43 |         3.29 |        0.93 |    3,538.33 | 1,732,708.00 |    4,036.00 | 3,465,416.00 |      2,018.00 |        1,732.50 |            0.46 |         0.00 |        0.00 |               1.14 |      27.33 |        0.27 |
| **yet**          | 595,298.83 |         0.37 |         2.79 |        0.87 |   29,285.22 | 1,732,708.00 |   27,095.00 | 3,465,416.00 |     13,547.50 |       12,546.00 |            0.42 |         0.01 |        0.01 |               0.99 |      58.04 |        0.24 |
| **immediately**  | 596,704.33 |         0.34 |         2.74 |        0.83 |   32,872.66 | 1,732,708.00 |   29,154.00 | 3,465,416.00 |     14,577.00 |       13,674.00 |            0.38 |         0.01 |        0.01 |               0.95 |      60.33 |        0.22 |
| **ever**         | 581,947.00 |         0.27 |         2.73 |        0.77 |    3,024.33 | 1,732,708.00 |    7,812.50 | 3,465,416.00 |      3,906.25 |        1,414.25 |            0.29 |         0.01 |        0.01 |               0.97 |      20.21 |        0.17 |
| **longer**       | 578,374.50 |         0.37 |         2.60 |        0.87 |      740.26 | 1,732,708.00 |    1,322.00 | 3,465,416.00 |        661.00 |          432.50 |            0.41 |         0.00 |        0.00 |               1.05 |      13.27 |        0.24 |
| **particularly** | 602,821.33 |         0.33 |         2.32 |        0.82 |   12,330.00 | 1,732,708.00 |   43,371.00 | 3,465,416.00 |     21,685.50 |       10,699.50 |            0.38 |         0.02 |        0.02 |               0.76 |      58.44 |        0.21 |
| **terribly**     | 584,488.17 |         0.31 |         2.04 |        0.81 |    7,802.35 | 1,732,708.00 |   10,998.50 | 3,465,416.00 |      5,499.25 |        4,258.75 |            0.37 |         0.00 |        0.01 |               0.69 |      35.96 |        0.21 |


