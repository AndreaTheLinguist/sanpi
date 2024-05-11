import contextlib
import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from source.utils.dataframes import (Timer, corners, describe_counts,
                                     print_md_table, set_count_dtype,
                                     sort_by_margins, square_sample,
                                     transform_counts)
from source.utils.general import FREQ_DIR, confirm_dir, print_iter
from source.utils.visualize import heatmap


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),  # TODO add description message
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-t', '--threshold',
        type=str, default='clean',
        help=('flag indicating frequency (percentage) threshold applied in filenames. '
              '"001" will point to `0-001`, "01" will point to `0-01`, etc.')
    )
    parser.add_argument(
        '-p', '--pattern',
        type=str, default='NEGmirror',
        help=('pattern category (i.e. directory in ./Pat/) to get complement of')
    )
    parser.add_argument(
        '-f', '--freq_out_dir',
        type=Path, default=FREQ_DIR,
        help='path to directory housing frequency tables'
    )
    parser.add_argument(
        '-d', '--describe',
        action='store_true',
        help=('whether to produce additional descriptive information files.')
    )
    return parser.parse_args()


N_FILES = 35
args = _parse_args()
THR_DEC_STR = args.threshold
DESCRIBE = args.describe
PAT_CAT = args.pattern
FREQ_OUT = args.freq_out_dir


def _main():
    if '+' in PAT_CAT:
        pat_1, pat_2 = PAT_CAT.split('+')

        frq_path_1, all_frq_path = locate_freq_tables(pat_1)
        frq_path_2, __ = locate_freq_tables(pat_2, verbose=False)
        pat_frq_path = FREQ_OUT.joinpath(
            f'combined_{PAT_CAT.replace("+","-")}/{frq_path_1.name}')
        confirm_dir(pat_frq_path.parent)

        # * load frequency table for ALL bigram tokens
        all_frq = sort_by_margins(load_baseline(
            all_frq_path, describe=DESCRIBE))

        df1 = load_pattern_counts(
            frq_path_1, describe=False).reindex_like(all_frq).fillna(0)
        df2 = load_pattern_counts(
            frq_path_2, describe=False).reindex_like(all_frq).fillna(0)
        pat_only = df1 + df2

    else:
        pat_frq_path, all_frq_path = locate_freq_tables()

        # * load frequency table for PAT tokens
        pat_only = load_pattern_counts(pat_frq_path)

        # * load frequency table for ALL bigram tokens
        all_frq = load_baseline(all_frq_path, describe=DESCRIBE)

    # * Adjust the shape
    pat_frq = adjust_shape(pat_only, all_frq, pat_frq_path)

    print(f'\n## Words with 0 tokens in the `{PAT_CAT}` results')
    adj_not_in_pat = pat_frq['SUM'] == 0
    print_md_table(pat_frq.loc[adj_not_in_pat, ['SUM']]
                   .join(all_frq.loc[adj_not_in_pat, ['SUM']],
                         lsuffix=f'_{PAT_CAT}'),
                   title='\n### Adjectives\n')

    adv_not_in_pat = pat_frq.T['SUM'] == 0
    print_md_table(pat_frq.T.loc[adv_not_in_pat, ['SUM']]
                   .join(all_frq.T.loc[adv_not_in_pat, ['SUM']],
                         lsuffix=f'_{PAT_CAT}'),
                   title='\n### Adverbs\n')

    print('\n## The Difference\n')
    # > calculate the difference by simple matrix subtraction
    frq_diff = all_frq - pat_frq
    print_md_table(corners(frq_diff, 3))

    # set the path
    pat_dir = pat_frq_path.parent
    frq_diff_dir = pat_dir / 'complement'
    confirm_dir(frq_diff_dir)

    frq_diff_pkl = frq_diff_dir.joinpath(
        f'diff_{pat_dir.name}-{all_frq_path.name}'
        .replace(f'{pat_dir.name}-all', f'all-{pat_dir.name}')
    )

    frq_diff = set_count_dtype(frq_diff, frq_diff_pkl)
    if DESCRIBE:
        describe_counts(frq_diff, frq_diff_pkl)
    # if path doesn't point to a file, save the table as path
    if not frq_diff_pkl.is_file():
        frq_diff.to_pickle(frq_diff_pkl)
    print(f'\n✅ complement frequency table saved as `{frq_diff_pkl}`')

    print_md_table(frq_diff['SUM'].describe().round(2).to_frame()
                   .rename(columns={'SUM': f'non-`{PAT_CAT}` ADJ totals'}), n_dec=2,
                   title='\n### Adverb stats for complement\n')

    print_md_table(frq_diff.T['SUM'].describe().round(2).to_frame().rename(
        columns={'SUM': f'non-`{PAT_CAT}` ADV totals'}), n_dec=2,
        title='\n### Adverb stats for complement\n'
    )

    print('\n## Frequency Table Corners')
    print_md_table(corners(all_frq, 4),
                   title='\n### ALL\n')

    print_md_table(corners(pat_frq.reindex_like(all_frq), 4),
                   title=f'\n### `{PAT_CAT}`\n')

    print_md_table(corners(frq_diff.reindex_like(all_frq), 4),
                   title='\n### _Complement_\n')
    print()

    # * ## Visualizations
    __ = visualize_samples(pat_frq, all_frq, frq_diff)

    frq_dfs = {
        'all': all_frq,
        PAT_CAT: pat_frq,
        'diff': frq_diff}
    print('\n## Top Values')
    for name, df in frq_dfs.items():
        print_md_table(sort_by_margins(df).iloc[:16, :11],
                       title=f'\n### Top (15 x 10) collocations in {name.upper()} frequencies (+ SUM)\n')
    print('\n## Totals')
    print_md_table(pd.Series({name.upper(): frq_df.loc['SUM', 'SUM']
                              for name, frq_df in frq_dfs.items()}
                             ).to_frame('totals'),
                   title='\n### Total Tokens per Frequency Group\n')

    for name, frq_df in frq_dfs.items():
        print_md_table(frq_df['SUM'].iloc[1:].describe().to_frame('individual adj totals').join(
            frq_df.T['SUM'].iloc[1:].describe().to_frame('individual adv totals')),
            title=f'\n### Marginal Frequencies for {name.upper()} Bigram Tokens\n')

    top_n = 30
    _compare_grp_totals(pat_frq, frq_diff, all_frq, top_n)


def sample_counts(frq_table, label,
                  rows=pd.Series(dtype='string'),
                  columns=pd.Series(dtype='string'),
                  color="nipy_spectral_r"):
    # color = 'Set1'
    # color = 'gist_rainbow'

    s = frq_table.copy()
    if not any(rows):
        s = s[s.index != 'SUM']
        s = s.iloc[5:int(frq_table.shape[0]*0.4),
                   :] if len(s.index) >= 80 else s
        rows = s.sample(min(len(s), 16)).index
    if not any(columns):
        s = s.loc[:, s.columns != 'SUM']
        s = s.iloc[:, 5:int(frq_table.shape[1]*0.4)
                   ] if len(s.columns) > 50 else s
        columns = s.T.sample(min(len(s.T), 8)).index
    sample_df = s.loc[rows, columns]
    # print(sample_df.describe().T.round(2).to_markdown())
    # fig = plt.figure(figsize=(6, 8), dpi=300)
    fig = plt.figure(dpi=130)
    # ax.barh(s20x10, width=1)
    sample_df.plot(kind='barh',
                   width=0.8,
                   figsize=(8, 10),
                   position=1,
                   title=f'{label} of sample',
                   grid=True,
                   colormap=color,
                   # colormap="gist_rainbow",
                   # colormap="rainbow",
                   #  colormap="brg",
                   #   colormap="nipy_spectral_r",
                   #    colormap="Set1",
                   ax=plt.gca())
    plt.show()
    fig = plt.figure(dpi=150)
    sample_df.plot(kind='barh',
                   stacked=True,
                   width=0.8,
                   figsize=(8, 10),
                   position=1,
                   title=label,
                   grid=True,
                   colormap=color,
                   # colormap="gist_rainbow",
                   #  colormap="brg",
                   #    colormap="nipy_spectral_r",
                   #    colormap="Set1",
                   ax=plt.gca()
                   )
    plt.show()

    heatmap(sample_df, size=(8, 10))  # default colormap ➡️ `'plasma'`
    # print(sample_df.round().to_markdown(floatfmt=',.0f'))

    return s, sample_df


def seek_frq_table(meta_tag_glob, parent_dir: str = 'RBdirect', stem_glob: str = None):

    stem_glob = (stem_glob or f'all*adj-x-adv*{meta_tag_glob}*'
                 ).replace('**', '*')
    glob_dir = (FREQ_OUT.joinpath(parent_dir).joinpath(f'partials/{N_FILES}f')
                if N_FILES < 35 and parent_dir == 'RBXadj'
                else FREQ_OUT.joinpath(parent_dir))
    frq_path = None
    try:
        frq_path = list(glob_dir.glob(f'{stem_glob}.pkl.gz'))[0]

    except IndexError:
        try:
            frq_path = list(glob_dir.glob(f'{stem_glob}.csv'))[0]
        except IndexError:
            glob_dir = FREQ_OUT.joinpath(parent_dir).joinpath('ucs_format')
            if glob_dir.is_dir():
                stem_glob = stem_glob.replace('all*adj-x-adv*','adv-x-adj*')
                with contextlib.suppress(IndexError):
                    frq_path = list(glob_dir.glob(f"{stem_glob}.tsv"))[0]

    if frq_path is None:
        raise FileNotFoundError('⚠️ frequency table corresponding to '
                                f'{stem_glob} not found in {parent_dir}.')
    return frq_path


def locate_freq_tables(_pat_cat=PAT_CAT, verbose=True):
    thresh_tag = (f'0-{THR_DEC_STR}'
                  if THR_DEC_STR.startswith(tuple('0123456789'))
                  else THR_DEC_STR)
    meta_tag_glob = f'{thresh_tag}*.{N_FILES}f'
    # ! will be embedded between *, so should not start or end with * to avoid an unintended ** situation

    if verbose:
        print('# Comparing Bigram Frequencies by Polarity\n',
              f'- for `{N_FILES}` corpus input `.conll` directories containing source `.conllu` files',
              (f'- with word types limited to only those that account for at least {THR_DEC_STR}'
               f' of the cleaned dataset (as sourced from {N_FILES} corpus file inputs)'),
              f'- file identifier = `{meta_tag_glob}`',
              sep='\n')

    paths = [seek_frq_table(meta_tag_glob, d) for d in (_pat_cat, 'RBXadj')]

    if verbose:
        with contextlib.suppress(AttributeError):
            global_count_floor = re.search(r'=(\d+)\+', paths[1].stem).groups()[0]
            print('- pattern matches restricted to only token word types with at least '
                f'`{global_count_floor}` total tokens across all combinations')
    print_iter((f'`{p}`' for p in paths),
               bullet='-', indent=2,
               header='- Selected Paths')

    return paths


def load_freq_table(frq_path):
    # // return set_count_dtype(pd.read_pickle(frq_pkl), frq_pkl)
    frq_df = pd.read_csv(
        frq_path) if frq_path.suffix == '.csv' else pd.read_pickle(frq_path)
    meta_col = frq_df.columns[frq_df.columns.str.contains(
        '_')].to_series().squeeze()
    if any(meta_col):
        if frq_df.index.name:
            frq_df = frq_df.reset_index()

        frq_df = frq_df.set_index(meta_col)

    elif not frq_df.index.name:
        frq_df.index.name = 'adj_form_lower'

    if not frq_df.columns.name:
        frq_df.columns.name = 'adv_form_lower'

    frq_df = frq_df.apply(pd.to_numeric, downcast='unsigned')

    if frq_path.suffix == '.csv':
        frq_df.to_pickle(frq_path.with_suffix('.pkl.gz'))
    return frq_df


def adjust_shape(pat_only, all_frq, pat_frq_path):
    print('👀 sanity checks:')

    print(f'only {PAT_CAT} dim:', pat_only.shape)
    print('     ALL dim:', all_frq.shape)

    pat_frq = set_count_dtype(pat_only.copy().reindex_like(all_frq).fillna(0),
                              pat_frq_path.with_name(pat_frq_path.name.replace('all-frq', 'ALL-WORDS')))
    print('adjusted NEG:', pat_frq.shape)
    return pat_frq


def visualize_samples(pat_frq, all_frq, frq_diff):
    adv_list = sort_by_margins(
        pat_frq[['exactly', 'definitely', 'necessarily', 'fully', 'fairly', 'somewhat', 'particularly',
                'extremely', 'that', 'ever', 'remotely', 'slightly', 'utterly', 'absolutely']]
    ).columns.to_list()

    __, sample_all = sample_counts(transform_counts(
        all_frq), label='`RBXadj` √ Frequencies', columns=adv_list)

    adj_list = sample_all.sort_index().index.to_list()

    __, sample_neg = sample_counts(transform_counts(pat_frq).reindex_like(all_frq),
                                   rows=adj_list,
                                   columns=adv_list,
                                   label=f'`{PAT_CAT}` √ Frequencies')

    __, sample_diff = sample_counts(transform_counts(frq_diff).reindex_like(all_frq),
                                    rows=adj_list,
                                    columns=adv_list,
                                    label=f'`RBXadj - {PAT_CAT}` (Complement) √ Frequencies')

    compare_sample = pd.concat(
        [sample_neg.T.add_suffix('-NOT').T, sample_diff]).sort_index()
    compare_sample = compare_sample.iloc[:-6, :]

    # join(sample_diff).sort_index(axis=1)
    print(compare_sample.round(2).to_markdown(floatfmt='.2f'))

    __ = sample_counts(compare_sample, columns=compare_sample.columns,
                       rows=compare_sample.index, label='Polarity Comparison Sample')
    return __


def load_frequencies(frq_path:Path):
    if frq_path.parent == 'ucs_format': 
        frq_tsv = pd.read_csv(frq_path, sep='\t', header=None)
        frq_tsv.columns = ['f'] + frq_path.name.split('_')[0].split('-x-')
        return frq_tsv
    return load_freq_table(frq_path)


def load_pattern_counts(pat_frq_path, describe: bool=DESCRIBE):
    _pat = pat_frq_path.parent.name
    print(f'\n## _`{_pat}`_ Frequencies Overview\n')
    pat_only = load_frequencies(pat_frq_path)
    if describe:
        describe_counts(df=pat_only, df_path=pat_frq_path)

    print_md_table(corners(pat_only, 6),
                   title=f'\n### Full Table Preview of _`{_pat}`_ Frequencies\n')

    print_md_table(square_sample(
        pat_only.iloc[:301, :201], 7), title=f'\n### (Semi-)Random Sample of _`{_pat}`_ Frequencies\n')
    return pat_only


def load_baseline(all_frq_path, describe: bool = DESCRIBE):
    print(
        f'\n## _ALL_ (`{PAT_CAT}` and non-`{PAT_CAT}`) Frequencies Overview\n')
    all_frq = load_freq_table(all_frq_path)
    if describe:
        describe_counts(df=all_frq, df_path=all_frq_path)

    print("\n### Full Table Preview of _All_ Frequencies\n")
    print(corners(all_frq, 6))

    print_md_table(
        sort_by_margins(square_sample(
            all_frq.copy().iloc[:401, :301], 6)),
        title='\n### (Semi-)Random Sample of _ALL_ Frequencies\n')

    return all_frq


def get_ratio(df, all_frq, transpose=False):
    all_vals = all_frq.transpose() if transpose else all_frq
    return (df
            .apply(lambda c: c / all_vals['SUM'])
            .sort_values('SUM', ascending=False)
            .sort_values('SUM', axis=1, ascending=False))


def get_totals_frame(pat_frq, frq_diff, all_frq, transpose):
    if transpose:
        pat_frq = pat_frq.transpose()
        frq_diff = frq_diff.transpose()

    neg_ratio_frq = get_ratio(pat_frq, all_frq, transpose=transpose)
    diff_ratio_frq = get_ratio(frq_diff, all_frq, transpose=transpose)

    totals_df = neg_ratio_frq['SUM'].to_frame(f'{PAT_CAT}/ALL')
    totals_df['DIFF/ALL'] = diff_ratio_frq['SUM']
    totals_df[f'{PAT_CAT}_RAW'] = pat_frq['SUM']
    totals_df['DIFF_RAW'] = frq_diff['SUM']
    return totals_df.sort_values(['DIFF/ALL', 'DIFF_RAW'])


def _compare_grp_totals(pat_frq, frq_diff, all_frq,
                        top_n: int = 30):

    for transpose in (True, False):
        pos = 'ADV' if transpose else 'ADJ'
        _totals = get_totals_frame(
            pat_frq, frq_diff, all_frq, transpose=transpose)
        title = f'\n#### Top {top_n} {pos} totals comparison\n'
        print_md_table(_totals.head(top_n).round(2), title=title, n_dec=2)


if __name__ == '__main__':
    _main()
