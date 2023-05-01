
from pathlib import Path
from sys import argv

import matplotlib.pyplot as plt
import pandas as pd
from LexicalCategories import PPI_ADVERBS, ADJ_BY_SCALE, ADV_OF_INTEREST


def determine_global_limits():
    try:
        input_1 = argv[1]
    except IndexError:
        n_files = 3
    else:
        n_files = int(input_1)

    try:
        input_2 = argv[2]
    except IndexError:
        n_hits = n_files * 200
    else:
        n_hits = int(input_2)
    return n_files, n_hits


def unpack_dict(input_dict: dict,
                values_name: str = 'adj',
                keys_name: str = 'type',
                return_df=False
                ):
    scale_df = (pd.Series(input_dict).to_frame().reset_index()
                .rename(columns={0: values_name, 'index': keys_name}))
    explodf = scale_df.explode(values_name).set_index(values_name)
    inv_flat_dict = explodf.to_dict()[keys_name]
    flat_unq_vals = tuple(set(inv_flat_dict.keys()))
    returns = (inv_flat_dict, flat_unq_vals)
    if return_df:
        returns += (explodf,)
    return returns


N_FILES, N_HITS = determine_global_limits()
N_EX = 3

SCALE_TYPES = ADJ_BY_SCALE.keys()

SCALE_DEFS, SCALE_ADJ = unpack_dict(ADJ_BY_SCALE, 'adj', 'scale_type')


def _main():

    print("Comparing Adverbs by Scale Type for:")
    print(" -", N_FILES, "files\n - frequency threshold of", N_HITS)
    text_csv_path = Path(
        f'/share/compling/projects/sanpi/notebooks/scale_comparison/out/scale-type_examples_{N_FILES}-{N_HITS}.csv')
    comp_index_csv_path = text_csv_path.with_stem(
        f'scalar_comparison-index_example.{N_FILES}-{N_HITS}')
    if not comp_index_csv_path.is_file():
        if not text_csv_path.is_file():

            print('\n## loading data...')
            df = load_data()
            rdf = restrict_data(text_csv_path, df)
        else:
            rdf = pd.read_csv(text_csv_path).convert_dtypes()

        rdf.describe()
        compare = compare_distributions(rdf, comp_index_csv_path)

    else:
        compare = pd.read_csv(
            comp_index_csv_path).convert_dtypes().set_index('adv_lemma')

    print('\n' + compare.round(3).to_markdown())

    visualize(text_csv_path, compare)


def get_proc_time(_t0: pd.Timestamp,
                  _t1: pd.Timestamp) -> str:
    t_comp = (_t1 - _t0).components
    time_str = (
        ":".join(str(c).zfill(2) for c
                 in (t_comp.hours, t_comp.minutes, t_comp.seconds))
        + f'.{round(t_comp.microseconds, 1)}')

    return time_str


def load_data():
    pkl_paths = select_pickles()
    _t0 = pd.Timestamp.now()
    df_list = []
    for p in pkl_paths:
        print(f'  + ../{p.relative_to(Path("/share/compling/data"))}')
        df = pd.read_pickle(p)
        df = constrain_data(df, SCALE_ADJ)
        df_list.append(df)
    loop_df = pd.concat(df_list)
    _t1 = pd.Timestamp.now()
    print('  > Time to create composite hits dataframe via loop:',
          get_proc_time(_t0, _t1))

    return loop_df


def constrain_data(df, target_adj):
    df = (df.loc[:, ['adv_lemma', 'adj_lemma', 'text_window', 'token_str', 'hit_text']]
          .astype('string'))
    df = df.loc[df.adj_lemma.isin(target_adj)
                & ~df.duplicated(['token_str', 'hit_text']), :]
    df.loc[:, 'adj_lemma'] = pd.Categorical(df.adj_lemma,
                                            categories=list(target_adj))

    return df


def select_pickles():
    pickle_dir = Path(
        '/share/compling/data/sanpi/2_hit_tables/advadj')
    # > make dataframe to load smallest files first (for testing)
    pkl_df = pd.DataFrame(pickle_dir.glob(
        'bigram-*hits.pkl.gz'), columns=['path'])
    pkl_df = pkl_df.assign(size=pkl_df.path.apply(lambda f: f.stat().st_size))
    pkl_paths = pkl_df.sort_values('size').head(N_FILES).reset_index().path
    return pkl_paths


def restrict_data(outdf_path, df):
    # > removing duplicates
    reduced_df = df.loc[~df.duplicated(['token_str', 'hit_text']), [
        'adv_lemma', 'adj_lemma', 'text_window']]
    adv_freq = reduced_df.adv_lemma.value_counts()
    key_freq = adv_freq.loc[adv_freq.index.isin(ADV_OF_INTEREST)]
    adverbs = (key_freq.loc[key_freq > N_HITS/3].index.to_list()
               + adv_freq.loc[(adv_freq > N_HITS)].index.to_list())
    adverbs = set(adverbs + PPI_ADVERBS)
    restricted_df = reduced_df.loc[reduced_df.adv_lemma.isin(adverbs), :]
    restricted_df = restricted_df.assign(scale_type=pd.Categorical(restricted_df.adj_lemma.apply(lambda a: SCALE_DEFS[a]),
                                                                   categories=SCALE_TYPES))
    restricted_df.to_csv(outdf_path)
    return restricted_df


def compare_distributions(df, outpath):
    # key_adv_found = set(df.loc[df.adv_lemma.isin(
    #     KEY_ADV_SOUGHT), 'adv_lemma'].to_list())

    scale_percents = df.value_counts('scale_type', normalize=True) * 100
    print('\n'
          + scale_percents.round(1).to_frame()
          .rename(columns={0: '% of selection'}).to_markdown()
          + '\n')

    adv_totals = df.value_counts('adv_lemma')
    adv_counts = adv_totals.to_frame().rename(columns={0: 'total'})
    for scale_type, aa in df.groupby('scale_type'):
        print(aa.value_counts(['scale_type', 'adv_lemma']).nlargest(5))
        adv_counts.loc[:, scale_type] = aa.value_counts('adv_lemma')
        print('-------------------------------------------')
    adv_counts = adv_counts.fillna(0)
    print('\n' + adv_counts.to_markdown())
    print('\n' + adv_counts.describe().transpose().round(1).to_markdown())

    compare = pd.DataFrame(index=adv_counts.index, columns=SCALE_TYPES)
    for scale_type in SCALE_TYPES:
        percent_col = f'adv{scale_type}_percent'
        adv_counts.loc[:, percent_col] = adv_counts[scale_type] / \
            adv_counts.total * 100
        compare.loc[:, scale_type] = adv_counts[percent_col] / \
            scale_percents[scale_type]
    compare = compare.round(5).apply(pd.to_numeric, downcast='float')
    compare = compare.assign(
        total_ratio=pd.to_numeric(df.adv_lemma.value_counts(normalize=True).round(3),
                                  downcast='float'),
        total_count=pd.to_numeric(
            df.adv_lemma.value_counts(), downcast='unsigned')
    )

    compare.to_csv(outpath)
    return compare


def visualize(outdf_path, compare):

    type_abbr = {'NON_G': 'N',
                 'OPEN': 'O',
                 'LOW_CLOSE': 'L',
                 'UP_CLOSE': 'U',
                 'TOT_CLOSE': 'T'}
    compare_abbr = compare.rename(
        columns=type_abbr)

    show_examples(compare, compare_abbr, outdf_path, type_abbr)
    show_adv_of_interest(compare, compare_abbr, outdf_path, type_abbr)
    show_ppi_adv(compare_abbr, outdf_path, type_abbr)
    show_all(compare_abbr, outdf_path, type_abbr)


def show_examples(compare, compare_abbr, outdf_path, type_abbr):
    examples = pick_examples(compare)
    examples_df = (compare_abbr.loc[compare_abbr.index.isin(examples), :]
                   .sort_values('total_count', ascending=False))
    print('\n' + examples_df.round(2).to_markdown())
    heatmap(
        examples_df,
        type_abbr.values(),
        outdf_path.with_suffix('.heat-ex.png').name
    )


def pick_examples(compare):
    examples = []
    ci = compare.sort_values('total_count').head(int(len(compare)/2))
    for scale_type in SCALE_TYPES:
        type_ci = ci[scale_type]
        examples += type_ci.nlargest(N_EX).index.to_list()
        examples += type_ci.nsmallest(N_EX).index.to_list()
    examples = list(set(examples))
    examples.sort()
    print('\nMost divergent adjectives (of 50% most frequent) for each scale type:' +
          ''.join(f'\n ¤ {e}' for e in examples))
    return examples


def show_adv_of_interest(compare, compare_abbr, outdf_path, type_abbr):
    key_adv_found = set(compare.index[compare.index.isin(ADV_OF_INTEREST)])
    compare_key = compare_abbr.loc[list(key_adv_found), :]
    top_30 = compare_key.total_count.nlargest(30).index
    all_key_df = compare_key.sort_values('total_count', ascending=False)
    print('\n' + all_key_df.round(2).to_markdown())
    heatmap(
        all_key_df.loc[top_30, :],
        type_abbr.values(),
        outdf_path.with_suffix('.heat-key.png').name
    )

    heatmap(
        all_key_df,
        type_abbr.values(),
        outdf_path.with_suffix('.heat-key.png').name.replace('_examples_', '_')
    )


def show_ppi_adv(compare_abbr, outdf_path, type_abbr):
    compare_ppi = compare_abbr.loc[compare_abbr.index.isin(PPI_ADVERBS), :]
    ppi_df = compare_ppi.sort_values('total_count', ascending=False)
    print('\n' + ppi_df.round(2).to_markdown())
    heatmap(
        ppi_df,
        type_abbr.values(),
        outdf_path.with_suffix(
            '.heat_ppi_m-mod.png').name.replace('_examples_', '_'),
        (10, 8)
    )


def show_all(compare_abbr, outdf_path, type_abbr):
    heatmap(
        compare_abbr.sort_values('total_count', ascending=False),
        type_abbr.values(),
        outdf_path.with_suffix('.heat-ALL.png').name.replace('_examples_', '_')
    )


def heatmap(df, columns=None, save_name=None, size=(8, 10)):

    plt.figure(figsize=size, dpi=100, facecolor="white")

    adv_labels = df.index + ' (' + df.total_count.astype('string') + ')'
    if columns:
        df = df.loc[:, columns]
    df = df.astype('float')
    # Displaying dataframe as an heatmap
    # with diverging colourmap as RdYlBu
    plt.imshow(df, cmap="RdYlBu")
    # plt.imshow(df, cmap="viridis")
    plt.autoscale(enable=True, axis='both')
    # Displaying a color bar to understand
    # which color represents which range of data
    plt.colorbar()

    # Assigning labels of x-axis
    # according to dataframe
    plt.xticks(range(len(df.columns)), df.columns)

    # Assigning labels of y-axis
    # according to dataframe
    plt.yticks(range(len(df.index)), adv_labels)

    # Displaying the figure
    plt.show()

    if save_name:
        out_dir = Path(
            '/share/compling/projects/sanpi/notebooks/scale_comparison/images')
        out_file = out_dir.joinpath(save_name)
        plt.savefig(out_file, dpi=300)
        print(f'Heatmap saved to:\n  {out_file}')


if __name__ == '__main__':
    _main()
