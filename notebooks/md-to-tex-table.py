# coding=utf-8
# %%
import contextlib
import re
import textwrap
from os import system
from pprint import pprint
from sys import argv

import matplotlib.pyplot as plt
from am_notebooks import (IMAGE_DIR, LATEX_TABLES, SANPI_HOME, TABLE_DIR,
                          WRITING_LINKS, Path, colors, 
                          compose_png_path, format_negatives, format_zeros,
                          confirm_dir, pd, save_latex_table, set_my_style,
                          snake_to_camel, timestamp_today)

from source.utils.general import camel_to_snake

VERBOSE = True

def tex_path_from_md(md_path):
    print(
        f'Loading markdown formatted table from\n-> "{md_path}"')
    tex_path = LATEX_TABLES.joinpath(
        str(md_path.with_name(md_path.name.replace('.', '_').replace('`', '').replace("'", '')
                              + f'.{timestamp_today()}.tex')).split('imports/')[-1])
    print(
        f'.tex output will be saved as:\n-> "{tex_path}')
    confirm_dir(tex_path.parent)
    return tex_path


def md_to_tex(md_path):

    tex_path = tex_path_from_md(md_path)
    system(f'ls -o {md_path}')
    system(
        f'pandoc -o {tex_path} --strip-comments -f markdown -t latex {md_path}')
    system(f'ls -o {tex_path}')
    return (tex_path, None)


plt.rcParams['font.family'] = 'serif'

# plt.style.use('seaborn-v0_8-paper')
plt.style.use('seaborn-v0_8-colorblind')
# plt.style.use('tableau-colorblind10')
args = [a for a in argv[1:] if not a.startswith('--')] + \
    list(SANPI_HOME.joinpath('notebooks/jw/imports/ch2').glob('*.csv'))
pprint(args)
# %%


def plot_barh(png_stem, df):
    col_names = [c for c in df.columns.to_list() if c]
    try:
        df.columns = df.columns.str.replace('_', ' ')
    except AttributeError:
        pass

    df = df.set_index(df.columns[0]).sort_values(df.columns[-1])
    df.plot(
        kind='barh', colormap='gist_yarg', legend=False,
        xlabel=', '.join(df.columns), grid=True, subplots=True)
    # print(col_names)
    _fig = plt.savefig(
        compose_png_path('-'.join([snake_to_camel(c.strip().replace(' ', '_'))
                                   for c in col_names]),
                         dirpath=IMAGE_DIR, label_str=png_stem),
        dpi=400, bbox_inches='tight', pad_inches=0.2)
    plt.show()
    return df


def plot_mermaid_str(mermaid_text, verbose):
    mermaid_parts = pd.Series([m.strip() for m in mermaid_text.splitlines()])
    param = mermaid_parts.str.extract(
        r'^(\S+) (.+)$').set_index(0).convert_dtypes()
    values = [int(x)
              for x in param.loc['bar', :].squeeze().strip('[]').split(',')]
    # print(values)
    labels = [w.strip('" ') for w in param.loc['x-axis',
                                               :].squeeze().strip('["]').split(',')]
    # print(labels)
    df = pd.DataFrame(index=labels, data=values,
                      columns=[
                          param.loc['y-axis', :]
                          .str.extractall(r'^"(.+)"')
                          .squeeze().strip()]
                      ).convert_dtypes()
    caption = param.loc['title', :].squeeze().strip('" ')
    f_stem = snake_to_camel(caption.replace(' ', '_')).replace('`', '')
    # print(f_stem)
    # _tex_path = (LATEX_TABLES / f_stem / f'{f_stem}.{timestamp_today()}.tex')
    # confirm_dir(_tex_path.parent)
    # print(_tex_path)
    # df.to_latex(_tex_path, caption=
    # caption, label=caption.replace(' ', '-'))
    sty = df.convert_dtypes().style.background_gradient('purple_rain')
    _tex_path = (save_latex_table(sty,
                                  caption=caption, latex_stem=f_stem,
                                  latex_subdir=f_stem,
                                  label=caption.strip().replace(' ', '-')))
    if verbose:
        print(Path(_tex_path).read_text())
    plot_barh(f_stem.strip(' _-'), df.reset_index())
    return df, sty


def process_table_input(arg_str, verbose: bool = False):

    if 'y-axis' in arg_str:
        plot_mermaid_str(arg_str, verbose)
    else:
        abs_path = Path(arg_str)
        if not abs_path.is_absolute():
            abs_path = TABLE_DIR.joinpath(arg_str)
        if abs_path.exists():
            if abs_path.suffixes[-1] == '.csv':
                return process_csv_input(abs_path,
                                         verbose=verbose)
            else:
                return md_to_tex(abs_path)
# %%


def process_csv_input(abs_path, verbose: bool = False):
    df = pd.read_csv(abs_path).convert_dtypes()
    indexer = df.columns[0]
    if indexer.lower().startswith(('adv', 'adj', 'polar bigram', 'bigram', 'trig')):
        df[indexer] = '<i>' + df[indexer] + '</i>'
    print(df.head().to_markdown(tablefmt='plain'))
    df['#'] = df.index.to_series() + 1
    df = df.set_index(['#', indexer])
    # print(df.head().to_markdown(tablefmt='latex'))
    if 'PosVers' in df.columns and 'AllVers' in df.columns:
        df['PosVers%AllVers'] = (df.PosVers / df.AllVers) * 100
        if 'NegVers' in df.columns:
            df['PosVers:NegVers'] = df.apply(
                lambda a: (a.PosVers / a.NegVers)
                if a.NegVers != 0 else None, axis=1
            )
        df = df.filter(['AllVers', 'PosVers', 'NegVers',
                        'PosVers%AllVers', 'NegVers%AllVers',
                        'PosVers:NegVers', 'NegVers:PosVers'])
    if len(df.columns) < 4:
        plot_barh(abs_path.stem, df)
    latex_path = LATEX_TABLES.joinpath(
        str(abs_path).split(
            'tables/' if 'tables/' in str(abs_path) else 'imports/')[-1]
    ).with_suffix(f'.{timestamp_today()}.tex')
    confirm_dir(latex_path.parent)
    if any(df.select_dtypes(exclude='number')):
        nonnums = df.select_dtypes(exclude='number').columns.to_list()
        df = df.reset_index().set_index(list(df.index.names) + nonnums)
    cmap = ('BuPu' if 'Polar' in str(abs_path)
            else ('RdPu' if 'NEQ' in str(abs_path)
                  else 'PuRd'))
    sty = format_zeros(format_negatives(
        df.style.background_gradient(cmap)
    ))
    if verbose: 
        with contextlib.suppress(Exception):
            display(set_my_style(sty))
    save_latex_table(
        sty,
        longtable=len(df) > 10,
        verbose=verbose, 
        position='ht',
        label=f'tab:{latex_path.stem}',
        latex_path=latex_path)
    if verbose:
        print(latex_path.read_text())
    return df, sty


for arg in args:
    arg = str(arg)
    df, sty = process_table_input(arg, verbose=VERBOSE)
    # display(set_my_style(df).background_gradient('BuGn'))


# %%

# print('\\singlespacing', '\\scriptsize',
#       snake_to_camel(df.style.background_gradient(
#           'BuPu' if 'Polar' in str(arg)
#           else ('RdPu' if 'NEQ' in str(arg)
#                 else 'PuRd')
#       ).format(escape='latex', thousands='',
#                ).to_latex(siunitx=['table-auto-round'],
#                           convert_css=True,
#                           environment='longtable',
#                           #    position_float='centering',
#                           position='ht',
#                           multirow_align='c', multicol_align='c',
#                           clines='all;data')
#           .replace('deltaP_mean', 'dPavg')).replace('%', '\%'),
#       '\\normalsize', '\\normalspacing',
#       sep='\n')

