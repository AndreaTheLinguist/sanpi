import argparse
import re
# from os import system
from pathlib import Path
from sys import exit as sysxit

from utils.dataframes import Timer
from utils.general import confirm_dir, print_iter
from utils.associate import prep_by_polarity, build_ucs_from_multiple

WORD_GAP = re.compile(r"(\b[a-z'-]+)\t([^_\s\t]+\b)")
_RSLT_DIR = Path('/share/compling/projects/sanpi/results')
_FREQ_DIR = _RSLT_DIR / 'freq_out'
_POL_DIR = _RSLT_DIR / 'ucs_tables' / 'polarity_prepped'
confirm_dir(_POL_DIR)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('Simple script to prepare token counts from data subsets representing '
                     '"positive" and "negative" polarity environements for contingency table '
                     '& association measure calculation via the `UCS` toolkit '
                     '(http://www.collocations.de/software.html).'
                     'It converts each (separate) ucs-formatted .tsv input file into a '
                     'new .tsv (saved in `../results/ucs_tables/polarity_prepped/`) '
                     'that is ready to be piped to the `ucs-make-tables --types` command. '
                     '"ucs-formatted" means that the count for each (attested) `L1 L2` combination '
                     'is encoded as tab-delimited values: `#tokens<tab>L1<tab>L2`. '
                     'Each line is altered by inserting the corresponding polarity '
                     'label as `L1` (first word of "bigram") position, and the former L1 and L2 are '
                     'joined with an underscore "_" and take the updated L2 position. For example: '
                     'the input line from the negated counts tsv, `14526	even    sure` '
                     'is transformed into `14526	NEGATED	even_sure`.'
                     '**After running this script successfully, run `` to create the composite polarity-bigram table'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-c', '--complement_counts',
        type=Path,
        default=(_FREQ_DIR / 'diff_RBXadj-RBdirect' / 'ucs_format' /
                 'diff-all_adj-x-adv_frq-thr0-001p.35f=868+.tsv'),
        help=('Path to ucs-formatted .tsv of COMPLEMENT bigram frequencies; i.e. '
              'counts for bigram tokens with no *identified* negation dependencies. '
              '(An approximation of bigrams occurring in "positive polarity" environments.) '
              'The transformed frequency data will be saved as `polarity_prepped/complement_bigram_counts.tsv')
    )

    parser.add_argument(
        '-C', '--comp_label',
        type=str, default='complement',
        help=('option so set the label for complement (set difference, not negated, "positive", etc.) counts. Used for output path generation.')
    )

    parser.add_argument(
        '-n', '--negated_counts',
        type=Path,
        default=(_FREQ_DIR / 'RBdirect' / 'ucs_format' /
                 'ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv'),
        help=('Path to ucs-formatted .tsv of NEGATED bigram frequencies; i.e. '
              'counts for bigram tokens with *identified* negation dependencies. '
              '(An approximation of bigrams occurring in "negative polarity" environments.)'
              'The transformed frequency data will be saved as `polarity_prepped/negated_bigram_counts.tsv')
    )

    parser.add_argument(
        '-N', '--neg_label',
        type=str, default='negated',
        help=('option so set the label for negated (or matching specific pattern) counts. Used for output path generation.')
    )

    parser.add_argument(
        '-R', '--run',
        action='store_true',
        help=('Option to immediately run the required UCS command to convert the newly reconfigured tables into a ucs contingency table. '
              'Output will be saved as `results/usc_tables/polarized-bigrams_min[MIN_COUNT]x.ds.gz')
    )

    parser.add_argument(
        '-m', '--min_count',
        type=int, default='3',
        help=('If `-r/--run` flag is given, this argument dictates the value of the `ucs-make-tables --threshold` paramenter; '
              'i.e., only lines with a count of this value or higher will be included as lines in the resultant table '
              '(but all counts will still be accounted for in marginal frequencies and expected frequency calculations). '
              'E.g. The default value of 3 will yield a table where the minimum observed frequency for any row is 3. '
              'All rows with only 1 or 2 tokens will count toward the totals, but will not appear as distinct rows.')
    )

    parser.add_argument(
        '-r', '--row_limit',
        type=int, default=None,
        help=('Option to limit the input rows from each original .tsv file; '
              'Will yield 2 tsv files with maximum of L rows/lines')
    )

    parser.add_argument(
        '-w', '--word_filter',
        type=str, default='bigram',
        help=('Option to reduce `l2` column to only 1 word of the bigram.'
              '"adv" will keep the input `l1` column only (i.e. the adverbs). '
              '"adj" will keep the input `l2` column only (i.e. the adjective). '
              'Both are kept and joined by an underscore `_` by default.')
    )

    return parser.parse_args()


def _main():
    args = _parse_args()
    in_paths_dict = {
        args.comp_label: args.complement_counts,
        args.neg_label: args.negated_counts
    }
    prepped_dict = prep_by_polarity(
        in_paths_dict, args.row_limit, args.word_filter)
    if args.run:
        out_path = build_ucs_from_multiple(prepped_dict, args.min_count, args.word_filter)


# def prep_by_polarity(in_paths_dict: dict,
#                      row_limit: int = None,
#                      words_to_keep: str = 'bigram'):
#     confirm_existing_tsv(in_paths_dict)
#     input_data_suff = _get_input_suff(in_paths_dict)
#     # input_data_suffix_strs = [''.join(p.suffixes) for p in in_paths_dict.values()]
#     # input_data_flag = {suff:len(suff) for suff in input_data_suffix_strs if }
#     print('---')
#     polar_dict = {counts_label: prep_lines(tsv_path=counts_tsv,
#                                            polarity=counts_label,
#                                            row_limit=row_limit,
#                                            data_suff=input_data_suff,
#                                            words_to_keep=words_to_keep)
#                   for counts_label, counts_tsv in in_paths_dict.items()}
#     # print('Polarity prepped counts saved as:')
#     # print(f'\n'.join((f'+ {n.capitalize(): >10} -> '
#     #                   + str(Path(*p.parts[-3:])) for n, p in polar_dict.items())))
#     print_iter((f'{n.capitalize(): >10} -> '
#                 + str(Path(*p.parts[-3:])) for n, p in polar_dict.items()),
#                bullet='+',
#                header='Polarity prepped counts saved as:')
#     return polar_dict


# def _get_input_suff(in_paths_dict):
#     suffix = '.tsv'
#     for p in in_paths_dict.values():
#         in_suff = re.findall(r'\.\d+f=\d+\+\.tsv', p.name)
#         if any(in_suff):
#             suffix = in_suff[0]
#             break
#     return suffix


# def confirm_existing_tsv(tsv_obj):
#     try:
#         file_exists = tsv_obj.is_file()
#     except AttributeError:
#         for tsv in tsv_obj.values():
#             if not Path(tsv).is_file():
#                 sysxit(f'Input data {tsv} not found!')
#     else:
#         if not file_exists:
#             sysxit(f'Input data {tsv} not found!')


# def prep_lines(tsv_path: Path,
#                polarity: str,
#                row_limit: int = None,
#                data_suff: str = '',
#                words_to_keep: str = 'bigram'):
#     # // confirm_existing_tsv(tsv_path)
#     # 👆 not needed because run on entire dict before this is applied
#     prep_path = _POL_DIR / \
#         f'{polarity.lower()}_{words_to_keep}_counts{data_suff}'
#     print(
#         f'\nProcessing {polarity} counts loaded from {tsv_path.relative_to(_RSLT_DIR)}...')
#     if not prep_path.is_file():
#         prep_path.write_text('\n'.join(new_line_gen(
#             tsv_path, polarity, row_limit, words_to_keep)) + '\n')
#     else:
#         print(
#             f'+ [{prep_path.relative_to(_RSLT_DIR)} already exists -- not overwritten]')
#     print('+ ✓ done')
#     return prep_path


# def new_line_gen(tsv_path: Path, polarity: str, row_limit: int = None, words_to_keep: str = 'bigram'):
#     sub_keep_str = polarity.upper()
#     if words_to_keep == 'bigram':
#         sub_keep_str += r'\t\1_\2'
#     elif words_to_keep == 'adv':
#         sub_keep_str += r'\t\1'
#     elif words_to_keep == 'adj':
#         sub_keep_str += r'\t\2'

#     for line in read_rows(tsv_path, row_limit):
#         yield WORD_GAP.sub(sub_keep_str, line)


# def read_rows(tsv_path: Path, row_limit: int = 0):
#     return (tsv_path.read_text().splitlines()[:row_limit]
#             if row_limit
#             else tsv_path.read_text().splitlines())


# def _build_polar_ucs(polar_dict, min_count, count_type='bigram'):
#     cat_count_tsv_cmd = f'(cat {polar_dict["complement"]} && cat {polar_dict["negated"]})'
#     ucs_save_path = f'{_POL_DIR.parent}/polarized-{count_type}_min{min_count}x.ds.gz'
#     build_ucs_table(min_count, ucs_save_path, cat_count_tsv_cmd)


if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print(f'\nScript Complete.\n> total time elapsed: {timer.elapsed()}')
