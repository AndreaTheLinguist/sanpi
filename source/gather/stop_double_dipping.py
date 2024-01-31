# %%
import argparse
from pathlib import Path

import pandas as pd
from utils.dataframes import print_md_table, save_table, Timer
from utils.general import confirm_dir

# corpus_parts = ('Pcc09', 'Pcc18', 'Pcc27', 'Nyt1')
DATA_DIR = Path('/share/compling/data/sanpi')
DEMO_DATA_DIR = Path('/share/compling/projects/sanpi/demo/data')


def _parse_args():

    parser = argparse.ArgumentParser(
        description=('module to eliminate extraneous hits for each unique bigram_id.'
                     'Can be run as a script or have methods imported elsewhere.'
                     'Condenses the hits for a single corpus_part (e.g. `Pcc00`) and pattern category '
                     '(e.g. `NEGmirror`) and outputs: (1) `.tsv` of all removed hits, '
                     '(2) `.pkl.gz` of *all* hits, including double-dipping and all patterns for given category, '
                     '(3) an updated condensed `.pkl.gz` file with unique bigram_id values '
                     '(no bigram double-dipping) for all patterns in the category'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--pat_cat',
        type=str, default='NEGmirror',
        help=('Pattern category to process. Must correspond to a subdir of '
              '`data/sanpi/2_hit_tables/` (and also `projects/sanpi/Pat/`)')
    )

    parser.add_argument(
        '-c', '--corpus_part',
        type=str, default='bigram-PccVa',
        help='corpus part (i.e. directory name containing *.conllu files) to process. 1 flag per directory name.')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true', default=False,
        help='option to print detailed information on bigram double-dipping evaluation')

    parser.add_argument(
        '-d', '--demo',
        action='store_true',
        help='Option to direct program to run on data in `./demo/` instead of the default')

    parser.add_argument(
        '-D', '--data_dir',
        type=Path,
        default=DATA_DIR,
        help='Option to set the top level data directory directly (i.e. parent of `2_hits_table/`)')

    return parser.parse_args()


def _select_data(eval_dir: Path,
                 corpus_part_name: str):
    """
    Selects and returns the data from the specified evaluation directory and corpus part name.

    Args:
        eval_dir (Path): The path to the evaluation directory.
        corpus_part_name (str): The name of the corpus part.

    Returns:
        DataFrame: The concatenated data from the input hit paths.

    Examples:
        >>> _select_data(Path('/path/to/eval'), 'corpus_part')
        DataFrame(...)
    """
    input_hit_paths = eval_dir.glob(f'*{corpus_part_name}*pkl.gz')
    dfs = [pd.read_pickle(p) for p in input_hit_paths]
    df = pd.concat(dfs) if len(dfs) > 1 else dfs[0]
    print_md_table(
        df.loc[df.utt_len < df.utt_len.mean()*.7, :].sample(3).filter(
            regex=r'text|category|pattern|[gr]_head|deprel|forms_lower$'),
        title=f'\nSample of loaded {corpus_part_name} data')
    return df


def set_export_dir(eval_dir):
    export_dir = eval_dir / 'bigram_double-dipping'
    confirm_dir(export_dir)
    return export_dir


def print_dip_info(dips: pd.DataFrame, title='\n### Sample of Bigram Double-Dipping\n'):
    print_md_table(dips.loc[:, dips.columns.isin(['mir_form_lower', 'neg_form_lower',
                                                  'bigram_lower', 'text_window', 'pattern'])]
                   .head(8),
                   indent=0, title=title)
    print('\n***\n')

# %% [markdown]
# ⚠️ `tail(1)` is applied in `_select_nearest_trigger()` to select the hit with the nearest trigger node in the case of multiple hits with the same `text_window`.
#
# Hits are sorted by `hit_id` in ascending order, thus the hit with the greatest trigger index/nearest trigger node will be last.
#
# e.g. (despite this being a bad example of the phenomenon):
#
# `pcc_eng_28_044.5505_x0704677_29:4-5` dips
#
# | hit_id                                    | text_window                               | bigram_id                           | neg_form_lower   | bigram_lower   | pattern      |
# |:------------------------------------------|:------------------------------------------|:------------------------------------|:-----------------|:---------------|:-------------|
# | pcc_eng_28_044.5505_x0704677_29:**1**-4-5 | **No** no no no Closer to the edge Closer | pcc_eng_28_044.5505_x0704677_29:4-5 | no               | no_closer      | neg-mirror-R |
# | pcc_eng_28_044.5505_x0704677_29:**2**-4-5 | No **no** no no Closer to the edge Closer | pcc_eng_28_044.5505_x0704677_29:4-5 | no               | no_closer      | neg-mirror-R |
# | pcc_eng_28_044.5505_x0704677_29:**3**-4-5 | No no **no** no Closer to the edge Closer | pcc_eng_28_044.5505_x0704677_29:4-5 | no               | no_closer      | neg-mirror-R |
#
# ***
#
# Kept "dip" for `pcc_eng_28_044.5505_x0704677_29:4-5`
#
# | hit_id                                    | text_window                               | bigram_id                           | neg_form_lower   | bigram_lower   | pattern      |
# |:------------------------------------------|:------------------------------------------|:------------------------------------|:-----------------|:---------------|:-------------|
# | pcc_eng_28_044.5505_x0704677_29:**3**-4-5 | No no **no** no Closer to the edge Closer | pcc_eng_28_044.5505_x0704677_29:4-5 | no               | no_closer      | neg-mirror-R |
#
#


def trigger_nearest_bigram(dips: pd.DataFrame) -> pd.DataFrame:
    text_win_len = dips.text_window.apply(len)
    nearest = text_win_len == text_win_len.min()
    return dips.loc[nearest, :].tail(1)


def select_nearest_triggers(dd, verbose=False):
    """
    Selects and returns the nearest triggers from the given DataFrame.

    Args:
        dd (DataFrame): The DataFrame containing the data.
        verbose (bool, optional): Whether to print verbose information. Defaults to False.

    Returns:
        DataFrame: The concatenated DataFrame of the kept "dip" for each bigram.

    Examples:
        >>> select_nearest_triggers(df, verbose=True)
        DataFrame(...)
    """
    keepers = []
    for bigram_id, dips in dd.groupby('bigram_id'):
        if verbose:
            print_dip_info(dips, title=f'\n{bigram_id} dips\n')
        dips = trigger_nearest_bigram(dips)
        if verbose:
            print_dip_info(dips, title=f'\nKept "dip" for {bigram_id}\n')
        keepers.append(dips)
    return pd.concat(keepers)


def ignore_bigram_double_dipping(df,
                                 export_path: Path = None,
                                 verbose: bool = False):
    """
    Ignores bigram double-dipping in the given DataFrame and returns the modified DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the data.
        export_path (Path, optional): The path to export the dropped double-dips as a pickled DataFrame. Defaults to None.
        verbose (bool, optional): Whether to print verbose information. Defaults to False.

    Returns:
        DataFrame: The modified DataFrame after ignoring bigram double-dipping.

    Examples:
        >>> ignore_bigram_double_dipping(df, export_path=Path('/path/to/export'), verbose=True)
        DataFrame(...)
    """
    init_hits = len(df)
    print(f'Total loaded hits: {init_hits}')
    if any(df.duplicated(subset='bigram_id')):
        print('\n👀  bigram double-dipping found')
        doub_dips = df.loc[df.duplicated(
            'bigram_id', keep=False), :].sort_index(axis=0)
        print_dip_info(doub_dips)
        kept_dips = select_nearest_triggers(doub_dips, verbose=verbose)
        # > save dropped double-dips as pickled dataframe
        if export_path:
            print(
                f'double-dips removed -> {export_path.relative_to(export_path.parent.parent.parent)}')
            save_table(doub_dips[~doub_dips.index.isin(kept_dips.index)], save_path=export_path,
                       df_name='hits ignored due to bigram double-dipping (excluded from analysis)',
                       formats=['tsv'])

        df = pd.concat([df[~df.index.isin(doub_dips.index)],
                       kept_dips]).sort_index(axis=0)
    kept_hits = len(df)
    n_drop = init_hits - kept_hits
    print(f'\n- _{n_drop} double-dipped hits dropped, {round(n_drop/init_hits*100, 2)}% current hit selection_')
    return df


def _main():
    args = _parse_args()
    pat_cat = args.pat_cat
    eval_dir = (args.data_dir
                or (DEMO_DATA_DIR if args.demo else DATA_DIR)
                ) / '2_hit_tables' / pat_cat
    print('\n# Eliminating bigram double-dipping (non-unique',
          f'bigram_id values across hits) in `{eval_dir}/`')

    export_dir = set_export_dir(eval_dir)
    corpus_part_name = args.corpus_part

    # validate corpus part name given
    found = list(DATA_DIR.joinpath('subsets')
                 .glob(f'bigram_*/{corpus_part_name}'))
    if len(found) != 1 or not found[0].is_dir():
        raise FileNotFoundError(
            (f'Specified `corpus_part` "{corpus_part_name}" is not a unique corpus part directory. '
             '(Was there a typo or missing `--demo` flag?) Exiting.'))

    hits_group = f'{pat_cat}/{corpus_part_name}* hits'
    print(f'\n## Looking for `{pat_cat}` Bigram Double-Dipping',
          f'in `{corpus_part_name}` matches\n')
    df = _select_data(eval_dir, corpus_part_name)
    if 'bigram_id' not in df.columns:
        df = df.rename(columns={'colloc_id': 'bigram_id'})
    _save_original(export_dir, eval_dir, corpus_part_name, hits_group, df)
    export_path = export_dir.joinpath(
        f"{corpus_part_name.replace('bigram-', '')}-{pat_cat}_double-dips-ignored.pkl.gz")
    if not export_path.is_file():
        kept_hits = ignore_bigram_double_dipping(
            df, export_path, verbose=args.verbose)
        _save_updated_table(corpus_part_name, eval_dir, kept_hits)
    else:
        print(f'Bigram double-dipping already dealt with for {hits_group}')


def _save_updated_table(corpus_part, eval_dir, updated_df):
    condense_dir = eval_dir / 'condensed'
    confirm_dir(condense_dir)
    update_path = condense_dir.joinpath(
        f"{corpus_part.replace('bigram-','')}_all-{eval_dir.name}_unique-bigram-id_hits.pkl.gz")
    print('updated ->',
          f'{update_path.relative_to(update_path.parent.parent.parent)}')
    save_table(updated_df, update_path,
               f'updated table of all {eval_dir.name}/{corpus_part}* hits with only unique bigram_id strings')


def _save_original(export_dir, eval_dir, corpus_part, hits_group, df):
    out_path = export_dir / \
        f'{corpus_part}_all-{eval_dir.name}.pkl.gz'.replace('bigram-', '')
    if not out_path.is_file():
        print('original ->',
              f'{out_path.relative_to(out_path.parent.parent.parent)}')
        save_table(df, out_path,
                   f'all {hits_group} prior to bigram double-dipping filtering')


# %%
if __name__ == '__main__':
    with Timer() as timer:
        _main()
        print('\n* Total Time:', timer.elapsed())
