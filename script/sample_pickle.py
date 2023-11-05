# coding=utf-8
import argparse
from pathlib import Path

import pandas as pd


def print_sample():
    """
    prints a sample from a pickled DataFrame based on command line arguments.
    """
    
    args = _parse_args()

    #TODO: extend this to work with any type of tabular data input (or at least `.csv` and `.psv` files)
    data = pd.read_pickle(args.pickle)
    
    data, filtered = filter_rows(data, args.filters)

    sampled = data.sample(min(len(data), args.sample_size))
    if args.sort_by: 
        sampled = sampled.sort_values(args.sort_by)
    else:
        sampled = sampled.sort_index()
    
    sampled = select_columns(sampled, args.columns)
    
    length_info = (f'{len(sampled)} random rows' if len(sampled) < len(data) 
                  else f'All ({len(data)}) rows')
    if filtered: 
        length_info += ' matching filter(s)'
    print(f'\n## {length_info} from `{args.pickle.name}`\n')
    
    if args.markdown:
        print(sampled.to_markdown(floatfmt=',.0f'))
    else:
        print(sampled)

def filter_rows(input_data:pd.DataFrame, 
                filter_list:list):
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
        print('')
        f = input_data.copy()
        for filter_str in filter_list: 
            filter_col, filter_val = filter_str.rsplit('=',1)
            op = filter_col[-1]
            filter_col = filter_col[:-1]
            try: 
                target_param = f[filter_col]
            except KeyError: 
                print(f'- ✕ ERROR: Filter column `{filter_col}` not found. Filter `{filter_str}` ignored.')
                continue
            
            # `filter_col` NOT equal to `filter_val`
            if op == '!': 
                f = f.loc[target_param != filter_val, :]

                # `filter_col` IS equal to `filter_val`
            elif op == '=': 
                f = f.loc[target_param == filter_val, :]
                    
            if f.empty: 
                print(f'- Filter expression "{filter_str}" matched zero rows. Filter not applied.')
                f = input_data.copy()
            else: 
                filtered = True
                input_data = f
                print(f'- ✓ Applied filter: `{filter_str}`')
                
    return input_data, filtered

def select_columns(data_selection: pd.DataFrame, 
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
        selected_cols = []
        for col in seek_cols: 
            if col not in data_selection.columns: 
                print(f'\n- Warning‼️ "{col}" not in columns. Selection ignored.')
            else: 
                selected_cols.append(col)
        if selected_cols: 
            data_selection = data_selection[selected_cols]
    return data_selection


def _parse_args():
    """
    Parses the command line arguments.
    
    Returns:
        argparse.Namespace: The parsed command line arguments.

    """
    parser = argparse.ArgumentParser(
        description=(
            'simple script to print a sample of a pickled dataframe to stdout as either the default `pandas` output or as a markdown table (-m). Specific columns can be selected (defaults to all columns), and sample size can be dictated (defaults to 20 rows)'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('pickle',
                        type=Path, 
                        help=('path to pickled dataframe')
                        )

    parser.add_argument(
        '-N', '--sample_size',
        type=int, default=20,
        help=('number of rows to include in sample'))

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
        help=('option to specify columns to print. Each must have its own `-c` flag. E.g. `-c COLUMN_1 -c COLUMN_2`')
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
    
    return parser.parse_args()


if __name__ == '__main__':
    print_sample()
