# coding=utf-8
import re
import pandas as pd

from collections import namedtuple as ntp
from os import system
from pathlib import Path

import argparse

cluster = ntp('Cluster', ['index', 'probability', 'features'])
cluster_feat = ntp('Features', ['R', 'J'])
word = ntp('Word', ['lemma', 'prob'])

_LSC_DIR = Path('/share/compling/projects/sanpi/source/LSC')


def _main():
    mod_bin_path, view_size = _parse_args()
    print('# Parsing LSC Model for Viewing\n')
    mod_txt_path = mod_bin_path.parent.joinpath(f'text_view/{mod_bin_path.stem}_top{view_size}.txt')
    if not mod_txt_path.parent.is_dir(): 
        mod_txt_path.parent.mkdir()
    lsc_print_cmd = f"{_LSC_DIR.joinpath('src/lsc-print')} -n {view_size}"
    print(f'1. Parsing binary `../LSC/{mod_bin_path.relative_to(_LSC_DIR)}`\\',
          f'   into text `../LSC/{mod_txt_path.relative_to(_LSC_DIR)}`', 
          sep='\n')
    cmd = f'{lsc_print_cmd} {mod_bin_path} > {mod_txt_path}'
    system(cmd)

    text = mod_txt_path.read_text(encoding='utf8')
    sections = re.split(r'\n-{4,}\n', text)
    preamble = sections.pop(0)
    n_clust, n_feat = [int(n) for n in re.findall(r'\d+', preamble.strip())]
    feat_quant = 'both' if n_feat == 2 else f'all {n_feat}'
    print(f'2. Converting top {view_size} lemmas into `lemma × probability for cluster` table for {feat_quant} selectional features in all {n_clust} clusters.')

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
    overall_table.index.name= 'Cluster'
    print(overall_table.to_markdown(floatfmt='.2f'))
    n = 15
    print(f'\n## Adverb Specific Probabilities across {n_clust} clusters\n')
    R_cluster_p = join_cluster_frames(Rp_frames, R_lemmas, overall_p, n)
    df_out_path = mod_bin_path.with_name(f'{mod_bin_path.name}_{view_size}-ADV.csv')
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

    parser.add_argument(
        '-m', '--model', type=str, default=None,
        help=('path to (binary) model. If not absolute, relative '
              'to `../source/LSC/` (parent dir for this script) is assumed. '
              '*Binary model file should not have extension `.txt`*')
        )
    
    parser.add_argument(
        '-v', '--view_size',
        type=int, default=100,
        help=('# of words to assess per selection feature in each cluster. '
              '(i.e. # of words to translate from binary to text using '
              '`lsc-print` with `-n` flag.)')
    )
    args = parser.parse_args()
    
    if args.model: 

        model_path = Path(args.model)
        if not model_path.is_absolute():
            model_path = _LSC_DIR.joinpath(model_path)    
    else: 
        model_path = _LSC_DIR.joinpath('models/all-frq_thresh5.15f_LIMIT200_ADV-mn-std_m-10-24')
    # 'models/all-frq_thresh5.15f_LIMIT200_ADJ-mn-std_m-10-30')

    return model_path, args.view_size


def collect_feat_ranks(clust_id:str, feat_info) -> pd.DataFrame:
    lemmas_df = pd.DataFrame([
        word._make(w.strip().split('\t')) for w in feat_info
    ]).set_index('lemma')
    lemmas_df.columns = [clust_id]
    return lemmas_df


def join_cluster_frames(frames: list, 
                        lemmas: list, 
                        overall_p: pd.Series, 
                        n:int = 20) -> pd.DataFrame:
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
    _main()


