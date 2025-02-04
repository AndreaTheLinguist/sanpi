import argparse
import re
import textwrap
from pathlib import Path

import pandas as pd
from am_notebooks import (LATEX_TABLES, format_negatives, format_zeros,
                          save_latex_table)
from astropy.table import Table


def _parse_args():

    parser = argparse.ArgumentParser(
        description=(
            textwrap.dedent(
                '''script to:
                read latex formatted table into a pandas dataframe,
                apply color gradient background 
                and return to latex formatted table with added `\cellcolor{}` commands. 
                
                Takes one argument: path to latex formatted table (ending in ".tex"). 
                Output file will be the same with suffix ".color.tex" inplace of ".tex". 
                
                **Assumes all columns are numeric data only**
            ''')),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--tex_path',
        type=Path,
        default=Path('PBR_summary/versatility/pos-superset-most-vers-adj.tex'),
        help=('path to latex formatted table to apply color gradient to')
    )
    parser.add_argument(
        '-c', '--cmap',
        type=str, default=None,
        help=('string value indicating colormap to use for gradient')
    )
    parser.add_argument(
        '-a', '--axis',
        type=int, default=0,
        help=('integer value indicating axis to apply gradient on')
    )

    return parser.parse_args()


def _main():
    args = _parse_args()
    tex_path = args.tex_path

    if not tex_path.is_absolute():
        tex_path = LATEX_TABLES.joinpath(tex_path)

    # assets\tables\PBR_summary\{negative, positive, versatility}
    # tex_path = LATEX_TABLES.joinpath()

    tab = _get_df_from_tex(tex_path)

    tab.info()

    save_latex_table(
        format_zeros(
            format_negatives(
                tab.style.background_gradient(args.cmap))
        ), verbose=True,
        latex_path=tex_path.with_suffix('.color.tex'),
        label=tex_path.stem.split('.')[0],
        caption='\draft{Name colored \cmtt{'+tex_path.stem + '}}'
    )


def _get_df_from_tex(tex_path):
    tab = Table.read(tex_path).to_pandas().dropna().convert_dtypes()
    # tab = tab.set_index(tab.columns[0]).apply(
    tab.update(tab.select_dtypes(include='string').apply(
        lambda x: x.str.strip().str.replace(',', '').str.replace('%', '').str.replace('>', '')))
    tab = tab.convert_dtypes()
    
    #! #BUG There seems to be a bug here with convert_dtypes failing on number strings...
    #> #HACK applying `pd.to_numeric()` to relevant columns as a workaround
    str_cols = tab.select_dtypes('string').columns
    number_str_cols = str_cols[tab[str_cols].apply(
        lambda c: any(c.str.contains(r'\d{2,}', regex=True)))]
    tab[number_str_cols] = tab[number_str_cols].apply(pd.to_numeric)
    tab.update(
        tab.select_dtypes(include='string').apply(
        lambda c: c.apply(parse_formatting)))
    tab.columns = tab.columns.to_series().apply(parse_formatting).to_list()
    tab['#'] = tab.index + 1
    tab = tab.set_index(['#']
                        + tab.select_dtypes(exclude='number')
                        .columns.to_list())
    print(tab)
    return tab

def parse_formatting(string): 

    string = re.sub(r'\\textit\{(.+?)\}', r'<i>\1</i>', string)
    string = re.sub(r'\\textbf\{(.+?)\}', r'<b>\1</b>', string)
    string = re.sub(r'\\texttt\{(.+?)\}', r'<code>\1</code>', string)
    string = re.sub(r'\\cmtt\{(.+?)\}', r'<code>\1</code>', string)
    string = re.sub(r'\\_', '_', string)
    string = re.sub(r'\\[a-z]+\{(\w+)\}', r'\1', string)
    
    return string

if __name__ == '__main__':
    _main()
