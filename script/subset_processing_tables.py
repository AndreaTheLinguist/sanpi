from pathlib import Path
import pandas as pd

_DATA_DIR = Path('/share/compling/data/sanpi/corpora_shortcuts')


def table_counts(df, tally, grouper=None):
    obj = df.groupby(grouper) if grouper else df
    counts = obj.value_counts(tally).to_frame().rename(columns={0: 'counts'}) \
        .assign(percentage=((obj.value_counts(tally, normalize=True)*100).round(1)).astype('string')+'%')
    return counts


def _main():
    dir_glob = '[pn]*[_wt]?/*conll/subset_bigram/info'
    print(f'looking for latest .csv in {_DATA_DIR}/{dir_glob}')
    path_dfs = []
    for info_dir in _DATA_DIR.glob(dir_glob):
        csvs = list(info_dir.glob('*csv'))
        csvs.sort()
        path = csvs[-1]
        print(path)
        path_dfs.append(pd.read_csv(path).assign(source=path, corpus_chunk=info_dir.parts[-4]))
    print('total files read:', len(path_dfs))
    existing = pd.concat(path_dfs).convert_dtypes().set_index('STEM')

    existing.columns = existing.columns.str.lower().str.strip()

    out_cols = ['input_counts', 'subset_conllu',
                'subset_context', 'subset_counts']
    existing = existing.assign(
        corpus=existing.index.str.split('_', 1).str.get(0),
        incomplete=[any(existing.loc[i, out_cols] == ' ') for i in existing.index],
        complete=[all(existing.loc[i, out_cols] != ' ') for i in existing.index],
        in_progress=[
            any(existing.loc[i, out_cols] == ' ') 
            and any(existing.loc[i, out_cols] != ' ') for i in existing.index], 
        status='not started')
    existing.loc[existing.complete, 'status'] = 'completed ✓'
    existing.loc[existing.in_progress, 'status'] = 'in progress'
    print('### Everything\n')
    print(table_counts(existing, 'status').to_markdown())
    print('\n### By Corpus\n')
    by_corpus = table_counts(existing[['status', 'corpus', 'corpus_chunk']], 'status', 'corpus_chunk').reset_index()
    corp_names = {'pcc': 'puddin', 'apw': 'assoc_press', 'nyt':'new_york_times'}
    for cdir, cctab in by_corpus.groupby('corpus_chunk'):
        for c, ctab in cctab.groupby('corpus'):
            corpus = corp_names[c]
            if cdir.startswith('puddin'): 
                header = f'**`{corpus}`**: `{cdir}`'
            else:
                header = f'**`{cdir}`**: `{corpus}`'
            print(header)
            print(ctab.reset_index().set_index('status')[['counts', 'percentage']].to_markdown())
            print('\n---\n')
            
    is_missing = existing.isin(('', ' '))
    print(table_counts(is_missing.set_index(['corpus', 'input_conllu']), out_cols).reset_index().to_markdown())


if __name__ == '__main__':
    _main()
