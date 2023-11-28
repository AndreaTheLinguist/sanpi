# coding=utf-8
import re
from pathlib import Path
from typing import Union

# import statistics as stat
import pandas as pd
from scipy import stats

try:
    from utils.dataframes import cols_by_str, print_md_table, save_table
    from utils.general import confirm_dir, print_iter
    from utils.visualize import visualize_counts
except ModuleNotFoundError:
    from source.utils.dataframes import cols_by_str, print_md_table, save_table
    from source.utils.general import confirm_dir, print_iter
    from source.utils.visualize import visualize_counts

PKL_SUFF = '.pkl.gz'
SANPI_DIR = Path('/share/compling/projects/sanpi')
DATA_DIR = Path('/share/compling/data/sanpi')

REGEX_CORP_FROM_HIT = re.compile(
    r'^(nyt)_eng_(\d)|^(apw)|^(pcc)_eng_(\w{2})'
)


# def add_form_lower(df: pd.DataFrame,
#                     pull_prev: bool = True):
#     if ('adv_form_lower' not in df.columns
#             or 'adj_form_lower' not in df.columns):
#         forms = cols_by_str(df, end_str='form')
#         df[[f'{f}_lower' for f in forms]] = df[forms].apply(
#             lambda f: f.str.lower())
#     if 'bigram_lower' not in df.columns:
#         df['bigram_lower'] = (df.adv_form_lower + '_' + df.adj_form_lower)
#     if pull_prev and ('prev_form_lower' not in df.columns):
#         try:
#             ingredients = df[['adv_index', 'token_str']]
#         except KeyError:
#             print('Warning: `adv_index` and `token_str` are',
#                   'required to generate `prev_form_lower`:',
#                   'column not added.')
#         else:
#             df['prev_form_lower'] = ingredients.apply(
#                 _add_prev, axis=1)
#     lower_cols = cols_by_str(df, end_str='lower')
#     df.loc[:, lower_cols] = df[lower_cols].astype('string')
#     return df
def add_form_lower(df: pd.DataFrame, pull_prev: bool = True):
    required_cols = ['adv_form_lower', 'adj_form_lower', 'bigram_lower']
    if not df.columns.isin(required_cols).all():
        forms = cols_by_str(df, end_str='form')
        df = df.assign(**{f'{f}_lower': df[f].str.lower() for f in forms})
        if 'bigram_lower' not in df.columns:
            df['bigram_lower'] = df['adv_form_lower'].str.cat(
                df['adj_form_lower'], sep='_')
    if pull_prev and 'prev_form_lower' not in df.columns:
        try:
            ingredients = df[['adv_index', 'token_str']]
        except KeyError:
            print('Warning: `adv_index` and `token_str` are required to generate `prev_form_lower`: column not added.')
        else:
            df['prev_form_lower'] = ingredients.apply(_add_prev, axis=1)
    df = df.astype('string')
    return df


def _add_prev(row):
    prev_ix = row['adv_index'] - 1
    return row['token_str'].split()[prev_ix].lower() if prev_ix >= 0 else ''



def load_dataframe(df_path: Path) -> pd.DataFrame:
    if ''.join(df_path.suffixes[-2:]) == PKL_SUFF:
        return pd.read_pickle(df_path)
    else:
        raise ValueError('File must be in pickle format.')


def save_and_print_stats(desc: pd.DataFrame, stats_dir: Path, param: str, out_path_stem: str):
    if 'SUM' in desc.index:
        desc = desc.transpose()
        desc.columns = [f'Summed Across {param}s']
        print_md_table(desc.round(), title=' ')
    else:
        save_table(
            desc,
            f'{stats_dir}/{param[:4].strip("_-").upper()}-{out_path_stem}',
            f'{param} descriptive statististics for {out_path_stem}',
            ['csv'])
        print_md_table(desc.sample(min(len(desc), 6)).round(),
                       title=f'Sample {param} Stats ')


def describe_counts(df: pd.DataFrame = None,
                    df_path: Path = None) -> None:
    # if not any(df):
    #     if df_path.name.endswith(PKL_SUFF):
    #         df = pd.read_pickle(df_path)
    #     else:
    #         print(
    #             'Stats can only be determined from a given path if indicated file is in pickle format.')
    #         return
    # data_label = df_path.name.replace('.csv', '').replace(PKL_SUFF, '')
    # stats_dir = df_path.parent.joinpath('descriptive_stats')
    # confirm_dir(stats_dir)
    # out_path_stem = f'stats_{data_label}'
    # df = df.fillna(0)
    # most_var_col = df.columns.to_list()[1:21]
    # most_var_row = df.index.to_list()[1:21]
    # for frame, ax in ((df, 'columns'), (df.transpose(), 'rows')):
    #     param = frame.columns.name
    #     print(
    #         f'\n## Descriptive Statistics for `{frame.index.name}` by `{param}`')
    #     no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
    #     desc_no_sum = no_sum_frame.describe()
    #     # > need to exclude the ['SUM','SUM'] cell
    #     sum_col = frame.loc[frame.index != 'SUM', 'SUM']
    #     desc_sum = sum_col.describe().to_frame()

    #     for desc, values in [(desc_no_sum, no_sum_frame), (desc_sum, sum_col)]:
    #         desc = enhance_descrip(desc, values)
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
    #             if ax == 'columns':
    #                 most_var_col = _select_word_sample(desc)
    #             else:
    #                 most_var_row = _select_word_sample(desc)

    # visualize_counts(df.loc[['SUM'] + most_var_row,
    #                         ['SUM'] + most_var_col], df_path)

    # > Sourcery Simplification:

    if df is None:
        df = load_dataframe(df_path)

    data_label = df_path.stem
    stats_dir = df_path.parent / 'descriptive_stats'
    confirm_dir(stats_dir)
    out_path_stem = f'stats_{data_label}'
    df = df.fillna(0)
    most_var_col = df.columns.to_list()[1:21]
    most_var_row = df.index.to_list()[1:21]

    param = df.columns.name
    print(f'\n## Descriptive Statistics for `{df.index.name}` by `{param}`')
    no_sum_frame = df.loc[df.index != 'SUM', df.columns != 'SUM']
    desc_no_sum = no_sum_frame.describe()
    sum_col = df.loc[df.index != 'SUM', 'SUM']
    desc_sum = sum_col.describe().to_frame()

    save_and_print_stats(desc_no_sum, stats_dir, param, out_path_stem)
    save_and_print_stats(desc_sum, stats_dir, param, out_path_stem)

    most_var_col = _select_word_sample(desc_no_sum)
    most_var_row = _select_word_sample(desc_no_sum.transpose())

    visualize_counts(df.loc[['SUM'] + most_var_row,
                     ['SUM'] + most_var_col], df_path)


def describe_str_adx_counts(df: pd.DataFrame,
                            transpose: bool = True) -> pd.DataFrame:
    # [ ] if certain input `df` will have columns: df[['adj_form_lower', 'adv_form_lower']], change `contains` to `endswith`
    word_stats = pd.DataFrame(df[c].value_counts().describe()
                              for c in cols_by_str(df, start_str='ad'))

    return word_stats.transpose() if transpose else word_stats


def enhance_descrip(desc: pd.DataFrame,
                    values: pd.Series) -> pd.DataFrame:
    # values.apply(pd.to_numeric, downcast='unsigned')
    # desc = desc.transpose()
    # desc = desc.assign(total=values.sum(),
    #                    var_coeff=desc['std'] / desc['mean'],
    #                    range=desc['max'] - desc['min'],
    #                    IQ_range=desc['75%'] - desc['25%'])
    # desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
    #                    lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    # if 'SUM' not in desc.index:
    #     # BUG: this sometimes crashes. believe it's due to different shaped tables
    #     #       changed it for the output, so that some get transposed and some don't,
    #     #       depending on the number of columns. but I can't remember where that
    #     #       is exactly. And this isn't that important. So, for now, just skipping it.
    #     try:

    #         desc = desc.assign(
    #             plus1_geo_mean=values.add(1).apply(stat.geometric_mean),
    #             plus1_har_mean=values.add(1).apply(stat.harmonic_mean))
    #     except TypeError:
    #         print('(fyi, geometric and harmonic means not added to stats)')
    # for col in desc.columns:
    #     if col in ('mean', 'std', 'variance', 'coeff_var'):
    #         desc.loc[:, col] = pd.to_numeric(desc[col].round(2),
    #                                          downcast='float')
    #     else:
    #         desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    # return desc
    
    #> Sourcery 
    values = pd.to_numeric(values, downcast='unsigned')
    desc = desc.transpose()
    desc['total'] = values.sum()
    desc['var_coeff'] = desc['std'] / desc['mean']
    desc['range'] = desc['max'] - desc['min']
    desc['IQ_range'] = desc['75%'] - desc['25%']
    desc['upper_fence'] = desc['75%'] + (desc['IQ_range'] * 1.5)
    desc['lower_fence'] = desc['25%'] - (desc['IQ_range'] * 1.5)
    
    if 'SUM' not in desc.index:
        try:
            desc['plus1_geo_mean'] = stats.gmean(values.add(1))
            desc['plus1_har_mean'] = stats.hmean(values.add(1))
        except TypeError:
            print('(fyi, geometric and harmonic means not added to stats)')
    
    numeric_cols = ['mean', 'std', 'variance', 'coeff_var']
    desc[numeric_cols] = desc[numeric_cols].apply(lambda x: pd.to_numeric(x.round(2), downcast='float'))
    desc[desc.columns.difference(numeric_cols)] = desc[desc.columns.difference(numeric_cols)].apply(pd.to_numeric, downcast='unsigned')
    
    return desc

def infer_count_floor(filtered_df: pd.DataFrame) -> int:
    return min(
        filtered_df[c].value_counts().min()
        for c in ('adv_form_lower', 'adj_form_lower')
    )


# def load_from_txt_index(data_dir: Path,
#                         check_point: tuple = None,
#                         index_txt_path: Path = None):
#> Sourcery:
def load_from_txt_index(data_dir: Path,
                        check_point: Union[None, tuple] = None,
                        index_txt_path: Union[None, Path] = None):
    #! reason for weird argument duplication → imported to `count_neg.py`
    #! even though both default to None, at least *one* is required.
    # if check_point:
    #     print(f'* Found existing {check_point.stage}ed `hit_id` index for',
    #           f'{check_point.nfiles} files{set_thresh_message(check_point)}.')
    #     index_txt_path = check_point.index_path

    # # table_selections = []
    # # for hit_table_path, _ids in :

    # # #[x] iter over each pickle and return df with matching indicated index
    # table_selections = (_load_selection(p, i) for (p, i) in locate_relevant_hit_tables(
    #     data_dir, index_txt_path))

    #> Sourcery:
    if check_point:
        print(f'* Found existing {check_point.stage}ed `hit_id` index for',
              f'{check_point.nfiles} files{set_thresh_message(check_point)}.')
        index_txt_path = check_point.index_path
    elif not index_txt_path:
        raise ValueError("Either check_point or index_txt_path must be provided.")

    table_selections = (_load_selection(p, i) for (p, i) in locate_relevant_hit_tables(
        data_dir, index_txt_path))
    return pd.concat(table_selections)

def locate_relevant_hit_tables(data_dir, index_txt_path):
    simple_dir = data_dir.joinpath('simple')

    # * Path variation info
    # hit_ids_gen = iter_hit_id_index(check_point.index_path)
    # for hit_id in hit_ids_gen:
    # > examples of hit_id values and corresponding source path
    # nyt_eng_19970307_0512_1:15-16
    #   -> f'{simple_dir}/S_bigram-Nyt1_rb-bigram_hits.pkl.gz'
    # nyt_eng_20051129_0028_3:46-47
    #   -> f'{data_dir}/bigram-Nyt2_rb-bigram_hits.pkl.gz'
    #   > if "simple" table not processed yet, will be in `data_dir`
    #   > *BUT* this should not be the case if `hit_id` is in the index file
    # apw_eng_20050211_0660_8:8-9
    #   -> f'{simple_dir}/S_bigram-Apw_rb-bigram_hits.pkl.gz'
    # pcc_eng_val_3.00133_x34743_29:4-5
    #   -> f'{simple_dir}/S_bigram-PccVa_rb-bigram_hits.pkl.gz'
    # pcc_eng_06_108.0002_x1730749_18:5-6
    #   -> f'{simple_dir}/S_bigram-Pcc06_rb-bigram_hits.pkl.gz

    hit_ids = pd.Series(index_txt_path.read_text().splitlines(),
                        dtype='string')
    for corpus_cue, _ids in hit_ids.groupby(
        hit_ids.apply(lambda hit_id: ''.join(
            g.capitalize() if g else ''
            for g in REGEX_CORP_FROM_HIT.search(hit_id).groups()))):

        glob_str = f'*bigram-{corpus_cue}*hit*s.{PKL_SUFF}'

        hit_paths = list(simple_dir.glob(glob_str))
        if not any(hit_paths):
            hit_paths = list(data_dir.glob(glob_str))
        for hit_path in hit_paths:
            yield hit_path, _ids


def _load_selection(t_path, load_index):
    return select_count_columns(
        pd.read_pickle(t_path).loc[load_index, :])


def _select_word_sample(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
    nth = len(desc) // 6
    trim = int(len(desc) * 0.01)
    desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    top_means_metric = desc.loc[
        (desc['mean'] > (desc_interior['mean'].median() * .75))
        &
        (desc.total > (desc_interior['total'].median() * .75)), metric]
    return (
        top_means_metric.squeeze().nlargest(nth).index.to_list()
        if largest
        else top_means_metric.squeeze().nsmallest(nth).index.to_list()
    )


def save_filter_index(index_path: Path, df: pd.DataFrame):
    if 'adj_form_lower' in df.columns and 'adv_form_lower' in df.columns:
        hit_id_index = (df.index if df.index.name == 'hit_id'
                        else df.hit_id).to_list()
        if index_path.is_file() and not set(index_path.read_text().splitlines()).difference(hit_id_index):
            print('* Filter index previously saved and does not differ from current index:',
                  f'    {index_path}', sep='\n')
            return

        label_verb = ("cleaning" if "clean" in index_path.stem
                      else "frequency filtering")

        print(f'* Saving list of all {len(hit_id_index)} bigram hit_id',
              f'values retained after {label_verb} as\n  + {index_path}')
        index_path.write_text('\n'.join(hit_id_index), encoding='utf8')

    return


def select_count_columns(df):
    # * create `NODE_form_lower` if it does not exist yet
    df = add_form_lower(df)

    if 'pattern' in df.columns:
        df.loc[:, 'pattern'] = df.pattern.astype('category')

    #! made this more inclusive because it's now accessed from `count_neg` via imports
    cols = (
        ['bigram_id', 'token_str', 'pattern', 'category']
        # targets: adv/adj/neg/nr/relay_lemma/form(_lower), text_window, neg/mod_head/deprel
        + cols_by_str(df, end_str=('lemma', 'form',
                      'lower', 'window', 'deprel', 'head'))
        # targets: any `dep_str_*` columns if input from `3_dep_info/`
        + cols_by_str(df, start_str='dep_str')
    )

    #! use `.isin()` to avoid potential KeyError
    return df.loc[:, df.columns.isin(
        (c for c in cols if not c.startswith('mod_')))]


def show_interim_summary(df: pd.DataFrame,
                         title: str = 'interim summary stats',
                         indent: int = 2,
                         cols_label: str = '',
                         iter_head_bullet: str = '',
                         raw: bool = False):
    print_uniq_counts(df, label=cols_label, raw=raw,
                      head_mark=iter_head_bullet)
    print_md_table(describe_str_adx_counts(df),
                   indent=indent, n_dec=1, title=title)


def print_uniq_counts(df: pd.DataFrame,
                      cols=None,
                      raw: bool = True,
                      label: str = '',
                      head_mark: str = ''):
    if not label:
        label = 'initial' if raw else 'updated'
    if not head_mark:
        head_mark = '=' if raw else '+'
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


def set_thresh_message(check_point):
    return (f' and {check_point.frq_thr}% threshold'
            if check_point.frq_thr
            else '')
