# %%
import argparse
import re
from os import system
from pathlib import Path

import association_measures.binomial as bn
import association_measures.frequencies as fq
import association_measures.measures as am
import matplotlib.pyplot as plt
import pandas as pd
import utils as ut
from utils.dataframes import get_proc_time, print_md_table
from utils.general import confirm_dir, run_shell_command
from utils.general import convert_ucs_to_csv as txt_to_csv

SANPI_DIR = Path('/share/compling/projects/sanpi')

def _parse_args():

    parser = argparse.ArgumentParser(
        description=('Script to add extra association measures to perl script UCS tables for environement co-occurence frequencies for (1) bigrams, (2) adverbs, and (3) adjectives, each as a separate table', 
                     'If tables have not been previously run, they will be generated, given the minimum frequency parameter. The only pre-requisites are the "negated" and "not negated" (i.e. complement)'
                     'frequency table dataframes'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    
    parser.add_argument(
        '-m','--min_freq',
        type=int, default=15,
        help=('Minimum frequency of co-occurrences included as rows '
              '(everything is still included in the marginal frequencies) in association tables')
        )

    return parser.parse_args()


def get_csv(unit, frq_thresh):
    bare_input = (SANPI_DIR / 'results' / 'ucs_tables' / 'readable' /
                  f'polarized-{unit}_min{frq_thresh}x.rsort-view')
    input_csv = bare_input.with_name(f'{bare_input.name}.csv')
    if input_csv.is_file():
        return input_csv

    input_txt = bare_input.with_name(f'{bare_input.name}.txt')
    if not input_txt.is_file():
        init_ucs = (bare_input.parent.parent /
                    f'polarized-{unit}_min{frq_thresh}x.ds.gz')
        if not init_ucs.is_file():
            initialize = f'python {SANPI_DIR}/script/polarize_tsv_for_ucs.py -w {unit} -m {frq_thresh} -R'
            run_shell_command(initialize)

        transform = f'time bash {SANPI_DIR}/script/transform_ucs.sh \\\n  {init_ucs}'
        run_shell_command(transform)

    txt_to_csv(input_txt)

    return input_csv


# def run_shell_command(command_str):
#     print(command_str + '\n>>>')
#     system(command_str)


def _pull_data(frq_thresh):
    for unit in ('bigram', 'adv', 'adj'):

        yield unit, get_csv(unit, frq_thresh)


def identify_skewed_bigrams(dfs_plus, floor=0.9, count_cutoff=2):
    floor = 0.9
    count_cutoff = 2
    skewed_bigrams = dfs_plus['bigram'].loc[dfs_plus['bigram'].am_p1_given2 > floor, ['l1', 'adv', 'adj', 'f',
                                                                                      'am_expect_diff', 'am_p1_given2', 't_score', 'log_likelihood', 'log_ratio', 'conservative_log_ratio']].round(2)
    for ad in ['adv', 'adj']:
        neg_skewed_counts = skewed_bigrams[ad].astype('string').value_counts()

        print_md_table(neg_skewed_counts.loc[neg_skewed_counts > count_cutoff].to_frame('bigram count'),
                       title=f'### {ad.capitalize()} appearing in more than {count_cutoff} negatively "skewed" bigram (p1.given2 > {floor})\n', n_dec=2)

        print(
            f"\n+ mean bigram count for unique {ad} = {neg_skewed_counts.filter(regex=r'[a-z]').mean().round(1)}")
    print(
        f"skewed bigrams account for {round(100 * skewed_bigrams.f.sum()/ dfs_plus['bigram'].N.iat[0], 2)}% of all tokens")
    return skewed_bigrams


def _main():

    args = _parse_args()

    csv_paths = pd.Series(dict(_pull_data(args.min_frq)))

    print(csv_paths.to_frame('path to `ucs` scores').to_markdown())
    dfs = {count_type:
           load_from_ucs_csv(csv_paths[count_type])
           for count_type in csv_paths.index}

    # > save initial dataframe conversions as pickles
    save_optimized(dfs, csv_paths, verbose=True)

    # * Top Values based on adjusted conditional probability
    # >      of environment (`l1`) given bigram (`l2`): `p1.given2`
    for count_type, df in dfs.items():
        print(f'\n### By {count_type}\n')
        n = 5 if count_type == 'bigram' else 8
        print(df.head(n).round(2).T.to_markdown(floatfmt=',.2f'))

    # * Top `NEGATED` values
    for count_type, df in dfs.items():
        print(f'\n### Top `NEGATED`: By {count_type}\n')
        n = 5 if count_type == 'bigram' else 8
        print(df.filter(like='NEG', axis=0)
              .filter(regex=r'^[^r]').head(n)
              .round(3).T.to_markdown(floatfmt=',.3f'))

    for count_type, df in dfs.items():

        print_example(df, count_type)

    dfs_plus = add_extra_am(dfs)

    for unit, df in dfs_plus.items():
        print_example(df, unit, example_key='necessarily',
                      sort_by='conservative_log_ratio')

    adv = dfs_plus['adv']
    big = dfs_plus['bigram']
    adj = dfs_plus['adj']

    print_md_table(adv.loc[adv.am_p1_given2 > 0.6, ['l1', 'l2', 'f', 'am_expect_diff', 'am_p1_given2']],
                   title='adverbs with adjusted conditional probability of environment > 0.6')

    dfs_plus['bigram'] = dfs_plus['bigram'].assign(
        adv=big.l2.str.split("_").str.get(
            0).astype('string').astype('category'),
        adj=big.l2.str.split("_").str.get(1).astype('string').astype('category'))
    #! #FIXME looks like a bug
    print_example(adv, unit, example_key='necessarily',
                  sort_by='conservative_log_ratio')

    skewed_bigrams = identify_skewed_bigrams(dfs_plus)

    print_example(big, count_type='bigram', example_key='that_complicated')

    sorter = 'conservative_log_ratio'
    print_md_table(skewed_bigrams.copy().sort_values(sorter, ascending=False).reset_index(drop=True),
                   title=f'### Bigrams with adjusted conditional probability of env (`l1`) > 0.9, sorted by `{sorter}`', n_dec=2, comma=False)

    save_optimized(dfs_plus, csv_paths, added_measures=True)


def save_optimized(df_dict, csv_paths, added_measures=False, verbose=False):
    df_dict = _optimize(df_dict, verbose)
    for unit in csv_paths.index:
        save_dataframe(csv_paths[unit].name, df_dict[unit], added_measures)


def load_from_ucs_csv(input_csv):
    df = pd.read_csv(input_csv)
    df['key'] = df.l1.apply(lambda x: x[:3]) + '-' + df.l2
    return df.reset_index().set_index('key')


def print_example(df,
                  count_type=None,
                  example_key=None,
                  round_level=2,
                  sort_by='am_p1_given2',
                  columns_like=r'^([^ECORr_]|E11)',
                  regex=False) -> None:
    """
    Prints a specific example from a dataframe.

    Args:
        df (pandas.DataFrame): The dataframe to extract the example from.
        count_type (str, optional): The type of count to consider. Defaults to None.
        example_key (str, optional): The key of the example to print. Defaults to None.
        round_level (int, optional): The number of decimal places to round the example values to. Defaults to 2.
        sort_by (str, optional): The column to sort the example by. Defaults to 'am_p1_given2'.
        columns_like (str, optional): The regular expression pattern to match column names. Defaults to r'^([^ECORr_]|E11)'.
        regex (bool, optional): Whether to use regex pattern matching for the example key. Defaults to False.

    Returns:
        None
    """
    if not example_key:
        example_keys = {'bigram': 'exactly_sure',
                        'adv': 'exactly',
                        'adj': 'sure'}
        example_key = example_keys[count_type]
    if regex:
        example = df.round(round_level).filter(axis=0, regex=example_key)
    else:
        example = df.round(round_level).filter(axis=0, like=example_key)
    if sort_by not in example.columns:
        sort_by = example.columns.iloc[0]
    example = example.sort_values(
        sort_by, ascending=sort_by.startswith(('r_', 'l')))
    example = example.filter(regex=columns_like).sort_index(axis=1)
    if example.empty:
        print(f'🤷 No {count_type} match {example_key}')
    else:
        transpose = example.shape[0] < example.shape[1] * .9
        print_md_table(example, transpose=transpose, n_dec=round_level,
                       title=f'### {count_type.capitalize()} "{example_key}" examples sorted by `{sort_by}` column\n')
    print('\n---')


def add_extra_am(df_dict):
    for count_type, df in df_dict.items():
        try:
            scores = am.score(df)
        except KeyError:
            df = df.join(fq.observed_frequencies(df)).join(
                fq.expected_frequencies(df))
            scores = am.score(df)
        # loaded_cols = df.columns.to_list()
        df = df.copy().join(scores.loc[:, ~scores.columns.isin(df.columns)])

        print_example(df, count_type, columns_like=r'^[^ECORr]')
        df_dict[count_type] = df

    # am.conservative_log_ratio(dfs_plus['bigram'], alpha=0.05, boundary='poisson').nlargest(20)
    # am.conservative_log_ratio(adv, alpha=0.05, boundary='poisson').sort_values(ascending=False).abs().round(0).value_counts()
    # am.conservative_log_ratio(adv, alpha=0.05, boundary='poisson').sort_values(ascending=False).round(0).abs().nlargest(10)
    return df_dict


def _optimize(df_dict, verbose=False):
    for unit, _df in df_dict.items():
        if verbose:
            print('>> Unoptimized <<')
            _df.info(memory_usage='deep')
        str_cols = _df.select_dtypes(exclude='number').columns.to_list()
        int_cols = _df.columns[_df.columns.str.startswith(
            ('r_', 'C', 'R', 'N', 'f', 'index'))].to_list()
        is_float = ~_df.columns.isin(int_cols + str_cols)
        _df[int_cols] = _df[int_cols].apply(pd.to_numeric, downcast='unsigned')
        _df.loc[:, is_float] = _df.loc[:, is_float].apply(
            pd.to_numeric, downcast='float')
        _df[str_cols] = _df[str_cols].apply(
            lambda c: c.astype('string').astype('category')
            if c.dtype != 'category' and c.nunique() > (len(c) / 2)
            else c)
        if verbose:
            print('\n--------\n>> Optimized DataFrame')
            _df.info(memory_usage='deep')
        _df['l1'] = _df['l1'].astype('category')
        df_dict[unit] = _df
        if verbose:
            print('\n\n============\n\n')
    return df_dict


def save_dataframe(input_name, _df, added_measures=False):
    out_dir = SANPI_DIR / 'results' / 'ucs_tables' / 'dataframes'
    confirm_dir(out_dir)

    out_path = out_dir / input_name.replace('.csv', '.pkl.gz')

    if added_measures:
        out_path = out_path.with_name(
            out_path.name.replace('.pkl.gz', '_extra.pkl.gz'))

    _df.to_pickle(out_path)


# %%
if __name__ == '__main__':
    
    _t0 = pd.Timestamp.now()
    _main()
    _t1 = pd.Timestamp.now()

    print('✔️ Program Completed --', pd.Timestamp.now().ctime())
    print(f'   total time elapsed: {get_proc_time(_t0, _t1)}')
