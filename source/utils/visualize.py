# coding=utf-8
from pathlib import Path
import matplotlib.pyplot as plt
from .general import confirm_dir
import pandas as pd


# def heatmap(df,
#         columns=None,
#         save_name=None,
#         size=(8, 10),
#         save_dir: Path = None,
#         margin_name:'str'='SUM'):
# #TODO: update this with code from `explore_stats.ipynb`
# plt.figure(figsize=size, dpi=100, facecolor="white")
# sum_col = pd.Series(dtype='uint64')
# # sum_row = pd.Series()
# if margin_name in df.columns:
#     sum_col = df.loc[df.index != margin_name, margin_name]
# if margin_name in df.index:
#     sum_row = df.loc[margin_name, df.columns != margin_name]
# df = df.loc[df.index != margin_name, df.columns != margin_name]
# #! #BUG:  `row_labels` are not appearin as tick marks
# row_labels = df.index.to_series()
# if not sum_col.empty:
#     row_labels = row_labels + ' (' + sum_col.astype('string') + ')'
# if columns:
#     df = df.loc[:, columns]
# df = df.astype('float')
# # Displaying dataframe as an heatmap
# # with diverging colourmap as RdYlBu
# # plt.imshow(df, cmap="RdYlBu")
# plt.imshow(df, cmap="viridis")
# plt.autoscale(enable=True, axis='both')
# # Displaying a color bar to understand
# # which color represents which range of data
# plt.colorbar()

# # Assigning labels of x-axis
# # according to dataframe
# plt.xticks(range(len(df.columns)), df.columns)

# # Assigning labels of y-axis
# # according to dataframe
# plt.yticks(range(len(df.index)), row_labels)
# # TODO: add `rotation=20` etc. to plot
# # Displaying the figure
# plt.show()


def heatmap(df,
            columns=None,
            size=(8, 10),
            dpi=130,
            save_name=None,
            save_dir: Path = None,
            colormap="plasma",
            title: str = 'Frequency Heatmap'):

    plt.figure(figsize=size, dpi=dpi, facecolor="white")

    if columns:
        df = df.loc[:, columns]
    df = df.astype('float')
    # Displaying dataframe as an heatmap
    # with diverging colourmap as RdYlBu

    plt.imshow(df, cmap=colormap)
    # plt.imshow(df, cmap="gist_rainbow")
    # plt.imshow(df, cmap="jet")
    # plt.imshow(df, cmap="viridis")
    # plt.autoscale(enable=True, axis='both')
    # Displaying a color bar to understand
    # which color represents which range of data
    plt.colorbar()
    # Assigning labels of x-axis
    # according to dataframe
    plt.xticks(range(len(df.columns)), df.columns, rotation=-70)

    # Assigning labels of y-axis
    # according to dataframe
    plt.yticks(range(len(df.index)), df.index)
    plt.title(title)
    # Displaying the figure
    plt.show()

    # * ^ above code copied from notebooks where this was updated (transform_freqs.ipynb and compare_bigram-directNEG.ipynb)

    if save_name:
        if save_dir is None:
            save_dir = Path.cwd().joinpath('images')
        confirm_dir(save_dir)
        save_path = save_dir.joinpath(save_name)
        plt.savefig(save_path, dpi=300)
        print(f'Heatmap saved to:\n  {save_path}')


def plot_barh(sample_df: pd.DataFrame,
              chart_name: str,
              stacked: bool = False,
              color: str = 'gist_rainbow',
              dpi: int = 120):

    fig = plt.figure(dpi=dpi)
    sample_df.plot(kind='barh',
                   stacked=True,
                   width=0.8,
                   figsize=(8, 10),
                   position=1,
                   title=chart_name,
                   grid=True,
                   colormap=color,
                   ax=plt.gca()
                   )
    plt.show()
