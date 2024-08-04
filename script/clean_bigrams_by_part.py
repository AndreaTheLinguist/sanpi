import re
from pathlib import Path
from sys import argv

import pandas as pd
from more_itertools import batched

from source.utils.dataframes import (Timer, add_lower_cols, catify_hit_table,
                          extend_window, remove_duplicates, save_index_txt,
                          select_id_prefixes, write_part_parquet)
from source.utils.general import (HIT_TABLES_DIR, PKL_SUFF, POST_PROC_DIR,
                                  SANPI_HOME, confirm_dir)

try:
    PAT = argv[1]
except IndexError:
    PAT = 'RBXadj'

try:
    CHUNK_SZ = argv[2]
except IndexError:
    CHUNK_SZ = 500000

FORCE = True

OK_REGEX = re.compile(r'^o*\.?k+\.?a*y*$')
V_REGEX = re.compile(r'^v\.?$|^ve+r+y+$')
DEF_REGEX = re.compile(r'^def\.?$')
ESP_REGEX = re.compile(r'^esp\.?$')
EDGE_PUNCT = re.compile(r'^[\W_]+|[\W_]+$')
BRACSLASHDOT_REGEX = re.compile(r'[\[\\\/)]|\.{2,}')
ANY_ALPHA_REGEX = re.compile(r'[a-z]')
MISC_REGEX = re.compile(r'[^a-z0-9_\-\']|[^\d_]+\d[^\d_]+|-[^-]+-[^-]+-[^-]+-')
WS_REGEX = re.compile(r'[^\S\n]')
NAME_REGEX = re.compile(r'(?<=bigram-)\w+(?=_rb)')
_LOAD_COLS = ['hit_id', 'adv_form', 'adj_form', 'text_window',
              'token_str', 'adv_lemma', 'adj_lemma', 'adv_index', 'utt_len']
_DTYPES = {'hit_id': 'string',
           'adv_form': 'string',  # convert to category _after_ manipulations
           'adj_form': 'string',  # convert to category _after_ manipulations
           'text_window': 'string',
           'token_str': 'string',
           'adv_lemma': 'string',  # convert to category _after_ manipulations
           'adj_lemma': 'string',  # convert to category _after_ manipulations
           'adv_index': 'int64',
           'utt_len': 'int64'}


def _main():

    data_dir = HIT_TABLES_DIR.parent
    pat_hits_dir = HIT_TABLES_DIR / PAT
    cleaned_dir = pat_hits_dir / 'cleaned'
    confirm_dir(cleaned_dir)

    for i_part, csv_path in enumerate(pat_hits_dir.glob('bigram*csv'),
                                      start=1):
        use_new_index = False
        part = NAME_REGEX.search(csv_path.stem).group()
        preclean_index_path = (
            pat_hits_dir
            / f'{part}_bigram-index_clean.35f.txt')
        out_path = (
            cleaned_dir
            / f"clean_{csv_path.stem.replace(f'bigram-{part}',part)}.parq")
        new_index_path = out_path.with_stem(
            out_path.stem.replace('_hits', '_index')
        ).with_suffix('.txt')
        print(f'\n## Corpus Part {i_part}:  "{part}"\n\n'
              + pd.Series(
                  {'csv path': csv_path.relative_to(data_dir),
                   'index path': preclean_index_path.relative_to(data_dir),
                   'output path': out_path.relative_to(data_dir),
                   '*new* index path': new_index_path.relative_to(data_dir)},
                  name=part).to_markdown(tablefmt='double_grid'),
              end='\n\n')
        # > if updated `cleaned/*[part]*index.txt` exists for part
        if (new_index_path.is_file()
                and new_index_path.stat().st_size > 2):

            use_new_index = True

            if (out_path.exists()
                    and not FORCE):
                # this_script_age = SANPI_HOME.joinpath(
                #     'script/clean_bigrams_by_part.py').stat().st_mtime
                # index_age = preclean_index_path.stat().st_mtime
                # > if corresponding data also exists
                # //     and is more recent than the index or present code
                # if  (and out_path.stat().st_mtime < index_age
                # and out_path.stat().st_mtime < this_script_age)

                print(f'✓ Corpus part {part} previously processed.',
                      f'   Path: "{out_path.relative_to(pat_hits_dir)}"\n',
                      sep='\n')
                # > skip to next part --> NEXT
                continue

            # // > if new index exists, but data does not
            # ! This can't be used because it fails other necessary manipulations
            # else:
            #     with Timer() as prior_t:
            #         new_index_set = {i.strip()
            #                          for i in new_index_path.read_text().splitlines()}
            #         with pd.read_csv(csv_path,
            #                          index_col='hit_id',
            #                          usecols=_LOAD_COLS,
            #                          dtype=_DTYPES,
            #                          chunksize=CHUNK_SZ) as reader:
            #             df = pd.concat((chunk.filter(new_index_set, axis=0)
            #                             for chunk in reader))
            #             print('> Loaded and filtered to previously saved `cleaned/*index.txt`',
            #                   f'> ⏱️  -> {prior_t.elapsed()}', sep='\n')

        # # > if no prior cleaning outputs are found
        # else:
        if use_new_index:
            print('**Partial prior processing found!**',
                  '> Using updated index to filter:',
                  f'> "{new_index_path}"', sep='\n')
            df, index_changed = clean_part(new_index_path,
                                           csv_path, part,
                                           using_prior=True)
        else:
            df, index_changed = clean_part(preclean_index_path,
                                           csv_path, part)
        if index_changed:
            with Timer() as txt_t:
                save_index_txt(hit_ids=df.index.to_list(),
                            part=part,
                            index_path=new_index_path)
                print('\n*******',
              f'-> 🫧  Final clean "hit_id" index for "{part}" bigram tokens saved as',
              f'   🏷️  "{index_path}"',
              f'   ⏱️  {txt_t.elapsed()}',
              '*******\n',
              sep='\n', end='\n\n')
                
        # (Not used unless code above is changed)
        if '.csv' in out_path.suffixes:
            df.to_csv(out_path)

        elif out_path.suffix.startswith('.parq'):

            write_parquet(df, part, out_path)


def clean_part(clean_index_path: Path,
               csv_path: Path,
               part: str,
               using_prior: bool = False):
    keepers = {i.strip()
               for i in clean_index_path.read_text().splitlines()}
    print(f'{len(keepers):,} ids in loaded index filter')
    batch_size = max(200000,
                     int(round((len(keepers)//8)*1.01, -3)))
    keep_batches = tuple(batched(keepers, batch_size))

    with Timer() as _timer:
        with pd.read_csv(csv_path,
                         index_col='hit_id',
                         usecols=_LOAD_COLS,
                         dtype=_DTYPES,
                         chunksize=CHUNK_SZ) as reader:

            df = pd.concat(gen_keep_clean(reader, keep_batches, using_prior))
        total_dropped = df.pop('chunk_dropped').drop_duplicates().sum()
        print(f'\n### Chunk Processing Complete for "{part}"\n')
        cat_len = len(df)
        print('\n'+'*'*80+'\n')
        print(f'{cat_len:,} rows (hits) in concatenated "{part}" chunks')
        print(f'> {total_dropped:,} total hits removed from "{part}"')
        if not using_prior:
            df = remove_duplicates(df)
            dedup_len = len(df)
            print(
                f'{dedup_len:,} rows after final duplicate removal pass on composite')
            _print_diff(cat_len, dedup_len)
        df.index.name = 'hit_id'
        final_len = len(df)
        raw_len = total_dropped + final_len
        print(f'\n### `{part}` Processing{" (using prior index)" if using_prior else ""} Complete ✓\n'
              f'+ {final_len:,} total bigram tokens remaining',
              f'+ {round(final_len/raw_len * 100, 1):.1f}% of raw ({raw_len:,})',
              f'+ Time to process {CHUNK_SZ:,} rows at a time ⇾ {_timer.elapsed()}',
              sep='\n')
        print('-'*80)
    index_change = final_len != len(keepers)
    return df, index_change

# moved to `source.utils.dataframes`
# def add_lower_cols(ch: pd.DataFrame) -> pd.DataFrame:
#     def get_bigram_lower(ch: pd.DataFrame) -> pd.Series:
#         try:
#             bigram_lower = (ch['adv_form'] + '_' +
#                             ch['adj_form']).str.lower()
#         except KeyError:
#             try:
#                 bigram_lower = (ch['adv_form_lower'] + '_' +
#                                 ch['adj_form_lower'])
#             except KeyError:

#                 #! This should not happen, but...
#                 print(f'Warning: Could not add column `{lower_col}`:',
#                       '`ad*_form(_lower)` columns not found!')
#                 print('current columns:\n-',
#                       ch.columns.str.join('\n - '),
#                       end='\n\n')
#         return bigram_lower

#     for form_col in ['adv_form', 'adj_form', 'bigram', 'neg_form', 'mir_form']:
#         lower_col = f'{form_col}_lower'

#         if lower_col not in ch.columns or any(ch[lower_col].squeeze().isna()):

#             if form_col in ch.columns:
#                 ch[lower_col] = ch[form_col].str.lower()
#             elif lower_col == 'bigram_lower':
#                 ch[lower_col] = get_bigram_lower(ch)

#     return ch


def _print_diff(prev_len, now_len):
    delta = prev_len - now_len
    print(f'> {delta:,} rows dropped')
    return delta


def gen_keep_clean(reader,  # :pd.io.parsers.readers.TextFileReader,
                   keep_batches: tuple[tuple],
                   using_prior: bool = False):

    for i, chunk in enumerate(reader, start=1):
        succinct_len = None
        print(f'\n### Chunk {i}\n')
        init_len = len(chunk)
        print(f'{init_len:,} rows in initial chunk')
        chunk = pd.concat((chunk.filter(batch, axis=0)
                           for batch in keep_batches))
        # chunk = chunk.filter(keepers, axis=0)
        prior_filter_len = len(chunk)
        print(
            f'{prior_filter_len:,} rows after dropping hits already removed during previous cleaning')
        _print_diff(init_len, prior_filter_len)

        chunk = add_lower_cols(chunk)

        chunk = fix_orth(chunk, using_prior)
        orth_fix_len = len(chunk)
        print('\n'+'*'*20,
              f'{orth_fix_len:,} rows after dealing with odd orthography',
              sep='\n')
        _print_diff(prior_filter_len, orth_fix_len)
        if using_prior:
            print('  NOTE: "0" is expected.',
                  '    ↪ using index from partial prior processing (all "removals" already accounted for)',
                  '  🚧  -> except for typo fix catching one character "adj" missed before',
                  sep='\n')
            print('> Duplication previously handled as well,',
                  'but still extending "text_window" strings...')
            chunk = extend_window(chunk)
        else:
            chunk = remove_duplicates(chunk)
            succinct_len = len(chunk)
            print(
                f'{succinct_len:,} rows after removing duplicate `text_window` + `[bigram/all_forms]_lower` (for 20+ word sentences)')
            _print_diff(orth_fix_len, succinct_len)

        print('....................')
        print(f'Chunk {i} Summary')
        print('^^^^^^^^^^^^^^^^^^^^')
        print('> In total, ')
        delta = _print_diff(
            init_len, succinct_len or orth_fix_len or prior_filter_len)
        yield chunk.assign(chunk_dropped=delta).convert_dtypes()


def fix_orth(df: pd.DataFrame,
             using_prior: bool = False):

    ad_cols = df.filter(regex=r'ad[vj]_\w*l').columns.to_list()
    df = catify_hit_table(df, reverse=True)

    def update_bigram_lower(df):

        return df.assign(bigram_lower=(df.adv_form_lower + '_' + df.adj_form_lower).astype('string'))

    def adv_is_very(df):
        return df.adv_form_lower.str.contains(V_REGEX, regex=True)

    def adv_is_def(df):
        return df.adv_form_lower.str.contains(DEF_REGEX, regex=True)

    def adv_is_esp(df):
        return df.adv_form_lower.str.contains(ESP_REGEX, regex=True)

    def adj_is_ok(df):
        return df.adj_form_lower.str.contains(OK_REGEX, regex=True)

    print('\nFixing "null" strings interpreted as NaN...')
    df.loc[:, ad_cols + ['adv_form', 'adj_form']
           ] = df.filter(like='ad').astype('string').fillna('null')
    df = update_bigram_lower(df)
    if not using_prior:
        print('\nDropping most bizarre...\n')
        bracket_slash_dot = (df.bigram_lower.str.contains(
            BRACSLASHDOT_REGEX, regex=True))
        if any(bracket_slash_dot):
            print(df.loc[bracket_slash_dot,
                         ['adv_form_lower', 'adj_form_lower']].astype('string').value_counts()
                  .nlargest(10).to_frame().reset_index()
                  .to_markdown(floatfmt=',.0f', intfmt=','))
            df = df.loc[~bracket_slash_dot, :]

        print('\nDropping any ad* that contain no regular characters (a-z)')
        alpha_adv = df.adv_form_lower.str.contains(ANY_ALPHA_REGEX, regex=True)
        alpha_adj = df.adj_form_lower.str.contains(ANY_ALPHA_REGEX, regex=True)
        either_no_alpha = (~alpha_adv) | (~alpha_adj)
        if any(either_no_alpha):
            print(df.loc[either_no_alpha, ['adv_form_lower', 'adj_form_lower', 'text_window']]
                  .astype('string').value_counts().nlargest(10).to_frame().reset_index().to_markdown(floatfmt=',.0f')
                  )
            df = df.loc[~either_no_alpha, :]

    print('\nTranslating some known orthographic quirks...')
    # > variations on "very"
    v_adv = (adv_is_very(df)) & (df.adv_form_lower != 'very')
    if any(v_adv):
        print('\n==== very ====')
        print(df.loc[v_adv, 'adv_form_lower']
              .astype('string').value_counts().nlargest(10).to_frame()
              .to_markdown(floatfmt=',.0f', intfmt=','))
        df.loc[v_adv, :] = df.loc[v_adv, :].assign(
            adv_lemma='very',
            adv_form_lower='very')

    # > variations on "ok"

    ok_adj = adj_is_ok(df) & (df.adj_form_lower != 'ok')
    if any(ok_adj):
        print('\n==== ok ====')
        print(df.loc[ok_adj, 'adj_form_lower']
              .astype('string').value_counts().nlargest(10).to_frame().reset_index()
              .to_markdown(floatfmt=',.0f', intfmt=','))
        df.loc[ok_adj, :] = df.loc[ok_adj, :].assign(
            adj_form_lower='ok',
            adj_lemma='ok')

    # > variations on "definitely"
    definitely_adv = adv_is_def(df)
    if any(definitely_adv):
        print('\n==== definitely ====')
        print(df.loc[definitely_adv, 'adv_form_lower']
              .astype('string').value_counts().nlargest(10).to_frame().reset_index()
              .to_markdown(floatfmt=',.0f', intfmt=','))
        df.loc[definitely_adv, :] = df.loc[definitely_adv, :].assign(adv_form_lower='definitely',
                                                                     adv_lemma='definitely')

    # > variations on "especially"
    esp_adv = adv_is_esp(df)
    if any(esp_adv):
        print('\n==== especially ====')
        print(df.loc[esp_adv, 'adv_form_lower']
              .astype('string').value_counts().nlargest(10).to_frame().reset_index()
              .to_markdown(floatfmt=',.0f', intfmt=','))
        df.loc[esp_adv, :] = df.loc[esp_adv, :].assign(adv_form_lower='especially',
                                                       adv_lemma='especially')

    adv_punct = df.adv_form_lower.str.contains(EDGE_PUNCT, regex=True)
    adj_punct = df.adj_form_lower.str.contains(EDGE_PUNCT, regex=True)
    punct_edge = adv_punct | adj_punct
    if any(punct_edge):
        print('\nStripping leading/trailing punctuation...\n')
        print(df.loc[punct_edge].filter(
            ad_cols).sort_values('adv_lemma').to_markdown())
        df.loc[punct_edge, ad_cols] = df.loc[punct_edge, ad_cols].apply(
            lambda a: a.apply(
                lambda w: EDGE_PUNCT.sub('', w)))

    df = update_bigram_lower(df)
    # if not using_prior:
    #! realized this was only catching advs (typo listed `one_char_adv | one_char_adv`, so it needs to be rerun)
    # > drop any single character "words"
    one_char_adv = df.adv_form_lower.str.len() == 1
    one_char_adj = df.adj_form_lower.str.len() == 1
    either_one_char = one_char_adv | one_char_adj
    if any(either_one_char):
        print('\nDropping any single character "words"')
        print(df.loc[either_one_char, ['adv_form_lower', 'adj_form_lower']]
                .astype('string').value_counts().nlargest(10).to_frame().reset_index()
                .to_markdown(floatfmt=',.0f', intfmt=','))
    df = df.loc[~either_one_char, :]

    odd_remnant = df.bigram_lower.str.contains(MISC_REGEX, regex=True)
    if any(odd_remnant):
        print('\nMiscellaneous Remaining Oddities Dropped\n')
        if using_prior:
            print(
                'WARNING‼️ This is unexpected, since index from partial prior processing was used.')
        print(df[odd_remnant].value_counts('bigram_lower').to_markdown())
        df = df.loc[~odd_remnant, :]
    df = df.loc[~df.adv_form_lower.isin({'is', 'ie', 'etc', 'th'}), :]
    df = update_bigram_lower(df)

    return catify_hit_table(df)


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('\n## All Corpus Parts Processed ✓\n  + Finished @',
              pd.Timestamp.now().ctime())
        print(f'  + total time elapsed: {timer.elapsed()}')
