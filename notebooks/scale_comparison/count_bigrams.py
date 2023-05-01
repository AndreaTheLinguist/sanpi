from pathlib import Path
# from pprint import pprint
from sys import argv

import matplotlib.pyplot as plt
import pandas as pd
from LexicalCategories import SAMPLE_ADJ, SAMPLE_ADV


def determine_global_limits():
    try:
        input_1 = argv[1]
    except IndexError:
        n_files = 2
    else:
        n_files = int(input_1)

    try:
        input_2 = argv[2]
    except IndexError:
        n_hits = n_files * 100
    else:
        n_hits = int(input_2)
    return n_files, n_hits


N_FILES, N_HITS = determine_global_limits()
N_EX = 3


def _main():
    print(pd.Timestamp.now().ctime())
    print(
        f"Collecting sample vocabulary frequencies for {N_FILES} *hits.pkl.gz files"
    )
    # print(" -", N_FILES, "files\n - frequency threshold of", N_HITS)
    outdir = Path(
        '/share/compling/projects/sanpi/notebooks/scale_comparison/freq_out')
    if not outdir.is_dir():
        outdir.mkdir(parents=True)
    all_bigrams_pkl = outdir.joinpath(f'bigrams_all.{N_FILES}f.pkl.gz')
    th5_bigrams_pkl = outdir.joinpath(
        f'bigrams-only_thresh5.{N_FILES}f.pkl.gz')

    print('\n## Adj Vocab J')
    # pprint(SAMPLE_ADJ)
    J, J_df = unpack_dict(SAMPLE_ADJ)
    print('\n' + J_df.to_markdown() + '\n')

    print('\n## Adv Vocab R')
    # pprint(SAMPLE_ADV)
    R, R_df = unpack_dict(SAMPLE_ADV, values_name='adv')
    print('\n' + R_df.to_markdown() + '\n')

    _t0 = pd.Timestamp.now()
    print('\n## loading data...')
    if th5_bigrams_pkl.is_file():
        print(f'Found previous output. Loading data from {th5_bigrams_pkl}')
        rdf = pd.read_pickle(th5_bigrams_pkl)
    else:
        if all_bigrams_pkl.is_file():
            print(f'Found previous output. Loading data from {all_bigrams_pkl}')
            df = pd.read_pickle(all_bigrams_pkl).set_index('hit_id')
        else:
            df = load_data()
            save_table(df, str(all_bigrams_pkl).split('.pkl', 1)[0], "unrestricted bigrams")
            # df.to_pickle(all_bigrams_pkl)
        rdf = restrict_data(df)
        save_table(rdf, str(th5_bigrams_pkl).split('.pkl', 1)[0],
                   'restrictred bigrams (5+ frequency threshold)')
        # rdf.to_pickle(th5_bigrams_pkl)
    _t1 = pd.Timestamp.now()

    print('✓ time:', get_proc_time(_t0, _t1))
    rdf.describe()
    xfrq = sort_by_margins(
        pd.crosstab(index=rdf.adj_lemma,
                    columns=rdf.adv_lemma,
                    margins=True,
                    margins_name='SUM'))
    save_table(xfrq,
               outdir.joinpath(f'all-frq_thresh5.{N_FILES}f'),
               "all adj x adj frequency",
               formats=['csv'])
    # xfrq.to_csv(outdir.joinpath(f'all-frq_thresh5.{N_FILES}f'))
    JxR = rdf.loc[rdf.adj_lemma.isin(J)
                  & rdf.adv_lemma.isin(R), :].astype('string')
    # JxRcat = JxR.assign(
    #     adj_lemma=pd.Categorical(JxR.adj_lemma, categories=J),
    #     adv_lemma=pd.Categorical(JxR.adv_lemma, categories=R),
    #     )
    JxRfrq = pd.crosstab(index=JxR.adj_lemma,
                         columns=JxR.adv_lemma,
                         margins=True,
                         margins_name='SUM')
    found_J = J_df.index.isin(JxRfrq.index)
    found_R = R_df.index.isin(JxRfrq.columns)
    # JxRcatfrq = pd.crosstab(index=JxRcat.adj_lemma, columns=JxRcat.adv_lemma, margins=True, margins_name='SUM')
    JxRfrq = JxRfrq.loc[J_df[found_J].index.to_list() + ['SUM'],
                        R_df[found_R].index.to_list() + ['SUM']]
    save_table(JxRfrq,
               outdir.joinpath(f'JxR-frq_thresh5.{N_FILES}f'),
               'scale diagnostics adj x adv frequency',
               formats=['csv'])
    # JxRfrq.to_csv(outdir.joinpath(f'JxR-frq_thresh5.{N_FILES}f.csv'))
    # visualize(text_csv_path)


def sort_by_margins(crosstab_df, margins_name='SUM'):
    crosstab_df = (crosstab_df.sort_values(
        margins_name,
        ascending=False).transpose().sort_values(margins_name,
                                                 ascending=False).transpose())
    return crosstab_df


def unpack_dict(input_dict: dict,
                values_name: str = 'adj',
                keys_name: str = 'type',
                return_df=True,
                return_dict=False):
    scale_df = (pd.Series(input_dict).to_frame().reset_index().rename(
        columns={
            0: values_name,
            'index': keys_name
        }))
    explodf = scale_df.explode(values_name).set_index(values_name)
    inv_flat_dict = explodf.to_dict()[keys_name]
    flat_unq_vals = list(set(inv_flat_dict.keys()))
    flat_unq_vals.sort()
    returns = (flat_unq_vals, )
    if return_df:
        returns += (explodf, )
    if return_dict:
        returns += (inv_flat_dict, )

    return returns


def get_proc_time(start: pd.Timestamp, end: pd.Timestamp) -> str:
    t_comp = (end - start).components
    time_str = (":".join(
        str(c).zfill(2)
        for c in (t_comp.hours, t_comp.minutes, t_comp.seconds)) +
                f'.{round(t_comp.microseconds, 1)}')

    return time_str


def load_data():
    pkl_paths = select_pickles()
    _ts = pd.Timestamp.now()
    df_list = []
    for p in pkl_paths:
        print(f'  + ../{p.relative_to(Path("/share/compling/data"))}')
        # check for previous simplification
        simple_out_dir = p.parent.joinpath('simple')
        if not simple_out_dir.is_dir():
            simple_out_dir.mkdir(parents=True)
        simple_hits_pkl = simple_out_dir.joinpath('S_' + p.name)

        if simple_hits_pkl.is_file():
            print(f'Found previous output. Loading data from {simple_hits_pkl}')
            df = pd.read_pickle(simple_hits_pkl)
        else:
            df = pd.read_pickle(p)
            df = select_cells(df)

            save_table(df, str(simple_hits_pkl).split('.pkl')[0], df_name='simplified hits')

        df_list.append(df)

    combined_df = pd.concat(df_list)

    _te = pd.Timestamp.now()
    print('  > Time to create composite hits dataframe:',
          get_proc_time(_ts, _te))

    return combined_df


def save_table(df: pd.DataFrame,
               path_str:str,
               df_name: str = '',
               formats: list = ['pickle']):
    df_name += ' '
    
    for form in formats:
        print(f'~ Saving {df_name} as {form}...')
        t0 = pd.Timestamp.now()
        if form == 'pickle':
            out_path = str(path_str) + '.pkl.gz'
            df.to_pickle(out_path)
        elif form == 'csv':
            out_path = str(path_str) + '.csv'
            df.to_csv(out_path)
        elif form == 'psv':
            out_path = str(path_str) + '.csv'
            df.to_csv(out_path, sep='|')
        elif form == 'tsv':
            out_path = str(path_str) + '.tsv'
            df.to_csv(out_path, sep='\t')
        t1 = pd.Timestamp.now()
        print(f'   >> successfully saved as {out_path}\n' +
              f'      (time elapsed: {get_proc_time(t0, t1)})')


def select_pickles():
    pickle_dir = Path('/share/compling/data/sanpi/2_hit_tables/advadj')
    # > make dataframe to load smallest files first (for testing)
    pkl_df = pd.DataFrame(pickle_dir.glob('bigram-*hits.pkl.gz'),
                          columns=['path'])
    pkl_df = pkl_df.assign(size=pkl_df.path.apply(lambda f: f.stat().st_size))
    pkl_paths = pkl_df.sort_values('size').head(N_FILES).reset_index().path
    return pkl_paths


def select_cells(df,
                 #  target_adj, target_adv
                 ):
    df = (df.loc[:, ['adv_lemma', 'adj_lemma', 'text_window', 'token_str']].
          astype('string'))
    df = df.loc[~df.duplicated(['token_str', 'text_window']), :]
    # df_J = df.loc[df.adj_lemma.isin(target_adj), :]
    # df_R = df.loc[df.adv_lemma.isin(target_adv), :]
    # dfuq = df.loc[~df.duplicated(['token_str', 'text_window']), :]
    # dfuq.assign(
    #     adj_lemma=pd.Categorical(dfuq.adj_lemma, categories=target_adj),
    #     adv_lemma=pd.Categorical(df_RJuq.adv_lemma, categories=target_adv))
    return df


def restrict_data(df: pd.DataFrame) -> pd.DataFrame:
    # > removing duplicates
    ts = pd.Timestamp.now()
    input_len = len(df)
    is_duplicate = df.duplicated(['token_str', 'text_window'])
    print(
        f'Removing {is_duplicate.value_counts()[True]} duplicates between input tables. Examples:'
    )
    print(df.loc[df.duplicated(['token_str', 'text_window'], keep=False),
                 'text_window'].sort_values())
    df = df.loc[~is_duplicate, ['adv_lemma', 'adj_lemma']].astype('string')

    #> drop rare adv
    adv5 = df.adv_lemma.value_counts() >= 5
    df = df.loc[df.adv_lemma.isin(adv5[adv5].index), :]

    #> freq for limiting adj calculated *after* removing rare adv
    adj5 = df.adj_lemma.value_counts() >= 5
    df = df.loc[df.adj_lemma.isin(adj5[adj5].index), :]
    #> run through the weed out process again, in case dropped rows put items below threshold
    adv5 = df.adv_lemma.value_counts() >= 5
    df = df.loc[df.adv_lemma.isin(adv5[adv5].index), :]
    adj5 = df.adj_lemma.value_counts() >= 5
    df = df.loc[df.adj_lemma.isin(adj5[adj5].index), :]

    #> set dtype to 'category' _after_ dropping rare items
    df = df.assign(adj_lemma=df.adj_lemma.astype('category'),
                   adv_lemma=df.adv_lemma.astype('category'))
    restricted_len = len(df)
    te = pd.Timestamp.now()
    print(input_len - restricted_len, 'total rows/bigram tokens removed in',
          get_proc_time(ts, te))
    return df


def visualize(outdf_path, df):

    type_abbr = {
        'NON_G': 'N',
        'OPEN': 'O',
        'LOW_CLOSE': 'L',
        'UP_CLOSE': 'U',
        'TOT_CLOSE': 'T'
    }
    # compare_abbr = compare.rename(
    #     columns=type_abbr)

    # show_examples(compare, compare_abbr, outdf_path, type_abbr)
    # show_adv_of_interest(compare, compare_abbr, outdf_path, type_abbr)
    # show_ppi_adv(compare_abbr, outdf_path, type_abbr)
    show_all(df, outdf_path, type_abbr)


# def show_examples(compare, compare_abbr, outdf_path, type_abbr):
# examples = pick_examples(compare)
# examples_df = (compare_abbr.loc[compare_abbr.index.isin(examples), :]
#                .sort_values('total_count', ascending=False))
# print('\n' + examples_df.round(2).to_markdown())
# heatmap(
#     examples_df,
#     type_abbr.values(),
#     outdf_path.with_suffix('.heat-ex.png').name
# )

# def pick_examples(compare):
# examples = []
# ci = compare.sort_values('total_count').head(int(len(compare)/2))
# for scale_type in SCALE_TYPES:
#     type_ci = ci[scale_type]
#     examples += type_ci.nlargest(N_EX).index.to_list()
#     examples += type_ci.nsmallest(N_EX).index.to_list()
# examples = list(set(examples))
# examples.sort()
# print('\nMost divergent adjectives (of 50% most frequent) for each scale type:' +
#       ''.join(f'\n ¤ {e}' for e in examples))
# return examples

# def show_adv_of_interest(compare, compare_abbr, outdf_path, type_abbr):
# key_adv_found = set(compare.index[compare.index.isin(ADV_OF_INTEREST)])
# compare_key = compare_abbr.loc[list(key_adv_found), :]
# top_30 = compare_key.total_count.nlargest(30).index
# all_key_df = compare_key.sort_values('total_count', ascending=False)
# print('\n' + all_key_df.round(2).to_markdown())
# heatmap(
#     all_key_df.loc[top_30, :],
#     type_abbr.values(),
#     outdf_path.with_suffix('.heat-key.png').name
# )

# heatmap(
#     all_key_df,
#     type_abbr.values(),
#     outdf_path.with_suffix('.heat-key.png').name.replace('_examples_', '_')
# )

# def show_ppi_adv(compare_abbr, outdf_path, type_abbr):
# compare_ppi = compare_abbr.loc[compare_abbr.index.isin(PPI_ADVERBS), :]
# ppi_df = compare_ppi.sort_values('total_count', ascending=False)
# print('\n' + ppi_df.round(2).to_markdown())
# heatmap(
#     ppi_df,
#     type_abbr.values(),
#     outdf_path.with_suffix(
#         '.heat_ppi_m-mod.png').name.replace('_examples_', '_'),
#     (10, 8)
# )


def show_all(compare_abbr, outdf_path, type_abbr):
    heatmap(
        compare_abbr.sort_values('total_count', ascending=False),
        type_abbr.values(),
        outdf_path.with_suffix('.heat-ALL.png').name.replace(
            '_examples_', '_'))


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
