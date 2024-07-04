# coding=utf-8
import argparse
# import itertools as itt
import re
from pathlib import Path

import pandas as pd

from source.utils.dataframes import Timer
from source.utils.dataframes import filter_csv_by_index as filter_csv
from source.utils.general import HIT_TABLES_DIR
from source.utils.general import run_shell_command as shell_cmd

CLEAN_RBX_DIR = HIT_TABLES_DIR / 'RBXadj' / 'pre-cleaned'
SUPER_NEG = HIT_TABLES_DIR / 'RBdirect'
COM_HIT_DIR = HIT_TABLES_DIR / 'not-RBdirect'


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '-p', '--corpus_part', default=None,
        type=str, help=('corpus part tag to select both `--csv_path` and `--index_path`.'
                        '(index will default to `alpha` version.)'))

    parser.add_argument(
        '-c', '--csv_path',
        type=Path,
        # default=CLEAN_RBX_DIR / 'clean_bigram-PccVa_rb-bigram_hits.csv',
        # 2_hit_tables/RBdirect/bigram-PccTe_direct-adj-head_hits.csv.bz2
        default=SUPER_NEG / 'bigram-PccVa_direct-adj-head_hits.csv.bz2',
        help=('path to dataframe saved as csv')
    )

    parser.add_argument(
        '-x', '--index_path',
        type=Path,
        # default=HIT_TABLES_DIR / 'not-RBdirect' / 'clean_bigram-PccVa_not-RBdirect_index.txt',
        default=SUPER_NEG / 'pre-cleaned' / \
        'PccVa_trigger_bigram-index_alpha-REclean.35f.txt',
        help=('path to text file containing `bigram_id` filter; id strings only separated by new lines')
    )

    rgs = parser.parse_args()
    # if all([p.is_file() for __,p in rgs._get_kwargs()]):
    for a, p in rgs._get_kwargs():
        if isinstance(p, Path):
            if not p.is_file():
                raise FileNotFoundError(
                    f"\n* Invalid '--{a}' value\n  > '{p}' not found.")

    return rgs


def _main():
    args = _parse_args()
    if args.corpus_part is not None: 
        part = args.corpus_part
        neg_top = HIT_TABLES_DIR / 'RBdirect'
        neg_preclean = neg_top / 'pre-cleaned'
        # neg_condensed = neg_top / 'condensed'
        # pkl_path = neg_condensed.glob(f'*{part}*_hits.pkl.gz')
        index_path = neg_preclean.joinpath(
            f'{part}_trigger_bigram-index_alpha-REclean.35f.txt')
        csv_paths = list(neg_preclean.glob(f'*{part}*REclean_hits.csv.bz2'))
        if not any(csv_paths): 
            csv_paths = list(neg_top.glob(f'*{part}*hits.csv.bz2'))
            if not any(csv_paths): 
                csv_paths = list(neg_top.glob(f'*{part}*hits.csv'))
            # columns in original hit tables: 
                # hit_id, colloc, sent_text, #! obsolete---"colloc" -> "bigram_lower"
                # neg_form, #> "neg" -> "mir" for POSmirror
                # adv_form, adj_form, 
                # hit_text, text_window, 
                # sent_id, match_id, colloc_id, #! obsolete--"colloc_id" -> "bigram_id"
                # token_str, lemma_str, 
                # neg_deprel, neg_head, #> "neg" -> "mir" for POSmirror
                # mod_deprel, mod_head, 
                # neg_lemma, #> "neg" -> "mir" for POSmirror
                # adv_lemma, adj_lemma, 
                # neg_index, #> "neg" -> "mir" for POSmirror
                # adv_index, adj_index, 
                # neg_all_dep_target, #> "neg" -> "mir" for POSmirror
                # adv_all_dep_target, adj_all_dep_target, 
                # dep_neg, #> "neg" -> "mir" for POSmirror
                # dep_mod, 
                # json_source, utt_len, pattern, category
            
        else: 
            # columns in `REclean`ed hit tables: 
                # hit_id, bigram, sent_text, #^ "bigram" was "colloc"
                # neg_form, #> "neg" -> "mir" for POSmirror
                # adv_form, adj_form,
                # hit_text, text_window, 
                # sent_id, match_id, bigram_id, #^ "bigram_id" was "colloc_id"
                # token_str, lemma_str, 
                # neg_deprel, neg_head, #> "neg" -> "mir" for POSmirror
                # mod_deprel, mod_head, 
                # neg_lemma, #> "neg" -> "mir" for POSmirror
                # adv_lemma, adj_lemma,
                # neg_index, #> "neg" -> "mir" for POSmirror
                # adv_index, adj_index, 
                # neg_all_dep_target, #> "neg" -> "mir" for POSmirror
                # adv_all_dep_target, adj_all_dep_target,
                # dep_neg, #> "neg" -> "mir" for POSmirror
                # dep_mod, 
                # json_source, utt_len, pattern, category
                # ! missing: "part", "slice", "ad*_form_lower", "bigram_lower"
            pass
        for csv_path in csv_paths: 
            prep_csv(part, index_path, csv_path)
    else: 
        index_path = args.index_path
        csv_path = args.csv_path
        part = re.search(r'[ANP][pwytc]{2}[VaTe\d]*', index_path.stem).group()
        prep_csv(part, index_path, csv_path)

def prep_csv(part:str, 
             index_path:Path, 
             csv_path:Path, 
             dtype_dict:dict=None):
    pattern = csv_path.name.split(f'{part}_')[1].split('_hits')[0]
    print(f'\n# Filtering "{pattern}" hits in "{part}"\n\n'
          f'- original csv: `{csv_path}`\n'
          f'- filtering index: `{index_path}`')
    if str(index_path.parent)==str(neg_preclean):
        output_csv_path = index_path.parent / (
            f'{part}_{pattern}'
            + re.search(r'(?<=index)[\w-]+(?=\.)',
                        index_path.stem).group()
            + '_hits.csv.bz2')
    else:
        output_csv_path = Path(
            str(index_path).replace('_index.txt', '_hits.csv.bz2'))
    print(f'- updated file: {output_csv_path}\n\n*********************')

    if output_csv_path.is_file():
        print(f'✓ Corpus part {part} previously processed:\n  '
              f'{output_csv_path.relative_to(HIT_TABLES_DIR)} already exists.')
        shell_cmd(
            f'tree -hD {output_csv_path.parent} | grep "{part}" && wc -l {output_csv_path.parent}/*{part}*[tv]')
    else:
        # columns in `pre-cleaned/*csv`
        #   hit_id,adv_form,adj_form,text_window,token_str,adv_lemma,adj_lemma,adv_index,adv_form_lower,adj_form_lower,bigram_lower,utt_len
        #! convert strings to category _after_ manipulations
        dtype_dict = {h: ('int64' if h.endswith(('index', 'len')) else 'string')
                      #! strip ".bz2" to get first line only
                      for h in (Path(str(csv_path).strip('.bz2'))
                                .read_text(encoding='utf8')
                                .splitlines()[0].split(','))
                      }

        df = filter_csv(index_txt_path=index_path,
                        df_csv_path=csv_path,
                        dtype_dict=dtype_dict,
                        outpath=output_csv_path)

        if df:
            print(
                f'+ {len(df):,} total {index_path.parent.name} hits in {part}')
            with Timer() as _t:
                df.to_csv(output_csv_path)
                print(
                    f'+ saved as {output_csv_path}'
                    f'  + time to write new csv: {_t.elapsed()}',
                    sep='\n')

if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print('\n✓ Program Completed @ ', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
