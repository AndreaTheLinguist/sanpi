```python
import pandas as pd
from am_notebooks import nb_show_table

from source.utils.dataframes import (calculate_var_coeff, enhance_descrip,
                                     get_mad, quartile_dispersion)
from source.utils.general import SANPI_HOME, confirm_dir, timestamp_today

subtotals_outdir = SANPI_HOME.joinpath('info/final_subtotals')
subtotals = pd.concat([pd.read_csv(csv, index_col='part').astype('int').sort_index().T 
             for csv in SANPI_HOME.joinpath('info/final_subtotals').glob('*.csv')]).T
nb_show_table(subtotals.convert_dtypes(), 
              outpath=subtotals_outdir/f'COMBINED_final-subtotals.{timestamp_today()}.md')

    
```


|           |   `POSmirror_hits` |   `mirrorNEQ_hits` |   `not-RBdirect_hits` |   `superNEQ_hits` |   `NEGmirror_hits` |   `RBdirect_hits` |
|:----------|-------------------:|-------------------:|----------------------:|------------------:|-------------------:|------------------:|
| **Apw**   |             17,294 |              3,805 |             1,878,981 |            86,805 |              5,320 |            90,499 |
| **Nyt1**  |             26,803 |              5,474 |             1,937,910 |            89,336 |             10,796 |            98,361 |
| **Nyt2**  |             41,008 |              8,679 |             2,746,650 |           126,486 |             14,761 |           136,138 |
| **Pcc00** |             43,742 |              9,078 |             2,100,614 |            96,962 |              8,541 |            95,376 |
| **Pcc01** |             43,095 |              9,151 |             2,068,435 |            95,634 |              8,498 |            94,471 |
| **Pcc02** |             42,597 |              9,057 |             2,032,504 |            93,915 |              8,585 |            92,869 |
| **Pcc03** |             43,303 |              8,903 |             2,073,494 |            95,492 |              8,739 |            94,950 |
| **Pcc04** |             43,191 |              9,013 |             2,071,538 |            95,210 |              8,679 |            94,190 |
| **Pcc05** |             43,447 |              9,064 |             2,082,218 |            96,276 |              8,813 |            95,371 |
| **Pcc06** |             45,422 |              9,637 |             2,158,603 |            99,462 |              9,061 |            98,355 |
| **Pcc07** |             43,161 |              9,008 |             2,051,873 |            94,592 |              8,673 |            94,404 |
| **Pcc08** |             44,889 |              9,503 |             2,140,164 |            98,722 |              8,958 |            96,890 |
| **Pcc09** |             43,195 |              8,959 |             2,063,787 |            95,298 |              8,569 |            94,183 |
| **Pcc10** |             42,785 |              9,085 |             2,050,397 |            94,563 |              8,597 |            94,632 |
| **Pcc11** |             42,975 |              8,945 |             2,067,797 |            95,398 |              8,552 |            94,501 |
| **Pcc12** |             43,871 |              9,220 |             2,106,105 |            97,295 |              8,921 |            97,305 |
| **Pcc13** |             42,490 |              9,002 |             2,025,964 |            93,235 |              8,562 |            92,541 |
| **Pcc14** |             42,910 |              8,941 |             2,030,054 |            93,298 |              8,640 |            93,545 |
| **Pcc15** |             42,575 |              9,025 |             2,027,709 |            93,609 |              8,447 |            92,783 |
| **Pcc16** |             44,291 |              9,245 |             2,093,696 |            96,596 |              8,685 |            95,411 |
| **Pcc17** |             42,742 |              8,930 |             2,048,259 |            94,653 |              8,410 |            93,898 |
| **Pcc18** |             43,988 |              9,194 |             2,117,053 |            97,308 |              8,764 |            96,685 |
| **Pcc19** |             44,826 |              9,406 |             2,139,234 |            98,870 |              9,181 |            97,836 |
| **Pcc20** |             44,034 |              9,329 |             2,102,322 |            96,686 |              8,818 |            96,346 |
| **Pcc21** |             42,806 |              8,971 |             2,038,043 |            93,481 |              8,480 |            93,045 |
| **Pcc22** |             43,859 |              9,223 |             2,080,162 |            95,861 |              8,840 |            95,906 |
| **Pcc23** |             44,082 |              9,228 |             2,094,183 |            96,892 |              8,745 |            95,624 |
| **Pcc24** |             43,867 |              9,209 |             2,077,021 |            96,231 |              8,714 |            95,410 |
| **Pcc25** |             42,977 |              9,045 |             2,039,960 |            94,028 |              8,582 |            93,534 |
| **Pcc26** |             42,132 |              8,838 |             2,014,969 |            92,834 |              8,619 |            92,787 |
| **Pcc27** |             42,081 |              8,824 |             2,013,996 |            92,897 |              8,422 |            92,345 |
| **Pcc28** |             43,311 |              9,187 |             2,061,840 |            95,783 |              8,675 |            94,606 |
| **Pcc29** |             42,438 |              8,990 |             2,020,064 |            93,800 |              8,500 |            92,838 |
| **PccTe** |              1,371 |                274 |                66,019 |             3,108 |                291 |             2,970 |
| **PccVa** |              1,340 |                293 |                66,074 |             3,065 |                297 |             3,076 |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/COMBINED_final-subtotals.2024-08-06.md`




```python
nb_show_table(subtotals.describe().T.round(1).convert_dtypes().sort_values(['mean', '50%']), n_dec=1, 
              outpath=subtotals_outdir / f'simple-stats_env-by-part.{timestamp_today()}.md')
```


|                       |   `count` |      `mean` |     `std` |   `min` |       `25%` |     `50%` |       `75%` |     `max` |
|:----------------------|----------:|------------:|----------:|--------:|------------:|----------:|------------:|----------:|
| **NEGmirror_hits**    |        35 |     8,335.3 |   2,365.4 |     291 |     8,520.5 |     8,640 |     8,788.5 |    14,761 |
| **mirrorNEQ_hits**    |        35 |     8,335.3 |   2,284.2 |     274 |     8,935.5 |     9,025 |     9,201.5 |     9,637 |
| **POSmirror_hits**    |        35 |    39,682.8 |  10,892.7 |   1,340 |    42,532.5 |    43,095 |    43,863.0 |    45,422 |
| **RBdirect_hits**     |        35 |    90,676.6 |  23,052.2 |   2,970 |    92,957.0 |    94,501 |    95,765.0 |   136,138 |
| **superNEQ_hits**     |        35 |    90,676.6 |  22,644.0 |   3,065 |    93,545.0 |    95,298 |    96,641.0 |   126,486 |
| **not-RBdirect_hits** |        35 | 1,965,362.6 | 491,198.3 |  66,019 | 2,028,881.5 | 2,063,787 | 2,093,939.5 | 2,746,650 |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/simple-stats_env-by-part.2024-08-06.md`




```python
nb_show_table(subtotals.T.describe().round(1).T.sort_values('min', ascending=False).sort_values(['mean', '50%']).convert_dtypes(),
              n_dec=1, 
              outpath=subtotals_outdir / f'simple-stats_part-by-env.{timestamp_today()}.md')
```


|           |   `count` |    `mean` |       `std` |   `min` |    `25%` |    `50%` |     `75%` |     `max` |
|:----------|----------:|----------:|------------:|--------:|---------:|---------:|----------:|----------:|
| **PccTe** |         6 |  12,338.8 |    26,327.0 |     274 |    561.0 |  2,170.5 |   3,073.5 |    66,019 |
| **PccVa** |         6 |  12,357.5 |    26,345.2 |     293 |    557.8 |  2,202.5 |   3,073.2 |    66,074 |
| **Apw**   |         6 | 347,117.3 |   751,491.0 |   3,805 |  8,313.5 | 52,049.5 |  89,575.5 | 1,878,981 |
| **Nyt1**  |         6 | 361,446.7 |   773,324.5 |   5,474 | 14,797.8 | 58,069.5 |  96,104.8 | 1,937,910 |
| **Pcc27** |         6 | 376,427.5 |   803,127.8 |   8,422 | 17,138.2 | 67,213.0 |  92,759.0 | 2,013,996 |
| **Pcc26** |         6 | 376,696.5 |   803,474.2 |   8,619 | 17,161.5 | 67,459.5 |  92,822.2 | 2,014,969 |
| **Pcc29** |         6 | 377,771.7 |   805,451.6 |   8,500 | 17,352.0 | 67,638.0 |  93,559.5 | 2,020,064 |
| **Pcc13** |         6 | 378,632.3 |   807,907.4 |   8,562 | 17,374.0 | 67,515.5 |  93,061.5 | 2,025,964 |
| **Pcc15** |         6 | 379,024.7 |   808,576.8 |   8,447 | 17,412.5 | 67,679.0 |  93,402.5 | 2,027,709 |
| **Pcc14** |         6 | 379,564.7 |   809,463.3 |   8,640 | 17,433.2 | 68,104.0 |  93,483.2 | 2,030,054 |
| **Pcc02** |         6 | 379,921.2 |   810,487.1 |   8,585 | 17,442.0 | 67,733.0 |  93,653.5 | 2,032,504 |
| **Pcc21** |         6 | 380,804.3 |   812,764.2 |   8,480 | 17,429.8 | 67,925.5 |  93,372.0 | 2,038,043 |
| **Pcc25** |         6 | 381,354.3 |   813,442.4 |   8,582 | 17,528.0 | 68,255.5 |  93,904.5 | 2,039,960 |
| **Pcc17** |         6 | 382,815.3 |   816,802.6 |   8,410 | 17,383.0 | 68,320.0 |  94,464.2 | 2,048,259 |
| **Pcc10** |         6 | 383,343.2 |   817,594.1 |   8,597 | 17,510.0 | 68,674.0 |  94,614.8 | 2,050,397 |
| **Pcc07** |         6 | 383,618.5 |   818,178.8 |   8,673 | 17,546.2 | 68,782.5 |  94,545.0 | 2,051,873 |
| **Pcc28** |         6 | 385,567.0 |   822,115.9 |   8,675 | 17,718.0 | 68,958.5 |  95,488.8 | 2,061,840 |
| **Pcc09** |         6 | 385,665.2 |   823,014.3 |   8,569 | 17,518.0 | 68,689.0 |  95,019.2 | 2,063,787 |
| **Pcc11** |         6 | 386,361.3 |   824,641.2 |   8,552 | 17,452.5 | 68,738.0 |  95,173.8 | 2,067,797 |
| **Pcc01** |         6 | 386,547.3 |   824,862.9 |   8,498 | 17,637.0 | 68,783.0 |  95,343.2 | 2,068,435 |
| **Pcc04** |         6 | 386,970.2 |   826,166.2 |   8,679 | 17,557.5 | 68,690.5 |  94,955.0 | 2,071,538 |
| **Pcc03** |         6 | 387,480.2 |   826,885.4 |   8,739 | 17,503.0 | 69,126.5 |  95,356.5 | 2,073,494 |
| **Pcc24** |         6 | 388,408.7 |   828,166.3 |   8,714 | 17,873.5 | 69,638.5 |  96,025.8 | 2,077,021 |
| **Pcc22** |         6 | 388,975.2 |   829,426.1 |   8,840 | 17,882.0 | 69,860.0 |  95,894.8 | 2,080,162 |
| **Pcc05** |         6 | 389,198.2 |   830,324.4 |   8,813 | 17,659.8 | 69,409.0 |  96,049.8 | 2,082,218 |
| **Pcc16** |         6 | 391,320.7 |   834,904.6 |   8,685 | 18,006.5 | 69,851.0 |  96,299.8 | 2,093,696 |
| **Pcc23** |         6 | 391,459.0 |   835,080.6 |   8,745 | 17,941.5 | 69,853.0 |  96,575.0 | 2,094,183 |
| **Pcc00** |         6 | 392,385.5 |   837,776.6 |   8,541 | 17,744.0 | 69,559.0 |  96,565.5 | 2,100,614 |
| **Pcc20** |         6 | 392,922.5 |   838,351.2 |   8,818 | 18,005.2 | 70,190.0 |  96,601.0 | 2,102,322 |
| **Pcc12** |         6 | 393,786.2 |   839,797.2 |   8,921 | 17,882.8 | 70,583.0 |  97,302.5 | 2,106,105 |
| **Pcc18** |         6 | 395,498.7 |   844,311.7 |   8,764 | 17,892.5 | 70,336.5 |  97,152.2 | 2,117,053 |
| **Pcc08** |         6 | 399,854.3 |   853,501.1 |   8,958 | 18,349.5 | 70,889.5 |  98,264.0 | 2,140,164 |
| **Pcc19** |         6 | 399,892.2 |   853,038.0 |   9,181 | 18,261.0 | 71,331.0 |  98,611.5 | 2,139,234 |
| **Pcc06** |         6 | 403,423.3 |   860,798.4 |   9,061 | 18,583.2 | 71,888.5 |  99,185.2 | 2,158,603 |
| **Nyt2**  |         6 | 512,287.0 | 1,095,989.6 |   8,679 | 21,322.8 | 83,747.0 | 133,725.0 | 2,746,650 |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/simple-stats_part-by-env.2024-08-06.md`




```python
nb_show_table(enhance_descrip(subtotals).round(1).convert_dtypes(), 
              n_dec=1, transpose=False, 
              outpath=subtotals_outdir / f'extended-stats_env-by-part.{timestamp_today()}.md')

```


```python
nb_show_table(enhance_descrip(subtotals).round(1).convert_dtypes(), 
              n_dec=1, transpose=True, 
              outpath=subtotals_outdir / f'extended-stats_env-by-part_T.{timestamp_today()}.md')
```


|                       | `unique_forms` |      `mean` |     `std` |  `min` |       `25%` |  `median` |       `75%` |     `max` |    `total` | `var_coeff` |   `range` | `IQ_range` | `Q_disper` |  `MAD` | `upper_fence` | `lower_fence` |
|:----------------------|---------------:|------------:|----------:|-------:|------------:|----------:|------------:|----------:|-----------:|------------:|----------:|-----------:|-----------:|-------:|--------------:|--------------:|
| **POSmirror_hits**    |             35 |    39,682.8 |  10,892.7 |  1,340 |    42,532.5 |    43,095 |    43,863.0 |    45,422 |  1,388,898 |         0.3 |    44,082 |    1,330.5 |          0 |    657 |      45,858.8 |      40,536.8 |
| **mirrorNEQ_hits**    |             35 |     8,335.3 |   2,284.2 |    274 |     8,935.5 |     9,025 |     9,201.5 |     9,637 |    291,735 |         0.3 |     9,363 |      266.0 |          0 |    162 |       9,600.5 |       8,536.5 |
| **not-RBdirect_hits** |             35 | 1,965,362.6 | 491,198.3 | 66,019 | 2,028,881.5 | 2,063,787 | 2,093,939.5 | 2,746,650 | 68,787,692 |         0.2 | 2,680,631 |   65,058.0 |          0 | 33,733 |   2,191,526.5 |   1,931,294.5 |
| **superNEQ_hits**     |             35 |    90,676.6 |  22,644.0 |  3,065 |    93,545.0 |    95,298 |    96,641.0 |   126,486 |  3,173,681 |         0.2 |   123,421 |    3,096.0 |          0 |  1,594 |     101,285.0 |      88,901.0 |
| **NEGmirror_hits**    |             35 |     8,335.3 |   2,365.4 |    291 |     8,520.5 |     8,640 |     8,788.5 |    14,761 |    291,735 |         0.3 |    14,470 |      268.0 |          0 |    140 |       9,190.5 |       8,118.5 |
| **RBdirect_hits**     |             35 |    90,676.6 |  23,052.2 |  2,970 |    92,957.0 |    94,501 |    95,765.0 |   136,138 |  3,173,681 |         0.3 |   133,168 |    2,808.0 |          0 |  1,456 |      99,977.0 |      88,745.0 |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/extended-stats_env-by-part.2024-08-06.md`



|                    | `POSmirror_hits` | `mirrorNEQ_hits` | `not-RBdirect_hits` | `superNEQ_hits` | `NEGmirror_hits` | `RBdirect_hits` |
|:-------------------|-----------------:|-----------------:|--------------------:|----------------:|-----------------:|----------------:|
| **`unique_forms`** |             35.0 |             35.0 |                35.0 |            35.0 |             35.0 |            35.0 |
| **`mean`**         |         39,682.8 |          8,335.3 |         1,965,362.6 |        90,676.6 |          8,335.3 |        90,676.6 |
| **`std`**          |         10,892.7 |          2,284.2 |           491,198.3 |        22,644.0 |          2,365.4 |        23,052.2 |
| **`min`**          |          1,340.0 |            274.0 |            66,019.0 |         3,065.0 |            291.0 |         2,970.0 |
| **`25%`**          |         42,532.5 |          8,935.5 |         2,028,881.5 |        93,545.0 |          8,520.5 |        92,957.0 |
| **`median`**       |         43,095.0 |          9,025.0 |         2,063,787.0 |        95,298.0 |          8,640.0 |        94,501.0 |
| **`75%`**          |         43,863.0 |          9,201.5 |         2,093,939.5 |        96,641.0 |          8,788.5 |        95,765.0 |
| **`max`**          |         45,422.0 |          9,637.0 |         2,746,650.0 |       126,486.0 |         14,761.0 |       136,138.0 |
| **`total`**        |      1,388,898.0 |        291,735.0 |        68,787,692.0 |     3,173,681.0 |        291,735.0 |     3,173,681.0 |
| **`var_coeff`**    |              0.3 |              0.3 |                 0.2 |             0.2 |              0.3 |             0.3 |
| **`range`**        |         44,082.0 |          9,363.0 |         2,680,631.0 |       123,421.0 |         14,470.0 |       133,168.0 |
| **`IQ_range`**     |          1,330.5 |            266.0 |            65,058.0 |         3,096.0 |            268.0 |         2,808.0 |
| **`Q_disper`**     |              0.0 |              0.0 |                 0.0 |             0.0 |              0.0 |             0.0 |
| **`MAD`**          |            657.0 |            162.0 |            33,733.0 |         1,594.0 |            140.0 |         1,456.0 |
| **`upper_fence`**  |         45,858.8 |          9,600.5 |         2,191,526.5 |       101,285.0 |          9,190.5 |        99,977.0 |
| **`lower_fence`**  |         40,536.8 |          8,536.5 |         1,931,294.5 |        88,901.0 |          8,118.5 |        88,745.0 |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/extended-stats_env-by-part_T.2024-08-06.md`






```python
cat_totals = subtotals.sum().sort_values().to_frame('totals').convert_dtypes()
nb_show_table(cat_totals)
total_total = cat_totals.T.filter(like='direct').squeeze().sum()
```


|                       |   `totals` |
|:----------------------|-----------:|
| **mirrorNEQ_hits**    |    291,735 |
| **NEGmirror_hits**    |    291,735 |
| **POSmirror_hits**    |  1,388,898 |
| **superNEQ_hits**     |  3,173,681 |
| **RBdirect_hits**     |  3,173,681 |
| **not-RBdirect_hits** | 68,787,692 |




```python
subtotals.loc['Total', :] = subtotals.sum(axis=0)
subtotals.loc['Avg', :] = subtotals.mean(axis=0)
subtotals.filter(like='RBdirect').loc[:, 'Total'] = subtotals.sum(axis=1)
subtotals.loc[:, 'Avg'] = subtotals.mean(axis=1)
subtotals = subtotals.astype('int')
# print(subtotals.to_markdown(intfmt=',', floatfmt=',.0f'))
```


```python
print(f'${total_total:,}$ hits remaining in superset polar comparison---_`ANYdirect` essentially_')
```

$71,961,373$ hits remaining in superset polar comparison---_`ANYdirect` essentially_



```python
envs = cat_totals.index.to_series()
polar_approx_method = (envs
                       .str.extract(r'(mirror|super|direct)', expand=False)
                       .str.replace(r'super|direct', 'superset (negative trigger absent)', regex=True)
                       .str.replace('mirror', 'mirror subset (positive trigger present)'))
cat_totals.loc[:, 'approximation method'] = polar_approx_method
cat_totals['polarity'] = (envs.str.extract(r'(NE[QG]|POS|n?o?t?-?RBdirect)', expand=False)
                          .str.replace(r'(not-RBdirect|POS|NEQ)', '(+)', regex=True)
                          .str.replace(r'(RBdirect|NEG)', '(-)', regex=True))
cat_totals['data selection'] = envs.str.extract(r'(NEQ)', expand=False).fillna('ALL')
cat_totals
```


```python
cat_totals['% of "ANYdirect" superset'] = ((cat_totals.totals / total_total) * 100).round(1)
cat_totals = cat_totals.sort_index().sort_values('totals')
cat_totals.index.name = 'environment dataset'
cat_totals.convert_dtypes()
```


|                       |   `Totals` | `approximation method`                     | `polarity`   | `data selection`   |   `% of full "ANYdirect" superset` |
|:----------------------|-----------:|:-------------------------------------------|:-------------|:-------------------|-----------------------------------:|
| **NEGmirror_hits**    |    291,735 | *mirror subset (positive trigger present)* | (-)          | ALL                |                               0.41 |
| **mirrorNEQ_hits**    |    291,735 | *mirror subset (positive trigger present)* | (+)          | NEQ                |                               0.41 |
| **POSmirror_hits**    |  1,388,898 | *mirror subset (positive trigger present)* | (+)          | ALL                |                               1.93 |
| **RBdirect_hits**     |  3,173,681 | *superset (negative trigger absent)*       | (-)          | ALL                |                               4.41 |
| **superNEQ_hits**     |  3,173,681 | *superset (negative trigger absent)*       | (+)          | NEQ                |                               4.41 |
| **not-RBdirect_hits** | 68,787,692 | *superset (negative trigger absent)*       | (+)          | ALL                |                              95.59 |




```python
mir_totals = cat_totals.filter(like='mirror_hits', axis=0).totals
mir_totals
mir_total_sum = mir_totals.sum()
cat_totals['N']=cat_totals['approximation method'].apply(lambda x:  mir_total_sum if x.startswith('mirror') else total_total)
cat_totals.loc[cat_totals['data selection'] == 'NEQ', 'N'] = cat_totals.filter(like='NEQ', axis=0).totals * 2
cat_totals['% of "ANYmirror" subset'] = (cat_totals.totals / mir_total_sum * 100).round(1)
cat_totals = cat_totals.sort_values(['N', 'totals'])
cat_totals
```


```python
#// cat_totals.loc[:, cat_totals.columns.str.startswith('%')] = cat_totals.loc[:, cat_totals.columns.str.startswith('%')].astype('string') + '%'
nb_show_table(cat_totals.convert_dtypes().sort_index(axis=1, ascending=False), outpath=subtotals_outdir/f'env-totals-overview.{timestamp_today()}.md')
```


|                       |   `totals` | `polarity`   | `data selection`   | `approximation method`                     |        `N` |   `% of "ANYmirror" subset` |   `% of "ANYdirect" superset` |
|:----------------------|-----------:|:-------------|:-------------------|:-------------------------------------------|-----------:|----------------------------:|------------------------------:|
| **mirrorNEQ_hits**    |    291,735 | (+)          | NEQ                | *mirror subset (positive trigger present)* |    583,470 |                       17.40 |                          0.40 |
| **NEGmirror_hits**    |    291,735 | (-)          | ALL                | *mirror subset (positive trigger present)* |  1,680,633 |                       17.40 |                          0.40 |
| **POSmirror_hits**    |  1,388,898 | (+)          | ALL                | *mirror subset (positive trigger present)* |  1,680,633 |                       82.60 |                          1.90 |
| **superNEQ_hits**     |  3,173,681 | (+)          | NEQ                | *superset (negative trigger absent)*       |  6,347,362 |                      188.80 |                          4.40 |
| **RBdirect_hits**     |  3,173,681 | (-)          | ALL                | *superset (negative trigger absent)*       | 71,961,373 |                      188.80 |                          4.40 |
| **not-RBdirect_hits** | 68,787,692 | (+)          | ALL                | *superset (negative trigger absent)*       | 71,961,373 |                    4,093.00 |                         95.60 |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/env-totals-overview.2024-08-06.md`




```python
super_totals = cat_totals.filter(like='RBdirect', axis=0).totals
prepond = pd.DataFrame([
    [t.min() for t in (super_totals, mir_totals)],
    [t.max() for t in (super_totals, mir_totals)],
              ], columns=['superset', 'mirr_sub'], index=['neg_count', 'pos_count'], dtype='int'
             ).transpose()
prepond["N"] = prepond.sum(axis=1)

prepond['neg_proportion'] = (prepond.neg_count / prepond.N * 100).round(2).astype('string') + '%'
prepond['pos_proportion'] = (prepond.pos_count / prepond.N * 100).round(2).astype('string')+ '%'
prepond['pos_odds'] = '**' + (prepond.pos_count / prepond.neg_count).multiply(1).round(0).astype('int').astype('string') + ':1**'
# prepond['(neg_odds)'] = (prepond.neg_count / prepond.pos_count).multiply(1).round(2).astype('string') + ':1'

nb_show_table(prepond, title='## Size Discrepancies\n', outpath=subtotals_outdir/ f'env-size-discrepancies.{timestamp_today()}.md')
# preponderance_df.assign
# pd.Series(name='positive preponderance', data={f'Superset': f'~{int(round(super_totals.max() / super_totals.min(), 0))}:1 odds',
# f'Mirr Sub':  f'~{int(round(mir_totals.max() / mir_totals.min(), 0))}:1 odds'}).to_frame().assign(negated=[super_totals.min(), mir_totals.min()], 
#                                                                                                   positive=[super_totals.max(), mir_totals.max()])
```


## Size Discrepancies

|              |   `neg_count` |   `pos_count` |        `N` | `neg_proportion`   | `pos_proportion`   | `pos_odds`   |
|:-------------|--------------:|--------------:|-----------:|:-------------------|:-------------------|:-------------|
| **superset** |     3,173,681 |    68,787,692 | 71,961,373 | 4.41%              | 95.59%             | **22:1**     |
| **mirr_sub** |       291,735 |     1,388,898 |  1,680,633 | 17.36%             | 82.64%             | **5:1**      |


> saved as:  
> `/share/compling/projects/sanpi/info/final_subtotals/env-size-discrepancies.2024-08-06.md`




| Polarity Approx.             |       $*E$ |      $@E$ |
|:-----------------------------|-----------:|----------:|
| **Negative Polarity Margin** |  3,173,681 |   291,735 |
| **Positive Polarity Margin** | 68,787,692 | 1,388,898 |
| $N$ (either)                 | 71,961,373 | 1,680,633 |
| **Negative Proportion**      |      4.41% |    17.36% |
| **Positive Proportion**      |     95.59% |    82.64% |
| **_Positive Preponderance_** |   **22:1** |   **5:1** |

<!-- 
| Polarity Approx. | Negative Polarity Margin | Positive Polarity Margin | `N` (either) |
|:-----------------|-------------------------:|-------------------------:|-------------:|
| $*E$             |                3,173,681 |               68,787,692 |   71,961,373 |
| $@E$             |                  291,735 |                1,388,898 |    1,680,633 |



|      | Negative Proportion | Positive Proportion | _Positive Preponderance_ |
|:----:|--------------------:|--------------------:|-------------------------:|
| $*E$ |               4.41% |              95.59% |                 **22:1** |
| $@E$ |              17.36% |              82.64% |                  **5:1** |
-->
