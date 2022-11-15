# coding=utf-8

import argparse
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
pd.set_option('display.max_columns', 10, 'display.width', 120)
DATA_DIR = Path.home().joinpath('data')


def _parse_args():
    parser = argparse.ArgumentParser(
        description='script consolidate relevant hit data from filled json files into csv files')

    parser.add_argument('grew_match_dir', type=Path,
                        help='path to directory containing filled json files '
                             'for pattern.')
    # removed: with new data archictecture, this can be pulled from `grew_match_dir` path
    # // parser.add_argument('outputPrefix', type=str,
    # //                     help=('prefix for output file to be written to the '
    # //                           '`~/data/sanpi/2_csv_hits` subdirectory (created if necessary) '
    # //                           'found in the directory the script is run from. '
    # //                           'This should be a string which contains info about '
    # //                           'the patterns, corpus data set, and nodes counted; '
    # //                           'e.g. `Nyt1_[pattern filename]_` '
    # //                           #  'which would '
    # //                           #  'result in the output file \'freq/Nyt1_p1-n1_adv-'
    # //                           #  'adj_counts.csv\'.'
    # //                           )
    # //                     )

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    return parser.parse_args()


def tabulate_hits(match_dir):

    # json_dir = args.grew_match_dir
    if not match_dir.exists():
        sys.exit('Error: Specified json directory does not exist.')
    if not match_dir.is_dir():
        sys.exit('Error: Specified json path is not a directory.')

    hit_data = _get_hit_data(match_dir)

    hit_count = len(hit_data)
    if hit_count > 0:
        print(f'\n^_^ Finished tabulating data for {hit_count}'
              f' matching hit(s) from all json files in {match_dir}/\n'
              '-> Writing tables to csv files...')
        _create_output(hit_data, match_dir)
    else:
        sys.exit('No valid hits found. No output written.')


def _get_hit_data(json_dir):

    file_count = 0
    df_from_json = pd.DataFrame()

    # check if there are any files other than the ...raw.json files
    # processed_files = tuple(json_dir.glob('**/*[!w].json'))
    #! has to be tuple because `not [empty generator function] == True`
    processed_files = tuple(json_dir.glob('*[!w].json'))
    if not processed_files:
        sys.exit('Error: specified json directory does not contain any '
                 'processed json files.')

    for json_file in processed_files:

        file_count += 1

        print(f'-> Processing {json_file.name}...')

        with open(json_file, 'r', encoding='utf-8') as j:

            json_dicts = json.load(j)

            if len(json_dicts) < 1:

                print('--> File is empty. Skipping.')
                continue

            # > i.e. default/raw 'matching' entry replace in matchin info processing
            # >      so if it's in the dictionaries here, something went wrong
            if 'matching' in json_dicts[0].keys():
                raw_path = json_file.with_suffix('.raw.json')
                print(f'-> Warning: Node labels have not been filled for {json_file}. '
                      'Skipping file.\n     * Hint: Run FillJson.py on '
                      f'{raw_path.name} and then try again.')
                continue

        df = pd.json_normalize(json_dicts, max_level=2)

        df.columns = (df.columns.str.replace('.', '_', regex=False)
                      .str.replace('s_', '_', regex=False))

        df = (df.rename(columns={'text': 'sent_text'})
              .assign(json_source=json_file.stem))

        invert_pat = re.compile(r'(\w+)_([A-Z]+)')
        df.columns = [invert_pat.sub(r'\2_\1', label).lower()
                      for label in df.columns]

        df = _remove_redundant(df)

        df = _process_ix(df)

        df = df.convert_dtypes()

        # Note: This does not check that the adv and adj are actually true collocates
        if 'adv_form' in df.columns and 'adj_form' in df.columns:
            collocs = df.adv_form + '_' + df.adj_form
        else:
            collocs = ''
        
        #> pre-existing `hit_id` includes only sentence number, adv index, and adj index
        #>  match_ix is `[neg ix]-[adv ix]-[adj ix]`
        #   (having both adv and adj is unnecessary since they are required to be contiguous with ADV first, 
        #    but I'm sure I'd get confused about which token it is if only 1 was included)
        #> change ADV-ADJ only id to `colloc_id` and set `hit_id` to NEG-ADV-ADJ version
        df = df.assign(colloc_id=df.hit_id, 
                       hit_id=df.sent_id + ':' + df.match_ix,
                       colloc=collocs)

        df_from_json = pd.concat([df, df_from_json])

    return df_from_json


def _remove_redundant(df: pd.DataFrame()):
    is_unfilled = df.sent_text.isna()
    unfilled_rows = df.loc[is_unfilled, :]
    unfilled_ids = unfilled_rows.hit_id
    filled_ids = df.hit_id[~is_unfilled].unique()
    # reconfigure dataframe to be:
    #   all filled rows
    #   + all unfilled rows representing an otherwise unaccounted hit (not in filled rows)
    unaccounted_raw = unfilled_rows.loc[~unfilled_ids.isin(filled_ids), :]
    fdf = pd.concat([df.loc[~is_unfilled, :], unaccounted_raw])
    if unaccounted_raw.empty:
        fdf = fdf.loc[:, fdf.columns[~fdf.columns.str.contains('matching_')]]
    else:
        print('-> Warning: unfilled nonduplicate rows remaining in dataframe.')

    # then also remove any full duplicates
    #! `neg_index` required because `hit_id` is: SENT-ADV-ADJ
    keep_df = fdf.loc[~fdf.duplicated(['hit_id', 'neg_index', 'token_str']), :]
    return keep_df


def _process_ix(df):
    if any(df.token_str.isna()):
        print(' --> WARNING: empty token string(s) in json data.')
    df = df.assign(token_str=df.token_str.astype('string').fillna(''))
    # TODO: instead of calculating this from the string, pull value from length of tokens object in previous module (add utt len to json file)
    utt_len = pd.to_numeric(df.token_str.apply(lambda x: len(x.split())),
                            downcast='integer')
    ix_df = df.loc[:, df.columns.str.endswith(('index'))]
    ix_df = ix_df.fillna(0).apply(pd.to_numeric, downcast='integer')

    ix_df = ix_df.assign(hit_start_ix=pd.to_numeric(ix_df.apply(min, axis=1), downcast='integer'),
                         hit_final_ix=pd.to_numeric(ix_df.apply(max, axis=1), downcast='integer') + 1,
                         utt_len=utt_len,
                         token_str=df.token_str)
    
    # > same hit_id but one is unprocessed for some reason (unresolved bug in fill_match_info)
    # duplicate_hits = ix_df.loc[ix_df.duplicated(['token_str', 'hit_start_ix', 'hit_final_ix'], keep=False),ix_df.columns.str.endswith(('index', 'str'))].sort_values('token_str')
    # windows = list(_generate_window(ix_df))
    # ^ trying this a new way:
    win_df = ix_df.assign(ix_3_before=ix_df.hit_start_ix - 3,
                          #! +4 instead of +3 because indexing works as [start, end).
                          #    That is, start is included in selection, but end is not,
                          #    so to get e.g. word 4 through word 8, must use words[4:9]
                          ix_3_after=ix_df.hit_final_ix + 4)
    #! similarly, utt_len (len(token_str)) is fine as is
    #   (do not need to adjust for 0 indexing with `utt_len - 1`
    #   because end is not included)
    win_df = win_df.assign(win_start_ix=win_df.ix_3_before.apply(lambda x: max(x, 0)),
                           win_final_ix=win_df.loc[:, ['ix_3_after', 'utt_len']].min(axis=1))

    win_df = win_df.assign(
        win_str=pd.Series(win_df.index).apply(
            lambda i: ' '.join(win_df.at[i, 'token_str']
                               .split()[win_df.win_start_ix[i]:win_df.win_final_ix[i]])
        ),
        hit_str=pd.Series(win_df.index).apply(
            lambda i: ' '.join(win_df.at[i, 'token_str']
                               .split()[win_df.hit_start_ix[i]:win_df.hit_final_ix[i]])
        )
    )

    #? Is this still used/needed? Pretty sure the hit_id column already exists at this point now
    #? Are the numbers different than the hit id numbers? i.e. actual index values?
    # select index int columns to be used in creating hit id
    tok_ix_df = ix_df.loc[:, ix_df.columns.str.startswith(
        ('neg', 'adv', 'adj'))].apply(lambda c: c.astype('string'))

    df = df.assign(match_ix=tok_ix_df.apply(lambda x: '-'.join(x), axis=1),
                   hit_text=win_df.hit_str,
                   text_window=win_df.win_str, 
                   utt_len=win_df.utt_len)
    return df


# def _generate_window(df):
    # # todo: had issue with some sort of error. tried changing types and messing around with stuff--see if it has been fixed?
    # for row in df.index:
    #     # hit_start_ix = df.at[row, 'hit_start_ix']
    #     # hit_final_ix = df.at[row, 'hit_final_ix']
    #     go_back_2 = df.hit_start_ix[row] - 2
    #     go_forward_2 = df.hit_final_ix[row] + 2

    #     w0 = max(0, go_back_2)
    #     w1 = min(df.utt_len[row],
    #              go_forward_2) + 1

    #     yield ' '.join(df.token_str[row].split()[w0:w1])


def _create_output(hits_df, match_dir, verbose=False):

    # home/arh234/data/sanpi/1_json_grew-matches/immediateNeg/PccVa.without-relay
    pat_category = match_dir.parent.name
    output_dir = Path(*(match_dir.parts[:-3] + ('2_csv_hits', pat_category)))

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    hits_df = hits_df.set_index('hit_id')
    hits_df = hits_df.assign(category=pat_category).convert_dtypes()
    hit_cols = hits_df.columns

    # set given columns as categories (to reduce memory impact)
    catcols = hit_cols.str.endswith(('form', 'lemma','category',
                                            'relation', 'json_source'))
    # catcols = ['colloc', 'adv_form', 'adj_form',
            #    'neg_form', 'nr_form', 'json_source', 'category',
            #    # 'mit_form', pos_form, test_form
            #    ]
    # for col in catcols:
        # if col not in hit_cols:
        #     hits_df[col] = '?'
    mem_init = hits_df.memory_usage(deep=True)
    hits_df.loc[:, catcols] = hits_df.loc[:, catcols].astype('category')
    mem_cat=hits_df.memory_usage(deep=True)
    numeric_cols = hit_cols.str.endswith(('_len','index'))
    hits_df.loc[:, numeric_cols] = hits_df.loc[:, numeric_cols].apply(pd.to_numeric, 
                                                                      downcast='unsigned')
    mem_cat_down=hits_df.memory_usage(deep=True)
    print(pd.DataFrame([mem_init, mem_cat, mem_cat_down]).transpose())
    # sort columns of dataframe
    required_cols = ['colloc', 'sent_text']
    priority_cols = [c for c in hit_cols
                     if c in ('hit_text', 'text_window', 'neg_form',
                              'adv_form', 'adj_form', 'relay_form', 'nr_form')]
    other_cols = [c for c in hit_cols
                  if c not in priority_cols + required_cols]
    hits_df = hits_df[required_cols + priority_cols + other_cols]

    # write rows to file

    fstem = f"{match_dir.name.replace('.', '_')}_hits"
    hits_df.to_csv(output_dir.joinpath(f'{fstem}.csv'))
    #! psv/pipe delimited (`|`) required because table includes commas (`,`)
    hits_df.to_csv(output_dir.joinpath(f'{fstem}.psv'), sep='|')
    hits_df.to_pickle(output_dir.joinpath(f'{fstem}.pkl.gz'))

    view_sample_size = min(5, len(hits_df))

    if verbose:
        try:
            print_table = hits_df[['neg_form', 'colloc', 'sent_text']].sample(
                view_sample_size).to_markdown()
        except ImportError:
            pass
        else:
            print('```\n#### Data Sample\n')
            print(print_table)
            print('```')


if __name__ == '__main__':
    absStart = time.perf_counter()
    # print("```\n### Tabulating hits via `tabulateHits.py`...\n```")
    args = _parse_args()

    tabulate_hits(*args)

    absFinish = time.perf_counter()
    print(f'\nTime elapsed: {round(absFinish - absStart, 3)} seconds\n'
          '====================================\n')
