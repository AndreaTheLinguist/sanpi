
# `[DATA_DIR]/3_dep_info/` addition

Feb 15, 2023

*The following discusses the `./demo/data/`* directory specifically, but the same
structuring will hold for the main `/share/compling/data/sanpi/` directory.*

There are some new tables in
[`./demo/data/3_dep_info/` (github link)](https://github.com/AndreaTheLinguist/sanpi/tree/master/demo/data/3_dep_info).

## At the top level, there are 5 subdirectories

### 4 of these corresponding dataframes with added info for identifying dependency relationships for a hit

- They match the structuring `../2_hit_tables/`:
  - `advadj` for all instances of adverb-adjective collocations
  - 3 "negative polarity" (a.k.a. $NegPol$) pattern collections
  - `contig` for collocations (`ADV` + `ADJ` node bigrams) with a ***contig**uous*
  dependency relationship to an identified negative element (`NEG` node)
  - `scoped` for collocations with a single intervening dependency relationship
  between the `ADJ` node and the `NEG` node.
  - `raised` for collocations with an identified *neg-raising* element intervening between
  the `ADJ` (or, in `scoped` cases, `RELAY`) node and the `NEG` node.
- Within these subdirectories, there are 2 dataframes per dataset.
  - following the naming schema of
    > [filestem of input (from `2_hit_tables/`)]{`+deps`, `_dep-node-info`}`.pkl.gz`
  - e.g.
    - `../exactly_puddin-val_sans-relay_hits+deps.pkl.gz`\
      is `exactly_puddin-val_sans-relay_hits` with added columns
      for variations of dependency string identifiers

    - `../exactly_puddin-val_sans-relay_hits_dep-node-info.pkl.gz`

      is a reconfiguration of the `dep_[node]` columns in
      `exactly_puddin-val_sans-relay_hits` ,
      plus the added dependency string identifier columns,
      with every dependency relationship indexed by both the `hit_id`
      and an ordinal node index (i.e. `0`-`3`).

      That is, this table has more than 1 row per `hit_id`
      (each `advadj` hit has only 1 dependency relationship (`dep_mod`),
      but all the $NegPol$ patterns produce at least 2 `dep_mod` & `dep_neg`,
      with optional `dep_relay` and `dep_raised` dependencies as well).

### The final directory at the top level is `../crosstab`

This contains crosstabulations
of columns in the `...hits+deps` dataframes concatonated.

- depending on the `rows` value given to `panas.crosstab()`,
  corresponding to the vertical index,these are either
  - boolean tables in the format of `1` and `0` values
    (running `.astype('bool')` on the dataframe will convert them to `True` and `False`)
  - or frequency tables where the values represent the number of times the
    `[row, column]` combination appears in the data
- there are also a `SUM` row and column, and the `[SUM, SUM]` cell
    represents the total number of rows in the dataset

    📍*Note: the `SUM` values have to be dropped for the boolean conversion to work*
    *(can only interpret 0s and 1s into boolean values)*
- These "cross-tables" are organized in subdirectories of `../crosstab/` corresponding to
    the selected `cross` column (i.e. the `rows` parameter value passed to the function)

- Each subdirectory of "cross-tables" (in `.csv` format), also contain a `.md` file
    summarizing the top values for each crosstabulation
    (and how many rows were defined for the given columns)
    as well as the full path to the output.
  - The `hit_id`  cross-table, i.e. the boolean tables, are summarized in
    [`../crosstab/hit_id/demo_exactly_X-hit_id_info.md` (github link)](https://github.com/AndreaTheLinguist/sanpi/blob/master/demo/data/3_dep_info/crosstab/hit_id/demo_exactly_X-hit_id_info.md)

  - ⁂ Notes:
    - **These values include `advadj` hits which overlap with the $NegPol$ pattern hits**
    - The 'most frequent' tables are identical between
          the different "crosses" though, unless the given `cross` column
          is undefined for some of the initial rows. (e.g. `neg_lemma`)

## 👀 Example Crosstabulation Summary Excerpt

> ## `category` x `hit_id`
>
> - *both values defined for 302 rows*
>
> - Full crosstabulation dataframe saved to
>   `data/3_dep_info/crosstab/hit_id/demo_exactly_X-hit_id_category.csv`
>
> ### 5 most common `category` values
>
> | category   |   SUM |
> |:-----------|------:|
> | advadj     |   193 |
> | contig     |   102 |
> | scoped     |     4 |
> | raised     |     3 |
>
>
> ## `colloc` x `hit_id`
>
> - *both values defined for 302 rows*
>
> - Full crosstabulation dataframe saved to
>   `data/3_dep_info/crosstab/hit_id/demo_exactly_X-hit_id_colloc.csv`
>
> ### 5 most common `colloc` values
>
> | colloc              |   SUM |
> |:--------------------|------:|
> | exactly_sure        |    44 |
> | exactly_clear       |    12 |
> | exactly_right       |    12 |
> | exactly_alike       |     5 |
> | exactly_appropriate |     4 |
>
> ...
>
> ## `dep_str` x `hit_id`
>
> - *both values defined for 302 rows*
>
> - Full crosstabulation dataframe saved to
>   `data/3_dep_info/crosstab/hit_id/demo_exactly_X-hit_id_dep-str.csv`
>
> ### 5 most common `dep_str` values
>
> | dep_str                              |   SUM |
> |:-------------------------------------|------:|
> | sure>exactly[=mod]                   |    22 |
> | sure>not[=neg]; sure>exactly[=mod]   |    22 |
> | right>exactly[=mod]                  |    12 |
> | clear>exactly[=mod]                  |     6 |
> | clear>not[=neg]; clear>exactly[=mod] |     5 |
>
> ...
>
> ## `dep_str_mask` x `hit_id`
>
> - *both values defined for 302 rows*
>
> - Full crosstabulation dataframe saved to
>   `data/3_dep_info/crosstab/hit_id/demo_exactly_X-hit_id_dep-str-mask.csv`
>
> ### 5 most common `dep_str_mask` values
>
> | dep_str_mask   |   SUM |
> |:---------------|------:|
> | JJ>RB          |   179 |
> | JJ>not; JJ>RB  |   100 |
> | JJ>RBS         |     4 |
> | JJ>RBR         |     3 |
> | JJR>RB         |     3 |
>
