# %% [markdown]
# # Comparing bigram associations with polarity for different methods
#
# 1. **mirror** comparison associations
# 1. (original) "set **complement**" associations

# %%
from pathlib import Path

import pandas as pd

UCS_DIR = Path('/share/compling/projects/sanpi/results/ucs')
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 200)

# %% [markdown]
# - "skewed" cutoff set to adjusted conditional probability of polar context `> 0.8`
# - loaded data contains rows for only pairings that occur `>= 15` times

# %%

COUNT_FLOOR = 15
THRESH = 0.8


def select_data(df):
    return (df.loc[df.am_p1_given2 > THRESH, :]
            # > remove the "rank" columns
            .filter(regex=r'^[^r][^_]'))

# %% [markdown]
# ## Set paths for current parameters

# %%


def set_paths():
    return {
        'mirr': {
            'csv': UCS_DIR.joinpath(
                f'readable/MIRROR_polar_bigram/polarized-bigram_MIRROR.35f-868thresh_min{COUNT_FLOOR}x.rsort-view.csv'),
            'pickle': UCS_DIR.joinpath(
                f'dataframes/polarized-bigram_MIRROR.35f-868thresh_min{COUNT_FLOOR}x.rsort-view_extra.pkl.gz')},
        'comp': {
            'csv': UCS_DIR.joinpath(
                f'readable/polarized_bigram/polarized-bigram_min{COUNT_FLOOR}x.rsort-view.csv'),
            'pickle': UCS_DIR.joinpath(
                f'dataframes/polarized-bigram_min{COUNT_FLOOR}x.rsort-view_extra.pkl.gz')}
    }


PATHS = set_paths()

# %% [markdown]
# ## Identify all skewed bigram-polarity pairings

# %%
def get_skewed(method, load_format):
    if load_format == 'csv':
        adf = pd.read_csv(PATHS[method]['csv'])
    else:
        adf = pd.read_pickle(PATHS[method]['pickle'])
    print(f'\n### {method} {load_format}\n')
    print(adf.head(3))
    
    skew_df = select_data(adf)
    
    skew_df.info()
    print(skew_df.l1.value_counts().to_frame('polarity totals in "skewed"'))
    print(f'### Top 10 skewed {method} (from {load_format})')
    print(skew_df.head(10).to_markdown(floatfmt='.2f'))
    
    return skew_df

# %% [markdown]
### Loading from `*.pkl.gz` tables

#### mirror associations (from `*.pkl.gz`)

# %%
get_skewed('mirr', 'pickle')

# %% [markdown]
#### complement associations (from `*.pkl.gz`)
# %%
get_skewed('comp', 'pickle')

# %% [markdown]
### Loading from `*.csv` tables

#### mirror associations (from `*.csv`)

# %%
get_skewed('mirr', 'csv')

# %% [markdown]
#### complement associations (from `*.csv`)
# %%
get_skewed('comp', 'csv')


# %% [markdown]
# ### mirror associations (from `*.pkl.gz`)

# %%
get_skewed('mirr', 'pickle')

# %% [markdown]
# ### complement associations (from `*.pkl.gz`)
# %%
get_skewed('comp', 'pickle')
