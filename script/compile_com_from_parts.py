# coding=utf-8
import argparse
import re
from pathlib import Path

import pandas as pd
from more_itertools import batched

from source.utils.dataframes import Timer
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import confirm_dir
from source.utils.general import HIT_TABLES_DIR, run_shell_command, timestamp_now
try:
    import pyarrow
except ImportError:
    PYARROW = False
else:
    PYARROW = True
# TODO Try this if compiling is the problem!
# from fastparquet import ParquetFile

# df.to_parquet(tmp_file, engine='pyarrow', compression='gzip')
# pf = ParquetFile(tmp_file)
# for df in pf.iter_row_groups():
#     print(df.head(n=10))

NEG_REGEX = re.compile(
    r"\bno\b|\bn[o']t\b|\bnobody\b|\bno one\b|\bnothing\b|\bnowhere\b|\brarel?y?\b|\bscarcely\b|\bbarely\b|\bhardly\b|\bseldoml?y?\b|\bwithout\b|\bnever\b")
PART_LABEL_REGEX = re.compile(r'[NAP][pwytcVaTe\d]{2,4}')
RBX_PC = HIT_TABLES_DIR.joinpath('RBXadj/pre-cleaned')


def _main():
    args = _parse_args()
    data_dir = args.data_dir
    print(f'\n> ... Starting parquet processing @ {timestamp_now()}')
    with Timer() as proc_t:
        updated_part_parqs = tuple(process_parts(data_dir))
        print(f'* Time to process all parts (as needed) → {proc_t.elapsed()}')
    with Timer() as load_t:
        updated_parts = (
            pd.read_parquet(p, 
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
    all_enforced = remove_duplicates(all_enforced)
    all_enforced = catify(all_enforced.convert_dtypes())
    
    print('\n### Saving `ALL` Final Info')
    save_final_info(all_enforced, data_dir)

    equal_sized_sample = get_neg_equiv_sample(all_enforced, data_dir)
    print('\n### Saving `NEQ` Sample info')
    save_final_info(equal_sized_sample, data_dir, tag='NEQ')
    
    entire_parquet = data_dir/'ALL_not-neg.parq'
    entire_parq_part = str(entire_parquet).replace('parq', 'part-slice.parq')
    sample_parq_part = (str(entire_parquet)
                        .replace('ALL', 'NEQ')
                        .replace('.parq', f'.sample{timestamp_now()}.parq'))

    save_composite_parq(equal_sized_sample, sample_parq_part,
                        sample=True, partition_on=['part'])
    save_composite_parq(all_enforced, entire_parq_part)
    # run_shell_command(
    #     f'tree -Dh -L 2 {Path(entire_parq_part).parent}/*parq', verbose=True)
    # run_shell_command(
    #     f'du -hc {Path(entire_parq_part).parent}/*parq/*/*', verbose=True)


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
    # parser.add_argument(
    #     '-v', '--verbose',
    #     default=False,
    #     action='store_true',
    #     help=('option to get more detailed output')
    # )

    return parser.parse_args()


def get_neg_equiv_sample(all_enforced, data_dir):
    comp_total = len(all_enforced)
    # TODO Update this method to get total updated `RBdirect` count

    neg_dir = data_dir.parent.joinpath('RBdirect/pre-cleaned')
    neg_counts = neg_dir/'alpha-index_counts.txt'
    if not neg_counts.is_file():
        run_shell_command(
            f'wc -l {neg_dir}/*alpha*txt > {neg_counts}',
            verbose=True)
    neg_total = int(neg_counts.read_text(
        encoding='utf8').splitlines()[-1].split()[0])

    print(f'\n## Creating negated sample equivalent: N = {neg_total:,}\n')
    combined_total = comp_total + neg_total
    print('+ updated NEG:',
          f'{round(neg_total/combined_total * 100, 1):.1f}%',
          'of all bigrams')
    print('+ updated COM:',
          f'{round(comp_total/combined_total * 100, 1):.1f}%',
          'of all bigrams')
    print(f'+ ~{round(comp_total / neg_total)}:1 odds',
          'that utterance is _NOT negated_')
    print(f'+ Sample: {round(neg_total/comp_total * 100, 1):.1f}%',
          'of entire updated complement')

    return all_enforced.sample(min(comp_total, neg_total))


def save_final_info(final_hits, data_dir, tag:str='ALL'):
    info_dir = data_dir.parent.parent / 'info'
    confirm_dir(info_dir)
    freq_tsv_dir = data_dir / 'ucs_format'
    confirm_dir(freq_tsv_dir)
    category = data_dir.name
    final_hits = final_hits.assign(category=category)
    #> set paths
    final_index_path = data_dir / f'{tag}_{category}_final-index.txt'
    final_index_parq = info_dir / f'{tag}-{category}_final-hits_basic.parq'
    subtotals_path = info_dir / f'{tag}_{category}_final-subtotals.csv'
    basic_freq_tsv = freq_tsv_dir / f'AdvAdj_{tag}-final-freq.tsv'
    
    # * save subtotals for part
    final_hits.value_counts(['part', 'category']).to_frame('total_hits').reset_index().to_csv(
        subtotals_path, index=False)
    print(f'+ Part Subtotals saved as {subtotals_path} ✓')
    
    final_index = final_hits.index.to_list()
    final_index.sort()
    final_index_path.write_text('\n'.join(final_index), encoding='utf8')
    print(f'+ `hit_id` index for final selection of `{category}` hits',
          f'saved as {final_index_path} ✓', sep='  \n  ')


    # * save basic frequency TSV!
    joint_f = final_hits.value_counts('bigram_lower').to_frame('f')
    joint_f.join(joint_f.index.to_series().str.extract(r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$')).to_csv(
        basic_freq_tsv, sep='\t', index=False, header=False)
    print('+ basic `adv~adj` frequencies for final hits',
          f'saved as {basic_freq_tsv} ✓', sep='  \n  ')

    # > save most basic info as parquet
    catify(final_hits.reset_index()
           .filter(['hit_id', 'part', 'category', 'bigram_lower'])
           ).to_parquet(str(final_index_parq), index=None,
                        partition_cols=['category', 'part'])


def process_parq(data_dir, parq):
    with Timer() as proc_part_t:
        part = PART_LABEL_REGEX.search(parq.stem).group()

        try:
            com_index_filter = tuple(
                data_dir.glob(f'*{part}*alpha*.txt'))[0]
        except IndexError:
            if 'DEMO' in data_dir.parts:
                return None
            raise FileNotFoundError(
                f'complement hit_id index for {part} (*{part}*alpha*.txt) not found')

        print(f'\n## Corpus Part: `{part}`\n')
        enforced_dir = com_index_filter.with_name('enforced')
        confirm_dir(enforced_dir)
        enforced_parq = enforced_dir.joinpath(
            com_index_filter.name.replace('index.txt', 'hits.parq'))
        if not enforced_parq.exists():
            df = pd.read_parquet(
                parq, engine='pyarrow' if PYARROW else 'fastparquet'
            ).astype('string')
            init_len = len(df)
            df = df.assign(
                utt_len=pd.to_numeric(df.utt_len),
                adv_index=pd.to_numeric(df.adv_index),
                part=part)
            df = pd.concat(
                iter_enforce_filter(
                    df, parq=parq, part=part,
                    com_ids=com_index_filter.read_text().splitlines())
            )
            print(
                f'\n### Removing Duplicates from all `{part}` chunks combined')
            df = remove_duplicates(df)
            print(
                f'\n### `{part} Summary\n',
                f'{len(df)} remaining hits',
                f'{round(len(df)/init_len*100, 1):.1f}% of loaded)',
                f'Time to process `{part}` corpus part → {proc_part_t.elapsed()}',
                sep='\n* ')
            with Timer() as save_time:
                df.to_parquet(str(enforced_parq),
                              partition_cols=['slice'])
                print(
                    f'* Time to save updated `{part}` as "slice" partitioned parquet → {save_time.elapsed()}')
                print(f'  + path:\n    `{enforced_parq}`')
        else:
            print(
                f'* {part} already processed.\n  > path:  \n  > `{enforced_parq}`')
        print(f'\n* Total Time for `{part}` → `{proc_part_t.elapsed()}`')
    return enforced_parq


def iter_enforce_filter(df, com_ids, parq, part):
    for i, ix_batch in enumerate(batched(com_ids, 500000), start=1):
        print('\n### Processing',
              f'`{part}`: Chunk {i:,}\n')
        chunk = df.filter(items=ix_batch, axis=0)
        print(f'* {len(chunk):,} initial hits')
        print(f'\n#### Removing Duplicates from `{part}`:{i}\n')
        chunk = remove_duplicates(chunk)
        print(f'\n#### Enforcing Negative Prohibition for `{part}`:{i}\n')
        yield enforce_not_neg(chunk, parq, i).assign(
            part=chunk.part.astype('string'))


def process_parts(data_dir):

    parq_paths = tuple(RBX_PC.glob('*alpha*.parq'))
    if len(parq_paths) < 35:
        yield from process_by_csvs(data_dir)
    else:
        for parq in parq_paths:

            enforced_parq_path = process_parq(data_dir, parq)
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

        # ? #HACK temp
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
            '.parq'), engine='pyarrow', partition_cols='adv_lemma')
        yield updated_df


def num_drop(df):
    init_len = len(df)
    df = df.loc[(df.adj_lemma.str
                 .contains(r'[a-z]|50-50', regex=True)), :]
    df = df.loc[(df.adv_lemma.str
                 .contains(r'[a-z]', regex=True)), :]
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


def enforce_not_neg(not_neg: pd.DataFrame,
                    input_path: Path,
                    processing_index: int = None) -> pd.DataFrame:
    def get_preceding_text(tok_str: pd.Series,
                           adv_index: pd.Series = None):
        tok_index = tok_str.index.to_series()
        pre_adv_index = (
            pd.to_numeric(adv_index, downcast='unsigned') if adv_index is not None
            else
            pd.to_numeric((tok_index
                           .str.split(':').str.get(-1)
                           .str.split('-').str.get(0)),
                          downcast='unsigned')
        ) - 1

        preceding_texts = tok_index.apply(lambda x: tok_str[x].split()[
            :pre_adv_index[x]]).str.join(' ')

        return preceding_texts.astype('string').fillna('')

    not_neg = not_neg.rename(columns={'Unnamed: 0': 'hit_id'})
    init_total = len(not_neg)
    if 'hit_id' in not_neg.columns:
        not_neg = not_neg.set_index('hit_id')
    else:
        not_neg.index.name = 'hit_id'

    preceding = get_preceding_text(
        tok_str=not_neg.token_str,
        adv_index=(not_neg.adv_index if 'adv_index' in not_neg.columns
                   else None)
    ).str.lower()
    after_neg = preceding.str.contains(NEG_REGEX)

    total_after_neg = after_neg.value_counts()[True]
    total_not_neg = after_neg.value_counts()[False]
    print(f'* _removed_ {total_after_neg:,} potentially negated hits.')
    print(f'* _keeping_ {total_not_neg:,} (likely) "not negated" hits.')
    print(f'* { total_not_neg / init_total * 100:.1f}% of hits retained.')
    if '.csv' in input_path.suffixes:
        append_hits_to_csv(not_neg.loc[after_neg, :],
                           input_path, processing_index == 1, reject=True)
        append_hits_to_csv(not_neg.loc[~after_neg, :],
                           input_path, processing_index == 1)
    return not_neg.loc[~after_neg, :]


def append_hits_to_csv(hits_chunk: pd.DataFrame,
                       input_path: Path,
                       first_slice: bool,
                       reject: bool = False) -> None:
    with Timer() as write_timer:
        outpath = _get_save_path(input_path, reject=reject)

        mode = 'w' if first_slice else 'a'

        hits_chunk.to_csv(outpath, header=first_slice, mode=mode)
        print(f'* Time to write new rows to `{outpath.relative_to(HIT_TABLES_DIR)}`:\n',
              f' `{write_timer.elapsed()}`')


def save_composite_parq(df: pd.DataFrame,
                        parq_path: str,
                        partition_on: list = None,
                        sample: bool = False):
    partition_on = partition_on or ['part', 'slice']
    data_dir = Path(parq_path).parent
    
    if Path(parq_path).exists(): 
        
        run_shell_command(f'mv {parq_path} $(dirname {parq_path})/.Prior_$(basename {parq_path})')
    print('\n### Saving Composite Table\n')
    # engine = 'pyarrow' if PYARROW else 'fastparquet'
    engine_used = None
    with Timer() as time_parq:
        try:
            df.to_parquet(
                parq_path, engine='pyarrow',
                partition_cols=partition_on)

        except ImportError:
            try:
                df.to_parquet(
                    parq_path, engine='fastparquet',
                    partition_cols=partition_on)

            except ImportError:
                with Timer() as time_csv:
                    entire_csv_bz2 = parq_path.replace('.parq', '.csv.bz2')
                    all_enforced.to_csv(entire_csv_bz2)
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
            print(
                f'* Complement{" NEQ Sample" if sample else ""} saved as parquet ✓')
            print(f'  * engine used: "{engine_used}"')
            print(f'  * partitioned on: {", ".join(partition_on)}')
            #   f'  * Path: `{entire_parquet.relative_to(HIT_TABLES_DIR.parent)}`',
            if sample:
                print(f'  * NEQ: `{Path(parq_path).relative_to(HIT_TABLES_DIR.parent)}`',
                      f'       ↪️ Negated-Equivalent → same size sample; N = {len(df):,}',
                      sep='\n')
            else:
                print(
                    f'  * ALL: `{Path(parq_path).relative_to(HIT_TABLES_DIR.parent)}`')
        print(f'  * Time elapsed: `{time_parq.elapsed()}`')

    return


def extend_window(df,
                  tokens_before: int = 6,
                  tokens_after: int = 6):
    # > just replace `text_window` instead of adding new column
    df['text_window'] = df.apply(
        lambda x: x.token_str.split()[
            max(0, x.adv_index - tokens_before):(
                x.adv_index + 1 + tokens_after)],
        axis=1).str.join(' ').str.lower().astype('string')
    return df


def remove_duplicates(hit_df):
    def weed_windows(df):
        if 'adv_index' not in df.columns:
            df['adv_index'] = pd.to_numeric(df.index.str.split(
                ':').str.get(-1).str.split('-').str.get(-2), downcast='integer')
        if df.text_window.sample(300).str.count(' ').max() < 14:
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
            print('\nCompiled Duplicatation Counts\n\n' +
                  info_df.to_markdown(intfmt=',', floatfmt=',.0f'))
            print('\nExample of Duplication Removal (1 kept per "text_window")\n\n```log')
            print((df_over20[is_duplicated]
                  .filter(['utt_len', 'bigram_lower', 'text_window', 'token_str'])
                  # //.sort_values(['extend_window', 'bigram_lower'])
                   .sort_values(['bigram_lower', 'text_window']))
                  .head(6)
                  .to_markdown(maxcolwidths=[18, None, None, 28, 50], tablefmt='rounded_grid'))
            print('```\n')
            yield df_over20.loc[~discard, :]
        else:
            print('\n> [[ No duplicates found ]]\n')
            yield df_over20

    if 'utt_len' not in hit_df.columns:
        hit_df['utt_len'] = pd.to_numeric(
            hit_df.token_str.apply(
                lambda t: len(t.split())),
            downcast='unsigned')

    succinct = pd.concat(weed_windows(hit_df))
    print(f'* {len(succinct):,} hits remaining after additional duplicate filtering',
          f'  * ({len(hit_df) - len(succinct):,} hits removed as duplicates.)',
          sep='\n')

    return succinct


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print(
            f'## Enforcement and Compilation Completed ✓\n+ {pd.Timestamp.now().ctime()}')
        print(f'+ total time elapsed: `{timer.elapsed()}`')
