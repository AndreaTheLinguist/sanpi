# %%
from pathlib import Path
import pandas as pd
from utils.dataframes import get_proc_time, print_md_table
from utils.general import file_size_round

SANPI_DATA = Path('/share/compling/data/sanpi')
TMP_SAVE = SANPI_DATA.joinpath('info/meta_df.tmp.pkl.gz')
SUBSETS_DIR = SANPI_DATA.joinpath('subsets')


def _main():
    if TMP_SAVE.is_file():
        path_gen_meta_df = pd.read_pickle(TMP_SAVE)
    else:
        path_gen_meta_df = build_bigram_path_df()

    print_basic_file_info(path_gen_meta_df)

    # >>>>>>>---------------------->>>
    meta_df = add_paths_to_counts(path_gen_meta_df)

    in_counts_df, bg_counts_df = get_counts(meta_df)

    full_info = meta_df.join(in_counts_df.iloc[:, :3]).join(
        bg_counts_df.iloc[:, :3])
    full_info.to_pickle(SANPI_DATA.joinpath(
        'info/subset_compare-meta-info.pkl.gz'))
    desc = full_info.describe().T.assign(total=full_info.fillna(0).sum())
    print_md_table(desc, transpose=True, title='\n### Comparison Summary\n')
    desc.to_csv(SANPI_DATA.joinpath('info/subset_compare-stats.csv'))
    for corp, cdf in full_info.groupby('corpus'):
        summ_table = cdf.describe().T.assign(total=cdf.fillna(0).sum())
        print_md_table(summ_table, transpose=True,
                       title=f'#### Comparison Summary for `{corp}`\n')
        summ_table.to_csv(SANPI_DATA.joinpath(
            f'info/subset_compare-stats_{corp}.csv'))


def print_basic_file_info(path_meta_df):
    print_md_table(path_meta_df.sample(1),
                   title='#### Meta Info Sample', transpose=True)
    print_md_table(path_meta_df.select_dtypes(exclude='number'),
                   describe=True, transpose=True, title='#### Top Level Bigram Subset Descriptive Stats')

    compare_sizes_by_group(path_meta_df)


def compare_sizes_by_group(path_meta_df):
    print_md_table(compare_sizes(path_meta_df), title='\n##### Overall Size Comparison\n')
    print_md_table(diff_by_corpus(path_meta_df), title='\n##### Size Comparison by Corpus\n')


def diff_by_corpus(path_meta_df):
    first_df = []
    for corp, cdf in path_meta_df[['corpus', 'size', 'init_size']].groupby('corpus'):
        size_info = compare_sizes(cdf, data_label=f'`{corp}`'
                                  ).add_prefix(f'`{corp}`:')
        if any(first_df): 
            return first_df.join(size_info)
        else: 
            first_df = size_info

def compare_sizes(path_meta_df, data_label='Entire'):
    return (
        summarize_file_size(
            path_meta_df.init_size, label='starting',
            table_name=f'\n#### {data_label} Starting Corpus File Size\n')
        .join(
            summarize_file_size(
                path_meta_df['size'], label='subset',
                table_name=f'\n#### {data_label} Corpus Subset File Sizes\n'))
        .join(
            summarize_file_size(
                path_meta_df.init_size - path_meta_df['size'], label='reduction',
                table_name=f'\n##### {data_label} Size Reduction\n'))
    )


def summarize_file_size(file_size_series: pd.Series, label: str = 'summary',
                        table_name: str = ''):
    # change_sign = any(file_size_series < 0)
    # if change_sign:
    #     file_size_series = file_size_series.abs()
    size_info = file_size_series.describe().round().squeeze()
    size_info['total'] = file_size_series.sum()
    size_info = pd.to_numeric(size_info, downcast='unsigned')
    size_info.iloc[1:] = size_info.iloc[1:].apply(file_size_round)
    # if change_sign:
    #     size_info.iloc[1:] = '-'+size_info[1:]
    size_info = size_info.rename(index={'50%': 'median'})
    size_info_df = size_info.to_frame(label)
    print_md_table(size_info_df, title=table_name)
    return size_info_df


def get_counts(meta_df):

    in_counts_dict, bg_counts_dict = retrieve_totals(meta_df)

    in_counts_df = pd.DataFrame.from_dict(
        in_counts_dict,
        orient='index', dtype='uint').add_prefix('initial_')
    in_counts_df.index.name = 'data_key'
    bg_counts_df = pd.DataFrame.from_dict(
        bg_counts_dict,
        orient='index', dtype='uint').add_prefix('bigram_')
    bg_counts_df.index.name = 'data_key'
    in_counts_df.to_csv(SANPI_DATA.joinpath(
        'info/initial_totals_by_conllu.csv'))
    bg_counts_df.to_csv(SANPI_DATA.joinpath(
        'info/bigram_totals_by_conllu.csv'))

    return in_counts_df, bg_counts_df


def retrieve_totals(meta_df: pd.DataFrame):
    in_counts_dict = {}
    bg_counts_dict = {}
    print('\n## Loading "total" values from `*.counts.json`\n')
    # HACK
    # for i, data_key in enumerate(meta_df.sample(50).sort_index(axis=0).index, start=1):
    for i, data_key in enumerate(meta_df.sort_index(axis=0).index, start=1):
        print(f'{str(i).zfill(4)}. `{data_key}`')
        in_counts_dict[data_key] = load_totals(
            meta_df.at[data_key, 'input_counts'])
        bg_counts_dict[data_key] = load_totals(
            meta_df.at[data_key, 'subset_counts'])

    return in_counts_dict, bg_counts_dict


def add_paths_to_counts(path_gen_meta_df):
    subframes = []
    for paths_csv, df in path_gen_meta_df.groupby('path_index_csv'):
        # print(paths_csv)
        path_info = read_index_csv(paths_csv)
        if any(path_info.filter(like='counts', axis=1).count() < len(path_info)):
            print(
                f'WARNING: There are missing `.counts.json` paths in {paths_csv}')
        subframes.append(df.join(path_info))

    df = pd.concat(subframes)

    # print(df.select_dtypes(exclude='number').describe().T.to_markdown(floatfmt=',.0f'))

    # df.drop(['path_index_csv', 'subset_info_dir'])
    return df


def build_bigram_path_df():
    with Timer() as timer:
        data = collect_path_info()
        print(f'Time to collect path data: {timer.elapsed()}')

    with Timer() as timer:
        meta_df = _convert_to_df(data)
        print(f'Time to convert path info dict to dataframe {timer.elapsed()}')
    meta_df.to_pickle(TMP_SAVE)
    return meta_df


def _convert_to_df(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df['size'] = pd.to_numeric(df['size'], downcast='unsigned')
    df['init_conllu'] = df.name.str.replace('BIGRAM.', '', regex=False)
    df['data_key'] = df.index.str.replace('BIGRAM.', '', regex=False)
    df = _add_source_path_info(df)
    # df['path_index_csv'] = df.subset_info_dir.apply(find_latest)
    df['path_index_csv'] = df.subset_info_dir.apply(
        lambda i: max(Path(i).glob('subset-bigram_path-index*csv'),
                      key=lambda file: file.stat().st_ctime))
    df = df.convert_dtypes()

    return df.rename_axis('subset_stem').reset_index().set_index('data_key')


# def find_latest(info_dir):
#     files = info_dir.glob('subset-bigram_path-index*csv')
#     file_times = pd.to_numeric(
#         {f: f.stat().st_ctime for f
#          in files}
#     )
#     return file_times.nlargest(1).index


# def determine_path_index_csv(subset_info_dir):
#     subset_info_dir = subset_info_dir.apply(Path)
#     return subset_info_dir.apply(lambda i: max(i.glob('subset-bigram_path-index*csv'),
#                                                key=lambda file: file.stat().st_ctime))


def _add_source_path_info(_df):
    _df[['corpus_part', 'corpus_part_dir', 'corpus', 'subset_info_dir']] = _df.source_path.apply(
        lambda x: pd.Series(_def_source_path_info(x))
    )
    _df['init_path'] = _df.corpus_part_dir / _df.init_conllu.apply(Path)
    _df['init_size'] = pd.to_numeric(_df.init_path.apply(lambda i: i.stat().st_size),
                                     downcast='unsigned')
    # df['init_size']=df.init_path.apply(lambda conllu: Path(conllu).stat().st_size)
    return _df


def _def_source_path_info(source_path):
    source_path = Path(source_path)
    grandparent_path = source_path.parent.parent
    return [grandparent_path.stem,
            grandparent_path,
            grandparent_path.parent.stem,
            source_path.with_name('info')]


def get_file_info(p: Path):
    return {
        'parent': p.parent.name,
        'name': p.name,
        'path': p,
        'source_path': p.readlink(),
        'subset_corpus': p.parent.parent.name,
        'size': p.stat().st_size
    }


def collect_path_info():
    return {p.stem: get_file_info(p) for p in SUBSETS_DIR.rglob('*.conllu')}


def read_index_csv(index_csv_path: Path):
    try:
        path_info = pd.read_csv(
            index_csv_path,
            usecols=['STEM', ' INPUT_COUNTS', ' SUBSET_COUNTS'],
            dtype='string'
        )
    except ValueError:
        path_info = pd.read_csv(
            index_csv_path,
            usecols=['STEM', 'INPUT_COUNTS', 'SUBSET_COUNTS'],
            dtype='string'
        )
    clean_csv_count_cols(path_info)

    return path_info.set_index('stem')


def clean_csv_count_cols(path_info):
    path_info.columns = path_info.columns.str.strip().str.lower()
    for col in path_info.columns:
        path_info[col] = path_info[col].str.strip()
        if any(path_info[col].str.startswith('corpora_shortcuts')):
            path_info[col] = path_info[col].apply(
                SANPI_DATA.joinpath).astype('string')
            if not all(path_info[col].apply(Path).apply(Path.is_file)):
                print('ERROR: paths corrupted! files not found.')


def load_totals(counts_path: Path):
    counts_path = Path(counts_path)
    # print(f'Loading from: {counts_path}')
    if not counts_path.is_absolute():
        try_path = SANPI_DATA.joinpath(counts_path)
        if try_path.is_file():
            counts_path = try_path
    counts_df = pd.read_json(counts_path)
    totals = counts_df.loc[:, 'total']
    return pd.to_numeric(totals.dropna(), downcast='unsigned').to_dict()


class Timer:

    """
    A context manager for measuring elapsed time using a start and end timestamp.

    __enter__ method sets the start timestamp and returns the Timer instance.
    __exit__ method sets the end timestamp.
    elapsed method calculates and returns the elapsed time as a string.

    Attributes:
        start (pd.Timestamp): The start timestamp.
        end (pd.Timestamp): The end timestamp.

    Methods:
        elapsed(): Calculates and returns the elapsed time as a string.

    Example usage:
        with Timer() as timer:
            # Code to measure elapsed time

        print(timer.elapsed())  # Output: Elapsed time in the format HH:MM:SS.S
    """

    def __init__(self) -> None:
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = pd.Timestamp.now()
        return self

    def __exit__(self, *args):
        self.end = pd.Timestamp.now()

    def elapsed(self):
        return get_proc_time(self.start, pd.Timestamp.now())


if __name__ == '__main__':
    _t0 = pd.Timestamp.now()
    _main()
    _t1 = pd.Timestamp.now()

    print('✔️ Program Completed --', pd.Timestamp.now().ctime())
    print(f'   total time elapsed: {get_proc_time(_t0, _t1)}')
