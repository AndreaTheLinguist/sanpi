# coding=utf-8

# > Imports
import argparse
# import statistics as stat
from pathlib import Path
# from re import search
import re

import pandas as pd
from utils import (cols_by_str, confirm_dir,  # pylint: disable=import-error
                   file_size_round, find_glob_in_dir,
                   get_proc_time, print_iter, print_md_table, save_table,
                   sort_by_margins, unpack_dict, Timer)
from utils.LexicalCategories import (  # pylint: disable=import-error
    SAMPLE_ADJ, SAMPLE_ADV)
from utils.visualize import heatmap  # pylint: disable=import-error
from count_bigrams import (save_filter_index, describe_counts,
                           locate_relevant_hit_tables,
                           select_count_columns,
                           load_from_txt_index)

# > Globals
_SANPI_DIR = Path('/share/compling/projects/sanpi')
_DATA_DIR = Path('/share/compling/data/sanpi')

META_TAG_REGEX = re.compile(r'(th.+p).(\d{1,2}f)')

pd.set_option('display.max_colwidth', 40)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)


def _main():
    print(pd.Timestamp.now().ctime())

    (filter_ids_path, hits_dir,
     frq_out_dir, frq_groups) = _parse_args()

    df = prepare_hit_table(
        filter_ids_path,
        neg_hits_dir=hits_dir)

    _summarize_hits(df)

    if not frq_groups:
        freq_out(filter_ids_path.name, frq_out_dir, df, group='all')

    else:
        for group in frq_groups:

            freq_out(filter_ids_path
                     .name, frq_out_dir, df, group)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-b',
        '--bigram_filter',
        type=Path,
        default=_DATA_DIR.joinpath(
            "4_post-processed/RBXadj/bigram-index_frq-thr0-001p.35f.txt"  # > 0.001% threshold
            # "4_post-processed/RBXadj/bigram-index_frq-thr0-001p.10f.txt" #> 0.001% threshold
            # "4_post-processed/RBXadj/bigram-index_frq-thr0-1p.10f.txt"
            # '4_post-processed/RBXadj/bigram-IDs_thr0-005p.4f.txt'
            # '4_post-processed/RBXadj/bigram-IDs_thr0-1p.35f.txt'
            # '4_post-processed/RBXadj/bigrams-only_thr0-1p.35f.pkl.gz'  # > 0.1% threshold
            # '4_post-processed/RBXadj/bigrams-only_thr0-01p.35f.pkl.gz'  # > 0.01% threshold
            # '4_post-processed/RBXadj/bigrams-only_thr0-001p.35f.pkl.gz' #> 0.001% threshold
            # '4_post-processed/RBXadj/bigrams-only_thr0-0005p.35f.pkl.gz'  # > 0.0005% threshold
        ),
        help=('Path to table of all relevant bigrams: *all* bigrams found for the same corpora, '
              'with cleaning and frequency (of desired threshold) filtering applied.'
              ' as the current negative pattern matches to be "counted". '
              'This is to required to line up the negative environment data '
              'with the frequency filtering applied to the full collection of bigrams.'
              'Should be a pickled dataframe indexed by `hit_id` => negation data `bigram_id`). '))

    parser.add_argument(
        '-d',
        '--hits_dir',
        type=Path,
        default=_DATA_DIR.joinpath('2_hit_tables/RBdirect'),
        help=('Path to location of original hit tables. '
              '(i.e. tables indexed by `hit_id`). '))

    parser.add_argument(
        '-o',
        '--frq_out_dir',
        type=Path,
        default=_SANPI_DIR.joinpath('results/freq_out/RBdirect'),
        help=('Path to location for frequency results (adj_lemma ✕ adv_lemma tables). '
              'Name of file(s) will correspond to `bigram_hits` path'))

    parser.add_argument(
        '-g', '--frequency_group',
        type=str, action='append', dest='frq_groups',
        default=[],
        help=('')
    )

    args = parser.parse_args()
    print_md_table(pd.Series(dict(list(args._get_kwargs()))
                             ).to_frame('arguments given'))
    return (args.bigram_filter, args.hits_dir,
            args.frq_out_dir.resolve(), set(args.frq_groups))


def prepare_hit_table(filter_ids_path: Path,
                      neg_hits_dir: Path) -> pd.DataFrame:

    # TODO: update this method to load from `3_dep_info/`
    with Timer() as timer:
        print('\n## loading data...\n')
        file_tag = META_TAG_REGEX.search(filter_ids_path.stem).group()
        neg_filtered_hits_path = filter_ids_path.parent.parent.joinpath(
            f'{neg_hits_dir.name}/trigger-bigrams_{file_tag}'
        )
        neg_filter_index_path = neg_filtered_hits_path.with_name(
            f'trigger-index_{file_tag}')

        if neg_filtered_hits_path.is_file():
            print(
                f'* Found previous output. Loading data from {neg_filtered_hits_path}...')
            df = pd.read_pickle(neg_filtered_hits_path)  # //.convert_dtypes()
            save_filter_index(neg_filter_index_path, df)
            if not cols_by_str(df, end_str='lower'):
                _add_form_lower(df)
                # forms = cols_by_str(df, end_str='form')
                # df[[f'{f}_lower' for f in forms]] = df[forms].apply(
                #     lambda f: f.str.lower())
                # defaults to `.pkl.gz`
                save_table(df, str(neg_filtered_hits_path.resolve()),
                           '*_form_lower columns added')
        elif neg_filter_index_path.is_file():
            df = load_from_txt_index(
                data_dir=neg_hits_dir, index_txt_path=neg_filter_index_path)
        else:
            df = _prep_df_from_raw(
                filter_ids_path, neg_hits_dir, neg_filtered_hits_path
            )
        # df = _ignore_double_dipping(df)
        # XXX #? what exactly is this doing?
        df['bigram_id'] = df.index.str.rstrip()
        print('✓ time:', timer.elapsed())
    return df


# def _ignore_double_dipping(df):
#     #! #HACK
#     if any(df.duplicated(subset='bigram_id')):
#         print('\n## Found bigram double-dipping!\n\n'
#               '- dropping duplicated bigram environments.')
#         doub_dips = df.loc[df.duplicated('bigram_id', keep=False), :].sort_values('bigram_id')
#         print_md_table(doub_dips.loc[:40, df.columns.isin(['bigram_id', 'mir_form_lower', 'neg_form_lower', 'bigram_lower', 'text_window'])],
#                        indent=2, title='Sample of Bigram Double-Dipping')
#         df = _drop_more_distant_dep(doub_dips)
#     return df


# def _drop_more_distant_dep(dd):
#     for bigram_id, dips in dd.groupby('bigram_id'):
#         dips = dips.loc[dips.text_window == dips.text_window.apply(len).min(), :]

def _prep_df_from_raw(filter_ids_path,
                      neg_hits_dir,
                      neg_filtered_hits_path):

    # df = load_from_txt_index(neg_hits_dir, index_txt_path=filter_ids_path)

    df = _load_and_limit_data(filter_ids_path, data_dir=neg_hits_dir)
    if df.index.name != 'hit_id':
        df = df.set_index('hit_id')
        # print(f'\n> {len(df):,} initial hits')
    _print_uniq_cols_count(df)
    print_md_table(
        _describe_str_word_counts(df).round(),
        indent=2,
        title='Descriptive Stats of Word Columns',
    )

    save_table(
        df,
        str(neg_filtered_hits_path.resolve()).split('.pkl', 1)[0],
        f"filtered {neg_hits_dir.name} hits",
    )

    if len(df) < 10 ^ 6:
        save_table(
            df=df,
            path_str=str(neg_filtered_hits_path.resolve()).split('.pkl', 1)[0],
            df_name=f"filtered {neg_hits_dir.name} hits",
            formats=['psv', 'csv'],
        )

    elif len(df) < 2 * 10 ^ 6:
        save_table(
            df=df,
            path_str=str(neg_filtered_hits_path.resolve()).split('.pkl', 1)[0],
            df_name=f"filtered {neg_hits_dir.name} hits",
            formats=['psv'],
        )

    return df


def freq_out(bigram_filter_name: str,
             frq_out_dir: Path,
             df: pd.DataFrame,
             group: str) -> None:
    _t0 = pd.Timestamp.now()
    #! #[x] modify `get_freq_info` to deal with relevant negation data
    # ^ #[x] modify to set parameter for different crosstab vectors

    frq_gen = gen_freq_info(
        file_tag=META_TAG_REGEX.search(bigram_filter_name).group(),
        df=df, group=group, frq_out_dir=frq_out_dir)

    for frq_df, frq_df_path in frq_gen:

        describe_counts(frq_df, frq_df_path)

    _t1 = pd.Timestamp.now()
    print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')


def _describe_str_word_counts(df: pd.DataFrame) -> pd.DataFrame:
    # [ ] if certain input `df` will have columns: df[['adj_form_lower', 'adv_form_lower']], change `contains` to `endswith`
    word_stats = (df.columns[df.columns.str.contains('_form')]
                  # was: lemma_stats = (df.columns[df.columns.str.endswith('_lemma')]
                  .to_series().apply(
        lambda c: df[c].value_counts().describe())
    ).T
    # was: word_stats.columns = word_stats.columns.str.replace('lemma', 'counts')
    word_stats.columns = word_stats.columns.str.replace('form', 'counts')
    return word_stats.round()


# replaced with ⬆️
# // def _describe_str_lemma_counts(df: pd.DataFrame) -> pd.DataFrame:
    # // # [x] copy changes from `count_bigrams.py` updates
    # // lemma_stats = (df.columns[cols_by_str(df, end_str=('lower', 'lemma'))]
    # //                .to_series().apply(
    # //                    lambda c: df[c].value_counts().describe())
    # //                ).T
    # // lemma_stats.columns = lemma_stats.columns.str.replace('lemma', 'counts')
    # // return lemma_stats.round()


def _load_and_limit_data(filter_ids_path, data_dir: Path) -> pd.DataFrame:
    with Timer() as timer:

        df_iter = filter_hits(data_dir, filter_ids_path)

        combined_df = pd.concat(df_iter)

        print_md_table(combined_df.describe().T.convert_dtypes(),
                       title='\n## Combined Raw Hits Summary')

        print('+ Time to create composite hits dataframe:', timer.elapsed())

    return combined_df


def filter_hits(data_dir: Path, filter_ids_path: Path):

    for i, (pkl, bigram_ids) in enumerate(
            locate_relevant_hit_tables(
                data_dir, filter_ids_path),
            start=1):

        print(f'\n{i}. ../{Path(*pkl.parts[-3:])}')
        print('   + size:', file_size_round(pkl.stat().st_size))

        df = pd.read_pickle(pkl)

        # > select relevant columns
        df = select_count_columns(df)

        print('   + Before filtering to target bigrams only')
        desc_t = df.select_dtypes(
            exclude='object').describe().T.convert_dtypes()
        print_md_table(desc_t.sort_index(),
                       n_dec=0, comma=True,
                       indent=5, title=f'({i}) `{pkl.stem}` summary')

        # > filter to kept bigrams
        #! categories need to be reverted to strings before filtering
        #!   and then redefine categories after rows are removed.
        #!   Otherwise, removed lemmas, etc. will persist as "empty" categories
        cat_cols = df.select_dtypes(include='category').columns
        df[cat_cols] = df[cat_cols].astype('string')
        df = df.loc[df.bigram_id.isin(bigram_ids), :]

        if not df.empty:
            df[cat_cols] = df[cat_cols].astype('category')
            print('   + After filtering to target bigrams')
            print_md_table(df.select_dtypes(exclude='object')
                           .describe().T.convert_dtypes(),
                           indent=5, title=f'({i}) `{pkl.stem}` summary')
            yield df


def flatten_deps(input_path, df):
    for i, dep_col in enumerate(cols_by_str(df, start_str='dep_')):
        #! #BUG get this method working --> KeyError
        dep_df = (pd.json_normalize(df[dep_col], sep='_')
                    .assign(hit_id=df.index,
                            pattern=df.pattern[0])
                    .set_index(['hit_id', 'pattern'], drop=True)
                    .convert_dtypes())
        node = dep_df.node[0]
        dep_df.pop('node')
        dep_df.columns = node + '_' + dep_df.columns
        if i == 0:
            dep_info = dep_df
        else:
            dep_info.join(dep_df)

    print(dep_info)
    dep_path = Path(*input_path.parts[:-3] + (
        '3_dep_info', input_path.parts[-2], input_path.name.replace('hits.pkl.gz', 'deps')))
    save_table(df=dep_info, path_str=str(dep_path),
               df_name=dep_path.stem, formats=['pickle', 'csv'])


# def select_count_columns(df):
    # # * create `NODE_form_lower` if it does not exist yet
    # _add_form_lower(df)

    # _add_prev(df)
    # if 'pattern' in df.columns:
    #     df.loc[:, 'pattern'] = df.pattern.astype('category')

    # cols = (
    #     ['bigram_id', 'token_str', 'pattern', 'category']
    #     # targets: adv/adj/neg/nr/relay_lemma/form(_lower), text_window, neg/mod_head/deprel
    #     + cols_by_str(df, end_str=('lemma', 'form', 'lower', 'window', 'deprel', 'head'))
    #     # targets: any `dep_str_*` columns if input from `3_dep_info/`
    #     + cols_by_str(df, start_str='dep_str')
    # )

    # #! use `.isin()` to avoid potential KeyError
    # sdf = df.loc[:, df.columns.isin(
    #     (c for c in cols if not c.startswith('mod_')))]

    # return sdf


def _add_form_lower(df):
    if ('adv_form_lower' not in df.columns
            or 'adj_form_lower' not in df.columns):

        forms = cols_by_str(df, end_str='form')
        df[[f'{f}_lower' for f in forms]] = df[forms].apply(
            lambda f: f.str.lower())
    if 'bigram_lower' not in df.columns:
        df['bigram_lower'] = df.adv_form_lower + '_' + df.adj_form_lower


def _add_prev(df):
    prev_ix = df.adv_index - 1
    has_word_between = df.neg_index != prev_ix
    # post_adj_ix = df.adj_index + 1
    df.loc[has_word_between, 'prev_form_lower'] = (
        has_word_between.index.to_series()
        .apply(lambda i:
               df.token_str[i].split()[prev_ix[i]].lower())
        .astype('category'))


def _print_uniq_cols_count(df: pd.DataFrame,
                           cols=None,
                           updated: bool = True,
                           label: str = '',
                           head_mark: str = ''):
    if not label:
        label = 'updated' if updated else 'initial'
    if not head_mark:
        head_mark = '+' if updated else '='
    if not cols:
        # ! modified to default to `.contains('_form')`
        # [ ] if certain `adv_form_lower` and `adj_form_lower` have both been added to any frame this is called on, change to `.endswith('form_lower')`
        cols = df.columns[df.columns.str.contains('_form')]
    counts_info = {
        c.upper(): df[c].nunique()
        for c in cols
    }
    str_len = len(max(counts_info.keys()))
    num_len = len(str(max(counts_info.values()))) + 1
    counts = ['{0:<{1}s}:  {2:>{3},d}'.format(k, str_len, v, num_len)  # pylint: disable=consider-using-f-string
              for k, v in counts_info.items()]
    print_iter(counts,
               header=f'{head_mark} unique columns in {label} hits',
               indent=2)

    # if not label:
    #     label = 'updated' if updated else 'initial'
    # if not head_mark:
    #     head_mark = '+' if updated else '='
    # if not cols:
    #     suffix='form_lower' if 'adj_form_lower' in df.columns else 'form'
    #     cols = cols_by_str(df, end_str=suffix)
    # counts_info = {
    #     c.upper(): count_uniq(df[c])
    #     for c in cols
    # }
    # str_len = len(max(counts_info.keys()))
    # num_len = len(str(max(counts_info.values()))) + 1
    # counts = ['{0:<{1}s}:  {2:>{3},d}'.format(k, str_len, v, num_len)  # pylint: disable=consider-using-f-string
    #           for k, v in counts_info.items()]
    # print_iter(counts,
    #            header=f'{head_mark} unique lemmas in {label} hits',
    #            indent=2)


def _summarize_hits(df):
    lemma_counts_summ = _describe_str_word_counts(df)
    tok_thresh_c = int(lemma_counts_summ.loc['min', :].min())
    print(f'    ⇟ minimum hits/lemma in data: {tok_thresh_c:,}')
    print_md_table(df.describe().T, indent=2,
                   title='Frequency Filtered Hits Summary')
    print_md_table(lemma_counts_summ, indent=2,
                   title='Frequency Filtered Lemma Distributions')


def gen_freq_info(df: pd.DataFrame,
                  group: str,
                  frq_out_dir: Path,
                  file_tag: str) -> tuple:
    print(f'\n## Processing Frequency data for {group} hits.')
    if group != 'all':
        frq_out_dir = frq_out_dir.joinpath(group)
    confirm_dir(frq_out_dir)
    df['bigram_lower'] = df.adv_form_lower + '_' + df.adj_form_lower
    cross_vectors_dict = {
        # ^#[ ] turn these into namedtuples?
        'adj-x-neg': ['adj_form_lower', 'neg_form_lower'],
        'adj-x-adv': ['adj_form_lower', 'adv_form_lower'],
        'adv-x-neg': ['adv_form_lower', 'neg_form_lower'],
        'bigram-x-neg': ['bigram_lower', 'neg_form_lower'],
        'bigram-x-deprel': ['bigram_lower', 'neg_deprel'],
        'bigram-x-negHead': ['bigram_lower', 'neg_head'],
        'bigram-x-pattern': ['bigram_lower', 'pattern'],
        'bigram-x-prev': ['bigram_lower', 'prev_form_lower'],
        'prev-x-negLemma': ['prev_form_lower', 'neg_lemma'],
        # TODO#[ ] add `dep_str_*` values for loading from `3_def_info/`
    }
    # HACK This is a shortcut to deal with positive mirrors. A better approach would be to:
    # TODO #[ ] configure initial `cross_vectors_dict` to infer relevant columns from current columns. E.g. collect all node types using a regex r'(\w+)_form_lower' on the columns and set cross values for each
    if not any(df.columns.str.startswith('neg')):
        cross_vectors_dict = {k.replace('neg', 'mir'): [v.replace(
            'neg', 'mir') for v in v_list] for k, v_list in cross_vectors_dict.items()}
    # > these values have to be inherited from the
    # > bigram frequency filtering used to select negated hits
    # ^#[x] modify this to encode different crosstabulations if that option is added
    for cross_label, cross_vector_names in cross_vectors_dict.items():
        if any(n not in df.columns for n in cross_vector_names):
            print(
                f'Error: {cross_vector_names} not (both) found in dataframe.')
            continue
        frq_out_stem = get_freq_out_stem(cross_label, file_tag, group)

        # > method returns `None` if stem not found
        frq_df_path = find_glob_in_dir(frq_out_dir, f'*{frq_out_stem}*pkl.gz')

        # > if crosstabulated frequency table is found
        if frq_df_path:
            print(f'\n* frequency table ({group}) found.')
            frq_df = _load_frq_table(frq_df_path)

        # > if frequency table is not found;
        # >   i.e. `find_glob_in_dir` call returned None
        else:
            frq_df_path = frq_out_dir.joinpath(frq_out_stem + '.pkl.gz')
            # > sanity check
            if not frq_df_path.name.endswith('f.pkl.gz'):
                exit(f'frequency path error: {frq_df_path}')

            # [x] move this to earlier
            # // forms=cols_by_str(df, end_str='form')
            # // df[[f'{f}_lower' for f in forms]] = df[forms].apply(lambda f: f.str.lower())
            # // frq_df = _build_frq_df(df.adj_form_lower, df.adv_form_lower, frq_df_path, group)
            frq_df = _build_frq_df([df[v] for v in cross_vector_names], cross_label,
                                   save_path=frq_df_path, group_code=group)
        yield frq_df, frq_df_path


def get_freq_out_stem(cross_label: str,
                      freq_meta_tag: str, group_code):
    return f'{group_code}-frq_{cross_label}_{freq_meta_tag}'


def _load_frq_table(frq_df_path):
    print(f'  Loading from ../{frq_df_path.relative_to(_SANPI_DIR)}...')
    if frq_df_path.suffix.endswith('csv'):
        frq_df = pd.read_csv(frq_df_path)
        frq_df.columns = frq_df.columns.str.strip()
    elif '.pkl' in frq_df_path.suffixes:
        frq_df = pd.read_pickle(frq_df_path)

    if not frq_df.index.name and any(frq_df.columns.str.contains('_')):
        indexer = str(frq_df.columns[frq_df.columns.str.contains('_')][0])
        frq_df = frq_df.set_index(indexer)
    # // frq_df.columns.name = 'adv_lemma'
    return frq_df


def _build_frq_df(cross_vectors: list,
                  #   freq_table_rows: pd.Series,
                  #   freq_table_cols: pd.Series,
                  cross_label: str,
                  save_path: Path,
                  group_code: str = 'all') -> pd.DataFrame:
    # ! #[x]: modify this method to run on `*_form.str.lower()` instead of `*_lemma`
    # ^ #[x]: also modify to have nodes to crosstab as arguments so it can be run for multiple different combinations
    freq_table_rows, freq_table_cols = _filter_bigrams(
        cross_vectors) if group_code.lower() != 'all' else cross_vectors

    # * Crosstabulate vectors to get co-occurrence frequencies
    _t0 = pd.Timestamp.now()
    frq_df = pd.crosstab(index=freq_table_rows,
                         columns=freq_table_cols,
                         margins=True,
                         margins_name='SUM')
    _t1 = pd.Timestamp.now()

    print(
        f'[ Time to crosstabulate {cross_label} frequencies: {get_proc_time(_t0, _t1)} ]')

    frq_df = sort_by_margins(frq_df, margins_name='SUM')
    title = (f'{group_code} {freq_table_rows.name} ✕ {freq_table_cols.name} frequency table'
             .replace('JxR', 'scale diagnostics'))
    save_table(frq_df,
               str(save_path),
               title, formats=['pickle', 'csv'])
    return frq_df


def _filter_bigrams(cross_vectors: list):
    # [ ]: This needs adjustments if the filter is to apply to dependency paths
    for i, series in enumerate(cross_vectors):
        # > don't try to apply this filter to other attribute types
        if not series.name.endswith(('lemma', 'form', 'lower')):
            continue
        # > filter adjectives
        if series.name.startswith('adj'):
            adj_filter, __ = unpack_dict(SAMPLE_ADJ)
            cross_vectors[i] = series.loc[series.isin(adj_filter)]
        # > filter adverbs
        elif series.name.startswith('adv'):
            adv_filter, __ = unpack_dict(SAMPLE_ADV, values_name='adv')
            cross_vectors[i] = series.loc[series.isin(adv_filter)]
    return cross_vectors


# def _describe_counts(df: pd.DataFrame,
    #  df_path: str) -> None:
    # data_label = df_path.name.replace('.csv', '')
    # stats_dir = df_path.parent.joinpath('descriptive_stats')
    # confirm_dir(stats_dir)
    # out_path_stem = f'stats_{data_label}'
    # df = df.fillna(0)
    # most_var_col = df.columns.to_list()[1:21]
    # most_var_row = df.index.to_list()[1:21]
    # for frame in (df, df.transpose()):
    #     param = frame.columns.name
    #     print(
    #         f'\n## Descriptive Statistics for `{frame.index.name}` by `{param}`')
    #     no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
    #     desc_no_sum = no_sum_frame.describe()
    #     # > need to exclude the ['SUM','SUM'] cell
    #     sum_col = frame.loc[frame.index != 'SUM', 'SUM']
    #     desc_sum = sum_col.describe().to_frame()

    #     for desc, values in [(desc_no_sum, no_sum_frame), (desc_sum, sum_col)]:
    #         desc = _enhance_descrip(desc, values)
    #         if 'SUM' in desc.index:
    #             desc = desc.transpose()
    #             desc.columns = [f'Summed Across {param}s']
    #             print_md_table(desc.round(), title=' ')
    #         else:
    #             save_table(
    #                 desc,
    #                 f'{stats_dir}/{param[:4].strip("_-").upper()}-{out_path_stem}',
    #                 f'{param} descriptive statististics for {out_path_stem}',
    #                 ['csv'])
    #             print_md_table(desc.sample(min(len(desc), 6)).round(),
    #                            title=f'Sample {param} Stats ')

    #             # [ ] # ? (old) add simple output of just `df.var_coeff`?
    #             # desc.info()
    #             if param == 'Adverb':
    #                 most_var_col = _select_words(desc)
    #             else:
    #                 most_var_row = _select_words(desc)

    # _visualize_counts(df.loc[['SUM'] + most_var_row,
    #                   ['SUM'] + most_var_col], df_path)


# def _enhance_descrip(desc: pd.DataFrame,
    #  values: pd.Series) -> pd.DataFrame:
    # values.apply(pd.to_numeric, downcast='unsigned')
    # desc = desc.transpose()
    # desc = desc.assign(total=values.sum(),
    #                    var_coeff=desc['std'] / desc['mean'],
    #                    range=desc['max'] - desc['min'],
    #                    IQ_range=desc['75%'] - desc['25%'])
    # desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
    #                    lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    # if 'SUM' not in desc.index:
    #     desc = desc.assign(
    #         plus1_geo_mean=values.add(1).apply(stat.geometric_mean),
    #         plus1_har_mean=values.add(1).apply(stat.harmonic_mean))
    # for col in desc.columns:
    #     if col in ('mean', 'std', 'variance', 'coeff_var'):
    #         desc.loc[:, col] = pd.to_numeric(desc[col].round(2),
    #                                          downcast='float')
    #     else:
    #         desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    # return desc


# def _select_words(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
    # nth = len(desc) // 6
    # trim = int(len(desc) * 0.01)
    # desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    # top_means_metric = desc.loc[
    #     (desc['mean'] > (desc_interior['mean'].median() * .75))
    #     &
    #     (desc.total > (desc_interior['total'].median() * .75)), metric]
    # # ? Is the following just temporarily commented out or fully obsolete ⬇️
    # # info_list = []
    # # for label, desc_df in {'interior': desc.iloc[5:, :], 'full': desc}.items():
    # # top_means = desc_df.loc[
    # #     (desc_df['mean'] > (desc_df['mean'].median() + 0.5 * 1))
    # #     &
    # #     (desc_df.total > (desc_df.total.median() * 1.1))
    # #     , [metric, 'mean', '50%', 'total', 'max', 'range']]
    # # info = top_means.describe()
    # # info.columns = info.columns.astype('string') + f'_{label}'
    # # info_list.append(info)
    # # print_md_table(info_list[0].join(info_list[1]).sort_index(axis=1).round(0),
    # #                title='Compare descriptive stats')
    # if largest:
    #     words = top_means_metric.squeeze().nlargest(nth).index.to_list()
    # else:
    #     words = top_means_metric.squeeze().nsmallest(nth).index.to_list()
    # return words


def _visualize_counts(frq_df, frq_df_path):
    heat_dir = frq_df_path.parent.joinpath('images')
    confirm_dir(heat_dir)
    heat_fname = f'heatmap_{frq_df_path.stem}.png'
    if len(frq_df) < 60 and len(frq_df.columns) < 40:
        heatmap(frq_df,
                save_name=heat_fname,
                save_dir=heat_dir)
    else:
        heatmap(frq_df.sample(min(60, len(frq_df))).T.sample(min(30, len(frq_df.T))).T,
                save_name=f'sample-{heat_fname}',
                save_dir=heat_dir)


if __name__ == '__main__':
    global_start_time = pd.Timestamp.now()
    _main()
    global_end_time = pd.Timestamp.now()
    finish_str = ('✓ Finished @ '
                  + global_end_time.strftime("%Y-%m-%d %I:%M%p"))
    w = len(finish_str)+1
    print('',
          '.'*w,
          finish_str,
          sep='\n')
    time_str = '== Total Run Time =='
    print(time_str)
    print(get_proc_time(global_start_time, global_end_time).center(len(time_str)))
