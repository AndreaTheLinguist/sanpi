from pathlib import Path
from pprint import pprint

import pandas as pd
import pyarrow as pyar
from source.utils.associate import POLAR_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import update_assoc_index as update_index
from source.utils.general import (confirm_dir, print_iter, snake_to_camel,
                                  timestamp_today)
FOCUS = ['f',
         'am_p1_given2', 'am_p1_given2_simple',
         'conservative_log_ratio',
         'am_log_likelihood',
         'mutual_information',
         'am_odds_ratio_disc', 't_score',
         'N', 'f1', 'f2', 'E11', 'unexpected_f',
         'l1', 'l2',
         'adv', 'adv_total', 'adj', 'adj_total']


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

    pprint(am_paths)
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
                 metric_filter: str | list = ['am_p1_given2', 'conservative_log_ratio'],
                 k: int = 10,
                 val_col: str = None,
                 ignore_neg_adv: bool = True):
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
                      k:int=15, 
                      filter_and_sort:list=['conservative_log_ratio', 
                                            'am_log_likelihood', 
                                            'am_p1_given2']):
    
    _l1 = adv_df.filter(like='O', axis=0).l1.iat[0].lower().strip()
    _N = int(adv_df.N.iat[0])
    ie = '(`set_diff`, $*\complement_{N^+}$)' if _l1.startswith("com") else '(`mirror`, $@P$)'
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
            ).round(2).sort_values(filter_and_sort, ascending=False).set_index('l2').drop(['N', 'l1'], axis=1)
    )



def force_ints(_df):
    count_cols = _df.filter(regex=r'total|^[fN]').columns
    _df[count_cols] = _df[count_cols].astype('int')

    return _df


def nb_show_table(df, n_dec: int = 2,
                  adjust_columns: bool = True,
                  outpath: Path = None,
                  return_df: bool = False) -> None:
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
        _df = adjust_assoc_columns(_df)
    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index]
    table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    if outpath:
        outpath.write_text(table)

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
    print(
        f'## Top {bigram_k} "most negative" bigrams corresponding to top {sample_size} adverbs\n')
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
            bdf = adjust_assoc_columns(
                bdf[[c for c in set(focus_cols + ['adj', 'adj_total', 'adv', 'adv_total']) if c in bdf.columns]])
            bdf = bdf.loc[bdf.LRC >= 1, :]
            adv_pat_bigrams = get_top_bigrams(bdf, adv, bigram_k)

            if adv_pat_bigrams.empty:
                print(f'No bigrams found in loaded `{pat}` AM table.')
            else:
                print(
                    f'\n#### Top {len(adv_pat_bigrams)} `{pat}` "{adv}_*" bigrams (sorted by `{selector}`; `LRC > 1`)\n')
                column_list = column_list if column_list is not None else bdf.columns
                nb_show_table(adv_pat_bigrams.filter(column_list), n_dec=2)

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
                data_tag:str='ALL',
                env_filter: str = 'NEG',
                filter_items: list = FOCUS,
                k: int = 10) -> pd.DataFrame:

    def _fill_empties(name_1, name_2, both, loaded_paths, adv_set):

        def load_backup(
                        adv_set:set,
            lower_floor: int = None,
                        loaded_path: Path = adv_am_paths['RBdirect'], 
                        ) -> pd.DataFrame:
            lower_floor = lower_floor or round(SET_FLOOR//3, (-2 if SET_FLOOR//3 > 100 else -1))
            located_paths = tuple(loaded_path.parent.glob(
                f'{data_tag}*min{lower_floor}x*parq'))
            try:
                backup_path = located_paths[0] 
            except IndexError: 
                try:
                    backup_path = tuple(loaded_path.parent.glob(f'*{data_tag}*min5x*parq'))[0]
                except IndexError as e: 
                    raise FileNotFoundError('Error. Backup data not found. [in fill_empties()]') from e
            
            backup_df = pd.read_parquet(backup_path, columns=FOCUS, filters=[('l2', 'in', adv_set)])

            backup_df = backup_df.filter(like='NEG', axis=0).reset_index().set_index('l2')
            backup_df.index.name = 'adv'
            
            return backup_df

        for name in (name_1, name_2):
            name = name.strip('_')
            path = loaded_paths['RBdirect'] if name == 'SET' else loaded_paths['mirror']
            if any(both[f'f_{name}'].isna()):

                floor = 10
                neg_backup = load_backup(lower_floor=floor, loaded_path=path, adv_set=adv_set)

                neg_backup.columns = (pd.Series(adjust_assoc_columns(neg_backup.columns)
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
        df = adjust_assoc_columns(
            df.filter(items=filter_items)
            .filter(like=env_filter, axis=0)
            .reset_index().set_index('l2')
            .filter(top_adv, axis=0)).sort_values(['LRC', 'dP1'], ascending=False)
        df.index.name = 'adv'
        nb_show_table(df.drop(['N', 'key', 'l1'], axis=1).round(
            2).sort_values(['LRC', 'dP1', ], ascending=False))

        return df
    
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     
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
    both = _fill_empties(name_1, name_2, both, adv_am_paths, adv_set=set(top_adv))
    both = force_ints(both)
    both = _add_means(both)
    both = _add_f_ratio(both, name_2, name_1)
    return both.sort_values('mean_dP1', ascending=False)
