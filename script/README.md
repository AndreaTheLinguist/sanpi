# `./script/` Readme

The full pipeline of `sanpi` processing as of August 15, 2024 is described below.

## Each pattern category

(can also be passed in bulk, but processing is separate)

1. initial pattern match retrieval and consolidation: [`run_pipeline.py`](../run_pipeline.py)
   
   ```shell
   (sanpi) ../../sanpi$ python run_pipeline.py [ARGS]
   ```

   ```python
    usage: run_pipeline.py [-h] [-c CORPORA] [-p PATTERNDIRS] [-g GREW_OUTPUT_DIR] [-R] [-T]
                        [-E]

    simple "glue" script to initiate multiple pipes in one go. If no arguments are given,
    every corpus dir and pattern subdir in the current working directory will be run.

    options:
    -h, --help            show this help message and exit
    -c CORPORA, --corpus CORPORA
                            specify any corpus directory to be searched for pattern(s). Can
                            include as many as desired, but each one needs a flag. If none
                            specified, all `.conll` directories will be searched.
    -p PATTERNDIRS, --patterns PATTERNDIRS
                            specify pattern directory containing patterns to search for. Can
                            include as many as desired, but each one needs a flag. If none
                            specified, all patterns (`.pat` files) will be sought.
    -g GREW_OUTPUT_DIR, --grew_output_dir GREW_OUTPUT_DIR
                            specify location to direct output to other than default supplied
                            by `grew_search.py`: /share/compling/data/sanpi/1_json_grew-
                            matches
    -R, --rerun_grew_search
                            option to replace existing raw grew json output (`...raw.json`
                            files) from a previous run. If not included, previous data will
                            not be overwritten and grew search step will only be performed
                            for data directories that are incompletely populated. Raw data
                            processing scripts will still be run regardless (on existing
                            `.raw.json` files).
    -T, --tabulate_only   option to jump directly to tabulate step.Use if previous
                            processing interrupted during tabulation.
    -E, --env_check       option to confirm environment satisfies requirements before
                            running programs.
   ```

   This script calls, in turn: 

   1. `source.gather.grew_search.grew_search`: [`../source/gather/grew_search.py`](source/gather/grew_search.py)
   2. `source.gather.fill_match_info.fill_json`: [`../source/gather/fill_match_info.py`](source/gather/fill_match_info.py)
   3. `source.gather.tabulate_hits.tabulate_hits`: [`../source/gather/tabulate_hits.py`](source/gather/tabulate_hits.py)

2. Limit "triggered" results (contextualzied bigram pattern matches) to single trigger/hit per bigram: 

   * note: not applied/irrelevant for bigram baseline [`Pat/RBXadj`](../Pat/RBXadj/rb-bigram.pat)
   
   ```shell
   (sanpi) arh234@Adele:/share/compling/projects/sanpi/source/gather$ python stop_double_dipping.py -h
    usage: stop_double_dipping.py [-h] [-p PAT_CAT] [-c CORPUS_PART] [-v] [-d] [-D DATA_DIR]

    module to eliminate extraneous hits for each unique bigram_id.Can be run as a script or
    have methods imported elsewhere. Condenses the hits for a single corpus_part (e.g.
    `Pcc00`) and pattern category (e.g. `NEGmirror`) and outputs: 
    (1) `.tsv` of all removed hits, 
    (2) `.pkl.gz` of *all* hits, including double-dipping and all patterns for given category, 
    (3) an updated condensed `.pkl.gz` file with unique bigram_id values 
    (no bigramdouble-dipping) for all patterns in the category

    options:
    -h, --help            show this help message and exit
    -p PAT_CAT, --pat_cat PAT_CAT
                            Pattern category to process. Must correspond to a subdir of
                            `data/sanpi/2_hit_tables/` (and also `projects/sanpi/Pat/`)
                            (default: NEGmirror)
    -c CORPUS_PART, --corpus_part CORPUS_PART
                            corpus part (i.e. directory name containing *.conllu files) to
                            process. 1 flag per directory name. (default: bigram-PccVa)
    -v, --verbose         option to print detailed information on bigram double-dipping
                            evaluation (default: False)
    -d, --demo            Option to direct program to run on data in `./demo/` instead of
                            the default (default: False)
    -D DATA_DIR, --data_dir DATA_DIR
                            Option to set the top level data directory directly (i.e. parent
                            of `2_hits_table/`) (default: /share/compling/data/sanpi)
   ```

3. First pass of cleaning embedded in [`source/analyze/count_bigrams.py`](source/analyze/count_bigrams.py)
   (without `slurm` managment)

   ```shell
   (sanpi) arh234@Adele:/share/compling/projects/sanpi/source/analyze$ python count_bigrams.py -h

   usage: count_bigrams.py [-h] [-f N_FILES] [-t PERCENT_HITS_THRESHOLD] [-d DATA_DIR]
                           [-p POST_PROC_DIR] [-o FRQ_OUT_DIR] [-g FRQ_GROUPS] [-s]
   
   options:
   -h, --help            show this help message and exit
   -f N_FILES, --n_files N_FILES
                           number of dataframe `.pkl.gz` files to load from
                           `../hit_tables/RBXadj/` (divided by corpus chunk/slice). Files
                           are sorted by size so smaller files are selected first. (i.e.
                           `f=5` will load the 5 smallest tables of hits) (default: 2)
   -t PERCENT_HITS_THRESHOLD, --percent_hits_threshold PERCENT_HITS_THRESHOLD
                           Minimum frequency threshold of hits per word type (in summation)
                           for it to be included. **Specified as PERCENTAGE of total
                           (cleaned) hits, not as explicit integer of hits!** Any adverb or
                           adjective form which does not meet this minimum frequency
                           threshold (combined with any other form) will be dropped. NOTE:
                           This filter is applied iteratively, with sums recalculated after
                           the previous set of forms and their correpsonding bigram tokens
                           are dropped. (default: 0.001)
   -d DATA_DIR, --data_dir DATA_DIR
                           Path to location of original hit tables. (i.e. tables indexed by
                           `hit_id`). `n_files` indicates the number of files to load from
                           this directory. (default:
                           /share/compling/data/sanpi/2_hit_tables/RBXadj)
   -p POST_PROC_DIR, --post_proc_dir POST_PROC_DIR
                           Path to location for saving post processed hits. (i.e. tables
                           indexed by `hit_id`). Name of file(s) generated from `n_files`
                           and `tok_threshold` (default: /share/compling/data/sanpi/4_post-
                           processed/RBXadj)
   -o FRQ_OUT_DIR, --frq_out_dir FRQ_OUT_DIR
                           Path to location for bigram frequency results (adj_form_lower ✕
                           adv_form_lower tables). Name of file(s) generated from `n_files`
                           and `tok_threshold` (default:
                           /share/compling/projects/sanpi/results/freq_out/RBXadj)
   -g FRQ_GROUPS, --frequency_group FRQ_GROUPS
   -s, --get_stats       option to calculate in-depth descriptive statistics by axis
                           values of frequency table (default: False)
   ```

   - applied to bigram baseline (`2_hit_tables/RBXadj/*hits.pkl.gz`) only
   - `count_bigrams.py` yields an overall "clean index" of hit ids, in addition to frequency filtering and crosstabulated outputs
   
   ⚠️ **the frequency filtered hits and crosstabulated counts in `results/freq_out/` are no longer used**

   Cleaning steps in `count_bigrams` includes: 

   - drop bigrams where either `adv_lemma` or `adj_lemma` has unexpected characters

     this "odd orthography" is defined as:

     ```python
     (lemmas.str.startswith(('-', '&', '.'))
      | lemmas.str.endswith(('-', '&'))
      | lemmas.str.contains(r"[^-&\w\.][a-zA-Z]"))
     ```
     
     or, alternatively:
     
     ```python
     lemmas.str.contains(r"(?:^[&\.\[-])"
                         r"|(?:[^&\w\.-][a-zA-Z])"
                         r"|(?:[\]_&-]$)")
     ```
     
     In English, lemmas considered to have "odd orthography" are those that: 
     1. start with `-`, `&`, or `.`
     2. end with `-` or `&`
     3. or contains any character **not** in `{-, &, a-z, A-Z, 0-9, _, .}` that is then followed by a regular letter (`[a-zA-Z]`)
        📝 in hindsight, this was likely insufficient, since it doesn't account for many cases seen; e.g. `'[...]'` parsed as an adjective
   - drop sentences that are implausibly long---i.e. indication of inaccurate sentence segmentation, which probably _also_ has poor parsing quality.
     
     (or, if the "sentence" really _is_ that long, the parsing of it is still unlikely to be accurate.)

     **Max token count _allowed_ per sentence: `250`** 

     > _keep if 250. discard if 251+_

     ```python
     _MAX_TOK_PER_SENT = 250
     too_long = df.tok_in_sent > _MAX_TOK_PER_SENT
     ```

   - drop fully duplicated sentences _with more than 10 tokens_.
     
     📝 Note: This is case-sensitive! Strings where only the case differs are considered distinct.

     ```python
     over_10_tok = df.tok_in_sent > 10
     is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
     definite_duplicate = over_10_tok & is_duplicate_hit
     ```

4. the "clean index" file was then split up by corpus part post-hoc 
   using the simple script, [`chunk_index_by_file.sh`](chunk_index_by_file.sh)

   ```shell
   ../../sanpi$ bash script/chunk_index_by_file.sh [directory name] [index file name]
   ```
   
   ```shell
   DATA_DIR='/share/compling/data/sanpi'
   DEFAULT_INDEX="${DATA_DIR}/4_post-processed/RBXadj/bigram-index_clean.35f.txt"
   DF_DIR_NAME=${1:-'RBXadj'}
   INDEX_NAME=${2:-'bigram-index_clean.35f.txt'}
   ```

   Full "clean" index output from running previous `count_bigrams.py` step on the
   entirety of the corpus data available, all 35 separate parts (32 Pcc, 2 Nyt, 1 Apw)
   should have the path indicated above as the `DEFAULT_INDEX`: 

   ```shell
   "/share/compling/data/sanpi/4_post-processed/RBXadj/bigram-index_clean.35f.txt"
   ```

   `chunk_index_by_file.sh` will simply split the hit(bigram)_ids into separate `*.txt` files
   based on
   1. the original hit files found in the passed `DF_DIR_NAME`
      (assumed to be in `"${DATA_DIR}/2_hit_tables"`)
   
   and 

   2. a predefined translation that identifies the `hit_id` strings pertaining to each part

5. clean each of `RBXadj` 'hit tables' for the 35 parts: [`clean_bigrams_by_part.py`](clean_bigrams_by_part.py)

   This apply more thorough cleaning steps on each part individually, 
      processing each (`.csv`) in chunks, without ever loading the full set at the same time.^[This type of processing is not an option for pickle files, and is the primary reason that I transistioned all storage of large files to `parquet` format in later development]
      
   - prior slapdash cleaning attempted to run on _everything_ all together
   - with the data sizes as they are, it is much more efficient 
     (and therefore faster, esp. since it avoids the `OOM killer`; 
       like lots of tiny bites instead of trying to swallow something whole)

   The script gradually appends the full _clean_ information to a new `.csv.bz2` file in `../../../data/2_hit_tables/RBXadj/cleaned/`, 
   and the `hit_id` (i.e. `bigram_id` implicitly for these data) values are recorded 
   in a text file: `RBXadj/cleaned/clean*[PART]*index.txt`

---

## PBR Methods

6. After the baseline has been cleaned, each corpus part's hit_id `clean*index.txt` file filter serves as 
   a filter for the superset environments.

   The **negative polarity** superset is `RBdirect`, and its hits will have been collected and "condensed" (via "double-dipping" removals)
   in preceding steps. 

   The **positive polarity** superset is represented by `not-RBdirect`, and needs to be deduced
   from comparing the negative polarity `RBdirect` hits with the bigram baseline set `RBXadj`.

   The simple shell scripts below utilize the bash command `comm` to identify compare the negative ids
   for each part with the cleaned bigram baseline ids for it. 

   - complement ids: [`collect_com_ids.sh`](collect_com_ids.sh)
   - (clean) negative ids: [`collect_updatedNeg_ids.sh`](collect_updatedNeg_ids.sh)

   If no existing id files exist for the negated hits, 
   they can be inferred from `*.csv` files using [`get-index-from-csv.sh`](get-index-from-csv.sh).
   However! Keep in mind that the `hit_id` for environment specific hits (i.e. with a trigger node in the pattern, not just ADV ADJ)
   will not be an exact match for the `hit_id`s in RBXadj---the `bigram_id` values must be used for comparison. 
   And the complement of `RBdirect` hits needs to be determined from the `bigram_id` column.

   If the `hit_id` values are the only thing available in plain text format, they can be converted to `bigram_id` values by:
   using string manipulations to remove the first "index" following the `:` in the `hit_id` string
   e.g. 

   `hit_id=nyt_eng_20040505_0023_33:7-8-9` ➡️ `bigram_id=nyt_eng_20040505_0023_33:8-9`

   However, the `bigram_id` value should be stored in the hit tables.

7. Once the bigram_id sets are generated for each polarity, 
   The negated `RBdirect` hits need to updated to their "cleaned" index. 
   This is done using [`update_env_hits.py`](update_env_hits.py), which also applies negative specific processing if any columns startwith `'neg_'`
   - this operates on each part separately.
   - If on the cluster, there is a slurm-array script which will pass each part. 
   - If operating without `slurm`, the only required argument is `-p [CORPUS_PART]` 
     e.g. `-p Pcc23`, `-p Nyt1`, etc.
     - To run this on `NEGmirror` or `POSmirror` hits, pass the directory as well using: 
       `-d ../2_hit_tables/NEGmirror` or `-d ../2_hit_tables/POSmirror`
   
8. Then compiled into a single unified dataset, 
   using [`compile_env_from_parts.py`](compile_env_from_parts.py). 
   A final duplicate sweep will remove repetition between parts.
   - this step outputs a combined "subtotals.csv" which is used to create the "negative equivalent" sample for the positive set, 
     so it is recommended that this stage be completed for the negative set _first_ 
     i.e.
     1. `update_eng_hits.py -p [PART]` for each of the 35 parts 
     2. `compile_env_from_parts.py (--data_dir /share/compling/data/sanpi/2_hit_tables/RBdirect)`(defaults to `../RBdirect`) 
     3. _Then_ continue with next step 👇

8. The complement `not-RBdirect/` set, however, needs to "retrieved" from the baseline: 
   This is done using [`compile_com_from_parts.py`](compile_com_from_parts.py)

   It takes individual index files, creates corresponding hit tables for each, performs 
   positive polarity specific processing, then compiles them all together. 
   Once the full dataset is compiled, a final duplicate sweep can be run, to catch repetition between parts. 

   Then the `NEQ` sample will be created using the subtotals collected for RBdirect in the preceding step.
   And then the final `ALL` data is saved and viola! 

9. Prepare joint frequencies for association measure calculation: [`cat_tsvs.sh`](cat_tsvs.sh)

   Both `compile_*_from_parts.py` scripts also output corresponding `*RBdirect/ucs_format/AdvAdj_[ALL or NEQ]_*RBdirect-final-freq.tsv` files, 
   containing only `'[joint frequency]\t[adv_form_lower]\t[adj_form_lower]'` for each adverb and adjective pair with at least 1 co-occurrence. 
   e.g. 

        44441  as           good
        30092  very         good
        27548  as           bad
        26480  so           sure
        26026  quite        sure
        25656  too          late
        24459  always       easy
        24416  immediately  clear
        23250  as           easy
        21741  so           much 

   Example Log output snippet

   > ### Saving `ALL` Final Info
   > 
   > + ✓ Part Subtotals saved as  
   >   `/share/compling/data/sanpi/info/ALL_not-RBdirect_final-subtotals.csv`
   > + ✓ `hit_id` index for final selection of `not-RBdirect` hits saved as  
   >   `/share/compling/data/sanpi/2_hit_tables/not-RBdirect/ALL_not-RBdirect_final-index.txt`
   > 
   > Top 10 joint frequencies:
   > 
   >               (f  adv    adj)
   >        1,054,984  so     many
   >          692,294  most   important
   >          505,619  so     much
   >          452,725  more   likely
   >          433,550  too    much
   >          419,112  very   good
   >          375,283  most   popular
   >          372,633  as     many
   >          350,824  too    many
   >          335,616  very   important 
   > 
   > + ✓ basic `adv~adj` frequencies for final hits saved as  
   >   `/share/compling/data/sanpi/2_hit_tables/not-RBdirect/ucs_format/AdvAdj_ALL_not-RBdirect-final-freq.tsv`

   The script `cat_tsvs.sh` 
   
   1. links the `final-freq.tsv` files to `sanpi/5_freq_tsv/direct/` (if `*RBdirect`, `mirror/` if `*mirror` data)

   2. concatenates the 2 polar sets into `5_freq_tsv/ANYdirect/AdvAdj_[{ALL,NEQ}]_any-direct_final-freq.tsv` 
      (if `*RBdirect`, `ANYmirror/*any-mirror*tsv` if `*mirror` data)

   The 4 comparison spaces need to be processed: 
   1. `RBdirect/ALL`: 🏃‍♀️ `bash script/cat_tsvs.sh`
   1. `RBdirect/NEQ`: 🏃‍♀️ `bash script/cat_tsvs.sh -s`
   1. `mirror/ALL`: 🏃‍♀️ `bash script/cat_tsvs.sh -p mirror`
   1. `mirror/NEQ`: 🏃‍♀️ `bash script/cat_tsvs.sh -p mirror -s`

10. Then everything needs to be processed using `UCS`, which is run through: 
    [`polar_assoc.py`](polar_assoc.py)

    To simplify running this with the desired specifications seamlessly, use
    [`run_assoc.sh`](run_assoc.sh)
   
    e.g.
    ```shell
    ( bash script/run_assoc.sh -P mirror && bash script/run_assoc.sh -P mirror -E ) \
      > logs/associate/run_mirror_AM.`ndayh12`.log 2>&1
    
    ( bash script/run_assoc.sh && bash script/run_assoc.sh -E ) \
      > logs/associate/run_direct_AM.`ndayh12`.log 2>&1
    ```
    where `-P mirror` selects the mirror subset data
    and `-E` specifies using the `NEQ` sample comparison.