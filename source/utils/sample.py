# coding=utf-8
import contextlib
from tabulate import tabulate
import re
from pathlib import Path

import pandas as pd

try:
    from utils import (print_iter,  # pylint: disable=import-error
                       print_md_table, set_pd_display)
except ModuleNotFoundError:
    with contextlib.suppress(ModuleNotFoundError):
        from source.utils import print_iter, print_md_table, set_pd_display
        from source.utils.associate import adjust_assoc_columns
else:
    from utils.associate import adjust_assoc_columns
SANPI_DATA = Path('/share/compling/data/sanpi')


def sample_pickle(data_path: Path,
                  sample_size: int = 20,
                  sort_by: str = '',
                  columns: list = None,
                  regex: bool = False,
                  filters: list = None,
                  markdown: bool = False,
                  transpose: bool = False,
                  max_cols: int = 16,
                  max_colwidth: int = 40,
                  max_width: int = 120,
                  tabbed: bool = False,
                  comma: bool = False,
                  piped: bool = False,
                  grid: bool = False,
                  outline: bool = False,
                  fancy: bool = False,
                  quiet: bool = False,
                  print_sample: bool = True,
                  n_dec: int = 0) -> pd.DataFrame:
    """
    Samples and displays data from a pickle file with various formatting and display options.

    Args:
        data_path: The path to the pickle file containing the data.
        sample_size (int): The size of the sample to display (default is 20).
        sort_by (str): The column to sort the data by (default is '').
        columns (list): List of columns to display (default is None).
        regex (bool): Flag indicating whether filters should be treated as regex patterns (default is False).
        filters (list): List of filters to apply (default is None).
        markdown (bool): Flag to format the output as markdown (default is False).
        transpose (bool): Flag to transpose the table (default is False).
        max_cols (int): Maximum number of columns to display (default is 16).
        max_colwidth (int): Maximum width of columns (default is 40).
        max_width (int): Maximum width of the output (default is 120).
        tabbed (bool): Flag to format the output with tab separation (default is False).
        comma (bool): Flag to format the output as comma-separated values (default is False).
        piped (bool): Flag to format the output with pipe separation (default is False).
        grid (bool): Flag to format the output as a grid (default is False).
        outline (bool): Flag to format the output with an outline (default is False).
        fancy (bool): Flag to use fancy formatting for the output (default is False).
        quiet (bool): Flag to suppress printing messages (default is False).
        print_sample (bool): Flag to print the sampled data (default is True).
        n_dec (int): Number of decimal places to round to (default is 0).

    Returns:
        pd.DataFrame: The sampled data from the pickle file.
    """
    pd.set_option("display.memory_usage", 'deep')
    pd.set_option("display.precision", n_dec)
    pd.set_option("styler.format.precision", n_dec)
    pd.set_option("styler.format.thousands", ',')
    pd.set_option("display.float_format", ('{:,.' + str(n_dec) + 'f}').format)
    if transpose:
        max_cols = sample_size or max_cols

    if not any((columns, tabbed, piped, markdown, comma)):
        set_pd_display(max_colwidth=max_colwidth,
                       max_width=max_width,
                       max_cols=max_cols)

    data_sample = _get_data_sample(sample_size=sample_size, data_path=data_path, filters=filters,
                                   columns=columns, sort_by=sort_by, regex=regex,
                                   quiet=quiet, markdown=markdown, n_dec=n_dec)
    if print_sample:
        _print_table(data_sample=data_sample, quiet=quiet,
                     max_cols=max_cols, transpose=transpose,
                     markdown=markdown, tabbed=tabbed, comma=comma,
                     piped=piped, grid=grid, fancy=fancy, outline=outline,
                     n_dec=n_dec)

    return data_sample


def _get_data_sample(sample_size: int,
                     data_path: Path,
                     filters: list = None,
                     columns: list = None,
                     sort_by: str = '',
                     regex: bool = False,
                     n_dec: int = 0,
                     quiet: bool = False,
                     markdown: bool = False) -> pd.DataFrame:
    """
    Gets a sample of data from a DataFrame based on specified parameters like sample size, filters, columns, sorting, and formatting options.

    Args:
        sample_size (int): The size of the sample to retrieve.
        data_path: The path to the data file.
        filters (list): List of filters to apply (default is None).
        columns (list): List of columns to select (default is None).
        sort_by (str): The column to sort the data by (default is '').
        regex (bool): Flag indicating whether filters should be treated as regex patterns (default is False).
        n_dec (int): Number of decimal places to round to (default is 0).
        quiet (bool): Flag to suppress printing messages (default is False).
        markdown (bool): Flag to format the output as markdown (default is False).

    Returns:
        pd.DataFrame: The sampled and processed DataFrame based on the specified parameters.
    """

    full_frame = _read_data(data_path, quiet)

    filtered_data, filter_applied = _filter_rows(
        full_frame, filters, regex, quiet)
    if sample_size:
        data = filtered_data.sample(min(len(filtered_data), sample_size))
    data = data.sort_values(sort_by) if sort_by else data.sort_index()
    data = _select_columns(data, columns, quiet)
    if markdown or not quiet:
        _print_header(len(data), len(filtered_data),
                      data_path.name, filter_applied)
    data.update(
        data.select_dtypes(include='float').apply(pd.to_numeric, downcast='float').apply(
            round, ndigits=n_dec))
    return data


def _read_data(read_path, quiet=False) -> pd.DataFrame:
    """
    Reads data from a file based on the file format and returns the corresponding DataFrame.

    Args:
        read_path: The path to the file to be read.
        quiet (bool): Flag to suppress printing messages (default is False).

    Returns:
        pd.DataFrame: The DataFrame containing the data read from the file.
    """

    if not read_path.is_file():
        exit(f'Error: Input file not found:\n ✕ {read_path}')

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
    if not quiet:
        print(f'\n## Sampling from `{read_path}`')
    return full_data


def _print_header(n_sample_rows, n_input_rows, file_name: str,
                  filter_applied: bool):
    """
    Prints a header with information about the number of sample rows, total input rows, file name, and filter application status.

    Args:
        n_sample_rows: The number of sample rows to be displayed.
        n_input_rows: The total number of input rows.
        file_name (str): The name of the file being processed.
        filter_applied (bool): Flag indicating if a filter has been applied.

    Returns:
        None
    """

    length_info = (f'{n_sample_rows} random row{"s" if n_sample_rows != 1 else ""}'
                   if n_sample_rows < n_input_rows
                   else f'All ({n_sample_rows}) row(s)')
    if filter_applied:
        length_info += ' matching filter(s)'
    print(f'\n### {length_info} from `{file_name}`\n')


def _parse_filter(filter_str: str,
                  f: pd.DataFrame,
                  quiet: bool) -> tuple:
    """
    Parses a filter string to extract filter column, operator, and filter value from a DataFrame.

    Args:
        filter_str (str): The filter string to parse.
        f (pd.DataFrame): The DataFrame to extract the filter column from.
        quiet (bool): Flag to suppress warning messages.

    Returns:
        tuple: A tuple containing the target parameter, filter value, and operator extracted from the filter string.
    """

    filter_col, op, filter_val = re.match(
        r'(^\w+)([!=])=(.+$)', filter_str).groups()

    try:
        target_param = f[filter_col]
    except KeyError:
        if not quiet:
            print(f'  - ✕ WARNING: Filter column `{filter_col}`',
                  f'not found. Filter `{filter_str}` ignored.')
        return (None, None, None)
    return (target_param, filter_val, op)


def _filter_rows(input_data: pd.DataFrame,
                 filter_list: list,
                 regex: bool = False,
                 quiet=False) -> tuple[pd.DataFrame, bool]:
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
    filter_applied = False
    if filter_list:
        if not quiet:
            print(f'\n- *filtering rows...*\n  - regex parsing = {regex}')
        f = input_data.copy()
        for filter_str in filter_list:
            # filter_col, filter_val = filter_str.rsplit('=', 1)
            # op = re.match(r'^.*(.)=.$', filter_str).groups()[0]
            # op = '!' if '!' in filter_str else '='
            target_param, filter_val, op = _parse_filter(filter_str, f, quiet)
            if not filter_val:
                continue
            # matches_filter = pd.Series(_id_filter_matches(target_param, filter_val, regex))
            # matches_filter = target_param.apply(lambda x: _assess_value_for_target(value=x, target=filter_val, regex=regex))
            matches_filter = target_param.astype('string').apply(_assess_value_for_target,
                                                                 target=filter_val, regex=regex)
            # `filter_col` NOT equal to `filter_val`
            if op == '!':
                f = f.loc[~matches_filter, :]

                # `filter_col` IS equal to `filter_val`
            elif op == '=':
                f = f.loc[matches_filter, :]

            if f.empty:
                if not quiet:
                    print(
                        f'  - Filter expression `{filter_str}` matched zero rows. Filter not applied.')
                f = input_data.copy()
            else:
                filter_applied = True
                input_data = f
                if not quiet:
                    print(f'  - ✓ Applied filter: `{filter_str}`')

    return input_data, filter_applied


# def _id_filter_matches(target_param, filter_str, regex):

    # for value in target_param:
    #     yield _assess_value_for_target(value=value,
    #                                    target=filter_str, regex=regex)
    # # return target_param.apply(_assess_value_for_target, target=filter_str, regex=regex)


def _assess_value_for_target(value: str,
                             target: str = '',
                             regex=False):
    """
    Checks if a value matches a target string or regex pattern.

    Args:
        value (str): The value to assess.
        target (str): The target string or regex pattern to match against (default is '').
        regex (bool): Flag indicating whether the target should be treated as a regex pattern (default is False).

    Returns:
        bool: True if the value matches the target string or regex pattern, False otherwise.
    """

    return (any(re.findall(target, value)) if regex else value == target)


def _select_columns(data_selection: pd.DataFrame,
                    seek_cols: list = None,
                    quiet: bool = True):
    """
    Selects columns from a DataFrame based on a list of column names or prefixes.

    Args:
        data_selection (pd.DataFrame): The DataFrame from which columns are selected.
        seek_cols (list): List of column names or prefixes to select (default is None).
        quiet (bool): Flag to suppress printing messages (default is True).

    Returns:
        pd.DataFrame: DataFrame with the selected columns.
    """

    if seek_cols:
        existing_cols = data_selection.columns
        # if not quiet:
        #     print('\n- *selecting columns...*')

        sought = pd.Series(seek_cols)
        infer = sought.str.startswith(('WITH::', 'START::', 'END::'))
        sought.loc[infer] = sought[infer].apply(
            read_cue, df_cols=existing_cols, quiet=quiet)
        found = sought.isin(existing_cols)
        sought[~infer] = sought[~infer & found]
        # sought.loc[] = sought.loc[explicit_found]

        selected_cols = sought.explode().drop_duplicates().to_list()

        missing_cols = sought[~infer & ~found]
        if any(missing_cols) and not quiet:
            print_iter(
                missing_cols,
                indent=6,
                bullet='-',
                header='  - Warning: The following requested columns were not found. Selection ignored.',
            )
        if any(selected_cols):
            # if not quiet:
            #     print_iter(selected_cols, bullet='-',
            #                header='  - Column Selection:', indent=6)
            data_selection = data_selection[selected_cols]
    return data_selection


def read_cue(col_request: str,
             df_cols: pd.Index or pd.Series,
             quiet: bool = True
             ) -> list:
    """
    Reads a cue from a column request string and returns the corresponding match functions as a list.

    Args:
        col_request (str): The column request string in the format 'cue::column_partial'.
        df_cols (pd.Index or pd.Series): The columns of the DataFrame.

    Returns:
        list: A list of match functions corresponding to the cue.

    Example:
        >>> read_cue('WITH::log', df.columns)
        ['log_likelihood', 'am_log_likelihood', 'am_log_likelihood_tt', 
         'log_ratio', 'conservative_log_ratio']
    """

    cue, col_partial = col_request.split('::', 1)
    # if not quiet:
    #     read_as = {'WITH': 'contains',
    #                'START': 'startswith',
    #                'END': 'endswith'}[cue]
    #     print(
    #         f'  - column flag, `-c {cue}={col_partial}`, interpreted as `{read_as}({col_partial})`')

    return match_cue(cue, col_partial, df_cols).to_list()


def match_cue(cue_method: str,
              sub_col: str,
              df_cols: pd.Index or pd.Series
              ) -> pd.Series(dtype='bool'):
    """
    Matches a cue with the corresponding columns in a DataFrame.

    Args:
        cue_method (str): The cue method to use for matching ('WITH', 'START', or 'END').
        sub_col (str): The substring to match within the columns.
        df_cols (pd.Index or pd.Series): The columns of the DataFrame.

    Returns:
        pd.Series(dtype='bool'): A boolean series indicating the matching columns.

    Example:
        >>> match_cue('WITH', 'column_partial', df.columns)
        0    True
        1    False
        2    True
        dtype: bool
    """
    cue_cols_dict = {
        'WITH': df_cols.str.contains(sub_col),
        'START': df_cols.str.startswith(sub_col),
        'END': df_cols.str.endswith(sub_col)
    }
    return df_cols[cue_cols_dict[cue_method]]


def set_tablefmt(outline: bool,
                 grid: bool,
                 fancy: bool,
                 markdown: bool) -> str:

    if markdown:
        return 'pipe'

    fmts = [s for s, a in (('outline', outline),
                           ('grid', grid)) if a]

    fmt = fmts[0] if fmts else ''
    return f'fancy_{fmt}'.strip('_') if fancy else f'rounded_{fmt}'


def _print_table(data_sample: pd.DataFrame,
                 max_cols: int = 8,
                 transpose: bool = False,
                 markdown: bool = False,
                 tabbed: bool = False,
                 comma: bool = False,
                 piped: bool = False,
                 grid: bool = False,
                 fancy: bool = False,
                 outline: bool = False,
                 quiet: bool = False,
                 n_dec: int = 0) -> None:
    """
    Prints a formatted table from a DataFrame with various display options.

    Args:
        data_sample (pd.DataFrame): The DataFrame to be printed as a table.
        max_cols (int): Maximum number of columns to display (default is 8).
        transpose (bool): Flag to transpose the table for display (default is False).
        markdown (bool): Flag to format the table as markdown (default is False).
        tabbed (bool): Flag to format the table with tab separation (default is False).
        comma (bool): Flag to format the table as comma-separated values (default is False).
        piped (bool): Flag to format the table with pipe separation (default is False).
        grid (bool): Flag to format the table as a grid (default is False).
        fancy (bool): Flag to use fancy formatting for the table (default is False).
        outline (bool): Flag to format the table with an outline (default is False).
        quiet (bool): Flag to suppress printing messages (default is False).
        n_dec (int): Number of decimal places to round to (default is 0).

    Returns:
        None
    """

    # pd.set_eng_float_format(accuracy=n_dec, use_eng_prefix=True)
    round_ax = 1
    if transpose and not quiet:
        print('_note: table transposed for display_\n')
        data_sample = data_sample.transpose()
        round_ax = 0

    float_cols = data_sample.select_dtypes(include='float').columns
    data_sample[float_cols] = data_sample[float_cols].apply(
            round, ndigits=n_dec, axis=round_ax)

    if any([piped, markdown, tabbed, comma, grid, fancy, outline]):
        if data_sample.shape[1] > max_cols:
            print(f'- Printed columns restricted to first {max_cols} in table')
        data_sample = data_sample.iloc[:, 0:max_cols]
        if any((fancy, grid, outline, markdown)):
            columns = data_sample.columns
            fmt = set_tablefmt(outline, grid, fancy, markdown)
            if any(columns.str.startswith(
                       ('am_', 'E11', 'O11', 'f_', 'log_', 'odds_', 
                        'l1', 'l2', 'conservative_log_ratio'))):
                columns = adjust_assoc_columns(columns, style='camel')
            print(tabulate(data_sample,
                           headers=columns,
                           tablefmt=fmt,
                           intfmt=',',
                           floatfmt=f',.{n_dec}f'))

        elif comma:
            print(data_sample.to_csv(header=True))
        elif tabbed:
            print(data_sample.to_csv(header=True, sep='\t'))
        elif piped:
            print(data_sample.to_csv(header=True, sep='|'))
        # else:
        #     print_md_table(data_sample, n_dec=n_dec)
    else:
        print('```log')
        print(data_sample)
        print('```')
