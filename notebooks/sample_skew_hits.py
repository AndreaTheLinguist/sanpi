# %%
from utils import sample_pickle, print_md_table
import pandas as pd
from pathlib import Path
_SANPI_DIR = Path('/share/compling/projects/sanpi')
_DATA_DIR = Path('/share/compling/data/sanpi')

skew_path = _SANPI_DIR.joinpath(
    'results/ucs_tables/dataframes/polarized-bigram_MIRROR.35f-868thresh_min15x.SKEW_extra.csv')

if not skew_path.is_file():
    raise FileNotFoundError
# %%
sk = (pd.read_csv(skew_path) if skew_path.suffix == '.csv'
      else pd.read_pickle(skew_path))

sk.head(3)
# %%

print('Minimum adjusted conditional probability of polarity environment:',
      round(sk.am_p1_given2.abs().min(), 3))
sk.head().key
# %%
parts = sk.key.str.split(
    '-', expand=True).loc[:, :1].rename(columns={0: 'pol', 1: 'bigram'})
parts


# %%
parts['data_paths'] = parts.pol.apply(
    lambda p: pd.Series(Path(f'/share/compling/data/sanpi/4_post-processed/{p}mirror/')
                        .glob('*trigger*pkl.gz')).squeeze())
relevant_col = ['neg_form', 'mir_form', 'bigram_lower',
                'pattern', 'neg_deprel', 'mir_deprel', 'text_window', 'token_str']

# %%
n_bigrams = 30
n = 20
print('# Example Hits for "Skewed" Bigrams')
hit_tables = {}
for path, _df in parts.groupby('data_paths'):
    print(f'\n## {_df.pol.unique().squeeze()} Hits\n')
    print(f'- `{path}`')
    # samples = []
    print(f'- {len(_df)} relevant bigram forms')
    hits = pd.read_pickle(path)
    hit_tables[path.parent.name] = hits
    print_md_table(hits.select_dtypes('string'), describe=True,
                   transpose=True, title='\n table summary')

for bigram in sk.l2.head(n_bigrams):
    print(f'\n+ __`{bigram}`__')
    print_md_table(sk.loc[sk.l2 == bigram, :],
                    title='\n  Association Measures', transpose=True, indent=2)
    for pol, hits in hit_tables.items():
        exdf = hits.loc[hits.bigram_lower == bigram, :]
        exdf = exdf.drop_duplicates('text_window').filter(items=relevant_col)
        if not any(exdf): 
            print(f'No examples of *{bigram}* in `{pol}` hits')
        elif len(exdf) > n: 
            exdf = exdf.sample(n)
        print_md_table(
            df=(exdf.sort_values([exdf.columns[0], exdf.columns[4]])
                .reset_index(drop=True)),
            title=f'\n  {n} Random `{pol}` Hits', indent=2)
            # samples.append(
            # sample_pickle(
            # data_path=path, sample_size=1,
            # filters=[f'bigram_lower=={bigram}'],
            # columns=relevant_col,
            # print_sample=False)
            # )


# %%
