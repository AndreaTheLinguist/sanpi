# %%
from pathlib import Path

import pandas as pd
import requests
from utils.dataframes import Timer, print_md_table


def request_url(bigram):
    return f'https://en.wiktionary.org/api/rest_v1/page/definition/{bigram}?redirect=false'


def lexicalized(response):
    return 'en' in response.keys()


def assess_lexicalization(bigrams):
    entries = {}
    for bigram in bigrams:
        response = requests.get(request_url(bigram))
        entries[bigram] = response.json()

    df = pd.Series(entries).to_frame('response')
    df.index.name = 'bigram'
    df['lexical'] = df.response.apply(lexicalized)
    df.drop('response', axis=1, inplace=True)
    df.to_csv('/share/compling/projects/sanpi/results/bigram-lexicalized.csv')
    return df

def _main():
    lex_df = assess_lexicalization(
        Path('/share/compling/projects/sanpi/results/all-unique-bigrams_35f_min868.txt')
        .read_text(encoding='utf8').splitlines())
    print(lex_df.value_counts())
    print_md_table(lex_df.head(20).astype('bool'), title='\n First 20 bigrams')

# %%
if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print('\n✓ Program Completed --', pd.Timestamp.now().ctime())
        print(f'- total time elapsed: {timer.elapsed()}')
