import re
from pathlib import Path
from pprint import pprint

import pandas as pd
import pyarrow as pyar

from source.utils.associate import POLAR_DIR, TOP_AM_DIR, adjust_am_names
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import show_sample
from source.utils.dataframes import update_assoc_index as update_index
from source.utils.dataframes import write_part_parquet as parq_it
from source.utils.general import (confirm_dir, print_iter, run_shell_command,
                                  snake_to_camel, timestamp_today)
from source.utils.sample import sample_pickle as sp

BASIC_FOCUS = ['f',
               'am_p1_given2',
               'conservative_log_ratio',
               'am_p1_given2_simple',
               'am_log_likelihood',
               'l1', 'l2',
               'f1', 'f2',
               'N',
               'E11', 'unexpected_f',
               'unexpected_ratio',
               'am_odds_ratio_disc',
               't_score',
               'mutual_information',
               ]
ADX_COLS = ['adv', 'adv_total', 'adj', 'adj_total']
P2_COLS = ['am_p2_given1', 'am_p2_given1_simple']
DELTA_COLS = ['deltaP_max', 'deltaP_mean']
FOCUS_DICT = {
    'ALL': {
        'adv_adj': BASIC_FOCUS + P2_COLS + DELTA_COLS,
        'polar': BASIC_FOCUS + ADX_COLS},
    'NEQ': {
        'adv_adj': BASIC_FOCUS + P2_COLS,
        'polar': BASIC_FOCUS + P2_COLS + ADX_COLS
    }}
FOCUS = BASIC_FOCUS
ABBR_FOCUS = adjust_am_names(FOCUS)


def _set_priorities():
    _priority_dict = {
        # 'NEQ': ['LRC', 'P1', 'G2', 'P2'],
        'NEQ':  ['conservative_log_ratio', 'am_p1_given2_simple', 'am_log_likelihood', 'am_p2_given1_simple'],
        # 'ALL': ['dP1', 'LRC', 'G2', 'P1'],
        'ALL': ['am_p1_given2', 'conservative_log_ratio', 'am_log_likelihood', 'am_p1_given2_simple'],
    }
    tags = tuple(_priority_dict.keys())
    for tag in tags:
        cols = _priority_dict[tag]
        _priority_dict[f'{tag}_init'] = cols
        _priority_dict[f'{tag}'] = adjust_am_names(cols)
        blind_cols = ['conservative_log_ratio',
                      'deltaP_mean', 'deltaP_max', 'unexpected_ratio']
        _priority_dict[f'{tag}_blind'] = adjust_am_names(blind_cols)
    return _priority_dict


METRIC_PRIORITY_DICT = _set_priorities()

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def locate_polar_am_paths(data_tag: str = 'ALL',
                          unit: str = 'adv',
                          superset_floor: int = 1000,
                          mirror_floor: int = 500):
    globs = {'RBdirect': f'*{data_tag}*min{superset_floor}x*parq',
             'mirror': f'*{data_tag}*min{mirror_floor}x*parq'}
    if data_tag not in ('NEQ', 'ALL'):
        raise ValueError(
            f'Invalid data tag, "{data_tag}". Options are: "NEQ" or "ALL".')

    am_paths = {
        p.name:
            tuple((p/unit/'extra').glob(globs[p.name]))
        for p in POLAR_DIR.iterdir()}

    err_message_trunk = (', has no corresponding processing. Change the value or run:\n'
                         '  $ bash ../script/run_assoc.sh -m ')
    for key, paths_tuple in am_paths.items():
        if not paths_tuple:
            err_message_ends = (
                f'Provided frequency floor value, {superset_floor}', str(
                    superset_floor)
            ) if key == 'RBdirect' else (
                f'Provided frequency floor value, {mirror_floor}',
                f'{mirror_floor} -P "mirror"')
            raise ValueError(err_message_trunk.join(err_message_ends))

        am_paths[key] = paths_tuple[0]

    show_sample(format='fancy_grid',
                df=pd.DataFrame.from_dict(
                    am_paths, orient='index',
                    columns=['path to selected AM dataframe']))
    return am_paths


def locate_bigram_am_paths(data_tag, mirror_floor, bigram_floor):
    # // def floor(name):
    # //     return mirror_floor if name.endswith("mirror") else bigram_floor
    # // paths_dict = {
    # //     d.name: tuple(
    # //         d.joinpath('bigram/extra').glob(
    # //             f'*{data_tag}*min{floor(d.name)}x*extra.parq')
    # //     )[0]
    # //     for d in POLAR_DIR.iterdir()
    # // }
    # // pprint(paths_dict)
    # // return paths_dict

    return locate_polar_am_paths(data_tag, unit='bigram',
                                 superset_floor=bigram_floor,
                                 mirror_floor=mirror_floor)


def verify_columns(am_df):
    if 'adj' in am_df.columns and any(am_df['adj'].isna()):
        am_df[['adv', 'adj']] = am_df.l2.str.extract(
            r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$')


def load_bigram_dfs(bigram_am_paths) -> dict:
    return {n: catify(update_index(pd.read_parquet(p)),
                      reverse=True)
            for n, p in bigram_am_paths.items()}


def filter_load_adx_am(am_path: Path, column_list: list = None) -> pd.DataFrame:
    column_list = column_list or FOCUS
    backup_columns = pd.Series(column_list + ['adv', 'adv_total', 'adj', 'adj_total']
                               ).drop_duplicates(keep=False).tolist()
    if am_path.suffix.startswith('.parq'):
        try:
            am_df = pd.read_parquet(am_path, columns=column_list)
        except pyar.ArrowInvalid:
            am_df = pd.read_parquet(am_path, columns=backup_columns)

    elif am_path.suffix.startswith('.csv'):
        snippet_cols = pd.read_csv(am_path, nrows=3).columns
        am_df = pd.read_csv(
            am_path,
            usecols=['key'] + (column_list
                               if any(snippet_cols.str.startswith(('adv', 'adj')))
                               else backup_columns),
            index_col='key')
    elif '.pkl' in am_path.suffixes:
        am_df = pd.read_pickle(am_path).filter(column_list)
    return update_index(am_df.convert_dtypes())


def get_top_vals(df: pd.DataFrame,
                 index_like: str = 'NEG',
                 metric_filter: str or list = None,
                 k: int = 10,
                 val_col: str = None,
                 ignore_neg_adv: bool = True):
    if metric_filter is None:
        metric_filter = ['am_p1_given2', 'conservative_log_ratio']
    env_df = df.copy().loc[df.conservative_log_ratio >=
                           1].filter(like=index_like, axis=0)
    if ignore_neg_adv:
        env_df = env_df.loc[~df.l2.isin(
            ("n't", 'not', 'barely', 'never', 'no', 'none')), :]
    if isinstance(metric_filter, str):
        metric_filter = [metric_filter]

    top = pd.concat([env_df.nlargest(k, m) for m in metric_filter]
                    ).drop_duplicates(keep='first')

    if val_col:
        top = top[[val_col] + metric_filter]

    return top.sort_values(metric_filter, ascending=False)


def show_top_positive(adv_df,
                      k: int = 15,
                      filter_and_sort: list = None):

    if filter_and_sort is None:
        filter_and_sort = [
            'conservative_log_ratio',
            'am_log_likelihood',
            'am_p1_given2',
        ]
    _l1 = adv_df.filter(like='O', axis=0).l1.iat[0].lower().strip()
    _N = int(adv_df.N.iat[0])
    ie = '(`set_diff`, $*\complement_{N^+}$)' if _l1.startswith(
        "com") else '(`mirror`, $@P$)'
    print(f'#### Adverbs in top {k}',
          r'for $LRC$, $G^2$, and $\Delta P(\texttt{env}|\texttt{adv})$',
          f'measuring association with *{_l1.capitalize()}* Environments {ie}',
          end='\n'*2)
    print(f'Total Tokens in dataset: $N = {_N:,}$')
    nb_show_table(
        get_top_vals(
            adv_df.filter(items=FOCUS),
            k=k,
            metric_filter=filter_and_sort,
            index_like='O',  # should match "POS" & "COM", but neither "NEG*"
        ).round(2).sort_values(filter_and_sort, ascending=False)
        .set_index('l2').drop(['N', 'l1'], axis=1)
    )


def force_ints(_df):
    count_cols = _df.filter(regex=r'total|^[fN]').columns
    _df[count_cols] = _df[count_cols].astype('int')

    return _df


def nb_show_table(df, n_dec: int = 2,
                  adjust_columns: bool = True,
                  outpath: Path = None,
                  return_df: bool = False,
                  suppress_printing: bool = False
                  ) -> None or pd.DataFrame:
    _df = df.copy()
    try:
        start_0 = _df.index.start == 0
    except AttributeError:
        pass
    else:
        _df.index.name = 'rank'
        if start_0:
            _df.index = _df.index + 1
    if adjust_columns:
        _df = adjust_am_names(_df)
    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index]
    table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    if outpath:
        outpath.write_text(table)
    if not suppress_printing:
        print(f'\n{table}\n')
    return (_df if return_df else None)


def show_adv_bigrams(sample_size, C,
                     bigram_dfs,
                     selector: str = 'dP1',
                     column_list: list = None,
                     focus_cols: list = FOCUS) -> dict:
    def _force_ints(_df):
        count_cols = _df.filter(regex=r'total$|^[fN]').columns
        _df.loc[:, count_cols] = _df.loc[:, count_cols].apply(
            pd.to_numeric, downcast='unsigned')
        return _df

    def get_top_bigrams(bdf, adv, bigram_k):
        bdf = _force_ints(bdf.loc[bdf.adv == adv, :])
        top_by_metric = [bdf.nlargest(bigram_k * 2, m) for m in ['dP1', 'LRC']]
        half_k = bigram_k // 2
        adv_pat_bigrams = pd.concat(
            [top_bigrams.head(half_k) for top_bigrams in top_by_metric]).drop_duplicates()
        x = 0
        while len(adv_pat_bigrams) < min(bigram_k, len(bdf)):
            x += 1
            next_ix = half_k + x

            try:
                next_entries = [top_by_metric[0].iloc[[next_ix], :],
                                top_by_metric[1].iloc[[next_ix], :]]
            except IndexError:
                print(f'All bigrams for {adv} retrieved.')
                break
            else:
                adv_pat_bigrams = pd.concat((adv_pat_bigrams,
                                             *next_entries)).drop_duplicates()
        return adv_pat_bigrams.head(bigram_k)

    bigram_k = max(sample_size + 2, 10)
    print(f'## Top {bigram_k} "most negative" bigrams',
          f'corresponding to top {sample_size} adverbs\n')
    print(timestamp_today())
    patterns = list(bigram_dfs.keys())
    top_adverbs = C.index
    bigram_samples = {adv: dict.fromkeys(
        patterns + ['both', 'adj']) for adv in top_adverbs}
    bigrams, adj = [], []

    for rank, adv in enumerate(top_adverbs, start=1):
        print(f'\n### {rank}. _{adv}_\n')
        adj_for_adv = []
        adv_top = None

        for pat, bdf in bigram_dfs.items():
            bdf = adjust_am_names(
                bdf.loc[:, [
                    c for c in bdf.columns
                    if c in set(focus_cols + ADX_COLS)]
                ])
            bdf = bdf.loc[bdf.LRC >= 1, :]
            adv_pat_bigrams = (get_top_bigrams(bdf, adv, bigram_k)
                               .filter(adjust_am_names(focus_cols + ADX_COLS)))

            if adv_pat_bigrams.empty:
                print(f'No bigrams found in loaded `{pat}` AM table.')
            else:
                print(f'\n#### Top {len(adv_pat_bigrams)} `{pat}` "{adv}_*"',
                      f'bigrams (sorted by `{selector}`; `LRC > 1`)\n')
                column_list = column_list or adv_pat_bigrams.columns.to_list()
                nb_show_table(adv_pat_bigrams.filter(column_list)
                              .filter(regex=r'^[^a]|_total$'),
                              n_dec=2)

            adj_for_adv.extend(adv_pat_bigrams.adj.drop_duplicates().to_list())
            bigram_samples[adv][pat] = adv_pat_bigrams
            if adv_top is None:
                adv_top = adv_pat_bigrams
            else:
                adv_top = pd.concat([df.fillna('')
                                    for df in (adv_top, adv_pat_bigrams)])

        bigram_samples[adv]['adj'] = set(adj_for_adv)
        bigrams.extend(adv_top.l2.drop_duplicates().to_list())
        adj.extend(adj_for_adv)
        bigram_samples[adv]['both'] = adv_top

    bigram_samples['bigrams'] = set(bigrams)
    bigram_samples['adj'] = set(adj)
    return bigram_samples, bigram_k


# def uncat(df):
#     cats = df.select_dtypes('category').columns
#     df[cats] = df[cats].astype('string')
#     # print(df.dtypes)
#     return df, cats


def combine_top_adv(df_1: pd.DataFrame,
                    name_1: str,
                    df_2: pd.DataFrame,
                    name_2: str,
                    adv_am_paths,
                    data_tag: str = 'ALL',
                    env_filter: str = 'NEG',
                    filter_items: list = FOCUS,
                    set_floor: int = 5000,

                    k: int = 10) -> pd.DataFrame:

    def _fill_empties(name_1, name_2, both, loaded_paths, adv_set):

        def load_backup(
            adv_set: set,
            lower_floor: int = None,
            loaded_path: Path = adv_am_paths['RBdirect'],
        ) -> pd.DataFrame:
            lower_floor = lower_floor or round(
                set_floor//3, (-2 if set_floor//3 > 100 else -1))
            located_paths = tuple(loaded_path.parent.glob(
                f'{data_tag}*min{lower_floor}x*parq'))
            try:
                backup_path = located_paths[0]
            except IndexError:
                try:
                    backup_path = tuple(loaded_path.parent.glob(
                        f'*{data_tag}*min5x*parq'))[0]
                except IndexError as e:
                    raise FileNotFoundError(
                        'Error. Backup data not found. [in fill_empties()]') from e

            backup_df = pd.read_parquet(backup_path, columns=FOCUS, filters=[
                                        ('l2', 'in', adv_set)])

            backup_df = backup_df.filter(
                like='NEG', axis=0).reset_index().set_index('l2')
            backup_df.index.name = 'adv'

            return backup_df

        for name in (name_1, name_2):
            name = name.strip('_')
            path = loaded_paths['RBdirect'] if name == 'SET' else loaded_paths['mirror']
            if any(both[f'f_{name}'].isna()):

                floor = 10
                neg_backup = load_backup(
                    lower_floor=floor, loaded_path=path, adv_set=adv_set)

                neg_backup.columns = (pd.Series(adjust_am_names(neg_backup.columns)
                                                ) + f'_{name}').to_list()
                both, cats = catify(both, reverse=True)
                neg_backup, __ = catify(neg_backup, reverse=True)

                undefined_adv = both.loc[
                    both[f'f_{name}'].isna(), :].index.to_list()

                both.loc[undefined_adv,
                         neg_backup.columns] = neg_backup.filter(items=undefined_adv, axis=0)

                both[cats] = both[cats].astype('category')

        return both

    def _add_f_ratio(df, subset_name, superset_name):
        counts = df.filter(regex=r'^[Nf][12]?').columns.str.split(
            '_').str.get(0).drop_duplicates()
        for count in counts:
            ratio_col = f'ratio_{count}{subset_name}'
            df[ratio_col] = (df[f'{count}{subset_name}']
                             / df[f'{count}{superset_name}'])
            # print(df.filter(like=count))
        return df

    def _add_means(both):
        for metric in (both.select_dtypes(include='number').columns.to_series()
                       .str.replace(r'_(MIR|SET)$', '', regex=True).unique()):
            both[f'mean_{snake_to_camel(metric)}'] = both.filter(
                regex=f"^{metric}").agg('mean', axis='columns')
        return both

    def _narrow_selection(df: pd.DataFrame,
                          top_adv: list,
                          env_filter: str = 'NEG',
                          filter_items: list = FOCUS):
        df = adjust_am_names(
            df.filter(items=filter_items)
            .filter(like=env_filter, axis=0)
            .reset_index().set_index('l2')
            .filter(top_adv, axis=0)).sort_values(['LRC', 'dP1'], ascending=False)
        df.index.name = 'adv'
        nb_show_table(df.drop(['N', 'key', 'l1'], axis=1).round(
            2).sort_values(['LRC', 'dP1', ], ascending=False))

        return df

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    print(f'### `{data_tag}` Most Negative Adverb Selections')
    top_dfs = [
        (get_top_vals(adv_df,  k=k,
                      index_like=env_filter,
                      metric_filter=['am_p1_given2',
                                     'conservative_log_ratio'])
         .sort_values('conservative_log_ratio', ascending=False))
        for adv_df in [df_1, df_2]
    ]
    for i, name in enumerate([name_1, name_2]):

        print_iter(
            [f'_{w}_' for w in top_dfs[i].l2], bullet='1.',
            header=(f'`{name}`: union of top {k} adverbs ranked by '
                    r'$LRC$ & $\Delta P(\texttt{env}|\texttt{adv})$'))
    top_adv_lists = [dx.l2.to_list() for dx in top_dfs]
    top_adv = pd.Series(top_adv_lists[0] + top_adv_lists[1]).drop_duplicates()
    # top_adv = pd.concat((top_dfs[0].l2, top_dfs[1].l2)).drop_duplicates()

    print_iter(
        [f'_{w}_' for w in top_adv], bullet='1.',
        header=f'Union of top adverbs for `{name_1}` and `{name_2}`. (Novel `{name_2}` adverbs listed last)')
    print(f'\n### `{name_1}` Adverb Associations (in initially loaded table)\n')
    df_1 = _narrow_selection(df_1, top_adv, env_filter, filter_items)
    print(f'\n### `{name_2}` Adverb Associations (in initially loaded table)\n')
    df_2 = _narrow_selection(df_2, top_adv, env_filter, filter_items)

    name_1, name_2 = [f"_{n.strip('_')}" for n in [name_1, name_2]]
    both = df_1.join(df_2, how="outer", lsuffix=name_1, rsuffix=name_2)

    # ! Empty cells need to be filled _before_ calculating mean
    both = _fill_empties(name_1, name_2, both,
                         adv_am_paths, adv_set=set(top_adv))
    both = force_ints(both)
    both = _add_means(both)
    both = _add_f_ratio(both, name_2, name_1)
    return both.sort_values('mean_dP1', ascending=False)


def compare_datasets(adv_am,
                     metric_selection: str or list = 'dP1',
                     k=5):
    if isinstance(metric_selection, str):
        met_adv_am = adv_am.filter(like=metric_selection)
    else:
        met_adv_am = adv_am.filter(regex=r'|'.join(
            [f'^{m}|mean_{m}' for m in metric_selection]))
    if met_adv_am.empty:
        met_adv_am = adjust_am_names(adv_am).filter(metric_selection)
    if any(met_adv_am.columns.str.startswith('r_')):
        is_ratio = met_adv_am.columns.str.startswith('r_')
        met_adv_am.loc[:, is_ratio] = met_adv_am.loc[:, is_ratio] * 100
        met_adv_am.columns = met_adv_am.columns.str.replace('r_', '%_')
    for col in met_adv_am.columns:
        n_dec = 2
        if 'P' in col:
            n_dec = 3
        elif 'G' in col or '%' in col:
            n_dec = 1
        elif 'f' in col and not col.startswith(('r_', '%_', 'mean_')):
            n_dec = 0
            # col = col.replace('r_', '%_')
        print(f'Top {k} by descending `{col}`')
        print(met_adv_am.nlargest(k, col).to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=','), '\n')


def pin_top_adv(adv_am,
                select_col='mean_dP1',
                verbose: bool = True):

    sorted_adv_am = adv_am.sort_values(select_col, ascending=False)
    top = sorted_adv_am.index.to_series()
    if verbose:
        print_df = sorted_adv_am[select_col].reset_index()
        print_df.index = print_df.index.to_series().add(1)
        print(
            f'Top Adverb Selection, ranked by descending `{repr(select_col)}`',
            print_df.to_markdown(floatfmt=',.3f'),
            sep='\n\n', end='\n\n'
        )
    return top.to_list(), sorted_adv_am

# * bigram-composition


def load_hit_table(adv_set, pos_hits, neg_hits, tag_top_dir, adv_floor):

    out_path = tag_top_dir.joinpath(
        f'{tag_top_dir.name}adv_sample-hits_{timestamp_today()}.parq')
    if not out_path.exists():

        dfs = []
        for pol, path in {'pos': pos_hits, 'neg': neg_hits}.items():
            _df = pd.read_parquet(
                path, engine='pyarrow',
                filters=[('adv_form_lower', 'in', adv_set)])
            _df = _df.filter(['token_str', 'text_window', 'all_forms_lower',
                              'bigram_lower', 'adv_form_lower', 'adj_form_lower', 'neg_lemma'])
            if 'all_forms_lower' not in _df.columns:
                if pol == 'pos':
                    _df = _df.assign(
                        all_forms_lower='(+)_' + _df.bigram_lower,
                        neg_lemma='')
                else:
                    _df['all_forms_lower'] = (
                        _df.neg_form_lower + '_' + _df.bigram_lower)
            _df = catify(_df, reverse=True).drop_duplicates('text_window')
            dfs.append(_df.assign(polarity=pol))

        hit_df = catify(pd.concat(dfs).drop_duplicates('text_window'))
        parq_it(hit_df,
                data_label='Sample of bigram tokens',
                part=f'{tag_top_dir.name}[{adv_floor}]',
                out_path=out_path,
                partition_by=['adv_form_lower'])
    else:
        hit_df = pd.read_parquet(
            out_path, engine='pyarrow',
            filters=[('adv_form_lower', 'in', adv_set)])
        hit_df = catify(
            hit_df
            .drop_duplicates('text_window').filter(
                regex=r'token_str|text_window|bigram_lower|adv_form_lower|adj_form_lower'))

    return hit_df


# def collect_examples(amdf,
    #                  hits_df,
    #                  adv: str = 'exactly',
    #                  n_bigrams: int = 10,
    #                  n_examples: int = 50,
    #                  metric: str = 'LRC') -> dict:
    # df = amdf.copy().filter(like=adv, axis=0).nlargest(n_bigrams, metric)
    # examples = {}
    # for i, adj in enumerate(df['l2'].unique(), start=1):
    #     bigram = f'{adv}_{adj}'
    #     print(f'\n{i}. {bigram}')
    #     examples[bigram] = sp(
    #         data=hits_df, print_sample=False,
    #         sample_size=n_examples, quiet=True,
    #         filters=[f'bigram_lower=={bigram}'],
    #         columns=['bigram_lower', 'text_window', 'token_str'])
    #     print('   > ', examples[bigram].sample(1).token_str.squeeze())
    # return examples


def sample_adv_bigrams(adverb: str,
                       data_tag: str,
                       amdf: pd.DataFrame,
                       hits_df: pd.DataFrame,
                       n_top_bigrams: int = 10,
                       verbose: bool = False,
                       bigram_floor: int = 50):
    print(f'\n## *{adverb}*\n')
    output_dir = TOP_AM_DIR / data_tag / 'any_bigram_examples' / adverb
    confirm_dir(output_dir)

    this_adv_am = catify(
        amdf.filter(like=adverb, axis=0)
        .nlargest(n_top_bigrams,
                  columns=METRIC_PRIORITY_DICT[data_tag][:2]),
        reverse=True
    )
    table_csv_path = output_dir.joinpath(
        f'{data_tag}-{adverb}_top{n_top_bigrams}-bigrams-{bigram_floor}_AMscores_{timestamp_today()}.csv')
    this_adv_am.to_csv(table_csv_path)

    nb_show_table(this_adv_am, n_dec=2,
                  outpath=table_csv_path.with_suffix('.md'))
    n_ex = int(n_top_bigrams * 8)
    # examples = collect_examples(this_adv_am, hits_df, adv=adverb, metric='LRC')
    examples = collect_adv_bigram_ex(
        amdf=this_adv_am, hits_df=hits_df, adv=adverb,
        metric_selection=METRIC_PRIORITY_DICT[data_tag][:2],
        n_examples=n_ex, n_bigrams=n_top_bigrams,
        verbose=verbose, output_dir=output_dir)

    print(f'\nSaving Samples in {output_dir}/...')
    paths = []
    for key, df in examples.items():
        out_path = output_dir.joinpath(f'{key}_{n_ex}ex~{len(df)}.csv')
        if out_path.is_file() and not len(df) < n_ex:
            alt_dir = output_dir.joinpath('alt_ex')
            run_shell_command(f'echo "Renaming existing sample..."; mkdir -p "{alt_dir}"; '
                              f'mv -v --backup=numbered "{out_path}" "{alt_dir}/" ; '
                              f'bash /share/compling/projects/tools/datefile.sh "{alt_dir}/{out_path.name}" -r ')
        df.to_csv(out_path)
        paths.append(out_path)
    print_iter(paths, header='\nSamples saved as...', bullet='+')

# * bigram-polarity


def collect_adv_bigram_ex(amdf: pd.DataFrame,
                          hits_df: pd.DataFrame,
                          adv: str = 'exactly',
                          n_bigrams: int = 10,
                          n_examples: int = 50,
                          verbose: bool = False,
                          output_dir: Path = None,
                          metric_selection: str | list = ['dP1', 'LRC']) -> dict:
    if not any(amdf.l2.str.contains('_')):
        n_unique_adv = amdf.l1.nunique()
        bigrams = (amdf.l1 + '_' + amdf.l2).unique()
    else:
        n_unique_adv = amdf.adv.nunique()
        bigrams = amdf.l2.unique()

    if n_unique_adv > 1:
        amdf = (amdf
                .filter(like=f'(?<=~|\b){adv}(?=_|~)',
                        axis=0)
                .nlargest(n_bigrams, columns=metric_selection))
    examples = {}
    for i, bigram in enumerate(bigrams, start=1):
        bigram_text = bigram.replace("_", " ")
        if verbose:
            print(f'\n### {i}. _{bigram_text}_\n')

        ex_for_bigram = sp(
            data=hits_df, print_sample=False, quiet=True,
            sample_size=n_examples,
            sort_by=hits_df.filter(
                ['all_forms_lower', 'bigram_lower']).columns.tolist()[0],
            filters=[f'bigram_lower=={bigram}'],
            columns=['END::lower', 'text_window', 'token_str'])
        excerpt = embolden(
            ex_for_bigram.sample(min(len(ex_for_bigram), 8))[
                'token_str'],
            bold_regex=f' ({bigram_text}) '
        ).to_frame()
        excerpt.index = '`'+excerpt.index.astype('string')+'`'
        # TODO: modify this to save markdown example table as file
        nb_show_table(excerpt, suppress_printing=not verbose,
                      outpath=output_dir.joinpath(f'{bigram}_ex.md'))
        # print('\n   > ', [f'> {}' for i in ex_for_bigram.sample(3).index])
        examples[bigram] = ex_for_bigram
    return examples


def populate_adv_dir(adverb: str,
                     bigram_am: pd.DataFrame,
                     hits_df: pd.DataFrame,
                     data_tag: str,
                     n_bigrams: int = 10,
                     n_ex: int = 50,
                     rank_by: str | list = ['dP1', "LRC"],
                     verbose: bool = False):
    output_dir = TOP_AM_DIR / data_tag / 'neg_bigram_examples' / adverb
    table_csv_path = output_dir / \
        f'{adverb}_{n_bigrams}mostNEG-bigrams_AMscores_{timestamp_today()}.csv'
    confirm_dir(output_dir)
    this_adv_amdf = bigram_am.filter(
        like=f'~{adverb}_', axis=0).sort_values(rank_by, ascending=False)
    this_adv_amdf.to_csv(table_csv_path)

    nb_show_table(this_adv_amdf.filter(['N', 'f1', 'adv_total'])
                  .set_index(this_adv_amdf.l1 + f'_{adverb}').drop_duplicates(),
                  n_dec=0,
                  outpath=output_dir /
                  f'{adverb}_MarginalFreqs_{timestamp_today()}.md',
                  suppress_printing=not verbose)

    nb_show_table((this_adv_amdf
                   .filter(regex=r'^([dLGeu]|f2?$|adj_total)')
                   .round(2)
                   .sort_values(rank_by, ascending=False)),
                  n_dec=2,
                  outpath=table_csv_path.with_suffix('.md'),
                  suppress_printing=not verbose)

    examples = collect_adv_bigram_ex(
        this_adv_amdf, hits_df, metric_selection=rank_by, n_examples=n_ex, verbose=verbose)

    print(f'\nSaving Samples in {output_dir}/...')

    paths = []
    for key, df in examples.items():
        out_path = output_dir.joinpath(f'{key}_{n_ex}ex.csv')
        df.to_csv(out_path)
        paths.append(out_path)

    if verbose:
        print_iter((f'`{p.relative_to(output_dir.parent.parent)}`' for p in paths),
                   header='\nSamples saved as...', bullet='1.')


def embolden(series,
             bold_regex=None):
    bold_regex = bold_regex or r" (n[o']t) "
    return series.apply(
        lambda x: re.sub(bold_regex,
                         r' __`\1`__ ', x, flags=re.I))


def seek_top_adv_am(date_str: str,
                    adv_floor: int,
                    tag_top_dir: Path,
                    tag_top_str: str = None
                    ) -> pd.DataFrame:
    if tag_top_str is None:
        tag_top_str = tag_top_dir.name
    adv_am = []
    while not any(adv_am):
        try:
            adv_am = pd.read_csv(
                tag_top_dir /
                f'{tag_top_str}_NEG-ADV_combined-{adv_floor}.{date_str}.csv',
                index_col='adv')
        except FileNotFoundError:
            date_str = day_before(date_str)

    adv_am = adjust_am_names(adv_am).convert_dtypes()
    return adv_am


def day_before(date_str):
    return date_str[:-1]+str(int(date_str[-1])-1)


def save_top_bigrams_overall_md(bigram_am: pd.DataFrame,
                                out_dir: Path,
                                metric_columns: list = None,
                                overall_k: int = 50,
                                adv_floor: int = 5000,
                                bigram_floor: int = 50,
                                suppress: bool = False):
    if 'LRC' not in bigram_am.columns:
        bigram_am = adjust_am_names(bigram_am)

    if metric_columns is None or not any(bigram_am.columns.isin(metric_columns)):
        metric_columns = bigram_am.filter(METRIC_PRIORITY_DICT[
            out_dir.name.split('-Top')[0]]).columns.to_list()
    if not any(metric_columns):
        metric_columns = bigram_am.columns.to_list()

    outpath = out_dir.joinpath(f'{out_dir.name}_NEG-ADV-{adv_floor}_'
                               + f'top{overall_k}bigrams-overall'
                               + f'.min{bigram_floor}.{timestamp_today()}.md')
    print(f'> Saving **Top Overall Bigrams** table as  \n>   `{outpath}`')
    nb_show_table(bigram_am.round(2).nlargest(overall_k, columns=metric_columns),
                  outpath=outpath,
                  suppress_printing=suppress)
