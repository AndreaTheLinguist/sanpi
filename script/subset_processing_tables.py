from pathlib import Path
from sys import argv

import pandas as pd


def table_counts(df, tally, grouper=None):
    obj=df.groupby(grouper) if grouper else df
    counts = obj.value_counts(tally).to_frame().rename(columns={0:'counts'}) \
    .assign(percentage=obj.value_counts(tally, normalize=True).round(3)*100)
    return counts

def _main():
    dir_glob = '*conll/subset_bigram/info/'
    file_glob = '*04-05_15*.csv' if len(argv) == 1 else argv[1]
    path_dfs = []
    for corpdir in (Path('/share/compling/data/news'), Path('/share/compling/data/puddin')):
        for path in corpdir.glob(dir_glob + file_glob):
            path_dfs.append(pd.read_csv(path).assign(source=path))

    existing = pd.concat(path_dfs).convert_dtypes().set_index('STEM')

    existing.columns = existing.columns.str.lower().str.strip()

    out_cols = ['input_counts', 'subset_conllu', 'subset_context', 'subset_counts']
    existing = existing[out_cols].assign(
        corpus=existing.index.str.split('_', 1).str.get(0),
        incomplete=[any(existing.loc[i, :] == ' ') for i in existing.index],
        complete=[all(existing.loc[i, :] != ' ') for i in existing.index],
        partial=[any(existing.loc[i, out_cols] == ' ') 
                 and any(existing.loc[i, out_cols] != ' ') 
                 for i in existing.index])

    print(table_counts(
        existing, ['partial', 'incomplete', 'complete']).reset_index().to_markdown())

    print(table_counts(existing.loc[:,['partial', 'complete', 'corpus']], 
                       ['complete', 'partial'], 'corpus').reset_index().to_markdown())

if __name__ == '__main__':
    _main()
