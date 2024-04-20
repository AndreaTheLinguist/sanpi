# %%
import contextlib
import itertools as it
from pprint import pprint
from re import findall as re_findall
from tabulate import tabulate
import matplotlib as mpl
import matplotlib.colors as mpc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps as mcm
from matplotlib.colors import LinearSegmentedColormap as gradient_cmap
from matplotlib.colors import ListedColormap as categorical_cmap
try:
    from source.utils.general import gen_random_array
except ModuleNotFoundError:
    from general import gen_random_array
from typing import Iterable, Sequence


def safe_register(cmap: (mpc.ListedColormap | mpc.LinearSegmentedColormap)
                  ) -> None:
    with contextlib.suppress(ValueError):
        mcm.register(cmap=cmap)


def partition_gradient(cmap: gradient_cmap, n_parts:int=4):
    return [cmap(x) for x in np.linspace(0.05, 0.95, n_parts)]

def _reverse_and_register(cmaps: Iterable,
                          verbose: bool = False) -> tuple:
    # if verbose:
    #     print(tabulate([[c.name, type(c)] for c in cmaps], tablefmt='fancy_grid'))
    reversed_cm = tuple(cm.reversed() for cm in cmaps)

    for cm in cmaps + reversed_cm:
        if verbose:
            print(f'+ registering "{cm.name}"')
        safe_register(cm)
    return tuple(reversed_cm)


def plot_color_gradients(category, colormaps: Sequence,
                         reverse_order: bool = False,
                         cmap_dict: dict = None,
                         return_dict: bool = False):
    _gradient = np.linspace(0, 1, 256)
    _gradient = np.vstack((_gradient, _gradient))
    if cmap_dict is None:
        cmap_dict = {}
    # Create figure and adjust figure height to number of colormaps
    nrows = len(colormaps)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)
    title = f'{category} colormaps'
    if reverse_order:
        title += ': reversed'
    axs[0].set_title(title, fontsize=14)

    for ax, name in zip(axs, colormaps):
        cmap = mcm[name]
        if reverse_order:
            cmap = cmap.reversed()
            name = cmap.name
        ax.imshow(_gradient, aspect='auto', cmap=cmap)
        ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    plt.show()

    # Save colormap list for later.
    if return_dict:
        cmap_dict[category] = colormaps
        return cmap_dict


def plot_examples(colormaps: list | tuple,
                  resample_n: int = None,
                  reverse_order: bool = False,
                  row_len: int = 4,
                  data_hist: bool = False) -> dict or None:
    """
    Helper function to plot data with associated colormap.
    """
    np.random.seed(
        int(f"{np.datetime64('now', 'h')}".replace('-', '').replace('T', '')))
    data = np.random.randn(30, 30)
    colormaps = list(colormaps)

    if resample_n:
        colormaps = (c.resampled(resample_n) for c in colormaps)
    if data_hist:
        plt.hist(data)
    for cm_grp in it.zip_longest(*[iter(colormaps)]*row_len):
        n = len(list(it.takewhile(lambda cm: cm is not None, cm_grp)))
        fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                                layout='constrained', squeeze=False)
        for [ax, cmap] in zip(axs.flat, cm_grp):
            stitle = str(cmap.name)

            if cmap is None:
                break
            if reverse_order:
                cmap = cmap.reversed()
            psm = ax.pcolormesh(
                data, cmap=cmap, rasterized=True, vmin=-3, vmax=3)
            ax.set(title=stitle)
            fig.colorbar(psm, ax=ax)
        plt.show()


def compare_maps(colormaps: Sequence = None,
                 with_reverse: bool = False,
                 data: np.ndarray = None,
                 floor: int = 0,
                 ceiling: int = 250,
                 verbose: bool = False):
    colormaps = colormaps or ['violet_seafoam',
                              'violet_seafoam_pink', 'violet_seafoam_dark']
    if data:
        floor = min(data.min())
        ceiling = max(data.max())
    else:
        data = list(gen_random_array(low=floor, high=ceiling))
        if verbose:
            print(tabulate(data, tablefmt='fancy_grid'))
        # data = np.random.randn(5, 5)
        # data = [[-16, -8, 0, 8, 16],
        #         [1, 2, 4, 10, 12],
        #         [-2, 1, 2, 4, 8],
        #         [-16, -4, 0, 1, 4]]
        # plt.hist(data)
    n = len(colormaps)
    fig, axes = plt.subplots(ncols=2 if with_reverse else 1,
                             nrows=n, figsize=(5, n * 3 + 3), layout='tight')

    def _create_plot(this_plot, colormap,  vmin=floor, vmax=ceiling):
        psm = this_plot.pcolormesh(data, cmap=colormap, rasterized=True,
                                   vmin=vmin, vmax=vmax)
        this_plot.set_title(colormap.name, fontfamily='Nimbus Roman')
        fig.colorbar(psm, ax=this_plot)

    for row_ix, cm in enumerate(colormaps):
        try:
            cmap = mcm[cm]
        except TypeError:
            cmap = cm
            cm = cmap.name
        if with_reverse:
            rev = cmap.reversed()
            for col_ix, c in enumerate([cmap, rev]):
                this_plot = axes[row_ix][col_ix]
                _create_plot(this_plot, c)
                # ax1[ax].imshow(data, cmap=cmap)
                # ax1[ax].set_title(cm)
                # ax2[ax].pcolormesh()
                # ax2[ax].imshow(data, cmap=rev)
                # ax2[ax].set_title(rev.name)
        else:
            this_plot = axes[row_ix]
            _create_plot(this_plot, cmap)

    plt.show()


def compare_resampling(cmap, sample_sizes=None):

    if sample_sizes is None:
        sample_sizes = [12, 9, 7, 6, 5, 4, 3]
    plot_examples([cmap] + [cmap.resampled(n) for n in sample_sizes])


def view_builtin_cmaps():

    # Sequential
    plot_color_gradients('Perceptually Uniform Sequential',
                         ['viridis', 'plasma', 'inferno', 'magma', 'cividis'])
    plot_color_gradients('Sequential',
                         ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                          'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                          'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'])
    plot_color_gradients('Sequential (2)',
                         ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                          'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                          'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'])

    # Diverging
    plot_color_gradients('Diverging',
                         ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                          'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'])

    # Cyclic
    plot_color_gradients('Cyclic', ['twilight', 'twilight_shifted', 'hsv'])

    # Qualitative
    plot_color_gradients('Qualitative',
                         ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                          'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'])
    # Miscellaneous
    plot_color_gradients('Miscellaneous',
                         ['flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                          'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                          'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                          'turbo', 'nipy_spectral', 'gist_ncar'])

    plt.show()


def view_categoricals(with_ex: bool = False):

    plot_color_gradients('New Categorical Colormaps',
                         list(CATEGORICAL_COLORS.keys()))

    if with_ex:
        plot_examples(list(CATEGORICAL_COLORS.values())[:2])
        plot_examples(list(CATEGORICAL_COLORS.values())[-2:])
        compare_resampling(list(CATEGORICAL_COLORS.values())[2], [5])


def view_gradients(with_ex: bool = False):
    new_gradient_names = list(GRADIENT_COLORS.keys())
    plot_color_gradients('New Gradient Colormaps', new_gradient_names)

    if with_ex:

        plot_examples(list(GRADIENT_COLORS.values())[:3])

        plot_examples(list(GRADIENT_COLORS.values())[3:6], reverse_order=True)

        compare_resampling(list(GRADIENT_COLORS.values())[-5], [12, 9, 5])


def _make_cmaps(colormaps: Iterable = None,
                gradient: bool = False,
                verbose: bool = False) -> dict:

    if colormaps:
        if verbose:
            print('colormaps iterable specified')
            plot_examples(colormaps)
        _cmaps = tuple(colormaps)

    elif gradient:
        _cmaps = (
            gradient_cmap.from_list(
                "lavender_teal",
                ["lavender", "purple", "xkcd:bright teal"]),
            gradient_cmap.from_list('deep_waters',
                                    ['xkcd:royal purple', "xkcd:night blue", "xkcd:ocean", "lightseagreen"]),
            gradient_cmap.from_list('purple_blue_green',
                                    ["#890091", "#3f6ea8", "#9fff96"]),
            gradient_cmap.from_list("purple_teal",
                                    ["purple", "violet", "xkcd:off white", "lightseagreen", "teal"]),
            gradient_cmap.from_list("light_rain",
                                    ["xkcd:barney purple", "violet", "pink", "lightgreen",
                                     "lightseagreen", "teal", "slateblue"]),
            gradient_cmap.from_list("myrain_bluer",
                                    ["purple", "magenta", "red", "orange", "yellow",
                                     "lightgreen", 'lightseagreen', "blue", "darkblue", "indigo"]),
            gradient_cmap.from_list("myrain_pinker",
                                    ["indigo", "purple", "magenta", "red", "orange",
                                     "yellow", "lightgreen", 'lightseagreen', "blue", "darkblue"]),
            gradient_cmap.from_list("myrain",
                                    ["purple", "magenta", "red", "orange", "yellow",
                                     "lightgreen", 'lightseagreen', "blue", "darkblue"]),
            gradient_cmap.from_list("myrain_split",
                                    ["darkviolet", "magenta", "red", "gold",
                                     "lightyellow", "lightgreen", 'lightseagreen', "blue", "darkblue"]),
            gradient_cmap.from_list("lisa_frank",
                                    ['xkcd:tiffany blue', 'xkcd:cerulean', 'xkcd:ultramarine', 'xkcd:purply pink', "xkcd:light rose"]),
            gradient_cmap.from_list("anastasia",
                                    ["xkcd:royal", 'xkcd:cerulean', 'xkcd:ice blue', 'w', 'xkcd:pale pink', "xkcd:medium pink", "purple"]),
            gradient_cmap.from_list("lilac_rose",
                                    ["xkcd:indigo", "xkcd:lilac", 'xkcd:off white', "xkcd:rose pink", "xkcd:dark rose"]),
            gradient_cmap.from_list("purple_rain",
                                    ["lavender", "violet", "purple", "indigo"]),
            gradient_cmap.from_list("blue_dark_pink",
                                    ["xkcd:robin's egg", 'xkcd:cerulean', 'xkcd:dark indigo', 'xkcd:purply pink', "xkcd:light rose"]),
            gradient_cmap.from_list("green_dark_purple",
                                    ['xkcd:celadon', 'xkcd:bluegreen', 'xkcd:dark indigo', 'xkcd:electric purple', 'xkcd:pale lavender']),
            gradient_cmap.from_list("blue_light_purple",
                                    ["darkblue", "blue", "cyan", "xkcd:pale grey", "pink", "magenta", "purple"]),
            gradient_cmap.from_list("blue_black_pink",
                                    ["cyan", "blue", "darkblue", "black", "purple",  "magenta", "pink"]),
            gradient_cmap.from_list("cerulean_royalty",
                                    ['xkcd:cerulean', 'xkcd:very light pink', 'xkcd:royal purple']),
            gradient_cmap.from_list("cerulean_royalty_dark",
                                    ['xkcd:light blue', 'xkcd:cerulean', 'xkcd:almost black', 'xkcd:royal purple', 'xkcd:lavender']),
            gradient_cmap.from_list("cerulean_royalty_dkbl",
                                    ['xkcd:light blue', 'xkcd:cerulean', 'xkcd:very dark blue', 'xkcd:royal purple', 'xkcd:lavender']),
            gradient_cmap.from_list("violet_seafoam",
                                    ['xkcd:violet', 'w', 'xkcd:seafoam']),
            gradient_cmap.from_list("violet_seafoam_dark", [
                'xkcd:violet', 'black', 'xkcd:seafoam']),
            gradient_cmap.from_list("violet_seafoam_pink",
                                    ['xkcd:violet', 'xkcd:medium pink', 'w', 'xkcd:seafoam', 'xkcd:deep green']),
            gradient_cmap.from_list("petrol_wine",
                                    ['xkcd:petrol', 'xkcd:pale grey', 'xkcd:wine']),
            gradient_cmap.from_list("petrol_wine_dark",
                                    ['xkcd:bright teal', 'xkcd:petrol', 'xkcd:deep blue', 'xkcd:wine', 'xkcd:dusty rose']),
            gradient_cmap.from_list("aqua_purple",
                                    ['xkcd:aqua', 'xkcd:very dark blue', 'xkcd:bright purple']),
            gradient_cmap.from_list("bruise",
                                    ['xkcd:light aqua', 'xkcd:deep blue', 'xkcd:lilac'])
        )
    else:
        _cmaps = (
            categorical_cmap(["purple", "gold", "teal"], name='mardi_gras'),
            categorical_cmap(
                ['xkcd:easter purple', 'purple', 'xkcd:purpley pink',
                 'xkcd:bubblegum pink', 'xkcd:light pink', 'xkcd:light salmon',
                 '#ffcc6e', "xkcd:lemon", 'lightgreen',
                 'xkcd:light sky blue', "xkcd:robin's egg",
                 'xkcd:cerulean blue', 'xkcd:royal'],
                name='easter'),
            categorical_cmap(
                ["xkcd:royal purple", "xkcd:barney purple", "xkcd:pale purple",
                 "xkcd:pale lilac", "xkcd:heather", "xkcd:silver", "xkcd:steel",
                 "xkcd:light grey blue", "xkcd:cornflower blue", "xkcd:marine",
                 "xkcd:aquamarine", "xkcd:light blue green",  "xkcd:green", "g",
                 "xkcd:lemon", "xkcd:pale gold",  "xkcd:sunflower", "xkcd:ecru"],
                name='catmap'),
            categorical_cmap(
                ['xkcd:pale green', 'lawngreen', 'xkcd:green',
                 'g', 'xkcd:deep green', 'xkcd:dark green',
                 'k', 'xkcd:charcoal', 'xkcd:silver', 'w'],
                name='green_kw'
            ),
            categorical_cmap(
                ['lawngreen', 'xkcd:green',
                 'g', 'xkcd:deep green', 'xkcd:dark green',
                 'k', 'xkcd:charcoal', 'xkcd:silver'],
                name='green_k'
            ),
            categorical_cmap(
                ['lawngreen', 'xkcd:green',
                 'xkcd:deep green',
                 'k', 'xkcd:charcoal', 'xkcd:silver'],
                name='green_k6'
            ),
            categorical_cmap(
                ["purple", "violet", "lightgreen", "lightseagreen", "teal"],
                name='little_mermaid'),
        )

    cm_dict = {c.name: c for c in (
        _cmaps + _reverse_and_register(_cmaps, verbose))}
    if verbose:
        compare_maps(list(cm_dict.values())[:2])
        compare_maps(list(cm_dict.values())[-2:])
    return cm_dict


# %%
CATEGORICAL_COLORS = _make_cmaps()
GRADIENT_COLORS = _make_cmaps(gradient=True)

# %%


def _get_smoothies():

    def _make_smoothies(n_colors: Sequence = None):
        n_colors = n_colors or [3, 4, 5, 6, 7, 8, 9, 10, 12]
        for cn, cm in CATEGORICAL_COLORS.items():
            if (len(cm.colors) <= min(n_colors)
                    and not str(cn).endswith(('_r', '6'))):

                yield gradient_cmap.from_list(name=f'{cn}_smoothie',
                                              colors=list(cm.colors))

        for n in n_colors:
            yield from _resample_smoothie(n)

    def _resample_smoothie(n):
        for cn, cm in CATEGORICAL_COLORS.items():
            if not cn.endswith(('_r', '6')) and len(cm.colors) > n:
                yield gradient_cmap.from_list(
                    name=f'{cn}{n}_smoothie',
                    colors=list(cm.resampled(n).colors)
                )

    return _make_cmaps(colormaps=_make_smoothies())


SMOOTHIES = _get_smoothies()


def view_smoothies(by_size: bool = False, by_colors: bool = True):

    plot_color_gradients('All "Smoothie"',
                         [name for name in SMOOTHIES.keys()
                          if not name.endswith('_r')])
    name_smash = '\n'.join(SMOOTHIES.keys())

    if by_size:
        unique_n = [int(x) if x else 0 for x in set(
            re_findall(r'[a-z_]+(.*)_smoothie', name_smash))]
        unique_n.sort()
        for n in unique_n:
            if n == 0:
                n = ''
            if n_smoothies := [
                name for name in SMOOTHIES.keys() if name.endswith(f'{n}_smoothie')
            ]:
                plot_color_gradients(f'{n} Ingredient "Smoothie"', n_smoothies)

    if by_colors:
        color_sets = list(set(re_findall(r'([a-z_]+).*_smoothie', name_smash)))
        color_sets.sort()
        for c in color_sets:
            if c_smoothies := [
                name for name in SMOOTHIES.keys() if name.startswith(c) and not name.endswith('_r')
            ]:
                plot_color_gradients(f'{c} "Smoothie"', c_smoothies)


# %%
GRADIENT_COLORS.update(SMOOTHIES)


def random_colormap_selection(selection_size: int = 1,
                              color_dict: dict = None, 
                              categories: bool = False
                              ) -> list | gradient_cmap | categorical_cmap:
    color_set = color_dict or (CATEGORICAL_COLORS if categories else GRADIENT_COLORS)
    options = list(color_set.values())
    random_indexer = []
    while len(random_indexer) < selection_size:

        random_indexer.extend(
            list(np.random.default_rng().integers(
                low=0, high=len(options)-1, size=selection_size - len(random_indexer))))
        random_indexer = list(set(random_indexer))
    random_indexer.sort()
    selection = [options[i] for i in random_indexer]
    return selection[0] if selection_size == 1 else selection


# %%[markdown]
# %%[markdown]
# ## To compare colormaps visually
#
# 1. `compare_maps()`
#
#    ```python
#    random_gmap = random_colormap_selection()
#    compare_maps([random_gmap,
#                random_gmap.resampled(7),
#                random_gmap.reversed()],
#                with_reverse=False)
#
#    compare_maps((random_gmap, random_gmap.resampled(5)), ceiling=50000)
#
#    random_2 = random_colormap_selection(selection_size=2)
#    compare_maps(random_2, ceiling=800000)
#
#    plot_color_gradients('5 random', [x.name for x in random_colormap_selection(5)])
#    compare_maps([(x.resampled(10)) for x in random_colormap_selection(5)], ceiling=50000)
#    ```
#
# 2. `view_*()`
#
#    ```python
#    view_builtin_cmaps()
#    view_categoricals(with_ex=True)
#    view_gradients(with_ex=True)
#    view_smoothies(by_size=False, by_colors=False)
#    ```
