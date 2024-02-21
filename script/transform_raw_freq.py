# coding=utf-8

import statistics as stat
from collections import namedtuple
from pathlib import Path
from sys import argv
import matplotlib.pyplot as plt
import pandas as pd

from source.utils.dataframes import Timer, corners, transform_counts, print_md_table
from source.utils.general import confirm_dir, PKL_SUFF, SANPI_HOME
from source.utils.visualize import heatmap

ADV_REPRESENT = 'adv_form_lower'
ADJ_REPRESENT = 'adj_form_lower'

# HACK use this to suppress plot windows
SHOW_PLOTS = False

try:
    INPUT_FREQ_PATH = Path(argv[1])
except IndexError:
    INPUT_FREQ_PATH = Path(
        '/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz')
if not INPUT_FREQ_PATH.is_file():
    INPUT_FREQ_PATH = Path(
        '/share/compling/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.pkl.gz')
try:
    INPUT_DIR_NAME = INPUT_FREQ_PATH.parent.name
except ValueError:
    INPUT_FREQ_PATH = INPUT_FREQ_PATH.resolve()
    INPUT_DIR_NAME = INPUT_FREQ_PATH.parent.name


def _enhance_descrip(df: pd.DataFrame) -> pd.DataFrame:
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


def display_sample(sample_df: pd.DataFrame,
                   label: str,
                   dpi=130,
                   color='gist_rainbow'):
    # color suggestions:
    #   color="RdYlBu"
    #   color="plasma"
    #   color="gist_rainbow",
    #   color="rainbow",
    #   color="viridis",
    #   color="brg",
    #   color="nipy_spectral_r",
    #   color="Set1",
    sample_name = f'{label} of sample'

    plot_barh(sample_df,
              chart_name=sample_name, color=color, dpi=dpi)
    plot_barh(sample_df,
              chart_name=sample_name, color=color, dpi=dpi, stacked=True)

    heatmap(sample_df, size=(8, 10), title=sample_name)
    # [ ] #TODO add `save_dir` and `save_name` arguments


def sample_counts(frq_table, label,
                  rows=pd.Series(dtype='string'),
                  columns=pd.Series(dtype='string'),
                  display=SHOW_PLOTS):

    s = frq_table.iloc[:int(frq_table.shape[0]/4), :int(frq_table.shape[1]/3)]

    rows = rows if any(rows) else s.sample(16).index
    columns = columns if any(columns) else s.T.sample(8).index
    sample_df = s.loc[rows, columns]

    if display:
        set_sample_path(label, )
        display_sample(sample_df, label)
    else:
        print(sample_df.round().to_markdown(floatfmt=',.0f'))

    return s, sample_df


def arrange_paths(prefix_list: list,
                  object_list: list,
                  base_name: str = 'tmp.txt',
                  parent_dir: Path = Path.cwd(),
                  new_suffix: str = '',
                  sep: str = '_',
                  temp: bool = False) -> dict:

    fields = ['path', 'parent', 'stem', 'extension', 'obj', 'type']
    defaults = [None] * len(fields)

    directory_entry = namedtuple('FileDirectoryEntry', fields,
                                 defaults=defaults)

    if temp:
        parent_dir = parent_dir.joinpath('tmp')
    if parent_dir == Path.cwd():
        print('> All paths are relative to current working directory:',
              f'> + `{Path.cwd()}/`',
              sep='\n')

    rel_base_path = Path(base_name)
    base_stem = rel_base_path.name.replace(
        PKL_SUFF, '') if rel_base_path.name.endswith(PKL_SUFF) else rel_base_path.stem

    ext = (f".{new_suffix.strip('.')}"
           if new_suffix
           else (PKL_SUFF
                 if rel_base_path.name.endswith(PKL_SUFF)
                 else rel_base_path.suffix)
           )
    directory_dict = {}
    for prefix, obj in zip(prefix_list, object_list):
        fstem = f"{prefix}{sep}{base_stem}"
        directory_dict[prefix] = directory_entry(
            parent=parent_dir,
            stem=fstem,
            extension=ext,
            path=parent_dir.joinpath(fstem+ext),
            obj=obj,
            type=type(obj))
    return directory_dict


def show_directory(directory: dict):
    lines = []
    for i, entry in enumerate(directory.values()):
        if i == 0:
            lines.append(f'{entry.parent}/')

        lines.append(f'  ↪  {entry.stem}({entry.extension})')
    print('\n'.join(lines))


def set_sample_path(label: str,
                    parent_dir: Path,
                    stem: str,
                    n_adj: int,
                    n_adv: int,
                    suffix: str = '.csv',
                    top: bool = True):
    samples_dir = parent_dir / 'samples'
    confirm_dir(samples_dir)
    return samples_dir.joinpath(f'{stem}.{"top" if top else "random"}{n_adj}x{n_adv}{suffix}')


def _get_sample(obj, md_adj, md_adv, n_dec):
    return obj.iloc[:md_adj, :md_adv].round(n_dec)


def save_top_vals(entry: tuple, label: str):
    print(f'Saving top values for {label}:')

    for suffix, n_adj, n_adv, n_dec in [('.md', 20, 10, 1),
                                        ('.csv', 250, 100, 2)]:
        if label in ('raw', 'add1'):
            n_dec = 0
        sample_path = set_sample_path(
            label, entry.parent, entry.stem, n_adj, n_adv, suffix)
        print(
            f"* {suffix.strip('.')} path = `{sample_path.relative_to(SANPI_HOME)}`")
        if sample_path.is_file() and sample_path.stat().st_size > 4:
            continue
        sample_df = _get_sample(entry.obj.copy(), n_adj, n_adv, n_dec)
        if suffix == '.md':
            sample_path.write_text(
                print_md_table(sample_df, n_dec=n_dec, suppress=True,
                               title=f'Top {n_adj}x{n_adv} `{label}`: `{entry.stem}`\n'),
                encoding='utf8')
        else:
            sample_df.to_csv(sample_path)


def write_directory(directory: dict, iter_sep: str = '\n', round_level=4):
    for label, entry in directory.items():
        path = entry.path
        obj = entry.obj
        obj = obj.round(round_level).apply(pd.to_numeric, downcast='float')
        save_top_vals(entry, label)
        if label == 'raw':
            continue
        if not path.is_file():
            ext = entry.extension
            print(f'+ writing {label} to {ext} file...')

            if ext.endswith('sv'):
                sep_dict = {'.csv': ',',
                            '.tsv': '\t',
                            '.psv': '|'}
                try:
                    obj.to_csv(path, sep=sep_dict[ext], encoding='utf8')
                except AttributeError:
                    pass
                else:
                    continue

            if ext.startswith('.pkl'):
                try:
                    obj.to_pickle(path)
                except AttributeError:
                    pass
                else:
                    continue

            if ext.endswith('json'):
                try:
                    __ = json.dumps(
                        obj)  # pylint: disable=used-before-assignment
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
                path.write_text(str(obj), encoding='utf8')
        else:
            print(f'* ({path.name} previously saved on:',
                  (pd.Timestamp.fromtimestamp(path.stat().st_mtime)
                     .strftime("%a %x at %I:%M%p").capitalize()
                   + '.)')
                  )


def _main():

    frq_raw = pd.read_csv(
        INPUT_FREQ_PATH) if INPUT_FREQ_PATH.suffix == '.csv' else pd.read_pickle(INPUT_FREQ_PATH)
    frq_raw.columns = frq_raw.columns.str.strip()

    if ADV_REPRESENT in frq_raw.columns:
        frq_raw = frq_raw.set_index(ADV_REPRESENT).transpose()
    if frq_raw.index.name != ADJ_REPRESENT:
        if ADJ_REPRESENT in frq_raw.columns:
            frq_raw = frq_raw.set_index(ADJ_REPRESENT)
        else:
            frq_raw.index.name = ADJ_REPRESENT
    frq_raw = frq_raw.apply(pd.to_numeric, downcast='unsigned')
    frq_raw.columns.name = ADV_REPRESENT
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

    frq0_sqrt = transform_counts(frq_raw)

    sqrt0_head, sqrt0_sample = sample_counts(
        frq0_sqrt, label='square root')
    sample_rows = sqrt0_sample.index
    sample_cols = sqrt0_sample.columns

    frq_log10 = transform_counts(frq_raw, method='log10')

    log10_head, log10_sample = sample_counts(
        frq_log10, label='log10',
        rows=sample_rows,
        columns=sample_cols)

    frq1_sqrt = transform_counts(frq_raw, plus1=True)

    add1_sqrt_head, add1_sqrt_sample = sample_counts(frq1_sqrt,
                                                     label='+1 smoothed square root',
                                                     rows=sample_rows, columns=sample_cols)

    raw_head, raw_sample = sample_counts(frq_raw, label='raw counts',
                                         rows=sample_rows, columns=sample_cols)

    frq_log2 = transform_counts(frq_raw, method='log2')

    log2_head, log2_sample = sample_counts(frq_log2, label='Binary Log',
                                           rows=sample_rows,
                                           columns=sample_cols)

    transform_dir = INPUT_FREQ_PATH.parent.parent.with_name(
        'transformed').joinpath(INPUT_DIR_NAME)
    confirm_dir(transform_dir)
    print(f'output directory: {transform_dir}')
    output_directory = arrange_paths(parent_dir=transform_dir,
                                     prefix_list=[
                                         'sqrt', 'log2', 'add1', 'raw'],
                                     object_list=[frq1_sqrt,
                                                  frq_log2, frq_raw.add(1), frq_raw],
                                     base_name=INPUT_FREQ_PATH.name)

    # print(len(output_directory), 'entries:', list(output_directory.keys()))

    show_directory(output_directory)

    for label in output_directory.keys():
        print(f'\n## `{label}` info\n')
        for k, v in (output_directory[label]._asdict().items()):
            if k == 'obj' and isinstance(v, pd.DataFrame):
                v = corners(v.round(2), size=4).to_markdown(floatfmt=',.2f')
            else:
                v = f'`{v}`'
            print(f'\n### `{label}` {k}\n' + v)

    write_directory(output_directory)


if __name__ == '__main__':
    with Timer() as timer:
        _main()

        print('✔️ Program Completed --', pd.Timestamp.now().ctime())
        print(f'   total time elapsed: {timer.elapsed()}')
