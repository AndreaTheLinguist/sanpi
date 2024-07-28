from pathlib import Path
from pprint import pprint

import pandas as pd

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

def locate_bigram_am_paths(data_tag, mirror_floor, bigram_floor):
    def floor(name):
        return mirror_floor if name.endswith("mirror") else bigram_floor
    paths_dict = {
        d.name: tuple(
            d.joinpath('bigram/extra').glob(
                f'*{data_tag}*min{floor(d.name)}x*extra.parq')
        )[0]
        for d in POLAR_DIR.iterdir()
    }
    pprint(paths_dict)
    return paths_dict


def load_bigram_dfs(bigram_am_paths):
    return {n: catify(update_index(pd.read_parquet(p)),
                      reverse=True)
            for n, p in bigram_am_paths.items()}


def force_ints(_df):
    count_cols = _df.filter(regex=r'total|^[fN]').columns
    _df[count_cols] = _df[count_cols].astype('int')
    # _df[count_cols] = _df[:, count_cols].astype('int64')
    # print(_df.dtypes.to_frame('dtypes'))
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
                adv_top = pd.concat([df.fillna('') for df in (adv_top, adv_pat_bigrams)])

        bigram_samples[adv]['adj'] = set(adj_for_adv)
        bigrams.extend(adv_top.l2.drop_duplicates().to_list())
        adj.extend(adj_for_adv)
        bigram_samples[adv]['both'] = adv_top

    bigram_samples['bigrams'] = set(bigrams)
    bigram_samples['adj'] = set(adj)
    return bigram_samples, bigram_k