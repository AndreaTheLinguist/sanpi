# coding=utf-8
import re
import pandas as pd

from collections import namedtuple as ntp
from os import system
from pathlib import Path
from sys import exit as syxit

import argparse

from utils import save_in_lsc_format as save_lsc  # pylint: disable=import-error
from utils import get_proc_time  # pylint: disable=import-error

cluster = ntp('Cluster', ['index', 'probability', 'features'])
cluster_feat = ntp('Features', ['R', 'J'])
word = ntp('Word', ['lemma', 'prob'])

_SANPI_DIR = Path('/share/compling/projects/sanpi')
_LSC_DIR = _SANPI_DIR.joinpath('source/LSC')
_FREQ_OUT_DIR = _SANPI_DIR.joinpath('results/freq_out')


def _main():
    mod_bin_path, view_size, frq_path, k, i, metric_name = _parse_args()

    if not mod_bin_path:
        if frq_path.exists() and frq_path.suffix == '.csv':
            mod_bin_path = train_model(frq_path, k, i)
        else:
            syxit('Error: No valid frequency data or binary model specified. Exiting.')

    mod_txt_path = textify_model(mod_bin_path, view_size)

    # * load text model & apply stats filter
    text = mod_txt_path.read_text(encoding='utf8')

    # ! pasted in 👇
    # find stats csv files (2 = 1 for adv, 1 for adj)
    stats_dir = _FREQ_OUT_DIR.joinpath('descriptive_stats')
    if not stats_dir.is_dir():
        syxit('Error: stats dir not found.')

    stats_path_key = mod_bin_path.name.split('_m')[0]
    print(f'+ Seeking stats for `{stats_path_key}` data')
    stats_paths = tuple(stats_dir.glob(f'*{stats_path_key}*'))

    if not stats_paths:
        syxit('Error: No corresponding stats found. Exiting.')

    if len(stats_paths) > 2:
        syxit('Error: data key is ambiguous. Too many stats tables found.')

    # load stats and isolate stats metric to filter on
      # metric_name = 'var_coeff' name of column in stats csvs
    for path in stats_paths:
        # > there should be only 2 paths for fully informative keys
        p_lower = path.name.lower()
        if 'adj' in p_lower:
            adj_metric = load_stat(metric_name, path, lemma_col='adj_lemma')
        elif 'adv' in p_lower:
            adv_metric = load_stat(metric_name, path, lemma_col='adv_lemma')
            # adv_metric = pd.read_csv(path, usecols=['adv_lemma', metric_name]).convert_dtypes().set_index('adv_lemma').sort_values(metric_name).squeeze()

    # filter text
    filter_mod_txt_path = mod_txt_path.with_stem(
        mod_txt_path.stem + f'_{metric_name}-filter')
    keep_lemmas = []
    for series in (adj_metric, adv_metric):
        keep_lemmas.extend(filter_lemmas(series))
    keep_strings = tuple(keep_lemmas) + ('---', 'Number', 'Cluster', 'Feature')
    filtered_lines = []
    print('=============================================')
    # print('```{text}')
    for line in text.splitlines():
        if line.strip().startswith(keep_strings):
            # print(line)
            filtered_lines.append(line)
    # print('```')
    # print('=============================================')
    filter_mod_txt_path.write_text('\n'.join(filtered_lines))
    print(f'\nModel text filtered by {metric_name} saved as {filter_mod_txt_path.relative_to(_SANPI_DIR)} ')
    # ! pasted in 👆

    # * parse text model info into table(s)
    sections = re.split(r'\n-{4,}\n', text)
    n_clust = parse_preamble(view_size, sections)

    parse_model(mod_bin_path, view_size, sections, n_clust)


def load_stat(metric_name, p, lemma_col):
    return pd.read_csv(p, usecols=[lemma_col, metric_name]).convert_dtypes().set_index(lemma_col).sort_values(metric_name).squeeze()


def filter_lemmas(metric):
    desc = metric.describe()
    Q1 = desc['25%']
    lower_fence = Q1 - 1.5 * (desc['75%'] - Q1)
    keep_lemmas = metric.loc[metric > Q1].index.astype('string').dropna().to_list()
    return keep_lemmas


def parse_preamble(view_size, sections):
    preamble = sections.pop(0)
    n_clust, n_feat = [int(n) for n in re.findall(r'\d+', preamble.strip())]
    feat_quant = 'both' if n_feat == 2 else f'all {n_feat}'
    print(f'+ Converting top {view_size} lemmas into `lemma ×',
          f'probability for cluster` table for {feat_quant}',
          f'selectional features in all {n_clust} clusters.')

    return n_clust


def parse_model(mod_bin_path, view_size, sections, n_clust):
    Rp_frames = []
    Jp_frames = []
    R_lemmas = set()
    J_lemmas = set()
    overall_p = pd.Series(dtype='float')

    for x in [re.split(r'(Cluster \d+)', s.strip())[1:] for s in sections]:
        clust_id = x[0].replace('Cluster ', 'C')
        clp_flt = float(x[1].split('\n', 1)[0].strip())
        overall_p[clust_id] = clp_flt

        feat_str = x[1].split('\n', 1)[1]
        # print(f'{clust_id}: {round(clp_flt*100, 2)}%')
        feat_split = cluster_feat._make(
            [f.splitlines() for f in re.split(r'Feature \d\n', feat_str)][1:])

        Rp_df, Jp_df = [collect_feat_ranks(clust_id, f) for f in feat_split]
        Rp_frames.append(Rp_df)
        Jp_frames.append(Jp_df)
        R_lemmas = R_lemmas.union(Rp_df.index)
        J_lemmas = J_lemmas.union(Jp_df.index)

    print('\n## Overall Probability of Each Cluster\n')
    overall_table = (overall_p * 100).round(2).to_frame('Probability (%)')
    overall_table.index.name = 'Cluster'
    print(overall_table.to_markdown(floatfmt='.2f'))

    n = 15
    print(f'\n## Adverb Specific Probabilities across {n_clust} clusters\n')
    R_cluster_p = join_cluster_frames(Rp_frames, R_lemmas, overall_p, n)
    df_out_path = mod_bin_path.with_name(
        f'{mod_bin_path.name}_{view_size}-ADV.csv')
    print(f'\nTable saved as `../LSC/{df_out_path.relative_to(_LSC_DIR)}`')
    R_cluster_p.to_csv(df_out_path, float_format="%.4f")

    print(f'\n## Adjective Specific Probabilities across {n_clust} clusters\n')
    J_cluster_p = join_cluster_frames(Jp_frames, J_lemmas, overall_p, n)
    df_out_path = df_out_path.with_stem(df_out_path.stem.replace('ADV', 'ADJ'))
    print(f'\nTable saved as `../LSC/{df_out_path.relative_to(_LSC_DIR)}`')
    J_cluster_p.to_csv(df_out_path, float_format="%.4f")


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('script to parse binary LSC model into '
                     '(1) original `lsc-print` text and '
                     '(2) csv tables for each feature (e.g. adv & adj) '
                     'compiled across all clusters'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-m', '--model_path',
                        type=str, default=None,
                        help=('path to (binary) model. If not absolute, relative '
                              'to `../source/LSC/` (parent dir for this script) is assumed. '
                              '*Binary model file should not have extension `.txt`*')
                        )

    parser.add_argument('-f', '--frequency_path',
                        type=Path, default='all-frq_thresh25.3f.csv',
                        help=('path to frequency dataframe. If not absolute, relative '
                              'to `../results/freq_out/` is assumed. **Note: this will '
                              'only be used if `--model_path` is not given or does not exist.')
                        )

    parser.add_argument('-v', '--view_size',
                        type=int, default=100,
                        help=('# of words to assess per selection feature in each cluster. '
                              '(i.e. # of words to translate from binary to text using '
                              '`lsc-print` with `-n` flag.)')
                        )

    parser.add_argument('-i', '--iterations',
                        type=int, default=10,
                        help=('# of iterations for training lsc model '
                              ' from frequency data (loaded from `--freq_path`) '
                              '**Does nothing if used with `--model_path`!'
                              )
                        )

    parser.add_argument('-k', '--clusters',
                        type=int, default=8,
                        help=('# of clusters for training lsc model '
                              ' from frequency data (loaded from `--freq_path`) '
                              '**Does nothing if used with `--model_path`!'
                              )
                        )

    parser.add_argument('-s', '--filter_stat',
                        type=str, default='var_coeff',
                        help=('name of column in descriptive statistics tables '
                              'with which to filter lemmas in model text. '
                              'Example .csv files can be found in `{}`'.format(
                                  _FREQ_OUT_DIR.joinpath('descriptive_stats')))
                        )
    args = parser.parse_args()

    model_path = args.model_path
    if model_path:
        model_path = Path(model_path)
        if not model_path.is_absolute():
            _LSC_DIR.joinpath(model_path)

    frq_path = Path(args.frequency_path)
    if not frq_path.is_absolute():
        frq_path = _FREQ_OUT_DIR.joinpath(frq_path)

    return (model_path, args.view_size, 
            frq_path, args.clusters, args.iterations, 
            args.filter_stat)


def verify_path_arg(parg, default, rel_dir):
    if parg:
        model_path = Path(parg)
        if not model_path.is_absolute():
            model_path = rel_dir.joinpath(model_path)
    else:
        model_path = rel_dir.joinpath(default)
    return model_path


def train_model(frq_path, k, i):
    print('## Training lsc model')
    print('- path to input frequency table:',
          f'`{str(frq_path.relative_to(_FREQ_OUT_DIR.parent))}`')
    frq_df = pd.read_csv(frq_path).convert_dtypes()
    training_input = _LSC_DIR.joinpath(
        f"data/{frq_path.name.replace('.csv', '.tsv')}")
    if not training_input.is_file():
        print('- formatting frequency table for model training...')
        t0 = pd.Timestamp.now()
        save_lsc(frq_df, training_input)
        t1 = pd.Timestamp.now()
        print('> Time to format data to train model:',
              f'`{get_proc_time(t0, t1)}`')

    mod_dir = _LSC_DIR.joinpath("models")
    if not mod_dir.is_dir():
        mod_dir.mkdir()
    mod_name = f"{training_input.name.replace('.tsv', '')}_m-{k}k-{i}i"
    mod_bin_path = mod_dir.joinpath(mod_name)
    print('- binary model path:',
          f'`{str(mod_bin_path.relative_to(_LSC_DIR))}`')
    if mod_bin_path.is_file():
        print('  - Existing model found!')
    else:
        print(f'\ntraining model with {k} clusters and {i} iterations...')
        train = _LSC_DIR.joinpath("src/lsc-train")
        # from shell script: src/lsc-train ${N_CLUST} ${N_ITERS} ${DATA} >${MOD_NAME}
        train_cmd = f'{train} {k} {i} {training_input} > {mod_bin_path}'
        print(f'\n```\n{train_cmd}\n')
        t0 = pd.Timestamp.now()
        system(train_cmd)
        t1 = pd.Timestamp.now()
        print(f'```\n> Time to train model: `{get_proc_time(t0, t1)}`')
    return mod_bin_path


def textify_model(mod_bin_path, view_size):
    print('\n## Parsing LSC Model for Viewing\n')
    mod_txt_path = mod_bin_path.parent.joinpath(
        f'text_view/{mod_bin_path.stem}_top{view_size}.txt')
    if not mod_txt_path.parent.is_dir():
        mod_txt_path.parent.mkdir()
    lsc_print_cmd = f"{_LSC_DIR.joinpath('src/lsc-print')} -n {view_size}"
    print(f'+ Parsing binary `../LSC/{mod_bin_path.relative_to(_LSC_DIR)}`\\',
          f'   into text `../LSC/{mod_txt_path.relative_to(_LSC_DIR)}`',
          sep='\n')
    cmd = f'{lsc_print_cmd} {mod_bin_path} > {mod_txt_path}'
    system(cmd)
    return mod_txt_path


def collect_feat_ranks(clust_id: str, feat_info) -> pd.DataFrame:
    lemmas_df = pd.DataFrame([
        word._make(w.strip().split('\t')) for w in feat_info
    ]).set_index('lemma')
    lemmas_df.columns = [clust_id]
    return lemmas_df


def join_cluster_frames(frames: list,
                        lemmas: list,
                        overall_p: pd.Series,
                        n: int = 20) -> pd.DataFrame:
    row_labels = ['CLUSTER']
    print(len(set(lemmas)), 'unique lemmas')
    row_labels.extend(set(lemmas))
    composite = pd.DataFrame(index=row_labels, columns=overall_p.index)

    for df in frames:
        composite.update(df)
    composite.loc[row_labels[0], :] = overall_p
    composite = composite.apply(pd.to_numeric, downcast='float')
    composite = composite.assign(lemma_total=pd.to_numeric(composite.sum(axis=1),
                                                           downcast='float'))
    print('\n### Descriptive Stats for Clusters\n')
    lemmas_only = composite.loc[row_labels[1:], :]
    print(lemmas_only.describe().T
          .assign(all_lemmas_summed=lemmas_only.sum())
          .round(4).to_markdown())

    composite = (composite
                 .sort_values('lemma_total', ascending=False)
                 .sort_values('CLUSTER', axis=1, ascending=False)
                 .round(4))

    print(f'\n### {n} Lemmas with Highest Cumulative Probability\n')
    print(composite.head(n).to_markdown(floatfmt='.4f'))
    return composite


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    _main()
    proc_t1 = pd.Timestamp.now()
    print(f'   total time elapsed: {get_proc_time(proc_t0, proc_t1)}')
