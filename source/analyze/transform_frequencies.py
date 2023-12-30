# coding=utf-8
import statistics as stat
from math import sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import get_proc_time, print_md_table, print_iter

_SANPI_DIR = Path('/share/compling/projects/sanpi')
_FREQ_OUT_DIR = _SANPI_DIR.joinpath('results/freq_out')
_TRANSFORM_DIR = _FREQ_OUT_DIR.with_name('transformed')


def _main():

    raw_tables = list(_FREQ_OUT_DIR.glob('all*35f.csv'))
    print_iter(raw_tables, bullet='*', header='Raw Frequency Files Found')
    tr_methods = ['sqrt', 'log2']
    output_pref = tr_methods + ['add1']
    
    for input_csv in raw_tables:
        print(f'\n## Transforming: {input_csv.relative_to(_SANPI_DIR)}\n')
        prelim_file_info = arrange_paths(output_pref, base_name=input_csv.name, 
                                         parent_dir=_TRANSFORM_DIR)
        if all(f.path.is_file() for f in prelim_file_info.values()):
            print('All transformations are already complete.')
            for f in prelim_file_info.values():
                write_time = (
                    pd.Timestamp.fromtimestamp(f.path.stat().st_mtime)
                    .strftime("%a %x at %I:%M%p").capitalize())
                print(f'+ {f.path.relative_to(_TRANSFORM_DIR)}', 
                      f'  + modified: {write_time}',
                      sep='\n')
        else:
            frq_raw = prep_freqs(input_csv)
            print(_enhance_descrip(frq_raw))
        
            # * transform frequencies
            trans_dict = transform(frq_raw)
            
            show_max(frq_raw, 'raw')
            for meth, rslt in trans_dict.items():
                show_max(rslt, meth)

            file_directory = arrange_paths(parent_dir=_TRANSFORM_DIR,
                                            prefix_list=list(trans_dict.keys()) + ['add1'],
                                            object_list=list(trans_dict.values()) +[frq_raw.add(1)],
                                            base_name=input_csv.name)

            print(len(file_directory), 'entries:', list(file_directory.keys()))

            show_directory(file_directory)

            for label in file_directory.keys():
                print(f'\n## `{label}` info\n')
                for k, v in (file_directory[label]._asdict().items()):
                    if k == 'obj' and isinstance(v, pd.DataFrame):
                        v = corners(v.round(2), size=4).to_markdown(
                            floatfmt=',.2f')
                    else:
                        v = f'`{v}`'
                    print(f'\n### `{label}` {k}\n\n' + v)

            write_directory(file_directory)


def prep_freqs(input_csv):
    frq_raw = pd.read_csv(input_csv)
    frq_raw.columns = frq_raw.columns.str.strip()
    if 'adv_lemma' in frq_raw.columns:
        frq_raw = frq_raw.set_index('adv_lemma').transpose()
    if frq_raw.index.name != 'adj_lemma':
        if 'adj_lemma' in frq_raw.columns:
            frq_raw = frq_raw.set_index('adj_lemma')
        else:
            frq_raw.index.name = 'adj_lemma'
    frq_raw = frq_raw.apply(pd.to_numeric, downcast='unsigned')
    frq_raw.columns.name = 'adv_lemma'
    frq_raw.columns = frq_raw.columns.astype('string')
    if 'SUM' in frq_raw.index:
        SUM_row = frq_raw.loc['SUM', :]
    if 'SUM' in frq_raw.columns:
        SUM_col = frq_raw.loc[:, 'SUM']
    frq_raw = frq_raw.loc[frq_raw.index !=
                          'SUM', frq_raw.columns != 'SUM']
    print(frq_raw.shape[0], 'rows (adj)')
    print(frq_raw.shape[1], 'columns (adv)')
    frq_raw.index = frq_raw.index.astype('string')
    return frq_raw



def _enhance_descrip(df: pd.DataFrame) -> pd.DataFrame:
    df = df
    desc = df.describe().transpose()
    desc = desc.assign(total=pd.to_numeric(df.sum()),
                       var_coeff=desc['std'] / desc['mean'],
                       range=desc['max'] - desc['min'],
                       IQ_range=desc['75%'] - desc['25%'])
    desc = desc.assign(upper_fence=desc['75%'] + (desc.IQ_range * 1.5),
                       lower_fence=desc['25%'] - (desc.IQ_range * 1.5))
    if 'SUM' not in desc.index:
        desc = desc.assign(
            plus1_geo_mean=df.add(1).apply(stat.geometric_mean),
            plus1_har_mean=df.add(1).apply(stat.harmonic_mean))
    for col in desc.columns:
        if col in ('mean', 'std', 'variance', 'var_coeff'):
            desc.loc[:, col] = desc[col].round(1)
        else:
            desc.loc[:, col] = pd.to_numeric(desc[col], downcast='unsigned')

    # mean_centr = no_sum_frame - no_sum_frame.mean()
    # mean_stand = no_sum_frame / no_sum_frame.mean()
    # mean_stand_centr = mean_stand - mean_stand.mean()
    # log2_trans = no_sum_frame.apply(np.log2)
    # log2_plus1_trans = no_sum_frame.add(1).apply(np.log2)
    # logn_plus1_trans = no_sum_frame.apply(np.log1p)

    return desc.round(1)


def transform_counts(df: pd.DataFrame,
                     method: str = 'sqrt',
                     plus1: bool = False):
    if plus1 or method.startswith('log'):
        df = df.add(1)
    if method == 'sqrt':
        df = df.apply(lambda x: x.apply(sqrt))
    elif method == 'log10':
        df = df.apply(lambda x: x.apply(np.log10))
    elif method == 'log2':
        df = df.apply(lambda x: x.apply(np.log2))
    return df


def heatmap(df, columns=None, save_name=None, size=(8, 10)):

    plt.figure(figsize=size, dpi=120, facecolor="white")

    adv_labels = df.index
    if columns:
        df = df.loc[:, columns]
    df = df.astype('float')
    # Displaying dataframe as an heatmap
    # with diverging colourmap as RdYlBu
    plt.imshow(df, cmap="plasma")
    # plt.imshow(df, cmap="gist_rainbow")
    # plt.imshow(df, cmap="jet")
    # plt.imshow(df, cmap="viridis")
    # plt.autoscale(enable=True, axis='both')
    # Displaying a color bar to understand
    # which color represents which range of data
    plt.colorbar()
    # Assigning labels of x-axis
    # according to dataframe
    plt.xticks(range(len(df.columns)), df.columns, rotation=-20)
    # Assigning labels of y-axis
    # according to dataframe
    plt.yticks(range(len(df.index)), adv_labels)
    # Displaying the figure
    plt.show()


def display_samples(sample_df, label):
    fig = plt.figure(dpi=130)
    # ax.barh(s20x10, width=1)
    sample_df.plot(kind='barh',
                   width=0.8,
                   figsize=(8, 10),
                   position=1,
                   title=f'{label} of sample',
                   grid=True,
                   colormap=color,
                   # colormap="gist_rainbow",
                   # colormap="rainbow",
                   #  colormap="brg",
                   #   colormap="nipy_spectral_r",
                   #    colormap="Set1",
                   ax=plt.gca())
    plt.show()
    fig = plt.figure(dpi=150)
    sample_df.plot(kind='barh',
                   stacked=True,
                   width=0.8,
                   figsize=(8, 10),
                   position=1,
                   title=f'{label} of sample',
                   grid=True,
                   colormap=color,
                   # colormap="gist_rainbow",
                   #  colormap="brg",
                   #    colormap="nipy_spectral_r",
                   #    colormap="Set1",
                   ax=plt.gca()
                   )
    plt.show()
    heatmap(sample_df, size=(8, 10))
    return fig


def sample_counts(frq_table, label,
                  rows=pd.Series(dtype='string'),
                  columns=pd.Series(dtype='string'), 
                  display=False):
    color = 'gist_rainbow'
    s = frq_table.iloc[:int(frq_table.shape[0]/4), :int(frq_table.shape[1]/3)]

    rows = rows if any(rows) else s.sample(16).index
    columns = columns if any(columns) else s.T.sample(8).index
    sample_df = s.loc[rows, columns]
    # print(sample_df.describe().T.round(2).to_markdown())
    if display:
        display_samples(sample_df, label)
    print_md_table(sample_df.round(1), n_dec=1, comma=False, title=label)

    return sample_df


def transform(frq_raw, methods=['sqrt', 'log2'], add1=True):

    frq_trans = pd.DataFrame()
    rows = None
    cols = None
    trans_dfs = {}
    for method in methods:
        print(f'\n### {method}\n')
        frq_trans = transform_counts(
            frq_raw, method=method, plus1=add1)
        trans_dfs[method] = frq_trans
        print(_enhance_descrip(frq_trans))
        if rows and cols:
            trans_sample = sample_counts(
                frq_trans, label=method,
                rows=rows, columns=cols)
        else:
            trans_sample = sample_counts(
                frq_trans, label=method)
            rows = trans_sample.index.to_list()
            cols = trans_sample.columns.to_list()

    sample_counts(frq_raw, label='raw counts')
    return trans_dfs


def show_max(frq_df, label=''):
    max_count = frq_df.max().max()
    # print(label, 'frequency MAX')
    print_md_table(df=frq_df.loc[frq_df.max(axis=1) == max_count,
                     frq_df.max() == max_count].round(1), 
                   indent=2,
                   n_dec=1,
                   title = f'MAX {label} frequency' '\n')


def arrange_paths(prefix_list: list,
                  object_list: list = None,
                  base_name: str = 'tmp.txt',
                  parent_dir: Path = Path.cwd(),
                  new_suffix: str = '',
                  sep: str = '_',
                  temp: bool = False) -> dict:

    fields = ['path', 'parent', 'stem', 'extension', 'obj', 'type']
    defaults = [None] * len(fields)
    try:
        directory_entry = namedtuple('FileDirectoryEntry', fields,
                                     defaults=defaults)
    except NameError:
        from collections import namedtuple
        directory_entry = namedtuple('FileDirectoryEntry', fields,
                                     defaults=defaults)
    if temp:
        parent_dir = parent_dir.joinpath('tmp')
    if parent_dir == Path.cwd():
        print('> All paths are relative to current working directory:',
              f'> + `{Path.cwd()}/`',
              sep='\n')
    if not parent_dir.is_dir():
        parent_dir.mkdir(parents=True)

    rel_base_path = Path(base_name)
    base_stem = rel_base_path.stem
    if new_suffix:
        ext = f".{new_suffix.strip('.')}"
    else:
        ext = rel_base_path.suffix

    directory_dict = {}
    if object_list:
        for prefix, obj in zip(prefix_list, object_list):
            fstem = f"{prefix}{sep}{base_stem}"
            directory_dict[prefix] = directory_entry(
                parent=parent_dir,
                stem=fstem,
                extension=ext,
                path=parent_dir.joinpath(fstem+ext),
                obj=obj,
                type=type(obj))
    else:
        for prefix in prefix_list:
            fstem = f"{prefix}{sep}{base_stem}"
            directory_dict[prefix] = directory_entry(
                parent=parent_dir,
                stem=fstem,
                extension=ext,
                path=parent_dir.joinpath(fstem+ext))
            
    return directory_dict


def show_directory(directory: dict):
    lines = []
    for i, entry in enumerate(directory.values()):
        if i == 0:
            lines.append(f'{entry.parent}/')

        lines.append(f'  ↪  {entry.stem}({entry.extension})')
    print('\n'.join(lines))


def corners(df, size: int = 5):
    index_name = df.index.name
    columns_name = df.columns.name
    df = df.reset_index().reset_index().set_index(
        ['index', index_name])
    df = df.T.reset_index().reset_index().set_index(
        ['index', columns_name]).T
    cdf = pd.concat(
        [dfs.iloc[:, :size].assign(__='...').join(
            dfs.iloc[:, -size:])
         for dfs in (df.head(size).T.assign(__='...').T,
                     df.tail(size))]
    )
    cdf = cdf.reset_index().set_index(index_name)
    cdf.pop('index')
    cdf = cdf.T.reset_index().set_index(columns_name)
    cdf.pop('index')
    return cdf.T.rename(columns={'': '...'}, index={'': '...'})


def write_directory(directory: dict, iter_sep: str = '\n'):
    sep_dict = {'.csv': ',',
                '.tsv': '\t',
                '.psv': '|'}
    for label, entry in directory.items():
        obj = entry.obj
        path = entry.path
        if not path.is_file():
            ext = entry.extension
            print(f'+ writing {label} to {ext} file...')

            if ext.endswith('sv'):
                try:
                    obj.to_csv(path, sep=sep_dict[ext], encoding='utf8')
                except AttributeError:
                    pass
                else:
                    continue

            if ext.endswith('pkl'):
                try:
                    obj.to_pickle(path)
                except AttributeError:
                    pass
                else:
                    continue

            if ext.endswith('json'):
                try:
                    __ = json.dumps(obj)
                except NameError:
                    import json
                obj = json.dumps(obj, indent=2)

            elif str(entry.type).endswith(("'list'>", "'tuple'>", "'dict'>", "'set'>")):
                if isinstance(obj, dict):
                    # key_width = len(max(list(obj.keys()))
                    obj = [f'{k} : {v}' for k, v in obj.items()]
                obj = iter_sep.join(obj)

            if ext.endswith('md'):
                title = f'# {entry.k}'
                obj = f'{title}\n\n{obj}'
            
            path.write_text(str(obj), encoding='utf8')
        else:
            print(f'* ({path.name} previously saved on:',
                  (pd.Timestamp.fromtimestamp(path.stat().st_mtime)
                     .strftime("%a %x at %I:%M%p").capitalize()
                   + '.)')
                  )


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    _main()
    proc_t1 = pd.Timestamp.now()
    print('✔️ Transformation Completed --', pd.Timestamp.now().ctime())
    print(f'   total time elapsed: {get_proc_time(proc_t1, proc_t0)}')
