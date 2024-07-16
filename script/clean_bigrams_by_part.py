import re
from pathlib import Path
from more_itertools import batched
import pandas as pd
from sys import argv
from source.utils import Timer, catify_hit_table, remove_duplicates
from source.utils.general import POST_PROC_DIR, HIT_TABLES_DIR, PKL_SUFF, SANPI_HOME

try:
    PAT = argv[1]
except IndexError:
    PAT = 'RBXadj'
CHUNK_SZ = 500000
OK_REGEX = re.compile(r'^o*\.?k+\.?a*y*$')
V_REGEX = re.compile(r'^v\.?$|^ve+r+y+$')
DEF_REGEX = re.compile(r'^def\.?$')
ESP_REGEX = re.compile(r'^esp\.?$')
EDGE_PUNCT = re.compile(r'^[\W_]+|[\W_]+$')
BRACSLASHDOT_REGEX = re.compile(r'[\[\\\/)]|\.{2,}')
ANY_ALPHA_REGEX = re.compile(r'[a-z]')
MISC_REGEX = re.compile(r'[^a-z0-9_\-\']|[^\d_]+\d[^\d_]+|-[^-]+-[^-]+-[^-]+-')
name_regex = re.compile(r'(?<=bigram-)\w+(?=_rb)')
load_cols = ['hit_id', 'adv_form', 'adj_form', 'text_window',
             'token_str', 'adv_lemma', 'adj_lemma', 'adv_index', 'utt_len']
dtype_dict = {'hit_id': 'string',
              'adv_form': 'string',  # convert to category _after_ manipulations
              'adj_form': 'string',  # convert to category _after_ manipulations
              'text_window': 'string',
              'token_str': 'string',
              'adv_lemma': 'string',  # convert to category _after_ manipulations
              'adj_lemma': 'string',  # convert to category _after_ manipulations
              'adv_index': 'int64'}


def add_lower_cols(ch: pd.DataFrame) -> pd.DataFrame:
    def get_bigram_lower(ch: pd.DataFrame) -> pd.Series:
        try:
            bigram_lower = (ch['adv_form'] + '_' +
                            ch['adj_form']).str.lower()
        except KeyError:
            try:
                bigram_lower = (ch['adv_form_lower'] + '_' +
                                ch['adj_form_lower'])
            except KeyError:

                #! This should not happen, but...
                print(f'Warning: Could not add column `{lower_col}`:',
                      '`ad*_form(_lower)` columns not found!')
                print('current columns:\n-',
                      ch.columns.str.join('\n - '),
                      end='\n\n')
        return bigram_lower

    for form_col in ['adv_form', 'adj_form', 'bigram', 'neg_form', 'mir_form']:
        lower_col = f'{form_col}_lower'

        if lower_col not in ch.columns:

            if form_col in ch.columns:
                ch[lower_col] = ch[form_col].str.lower()
            elif lower_col == 'bigram_lower':
                ch[lower_col] = get_bigram_lower(ch)

    return ch


def _print_diff(prev_len, now_len):
    print(f'> {prev_len - now_len:,} rows dropped')


def gen_keep_clean(reader, keep_batches):

    for i, chunk in enumerate(reader, start=1):
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

        chunk = remove_odd_orth_forms(chunk)
        orth_fix_len = len(chunk)
        print('\n'+'*'*20,
              f'{orth_fix_len:,} rows after dealing with odd orthography', 
              sep='\n')
        _print_diff(prior_filter_len, orth_fix_len)

        chunk = remove_duplicates(chunk)
        succinct_len = len(chunk)
        print(
            f'{succinct_len:,} rows after removing duplicate `text_window` + `[bigram/all_forms]_lower` (for 20+ word sentences)')
        _print_diff(orth_fix_len, succinct_len)

        print('....................')
        print(f'Chunk {i} Summary')
        print('^^^^^^^^^^^^^^^^^^^^')
        print('> In total, ')
        _print_diff(init_len, succinct_len)
        yield chunk


def _main():

    data_dir = HIT_TABLES_DIR.parent
    pat_hits_dir = HIT_TABLES_DIR / PAT
    # for csv_path in pat_hits_dir.glob('bigram*csv'):
    # ! #HACK temporary for debugging
    for csv_path in pat_hits_dir.glob('bigram*Nyt1*csv'):
        part = name_regex.search(csv_path.stem).group()
        clean_index_path = pat_hits_dir / f'{part}_bigram-index_clean.35f.txt'
        out_path = pat_hits_dir / 'pre-cleaned' / \
            f'clean_{csv_path.name.split(".csv")[0]}.parq'
        print("\n"
              + pd.Series(
                  {'csv path': csv_path.relative_to(data_dir),
                   'index path': clean_index_path.relative_to(data_dir),
                   'output path': out_path.relative_to(data_dir)},
                  name=part).to_markdown(),
              end='\n\n'
              )
        if out_path.exists():

            this_script_age = SANPI_HOME.joinpath(
                'script/get_pre-cleaned_subtables.py').stat().st_mtime
            index_age = clean_index_path.stat().st_mtime
            if (out_path.stat().st_mtime < index_age
                    and out_path.stat().st_mtime < this_script_age):
                print(f'✓ Corpus part {part} previously processed:',
                      f'  {out_path.relative_to(pat_hits_dir)} already exists.\n', 
                      sep='\n')
                continue
        keepers = {i.strip()
                      for i in clean_index_path.read_text().splitlines()}
        print(f'{len(keepers):,} ids in loaded index filter')
        batch_size = max(200000,
                         int(round((len(keepers)//8)*1.01, -3)))
        keep_batches = tuple(batched(keepers, batch_size))

        with Timer() as _timer:
            with pd.read_csv(csv_path,
                             index_col='hit_id',
                             usecols=load_cols,
                             dtype=dtype_dict,
                             chunksize=CHUNK_SZ) as reader:

                df = pd.concat(gen_keep_clean(reader, keep_batches))
            print(f'\n### Chunk Processing Complete for `{part}`\n')
            cat_len = len(df)
            print('\n'+'*'*80+'\n')
            print(f'{cat_len:,} rows (hits) in concatenated `{part}` chunks')
            df = remove_duplicates(df)
            dedup_len = len(df)
            print(
                f'{dedup_len:,} rows after final duplicate removal pass on composite')
            _print_diff(cat_len, dedup_len)
            df.index.name = 'hit_id'

            print((f'\n### `{part}` Processing Complete ✓\n'
                  f'\n+ Time to process {CHUNK_SZ:,} rows at a time ⇾ '),
                  _timer.elapsed())
            print('-'*80)

    if '.csv' in out_path.suffixes:
        df.to_csv(out_path)

    elif out_path.suffix.startswith('.parq'):

        df = df.assign(id_prefix=df.index.str[:(13 if part.startswith('P') else 12)])
        print(
            f'Saving composite cleaned "{part}" hits as parquet\n  partitioned by `id_prefix` (beginning of `hit_id`)...\n')
        prefix_counts = df.id_prefix.value_counts()
        print(prefix_counts.to_markdown(intfmt=',', floatfmt=',.0f'))
        max_rows = int(
            min(100000, int(round((prefix_counts.mean() * 1.001 // 3), -2))))
        group_max = int(min(30000, (max_rows // 3) + 1))
        group_min = int(min(prefix_counts.min() // 2,
                        (max_rows // 6)+1, (group_max // 3)+1))
        print(
            f'\n> no more than {max_rows:,} rows per individual `group-[#].parquet`')
        print(f'  - max rows in writing batch = {group_max:,}')
        print(f'  - min rows in writing batch = {group_min:,}')
        with Timer() as write_time:
            df.to_parquet(out_path,
                          engine='pyarrow',
                          partition_cols=['id_prefix'],
                          basename_template='group-{i}.parquet',
                          use_threads=True,
                          existing_data_behavior='delete_matching',
                          min_rows_per_group=group_min,
                          row_group_size=group_max,
                          max_rows_per_file=max_rows)
            print('Total time to write patitioned parquet ⇾', write_time.elapsed())


def remove_odd_orth_forms(df):

    ad_cols = df.filter(regex=r'ad._\w*l').columns.to_list()

    df.loc[:, ad_cols + ['bigram_lower']
           ] = df.loc[:, ad_cols + ['bigram_lower']].astype('string')

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

    print('Fixing "null" adjectives...')
    df.loc[:, ['adj_form', 'adj_lemma', 'adj_form_lower']
           ] = df.loc[:, ['adj_form', 'adj_lemma', 'adj_form_lower']
                      ].astype('string').fillna('null')
    df = update_bigram_lower(df)

    print('Dropping most bizarre...\n')
    bracket_slash_dot = (df.bigram_lower.str.contains(
        BRACSLASHDOT_REGEX, regex=True))
    if any(bracket_slash_dot):
        print(df.loc[bracket_slash_dot,
                     ['adv_form_lower', 'adj_form_lower']].astype('string').value_counts()
              .nlargest(10).to_frame().reset_index()
              .to_markdown(floatfmt=',.0f', intfmt=','))
        df = df.loc[~bracket_slash_dot, :]

    print('\nDropping plain numerals as ad*')
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

    # Strip leading or trailing punctuation
    adv_punct = df.adv_form_lower.str.contains(EDGE_PUNCT, regex=True)
    adj_punct = df.adj_form_lower.str.contains(EDGE_PUNCT, regex=True)
    punct_edge = adv_punct | adj_punct
    if any(punct_edge):
        print(df.loc[punct_edge].filter(ad_cols).sort_index(
            axis=1).sort_values('adv_lemma').to_markdown())
        df.loc[punct_edge, ad_cols] = df.loc[punct_edge, ad_cols].apply(
            lambda a: a.apply(
                lambda w: EDGE_PUNCT.sub('', w)))

    df = update_bigram_lower(df)

    # > drop any single character "words"
    print()
    one_char_adv = df.adv_form_lower.str.len() == 1
    one_char_adj = df.adj_form_lower.str.len() == 1
    either_one_char = one_char_adv | one_char_adv
    if any(either_one_char):

        print(df.loc[either_one_char, ['adv_form_lower', 'adj_form_lower']]
              .astype('string').value_counts().nlargest(10).to_frame().reset_index()
              .to_markdown(floatfmt=',.0f', intfmt=','))
    df = df.loc[~either_one_char, :]
    # print(df.loc[df.adv_form_lower.str.contains(
    #     r'^\w\W*$', regex=True), ['adv_form_lower', 'adj_form_lower']]
    #     .astype('string').value_counts().nlargest(10).to_frame().reset_index()
    #     .to_markdown(floatfmt=',.0f', intfmt=','))
    # print()
    # print(df.loc[df.adj_form_lower.str.contains(
    #     r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
    #     .astype('string').value_counts().nlargest(10).to_frame().reset_index()
    #     .to_markdown())
    # df = df.loc[~((df.adv_form_lower.str.contains(r'^\w\W*$'))
    #               | (df.adj_form_lower.str.contains(r'^\w\W*$'))), :]

    # # > delete remaining non-word characters (esp. `.` & `*`)
    # df = df.assign(
    #     adv_form_lower=df.adv_form_lower.str.strip(
    #         '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
    #     adv_lemma=df.adv_lemma.str.strip(
    #         '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True),
    #     adj_form_lower=df.adj_form_lower.str.strip(
    #         '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
    #     adj_lemma=df.adj_lemma.str.strip(
    #         '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True)
    # )
    odd_remnant = df.bigram_lower.str.contains(MISC_REGEX, regex=True)
    if any(odd_remnant):
        print('\nMiscellaneous Remaining Oddities Dropped\n')
        print(df[odd_remnant].value_counts('bigram_lower').to_markdown())
        df = df.loc[~odd_remnant, :]
    df = df.loc[~df.adv_form_lower.isin({'is', 'ie', 'etc', 'th'}), :]

    # print(df.loc[(df.adv_form_lower.str.contains(r"[^\w'-]", regex=True))
    #              | (df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)),
    #              ['adv_form_lower', 'adj_form_lower']]
    #       .astype('string').value_counts()
    #       .nlargest(10).to_frame().reset_index()
    #       .to_markdown(floatfmt=',.0f', intfmt=',')
    #       )
    # print(df[df.adv_form_lower.str.contains(r"[^\w'-]", regex=True)].value_counts(['adv_lemma', 'adv_form_lower','adj_form_lower']))
    # print()
    # print(df[df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)].value_counts(['adj_lemma', 'adj_form_lower','adv_form_lower']))
    df = update_bigram_lower(df)
    # df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
    #        ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
    #                   ].astype('category')
    return catify_hit_table(df)


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('\n## All Corpus Parts Processed ✓\n  + Finished @',
              pd.Timestamp.now().ctime())
        print(f'  + total time elapsed: {timer.elapsed()}')
