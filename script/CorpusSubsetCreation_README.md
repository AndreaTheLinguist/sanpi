# Making Corpus Subsets

## As a `slurm` job

To create the subsets as a `slurm` job, use `mkbigram` alias like so:
  (from anywhere with `sanpi` conda env)

  ```shell
  DIR=/share/compling/data/new_york_times; mkbigram
  DIR=/share/compling/data/puddin/puddin_1; mkbigram
  ```

  > [!WARNING] DIR must be absolute path.

- aliases employed
  - `mklog`
    ```shell
    alias mklog='LOGSTEM="/share/compling/data/sanpi/logs/`basename $DIR`/make_${NAME}_subset.`date +%y-%m-%d_%H%M`"; 
      mkdir -p $(dirname $LOGSTEM); echo "sending stdout & stderr to $LOGSTEM..."'
    ```
  - `runselect`    
    ```shell
    alias runselect='echo "bash /share/compling/projects/sanpi/script/select_for_subset.sh $DIR $NAME \"--requeue\" 1>$LOGSTEM.out 2>$LOGSTEM.err"; \
      bash /share/compling/projects/sanpi/script/select_for_subset.sh $DIR $NAME "--requeue" \
      1>$LOGSTEM.out 2>$LOGSTEM.err && echo "Script run successful. Closed @ `date`"'
    ```

    > [!TIP] To request different (non-default) memory or time allotments (or other slurm parameters)
    > add, e.g., `"--mem=15G -t1:00:00"` to `"--requeue"` string above (following `bash` commmand, not just `echo` command)
  - **`mkdir`**
    ```shell
    ## needs DIR!! (must be ABSOLUTE)
    alias mkbigram='NAME=bigram; echo -e "\nInitiating ${NAME} subset processing for ..${DIR#*compling}/\n== `date` =="; mklog; runselect'
    ```

### Call Order

1. `mkbigram` alias calls (`mklog` and) `runselect` alias, which calls **`./script/select_for_subset.sh`**
2. `./script/select_for_subset.sh` calls the slurm script **`./slurm/grewpy_subset.slurm.sh`**
   - I believe one of these shell scripts activates the `parallel-sanpi` env, so if that doesn't exist:
     - either create using the file `setup/parallel-sanpi_env.yml` following instructions in `setup/README.md`
     - or tweak the shell scripts to get around it (use a different env or not activate any from within the script)
3. the slurm script `grewpy_subset.slurm.sh` finally calls **`./script/create_grewpy_subset.py`**
   - example:

     ```shell
     time python "/share/compling/projects/sanpi/script/create_grewpy_subset.py" -n 'bigram' \
       "/share/compling/data/puddin/PccTe.conll/pcc_eng_test-01.conllu"`
     ```

   - help message
     > [!NOTE] The default pattern file path was obsolete/no longer existed. This 👇 has the updated path.

     ```log
     usage: create_grewpy_subset.py [-h] [-p PAT_PATH] [-n SUBSET_NAME] conllu_path
 
     positional arguments:
       conllu_path           path to `.conllu` file to get subset of
 
     options:
       -h, --help            show this help message and exit
       -p PAT_PATH, --pat_path PAT_PATH
                             path to `.pat` file for pattern to match (default:
                             /share/compling/projects/sanpi/Pat/RBXadj/rb-bigram.pat)
       -n SUBSET_NAME, --subset_name SUBSET_NAME
                             optional string to use as output file label for subset. If none given,
                             `pat_path` filestem will be used. Output path template: [conllu_path
                             parent]/subset_[label]/[label]:[conllu_path stem].{context.psv, conllu}
                             (default: None)
     ```

## Using the `python` script directly

To create the subset one conllu file at a time, just directly call it as indicated above

## Extra Post-Processing

To restructure storage of final outputs, I used this command:

```shell
(parallel-sanpi) arh234@compling-compute-02:~$ C=/share/compling/data/sanpi/corpora_shortcuts/debug; \
  N=/share/compling/data/sanpi/subsets/bigram_`basename $C`; echo $N; mkdir -p $N; cd $N; \
  ls $C/*conll/subset_bigram/*conllu \
  | parallel -k "echo -e '\nLinking {}'...; B=\$(basename {});\
      echo \"    \$(du -h --time {} | cut -d/ -f1)\$B\"; \
      D=\$(basename \$(dirname \$(dirname {}))); \
      S=bigram-\${D%.conll}; \
      mkdir -p \$S; echo \"  linkname -> \$S/\$B\"; \
      ln -s {} \$S/\$B" && ls */*conllu | head -3 \
      | parallel "echo; echo {}; echo '-------------------------------------------'; head {}"
/share/compling/data/sanpi/subsets/bigram_debug

Linking /share/compling/data/sanpi/corpora_shortcuts/debug/apw.conll/subset_bigram/BIGRAM.apw_eng_199911.conllu...
    100K        2023-04-02 23:53        BIGRAM.apw_eng_199911.conllu
  linkname -> bigram-apw/BIGRAM.apw_eng_199911.conllu

Linking /share/compling/data/sanpi/corpora_shortcuts/debug/apw.conll/subset_bigram/BIGRAM.apw_eng_200412.conllu...
    4.5M        2023-03-31 19:49        BIGRAM.apw_eng_200412.conllu
  linkname -> bigram-apw/BIGRAM.apw_eng_200412.conllu

Linking /share/compling/data/sanpi/corpora_shortcuts/debug/nyt.conll/subset_bigram/BIGRAM.nyt_eng_200402.conllu...
    5.0M        2023-03-31 19:48        BIGRAM.nyt_eng_200402.conllu
  linkname -> bigram-nyt/BIGRAM.nyt_eng_200402.conllu

Linking /share/compling/data/sanpi/corpora_shortcuts/debug/nyt.conll/subset_bigram/BIGRAM.nyt_eng_200405.conllu...
    1.3M        2023-03-31 19:47        BIGRAM.nyt_eng_200405.conllu
  linkname -> bigram-nyt/BIGRAM.nyt_eng_200405.conllu

bigram-apw/BIGRAM.apw_eng_199911.conllu
-------------------------------------------
# sent_id = apw_eng_19991101_0059_18
# text = Katz , an adviser to local governments and an expert on stadium financing , has tried to position himself as a moderate best able to build on the economic recovery generated under popular two-term Mayor Edward G. Rendell .
1       Katz    Katz    _       NNP     _       16      nsubj   16:nsubj        _
2       ,       ,       _       ,       _       0       -       0:-     _
3       an      a       _       DT      _       4       det     4:det   _
4       adviser adviser _       NN      _       1       appos   1:appos _
5       to      to      _       TO      _       4       prep    4:prep  _
6       local   local   _       JJ      _       7       amod    7:amod  _
7       governments     government      _       NNS     _       5       pobj    5:pobj  _
8       and     and     _       CC      _       4       cc      4:cc    _

bigram-apw/BIGRAM.apw_eng_200412.conllu
-------------------------------------------
# sent_id = apw_eng_20041227_0001_12
# text = Many worshippers said they did n't know about the earthquake until they arrived at Mass because they had been too tired from Christmas activities to watch television news .
1       many    many    _       JJ      _       2       amod    2:amod  _
2       worshippers     worshipper      _       NNS     _       3       nsubj   3:nsubj _
3       said    say     _       VBD     _       0       root    0:root  _
4       they    they    _       PRP     _       7       nsubj   7:nsubj _
5       did     did     _       AUXD    _       7       dep     7:dep   _
6       n't     not     _       RB      _       7       neg     7:neg   _
7       know    know    _       VB      _       3       ccomp   3:ccomp _
8       about   about   _       IN      _       7       prep    7:prep  _

bigram-nyt/BIGRAM.nyt_eng_200402.conllu
-------------------------------------------
# sent_id = nyt_eng_20040229_0052_34
# text = Of the newcomers , Posada said he was most comfortable with Vazquez , a former Expo , because they are fellow Puerto Ricans and played against each other in winter ball .
1       of      of      _       IN      _       6       prep    6:prep  _
2       the     the     _       DT      _       3       det     3:det   _
3       newcomers       newcomer        _       NNS     _       1       pobj    1:pobj  _
4       ,       ,       _       ,       _       0       -       0:-     _
5       Posada  Posada  _       NNP     _       6       nsubj   6:nsubj _
6       said    say     _       VBD     _       0       root    0:root  _
7       he      he      _       PRP     _       10      nsubj   10:nsubj        _
8       was     be      _       VBD     _       10      cop     10:cop  _
(parallel-sanpi) arh234@compling-compute-02:/share/compling/data/sanpi/subsets/bigram_debug$
```
