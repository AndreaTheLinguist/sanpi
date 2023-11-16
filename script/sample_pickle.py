# coding=utf-8
import argparse
from pathlib import Path

import pandas as pd

from utils import set_pd_display

# pd.set_option('display.max_colwidth', 40)
# pd.set_option('display.max_columns', 20)
# pd.set_option('display.width', 200)


def print_sample():
    """
    prints a sample from a pickled DataFrame based on command line arguments.
    """
    args = _parse_args()
    max_cols = set_max_cols(args)

    set_pd_display(max_colwidth=args.max_colwidth,
                   max_width=args.max_width,
                   max_cols=max_cols)

    data_sample = _get_data_sample(args)

    _print_table(data_sample, max_cols, 
                 args.transpose, args.markdown)


def set_max_cols(args):
    read_path = args.pickle
    if not read_path.is_file():
        exit(f'Error: Input file not found:\n ✕ {read_path}')
    max_cols = args.max_cols
    col_list = args.columns
    if args.transpose:
        max_cols = args.sample_size or max_cols
    elif col_list:
        max_cols = len(col_list)
    return max_cols


def _get_data_sample(args):
    sample_size = args.sample_size
    full_frame = _read_data(args.pickle)
    # [x]: extend this to work with any type of tabular data input (or at least `.csv` and `.psv` files)

    filtered_data, filter_applied = _filter_rows(full_frame, args.filters)
    if sample_size:
        data = filtered_data.sample(min(len(filtered_data), sample_size))
    if args.sort_by:
        data = data.sort_values(args.sort_by)
    else:
        data = data.sort_index()

    data = _select_columns(data, args.columns)

    _print_header(len(data), len(filtered_data),
                  filter_applied, args.pickle.name)

    return data


def _read_data(read_path):
    read_suffix = read_path.suffix
    if '.pkl' in read_path.suffixes:
        full_data = pd.read_pickle(read_path)
    elif read_suffix == '.csv':
        full_data = pd.read_csv(read_path)
    elif read_suffix == '.psv':
        full_data = pd.read_csv(read_path, delimiter='|')
    elif read_suffix == '.tsv':
        full_data = pd.read_csv(read_path, delimiter='\t')
    elif read_suffix == '.json':
        full_data = pd.read_json(read_path)
    else:
        exit(f'Error: Input file suffix, {read_suffix}, is either '
             + 'not interpretable or not an expected suffix for a DataFrame.')
    print(f'\n## Sampling from `{read_path}`')
    return full_data


def _print_header(n_sample_rows, n_input_rows, file_name: str,
                  filter_applied: bool):

    length_info = (f'{n_sample_rows} random row{"s" if n_sample_rows != 1 else ""}'
                   if n_sample_rows < n_input_rows
                   else f'All ({n_sample_rows}) row(s)')
    if filter_applied:
        length_info += ' matching filter(s)'
    print(f'\n### {length_info} from `{file_name}`\n')


def _filter_rows(input_data: pd.DataFrame,
                filter_list: list):
    """
        Filters rows of a pandas DataFrame based on a list of filter expressions.

        Args:
            input_data: The pandas DataFrame to filter.
            filter_list: A list of filter expressions in the format "column_name=filter_value" or "column_name!=filter_value".

        Returns:
            Tuple[pd.DataFrame, bool]: A tuple containing the filtered DataFrame and a boolean indicating if any rows were filtered.

        Raises:
            None

        Examples:
            >>> filter_rows(pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}), ["A=1", "B!=2"])
            (pd.DataFrame({"A": [1, 3], "B": [4, 6]}), True)
    """
    filtered = False
    if filter_list:
        print('\n- *filtering rows...*')
        f = input_data.copy()
        for filter_str in filter_list:
            filter_col, filter_val = filter_str.rsplit('=', 1)
            op = filter_col[-1]
            filter_col = filter_col[:-1]
            try:
                target_param = f[filter_col]
            except KeyError:
                print(
                    f'  - ✕ ERROR: Filter column `{filter_col}` not found. Filter `{filter_str}` ignored.')
                continue

            # `filter_col` NOT equal to `filter_val`
            if op == '!':
                f = f.loc[target_param != filter_val, :]

                # `filter_col` IS equal to `filter_val`
            elif op == '=':
                f = f.loc[target_param == filter_val, :]

            if f.empty:
                print(
                    f'  - Filter expression `{filter_str}` matched zero rows. Filter not applied.')
                f = input_data.copy()
            else:
                filtered = True
                input_data = f
                print(f'  - ✓ Applied filter: `{filter_str}`')

    return input_data, filtered


def _select_columns(data_selection: pd.DataFrame,
                   seek_cols: list):
    """
    Selects columns from a pandas DataFrame based on a list of column names.

    Args:
        data_selection: The pandas DataFrame to select columns from.
        seek_cols: A list of column names to select.

    Returns:
        pd.DataFrame: The pandas DataFrame with only the selected columns.

    Raises:
        None

    Examples:
        >>> select_columns(pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}), ["A"])
        pd.DataFrame({"A": [1, 2, 3]})
    """

    if seek_cols:
        print('\n- *selecting columns...*')
        selected_cols = []
        for col in seek_cols:
            if col not in data_selection.columns:
                print(
                    f'  - Warning‼️ `{col}` not in columns. Selection ignored.')
            else:
                selected_cols.append(col)
        if selected_cols:
            data_selection = data_selection[selected_cols]
    return data_selection


def _print_table(data_sample, max_cols, transpose, markdown):
    if transpose:
        print('_note: table transposed for display_\n')
        data_sample = data_sample.transpose()
    if markdown:
        data_sample = data_sample.iloc[:, 0:max_cols]
        print(data_sample.to_markdown(floatfmt=',.0f'))
    else:
        print('```')
        print(data_sample)
        print('```')


def _parse_args():
    """
    Parses the command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.

    """
    parser = argparse.ArgumentParser(
        description=(
            'simple script to print a sample of a pickled dataframe to stdout '
            'as either the default `pandas` output or as a markdown table (-m). '
            'Specific columns can be selected (defaults to all columns), '
            'and sample size can be dictated (defaults to 20 rows). '
            'Tip: use `-N 1 -t` to see example of all included columns'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('pickle',
                        type=Path,
                        help=('path to pickled dataframe')
                        )

    parser.add_argument(
        '-N', '--sample_size',
        type=int, default=20,
        help=('number of rows to include in sample. '
              'To disable sampling (show entire '
              'table--use with caution! ⚠️), use `-N 0`'))

    parser.add_argument(
        '-s', '--sort_by',
        type=str, default=None,
        help=('name of column to sort sample by; '
              "needn't be selected for printout. "
              '*note* this will be _ascending_ (A-Z or increasing numerical values)'))

    parser.add_argument(
        '-c', '--column',
        type=str, action='append', dest='columns',
        default=[],
        help=('option to specify columns to print. '
              'Each must have its own `-c` flag. E.g. `-c COLUMN_1 -c COLUMN_2`')
    )

    parser.add_argument(
        '-f', '--filter',
        type=str, action='append', dest='filters',
        default=[],
        help=('option to filter rows before sampling. '
              'Specify as a string of the format: '
              '`COLUMN_NAME==VALUE` or `COLUMN_NAME!=VALUE` to invert the filter. '
              'For example, to limit the sample to only rows with the adverb '
              '"absolutely", use → `adv_lemma==absolutely` or `adv_form==absolutely` '
              'To only see rows where the adjective is NOT "good", use → '
              '`adj_lemma!=good` or `adj_form!=good`. '
              'As with the --column flag, there can be multiple '
              'filters, but every string needs its own flag. '
              'NOTE: row filtering is done *before* column selection '
              'so filters may be based on columns which will not be printed.')
    )

    parser.add_argument(
        '-m', '--markdown',
        action='store_true',
        default=False,
        help=('option to print in markdown table format')
    )

    parser.add_argument(
        '-t', '--transpose',
        action='store_true',
        default=False,
        help=('option to transpose the output (swap axes) for clearer viewing')
    )

    parser.add_argument(
        '-C', '--max_cols',
        type=int, default=20,
        help=('max number of columns to include in sample; overriden by '
              '--column flags if given (or --sample_size if --transpose specified)'))

    parser.add_argument(
        '-w', '--max_colwidth',
        type=int, default=40,
        help=('max width (in pixels?) of each column in sample display; '
              '*currently does not apply to markdown formatted displays, '
              'which include full values for every included cell.'))

    parser.add_argument(
        '-W', '--max_width',
        type=int, default=180,
        help=('max width of the entire display; '
              '*currently does not apply to markdown formatted displays, '
              'which will be the sum of the widest cell in every included columm'))

    return parser.parse_args()


if __name__ == '__main__':
    print_sample()
