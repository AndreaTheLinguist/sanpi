# coding=utf-8

# > Imports
import argparse
import statistics as stat
from pathlib import Path
from re import search

import pandas as pd
from utils import (cols_by_str, confirm_dir,  # pylint: disable=import-error
                   count_uniq, file_size_round, find_glob_in_dir,
                   get_proc_time, print_iter, print_md_table, save_table,
                   sort_by_margins, unpack_dict)
from utils.LexicalCategories import (  # pylint: disable=import-error
    SAMPLE_ADJ, SAMPLE_ADV)
from utils.visualize import heatmap  # pylint: disable=import-error

# > Globals
_SANPI_DIR = Path('/share/compling/projects/sanpi')
_DATA_DIR = Path('/share/compling/data/sanpi')


def _main():
    print(pd.Timestamp.now().ctime())

    (filtered_bigrams, hits_dir,
     frq_out_dir, frq_groups) = _parse_args()

    df = prepare_hit_table(
        filtered_bigrams,
        neg_hits_dir=hits_dir)

    _summarize_hits(df)

    if not frq_groups:
        frq_groups = ['all']

    for group in frq_groups:

        _t0 = pd.Timestamp.now()
        #! #[x] modify `get_freq_info` to deal with relevant negation data
        frq_df, frq_df_path = get_freq_info(file_tag=search(r'(th.+p).(\d{1,2}f)',
                                                            filtered_bigrams.name).group(),
                                            df=df, group=group, frq_out_dir=frq_out_dir)
        _t1 = pd.Timestamp.now()
        print('[ Time to process frequencies:', get_proc_time(_t0, _t1), ']')

        _describe_counts(frq_df, frq_df_path)


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-b',
        '--bigram_filter',
        type=Path,
        default=_DATA_DIR.joinpath(
            '4_post-processed/RBXadj/bigrams-only_thr0-1p.35f.pkl.gz'  # > 0.1% threshold
            # '4_post-processed/RBXadj/bigrams-only_thr0-01p.35f.pkl.gz' #> 0.01% threshold
            # '4_post-processed/RBXadj/bigrams-only_thr0-0005p.35f.pkl.gz' #> 0.0005% threshold
        ),
        help=('Path to table of all relevant bigrams: *all* bigrams found for the same corpora, '
              'with cleaning and frequency (of desired threshold) filtering applied.'
              ' as the current negative pattern matches to be "counted". '
              'This is to required to line up the negative environment data '
              'with the frequency filtering applied to the full collection of bigrams.'
              'Should be a pickled dataframe indexed by `hit_id` => negation data `colloc_id`). '))

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


def prepare_hit_table(bigram_hits: Path,
                      neg_hits_dir: Path):

    print('\n+ size of bigram hits table:',
          file_size_round(bigram_hits.stat().st_size))
    bigrams = pd.read_pickle(bigram_hits)
    if bigrams.index.name == 'hit_id':
        colloc_ids = bigrams.index
    else:
        colloc_ids = bigrams.hit_id

    _t0 = pd.Timestamp.now()
    print('\n## loading data...')
    filtered_neg_hits = bigram_hits.parent.joinpath(
        f'neg_compare/{bigram_hits.name.replace("bigrams-only", neg_hits_dir.name)}')
    if filtered_neg_hits.is_file():
        print(
            f'* Found previous output. Loading data from {filtered_neg_hits}...')
        df = pd.read_pickle(filtered_neg_hits).convert_dtypes()

    else:

        df = _load_data(ids=colloc_ids, data_dir=neg_hits_dir)
        if df.index.name != 'hit_id':
            df = df.set_index('hit_id')
        # print(f'\n> {len(df):,} initial hits')
        _print_uniq_lemma_count(df)
        print(_describe_str_lemma_counts(
            df).round().to_markdown(floatfmt=',.0f'))

        save_table(df,
                   str(filtered_neg_hits.resolve()).split('.pkl', 1)[0],
                   f"filtered {neg_hits_dir.name} hits")
        if len(df) < (10 ^ 6):
            save_table(df=df,
                       path_str=str(filtered_neg_hits.resolve()
                                    ).split('.pkl', 1)[0],
                       df_name=f"filtered {neg_hits_dir.name} hits",
                       formats=['psv', 'csv'])

        elif len(df) < (2 * 10 ^ 6):
            save_table(df=df,
                       path_str=str(filtered_neg_hits.resolve()
                                    ).split('.pkl', 1)[0],
                       df_name=f"filtered {neg_hits_dir.name} hits",
                       formats=['psv'])

    _t1 = pd.Timestamp.now()
    print('✓ time:', get_proc_time(_t0, _t1))
    return df


def _describe_str_lemma_counts(df: pd.DataFrame) -> pd.DataFrame:
    lemma_stats = (df.columns[df.columns.str.endswith('_lemma')]
                   .to_series().apply(
                       lambda c: df[c].value_counts().describe())
                   ).T
    lemma_stats.columns = lemma_stats.columns.str.replace('lemma', 'counts')
    return lemma_stats.round()


def _load_data(ids, data_dir: Path) -> pd.DataFrame:
    _ts = pd.Timestamp.now()
    df_iter = filter_hits(data_dir, ids)

    combined_df = pd.concat(df_iter)
    print_md_table(combined_df.describe().T.convert_dtypes(),
                   title='Combined Raw Hits Summary')

    _te = pd.Timestamp.now()
    print('> Time to create composite hits dataframe:',
          get_proc_time(_ts, _te))

    return combined_df


def filter_hits(data_dir: Path, ids: pd.Series):
    for i, p in enumerate(data_dir.glob('*hits.pkl.gz')):
        try:
            print_path = p.relative_to(Path("/share/compling/data"))
        except ValueError:
            print_path = p.resolve().relative_to(Path("/share/compling/projects"))

        print(f'\n{i+1}. ../{print_path}')
        print('   + size:', file_size_round(p.stat().st_size))

        df = pd.read_pickle(p)

        # > select relevant columns
        df = _select_columns(df)

        print('   + Before filtering to target bigrams only')
        desc_t = df.select_dtypes(
            exclude='object').describe().T.convert_dtypes()
        print_md_table(desc_t.sort_index(), n_dec=0, comma=True,
                       indent=5, title=f'({i+1}) `{p.stem}` summary')

        # > filter to kept bigrams
        #! categories need to be reverted to strings before filtering
        #!   and then redefine categories after rows are removed.
        #!   Otherwise, removed lemmas, etc. will persist as "empty" categories
        cat_cols = df.select_dtypes(include='category').columns
        df[cat_cols] = df[cat_cols].astype('string')
        df = df.loc[df.colloc_id.isin(ids), :]
        df[cat_cols] = df[cat_cols].astype('category')
        print('   + After filtering to target bigrams')
        print_md_table(df.select_dtypes(exclude='object').describe().T.convert_dtypes(),
                       indent=5, title=f'({i+1}) `{p.stem}` summary')
        # HACK #^ not sure what I'm doing with this `flatten_deps` ... but wanted to save it
        # flatten_deps(input_path=p, df=df)
        #! temporarily commented out-- not sure if this is needed or not
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


def _select_columns(df):
    cols = ['colloc_id', 'token_str', 'category']
    cols.extend(df.columns[df.columns.str.endswith(
        ('lemma', 'form', 'window'))].to_list())
    cols.extend(
        df.columns[df.columns.str.startswith(('dep', 'pat'))].to_list())

    sdf = df[cols]
    if 'pattern' in cols:
        sdf = sdf.assign(pattern=df.pattern.astype('category'))
    pre_adv_ix = df.adv_index - 1
    word_between_id = df.index[df.neg_index != pre_adv_ix]
    # post_adj_ix = df.adj_index + 1
    sdf.loc[word_between_id,
            'pre_adv_lemma'] = word_between_id.to_series().apply(
                lambda i: df.lemma_str[i].split()[pre_adv_ix[i]])
    return sdf.assign(pre_adv_lemma=sdf.pre_adv_lemma.astype('category'))


def _print_uniq_lemma_count(df: pd.DataFrame,
                            cols=None,
                            updated: bool = True,
                            label: str = '',
                            head_mark: str = ''):
    if not label:
        label = 'updated' if updated else 'initial'
    if not head_mark:
        head_mark = '+' if updated else '='
    if not cols:
        cols = df.columns[df.columns.str.endswith('_lemma')]
    counts_info = {
        c.replace('_lemma', '').upper(): count_uniq(df[c])
        for c in cols
    }
    str_len = len(max(counts_info.keys()))
    num_len = len(str(max(counts_info.values()))) + 1
    counts = ['{0:<{1}s}:  {2:>{3},d}'.format(k, str_len, v, num_len)  # pylint: disable=consider-using-f-string
              for k, v in counts_info.items()]
    print_iter(counts,
               header=f'{head_mark} unique lemmas in {label} hits',
               indent=2)


def _summarize_hits(df):
    lemma_counts_summ = _describe_str_lemma_counts(df)
    tok_thresh_c = int(lemma_counts_summ.loc['min', :].min())
    print(f'    ⇟ minimum hits/lemma in data: {tok_thresh_c:,}')
    print_md_table(df.describe().T, indent=2,
                   title='Frequency Filtered Hits Summary')
    print_md_table(lemma_counts_summ, indent=2,
                   title='Frequency Filtered Lemma Distributions')


def get_freq_info(df: pd.DataFrame,  
                  group: str,
                  frq_out_dir: Path,
                  file_tag: str) -> tuple:
    print(f'\n## Processing Frequency data for {group} lemmas.')
    if group != 'all':
        frq_out_dir = frq_out_dir.joinpath(group)
    confirm_dir(frq_out_dir)
    
    #> these values have to be inherited from the
    #> bigram frequency filtering used to select negated hits
    frq_out_stem = get_freq_out_stem(file_tag, group)
    
    #> method returns `None` if stem not found
    frq_df_path = find_glob_in_dir(frq_out_dir, f'*{frq_out_stem}*csv')

    #> if crosstabulated frequency table is found
    if frq_df_path:
        print(f'\n* frequency table ({group}) found.')
        frq_df = _load_frq_table(frq_df_path)
        
    #> if frequency table is not found;
    #>   i.e. `f` call returned None
    else:
        frq_df_path = frq_out_dir.joinpath(frq_out_stem + '.csv')
        #> sanity check
        if not frq_df_path.name.endswith('f.csv'):
            exit(f'frequency path error: {frq_df_path}')
        frq_df = _build_frq_df(df, frq_df_path, group)
    return frq_df, frq_df_path


def get_freq_out_stem(freq_meta_tag: str, group_code):
    return f'{group_code}-frq_{freq_meta_tag}'


def _load_frq_table(frq_df_path):
    print(f'  Loading from ../{frq_df_path.relative_to(_SANPI_DIR)}...')
    if frq_df_path.suffix.endswith('csv'):
        frq_df = pd.read_csv(frq_df_path)
        frq_df.columns = frq_df.columns.str.strip()
    elif '.pkl' in frq_df_path.suffixes:
        frq_df = pd.read_pickle(frq_df_path)

    if 'adj_lemma' in frq_df.columns:
        frq_df = frq_df.set_index('adj_lemma')
    frq_df.columns.name = 'adv_lemma'
    return frq_df


def _build_frq_df(df: pd.DataFrame,
                  frq_df_path: Path,
                  group_code: str,
                  ) -> pd.DataFrame:
    # ! #[ ]: modify this method to run on `*_form.str.lower()` instead of `*_lemma`
    # ^ #[ ]: also modify to have nodes to crosstab as arguments so it can be run for multiple different combinations
    rdf = df

    if group_code.lower() != 'all':
        J, __ = unpack_dict(SAMPLE_ADJ)
        R, __ = unpack_dict(SAMPLE_ADV, values_name='adv')
        rdf = df.loc[df.adj_lemma.isin(J)
                     & df.adv_lemma.isin(R), :].astype('string')
    _t0 = pd.Timestamp.now()
    frq_df = pd.crosstab(index=rdf.adj_lemma,
                         columns=rdf.adv_lemma,
                         margins=True,
                         margins_name='SUM')

    _t1 = pd.Timestamp.now()
    print(f'[ Time to crosstabulate frequencies: {get_proc_time(_t0, _t1)} ]')

    frq_df = sort_by_margins(frq_df, margins_name='SUM')
    title = (f'{group_code} adj ✕ adv frequency table'
             .replace('JxR', 'scale diagnostics'))
    save_table(frq_df,
               str(frq_df_path),
               title, formats=['csv'])
    return frq_df


def _describe_counts(df: pd.DataFrame,
                     df_path: str) -> None:
    data_label = df_path.name.replace('.csv', '')
    stats_dir = df_path.parent.joinpath('descriptive_stats')
    confirm_dir(stats_dir)
    out_path_stem = f'stats_{data_label}'
    df = df.fillna(0)
    most_var_adv = df.columns.to_list()[1:21]
    most_var_adj = df.index.to_list()[1:21]
    for frame, pos in ((df, 'Adverb'), (df.transpose(), 'Adjective')):

        print(f'\n## Descriptive Statistics by {pos}')
        no_sum_frame = frame.loc[frame.index != 'SUM', frame.columns != 'SUM']
        desc_no_sum = no_sum_frame.describe()
        # > need to exclude the ['SUM','SUM'] cell
        sum_col = frame.loc[frame.index != 'SUM', 'SUM']
        desc_sum = sum_col.describe().to_frame()

        for desc, values in [(desc_no_sum, no_sum_frame), (desc_sum, sum_col)]:
            desc = _enhance_descrip(desc, values)
            if 'SUM' in desc.index:
                desc = desc.transpose()
                desc.columns = [f'Summed Across {pos}s']
                print_md_table(desc.round(), title=' ')
            else:
                save_table(
                    desc,
                    f'{stats_dir}/{pos[:3].upper()}-{out_path_stem}',
                    f'{pos} descriptive statististics for {out_path_stem}',
                    ['csv'])
                print_md_table(desc.sample(6).round(),
                               title=f'Sample {pos} Stats ')

                #[ ] # ?  add simple output of just `df.var_coeff`?
                # desc.info()
                if pos == 'Adverb':
                    most_var_adv = _select_lemmas(desc)
                else:
                    most_var_adj = _select_lemmas(desc)

    _visualize_counts(df.loc[['SUM'] + most_var_adj,
                      ['SUM'] + most_var_adv], df_path)


def _enhance_descrip(desc: pd.DataFrame,
                     values: pd.Series) -> pd.DataFrame:
    desc = desc.transpose()
    desc = desc.assign(total=values.sum(),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'])
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    if 'SUM' not in desc.index:
        desc = desc.assign(
            plus1_geo_mean=values.add(1).apply(stat.geometric_mean),
            plus1_har_mean=values.add(1).apply(stat.harmonic_mean))
    for col in desc.columns:
        if col in ('mean', 'std', 'variance', 'coeff_var'):
            desc.loc[:, col] = pd.to_numeric(desc[col].round(2),
                                             downcast='float')
        else:
            desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    return desc


def _select_lemmas(desc: pd.DataFrame, metric='var_coeff', largest=True) -> list:
    nth = len(desc) // 6
    trim = int(len(desc) * 0.01)
    desc_interior = desc.sort_values('mean').iloc[trim:-trim, :]
    top_means_metric = desc.loc[
        (desc['mean'] > (desc_interior['mean'].median() * .75))
        &
        (desc.total > (desc_interior['total'].median() * .75)), metric]
    # ? Is the following just temporarily commented out or fully obsolete ⬇️
    # info_list = []
    # for label, desc_df in {'interior': desc.iloc[5:, :], 'full': desc}.items():
    # top_means = desc_df.loc[
    #     (desc_df['mean'] > (desc_df['mean'].median() + 0.5 * 1))
    #     &
    #     (desc_df.total > (desc_df.total.median() * 1.1))
    #     , [metric, 'mean', '50%', 'total', 'max', 'range']]
    # info = top_means.describe()
    # info.columns = info.columns.astype('string') + f'_{label}'
    # info_list.append(info)
    # print_md_table(info_list[0].join(info_list[1]).sort_index(axis=1).round(0),
    #                title='Compare descriptive stats')
    if largest:
        lemmas = top_means_metric.squeeze().nlargest(nth).index.to_list()
    else:
        lemmas = top_means_metric.squeeze().nsmallest(nth).index.to_list()
    return lemmas


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
