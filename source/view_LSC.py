# coding=utf-8
import argparse
import re

from collections import namedtuple as nametup
from os import system
from pathlib import Path
from sys import exit as syxit

import pandas as pd
from utils import (  # pylint: disable=import-error
    confirm_dir,
    get_proc_time,
    print_md_table,
    save_in_lsc_format as save_lsc
)
# // from utils import (
# //     save_in_lsc_format as save_lsc
# //                    )  # pylint: disable=import-error

# frequency tuple
freq_meta = nametup(
    'FrequencyMetaInfo',
    ['freq_table', 'lsc_reformat', 'hit_thresh', 'corp_coverage',
     'freq_type', 'freq_status', 'model_path', 'clusters', 'iterations'],
    defaults=[None, None, 0, 0, 'raw', 'cleaned+filtered', None, 0, 0])

# lsc tuples
cluster = nametup('Cluster', ['index', 'probability', 'features'])
cluster_feat = nametup('Features', ['R', 'J'])
word = nametup('Word', ['lemma', 'prob'])

# Paths
_SANPI_DIR = Path('/share/compling/projects/sanpi')
_LSC_DIR = _SANPI_DIR.joinpath('source/LSC')
_FREQ_OUT_DIR = _SANPI_DIR.joinpath('results/freq_out')
_MD_LOG = _LSC_DIR.joinpath('logs')
confirm_dir(_MD_LOG)


def _main():
    # // mod_bin_path, view_size, frq_path, k, i, metric_name = _parse_args()
    args = _parse_args()

    mod_bin_path, frq_path = assess_paths(args)
    view_size = args.view_size
    metric_name = args.filter_stat

    freq_info = acquire_model(mod_bin_path, frq_path, args)
    mod_bin_path = freq_info.model_path
    mod_txt_path = textify_model(mod_bin_path, view_size)

    # * load text model & apply stats filter
    model_text = filter_model_text(
        freq_info, metric_name, mod_txt_path)
    # * parse text model info into table(s)
    if not bool(model_text):
        model_text = mod_txt_path.read_text(encoding='utf8')
    sections = re.split(r'\n-{4,}\n', model_text)
    parse_model(mod_bin_path, view_size, sections)


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
    # // args = parser.parse_args()
    # //
    # // model_path = args.model_path
    # // if model_path:
    # //     model_path = Path(model_path)
    # //     if not model_path.is_absolute():
    # //         _LSC_DIR.joinpath(model_path)
    # //
    # // frq_path = Path(args.frequency_path)
    # // if not frq_path.is_absolute():
    # //     frq_path = _FREQ_OUT_DIR.joinpath(frq_path)
    # //
    # // return (model_path, args.view_size,
    # //         frq_path, args.clusters, args.iterations,
    # //         args.filter_stat)
    return parser.parse_args()


def assess_paths(args):
    mod_bin_path = args.model_path
    if mod_bin_path:
        mod_bin_path = Path(mod_bin_path)
        if not mod_bin_path.is_absolute():
            _LSC_DIR.joinpath(mod_bin_path)

    frq_path = Path(args.frequency_path)
    if not frq_path.is_absolute():
        frq_path = _FREQ_OUT_DIR.joinpath(frq_path)
    return mod_bin_path, frq_path


def acquire_model(mod_bin_path: Path, frq_path: Path, args) -> Path:

    if not mod_bin_path:
        frq_info = collect_meta_info(frq_path=frq_path,
                                     model_k=args.clusters,
                                     model_i=args.iterations)
        if frq_path.exists():
            if frq_path.suffix == '.csv':
                train_model(frq_info)
            else:
                syxit('Error: anticipated `.csv` file for frequency table input.\n'
                      + f'       × received: `{frq_path.name}`')
        else:
            syxit('Error: No valid frequency data or binary model specified. Exiting.')
    else:
        frq_info = collect_meta_info(mod_path=mod_bin_path,
                                     model_k=args.clusters,
                                     model_i=args.iterations)

    return frq_info


def collect_meta_info(frq_path: Path = None,
                      mod_path: Path = None,
                      model_k: int = 10,
                      model_i: int = 10) -> tuple:
    lsc_data_dir = _LSC_DIR.joinpath("data")
    if frq_path:
        frq_stem = frq_path.stem
        old_lsc_reformat = lsc_data_dir.joinpath(f"{frq_stem}.tsv")

        n_tok, n_files = [int(''.join(m))
                          for m in re.findall(r'thresh(\d+)|(\d+)f', frq_stem)]
        frq_info = freq_meta(freq_table=frq_path,
                             hit_thresh=n_tok,
                             corp_coverage=n_files,
                             clusters=model_k,
                             iterations=model_i)

        if frq_path.parent != _FREQ_OUT_DIR:
            frq_type = '_'.join(re.findall(
                r'log\d+|sqrt[^_]*|AD[\w-]+', frq_stem))
            frq_info = frq_info._replace(freq_type=frq_type,
                                         freq_status=frq_path.parent.name)

        selection_flag = 'JxR' if frq_stem.count('JxR') else 'all'
        frq_info = frq_info._replace(
            lsc_reformat=old_lsc_reformat.with_name(
                f"{frq_info.freq_type.upper()}_{selection_flag}-thresh{frq_info.hit_thresh}"
                + f"-{frq_info.corp_coverage}f.csv")
        )

        mod_dir = _LSC_DIR.joinpath("models")
        confirm_dir(mod_dir)
        frq_info = frq_info._replace(
            model_path=mod_dir.joinpath(
                f"{frq_info.lsc_reformat.stem}_m-{model_k}k-{model_i}i"))

        # if old_lsc_reformat.is_file():
        #     system(f'mv {str(old_lsc_reformat)} {str(frq_info.lsc_dir)}')

    elif mod_path:

        results_path = _FREQ_OUT_DIR.parent
        mod_stem = mod_path.stem
        frq_type, selection_flag, n_tok, n_files, model_i, model_k = re.findall(
            r'^([A-Z-]*)_(all|JxR).*thresh(\d+).(\d+)f_m-(\d+)k-(\d+)i', mod_stem)[0]
        lsc_reformat_stem = mod_stem.split('_m')[0]
        lsc_reformat = lsc_data_dir.joinpath(f'{lsc_reformat_stem}.tsv')
        frq_info = freq_meta(lsc_reformat=lsc_reformat,
                             hit_thresh=n_tok,
                             corp_coverage=n_files,
                             model_path=mod_path,
                             clusters=model_k,
                             iterations=model_i)
        frq_parent_list = None
        if frq_type.startswith('AD'):
            frq_type = frq_type[:3]+frq_type[3:].lower()
            frq_parent_list = list(results_path.glob('*stand*'))
        elif frq_type.startswith(('SQRT', 'LOG')):
            frq_type = frq_type.lower()
            frq_parent_list = results_path.glob('*trans*')
        else:
            frq_parent = _FREQ_OUT_DIR

        if frq_parent_list:
            frq_parent = frq_parent_list[0]
            frq_info = frq_info._replace(freq_type=frq_type,
                                         freq_status=frq_parent.name)

        frq_glob_list = list(frq_parent.glob(
            f'*{selection_flag}*thr*{n_tok}*{n_files}*'))
        if frq_glob_list:
            frq_path = frq_glob_list[0]
            frq_info = frq_info._replace(freq_table=frq_path)

    print_md_table(
        title='\n',
        indent=2,
        df=pd.DataFrame(frq_info,
                        columns=['Meta Info'],
                        index=freq_meta._fields))

    return frq_info


def train_model(frq_info: tuple,
                # frq_path: Path,
                # model_k: int,
                # model_i: int,
                # TODO: add code to transform/standardize on the fly
                transform: str = '',
                standard: str = ''
                ):

    print('\n## Training lsc model')

    if frq_info.model_path.is_file():
        print('- Existing model found!')
    else:
        if not frq_info.lsc_reformat.is_file():
            print(f'- loading frequency table:',
                  f'\n  - `../{str(frq_info.freq_table.relative_to(_SANPI_DIR))}`'
                  )
            t0 = pd.Timestamp.now()
            frq_df = pd.read_csv(frq_info.freq_table).convert_dtypes()
            t1 = pd.Timestamp.now()
            print('    > Time to load frequency data:',
                  f'`{get_proc_time(t0, t1)}`')

            print('- reformatting frequency table for model training...\n\n```')
            t0 = pd.Timestamp.now()
            save_lsc(frq_df, frq_info.lsc_reformat,
                     numeric_label=frq_info.freq_type)
            t1 = pd.Timestamp.now()
            print('```\n\n> Time to reformat frequency data:',
                  f'`{get_proc_time(t0, t1)}`\n')
        model_k = frq_info.clusters
        model_i = frq_info.iterations
        print(
            f'- training model with {model_k} clusters and {model_i} iterations...')
        train = _LSC_DIR.joinpath("src/lsc-train")
        # from shell script: src/lsc-train ${N_CLUST} ${N_ITERS} ${DATA} >${MOD_NAME}
        train_cmd = f'{train} {model_k} {model_i} {frq_info.lsc_reformat} > {frq_info.model_path}'
        print(f'\n```\n{train_cmd}\n')
        t0 = pd.Timestamp.now()
        system(train_cmd)
        t1 = pd.Timestamp.now()
        print(f'```\n- > Time to train model: `{get_proc_time(t0, t1)}`')


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


def filter_model_text(frq_info, metric_name, mod_txt_path):
    frq_path = frq_info.freq_table
    mod_bin_path = frq_info.model_path
    # > find stats csv files (2 = 1 for adv, 1 for adj)
    stats_paths = seek_stats(frq_info)
    model_text = mod_txt_path.read_text(encoding='utf8')
    if model_text.count('-nan') > 1:
        syxit('Error: Training Failed. Model is empty.')
    keep_lemmas = []
    if bool(stats_paths):

        # > load stats and isolate stats metric to filter on
        #   metric_name = name of column in stats csv = e.g. 'var_coeff'
        for path in stats_paths:
            #! there should be only 2 paths for fully informative keys
            p_lower = path.name.lower()
            if 'adj' in p_lower:
                adj_metric = load_stat(
                    metric_name, path, lemma_col='adj_lemma')
            elif 'adv' in p_lower:
                adv_metric = load_stat(
                    metric_name, path, lemma_col='adv_lemma')
                # adv_metric = pd.read_csv(path, usecols=['adv_lemma', metric_name]).convert_dtypes().set_index('adv_lemma').sort_values(metric_name).squeeze()
        for series in (adj_metric, adv_metric):
            keep_lemmas.extend(filter_lemmas(series))
    else:
        frq_df = pd.read_csv(frq_info.freq_table)
        frq_df.columns.name = 'adv_lemma'
        if 'adj_lemma' in frq_df.columns:
            frq_df = frq_df.set_index('adj_lemma')

        # adv_metric = frq_df.std() / frq_df.mean()
        # adj_metric = frq_df.std(axis=1) / frq_df.T.mean(axis=1)
        for ax in [0, 1]:
            cv = frq_df.std(axis=ax) / frq_df.mean(axis=ax)
            cv.name = 'var_coeff'
            keep_lemmas.extend(filter_lemmas(cv))

    # > filter text output
    filter_mod_txt_path = mod_txt_path.with_stem(
        mod_txt_path.stem + f'_{metric_name.replace("_","-")}-filter')
    keep_strings = tuple(keep_lemmas) + ('---', 'Number', 'Cluster', 'Feature')
    filtered_lines = []
    print('=============================================')
    # print('```{text}')
    for line in model_text.splitlines():
        if line.strip().startswith(keep_strings):
            # print(line)
            filtered_lines.append(line)
    # print('```')
    # print('=============================================')
    filter_mod_txt_path.write_text('\n'.join(filtered_lines))
    print(f'\nModel text filtered by {metric_name} saved',
          f'as {filter_mod_txt_path.relative_to(_SANPI_DIR)} ')

    return model_text


def seek_stats(frq_info) -> tuple:
    frq_path = frq_info.freq_table
    mod_bin_path = frq_info.model_path
    stats_dir = _FREQ_OUT_DIR.joinpath('descriptive_stats')
    stats_path_key = frq_path.stem
    if frq_path and frq_path.is_absolute():
        abs_stats_dir = frq_path.parent.joinpath('descriptive_stats')
        if not abs_stats_dir.is_dir():
            print(f'\nWarning: stats dir `{abs_stats_dir}/` not found.')
            print(f'- default will be used: `{stats_dir}/`')
        else:
            stats_dir = abs_stats_dir

    # TODO: add code to collect stats live if path not found (instead of exiting)
    #   ^ 1. make `count_bigrams._describe_counts()` a utility,
    #   ^   import and create full stats output for future use
    #   > 2. import `enhance_descrip()` and get full table
    #   > ☝️ this may be the best option...
    #   ? 3. just calculate the desired metric
    #   ?    but how to connect argument with required operations? 🤔

    print(f'+ Seeking stats for `{stats_path_key}` data')
    stats_paths = tuple(stats_dir.glob(f'*{stats_path_key}*'))
    if not stats_paths:
        if not frq_info.freq_table.is_file():
            stats_path_key = f'all*thresh{frq_info.hit_thresh}.{frq_info.corp_coverage}f'
            print(f'  - No stats found. Trying again with `{stats_path_key}`')
            stats_paths = tuple(stats_dir.glob(f'*{stats_path_key}*'))

    if len(stats_paths) > 2:
        print('\n+ `¯\_(ツ)_/¯` data key is ambiguous. Too many stats tables found.\n',
              ' Filtering will be based on variation coefficient for frequency table.')
    elif not(stats_paths):
        print('\n+ `¯\_(ツ)_/¯` Existing stats files not found.\n',
              ' Filtering will be based on variation coefficient for frequency table.')
    return stats_paths


def load_stat(metric_name, p, lemma_col):
    return pd.read_csv(p, usecols=[lemma_col, metric_name]).convert_dtypes().set_index(lemma_col).sort_values(metric_name).squeeze()


def filter_lemmas(metric):
    desc = metric.describe()
    Q1 = desc['25%']
    lower_fence = Q1 - 1.5 * (desc['75%'] - Q1)
    print(
        f'+ Dropping all lemmas with `{metric.name}` values under the first quartile: `{round(Q1, 2)}`')
    print_md_table(metric.nlargest(8).to_frame(), title='Top Values', indent=2)
    keep_lemmas = metric.loc[metric > Q1].index.astype(
        'string').dropna().to_list()
    print(f'  + {len(keep_lemmas):,} lemmas retained')
    dropped = metric.to_frame().loc[~metric.index.isin(
        keep_lemmas), :].sort_values(metric.name, ascending=False)
    print_md_table(dropped.head(
        25), title=f'Filtered out {len(dropped):,} total lemmas:', n_dec=2, comma=False, indent=2)
    print_md_table(dropped.iloc[-25:, :], title='...',
                   n_dec=2, comma=False, indent=2)
    return keep_lemmas


def parse_preamble(view_size, sections):
    preamble = sections.pop(0)
    n_clust, n_feat = [int(n) for n in re.findall(r'\d+', preamble.strip())]
    feat_quant = 'both' if n_feat == 2 else f'all {n_feat}'
    print(f'+ Converting top {view_size} lemmas into `lemma ×',
          f'probability for cluster` table for {feat_quant}',
          f'selectional features in all {n_clust} clusters.')

    return n_clust


def parse_model(mod_bin_path, view_size, sections):
    n_clust = parse_preamble(view_size, sections)
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
    meta_dir = mod_bin_path.parent.joinpath('meta')
    confirm_dir(meta_dir)
    print(f'\n## Adverb Specific Probabilities across {n_clust} clusters\n')
    R_cluster_p = join_cluster_frames(Rp_frames, R_lemmas, overall_p, n)
    meta_out_path = meta_dir.joinpath(
        f'{mod_bin_path.name}_{view_size}-ADV.csv')
    print(f'\nTable saved as `../LSC/{meta_out_path.relative_to(_LSC_DIR)}`')
    R_cluster_p.to_csv(meta_out_path, float_format="%.4f")

    print(f'\n## Adjective Specific Probabilities across {n_clust} clusters\n')
    J_cluster_p = join_cluster_frames(Jp_frames, J_lemmas, overall_p, n)
    meta_out_path = meta_out_path.with_stem(
        meta_out_path.stem.replace('ADV', 'ADJ'))
    print(f'\nTable saved as `../LSC/{meta_out_path.relative_to(_LSC_DIR)}`')
    J_cluster_p.to_csv(meta_out_path, float_format="%.4f")


# def verify_path_arg(parg, default, rel_dir):
    # if parg:
    #     model_path = Path(parg)
    #     if not model_path.is_absolute():
    #         model_path = rel_dir.joinpath(model_path)
    # else:
    #     model_path = rel_dir.joinpath(default)
    # return model_path


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
