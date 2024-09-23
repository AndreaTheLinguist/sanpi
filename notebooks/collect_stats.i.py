# %%
from pathlib import Path
import pandas as pd
# import json
# from pprint import pprint
from utils import file_size_round
subsets_dir = Path('/share/compling/data/sanpi/subsets')
# %%
data = {p.stem:
        {
            'parent': p.parent.name,
            'name': p.name,
            'path': p,
            'source_path': p.readlink(),
            'subset_corpus': p.parent.parent.stem,
            'is_link': p.is_symlink(),
            'size': file_size_round(p.stat().st_size),
        }
        for p in subsets_dir.rglob('*.conllu')
        }
bp_df = pd.DataFrame.from_dict(data, orient='index').convert_dtypes()
bp_df['init_conllu'] = bp_df.name.str.replace('BIGRAM.', '', regex=False)
bp_df['data_key'] = bp_df.index.str.replace('BIGRAM.', '', regex=False)
# bp_df = bp_df.set_index('name')
# bp_df.sample(1).T
# print(bp_df.sample(1).T.to_markdown())
# all(bp_df.is_link)

bp_df['corpus_part'], bp_df['corpus'], bp_df['subset_info_dir'] = zip(
    *bp_df.source_path.apply(
        lambda sp: (sp.parent.parent.stem,
                    sp.parent.parent.parent.stem,
                    sp.parent.joinpath('info')))
)
bp_df = bp_df.convert_dtypes()

print(bp_df.sample(1).T.to_markdown())
# // bp_df.join(pd.json_normalize(bp_df.index.to_series().apply(lambda ix:
# //   {'corpus_part':bp_df.source_path[ix].parent.parent.stem,
# //    'corpus': bp_df.source_path[ix].parent.parent.parent.stem,
# //    'subset_info_dir': bp_df.source_path[ix].parent.joinpath('info'),
# //    'index': ix
# //    })).set_index('index'))

# // bp_df['corpus_part', 'corpus', 'subset_info_dir'] = bp_df.source_path.apply(lambda sp: (sp.parent.parent.stem, sp.parent.parent.parent.stem, sp.parent.joinpath('info')))
# // bp_df['corpus_part'] = bp_df.source_path.apply(
# //   lambda sp: sp.parent.parent.stem)
# // bp_df['corpus'] = bp_df.source_path.apply(lambda p: p.parent.parent.parent.stem)
# // bp_df['subset_info_dir'] = bp_df.source_path.apply(lambda p: p.parent.joinpath('info'))


# %%

bp_df['path_index_csv'] = bp_df.subset_info_dir.apply(
    lambda i: max(i.glob('subset-bigram_path-index*csv'),
                  key=lambda file: file.stat().st_ctime))

# %%
X = bp_df.sample(1)

print(X.T.to_markdown())
X = X.squeeze()

# %% [markdown]

# Now to use these collected paths to access the compiled counts...

# %%
try:
    path_info = pd.read_csv(X.path_index_csv,
                            usecols=['STEM', ' INPUT_COUNTS', ' SUBSET_COUNTS']
                            ).set_index('STEM')
except ValueError:
    path_info = pd.read_csv(X.path_index_csv,
                            usecols=['STEM', 'INPUT_COUNTS', 'SUBSET_COUNTS']
                            ).set_index('STEM')

path_info.columns = path_info.columns.str.strip().str.lower()
path_info.columns

# %%
for stem in path_info.sample(3).T:
    print(f'- {stem}')
    print(f'  - input_counts = {path_info.input_counts[stem]}')
    print(f'  - subset_counts = {path_info.subset_counts[stem]}')

# %%
bp_df.index.name = 'subset_stem'
bp_df = bp_df.reset_index().set_index('data_key')
# %%
subframes = []
for path_ix, df in bp_df.groupby('path_index_csv'):
    print(path_ix)
    try:
        path_info = pd.read_csv(
            path_ix,
            usecols=['STEM', ' INPUT_COUNTS', ' SUBSET_COUNTS']
        ).set_index('STEM')
    except ValueError:
        path_info = pd.read_csv(
            path_ix,
            usecols=['STEM', 'INPUT_COUNTS', 'SUBSET_COUNTS']
        ).set_index('STEM')
    print(df.head(1).T.to_markdown())
    subframes.append(df.join(path_info))

meta_df = pd.concat(subframes)
meta_df.iloc[:, -2:] = meta_df.iloc[:, -2:].apply(lambda x: x.str.strip())
meta_df.columns = meta_df.columns.str.strip().str.lower()
# %%
Y = meta_df.sample(1).squeeze()

#%%
def load_totals(counts_path):
    counts_df = pd.read_json(counts_path)
    totals = counts_df.loc[:, 'total']
    return totals.dropna().to_dict()
# %%
in_counts_dict = {}
bg_counts_dict = {}
for data_key in meta_df.sample(50).index:

    in_counts_dict[data_key] = load_totals(meta_df.at[data_key, 'input_counts'])
    bg_counts_dict[data_key] = load_totals(meta_df.at[data_key, 'subset_counts'])
# %%   
in_counts_df = pd.DataFrame.from_dict(in_counts_dict, 
                       orient='index')
bg_counts_df = pd.DataFrame.from_dict(bg_counts_dict, 
                       orient='index')
print('\n### INPUTS\n', in_counts_df, sep='\n')
print('\n### BIGRAMS\n', bg_counts_df, sep='\n')
# %%
