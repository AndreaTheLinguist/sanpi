# %%
import argparse
from pathlib import Path

import pandas as pd
import requests
from utils.dataframes import Timer, print_md_table, save_table


def request_url(bigram):
    return f'https://en.wiktionary.org/api/rest_v1/page/definition/{bigram}?redirect=false'


def lexicalized(response):
    return 'en' in response.keys()


def assess_lexicalization(bigrams):
    entries = (lexicalized(requests.get(request_url(b)).json()) for b in bigrams)

    return pd.Series(index=bigrams, data=entries, name='lexical')
    # df = pd.Series(index=bigrams, data=entries, name='lexical').to_frame()
    # df.index.name = 'bigram'
    # df['lexical'] = df.response.apply(lexicalized)
    # df.drop('response', axis=1, inplace=True)
    
    # return df



def _parse_args():

    parser = argparse.ArgumentParser(
        description=('Script to add boolean column indicating lexicalization status to association measure tables for bigrams. '
                     'Uses Wiktionary API to assess whether the bigram has an lexical entry. '
                     'If a bigram has an entry, `lexical = True.` '
                     'If not, `lexical = False`'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    
    parser.add_argument(
        '-i','--input',
        type=Path, 
        default=Path('/share/compling/projects/sanpi/DEMO/results/assoc_df/polar/NEGmirror/extra/polarized-bigram_demo-MIRROR.3f-2thresh_min3x.rsort-view_extra.pkl.gz'),
        help=('path to dataframe to add "lexicalized" column to. '
              'Must have column "l2" corresponding to the bigram delimited by `_`')
        )

    return parser.parse_args().input


def _main():
    path = _parse_args()
    df = []
    try: 
        df = pd.read_pickle(path)
        bigrams = list(df['l2'].unique())
    except FileNotFoundError: 
        # try: 
        #     bigrams = Path('/share/compling/projects/sanpi/results/all-unique-bigrams_35f_min868.txt').read_text(encoding='utf8').splitlines()
        
        # except FileNotFoundError: 
        exit(f'Specified input {path} not found. ¯\_(ツ)_/¯')
    if any(df) and 'lexical' not in df.columns: 
        
        lex = assess_lexicalization(bigrams)
        print(lex.value_counts())
        print_md_table(lex.head(20).to_frame().astype('bool'), title='\n First 20 bigrams')

        df['lexical'] = df.l2.apply(lambda b: lex[b]).astype('bool')
        save_table(df, path.with_name(f'LEX_{path.name}'), 'Updated association measures table', formats=['pickle', 'csv'])
        
    # else:
    #     save_table(lex_df, '/share/compling/projects/sanpi/results/bigram-lexicalized.csv', 'simple lexicalization status table', formats=['csv'])


if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print('\n✓ Program Completed --', pd.Timestamp.now().ctime())
        print(f'- total time elapsed: {timer.elapsed()}')
