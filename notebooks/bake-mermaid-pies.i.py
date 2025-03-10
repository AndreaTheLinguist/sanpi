#%%
import contextlib
import re
import textwrap
from os import system
from pprint import pprint
from sys import argv

import matplotlib.pyplot as plt
from am_notebooks import (IMAGE_DIR, LATEX_TABLES, SANPI_HOME, TABLE_DIR,
                          WRITING_LINKS, Path, colors, compose_img_path,
                          confirm_dir, format_negatives, format_zeros, pd,
                          save_latex_table, set_my_style, snake_to_camel,
                          timestamp_today)

from source.utils.general import camel_to_snake

SHOW_MANUAL_PIES = False

# %%
if SHOW_MANUAL_PIES:
    pd.Series({"not (2,859,001)": 2859001,
               "OTHER (314,680)": 314680
               }).plot(
        kind='pie',
        cmap='deep_waters',
        title='Superset Negative Operators')
    pd.Series({
        "not (2,859,001)": 2859001,
        "never (110,553)": 110553,
        "nothing (99,861)": 99861,
        "OTHER (104,266)": 104266

    }).plot(kind='pie',
            cmap='viridis',
            title='Superset Negative Operators', )

    pd.Series({
        "none (31,278)":  31278,
        "nor (15,698)":  15698,
        "without (14,784)":  14784,
        "no (12,409)":  12409,
        "neither (6,517)":  6517,
        "nobody (6,332)":  6332,
        "hardly (5,490)":  5490,
        "rarely (4,457)":  4457,
        "few (4,249)":  4249,
        "{barely, seldom, scarcely} (3,052)": 3052

    }).plot(kind='pie',
            cmap='lisa_frank',
            title='"OTHER" Negatives (~3% of total)', )

    pd.Series({

        "never (110,566)": 110566,
        "nothing (99,391)":  99391,
        "none (31,078)":  31078,
        "nor (15,717)":  15717,
        "no (9,150)":   9150,
        "neither (6,480)":   6480,
        "nobody (6,328)":   6328,
        "hardly (5,492)": 5492,
        "{rarely, barely} (5,706)":  5706,

    }).plot(kind='pie',
            cmap='Spectral',
            title='Negative Mirror Trigger Proportions', )

# %%


# def bake_pie(df, cmap, startangle=100, pct_color='w', unit='', title=''):

    # def func(pct, values, unit=''):
    #     # absolute = int(values.round(pct/100.*np.sum(values)))
    #     # if unit:
    #     #     unit = ' ' + unit
    #     # return f"{pct:.1f}%\n({absolute:,}{unit})"
    #     return '{:,.2f}%'.format

    # wedges, texts, autotexts = df.squeeze().plot(
    #     kind='pie', cmap=cmap, legend=False,
    #     textprops=dict(color=pct_color),
    #     autopct=lambda pct: func(pct, df.squeeze()),
    #     startangle=startangle)

    # # ax.legend(wedges, ingredients,
    # #         title="Ingredients",
    # #         loc="center left",
    # #         bbox_to_anchor=(1, 0, 0.5, 1))

    # # plt.setp(autotexts, size=8, weight="bold")
    # if title:
    #     ax.set_title(title)

    # plt.show()

# %%
# mermaid_pies = [
#     '''title Comparative Size of Mirror Subset
#       "tokens in mirror subset = 1,680,633": 1680633
#       "tokens not in subset = 70,280,740": 70289740''',


#     ]

# %%

mermaid_pie_regex = re.compile(r'pie\s*\n([^`]+)\n\s*```')
title_regex = re.compile(r'title (?P<title>.+)\s*\n')
mermaid_data_regex = re.compile(
    r'\n?\s*"(?P<label>.+)"\s*:\s*(?P<total>.+)\s*\n?')


def convert_mermaid_pies(cmap: str = 'light_rain',
                         md_doc_path: Path = Path.home().joinpath('justwriting/ch2_PolarBigrams.md'),
                         pct_size: float = 8,
                         start_angle: float = 80,
                         pct_color: str = 'k',  # -> black
                         unit: str = '',
                         background_color: str = None,
                         stylesheet: str = None,
                         legend: bool = False,
                         pct_distance: float = 0.85,
                         label_width: int = 22,
                         label_distance: float = 1.15
                         ):
    image_dir = IMAGE_DIR.joinpath(md_doc_path.stem)
    confirm_dir(image_dir)
    print(f"Figures will be saved in:\n {image_dir}/\n\n***\n")
    if stylesheet:
        plt.style.use('seaborn-v0_8-colorblind')
    update_dict = {'polarity': 'polar',
                   'negative': 'neg',
                   'positive': 'pos',
                   'trigger': 'trig',
                   'operator': 'trig',
                   'distribution': 'distrib',
                   'proportion': 'propor',
                   'superset': 'super',
                   'subset': 'mir',
                   'mirror': 'mir',
                   #    'tokens': 'tok',
                   'of': '',
                   '"': '',
                   '~': '',
                   '(': '-',
                   ')': '',
                   '%': 'pct'}

    mermaid_pies = mermaid_pie_regex.findall(md_doc_path.read_text())
    for mer_pie_str in mermaid_pies:
        title = title_regex.search(mer_pie_str)['title']

        mermaid_pie = pd.json_normalize(
            pd.Series(mermaid_data_regex.finditer(mer_pie_str)
                      ).apply(lambda m: m.groupdict())
        ).set_index('label').astype('float')

        # print('Title:', title)
        fstem = (re.sub(r'|'.join(update_dict.keys()),
                        lambda m:
                        update_dict.get(m.group(), ''), title.lower()
                        ).title().replace(' ', ''))
        title = '\n'.join(textwrap.wrap(title, 40, break_long_words=False))
        save_latex_table(set_my_style(mermaid_pie, caption=title, precision=0)
                         .background_gradient(cmap).relabel_index(mermaid_pie.index.str.split('=').str.get(0)),
                         caption=title, latex_subdir=f'mermaid_pies/{md_doc_path.stem}',
                         latex_stem=f'{fstem}_totals')

        mermaid_pie.index = (
            mermaid_pie.index
            .str.replace(r' ?= ?(.+)', r'\n(\1)', regex=True)
            .to_series().apply(
                lambda i: textwrap.wrap(
                    i, label_width,
                    #    initial_indent=' ' * 2,
                    # subsequent_indent=' '*4
                )
            ).str.join('\n'))
        if legend:
            mermaid_pie.index = mermaid_pie.index.str.split('(').str.get(0)
        _start_angle = start_angle - \
            20 if len(mermaid_pie) < 4 else start_angle
        fig = plt.figure(dpi=400, figsize=(5, 7), facecolor=background_color

                         )

        # ax = mermaid_pie.squeeze().plot(
        mermaid_pie.squeeze().plot(
            kind='pie', title=title, cmap=cmap,
            startangle=_start_angle,
            # rotatelabels=True,
            legend=False,
            xlabel='', ylabel='',
            autopct='{:,.0f}%'.format,
            wedgeprops={'linewidth': 2, },
            textprops=dict(color=pct_color, size=pct_size,
                           family='serif',
                           #   weight='bold'
                           ),
            labeldistance=label_distance,
            pctdistance=pct_distance

        )
        if legend:
            ax.legend(  # wedges, ingredients,
                title=unit.title(),
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))
        plt.show()
        fig.savefig(image_dir.joinpath(f'pie_{fstem}.{timestamp_today()}.pgf'),
                    dpi='figure', transparent=False,
                    bbox_inches='tight', pad_inches=0.2)


convert_mermaid_pies(cmap='deep_waters', pct_color='white',
                     background_color='grey',
                     pct_distance=0.85,
                     start_angle=0,
                     pct_size=8.5,
                     unit='category',
                     label_width=20,
                     label_distance=1.1)
# %%
convert_mermaid_pies(md_doc_path=Path.home().joinpath('justwriting/ch6_data.md'),
                     cmap='deep_waters', pct_color='white',
                     background_color='grey',
                     pct_distance=0.85,
                     start_angle=0,
                     pct_size=8.5,
                     unit='category',
                     label_width=20,
                     label_distance=1.1)
#%%
convert_mermaid_pies(md_doc_path=Path.home().joinpath('justwriting/ch3.md'),
                     cmap='deep_waters', pct_color='white',
                     background_color='grey',
                     pct_distance=0.85,
                     start_angle=0,
                     pct_size=8.5,
                     unit='category',
                     label_width=20,
                     label_distance=1.1)

# %%
