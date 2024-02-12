# README for `sample_pickle.py`

## Usage

```log
usage: sample_pickle.py [-h] [-p PATH] [-N SAMPLE_SIZE] [-s SORT_BY] [-c COLUMNS] [-f FILTERS] [-r]
                        [-m] [-T] [-P] [-C] [-t] [-q] [-x MAX_COLS] [-w MAX_COLWIDTH] [-W MAX_WIDTH]

simple script to print a sample of a pickled dataframe to stdout as either the default `pandas` output
or as a markdown table (-m). Specific columns can be selected (defaults to all columns), and sample
size can be dictated (defaults to 20 rows). Tip: use `-N 1 -t` to see example of all included columns

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to dataframe to sample (default:
                        /share/compling/data/sanpi/DEMO/2_hit_tables/RBdirect/condensed/DEMO-Pcc_all-
                        RBdirect_unique-bigram-id_hits.pkl.gz)
  -N SAMPLE_SIZE, --sample_size SAMPLE_SIZE
                        number of rows to include in sample. To disable sampling (show entire table--
                        use with caution! ⚠️), use `-N 0` (default: 20)
  -s SORT_BY, --sort_by SORT_BY
                        name of column to sort sample by; needn't be selected for printout. *note* this
                        will be _ascending_ (A-Z or increasing numerical values) (default: None)
  -c COLUMNS, --column COLUMNS
                        option to specify columns to print. Each must have its own `-c` flag. E.g. `-c
                        COLUMN_1 -c COLUMN_2` (default: [])
  -f FILTERS, --filter FILTERS
                        option to filter rows before sampling. Specify as a string of the format:
                        `COLUMN_NAME==VALUE` or `COLUMN_NAME!=VALUE` to invert the filter. For example,
                        to limit the sample to only rows with the adverb "absolutely", use →
                        `adv_lemma==absolutely` or `adv_form==absolutely` To only see rows where the
                        adjective is NOT "good", use → `adj_lemma!=good` or `adj_form!=good`. As with
                        the --column flag, there can be multiple filters, but every string needs its
                        own flag. NOTE: row filtering is done *before* column selection so filters may
                        be based on columns which will not be printed. (default: [])
  -r, --regex           option to interpret filter string arguments as regex patterns, instead of full
                        string matches (default: False)
  -m, --markdown        option to print in markdown table format. Note: selecting markdown formatting
                        for output forces meta-message printing, overriding any simultaneous
                        `-q/--quiet` flag. (default: False)
  -T, --tabbed          option to print tab-delimited format (default: False)
  -P, --piped           option to print pipe-delimited (|) format (default: False)
  -C, --comma           option to print in csv format (default: False)
  -t, --transpose       option to transpose the output (swap axes) for clearer viewing (default: False)
  -q, --quiet           option to suppress meta-messages printed to stdout. (Can be used with
                        `-T/--tabbed` or `-P/--piped` or `-C/--comma` to write sample to file or use
                        with `column -T [-s,/-s\|]`) (default: False)
  -x MAX_COLS, --max_cols MAX_COLS
                        max number of columns to include in sample; overriden by --column flags if
                        given (or --sample_size if --transpose specified) (default: 20)
  -w MAX_COLWIDTH, --max_colwidth MAX_COLWIDTH
                        max width (in pixels?) of each column in sample display; *currently does not
                        apply to markdown formatted displays, which include full values for every
                        included cell. (default: 40)
  -W MAX_WIDTH, --max_width MAX_WIDTH
                        max width of the entire display; *currently does not apply to markdown
                        formatted displays, which will be the sum of the widest cell in every included
                        columm (default: 180)
```

## Examples

1. single input with markdown output

    ```shell
    python script/sample_pickle.py --sample_size 5 --sort_by adj_form --markdown -c colloc -c hit_text -c neg_deprel -c neg_form -c dep_str_rel   -f ADV_lemma==that -f neg_lemma!=not   /share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc00_direct-neg-head_hits.pkl.gz
    ```

    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc00_direct-neg-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 5 random rows matching filter(s) from `bigram-Pcc00_direct-neg-head_hits.pkl.gz`
    >
    > | hit_id                                    | colloc                     | hit_text                                                   | neg_deprel   | neg_form   |
    > |:------------------------------------------|:---------------------------|:-----------------------------------------------------------|:-------------|:-----------|
    > | pcc_eng_00_054.3086_x0861678_007:4-5-6    | more_aggravating           | nothing more aggravating than when conservative candidates | amod         | nothing    |
    > | pcc_eng_00_082.1665_x1312110_5:6-7-8      | more_effective             | nothing more effective than solving worksheets .           | amod         | nothing    |
    > | pcc_eng_00_104.0095_x1666096_245:33-34-35 | particularly_extraordinary | nothing particularly extraordinary about it .              | amod         | nothing    |
    > | pcc_eng_00_085.8518_x1371846_02:4-5-6     | really_gorry               | nothing really gorry ( sp ? )                              | amod         | nothing    |
    > | pcc_eng_00_029.0997_x0454078_3:3-4-5      | more_sweeter               | nothing more sweeter then watching them grow               | amod         | nothing    |

---

2. parallel inputs with markdown output

    ```shell
    ls  /share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc[01]2_direct-*-head_hits.pkl.gz | parallel "python script/sample_pickle.py   --sample_size 3 --sort_by adj_form --markdown   -c colloc -c hit_text -c neg_deprel -c neg_form -c dep_str_rel   -f ADV_lemma==that -f neg_lemma!=not {}"
    ```

    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc02_direct-neg-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 3 random rows matching filter(s) from `bigram-Pcc02_direct-neg-head_hits.pkl.gz`
    >
    > | hit_id                                   | colloc                     | hit_text                                            | neg_deprel   | neg_form   |
    > |:-----------------------------------------|:---------------------------|:----------------------------------------------------|:-------------|:-----------|
    > | pcc_eng_02_061.1077_x0972105_28:15-16-17 | more_complicated           | nothing more complicated than air as a              | amod         | nothing    |
    > | pcc_eng_02_075.8271_x1209950_052:3-4-5   | particularly_revolutionary | nothing particularly revolutionary at all about the | amod         | nothing    |
    > | pcc_eng_02_016.3676_x0248826_74:3-4-5    | too_small                  | nothing too small or too great to                   | amod         | nothing    |
    >
    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc12_direct-neg-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 3 random rows matching filter(s) from `bigram-Pcc12_direct-neg-head_hits.pkl.gz`
    >
    > | hit_id                                    | colloc            | hit_text                                  | neg_deprel   | neg_form   |
    > |:------------------------------------------|:------------------|:------------------------------------------|:-------------|:-----------|
    > | pcc_eng_12_087.2614_x1393891_33:16-17-18  | too_cool          | ain't too cool for Zool , no              | xcomp        | ain't      |
    > | pcc_eng_12_042.8369_x0676513_23:7-8-9     | too_exciting      | nothing too exciting .                    | amod         | nothing    |
    > | pcc_eng_12_055.0436_x0873750_027:09-10-11 | earth-_shattering | nothing earth- shattering or profound , I | amod         | nothing    |
    >
    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc02_direct-adj-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 3 random rows matching filter(s) from `bigram-Pcc02_direct-adj-head_hits.pkl.gz`
    >
    > | hit_id                                   | colloc    | hit_text                                  | neg_deprel   | neg_form   |
    > |:-----------------------------------------|:----------|:------------------------------------------|:-------------|:-----------|
    > | pcc_eng_02_055.4344_x0880462_04:3-5-6    | so_easy   | never been so easy to find the best       | advmod       | never      |
    > | pcc_eng_02_101.0758_x1618135_16:32-33-34 | very_good | never very good in the high minors        | advmod       | never      |
    > | pcc_eng_02_092.0778_x1472486_034:1-3-4   | quite_new | Nothing was quite new or polished and was | nsubj        | Nothing    |
    >
    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc12_direct-adj-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 3 random rows matching filter(s) from `bigram-Pcc12_direct-adj-head_hits.pkl.gz`
    >
    > | hit_id                                   | colloc         | hit_text                                       | neg_deprel   | neg_form   |
    > |:-----------------------------------------|:---------------|:-----------------------------------------------|:-------------|:-----------|
    > | pcc_eng_12_093.5642_x1496034_19:1-3-4    | more_apparent  | Nothing is more apparent than when the Vehicle | nsubj        | Nothing    |
    > | pcc_eng_12_031.8711_x0499845_27:18-19-20 | even_available | barely even available , and if it              | advmod       | barely     |
    > | pcc_eng_12_047.2252_x0747151_44:08-10-11 | so_partisan    | never been so partisan , and never so          | advmod       | never      |

---

3. parallel inputs with `pandas` default output

    ```shell
    ls  /share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc22_direct-*-head_hits.pkl.gz | parallel "python script/sample_pickle.py   --sample_size 5 --sort_by adj_form   -c colloc -c hit_text -c neg_deprel -c neg_form -c dep_str_rel   -f ADV_lemma==that -f neg_lemma!=not {}"
    ```

    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc22_direct-neg-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 5 random rows matching filter(s) from `bigram-Pcc22_direct-neg-head_hits.pkl.gz`
    >
    > ```
    >                                                      colloc                                          hit_text neg_deprel neg_form
    > hit_id
    > pcc_eng_22_022.4606_x0346051_057:18-19-20         less_cool             nothing less cool than a multi- genre       amod  nothing
    > pcc_eng_22_010.7991_x0158096_27:6-7-8          terribly_new  nothing terribly new or groundbreaking about the       amod  nothing
    > pcc_eng_22_099.5542_x1592599_03:29-31-32         as_radical            nothing like as radical as Brook 's or       amod  nothing
    > pcc_eng_22_016.7650_x0254289_59:18-19-20        too_serious                             nothing too serious .       amod  nothing
    > pcc_eng_22_005.5264_x0073123_02:3-4-5      inherently_wrong     nothing inherently wrong with a female mutant       amod  nothing
    > ```
    >
    > ## Sampling from `/share/compling/data/sanpi/2_hit_tables/RBdirect/bigram-Pcc22_direct-adj-head_hits.pkl.gz`
    >
    > - *filtering rows...*
    >   - ✕ ERROR: Filter column `ADV_lemma` not found. Filter `ADV_lemma==that` ignored.
    >   - ✓ Applied filter: `neg_lemma!=not`
    >
    > - *selecting columns...*
    >   - Warning‼️ `dep_str_rel` not in columns. Selection ignored.
    >
    > ### 5 random rows matching filter(s) from `bigram-Pcc22_direct-adj-head_hits.pkl.gz`
    >
    > ```
    >                                                colloc                               hit_text neg_deprel neg_form
    > hit_id
    > pcc_eng_22_054.7622_x0868693_22:1-2-3         TOO_OLD                NEVER TOO OLD TO PLAY !     advmod    NEVER
    > pcc_eng_22_028.0509_x0436422_15:16-18-19   only_angry             without being only angry .       mark  without
    > pcc_eng_22_034.2781_x0537498_18:19-21-22  ever_boring                  never , ever boring .     advmod    never
    > pcc_eng_22_100.4783_x1607563_1:28-31-32     as_clever  none are quite as clever as Cardiio .      nsubj     none
    > pcc_eng_22_019.5109_x0298505_09:07-09-10    so_strong     never been so strong , yet many of     advmod    never
    > ```
