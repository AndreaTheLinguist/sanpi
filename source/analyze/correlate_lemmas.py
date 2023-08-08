import pandas as pd
from matplotlib import pyplot as plt, rcParams
from pathlib import Path
# from scipy.stats import zscore
# from scipy.spatial.distance import (
# cosine,
# # jensenshannon as jenshan,
# # minkowski as mkow
# )

import numpy as np
from sys import argv
from math import sqrt
# from sklearn import cluster, decomposition as decomp
STRONG_CORR_MIN = 0.7
# rcParams['font.family'] = 'Liberation Serif'
rcParams['font.family'] = 'Nimbus Roman'
RESULTS_DIR = Path('/share/compling/projects/sanpi/results')


def _main():

    input_csv = get_data_path()
    frq_table = load_raw(input_csv)
    print(frq_table.shape[0], 'rows (adj)')
    print(frq_table.shape[1], 'columns (adv)')
    corr_dfs = correlate_axes(frq_table, input_csv)

    examine_correlations(input_csv, frq_table, corr_dfs)


def get_data_path():
    default = RESULTS_DIR.joinpath(
        'freq_out/all-frq_thresh8777.35f.csv'
        # '/share/compling/projects/sanpi/results/transformed/sqrt_all-frq_thresh8777.35f.csv'
    )
    try:
        arg_val = argv[1]
    except IndexError:
        return default
    print('input data given:', arg_val)
    return Path(arg_val) if Path(arg_val).is_file() else default


def load_raw(input_csv):
    frq_table = pd.read_csv(input_csv)

    frq_table = list(gen_axes(frq_table))[0]
    # frq_table = frq_table.apply(pd.to_numeric, downcast='unsigned')

    frq_table = remove_totals(frq_table)
    frq_table.index = frq_table.index.astype('string')
    return frq_table


def remove_totals(frq_table: pd.DataFrame,
                  total_label='SUM') -> pd.DataFrame:

    frq_table = frq_table.loc[
        frq_table.index != total_label,
        frq_table.columns != total_label]

    return frq_table


def gen_axes(table: pd.DataFrame, cols_name='adv_lemma', rows_name='adj_lemma'):
    if cols_name in table.columns:
        table = table.set_index(cols_name)
        if cols_name != rows_name:
            table = table.T
    if table.index.name != rows_name:
        if rows_name in table.columns:
            table = table.set_index(rows_name)
        else:
            table.index.name = rows_name

    table.columns.name = cols_name
    table.columns = table.columns.astype('string')
    table.index = table.index.astype('string')
    downtype = 'float' if '.' in str(table.iat[0, 0]) else 'unsigned'
    yield table.apply(pd.to_numeric, downcast=downtype)


def correlate_axes(frq_table: pd.DataFrame,
                   input_path: Path,
                   sample_n=20) -> tuple:
    sample_lemmas = {
        'adv': frq_table.T.sample(sample_n).sort_index().index.to_list(),
        'adj': frq_table.sample(sample_n).sort_index().index.to_list()
    }
    adv_output_stem = configure_paths(input_path, 'adv').with_suffix('.csv')
    adj_output_stem = configure_paths(input_path, 'adj').with_suffix('.csv')

    if adv_output_stem.is_file():
        yield from gen_axes(pd.read_csv(adv_output_stem), rows_name='adv_lemma')
    else:
        yield from correlate_columns(frq_table, sample_lemmas)

    if adj_output_stem.is_file():
        yield from gen_axes(pd.read_csv(adj_output_stem), cols_name='adj_lemma')
    else:
        yield from correlate_columns(frq_table, sample_lemmas,
                                     transpose=True)

    # return adverb_corr, adject_corr


def correlate_columns(frq_table,
                      sample_lemmas,
                      method='spearman',
                      transpose=False):
    pos = 'adv'
    if transpose:
        pos = 'adj'
        frq_table = frq_table.transpose()

    corr_matrix = get_corr(frq_table, method)
    # sqrt_corr_matrix = get_corr(frq_table, method, square_root=True)
    # if all(corr_matrix == sqrt_corr_matrix):
    #     print('[ℹ️] Spearman correlations are unaffected by square root transformation.')
    # >  heatmap for sample table
    # heatmap(sample_table.corr(method=method))
    visualize_samples(sample_lemmas, pos, corr_matrix)
    # visualize_samples(sample_lemmas, pos, corr_matrix, sqrt_corr_matrix)
    # heatmap(corr_matrix)

    yield corr_matrix


def visualize_samples(sample_lemmas: dict, pos: str,
                      corr_matrix: pd.DataFrame,
                      sqrt_corr_matrix: pd.DataFrame = None):
    output_stem = RESULTS_DIR.joinpath(
        f'freq_out/spearman/heatmaps/{pos.upper()}_sample_corr')
    indexer = sample_lemmas[pos]
    heatmap(corr_matrix.loc[indexer, indexer],
            # save_path=output_stem.with_suffix('.raw.png'))
            save_path=output_stem.with_suffix('.png'))
    if sqrt_corr_matrix is not None:
        heatmap(sqrt_corr_matrix.loc[indexer, indexer],
                save_path=output_stem.with_suffix('.sqr.png'))


def get_corr(frq_table,
             method='spearman',
             square_root=False):
    if square_root:
        frq_table = transform_counts(frq_table, plus1=True)
    return frq_table.corr(method=method).apply(pd.to_numeric, downcast='float')


def examine_correlations(input_csv: Path, frq_table: pd.DataFrame,
                         corr_dfs: tuple):

    print('# Spearman Correlations between Lemmas\n')

    for axis_name, matrix in zip(['adv', 'adj'], corr_dfs):
        examine_corr_for_axis(frq_table, input_csv, axis_name, matrix)


def examine_corr_for_axis(frq_table, input_path, axis_name, matrix):

    out_stem_path = configure_paths(input_path, axis_name)
    save_corr_csv(matrix, out_stem_path)
    corr_md_path = out_stem_path.with_suffix('.md')

    if axis_name == 'adj':
        print('\n---\n')
        frq_table = frq_table.T

    out_text = '\n'.join(generate_lines(
        axis_name, matrix, frq_table, out_stem_path))
    corr_md_path.write_text(out_text, encoding='utf8')
    print(f'✍ (◔◡◔) ✓ Correlation info written to:\n> {corr_md_path}')
    # for g, value in corr_grps.items():
    #     print('Group', g.upper())
    #     print(value.index.to_list())


def configure_paths(input_path: Path, axis_name: str):
    output_dir = set_output_dir(input_path)
    data_stem = input_path.stem.replace('.', '-')
    return output_dir.joinpath(f'{data_stem}_{axis_name}-corr')


def save_corr_csv(matrix: pd.DataFrame, out_stem: str):
    out_path = out_stem.with_suffix('.csv')
    if not out_path.is_file():
        matrix.to_csv(out_path)


def generate_lines(axis_name, matrix, frq_table, out_stem_path):
    yield f'# Speaman correlations between _{axis_name}_'
    print(f'## Speaman correlations between _{axis_name}_')

    # corr_grps = {}
    for ix, lemma_col in enumerate(matrix.columns):
        # new_lines, high_corr_frqs = eval_corr_for_lemma(
        yield from eval_corr_for_lemma(
            ix + 1, matrix, axis_name, frq_table, lemma_col, out_stem_path)

        # corr_grps[lemma_col] = high_corr_frqs


def eval_corr_for_lemma(ix, matrix, axis_name, frqs, lemma, out_stem_path):

    c_corr = matrix.loc[matrix.index != lemma, lemma]
    high_corr = c_corr[c_corr >= STRONG_CORR_MIN]
    high_corr = high_corr.to_frame('sp_corr').assign(abs_corr=high_corr.abs())
    high_corr = high_corr.sort_values('abs_corr', ascending=False)
    high_corr_count = len(high_corr)
    high_corr.pop('abs_corr')
    # ! `squeeze()` cannot be used because any single cell dataframe would turn into a single value, rather than a single index series
    high_corr = high_corr['sp_corr']
    high_corr_cols = [lemma] + high_corr.index.to_list()

    display_corr = high_corr_count + 8
    print(f'\n### ({ix}) {lemma}\n')

    print(f'**{high_corr_count}** strong correlations with `{lemma}` found')
    # if high_corr_count > 0:
    #     print(high_corr.round(3).to_frame(
    #         f'corr ≥ {STRONG_CORR_MIN}').to_markdown())
    # print(f'\nTop {display_corr} spearman values\n')
    # print(view_N_corr(matrix, lemma=c, N=display_corr, as_markdown=True))
    # print(c_corr.nlargest(display_corr).to_frame(
    #     f'Top `{c}` Correlates').round(2).to_markdown(), '\n')

    yield f'\n### {axis_name} {ix}: *`{lemma}`*\n'
    yield f'**{high_corr_count} strong correlations with `{lemma}` found**'
    if high_corr_count > 0:
        yield high_corr.round(3).to_frame(f'correlation ≥ {STRONG_CORR_MIN}').to_markdown()
    yield f'\nTop **{display_corr}** spearman values\n'
    yield view_N_corr(matrix, lemma=lemma, N=display_corr, as_markdown=True)

    high_corr_frqs = frqs.loc[:, high_corr_cols]
    yield from assess_corr_freqs(high_corr_frqs, lemma, axis_name, out_stem_path)

    # yield high_corr_cols, lines
    # return new_lines


def set_output_dir(input_csv):
    output_dir = input_csv.with_name('spearman')
    if not output_dir.is_dir():
        output_dir.mkdir()
    return output_dir


def heatmap(df, columns=None, save_path=None, size=(8, 10), title=''):

    df, title = prepare_data_to_plot(df, columns, title)
    plt.figure(figsize=size, dpi=120, facecolor="white")

    # Displaying dataframe as an heatmap
    # with diverging colourmap as RdYlBu
    plt.imshow(df, cmap="plasma")
    # plt.imshow(df, cmap="gist_rainbow")
    # plt.imshow(df, cmap="jet")
    # plt.imshow(df, cmap="viridis")
    # plt.autoscale(enable=True, axis='both')
    # Displaying a color bar to understand
    # which color represents which range of data
    plt.colorbar()
    # Assigning labels of x-axis
    # according to dataframe
    try:
        plt.xticks(range(len(df.columns)), df.columns,
                   rotation=-90, fontsize=9)
    except TypeError:
        pass
    # Assigning labels of y-axis
    # according to dataframe
    try:
        plt.yticks(range(len(df.index)), df.index, fontsize=9)
    except TypeError:
        pass
    # Displaying the figure
    plt.title(title)
    if save_path:
        plt.savefig(save_path, dpi=300, format='png')
    plt.show()
    plt.close()


def prepare_data_to_plot(df, columns=None, title=''):
    if bool(columns):
        df = df.loc[:, columns]
    df = df.astype('float')
    if len(df.columns) > (len(df) + 5):
        df = df.T
        title += ' (rotated!)'
    return df, title


def view_N_corr(corr_df, lemma, N,
                weakest=False,
                exclude_self=True,
                as_markdown=False):

    strength = 'LEAST' if weakest else 'MOST'
    if lemma not in corr_df.index:
        return
    col_label = f'{strength} correlated w/ `{lemma}`'
    lemma_corr = corr_df[lemma]
    if exclude_self and lemma in lemma_corr.index:
        not_self = lemma_corr.index != lemma
        lemma_corr = lemma_corr[not_self]
    selection = get_view_selection(N, weakest, lemma_corr)

    lemma_corr = lemma_corr[selection]
    lemma_df = (lemma_corr.to_frame(col_label)).round(3)

    if as_markdown:
        return lemma_df.to_markdown(floatfmt='.3f')

    return lemma_df.round(3)


def get_view_selection(N, weakest, lemma_corr):
    abs_corr = lemma_corr.abs()

    selection = abs_corr.nsmallest(N) if weakest else abs_corr.nlargest(N)
    return selection.index


def assess_corr_freqs(high_corr_raw, lemma, axis_name, out_stem_path):
    row_name = 'adj' if axis_name == 'adv' else 'adv'
    # TODO: come back to this and see if it's meaningful!!
    if len(high_corr_raw.columns) >= 3:
        frq_variations = gen_frq_info(high_corr_raw, lemma)
        # frq_labels = (
        #     # f'Top raw frequencies {row_name} for strongly correlated {axis_name}',
        #     f'Square root transformed frequencies of most common {row_name} for {axis_name} strongly correlated with `{lemma}`',
        #     # f'Raw frequencies standardized by {axis_name.strip("s")} means',
        #     f'Square root transformed frequencies standardized by {axis_name} means',
        # )
        main_title = (f'Most common {row_name} for {axis_name} strongly '
                      + f'correlated with `{lemma}`:')
        frq_labels = {
            'sqrt': (f'{main_title} Square root transformed frequencies'),
            'mstd': (f'{main_title} Square root standardized by {axis_name} means')
        }

        # dfs = (high_corr_raw,) + frq_variations
        dfs = tuple(frq_variations)

        yield from visualize_lemma_corr(dfs, frq_labels, out_stem_path, lemma)


def visualize_lemma_corr(frq_dfs: tuple,
                         frq_labels: dict,
                         out_stem_path: Path,
                         lemma_col: str):

    heat_dir = out_stem_path.with_name('heatmaps')
    if not heat_dir.is_dir():
        heat_dir.mkdir()

    for i, label in enumerate(frq_labels):
        frq_df = frq_dfs[i]
        title = frq_labels[label]
        yield (f'\n{title}')
        yield from print_head(frq_df, lemma_col)
        heat_path = heat_dir.joinpath(
            f'{out_stem_path.name}_{lemma_col.upper()}-top30-{label}.png')
        heatmap(frq_df.head(30),
                save_path=heat_path,
                title=title)
    # > was:
    # for i, frq_df in enumerate(frq_dfs):
    #     label = frq_labels[i]
    #     print(f'\n{label}')
    #     print_head(frq_df, lemma_col)
    #     heat_path = heat_dir.joinpath(
    #         f'{out_stem_path.name}_{lemma_col.upper()}-top30-heatmap.v{i}.png')
    #     heatmap(frq_df.head(30), save_path=heat_path,
    #             title=f'{lemma_col.upper()}: {label}')


def gen_frq_info(high_corr_raw, lemma_str):
    high_corr_sqrt = transform_counts(high_corr_raw)
    # ms_high_corr_raw, __ = standardize(high_corr_raw)
    ms_high_corr_sqrt, __ = standardize(high_corr_sqrt)
    # return high_corr_sqrt, ms_high_corr_raw, ms_high_corr_sqrt
    # return high_corr_sqrt, ms_high_corr_sqrt
    yield high_corr_sqrt
    yield standardize(high_corr_sqrt)[0]


def transform_counts(df: pd.DataFrame,
                     method: str = 'sqrt',
                     plus1: bool = False):
    if plus1 or method.startswith('log'):
        df = df.add(1)
    if method == 'sqrt':
        df = df.apply(lambda x: x.apply(sqrt))
    elif method == 'log10':
        df = df.apply(lambda x: x.apply(np.log10))
    elif method == 'log2':
        df = df.apply(lambda x: x.apply(np.log2))
    return df


def standardize(df, verbose=False):
    if any(df.mean() == 0):
        print('WARNING: data contains vectors with mean of 0')
    token_info = df.mean().to_frame().rename(columns={0: 'token_mean'})
    if verbose:
        print(token_info.assign(total=df.sum())
              .sort_values('token_mean', ascending=False))
    mdf = df.apply(lambda col: col / (col.mean()))
    # z = s.apply(zscore)
    # m.columns = 'ms_' + m.columns
    # z.columns = 'zs_' + z.columns
    # print('standard deviation of mean-standardized columns')
    cvar = mdf.apply(pd.DataFrame.std).round(3)
    # print('coefficient of variation of raw frequency columns (std/mean)')
    # print([round(s[c].std()/s[c].mean(), 3) for c in s.columns])
    # return m, z, cvar
    return mdf, cvar


def print_head(corr_frqs, sort_col):  # sourcery skip: avoid-builtin-shadow
    format = ',.0f' if max(corr_frqs.max()) > 1000 else '.1f'
    corr_frqs.round(1).sort_values(sort_col, ascending=False)
    # print(corr_frqs.head(15).to_markdown(floatfmt=format))
    yield corr_frqs.head(15).to_markdown(floatfmt=format)


if __name__ == '__main__':
    _main()
