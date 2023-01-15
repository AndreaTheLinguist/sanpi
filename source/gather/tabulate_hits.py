# coding=utf-8

import argparse
import json
import logging
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

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    return parser.parse_args()


def tabulate_hits(match_dir: Path):
    start_time = time.perf_counter()
    print(time.strftime("%Y-%m-%d_%I:%M%p"))
    log_dir = Path(*match_dir.parents._parts[:-3], 'logs', match_dir.name)
    if not log_dir.is_dir():
        log_dir.mkdir(parents=True)
    log_file = log_dir.joinpath(f'tabulate_{time.strftime("%Y-%m-%d_%R")}.log')
    print(f'Log will be saved to: {log_file}')
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
    # logging.debug('This message should NOT go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    logging.info('Tabulating hits from json files in %s', str(match_dir))
    # json_dir = args.grew_match_dir
    if not match_dir.exists():
        logging.error('Specified json directory does not exist.')
        sys.exit('Error: Specified json directory does not exist.')
    if not match_dir.is_dir():
        logging.error('Specified json path is not a directory.')
        sys.exit('Error: Specified json path is not a directory.')

    hit_data = _get_hit_data(match_dir)

    hit_count = len(hit_data)
    if hit_count > 0:
        logging.info(
            ('\n^_^ Finished tabulating data for %i matching hit(s) '
             'from all json files in %s/\n-> Writing tables to csv files...'),
            hit_count,
            str(match_dir))
        print(f'\n^_^ Finished tabulating data for {hit_count}'
              f' matching hit(s) from all json files in {match_dir}/\n'
              '-> Writing tables to csv files...')

        _create_output(hit_data, match_dir, start_time)
    else:
        logging.warning('No valid hits found. No hits table created. '
                        '=> Make sure this is because no matches were found!')
        print('No valid hits found. No hits table created.')
        sys.exit()


def _get_hit_data(json_dir):

    file_count = 0
    df_from_json = pd.DataFrame()

    # check if there are any files other than the ...raw.json files
    # processed_files = tuple(json_dir.glob('**/*[!w].json'))
    #! has to be tuple because `not [empty generator function] == True`
    processed_files = tuple(json_dir.glob('*[!w].json'))
    if not processed_files:
        logging.error(
            'Specified json directory does not contain any processed json files.')
        sys.exit('Error: specified json directory does not contain any '
                 'processed json files.')

    for json_file in processed_files:

        file_count += 1

        logging.info('-> Processing %s...', json_file.name)
        # print(f'-> Processing {json_file.name}...')

        with open(json_file, 'r', encoding='utf-8') as j:

            json_dicts = json.load(j)

            if len(json_dicts) < 1:

                print('--> File is empty. Skipping.')
                continue

            # > i.e. default/raw 'matching' entry replace in `fill_match_info`
            # >      so if it's in the dictionaries here, something went wrong
            if 'matching' in json_dicts[0].keys():
                raw_path = json_file.with_suffix('.raw.json')
                logging.warning(
                    'Node labels have not been filled for %s}. Skipping file. (** Hint: Run fill_match_info.py on %s and then try again.)', json_file, raw_path.name)
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

        #   (having both adv and adj is unnecessary since they are required to be contiguous with ADV first,
        #    but I'm sure I'd get confused about which token it is if only 1 was included)
        # > `hit_id` ->  NEG-ADV-ADJ
        # > `colloc_id` ->  ADV-ADJ (only)
        df = df.assign(hit_id=df.sent_id+':'+df.match_ix,
                       colloc_id=df.sent_id+':' +
                       df.adv_index.astype('string')+'-' +
                       df.adj_index.astype('string'),
                       colloc=collocs)

        df_from_json = pd.concat([df, df_from_json])

    return df_from_json


def _remove_redundant(df: pd.DataFrame()):
    logging.info('removing redundant pattern matches...')
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
        logging.warning('Unfilled nonduplicate rows remaining in dataframe.')
        print('-> Warning: unfilled nonduplicate rows remaining in dataframe.')

    # then also remove any full duplicates
    keep_df = fdf.loc[~fdf.duplicated(['hit_id', 'token_str']), :]
    return keep_df


def _process_ix(df):
    if any(df.token_str.isna()):
        logging.warning('Empty token string(s) in json data.')
    df = df.assign(token_str=df.token_str.astype('string').fillna(''))
    # TODO: instead of calculating this from the string, pull value from length of tokens object in previous module (add utt len to json file)
    utt_len = pd.to_numeric(df.token_str.apply(lambda x: len(x.split())),
                            downcast='integer')
    ix_df = df.loc[:, df.columns.str.endswith(('index'))]
    ix_df = ix_df.fillna(0).apply(pd.to_numeric, downcast='integer')

    ix_df = ix_df.assign(hit_start_ix=pd.to_numeric(ix_df.apply(min, axis=1), downcast='integer'),
                         hit_final_ix=pd.to_numeric(ix_df.apply(
                             max, axis=1), downcast='integer') + 1,
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

    # ? Is this still used/needed? Pretty sure the hit_id column already exists at this point now
    # ? Are the numbers different than the hit id numbers? i.e. actual index values?
    # select index int columns to be used in creating hit id
    tok_ix_df = ix_df.loc[:, ix_df.columns.str.startswith(
        ('neg', 'adv', 'adj'))].apply(lambda c: c.astype('string'))

    df = df.assign(match_ix=tok_ix_df.apply(lambda x: '-'.join(x), axis=1),
                   hit_text=win_df.hit_str,
                   text_window=win_df.win_str,
                   utt_len=win_df.utt_len)
    return df


# // def _generate_window(df):
    # //
    # // for row in df.index:
    # //     # hit_start_ix = df.at[row, 'hit_start_ix']
    # //     # hit_final_ix = df.at[row, 'hit_final_ix']
    # //     go_back_2 = df.hit_start_ix[row] - 2
    # //     go_forward_2 = df.hit_final_ix[row] + 2
    # //
    # //     w0 = max(0, go_back_2)
    # //     w1 = min(df.utt_len[row],
    # //              go_forward_2) + 1
    # //
    # //     yield ' '.join(df.token_str[row].split()[w0:w1])


def _create_output(hits_df, match_dir, start_time):
    logging.info('creating outputs...')
    # home/arh234/data/sanpi/1_json_grew-matches/immediateNeg/PccVa.without-relay
    pat_category = match_dir.parent.name
    output_dir = Path(*(match_dir.parts[:-3] + ('2_hit_tables', pat_category)))

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    hits_df = hits_df.set_index('hit_id')
    hits_df = hits_df.assign(category=pat_category).convert_dtypes()
    hit_cols = hits_df.columns

    # set given columns as categories (to reduce memory impact)
    catcols = hit_cols.str.endswith(('form', 'lemma', 'category',
                                     'relation', 'json_source'))
    # catcols = ['colloc', 'adv_form', 'adj_form',
    #    'neg_form', 'nr_form', 'json_source', 'category',
    #    # 'mit_form', pos_form, test_form
    #    ]
    # for col in catcols:
    # if col not in hit_cols:
    #     hits_df[col] = '?'
    # mem_init = hits_df.memory_usage(deep=True)
    # TODO: update this to avoid future error
    # ^  FutureWarning: In a future version, `df.iloc[:, i] = newvals` will
    # ^  attempt to set the values inplace instead of always setting a new array.
    # ^  To retain the old behavior, use either `df[df.columns[i]] = newvals`
    # ^  or, if columns are non-unique, `df.isetitem(i, newvals)`
    hits_df.loc[:, catcols] = hits_df.loc[:, catcols].astype('category')

    # mem_cat=hits_df.memory_usage(deep=True)
    numeric_cols = hit_cols.str.endswith(('_len', 'index'))
    hits_df.loc[:, numeric_cols] = hits_df.loc[:, numeric_cols].apply(pd.to_numeric,
                                                                      downcast='unsigned')
    # mem_cat_down=hits_df.memory_usage(deep=True)
    # print(pd.DataFrame([mem_init, mem_cat, mem_cat_down]).transpose())
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
    # ? Is this true? ^^
    hits_df.to_csv(output_dir.joinpath(f'{fstem}.psv'), sep='|')
    hits_df.to_pickle(output_dir.joinpath(f'{fstem}.pkl.gz'))

    view_sample_size = min(5, len(hits_df))
    print_cols = hits_df.columns[hits_df.columns.isin(
        ('neg_form', 'colloc', 'sent_text'))]
    try:
        print_table = hits_df[print_cols].sample(
            view_sample_size).to_markdown()

    except ImportError:
        print_table = hits_df[print_cols].sample(
            view_sample_size).to_string()

    logging.info('Sample of Tabulated Data:\n%s\n', print_table)
    print('\n#### Data Sample ####\n')
    print(print_table+'\n')

    finish_time = time.perf_counter()
    dur_str = dur_round(finish_time - start_time)
    print(f'Time to tabulate hits: {dur_str}')
    logging.info('Tabulation Step Complete! Time elapsed: %s', dur_str)


def dur_round(time_dur: float):
    """take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits

    Args:
        dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "m"

        if time_dur >= 60:
            time_dur = time_dur / 60
            unit = "h"

    if time_dur < 10:
        dur_str = f"{round(time_dur, 2):.2f}{unit}"
    else:
        dur_str = f"{round(time_dur, 1):.1f}{unit}"

    return dur_str


if __name__ == '__main__':
    absStart = time.perf_counter()
    # print("```\n### Tabulating hits via `tabulateHits.py`...\n```")
    args = _parse_args()

    tabulate_hits(*args)

    absFinish = time.perf_counter()
    print(f'\nTime elapsed: {round(absFinish - absStart, 3)} seconds\n'
          '====================================\n')
