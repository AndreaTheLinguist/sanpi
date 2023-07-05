# coding=utf-8
from pathlib import Path
import matplotlib.pyplot as plt


def heatmap(df,
            columns=None,
            save_name=None,
            size=(8, 10),
            save_dir: Path = None):

    plt.figure(figsize=size, dpi=100, facecolor="white")
    margin_name = 'SUM'
    try:
        totals = df.pop(margin_name)
    except AttributeError:
        margin_name = 'total_count'
        try:
            totals = df.pop(margin_name)
        except AttributeError:
            margin_name = 'All'
            try:
                totals = df.pop(margin_name)
            except AttributeError:
                totals = df.sum(axis=1)
            else:
                # `margin_name` -> 'All'
                rows = df.index != margin_name
                totals = totals[totals.index != margin_name]
        else: 
            # `margin_name` -> 'total_count'
            rows = df.index != margin_name
            totals = totals[totals.index != margin_name]
    else: 
        # `margin_name` -> 'SUM'
        rows = df.index != margin_name
        totals = totals[totals.index != margin_name]

    df = df.loc[rows, :]
    row_labels = df.index + ' (' + totals.astype('string') + ')'
    if columns:
        df = df.loc[:, columns]
    df = df.astype('float')
    # Displaying dataframe as an heatmap
    # with diverging colourmap as RdYlBu
    # plt.imshow(df, cmap="RdYlBu")
    plt.imshow(df, cmap="viridis")
    plt.autoscale(enable=True, axis='both')
    # Displaying a color bar to understand
    # which color represents which range of data
    plt.colorbar()

    # Assigning labels of x-axis
    # according to dataframe
    plt.xticks(range(len(df.columns)), df.columns)

    # Assigning labels of y-axis
    # according to dataframe
    plt.yticks(range(len(df.index)), row_labels)

    # Displaying the figure
    plt.show()

    if save_name:
        if save_dir is None:
            save_dir = Path.cwd().joinpath('images')
        if not save_dir.is_dir():
            save_dir.mkdir(parents=True)
        save_path = save_dir.joinpath(save_name)
        plt.savefig(save_path, dpi=300)
        print(f'Heatmap saved to:\n  {save_path}')