# coding=utf-8
import pandas as pd

try: 
    from utils.specific import show_interim_summary
    from utils.dataframes import Timer, print_md_table
except ModuleNotFoundError: 
    from source.utils.specific import show_interim_summary
    from source.utils.dataframes import Timer, print_md_table

def get_clean_data(df: pd.DataFrame,  # clean_index_path
                duplicate_check_only:bool =False) -> pd.DataFrame:
    # start_time = pd.Timestamp.now()

    # # > print overview of initial data
    # print('\n## Cleaning up hits: removing duplicated or exceptionally',
    #       'long sentences, strange orthography, and random capitals.')
    # starting_token_count = len(df)
    # # if clean_index_path.is_file():
    # #     clean_index = clean_index_path.read_text().splitlines()
    # #     df = df.loc[df.index.isin(clean_index), :]
    # df = _clean_data(df)

    # valid_token_count = len(df)
    # print(f'\n> {(starting_token_count - valid_token_count):,}',
    #       'total invalid hits removed during cleaning.')
    # show_interim_summary(
    #     df, title=f'Total valid/cleaned bigram hits: {valid_token_count:,}',
    #     cols_label='valid', iter_head_bullet='~')

    # print('\n[ Time to clean combined hits dataframe:',
    #       f'{get_proc_time(start_time, pd.Timestamp.now())} ]')
    
    #> Sourcery Simplification:
    with Timer() as timer:
        print('\n## Cleaning up hits: removing duplicated or exceptionally long sentences, strange orthography, and random capitals.')
        starting_token_count = len(df)
        df = _clean_data(df, duplicate_check_only)

        valid_token_count = len(df)
        print(f'\n> {starting_token_count - valid_token_count:,} total invalid hits removed during cleaning.')
        show_interim_summary(df, title=f'Total valid/cleaned bigram hits: {valid_token_count:,}', cols_label='valid', iter_head_bullet='~')

        print(f'\n[ Time to clean combined hits dataframe: {timer.elapsed()} ]')

    return df

def _clean_data(df, duplicate_check_only=False) -> pd.DataFrame:
    dirty_len = len(df)
    removals = {}
    if not duplicate_check_only:
        # * remove random capitalizations
        # > if needed anyway
        if any(f'{a}_form_lower' not in df.columns for a in ('adv', 'adj')):

            with Timer() as timer:
                print('\nNormalizing case (making everything lower)...')
                df = df.assign(adv_form_lower=df.adv_form.str.lower(),
                            adj_form_lower=df.adj_form.str.lower())
                
                # te = pd.Timestamp.now()
                show_interim_summary(df)
            
                print(f'> Time to normalize lemma case: {timer.elapsed()}')
                #       get_proc_time(ts, te), ']')
        else:
            print('\n✓ Case already normalized (to lower case).')

        # * drop abnormal orthography
        # ts = pd.Timestamp.now()
        with Timer() as timer:
        
            prior_len = len(df)
            df = _drop_odd_orth(df)
            removals['abnormal orthography'] = prior_len - len(df)
            # te = pd.Timestamp.now()
            show_interim_summary(df)        
            print(f'> Time to remove {removals["abnormal orthography"]:,} hits',
                f'due to abnormal orthography: {timer.elapsed()}')
            #   get_proc_time(ts, te))

        # * removing implausibly long, 
        if 'token_str' in df.columns:
        
            # * too long
            with Timer() as timer: 
                # _t0 = pd.Timestamp.now()
                prior_len = len(df)
                df = _drop_long_sents(df)
                removals['implausibly long sentence'] = prior_len - len(df)
                # _t1 = pd.Timestamp.now()
                show_interim_summary(df, cols_label='natural', iter_head_bullet='~')
                print(f'> Time to drop {removals["implausibly long sentence"]:,} hits from implausible "sentences":',
                        timer.elapsed())
                    # get_proc_time(_t0, _t1), ']')

    # * check for duplicate sentences
    if 'text_window' in df.columns and 'token_str' in df.columns:
        # * duplicates
        with Timer() as timer: 
            prior_len = len(df)
            show_interim_summary(
                df, cols_label='non-duplicated', iter_head_bullet='~')
            df = _drop_duplicate_sents(df)
            dup_type = "duplicates *between* corpus parts" if duplicate_check_only else 'duplicates *within* corpus part'
            removals[dup_type] = prior_len - len(df)
            print(f'> Time to drop {removals[dup_type]:,} hits from duplicated sentences:',
                timer.elapsed())
            
    removals['total'] = dirty_len - len(df)
    print_md_table(pd.Series(removals, dtype='int', name='Issue').to_frame('Hits Removed'))
    return df


def _drop_odd_orth(df: pd.DataFrame,
                   verbose=False) -> pd.DataFrame:

    print('\nRemoving lemmas with abnormal orthography...')
    J = df.adj_lemma
    J_filter = ~odd_lemma_orth(J)
    if verbose:
        meta_df = (J_filter.value_counts(normalize=True)
                   .multiply(100).round(3).to_frame('%_of_adj')
                   .assign(status=['kept', 'dropped'],
                           adj_tokens=J_filter.value_counts())
                   . set_index('status'))
        print_md_table(
            meta_df, title='ADV orthography filter outcomes', n_dec=2)

    R = df.adv_lemma
    R_filter = ~odd_lemma_orth(R)
    if verbose:
        print((R_filter.value_counts(normalize=True)
               .multiply(100).round(3).to_frame("%_of_adv")
               .assign(status=['kept', 'dropped'],
                       adv_tokens=R_filter.value_counts())
               .set_index('status').to_markdown()), '\n')

    return df.loc[J_filter & R_filter, :]


def odd_lemma_orth(lemmas: pd.Series) -> pd.Series:
    return pd.Series(
        lemmas.str.startswith(('-', '&', '.'))
        | lemmas.str.endswith(('-', '&'))
        | lemmas.str.contains(r"[^-&\w\.][a-zA-Z]", regex=True))


def _drop_long_sents(df: pd.DataFrame) -> pd.DataFrame:
    starting_df = df.copy()
    df = df.assign(tok_in_sent=df.token_str.apply(lambda s: len(s.split())))
    sent_limit = 250
    too_long = df.tok_in_sent > sent_limit
    uniq_too_long = df.loc[too_long, :].index.str.split(":",
                                                        1).str.get(0).unique()
    try:
        drop_count = too_long.value_counts()[True]
    except KeyError:
        print('No sentences are too long. Nothing dropped.')
    else:
        print(f'\nDropping {(drop_count):,} hits',
              f'from {len(uniq_too_long):,} "sentences" with',
              f'{sent_limit}+ tokens. For example:\n```')
        print((starting_df.loc[df.index.str.startswith(tuple(uniq_too_long)),
                               ['token_str']]).sample(1).squeeze()[:550] +
              '...\n```')
        df = df.loc[~too_long, :]
    return df


def _drop_duplicate_sents(df: pd.DataFrame, verbose: int = 0) -> pd.DataFrame:
    over_10_tok = df.tok_in_sent > 10
    is_duplicate_hit = df.duplicated(['token_str', 'text_window'])
    definite_duplicate = over_10_tok & is_duplicate_hit
    if any(definite_duplicate):
        print(f'\n≎ Removing {(definite_duplicate.value_counts()[True]):,}',
              'duplicate hits between input tables',
              '(provided sentence is longer than 10 tokens).')
    singletons = df.loc[~definite_duplicate,
                        # ['adv_lemma', 'adj_lemma', 'token_str']]
                        ['adv_form_lower', 'adj_form_lower', 'token_str']]
    if verbose == 1:
        all_dup = df.duplicated(['token_str', 'text_window'], keep=False)
        print('Examples of duplication:')
        print((df.loc[all_dup & over_10_tok,
                      ['tok_in_sent', 'token_str']]).sort_values(['token_str'
                                                                  ]).head(8))

    elif verbose == 2:
        init_sent_counts = df.token_str.value_counts(sort=False).sort_index()
        filter_sent_counts = singletons.token_str.value_counts(
            sort=False).sort_index()
        sent_diff = init_sent_counts - filter_sent_counts
        sent_with_dup = len(sent_diff[sent_diff != 0].index)
        print(f'  ⨳ {sent_with_dup:,} initial sentences had 1+ duplicates')
    # return singletons[['adv_lemma', 'adj_lemma']].astype('string')
    return singletons[['adv_form_lower', 'adj_form_lower']].astype('string')

# class Timer:
    
#     """
#     A context manager for measuring elapsed time using a start and end timestamp.

#     __enter__ method sets the start timestamp and returns the Timer instance.
#     __exit__ method sets the end timestamp.
#     elapsed method calculates and returns the elapsed time as a string.

#     Attributes:
#         start (pd.Timestamp): The start timestamp.
#         end (pd.Timestamp): The end timestamp.

#     Methods:
#         elapsed(): Calculates and returns the elapsed time as a string.

#     Example usage:
#         with Timer() as timer:
#             # Code to measure elapsed time

#         print(timer.elapsed())  # Output: Elapsed time in the format HH:MM:SS.S
#     """
    
#     def __enter__(self):
#         self.start = pd.Timestamp.now()
#         return self

#     def __exit__(self, *args):
#         self.end = pd.Timestamp.now()

#     def elapsed(self):
#         return get_proc_time(self.start, self.end)