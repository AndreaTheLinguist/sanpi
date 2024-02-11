# Shell commands to view specific hits

## ⚠️ Heads up!

There is a new, more direct way to do this now.

Use the script, [`../script/sample_pickle.py`](../script/sample_pickle.py),
or import `sample_pickle` from the `source.utils.sample` module. 



---

## Rudimentary shell commands

`COLS` variable can be changed to access other columns, which are ordered as follows:

**bigram pattern columns**

1. `hit_id`
1. `colloc`
1. `sent_text`
1. `adv_form`
1. `adj_form`
1. `hit_text`
1. `text_window`
1. `sent_id`
1. `match_id`
1. `colloc_id`
1. `token_str`
1. `lemma_str`
1. `context_prev_id`
1. `context_prev_sent`
1. `context_next_id`
1. `context_next_sent`
1. `adv_lemma`
1. `adj_lemma`
1. `adv_index`
1. `adj_index`
1. `dep_mod`
1. `json_source`
1. `utt_len`
1. `category`

**`contig` pattern columns**

1. `hit_id`
1. `colloc`
1. `sent_text`
1. `neg_form`
1. `adv_form`
1. `adj_form`
1. `hit_text`
1. `text_window`
1. `sent_id`
1. `match_id`
1. `colloc_id`
1. `token_str`
1. `lemma_str`
1. `context_prev_id`
1. `context_prev_sent`
1. `context_next_id`
1. `context_next_sent`
1. `neg_lemma`
1. `adv_lemma`
1. `adj_lemma`
1. `neg_index`
1. `adv_index`
1. `adj_index`
1. `dep_neg`
1. `dep_mod`
1. `json_source`
1. `utt_len`
1. `category`

### Adjective with `text_window`

```{shell}
KEY='_favorite'; \
    N_PER_INPUT=2; \
    COLS='7'; \
    GLOB="/share/compling/data/sanpi/2_hit_tables/advadj/bigram*psv"; \
    egrep --color='always' -m $N_PER_INPUT ${KEY} ${GLOB} \
        | cut -d\| -f${COLS} | column -t -s\| \
        | egrep -i --color=always ${KEY//_/.[a-z]*.}
```

### Adverb with `sent_text`

```{shell}
KEY='mostly_'; \
    N_PER_INPUT=2; \
    COLS='3'; \
    GLOB="/share/compling/data/sanpi/2_hit_tables/advadj/bigram*psv"; \
    egrep --color='always' -m $N_PER_INPUT ${KEY} ${GLOB} \
        | cut -d\| -f${COLS} | column -t -s\| \
        | egrep -i --color=always ${KEY//_/.[a-z]*.}
```

### Full bigram/collocation with `hit_id`

```{shell}
KEY='slightly_high'; \
    N_PER_INPUT=2; \
    COLS='1-2,7'; \
    GLOB="/share/compling/data/sanpi/2_hit_tables/advadj/bigram*psv"; \
    egrep --color='always' -h -m $N_PER_INPUT ${KEY} ${GLOB} \
        | cut -d\| -f${COLS} | column -t -s\| \
        | egrep -i --color=always ${KEY//_/.[a-z]*.}
```

### All hits for specific `colloc_id`

Include `\|` at end of `ID` if `colloc_id` match desired

```{shell}
ID='pcc_eng_10_108.00011_x1730777_09:4-5\|'; \
    COLS='1-3,7-8';\
     C="${ID%%.*}"; C=${C/_eng_} ; C=${C%_*}; \
    GLOB="/share/compling/data/sanpi/2_hit_tables/*/bigram*${C^}*psv"; \
    egrep -m 2  --color=always $ID $GLOB | cut -f$COLS -d\| \
    | egrep --color=always -i \|[a-z]+_[a-z]+\| | column -t -s\|
```

```{shell}
ID='pcc_eng_10_108.00011_x1730777_09:4-5\|'; \
    COLS='1-3,7'; \
        C="${ID%%.*}"; C=${C/_eng_} ; C=${C%_*}; \
            GLOB="/share/compling/data/sanpi/2_hit_tables/*/bigram*${C^}*psv" ;\
             ls $GLOB | parallel -k \
                "cut -f$COLS -d\| {} | head -1 | column -t -s\|; \
                 egrep -m 2  --color=always $ID {} | cut -f$COLS -d\| | column -t -s\| ;\
                 echo "
```
