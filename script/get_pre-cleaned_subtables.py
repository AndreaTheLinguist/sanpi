# %%
import re
from pathlib import Path
from more_itertools import batched
import pandas as pd
from sys import argv
from source.utils import Timer
from source.utils.general import POST_PROC_DIR, HIT_TABLES_DIR, PKL_SUFF

try: 
    PAT = argv[1]
except IndexError: 
    PAT = 'RBXadj'

CHUNK_SZ = 100000
name_regex = re.compile(r'(?<=bigram-)\w+(?=_rb)')
load_cols = ['hit_id', 'adv_form', 'adj_form', 'text_window',
             'token_str', 'adv_lemma', 'adj_lemma', 'adv_index']
dtype_dict = {'hit_id': 'string',
              'adv_form': 'string',  # convert to category _after_ manipulations
              'adj_form': 'string',  # convert to category _after_ manipulations
              'text_window': 'string',
              'token_str': 'string',
              'adv_lemma': 'string',  # convert to category _after_ manipulations
              'adj_lemma': 'string',  # convert to category _after_ manipulations
              'adv_index': 'int64'}


def add_lower_cols(ch:pd.DataFrame) -> pd.DataFrame:
    def get_bigram_lower(ch:pd.DataFrame) -> pd.Series:
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
        print(f'{orth_fix_len:,} rows after dealing with odd orthography')
        _print_diff(prior_filter_len, orth_fix_len)

        chunk = remove_duplicates(chunk)
        succinct_len = len(chunk)
        print(
            f'{succinct_len:,} rows after removing duplicate `text_window` + `[bigram/all_forms]_lower` (for 20+ word sentences)')
        _print_diff(orth_fix_len, succinct_len)

        print('....................')
        print(f'Chunk {i} Summary')
        print('""""""""""""""""""""')
        _print_diff(init_len, succinct_len)
        yield chunk


def _main():
    
    data_dir = HIT_TABLES_DIR.parent
    pat_hits_dir = HIT_TABLES_DIR / PAT
    for csv_path in pat_hits_dir.glob('bigram*csv'):
        part = name_regex.search(csv_path.stem).group()
        clean_index_path = pat_hits_dir / f'{part}_bigram-index_clean.35f.txt'
        out_path = pat_hits_dir / 'pre-cleaned' / f'clean_{csv_path.name}'
        print("\n"
              + pd.Series(
                  {'csv path': csv_path.relative_to(data_dir),
                   'index path': clean_index_path.relative_to(data_dir),
                   'output path': out_path.relative_to(data_dir)},
                  name=part).to_markdown(tablefmt='orgtbl'),
              end='\n\n'
              )
        if out_path.is_file(): 
            print(f'✓ Corpus part {part} previously processed:\n  {out_path.relative_to(pat_hits_dir)} already exists.\n')
            continue
        keepers = set(clean_index_path.read_text().splitlines())
        print(f'{len(keepers):,} ids in loaded index filter')
        keep_batches = tuple(batched(keepers,  len(keepers)//25))

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

            print(f'\n### `{part}` Processing Complete ✓\n+ Time to process {CHUNK_SZ:,} rows at a time:',
                  _timer.elapsed())
            print('-'*80)

        
        if not out_path.is_file():
            df.to_csv(out_path)
            # df.to_pickle(out_path.with_suffix(PKL_SUFF))


def remove_odd_orth_forms(df):

    df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
           ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
                      ].astype('string')

    def adv_is_very(df):
        return df.adv_form_lower.str.contains(r'^v\.?$|^ve+r+y+$', regex=True)

    def adv_is_def(df):
        return df.adv_form_lower.str.contains(r'^def\.?$', regex=True)

    def adj_is_ok(df):
        return df.adj_form_lower.str.contains(r'^o*\.?k+\.?a*y*$', regex=True)

    print('Dropping most bizarre...\n')
    print(df.loc[df.bigram_lower.str.contains(r'[\[\\\/)]', regex=True),
          ['adv_form_lower', 'adj_form_lower']].astype('string').value_counts()
          .nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df = df.loc[~df.bigram_lower.str.contains(r'[\[\\\/)]', regex=True), :]

    print('\nDropping plain numerals as adjectives')
    print()
    print(df.loc[df.adj_form_lower.astype('string').str.contains(r'^\d+$'), ['adv_form_lower', 'adj_form_lower', 'text_window']]
          .astype('string').value_counts().nlargest(10).to_frame().reset_index().to_markdown(floatfmt=',.0f')
          )
    df = df.loc[~df.adj_form_lower.astype('string').str.contains(r'^\d+$'), :]

    print('\nTranslating some known orthographic quirks...')
    # > variations on "very"
    print('\n==== very ====')
    print(df.loc[adv_is_very(df), 'adv_form_lower']
          .astype('string').value_counts().nlargest(10).to_frame()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df.loc[adv_is_very(df), :] = df.loc[adv_is_very(df), :].assign(
        adv_lemma='very',
        adv_form_lower='very')

    # > variations on "ok"
    print('\n==== ok ====')
    print(df.loc[adj_is_ok(df), 'adj_form_lower']
          .astype('string').value_counts().nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df.loc[adj_is_ok(df), :] = df.loc[adj_is_ok(df), :].assign(
        adj_form_lower='ok',
        adj_lemma='ok')

    # > variations on "definitely"
    print('\n==== definitely ====')
    print(df.loc[adv_is_def(df), 'adv_form_lower']
          .astype('string').value_counts().nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=','))
    df.loc[adv_is_def(df), :] = df.loc[adv_is_def(df), :].assign(adv_form_lower='definitely',
                                                                 adv_lemma='definitely')

    # > drop any single character "words"
    print()
    print(df.loc[df.adv_form_lower.str.contains(
        r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
        .astype('string').value_counts().nlargest(10).to_frame().reset_index()
        .to_markdown(floatfmt=',.0f', intfmt=','))
    print()
    print(df.loc[df.adj_form_lower.str.contains(
        r'^\w\W*$'), ['adv_form_lower', 'adj_form_lower']]
        .astype('string').value_counts().nlargest(10).to_frame().reset_index()
        .to_markdown())
    df = df.loc[~((df.adv_form_lower.str.contains(r'^\w\W*$'))
                  | (df.adj_form_lower.str.contains(r'^\w\W*$'))), :]

    # > delete remaining non-word characters (esp. `.` & `*`)
    df = df.assign(
        adv_form_lower=df.adv_form_lower.str.strip(
            '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
        adv_lemma=df.adv_lemma.str.strip(
            '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True),
        adj_form_lower=df.adj_form_lower.str.strip(
            '-').str.replace(r'[^a-z0-9&-]', '', regex=True),
        adj_lemma=df.adj_lemma.str.strip(
            '-').str.replace(r'[^a-zA-Z0-9&-]', '', regex=True)
    )
    df = df.loc[~df.adv_form_lower.isin({'is', 'ie'}), :]
    print('\n'+r"** ** ** Remaining [^\w'-] ** ** **")

    print(df.loc[(df.adv_form_lower.str.contains(r"[^\w'-]", regex=True))
                 | (df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)),
                 ['adv_form_lower', 'adj_form_lower']]
          .astype('string').value_counts()
          .nlargest(10).to_frame().reset_index()
          .to_markdown(floatfmt=',.0f', intfmt=',')
          )
    # print(df[df.adv_form_lower.str.contains(r"[^\w'-]", regex=True)].value_counts(['adv_lemma', 'adv_form_lower','adj_form_lower']))
    # print()
    # print(df[df.adj_form_lower.str.contains(r"[^\w'-]", regex=True)].value_counts(['adj_lemma', 'adj_form_lower','adv_form_lower']))
    df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
           ] = df.loc[:, ['adv_form_lower', 'adj_form_lower', 'adj_lemma', 'adv_lemma']
                      ].astype('category')
    return df.convert_dtypes()


def remove_duplicates(hit_df):
    hit_df['utt_len'] = pd.to_numeric(
        hit_df.token_str.apply(
            lambda t: len(t.split())),
        downcast='unsigned')

    succinct = weed_windows(hit_df)
    # print(f'{len(succinct):,} hits remaining after additional duplicate filtering',
    #       f'({len(hit_df) - len(succinct):,} hits removed as duplicates.)',
    #       sep='\n')
    return succinct


def weed_windows(df):
    return pd.concat(
        [df.loc[df.utt_len < 20, :],
         df.loc[df.utt_len >= 20, :].drop_duplicates(
            subset=['text_window',
                    ('all_forms_lower' if 'all_forms_lower' in df.columns
                     else 'bigram_lower')])
         ]
    )



if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('\n## All Corpus Parts Processed ✓\n  + Finished @',
              pd.Timestamp.now().ctime())
        print(f'  + total time elapsed: {timer.elapsed()}')
