# coding=utf-8

import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path

import pandas as pd

from source.utils import get_proc_time, print_md_table
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 120)
DATA_DIR = Path.cwd().joinpath('data')
if not DATA_DIR.is_dir():
    DATA_DIR = Path.home().joinpath('data')
    if not DATA_DIR.is_dir():
        DATA_DIR.mkdir()
# TIMESTAMP = time.perf_counter
TIMESTAMP = pd.Timestamp.now
MARGIN_SIZE = 4


def _parse_args():
    parser = argparse.ArgumentParser(
        description='script consolidate relevant hit data from filled json files into tables')

    parser.add_argument('grew_match_dir', type=Path,
                        help='path to directory containing filled json files '
                             'for pattern.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Option to increase verbosity of console output')

    return parser.parse_args()


def tabulate_hits(match_dir: Path, redo=False):
    start_time = TIMESTAMP()
    print(time.strftime("%Y-%m-%d @ %I:%M%p"))
    if check_for_prior(match_dir) and not redo:
        return

    print(f' ~ Grew Match Directory: {match_dir}')
    log_dir = Path(*match_dir.parts[:-3], 'logs', 'tabulate', match_dir.name)
    # print(f'Tabulate log destination: {log_dir}')
    if not log_dir.is_dir():
        log_dir.mkdir(parents=True)
    log_file = log_dir.joinpath(
        f'tabulate_{time.strftime("%Y-%m-%d_%R".replace(":",""))}.log')
    print(f'Log will be saved to: `{log_file}`')

    # Logging snippets:
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # logging.debug('This message should NOT go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö'

    logging.basicConfig(filename=log_file, encoding='utf-8',
                        # level=logging.DEBUG,
                        level=logging.INFO,
                        # level=logging.WARNING,
                        format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

    logging.info('Tabulating hits from json files in %s', str(match_dir))
    if not match_dir.exists():
        logging.error('Specified json directory does not exist.')
        sys.exit('Error: Specified json directory does not exist.')
    if not match_dir.is_dir():
        logging.error('Specified json path is not a directory.')
        sys.exit('Error: Specified json path is not a directory.')

    hit_data = _get_hit_data(match_dir)
    if hit_data.empty:
        return
    hit_count = len(hit_data)
    if hit_count > 0:
        logging.info(
            ('\n✔ Finished tabulating data for %i matching hit(s) '
             'from all json files in %s/\n-> Writing tables to files...'),
            hit_count,
            str(match_dir))
        print(f'\n✔ Finished tabulating data for {hit_count}'
              f' matching hit(s) from all json files in {match_dir}/\n'
              '-> Writing tables to files...')

        _create_output(hit_data, match_dir, start_time)
    else:
        logging.warning('No valid hits found. No hits table created. '
                        '=> Make sure this is because no matches were found!')
        print('No valid hits found. No hits table created.')
        sys.exit()


def check_for_prior(match_dir: Path) -> bool:
    out = get_csv_path(match_dir).with_suffix('.pkl.gz')
    if out.is_file() and out.stat().st_size > 0:
        print('Tabulation output files already exist and are non-empty. Processing Complete.\n  ',
              f'See {out}\n')
        return True
    return False


def _get_hit_data(json_dir):

    file_count = 0
    json_dir_df = pd.DataFrame()

    # check if there are any files other than the ...raw.json files
    # processed_files = tuple(json_dir.glob('**/*[!w].json'))
    #! has to be tuple because `not [empty generator function] == True`
    processed_files = tuple(json_dir.glob('*[!w].json'))
    if not processed_files:
        logging.error(
            'Specified json directory does not contain any processed json files.')
        print('Error: specified json directory does not contain any '
              'processed json files.')
        return pd.DataFrame()

    for json_file in processed_files:

        file_count += 1

        logging.info('-> Processing %s...', json_file.name)
        print(f'-> Processing {json_file.name}...')

        with open(json_file, 'r', encoding='utf-8') as j:

            jl0 = TIMESTAMP()
            json_dicts = json.load(j)
            jl1 = TIMESTAMP()
            jl_time = f'  Time to load json: {get_proc_time(jl0, jl1)}'
            logging.info(jl_time)
            # print(jl_time)

            if len(json_dicts) < 1:
                print('--> File is empty. Skipping.')
                continue

            # > i.e. default/raw 'matching' entry replace in `fill_match_info`
            # >      so if it's in the dictionaries here, something went wrong
            if 'matching' in json_dicts[0].keys():
                raw_path = json_file.with_suffix('.raw.json')
                logging.warning(
                    ('Node labels have not been filled for \n  %s}.\n  Skipping file. '
                     '(** Hint: Run fill_match_info.py on %s and then try again.)'),
                    json_file, raw_path.name)
                print('-> Warning: Node labels have not been filled for\n'
                      f'            {json_file}.\n'
                      '   ❌ Skipping file.\n     * Hint: Run `fill_match_info.py` on '
                      f'{raw_path.name} and then try again.')
                continue

        df = pd.json_normalize(json_dicts, sep='_', max_level=1)

        # * since `hit_id` is now added in previous module, it can be moved to the index immediately.
        df = df.convert_dtypes().set_index('hit_id')

        df.columns = (df.columns.str.replace('s_', '_', regex=False))

        df = df.assign(json_source=json_file)

        invert_pat = re.compile(r'(\w+)_([A-Z]+)')
        df.columns = [invert_pat.sub(r'\2_\1', str(label)).lower()
                      for label in df.columns]

        rr0 = TIMESTAMP()

        df = _remove_redundant(df, json_file)
        rr1 = TIMESTAMP()
        logging.info('Time to remove redundant entries: %s',
                     get_proc_time(rr0, rr1))

        pi0 = TIMESTAMP()
        df = _process_ix(df)
        pi1 = TIMESTAMP()
        logging.info('Time to process indices: %s', get_proc_time(pi0, pi1))

        df = df.convert_dtypes()

        # Note: This does not check that the adv and adj are actually true collocates
        if 'adv_form' in df.columns and 'adj_form' in df.columns:
            collocs = df.adv_form + '_' + df.adj_form
        else:
            collocs = ''

        # (having both adv and adj is unnecessary
        #  since they are required to be contiguous with ADV first,
        #  but I'm sure I'd get confused about which token it is
        #  if only 1 was included)
        # // > `hit_id` ->  NEG-ADV-ADJ
        # > (update) `hit_id` -> all nodes delineated by -
        # > `colloc_id` ->  ADV-ADJ (only)
        df = df.assign(
            # // hit_id=df.sent_id+':'+df.match_ix,
            # // colloc_id=(df.sent_id + ':' + df.adv_index.astype('string')
            # //            + '-' + df.adj_index.astype('string')),
            colloc=collocs,
            pattern=Path(df.json_source[-1]).parent.suffix.strip('.')
        )

        json_dir_df = pd.concat([df, json_dir_df])

    return json_dir_df


def _remove_redundant(df: pd.DataFrame,
                      json_path: Path):

    # FIXME: remove? Don't think this is still necessary since indexing was fixed.
    logging.info('removing redundant pattern matches...')
    # // is_unfilled = df.sent_text.isna()
    # // unfilled_rows = df.loc[is_unfilled, :]
    # // unfilled_ids = unfilled_rows.reset_index().hit_id
    # // filled_ids = df.reset_index().hit_id[~is_unfilled].unique()
    # // # > reconfigure dataframe to be:
    # // # >   all filled rows
    # // # >   + all unfilled rows representing an otherwise unaccounted hit (not in filled rows)
    # // unaccounted_raw = unfilled_rows.loc[~unfilled_ids.isin(filled_ids), :]
    # // fdf = pd.concat([df.loc[~is_unfilled, :], unaccounted_raw])
    # // if unaccounted_raw.empty:
    # //     fdf = fdf.loc[:, fdf.columns[~fdf.columns.str.contains('matching_')]]
    # //     logging.warning('Unfilled nonduplicate rows remaining in dataframe.')
    # // #! cheating, for now, because I'm not certain the above should be removed yet.
    # // df = df
    # ^ it's running ok wihtout it I think, so put it all back to `df`
    # > remove any full duplicates
    dep_cols = df.columns[df.columns.str.startswith('dep')].to_list()
    dup_assess_cols = df.columns[
        df.columns.isin(['match_id', 'sent_text',
                         'context_prev_sent', 'context_next_sent'])
        ].to_list() + dep_cols
    # dictionaries are not hashable types, so will crash with duplicated()
    dup_hashed = df.copy().loc[:, dup_assess_cols]
    unhashable = dup_hashed.dtypes != 'string'
    dup_hashed.loc[:, unhashable] = dup_hashed.loc[:,unhashable].astype('string')
    keep_duplicate = dup_hashed.duplicated(subset=dup_assess_cols, keep='first')
    #! use copy to create boolean indexer, but pull data from original
    keep_df = df.loc[~keep_duplicate, :]

    if len(keep_df) < len(df):

        logging.warning('%d duplicate hits removed from dataframe',
                        len(df) - len(keep_df))
        # TODO: remove -- tmp print
        print(f'{len(df) - len(keep_df)} duplicate hits removed from dataframe')
        is_duplicate = dup_hashed.duplicated(
            subset=dup_assess_cols, keep=False)
        all_dup_df = df.loc[is_duplicate, :]

        flat_deps_frame = pd.json_normalize(all_dup_df[dep_cols].to_dict(
            orient='records'), sep='_', max_level=1)
        flat_deps_frame = flat_deps_frame.loc[:, flat_deps_frame.columns.str.endswith(
            ('head', 'target', 'relation'))]
        #! # HACK
        all_dup_flat = pd.DataFrame()
        try:
            all_dup_flat = (
                all_dup_df.loc[:, ~all_dup_df.columns.str.startswith('dep')]
                .join(flat_deps_frame))
        except TypeError:
            err_location = '/share/compling/projects/sanpi/source/gather/tabulate_hits.py:259'
            logging.error("TypeError: '<' not supported between instances of 'str' and 'int'\n%s\n%s\n%s\n\n%s\n%s",
                          err_location,
                          "## `all_dup_df`:",
                          all_dup_df.to_markdown(),
                          "## `flat_deps_frame`:",
                          flat_deps_frame.to_markdown())
            print(
                f'⚠️   ERROR creating `all_dup_flat` in `tabulate_hits._remove_redundant()` at\n  {err_location}')
        else:
            # all_dup_df = all_dup_df[
            #     ['hit_id', 'json_source', 'sent_id', 'match_id','context_prev_sent', 'sent_text', 'context_next_sent']
            #     ].join(flatten_deps_df)
            all_dup_flat = (all_dup_flat
                            .assign(kept=all_dup_flat.index.isin(keep_df.index))
                            .sort_values('kept', ascending=False)
                            .sort_values('sent_text'))
            logging.info('\n%s', all_dup_flat.to_markdown())
        if logging.getLogger().getEffectiveLevel() < 20:
            DEBUG_OUT = DATA_DIR.joinpath('debug')
            if not DEBUG_OUT.is_dir():
                DEBUG_OUT.mkdir()
            for obj_name, df_obj in [('df', df),
                                     ('fdf', df),
                                     ('all-dup', all_dup_df),
                                     ('all-dup_dep-flat', all_dup_flat)]:
                if not df_obj.empty():
                    df_obj.to_pickle(DATA_DIR.joinpath(
                        'debug', f'err_{obj_name}.pkl'))
                    df_obj.to_csv(DEBUG_OUT.joinpath(f'err_{obj_name}.csv'))
        # BUG: slurm `segmentation fault`. this is where the log stops. 👇
        #! running following line in debug console just crashed everything...? do these things not exist?
        # ? commenting out this line eliminates the segmentation fault, but I have no idea why?
        # logging.info(all_dup_flat.loc[~all_dup_flat.kept, :].to_json(
        #     orient='records', indent=4))

        dup_csv_path = json_path.with_suffix('.duplicates.csv')
        all_dup_df.to_csv(dup_csv_path)
        # print(all_dup_df.to_json(orient='records', indent=3))
        logging.info('Duplicate hit info saved to %s', str(dup_csv_path))

    else:
        logging.info('No duplicated hits in %s', str(json_path.parts[-3:]))

    return keep_df


def _process_ix(df):
    # if any(df.token_str.isna()):
    #     logging.warning('Empty token string(s) in json data.')

    # # ? Are .fillna() applications necessary here?? they shouldn't be. These should all have values...
    # df = df.assign(token_str=df.token_str.astype('string').fillna(''))
    # utt_len = pd.to_numeric(df.token_str.apply(lambda x: len(x.split())),
    #                         downcast='integer')
    # ix_df = df.loc[:, df.columns.str.endswith(('index'))]
    # ix_df = ix_df.fillna(0).apply(pd.to_numeric, downcast='integer')

    # ix_df = ix_df.assign(hit_start_ix=pd.to_numeric(ix_df.apply(min, axis=1), downcast='unsigned'),
    #                      hit_final_ix=pd.to_numeric(ix_df.apply(
    #                          max, axis=1), downcast='unsigned'),
    #                      utt_len=utt_len,
    #                      token_str=df.token_str)

    # ix_df = ix_df.assign(
    #     win_start_ix=ix_df.hit_start_ix.apply(lambda x: max(x - MARGIN_SIZE, 0)),
    #     # testing for end of string is unnecessary. going over the len() value doesn't do anything
    #     win_final_ix=ix_df.hit_final_ix + MARGIN_SIZE
    # )

    # win_strs = tuple(_gen_window(
    #     ix_df.token_str, ix_df.win_start_ix, ix_df.win_final_ix))
    # hit_strs = tuple(_gen_window(
    #     ix_df.token_str, ix_df.hit_start_ix, ix_df.hit_final_ix))

    # df = df.assign(
    #     hit_text=hit_strs,
    #     text_window=win_strs,
    #     utt_len=ix_df.utt_len)
    # return df

    # > Sourcery "simplify code" output
    # if any(df.token_str.isna()):
    #     logging.warning('Empty token string(s) in json data.')

    # df = df.assign(token_str=df.token_str.astype('string').fillna(''))
    # utt_len = pd.to_numeric(df.token_str.str.split().str.len(), downcast='integer')

    # ix_df = (df.loc[:, df.columns.str.endswith(('index'))]
    #          .fillna(0)
    #          .apply(pd.to_numeric, downcast='integer')
    #          .assign(hit_start_ix=lambda df: pd.to_numeric(df.min(axis=1), downcast='unsigned'),
    #                  hit_final_ix=lambda df: pd.to_numeric(df.max(axis=1), downcast='unsigned'),
    #                  utt_len=utt_len,
    #                  token_str=df.token_str,
    #                  win_start_ix=lambda df: df.hit_start_ix.apply(lambda x: max(x - MARGIN_SIZE, 0)),
    #                  win_final_ix=lambda df: df.hit_final_ix + MARGIN_SIZE))

    # win_strs = tuple(_gen_window(ix_df.token_str, ix_df.win_start_ix, ix_df.win_final_ix))
    # hit_strs = tuple(_gen_window(ix_df.token_str, ix_df.hit_start_ix, ix_df.win_final_ix))

    # df = df.assign(hit_text=hit_strs, text_window=win_strs, utt_len=ix_df.utt_len)
    # return df

    # > Then additionally optimized for performance
    if any(df.token_str.isna()):
        logging.warning('Empty token string(s) in json data.')

    df.token_str = df.token_str.astype('string')
    df.token_str.fillna('', inplace=True)
    utt_len = pd.to_numeric(
        df.token_str.str.split().str.len(), downcast='integer')

    ix_df = df.loc[:, df.columns.str.endswith(('index'))]
    ix_df.fillna(0, inplace=True)
    ix_df = ix_df.apply(pd.to_numeric, downcast='integer')

    ix_df['hit_start_ix'] = pd.to_numeric(
        ix_df.min(axis=1), downcast='unsigned')
    ix_df['hit_final_ix'] = pd.to_numeric(
        ix_df.max(axis=1), downcast='unsigned')
    ix_df['utt_len'] = utt_len
    ix_df['token_str'] = df.token_str
    ix_df['win_start_ix'] = ix_df['hit_start_ix'].apply(
        lambda x: max(x - MARGIN_SIZE, 0))
    ix_df['win_final_ix'] = ix_df['hit_final_ix'] + MARGIN_SIZE

    win_strs = tuple(_gen_window(
        ix_df.token_str, ix_df.win_start_ix, ix_df.win_final_ix))
    hit_strs = tuple(_gen_window(
        ix_df.token_str, ix_df.hit_start_ix, ix_df.win_final_ix))

    df = df.assign(hit_text=hit_strs, text_window=win_strs,
                   utt_len=ix_df.utt_len)
    return df


def _gen_window(text_iter, start_iter, final_iter):
    for full_string, start, final in zip(text_iter, start_iter, final_iter):
        yield ' '.join(full_string.split()[start:1 + final])


def _create_output(hits_df, match_dir, start_time):
    logging.info('creating outputs...')
    # home/arh234/data/sanpi/1_json_grew-matches/immediateNeg/PccVa.without-relay
    csv_path = get_csv_path(match_dir)
    hits_df = hits_df.assign(category=match_dir.parent.name).convert_dtypes()
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
    #   ```
    #   FutureWarning: In a future version, `df.iloc[:, i] = newvals` will
    #    attempt to set the values inplace instead of always setting a new array.
    #    To retain the old behavior, use either `df[df.columns[i]] = newvals`
    #    or, if columns are non-unique, `df.isetitem(i, newvals)`
    #   ```
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
    #! psv/pipe delimited (`|`) required because table includes commas (`,`)
    # ? Is this true? ^^
    hits_df.to_csv(csv_path)
    hits_df.to_csv(csv_path.with_suffix('.psv'), sep='|')
    hits_df.to_pickle(csv_path.with_suffix('.pkl.gz'))

    view_sample_size = min(5, len(hits_df))
    sample_df = hits_df.sample(view_sample_size)
    print_cols = hits_df.columns[hits_df.columns.isin(
        ('neg_form', 'colloc', 'text_window', 'neg_deprel', 'neg_head', 'pattern'))].to_list()
    for pos in ('adj', 'adv', 'neg'):
        if any(sample_df.loc[:, f'{pos}_lemma'].astype('string') != sample_df.loc[:, f'{pos}_form'].astype('string')):
            print_cols.extend([f'{pos}_lemma', f'{pos}_form'])

    try:
        print_table = sample_df[print_cols].to_markdown()

    except ImportError:
        print_table = sample_df[print_cols].to_string()

    logging.info('Sample of Tabulated Data:\n%s\n', print_table)
    print_md_table(sample_df[print_cols],
                   title=f'#### Data Sample: `{sample_df.pattern[0]}` ####\n', )
    # print(print_table+'\n')

    finish_time = TIMESTAMP()
    dur_str = get_proc_time(start_time, finish_time)
    print(f'Time to tabulate hits: {dur_str}')
    logging.info('Tabulation Complete! Time elapsed: %s', dur_str)


def get_csv_path(match_dir):
    output_dir = Path(*(match_dir.parts[:-3]
                        + ('2_hit_tables', match_dir.parent.name)))

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    fstem = f"{match_dir.name.replace('.', '_')}_hits"
    csv_path = output_dir.joinpath(f'{fstem}.csv')

    return csv_path


if __name__ == '__main__':
    args = _parse_args()
    _t0 = pd.Timestamp.now()
    tabulate_hits(*args)
    _t1 = pd.Timestamp.now()

    print('✔️ Program Completed --', pd.Timestamp.now().ctime())
    print(f'   total time elapsed: {get_proc_time(_t0, _t1)}',
          '\n====================================\n')
