# -*- coding=utf-8 -*-

# * Globals
# %%
# Imports
import contextlib
import errno
import itertools as it
import os
import re
from collections import namedtuple
from math import log, log1p, log2, sqrt
from pathlib import Path
from typing import NamedTuple

import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import colormaps as mcm
from matplotlib import font_manager as fm
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from source.utils import PKL_SUFF, SANPI_HOME, UCS_DIR, confirm_dir
from source.utils.colors import CATEGORICAL_COLORS as ListCmapDict
from source.utils.colors import GRADIENT_COLORS as GradCmapDict
from source.utils.colors import (compare_maps, partition_gradient,
                                 random_colormap_selection, view_categoricals,
                                 view_gradients)
from source.utils.dataframes import corners, print_md_table
from source.utils.general import find_glob_in_dir as seek_in_dir
from source.utils.general import (gen_random_array, print_iter, snake_to_camel,
                                  timestamp_now, timestamp_today)
from source.utils.metaspecs import AssocTable as AMT

KEEP = [
    # // 'index',
    'f',
    'l1',
    'l2',
    'E11',
    'unexpected_count',
    'unexpected_ratio',
    # // 'r_log_likelihood', 'r_log_likelihood_tt', 'r_odds_ratio_disc', 'r_Dice', 'r_t_score',
    # // 'r_p1_given2', 'r_p2_given1', 'r_p1_given2_simple', 'r_p2_given1_simple',
    # // 'r_p1_given2_margin', 'r_p2_given1_margin', 'r_expect_diff',
    # 'am_log_likelihood', #//'am_log_likelihood_tt',
    # // 'am_Dice', 'am_t_score',
    'am_p1_given2', 'am_p1_given2_simple', 'conservative_log_ratio', 'am_odds_ratio_disc',
    # 'dice',
    # 'joint_probability',
    # // 'am_p1_given2_margin', 'am_p2_given1_margin', 'am_expect_diff',
    # 'f1', 'N', #! These values can be found in `env_totals`
    'log_ratio',  # > really only included to provide some insight about what is "conservative" about `conservative_log_ratio`
    'am_p2_given1',
    'am_p2_given1_simple',
    # // 'O11', 'O12', 'O21', 'O22',
    # // 'R1', 'R2', 'C1', 'C2', 'E12', 'E21', 'E22',
    # 'z_score', 't_score',
    # 'log_likelihood',
    # // 'simple_ll', 'min_sensitivity', 'liddell',
    # // 'mutual_information', 'local_mutual_information', 'ipm', 'ipm_reference', 'ipm_expected',
    # 'f2', 'adv', 'adj', 'adv_total', 'adj_total' #! These values are in `adX`
]

# Color Shortcuts
AllCmapDict = dict(zip(
    it.chain(ListCmapDict.keys(), GradCmapDict.keys()),
    it.chain(ListCmapDict.values(), GradCmapDict.values())))


def select_cmap_by_size(size: int = 3):
    try:
        colormap = [n for n, c in ListCmapDict.items()
                    if len(list(c.colors)) == size
                    ][0]
    except IndexError:
        colormap = (tuple(m for m in ListCmapDict.values()
                          if len(m.colors) > size)
                    + tuple(GradCmapDict.values())
                    )[0].resampled(size)
    return colormap


COLOR1 = 'myrain_pinker_r'
COLOR2 = 'violet_seafoam_pink'
COLOR_CATX = 'catmap'
# COLOR_CAT3 = 'mardi_gras'
COLOR_CAT3 = select_cmap_by_size()
# COLOR_CAT4 = 'little_mermaid'
COLOR_CAT4 = select_cmap_by_size(4)
COLOR_CAT5 = select_cmap_by_size(5)
COLOR_CAT6 = select_cmap_by_size(6)
# compare_maps([COLOR1, COLOR2, COLOR_CAT3, COLOR_CAT4,
#              COLOR_CAT5, COLOR_CAT6, COLOR_CATX], ceiling=50000)

# pandas options
pd.set_option('display.max_colwidth', 25)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 200)
pd.float_format = '{:.2f}'.format

#! this is an externally created softlink to Andrea's local machine documents directory
#  ➡️ imports directly into dissertation chapter markdown files
_IMAGE_OUT = SANPI_HOME.joinpath('info/md_import_images')
if not _IMAGE_OUT.is_dir():
    print('Image output directory does not exist! No figures will be saved.')
    print(f'  ⨂ `{_IMAGE_OUT}/` not found')

# matplotlib options
# %%[markdown]
# _`matplotlib` available style sheets_
# ```python
# >> print(plt.style.available)
# ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
#
# >> plt.style.use('Solarize_Light2')
# ```
#
# _view available fonts in interactive terminal or notebook_ \
# (remove `!` to run in local terminal)
#
# ```shell
# !fc-list | cut -f2- -d: | column -t -s:
# ```
# > style sheets
# %%
# plt.style.use('Solarize_Light2')
# plt.style.use('seaborn-v0_8-deep')
# plt.style.use('seaborn-v0_8-darkgrid')
# plt.style.use('dark_background')
# plt.style.use('seaborn-v0_8-dark-palette')
# plt.style.use('seaborn-v0_8-dark')
# plt.style.use('_mpl-gallery-nogrid')
# plt.style.use('bmh')
# plt.style.use('seaborn-v0_8-pastel')
# plt.style.use('seaborn-v0_8-ticks')
plt.style.use('seaborn-v0_8-paper')
# plt.style.use('seaborn-v0_8-notebook')
# plt.style.use('seaborn-v0_8-whitegrid')
# plt.style.use('seaborn-v0_8-bright')

plt.rcParams['font.family'] = 'lato'
# plt.rcParams['font.family'] = 'serif'

# column filtering regex
regex_p_given_ONLY = r'p[12]\w+[12]$'
regex_l12_OR_p_given = r'^[^r]*[lp][12]($|\w+[\de]$)'
regex_l12_OR_p1_given2 = r'l\d|p1_given2'
regex_l12_OR_conserv = r'(l\d|conserv)'

# * Specify Data to Load
bgr_specs = specs = AMT('RBdirect', polar=True, ucs_show_floor=20)
bgr_specs.show(with_env_totals=True)

# adv_specs = AMT('RBdirect', polar=True,
#                        ucs_show_floor=200, lex_targets='adv')
# adv_specs.show()

# * Compare Polar Approximation Methods--Top Level


def make_env_comparison(compare_et):
    comparison_pairs = {'COMPLEMENT': 'POSMIR',
                        'NEGATED': 'NEGMIR',
                        'NEG_&_COM': 'NEG_&_POS'}
    for set_diff_pol, mirror_pol in comparison_pairs.items():
        # compare_et.at[set_diff_pol, 'reduction']=compare_et.at[mirror_pol, 'total_bigram_tokens'] - compare_et.at[set_diff_pol, 'total_bigram_tokens']
        compare_et.at[set_diff_pol,
                      'mirror_total_tokens'] = compare_et.at[mirror_pol, 'total_bigram_tokens']
        compare_et.at[set_diff_pol,
                      'mirror_relative_%'] = compare_et.at[mirror_pol, 'relative_%']

    flat_compare = compare_et.loc[compare_et.pol_approx_method == 'set_diff',
                                  compare_et.columns != 'pol_approx_method'].rename(
        index={'COMPLEMENT': 'not negated',
               'NEGATED': 'negated',
               'NEG_&_COM': 'TOTAL'
               })

    flat_compare['mirror_reduction'] = (
        flat_compare.mirror_total_tokens - flat_compare.total_bigram_tokens)
    flat_compare.loc[:, '%_of_reduction'] = (100 *
                                             flat_compare.mirror_reduction / flat_compare.mirror_reduction.at['TOTAL'])
    flat_compare['reduction_%_of_total'] = (100 *
                                            flat_compare.mirror_reduction / flat_compare.total_bigram_tokens).round(2)

    # flat_compare
    env_numbers = flat_compare.select_dtypes(include='number')
    flat_compare.loc['(not negated - negated)', env_numbers.columns] = (
        env_numbers.loc['not negated'] - env_numbers.loc['negated']
    )
    flat_compare = flat_compare.loc[[
        'negated', 'not negated', '(not negated - negated)', 'TOTAL'], :]
    flat_compare.index.name = 'data subset'
    flat_compare.columns = flat_compare.columns.str.replace('_', ' ')
    flat_reduction = flat_compare.loc[:,
                                      flat_compare.columns.str.contains('reduc')]
    flat_values = flat_compare.loc[:, ~
                                   flat_compare.columns.isin(flat_reduction.columns)]
    env_compare_title = '_Relative Environment Data Size Discrepancies by Polarity Approximation Method_\n\n'
    env_compare_tables = '\n'.join([print_md_table(
        flat_df,
        n_dec=2,
        suppress=True,
    ) for flat_df in (flat_values, flat_reduction)])
    env_compare_view = env_compare_title + \
        env_compare_tables.replace('.00', '   ')
    print(env_compare_view)

    env_compare_path = SANPI_HOME.joinpath(
        'info/md_import_tables/env-margins_pol-approx-methods.md')
    if not env_compare_path.is_file():
        env_compare_path.write_text(
            env_compare_view
        )
    return compare_et, flat_compare, flat_values


compare_et, flat_compare, flat_values = make_env_comparison(
    pd.concat((specs.collect_l1_totals(other=tv, verbose=False)
               for tv in (False, True))
              ).sort_values('pol_approx_method', ascending=False))


def barchart_env_totals(token_totals_by_env):
    fig, (upper, lower) = plt.subplots(nrows=2, ncols=1, dpi=300,
                                       figsize=[7, 5], layout='constrained')
    # token_totals_by_env['set_diff tokens'].T.plot(ax=p_left,
    #     kind='bar', rot=0, cmap='mardi_gras')
    # token_totals_by_env['mirror tokens'].T.plot(ax=p_right,
    #     kind='bar', rot=0, cmap='mardi_gras_r')

    # token_totals_by_env.T.plot.bar(rot=0, cmap='little_mermaid', figsize=[3, 14])
    token_totals_by_env.columns = token_totals_by_env.columns.str.replace(
        ' tokens', '')
    token_totals_by_env.columns.name = 'method   results'
    token_totals_by_env.index.name = 'approximated polarity'
    fig.suptitle('Size Discrepancy between Polarity Approximation Methods',
                 fontsize='13', color='k', fontstyle='italic')
    t_df = token_totals_by_env.transpose()

    fig = t_df.plot.barh(
        logx=False, rot=0, cmap=COLOR_CAT3, ax=upper, xlabel='raw bigram token totals')
    fig = t_df.plot.barh(
        logx=True, rot=0, cmap=COLOR_CAT3, ax=lower, xlabel='log scaled bigram token totals')

    plt.savefig(_IMAGE_OUT.joinpath(
        f'barh_compare_approx_meth.{timestamp_now()}.png'))


def make_env_totals_pie(flat_values, N_vals):
    colors = {'pies': (['xkcd:pale green', 'xkcd:pastel blue',],
                       ['xkcd:pale pink', 'xkcd:lilac',]),
              'labels': ['xkcd:night blue', 'xkcd:wine']}
    pie_counts = flat_values.filter(like='tokens').T.reset_index(drop=True).T
    pie_percents = flat_values.filter(
        like='relative').T.reset_index(drop=True).T

    pie_labels = pie_counts.copy()
    for col_axis in pie_labels.columns:
        for ix in pie_labels.index:
            pie_labels.at[ix, col_axis] = \
                f'{pie_counts.at[ix, col_axis]:,.0f}\n{ix}'

    startangs = [120, 100]
    fig, ax_array = plt.subplots(nrows=1, ncols=2, dpi=300,
                                 figsize=[7, 5], layout='constrained')
    fig.suptitle('Relative Environment Totals by Polarity Approximation',
                 fontsize='13', color='k', fontstyle='italic')

    for col_axis in pie_counts.columns:
        labels = pie_labels[col_axis]
        counts = pie_counts[col_axis]
        ax_array[col_axis].pie(
            counts,
            colors=colors['pies'][col_axis],
            labels=labels, autopct='%1.1f%%',
            pctdistance=.7, labeldistance=1.2,
            startangle=startangs[col_axis],
            textprops=dict(color=colors['labels'][col_axis],
                           size=10, weight="bold", fontfamily='monospace'))

        pat_cat = flat_values.filter(
            like="tokens").columns[col_axis].replace(' tokens', '')
        subplot_title = (("present" if pat_cat == "mirror" else "absent")
                         + f' trigger ({pat_cat})\nN={N_vals[col_axis]:,.0f}')
        # ax_array[col_axis].suptitle(
        #     subplot_suptitle,
        #     loc='center', fontsize='11', va='top',
        #     color=colors['labels'][col_axis])
        ax_array[col_axis].set_title(
            subplot_title,
            loc='center', fontsize='10', fontfamily='monospace', va='top',
            color=colors['labels'][col_axis], linespacing=1.5)
        # ^ # TODO try this as nested pie or bar of pie plot as in https://matplotlib.org/stable/gallery/pie_and_polar_charts/index.html#pie-and-polar-charts
    # plt.show()
    # HACK: uncomment to refresh pie chart image file
    plt.savefig(SANPI_HOME.joinpath(
        f'info/md_import_images/pie_env_totals_by_approx.{timestamp_now()}.png'))


def visualize_env_totals(flat_values):

    N_vals = flat_values.filter(
        like='tokens').T.reset_index().TOTAL.astype('uint').to_list()
    flat_values = (
        flat_values.filter(regex=r'^n', axis=0)
        .rename(columns={'total bigram tokens': 'set_diff tokens',
                         'mirror total tokens': 'mirror tokens'}))

    make_env_totals_pie(flat_values, N_vals)

    barchart_env_totals(flat_values.filter(like='tokens'))

# HACK: uncomment to create visuals
# visualize_env_totals(flat_values.copy())

# %% [markdown]
# ## Preparing the Association Table

# %%
# * Load & Prep Table


def load_assoc(specs):
    amdf = pd.read_pickle(specs.pkl_path)
    am_full = amdf.copy()
    other_df = pd.read_pickle(specs.other_method_path)
    other_full = other_df.copy()

    def _adjust_df(df):
        _df = df.copy()
        if 'unexpected_count' not in _df.columns:
            if any(_df.filter(like='unexpected')):
                _df = _df.rename(columns={'unexpected_f': 'unexpected_count'})
            else:
                _df = _df.rename(
                    columns={'am_expect_diff': 'unexpected_count'})

        _df = _df[[k for k in KEEP if k in _df.columns]]
        #! This is required to deal with some strangeness around `float32` dtype versus `float64` that was interfering with rounding
        float32 = _df.select_dtypes(include='float32').columns
        _df[float32] = _df[float32].astype('float64')

        _df[['l1', 'l2']] = _df[['l1', 'l2']].astype('string')
        _df.update(_df.select_dtypes(include='float')
                   # .apply(round, ndigits=3)
                   .round(3)
                   )
        return _df

    amdf = _adjust_df(amdf)
    other_df = _adjust_df(other_full)

    return amdf, am_full, other_df, other_full


amdf, full_amdf, other_df, full_other = load_assoc(specs)

amdf
# %%
other_df
# %%


def pivot_metric(df,
                 metric: str = 'conservative_log_ratio',
                 index='l2',
                 columns='l1'):
    if metric is None:
        metric = 'conservative_log_ratio'
    return df.pivot(values=metric, index=index, columns=columns)


def compare_approx_by_metric(df1: pd.DataFrame,
                             df2: pd.DataFrame,
                             metric: str = None) -> pd.DataFrame:
    pvdf = pivot_metric(df1, metric).join(pivot_metric(df2, metric))
    return pvdf[[c.upper() for c in ['negated', 'complement', 'negmir', 'posmir'] if c in pvdf.columns.str.lower()]]


pivot_conservative_lr = compare_approx_by_metric(amdf, other_df)
pivot_conservative_lr
# %%


def get_4_colors(color_base=None):
    return partition_gradient(random_colormap_selection(color_dict=color_base), 5)[:4]


def pivot_hist_together(pivot_df, metric):
    plt.style.use('dark_background')
    colors4 = get_4_colors(GradCmapDict)
    fig, (ax1, ax2) = plt.subplots(dpi=300,
                                   nrows=1, ncols=2, sharex=True, figsize=[8, 5],
                                   layout='tight')
    fig.suptitle(
        f'{metric} distributions by environment'.capitalize(), fontstyle='italic')
    ax1.hist(pivot_df, color=colors4,
             label=pivot_df.columns.to_list())
    ax1.legend(loc='best', fontsize=8, title='environment')
    ax1.set_title('Raw', fontfamily='monospace', fontweight='bold')

    ax2.hist(pivot_df, log=True, color=colors4,
             label=pivot_df.columns.to_list())
    # ax2.legend()
    ax2.set_title('Log', fontfamily='monospace', fontweight='bold')

    plt.savefig(_IMAGE_OUT.joinpath(
        f'hist_byEnv_log-vs-raw_{snake_to_camel(metric.replace(" ", "_"))}.{timestamp_now()}.png'))


pivot_hist_together(pivot_conservative_lr.copy(), 'conservative log ratio')


def pivot_pdf(pivot_df, metric):
    plt.style.use('dark_background')

    colors2 = partition_gradient(random_colormap_selection(), 3)[:2]

    _min = min(pivot_df.min())
    _max = max(pivot_df.max())
    fig, axes = plt.subplots(dpi=300, sharex=True,
                             nrows=1, ncols=2, figsize=[8, 5], sharey=True,
                             layout='tight')
    fig.suptitle(
        f'{metric} densities by polarity approximation method'.capitalize(), fontstyle='italic', fontfamily='serif')
    for ix, (method, cols) in enumerate(
        {'set_diff': ['NEGATED', 'COMPLEMENT'],
         'mirror': ['NEGMIR', 'POSMIR']}.items()):
        ax = axes[ix]
        ax.hist(pivot_df[cols], color=colors2, rwidth=1,
                label=['negated', 'not negated'], density=True, stacked=False, bins=16,
                range=(_min, _max))
        ax.legend(loc='best', fontsize=8.5, title='approximated polarity')
        ax.set_title(method, fontfamily='monospace', fontweight='bold')

    plt.savefig(_IMAGE_OUT.joinpath(
        f'hist_densityByPolApprox_{snake_to_camel(metric.replace(" ", "_"))}.{timestamp_now()}.png'))


pivot_pdf(pivot_conservative_lr.copy(), 'conservative log ratio')


# %%
def pivot_hist(pivot_df, metric):
    plt.style.use('dark_background')
    pivot_df.columns = (
        snake_to_camel(metric.replace("ative", "").replace("ratio", "r"))
        + ': ' + pivot_df.columns)
    color_dict = dict(
        zip(pivot_df.columns, get_4_colors()))
    _min = min(pivot_df.min())
    _max = max(pivot_df.max())

    def make_hists(df, name, same_y, color_dict):
        sz = [6.5, 4]
        fig, axes = plt.subplots(
            ncols=2, dpi=300, sharex=True, sharey=same_y, figsize=sz, layout='tight')
        fig.suptitle(f'{name} comparison of {metric.replace("_", " ")} ({"log" if same_y else "raw"})'.capitalize(),
                     fontstyle='italic', fontfamily='serif')
        for i, env in enumerate(df.columns):
            ax = axes[i]
            ax.hist(df[env], log=same_y,
                    color=color_dict[env],
                    range=(_min, _max)
                    )
            ax.set_title(env, fontfamily='monospace')
        plt.savefig(_IMAGE_OUT.joinpath(
            f'hist_env-subplots_{snake_to_camel(metric)}-{"log" if same_y else "raw"}'
            f'_{snake_to_camel(name.replace(" ", "_"))}.{timestamp_now()}.png'))
        plt.show()

    for same_y in (True, False):
        for name, filter_df in [
            ('negated', pivot_df.filter(like='NEG')),
            ('not negated', pivot_df.filter(regex=r': [^N]')),
            ('trigger presence', pivot_df.filter(like='MIR')),
                ('trigger absence', pivot_df.filter(regex=r'[^R]$'))]:

            make_hists(filter_df, name, same_y, color_dict)


pivot_hist(pivot_conservative_lr.copy(), 'conservative_log_ratio')

# %% [markdown]
# TODO # [ ] set up loop to run pivots and different plots on selection of metrics, e.g. `am_p1_given2`, `am_p1_given2_simple`, `unexpected_ratio`?
# %%
pivot_p1_given2 = compare_approx_by_metric(amdf, other_df, 'am_p1_given2')
pivot_p1_given2.info()
pivot_hist(pivot_p1_given2)
# %% [markdown]
# ## Plotting Association Measures

# bigrams are a greater predictor of polarity than polarity is of specific bigrams.
# This makes sense given the huge variability within the bigram set.
#

# ```python
# p_given = amdf.copy().filter(regex=regex_p_given_ONLY)
# p_given.copy().sort_values('am_p1_given2').reset_index().plot(
#     rot=-25, title='sorted by p1_given2')
# ```


# %%
color = mcm['myrain_pinker_r'].resampled(7)
full_amdf.plot(kind='scatter',  c=full_amdf.f.apply(log), cmap=color,
               y='am_p1_given2', ylabel='polarity | bigram',
               x='am_p2_given1', xlabel='bigram | polarity',
               rot=25, title='Adjusted Conditional Probability Comparison\n**unrounded**')

amdf.plot(kind='scatter',  c=amdf.f.apply(log), cmap=color,
          y='am_p1_given2', ylabel='polarity | bigram',
               x='am_p2_given1', xlabel='bigram | polarity',
               rot=25, title='Adjusted Conditional Probability Comparison\n_rounded_')

# full_amdf.plot(kind='scatter', grid=True,  c=amdf.f.apply(log2), cmap=color,
#    x='am_p1_given2', y='am_p1_given2_simple',
#    rot=25, title='**unrounded**')


# %%
def plot_y_by_xs(xs, y, df, polarity, color='myrain_pinker_r', color_scale='f'):
    for x in xs:
        df.plot(kind='scatter', grid=True,
                x=x, y=y,
                # c=df[y],
                # # colormap='twilight_shifted',
                # # colormap='RdBu_r',
                # colormap='coolwarm',
                # > this maps the marker to a color according to the **magnitude**, regardless of sign
                c=(df[color_scale]**2).apply(log) if color_scale else df[y].abs(),
                colormap=color,
                rot=25,
                title=f'{polarity.capitalize()} `{y}` \nby `{x}`\n (color scale: `{color_scale}`)')


def illustrate_by_pol(polarity, df,
                      #   color='BuPu'
                      #   color='Wistia',
                      # color='autumn_r',
                      #   color='PuBuGn',
                      # color='hot',
                      #   color='turbo',
                      color='light_rain',
                      x_axes=None,
                      y_axes=None,
                      color_scale=None
                      ):
    x_df = (df.filter(items=x_axes).sort_values(x_axes[0]) if x_axes
            else df.filter(like='p1_given2').sort_values('am_p1_given2'))
    x_axes = x_df.columns.to_list()
    # if len(x_axes) > 1 :
    #     x_df.plot(
    #         grid=True,
    #         # cmap='PiYG',
    #         # cmap='brg',
    #         # cmap='Set1',
    #         # cmap='bwr',
    #         cmap='winter',
    #         # cmap= mpl.colormaps['viridis'].resampled(2),
    #         rot=25, title=f'{polarity.capitalize()} \n {", ".join(x_axes)}')
    # else:
    #     x_df.hist(grid=True)

    color_scale = color_scale or (
        [c for c in ('f_sqrt', 'f', 'bigram_total', 'f2_sqrt', 'f2',
                     'adv_total') if c in df.columns]
        + [None]
    )[0]
    for y in y_axes or ['conservative_log_ratio',
                        'am_odds_ratio_disc', 'log_ratio']:
        plot_y_by_xs(x_axes,
                     y, df, polarity, color,
                     color_scale=color_scale
                     )


# illustrate_by_pol('(any)', amdf.copy().reset_index())
illustrate_by_pol('(any)', full_amdf.copy().reset_index(),
                  color=COLOR1, color_scale='f2_sqrt')

# %%

for p, df in amdf.groupby('l1'):
    color_f = mcm['bruise_r' if p.startswith(
        'NEG') else 'lisa_frank'].resampled(7)
    color_f2 = mcm['light_rain' if p.startswith(
        'NEG') else 'lavender_teal'].resampled(7)
    illustrate_by_pol(p, df, color=color_f,
                      x_axes=['am_p1_given2'], y_axes=['conservative_log_ratio'],
                      color_scale='f')
    illustrate_by_pol(p, df.assign(f2=df.index.to_series().apply(lambda i: full_amdf.f2[i])),
                      color=color_f2,
                      x_axes=['am_p1_given2'], y_axes=['conservative_log_ratio'],
                      color_scale='f2')
    illustrate_by_pol(p, df, color=color_f,
                      x_axes=['am_p1_given2'], y_axes=['unexpected_count'],
                      color_scale='f')
    illustrate_by_pol(p, df.assign(f2=df.index.to_series().apply(lambda i: full_amdf.f2[i])),
                      color=color_f2,
                      x_axes=['am_p1_given2'], y_axes=['unexpected_count'],
                      color_scale='f2')

# %%
for p, df in full_amdf.groupby('l1'):
    color_lrc = mcm['inferno' if p.startswith(
        'NEG') else 'Blues'].resampled(9)
    color = 'xkcd:wine' if p.startswith('NEG') else 'xkcd:cerulean blue'
    illustrate_by_pol(p, df,
                      color=color_lrc,
                      y_axes=['conservative_log_ratio', 'am_p1_given2', 'am_p1_given2_simple'], x_axes=['f_sqrt'],
                      color_scale='f2_sqrt')
    df.filter(regex=r'o\w+ratio').hist(color=color, sharey=True)
    df.filter(regex=r'sqrt$').hist(color=color, sharey=True)
    df.filter(regex=r'given2[^a]*$').hist(color=color,
                                          sharey=True, sharex=True)


# %% [markdown]
# ## Split table by polarity env (`l1`)

# %%
pols = list(amdf.l1.astype('string').unique())
pol_split = {p: pf.set_index('l2') for p, pf in amdf.copy().filter(
    regex=r'^.([^d]|$)').groupby('l1')}
corners(pol_split[pols[0]], 4)

# %%
# sourcery skip: use-fstring-for-concatenation
for p, pf in pol_split.items():
    pf.drop('l1', axis=1, inplace=True)
    pf.columns = pf.columns + f'_{p[:3]}'
    pol_split[p] = pf
corners(pol_split[pols[0]], 3)

# %%
corners(pol_split[pols[1]])

# %%
by_pol = (pd.DataFrame(index=amdf.l2.unique())
          .join(pol_split[pols[0]])
          .join(pol_split[pols[1]])
          .sort_index(axis=1))

adX_pol = by_pol.join(specs.adX)


def filter_row(df, filter_like: str = None,
               filter_regex: str = None,
               filter_items: list = None):
    if filter_like:
        df = df.filter(like=filter_like, axis=0)
    if filter_regex:
        df = df.filter(regex=filter_regex, axis=0)
    if filter_items:
        df = df.filter(items=filter_items, axis=0)
    return df

# exactly = filter_row(adX_pol, filter_like='exactly')
# pretty = filter_row(adX_pol, filter_like='pretty')


def make_hists(_df, transform: bool = True):

    plt.figure(dpi=260)
    # plt.title(label='Comparing Distributions')
    if transform:
        for col in _df.columns:
            c_df = _df.copy()[[col]]
            print_md_table(c_df, describe=True, n_dec=1)
            c_mean = _df[col].mean()
            c_df[f'{col}: mean_std'] = c_df[col].squeeze() - c_mean
            c_df[f'{col}: abs'] = c_df[col].abs()
            with contextlib.suppress(ValueError):
                c_df[f'{col}: log2'] = c_df[col].add(1).apply(log2)
            # c_df[f'{col}: log'] = c_df[col].add(1).apply(log)

            print_md_table(c_df, describe=True, n_dec=1)
            c_df.hist(sharey=True, bins=8)
    else:
        _df.hist(bins=8, sharey=True)

# amdf.filter(items=['am_p1_given2', 'conservative_log_ratio', 'unexpected_count', 'unexpected_ratio']).apply(lambda c: c - c.mean()).hist()


# make_hists(amdf.filter(like='given2'), True)
make_hists(amdf.filter(items=[
           'am_p1_given2', 'conservative_log_ratio', 'am_p1_given2_simple']), True)

# %%


def hist_by_pol(df, filter_row_like: str = '', filter_row_regex: str = '',
                metrics: list = None, transform: bool = True):
    metrics = metrics or ['am_p1_given2',
                          'conservative_log_ratio']
    filter_given = filter_row_like or filter_row_regex
    if filter_given:
        _df = filter_row(df.copy(), filter_row_like, filter_row_regex)
    if 'l1' in _df.columns:
        for l1, l1_df in _df.groupby('l1'):
            l1_df = l1_df.filter(items=metrics)
            l1_df.columns = l1[:3] + '-' + l1_df.columns
            make_hists(l1_df)
    else:
        make_hists(_df.filter(regex=r'|'.join(metrics)))

        # title=f'\nl'\n'.join([filter_like, filter_regex])}'


# hist_by_pol(adX_pol, filter_row_like='very')
# %% [markdown]
# _slightly_ Bigrams
# %%
hist_by_pol(amdf, filter_row_like='~slightly_',
            metrics=['am_p1_given2', 'conservative_log_ratio']
            )


# %%
hist_by_pol(amdf, filter_row_like='~exactly_')

# %%
pretty.info()

# %%
fairly.hist(['am_p1_given2_NEG', 'conservative_log_ratio_NEG',
            'am_p1_given2_simple_NEG', 'log_ratio_NEG'])

# %%
adX_pol.sort_values('adv_total')

# %%
adX_pol.filter(regex='given2_simple_[CN]').hist(sharex=True, bins=20)
adX_pol.filter(regex='given2_simple_[CN]').hist(
    sharex=True, sharey=True, bins=20)


# %%
adX_pol.filter(regex='given2_[CN]').hist(sharex=True, bins=20)
adX_pol.filter(regex='given2_[CN]').hist(sharex=True, sharey=True, bins=20)


# %%
adX_pol.filter(regex='given2_[CN]').hist(sharex=True, bins=20)
adX_pol.filter(regex='given2_simple_[CN]').hist(sharex=True, bins=20)


# %%
adX_pol.filter(regex='given2_[CN]').abs().hist(sharex=True)

# %%
adX_pol.filter(regex='given2_[CN]').hist(sharey=True, sharex=True)

# %%
amdf.filter(like='COM~', axis=0).nlargest(20, columns=['am_p1_given2'])


# %%
amdf.hist(['conservative_log_ratio', 'am_p1_given2', 'am_p1_given2_simple'])

# %%
adX_pol.filter(like='conserv').copy(
).fillna(-20).sort_values('conservative_log_ratio_NEG')

# %%
full_amdf.filter(like='COM~', axis=0).loc[~full_amdf.adv.isin(
    ['not', "n't", 'never', 'hardly', 'no', 'none', 'rarely']), KEEP].nlargest(20, columns=['conservative_log_ratio'])


# %%
# amdf.filter(like = 'COM~exactly_', axis=0).nlargest(20, columns=['conservative_log_ratio'])
amdf.filter(like='COM~exactly_', axis=0).nsmallest(
    20, columns=['conservative_log_ratio'])


# %%
amdf.filter(like='pretty_', axis=0).nsmallest(
    20, columns=['am_p1_given2_simple'])


# %%
amdf.filter(like='COM~pretty_', axis=0).nlargest(
    20, columns=['conservative_log_ratio'])


# %%
# from source.utils.sample import sample_pickle as spkl
# hits_path

# %%


# %%
adX_pol.filter(like='exactly_', axis=0).nlargest(
    20, columns=['am_p1_given2_NEG'])

# %%
adX_pol.copy().filter(regex=r'given2_[NC]').fillna(0).plot()

# %%
adX_pol.copy().filter(regex=r'given2_[NC]').sort_values(
    'am_p1_given2_NEG').abs().plot()

# %%
# plot:
adX_pol.copy().filter(regex=r'given2_[NC]').abs().hist(['am_p1_given2_NEG', 'am_p1_given2_COM'], bins=8
                                                       )

# fig, ax = plt.subplots()
# ax.hist2d(adX_pol.f_NEG.fillna(0).apply(sqrt),
#           adX_pol.adv_total.fillna(0).apply(sqrt))

# # ax.set(xlim=(-2, 2), ylim=(-3, 3))

# plt.show()

# %%
for metric in ['conservative_log_ratio', 'am_p1_given2', 'unexpected_ratio']:
    illustrate_by_pol(df=adX_pol, x_axes=[f'{metric}_NEG'], y_axes=[
                      f'{metric}_COM'], polarity='(split)')
    illustrate_by_pol(df=adX_pol, x_axes=[f'{metric}_{p}' for p in ('NEG', 'COM')], y_axes=[
                      'adv_total', 'adj_total', 'bigram_total'], polarity='(split)')

# %%
sorter = 'am_p1_given2'
l_OR_p1_given2 = amdf.copy().filter(regex=regex_l12_OR_p1_given2).assign(
    abs_p1_given2=amdf.am_p1_given2.abs())
for polarity, polar_bigrams in (l_OR_p1_given2
                                .sort_values(sorter)
                                .groupby('l1')):

    polar_bigrams.copy().set_index('l2').plot(
        rot=25, title=f'{polarity} set\n(sorted by `{sorter}`)')

# %%
sorter = 'am_p1_given2_simple'
for polarity, polar_bigrams in (l_OR_p1_given2
                                .sort_values(sorter)
                                .groupby('l1')):

    polar_bigrams.copy().set_index('l2').plot(
        rot=25, title=f'{polarity} set\n(sorted by `{sorter}`)')

# %%

sorter = 'conservative_log_ratio'
for polarity, polar_bigrams in (amdf.filter(regex=regex_l12_OR_conserv)
                                .sort_values(sorter)
                                .groupby('l1')):

    polar_bigrams.copy().set_index('l2').plot(
        rot=25, title=f'{polarity} set\n(sorted by `{sorter}`)')

# %%
amdf.hist(['log_ratio', 'conservative_log_ratio', 'am_odds_ratio_disc'])

# %%
amdf.am_p1_given2.hist()
amdf.am_p1_given2_simple.hist()

# %%
n_acp12 = adX_pol.copy()[['am_p1_given2_NEG']].rename(
    columns={'am_p1_given2_NEG': 'acp'})
n_acp12 = n_acp12.assign(
    acp_abs=n_acp12.acp.abs(),
    acp_sq=n_acp12.acp ** 2,
    acp_mean_std=n_acp12.acp - n_acp12.acp.mean()
)
n_acp12.hist()
