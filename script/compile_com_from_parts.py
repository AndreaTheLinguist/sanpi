# coding=utf-8
import argparse
import re
import sys
from pathlib import Path
from time import sleep

import pandas as pd
from more_itertools import batched

from source.utils.dataframes import NEG_REGEX, POS_FEW_REGEX, Timer
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import (drop_underscores, embolden, extend_window,
                                     get_neg_equiv_sample, get_preceding_text,
                                     print_path_info, save_final_info,
                                     save_hit_id_index_txt, select_id_prefixes,
                                     show_sample, write_part_parquet)
from source.utils.general import HIT_TABLES_DIR, confirm_dir, run_shell_command

TEST_CAP = None
# try:
#     import pyarrow
# except ImportError:
#     PYARROW = False
# else:
PYARROW = True

PART_LABEL_REGEX = re.compile(r'[NAP][pwytcVaTe\d]{2,4}')
NUM_ID_TAG_REGEX = re.compile(r'^((?<=pcc_eng_)\d{2}|(?<=nyt_eng_)\d)')
RBX_CLEAN = HIT_TABLES_DIR.joinpath('RBXadj/cleaned')


def _main():
    args = _parse_args()
    data_dir = args.data_dir
    print(f'\n# Hit Table Processing for `{data_dir.name}`\n',
          f'* start time: {pd.Timestamp.now().ctime()}',
          '* script:  \n  `/share/compling/projects/sanpi/script/compile_com_from_parts.py`',
          f'* data directory:  \n  `{data_dir}/`',
          sep='\n', end='\n\n')
    force_redo = args.force
    composite_only = args.composite_only
    final_index_txt = data_dir.joinpath(f'ALL_{data_dir.name}_final-index.txt')
    enforced_parqs = tuple(data_dir.joinpath('enforced').glob(
        '*[PAN][cpy]*hits.parq'))
    if (final_index_txt.is_file()
        and (not force_redo)
        and (len(enforced_parqs) == 35
             or 'DEMO' in data_dir.parts)):
        all_enforced = _load_from_prior(final_index_txt, enforced_parqs)

    else:
        all_enforced = _load_from_raw(data_dir, force_redo)

    all_enforced = catify(drop_underscores(all_enforced))
    entire_parquet = str(data_dir/f'ALL_{data_dir.name}.parq')

    if not composite_only:
        _process_extras(all_enforced, entire_parquet)

    sleep(5)
    save_composite_parq(all_enforced, entire_parquet)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('This is a script to load pre-cleaned "positive" hit csv files in chunks '
                     'and drop all rows that match the "negative" regex preceding the adverb. '
                     'Compile the chunks for each part and save as updated part. '
                     'Then concatenate these smaller tables for each part into single and save. '
                     'There should be at least 35 files loaded as inputs, and at least 36 files saved.\n'
                     '⚠️ This should only be applied to *complement* or "positive" sets, not the full dataset.'
                     ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d', '--data_dir',
        type=Path,
        default=HIT_TABLES_DIR / 'not-RBdirect',
        help=('path to directory housing clean "positive" hit tables '
              'to enforce (ensure "not negated"). Intended to be: '
              "(1) '2_hit_tables/not-RBdirect' or "
              "(2) '2_hit_tables/POSmirror/pre-cleaned'")
    )
    parser.add_argument(
        '-C', '--composite_only',
        default=False,
        action='store_true',
        help=('option to skip straight to saving composite dataframe: no info output or "NEQ" sample made')
    )

    parser.add_argument(
        '-F', '--force',
        default=False,
        action='store_true',
        help=('option to force reprocessing of all parts')
    )

    return parser.parse_args()


def _load_from_prior(final_index_txt: Path,
                     enforced_parqs: tuple[Path],
                     #  data_dir: Path
                     ):
    print('> !!! Prior Index for Full Complement found.')
    print('\n## Loading from Partial Prior Processing\n',
          f'existing files:  \n  `{enforced_parqs[0].parent}/*`',
          f'existing final index:  \n  `{final_index_txt}`',
          sep='\n* ')

    unique_ids = pd.Series(final_index_txt
                           .read_text().splitlines(),
                           dtype='string'
                           ).str.strip().drop_duplicates()
    print(f'* {len(unique_ids):,} `hit_id`s in final index')

    print(
        f'* Loading predetermined selection from {len(enforced_parqs)} `*.parq` paths')

    def iter_filtered_parqs(unique_ids: pd.Series,
                            enforced_parqs: tuple[Path]):
        corpus_in_id = unique_ids.str[:3]
        # id_prefixes = unique_ids.str[:10]#.drop_duplicates()
        # id_tags =  id_prefixes.copy()
        id_tags = corpus_in_id.copy() + '_eng_'
        id_tags[corpus_in_id == 'nyt'] = unique_ids[corpus_in_id == 'nyt'].str[:9]
        id_tags[corpus_in_id == 'pcc'] = unique_ids[corpus_in_id == 'pcc'].str[:10]

        for i, ep in enumerate(enforced_parqs, start=1):
            with Timer() as iter_t:
                part = PART_LABEL_REGEX.search(ep.name).group().lower()
                id_tag = f'{part[:3]}_eng_{part[3:]}'
                print(f'  {str(i).rjust(2)}. `{id_tag}` hits:  \n',
                      f'     `{ep}`  ')
                # id_set = set(unique_ids
                #                 .loc[ids_by_corpus==part[:3]]
                #                 .loc[unique_ids.str.startswith(id_tag)])
                id_set = set(unique_ids.loc[id_tags == id_tag])
                pdf = pd.read_parquet(ep, engine='pyarrow',
                                      filters=[('hit_id', 'in', id_set)],
                                      use_threads=True)
                print(' '*5, iter_t.elapsed())
                yield pdf

    # * iterate over part & preselect part IDs
    with Timer() as load_t:
        try:
            prior_parqs = (iter_filtered_parqs(
                unique_ids,
                enforced_parqs[:TEST_CAP] if TEST_CAP
                else enforced_parqs))

        except Exception as exc:
            print('⚠️  Failed to load parquet files')
            print("/share/compling/projects/sanpi/script/compile_com_from_parts.py:163")
            print('\n  - '.join(('sys.exc_info(), ' +
                  repr(sys.exc_info()).strip('()')).split(', ')))
            raise exc

        print('* Time to load, filter to final ID index',
              '🪂  by part & *part* ids',
              f'  → {load_t.elapsed()}',
              sep='\n  ', end='\n\n')

    with Timer() as cat_t:
        all_enforced = pd.concat(prior_parqs)
        print((f'* Time to concat all {len(enforced_parqs)} parts'),
              '📚  by part iterator',
              f'  → {cat_t.elapsed()}',
              sep='\n  ', end='\n\n')

    try:
        print('Summary of loaded, filtered, & concatenated hits\n',
              all_enforced
              # .select_dtypes(include='string')
              .filter(regex=r'bigram|lemma|part|prefix|text_window')
              .describe().T.convert_dtypes().round()
              .to_markdown(floatfmt=',.0f', intfmt=','),
              sep='\n', end='\n\n')
    except Exception:
        print('failed to describe frame: "/share/compling/projects/sanpi/script/compile_com_from_parts.py:167"')
        print(sys.exc_info())
    # // print(f'Test Finished.\n{pd.Timestamp.now().ctime()}')
    # // sys.exit() #!  --- ** REMOVE ** ---- 🚩⚠️
    return all_enforced


def _load_from_raw(data_dir: Path,
                   force_redo: bool = False):
    print('\n> ... Starting parquet processing of parts @',
          pd.Timestamp.now().ctime())
    with Timer() as proc_t:
        updated_part_parqs = tuple(process_parts(data_dir, force_redo))
        print(
            f'* Time to process all parts (as needed) → {proc_t.elapsed()}')
    with Timer() as load_t:
        updated_parts = (
            pd.read_parquet(p, engine='pyarrow' if PYARROW else 'fastparquet'
                            # columns=['part', 'slice', 'adv_index',
                            #             'bigram_lower', 'text_window',
                            #             'utt_len', 'token_str']
                            )
            for p in updated_part_parqs)
        all_enforced = pd.concat(updated_parts).convert_dtypes()
        # print('* Time to load from pre-built parquets with limited columns →',
        print('* Time to load from pre-built parquets with all columns →',
              load_t.elapsed())
    print(f'\n## Final `{data_dir.name}` Concatenation\n')
    print(
        f'* {len(all_enforced):,} total hits remaining in {data_dir.name} final compilation')
    # sleep(30)
    unique_ids = remove_duplicates(
        catify(all_enforced.copy().filter(
            ['utt_len', 'adv_index', 'adv_form_lower', 'text_window'])),
        final=True)

    all_enforced = all_enforced.filter(unique_ids, axis=0)
    return all_enforced


def _process_extras(all_enforced, entire_parquet):
    data_dir = Path(entire_parquet).parent
    print('\n### Saving `ALL` Final Info')
    save_final_info(all_enforced, data_dir)
    sleep(10)

    timestamp = pd.Timestamp.now().strftime(".%y%m%d%H")
    sample_parq_part = (str(entire_parquet)
                        .replace('ALL', 'NEQ')
                        .replace('.parq', f'_sample{timestamp}.parq'))

    equal_sized_sample = get_neg_equiv_sample(all_enforced, data_dir)
    print('\n### Saving `NEQ` Sample Info')
    save_final_info(equal_sized_sample, data_dir, tag='NEQ',
                    date_flag=timestamp)

    sleep(5)

    save_composite_parq(equal_sized_sample,
                        sample_parq_part,
                        sample=True)


# > moved `_info` to `source.utils.dataframes` "/share/compling/projects/sanpi/source/utils/dataframes.py"


def process_parq(data_dir, parq,
                 force: bool = False):

    with Timer() as proc_part_t:
        part = PART_LABEL_REGEX.search(parq.stem).group()

        try:
            com_index_filter = tuple(
                data_dir.glob(f'*{part}*index.txt'))[0]
        except IndexError as e:
            if 'DEMO' in data_dir.parts:
                return None
            raise FileNotFoundError(
                f'complement hit_id index for {part} (*{part}*alpha*.txt) not found'
            ) from e

        print(f'\n## Corpus Part: `{part}`\n')
        enforced_dir = com_index_filter.with_name('enforced')
        confirm_dir(enforced_dir)
        reject_dir = com_index_filter.with_name('rejected')
        confirm_dir(reject_dir)
        enforced_parq = enforced_dir.joinpath(
            com_index_filter.name.replace('index.txt', 'hits.parq'))
        if force or not enforced_parq.exists():
            df = catify(pd.read_parquet(
                parq, engine='pyarrow' if PYARROW else 'fastparquet'
            ).assign(part=part), reverse=True)
            init_len = len(df)
            # df = df.assign(
            #     utt_len=pd.to_numeric(df.utt_len, downcast='unsigned'),
            #     adv_index=pd.to_numeric(df.adv_index, downcast='unsigned'))
            df = pd.concat(
                iter_enforce_filter(
                    df, parq=parq, part=part,
                    com_ids_path=com_index_filter,
                    reject_dir=reject_dir)
            )

            with Timer() as wrt_ix_t:
                print(f'* "Not negated"-enforced index for `{part}` saved as:',

                      save_hit_id_index_txt(index_vals=df.index,
                                                index_path=enforced_parq.with_name(
                                                    re.sub(
                                                        r'_hits.*$', '_no-neg_index.txt', enforced_parq.name)
                                                )),
                      sep='\n  > 🏷️  `', end='`\n')
                print(f'  > ⏱️  {wrt_ix_t.elapsed()}\n')

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # NOTE: # > Since same code is applied now at the previous cleaning stage of the _entire_ dataset,
                # > no additional removals are expected here.
            if 'not-RBdirect' not in enforced_parq.parts:
                print('\n### Removing Duplicates from all '
                      f'`{part}` chunks combined')
                df = remove_duplicates(df)

            # * 🏁✔️ Complement Processing for Part Finished
            print(
                f'\n### `{part}` Summary\n',
                f'* {len(df):,} remaining hits',
                f'  ({round(len(df)/init_len*100, 1):.1f}% of loaded)',
                f'* Time to process `{part}` corpus part → {proc_part_t.elapsed()}',
                sep='\n')

            write_part_parquet(df, part=part, out_path=enforced_parq,
                               data_label='final negation prohibited complement tokens')

            # max_rows = min(25000(round((df[partition_cols].value_counts().median() // 4) * 1.01, -2)))
            # with Timer() as save_time:
            #     df.sort_index().to_parquet(
            #         str(enforced_parq),
            #         partition_cols=partition_cols,
            #         engine='pyarrow',
            #         basename_template='group-{i}.parquet',
            #         use_threads=True,
            #         existing_data_behavior='delete_matching',
            #         row_group_size=12000,
            #         max_rows_per_file=12000)
            #     print(f'* Time to save updated `{part}` as {"-".join(partition_cols)} partitioned parquet'
            #           f' → {save_time.elapsed()}')
            #     print(f'  + path:\n    `{enforced_parq}`')
        else:
            print(
                f'* {part} already processed.\n  > path:  \n  > `{enforced_parq}`')
        print(
            f'\n* Total Time for `{part}` → {proc_part_t.elapsed()}\n\n---')
    return enforced_parq


def iter_enforce_filter(df, com_ids_path, parq, part, reject_dir):
    com_ids = com_ids_path.read_text().splitlines()
    reject_parq = reject_dir.joinpath(
        com_ids_path.name.replace('_index.txt', '_reject-hits.parq'))
    for i, ix_batch in enumerate(batched(com_ids, 500000), start=1):
        print('\n### Processing',
              f'`{part}`: Chunk {i:,}\n')
        chunk = df.filter(items=ix_batch, axis=0).assign(chunk=i)
        print(f'* {len(chunk):,} initial hits')
        # This 👇 is now done in the `RBXadj` clean_by_part step
        # // print(f'\n#### Removing Duplicates from `{part}`:{i}\n')
        # // chunk = remove_duplicates(chunk)
        print(f'\n#### Enforcing Negative Prohibition for `{part}`:{i}\n')
        yield enforce_not_neg(chunk, input_path=parq,
                              processing_index=i,
                              reject_parq=reject_parq)


def process_parts(data_dir: Path,
                  force_redo: bool = False):

    parq_paths = tuple(RBX_CLEAN.glob('*.parq'))
    if len(parq_paths) < 35:
        yield from process_by_csvs(data_dir)
    else:
        for parq in parq_paths:

            enforced_parq_path = process_parq(data_dir, parq, force=force_redo)
            if enforced_parq_path is None:
                continue
            yield enforced_parq_path


def process_by_csvs(data_dir):

    dtype_dict = None

    for bz2_csv_path in data_dir.glob('*[!0-9]_not*hits.csv.bz2'):

        if not dtype_dict:
            dtype_dict = {h: ('int64' if h.endswith(('index', 'len')) else 'string')
                          #! strip ".bz2" to get first line only
                          for h in bz2_csv_path.with_suffix('').read_text().splitlines()[0].split(',')}
            dtype_dict['Unnamed: 0'] = 'string'

        save_path = _get_save_path(bz2_csv_path)
        updated_chunk_iter = iterate_over_part(
            bz2_csv_path, dtype_dict, save_path)

        chunks = []
        for ch_df in updated_chunk_iter:
            ch_df = num_drop(ch_df)
            # print(ch_df.value_counts(['adv_lemma']))
            chunks.append(catify(ch_df))
        # updated_df = pd.concat(updated_chunk_iter)
        updated_df = pd.concat(chunks)
        corpus_part = save_path.name.split('_')[0]
        updated_df = updated_df.assign(
            part=corpus_part,
        )
        updated_df.to_parquet(save_path.with_suffix(
            '.parq'), engine='pyarrow', partition_cols='slice',
            basename_template='group-{i}.parquet',
            use_threads=True,
            existing_data_behavior='delete_matching',
            row_group_size=12000,
            max_rows_per_file=12000)

        yield updated_df


def num_drop(df):
    init_len = len(df)
    df = df.loc[
        df.adj_lemma.str.contains(r'[a-z]|50-50', regex=True) &
        df.adv_lemma.str.contains(r'[a-z]', regex=True),
        :
    ]
    print(f'    - {(init_len - len(df)):,} hits with numerical only adv or adj lemma dropped. {len(df):,} remaining in chunk.')
    return df


def iterate_over_part(bz2_csv_path, dtype_dict, save_path):
    print(f"\n## Processing {bz2_csv_path.stem.replace('_', ' ')}\n")
    print(f"* Input path: `{bz2_csv_path}`")
    if save_path.is_file():
        print(f"> Enforced hit table already saved as:\n>  '{save_path}'")
        print('> Loading from prior save')
        count = 1
        chunksize = 250000
        with pd.read_csv(save_path,
                         engine='c',
                         low_memory=True,
                         dtype=dtype_dict,
                         chunksize=250000,
                         index_col='hit_id') as hits_reader:
            print(f'  + chunk {count}... ({chunksize:,} rows)')
            count += 1
            yield from hits_reader

    else:
        with pd.read_csv(bz2_csv_path,
                         engine='c',
                         low_memory=True,
                         dtype=dtype_dict,
                         chunksize=200000) as hits_reader:
            print('* Resulting table with all potentially negated hits removed',
                  f"will be saved as:\n  `{save_path}`")
            yield from (enforce_not_neg(chunk, bz2_csv_path, i)
                        for i, chunk in enumerate(hits_reader, start=1))


def _get_save_path(input_path: Path, reject: bool = False) -> Path:
    label = 'potential-neg' if reject else 'enforced'
    save_dir = HIT_TABLES_DIR / \
        input_path.relative_to(HIT_TABLES_DIR).parts[0] / label
    confirm_dir(save_dir)
    tag = 'neg-regex' if reject else 'not-neg'
    save_name = input_path.name.replace(
        'clean_bigram-', '').replace('hits', f'{tag}_hits')
    return save_dir.joinpath(save_name)


def enforce_not_neg(com_df: pd.DataFrame,
                    input_path: Path,
                    reject_parq: Path,
                    processing_index: int = None) -> pd.DataFrame:

    def _save_maybe_neg(maybe_neg_hits, reject_parq):
        _max_rows = (len(maybe_neg_hits)//2)+1
        partition_by = ['chunk']
        if 'id_prefix' in maybe_neg_hits.columns:
            partition_by.append('id_prefix')
        part_counts = maybe_neg_hits.value_counts(partition_by)
        _max_rows = min(part_counts.max() + 1, 20000)
        _min_rows = min(int((part_counts.min())), 1000, _max_rows//2)
        maybe_neg_hits.to_parquet(
            str(reject_parq),
            engine='pyarrow',
            partition_cols=partition_by,
            # ^ this enables appending basically, without having different files
            basename_template='group-{i}.parquet',
            use_threads=True,
            existing_data_behavior='delete_matching',
            min_rows_per_group=_min_rows,
            max_rows_per_file=_max_rows,
            row_group_size=int(min(_max_rows//2, _min_rows*5)))
        print_path_info(
            reject_parq, 'dataframe of hits rejected due to potential negations', )

    com_df = com_df.rename(columns={'Unnamed: 0': 'hit_id'})
    init_total = len(com_df)
    if 'hit_id' in com_df.columns:
        com_df = com_df.set_index('hit_id')
    else:
        com_df.index.name = 'hit_id'

    preceding = get_preceding_text(
        tok_str=com_df.token_str,
        adv_index=(com_df.adv_index
                   if 'adv_index' in com_df.columns
                   else None))

    # This shouldn't be necessary anymore---determined source of discrepancy.
    #   See comments in `get_preceding_text()`
    # #// > test to see if adjective was included and remove is necessary
    # // preceding_words = preceding.str.lower().str.split()
    # // ultimate = preceding_words.str.get(-1)
    # // penultimate = preceding_words.str.get(-2)
    # // if any((ultimate == com_df.adj_form_lower) & (penultimate == com_df.adv_form_lower)):
    # //     preceding = preceding_words.str[:-1].str.join(' ')

    # found_neg = preceding.str.extract(NEG_REGEX, expand=False).fillna(''); print('-> **Using `extract`**')
    # print('-> **Using `findall`**')
    found_neg = preceding.str.findall(NEG_REGEX).str.join(';')
    adj_follows_neg = found_neg.astype('bool')

    # ! `extract` only returns the *first* match, but `findall` returns *all* matches (and then `join` converts list to str)
    #   so `found_neg == 'few'` really means, "few" was found and *nothing else*
    #   e.g. "a __few__ days later we are __no__ closer to a deal..." yields --> ['few', 'no'] (& becomes -> "few;no")
    #     but when "few" is the only `NEG_REGEX` match found, the value in `found_neg` is just "few"
    adj_follows_neg = allow_positive_few(preceding, found_neg, adj_follows_neg)

    chunk = com_df.chunk.iat[0]
    part = com_df.part.iat[0]
    _count_maybe_neg_in_chunk(adj_follows_neg, chunk, part, preceding)

    maybe_neg_hits = com_df.copy().assign(
        potential_negation=found_neg.astype('string'),
        nearest_neg=(found_neg.str.split(';')
                     .str.get(-1).astype('string'))
    ).loc[adj_follows_neg, :]


    _save_maybe_neg(maybe_neg_hits, reject_parq)

    total_maybe_neg = len(maybe_neg_hits)
    _sample_neg = pd.concat(
        d.sample() for __, d
        in maybe_neg_hits.loc[
            maybe_neg_hits.utt_len < 30,
            ['bigram_lower', 'token_str', 'nearest_neg']]
        .groupby('nearest_neg')
    )
    _sample_neg['token_str'] = embolden(_sample_neg.token_str, mono=False)

    print('\n> Sample of Potential Negations',
          '> (1 ex per type)\n',
          '```log',
          _sample_neg.to_markdown(tablefmt='simple_grid',
                                   maxcolwidths=[18, 22, 58]),
          '```',
          sep='\n', end='\n\n'
          )

    print(f'* _drop_ {total_maybe_neg:,} potentially negated hits', 
          f'from `{part}`, chunk {chunk}.')
    not_neg = com_df.loc[~adj_follows_neg, :]
    total_not_neg = len(not_neg)
    print(f'* _keep_ {total_not_neg:,} (likely) "not negated" hits.')
    print(f'* { total_not_neg / init_total * 100:.1f}% of hits retained.')
    if '.csv' in input_path.suffixes:
        append_hits_to_csv(not_neg.loc[adj_follows_neg, :],
                           input_path, processing_index == 1, reject=True)
        append_hits_to_csv(not_neg.loc[~adj_follows_neg, :],
                           input_path, processing_index == 1)

    return not_neg


def _count_maybe_neg_in_chunk(adj_follows_neg, chunk, part, preceding):
    print(f'\nEnforcement Summary for chunk {chunk} of `{part}`\n')
    maybe_neg_totals = (adj_follows_neg.value_counts()
                        .to_frame('# hits'))
    maybe_neg_totals.index.name = f"`{part}`, chunk {chunk}..."
    show_sample(
        df=(maybe_neg_totals
            .rename(index={'0': '_without_ potential negation(s)',
                           'False': '_without_ potential negation(s)',
                           False: '_without_ potential negation(s)',
                           '1': '**with** potential negation(s)',
                           'True': '**with** potential negation(s)',
                           True: '**with** potential negation(s)',
                           })),
        format='pipe')

    observed_unique_neg = preceding.str.extractall(NEG_REGEX).neg
    observed_unique_neg = observed_unique_neg.value_counts().to_frame().assign(
        percent=(observed_unique_neg
                 .value_counts(normalize=True) * 100
                 ).round(1))
    print('\nPotential Negations Identified: Type Subtotals',
          observed_unique_neg.to_markdown(intfmt=','),
          sep='\n\n', end='\n\n')


def allow_positive_few(preceding, found_neg, adj_follows_neg):
    just_few = found_neg == 'few'
    if any(just_few):
        few_is_pos = preceding.str.contains(POS_FEW_REGEX, na=False)
        just_pos_few = just_few & few_is_pos
        _few_ignores = (preceding[just_pos_few]
                        .str.findall(POS_FEW_REGEX).str.join('; ')
                        .value_counts().to_frame())
        print(f'* {_few_ignores["count"].sum():,} '
              '"positive few" matches permitted as "not negative"\n'
              '    (and no other negation match in text preceding bigram)')
        _few_ignores.index.name = '"positive few" match'
        show_sample(_few_ignores, format='simple_outline')
        adj_follows_neg = adj_follows_neg & ~just_pos_few
        print()
    return adj_follows_neg


def append_hits_to_csv(hits_chunk: pd.DataFrame,
                       input_path: Path,
                       first_slice: bool,
                       reject: bool = False) -> None:
    with Timer() as write_timer:
        outpath = _get_save_path(input_path, reject=reject)

        mode = 'w' if first_slice else 'a'

        hits_chunk.to_csv(outpath, header=first_slice, mode=mode)
        print(f'* Time to write new rows to `{outpath.relative_to(HIT_TABLES_DIR)}`:\n',
              f' {write_timer.elapsed()}')


def save_composite_parq(df: pd.DataFrame,
                        parq_path: str,
                        partition_on: list = None,
                        sample: bool = False):
    partition_on = partition_on or ['part']
    data_dir = Path(parq_path).parent

    print(f'\n### Saving{" *NEQ Sample* " if sample else " "}Composite Table\n')
    engine_used = None
    max_parq_rows = int(max(100000,
                            round(((df.part.value_counts().mean()//10)
                                   * 1.005), -3))
                        )

    with Timer() as time_parq:
        try:
            df.to_parquet(
                parq_path,
                engine='pyarrow',
                partition_cols=partition_on,
                min_rows_per_group=min(
                    df.part.value_counts().min() - 1,
                    max_parq_rows//8),
                row_group_size=max_parq_rows,
                max_rows_per_file=max_parq_rows,
                basename_template='group-{i}.parquet',
                use_threads=True,
                existing_data_behavior='delete_matching',
            )

        except ImportError:
            try:
                df.to_parquet(
                    parq_path, engine='fastparquet',
                    partition_cols=partition_on)

            except ImportError:
                with Timer() as time_csv:
                    entire_csv_bz2 = parq_path.replace('.parq', '.csv.bz2')
                    df.to_csv(entire_csv_bz2)
                    print('* Complement saved as compressed csv ✓',
                          f'  * Path: `{entire_csv_bz2.relative_to(HIT_TABLES_DIR.parent)}`',
                          f'  * Time elapsed: {time_csv.elapsed()}',
                          sep='\n', end='\n\n')
                    engine_used = None
            else:
                engine_used = 'fastparquet'
        else:
            engine_used = 'pyarrow'
        if engine_used:
            print(f'* Complement{" NEQ Sample" if sample else ""}',
                  'saved as parquet ✓',
                  f'* engine used: `{engine_used}`',
                  f'* partitioned by: `{repr(partition_on)}`\n',
                  '* properties included:  ',
                  '\n      ' + repr(df.columns
                                    ).replace('\n', '\n        ')+'\n\n',
                  f'* max rows per file: {max_parq_rows:,}',
                  sep='  \n  ')
            if sample:
                print(f'  * NEQ: `{Path(parq_path).relative_to(HIT_TABLES_DIR.parent)}`',
                      f'       ↪️ Negated-Equivalent → same size sample; N = {len(df):,}',
                      sep='\n')
            else:
                print(
                    f'  * ALL: `{Path(parq_path).relative_to(HIT_TABLES_DIR.parent)}`')

        print(f'  * Time elapsed: {time_parq.elapsed()}')

    return


# def extend_window(df,
#                   tokens_before: int = 7,
#                   tokens_after: int = 7):
#     # > was:
#     # # > just replace `text_window` instead of adding new column
#     # tok_lists = df.token_str.str.lower().str.split()
#     # df['text_window'] = df.apply(
#     #     lambda x: tok_lists[x.name][
#     #         max(0, x.adv_index - tokens_before):(
#     #             x.adv_index + 1 + tokens_after)],
#     #     axis=1
#     #     ).str.join(' ').astype('string')
#     # df['window_len'] = pd.to_numeric(
#     #     df.text_window.str.count(' ').add(1), downcast='unsigned')
#     # return df

#     # ^ sourcery suggestion
#     tok_lists = df.token_str.str.lower().str.split()
#     text_windows = [
#         ' '.join(tok_lists.iloc[i][max(
#             0, idx - tokens_before):(idx + 1 + tokens_after)])
#         for i, idx in enumerate(df.adv_index)
#     ]
#     df['text_window'] = pd.Series(
#         text_windows, dtype='string', index=tok_lists.index)
#     df['window_len'] = pd.to_numeric(
#         df.text_window.str.count(' ').add(1), downcast='unsigned')
#     return df


def remove_duplicates(hit_df, final: bool = False):
    def weed_windows(df, final: bool = False):
        if 'adv_index' not in df.columns:
            df['adv_index'] = pd.to_numeric(df.index.str.split(
                ':').str.get(-1).str.split('-').str.get(-2), downcast='integer')
        if (not final) and df.text_window.sample(300).str.count(' ').max() < 14:
            df = extend_window(df, 7, 7)

        over_20 = df.utt_len > 20
        yield df.copy().loc[~over_20, :]

        df_over20 = df.copy().loc[over_20, :]
        info_df = over_20.value_counts().to_frame('sent >20 tokens')
        compare_cols = ['text_window',
                        ('adv_form_lower'
                         if 'adv_form_lower' in df_over20.columns
                         else 'bigram_lower')]
        is_duplicated = df_over20[compare_cols].duplicated(
            keep=False, subset=compare_cols)
        if any(is_duplicated):
            info_df['& is/has duplicate'] = is_duplicated.value_counts()
            discard = df_over20[compare_cols].duplicated(
                keep='first', subset=compare_cols)
            info_df['& will be removed'] = discard.value_counts()
            info_df.index.name = '# hits...'
            print('\nCompiled Duplication Counts\n\n' +
                  info_df.to_markdown(intfmt=',', floatfmt=',.0f'))
            # print('\nExample of Duplication Removal (1 kept per "text_window")')
            # print('\n```log')
            # print((df_over20[is_duplicated]
            #       .filter(['utt_len', 'bigram_lower', 'text_window', 'token_str'])
            #       # //.sort_values(['extend_window', 'bigram_lower'])
            #        .sort_values(['bigram_lower', 'text_window']))
            #       .head(6)
            #       .to_markdown(maxcolwidths=[18, None, None, 28, 50], tablefmt='rounded_grid'))
            # print('```\n')
            yield df_over20.loc[~discard, :]
        else:
            print('> [[ No duplicates found ]]\n')
            yield df_over20

    if 'utt_len' not in hit_df.columns:
        hit_df['utt_len'] = pd.to_numeric(
            hit_df.token_str.str.count(' ').add(1),
            downcast='unsigned')

    succinct = pd.concat(weed_windows(hit_df, final))
    print(f'\n* {len(succinct):,} hits remaining after additional duplicate filtering',
          f'  * ({len(hit_df) - len(succinct):,} hits removed as duplicates.)',
          sep='\n')
    return succinct.index if final else succinct


if __name__ == '__main__':
    with Timer() as timer:

        _main()

        print(f'+ total time running script: {timer.elapsed()}')
