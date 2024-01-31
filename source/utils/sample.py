# coding=utf-8
import contextlib
import re
from pathlib import Path

import pandas as pd
try:
    from utils import set_pd_display, print_md_table  # pylint: disable=import-error
except ModuleNotFoundError:
    with contextlib.suppress(ModuleNotFoundError):
        from source.utils import set_pd_display, print_md_table

SANPI_DATA = Path('/share/compling/data/sanpi')


def sample_pickle(
    data_path: Path = SANPI_DATA.joinpath('DEMO/2_hit_tables/RBdirect/condensed/'
                                          'DEMO-Pcc_all-RBdirect_unique-bigram-id_hits.pkl.gz'),
    sample_size: int = 20,
    sort_by: str = '',
    columns: list = None,
    filters: list = None,
    markdown: bool = False,
    transpose: bool = False,
    max_cols: int = 20,
    max_colwidth: int = 40,
    max_width: int = 100,
    tabbed: bool = False,
    comma: bool = False,
    piped: bool = False,
    quiet: bool = False,
    regex: bool = False,
    print_sample: bool = True
):
    """
    Sample and print a table of data.

    Args:
        data_path (Path): The path to the data file. Defaults to '/share/compling/data/sanpi/4_post-processed/RBdirect/neg-bigrams_thr0-001p.10f.pkl.gz'.
        sample_size (int): The number of rows to sample. Defaults to 20.
        sort_by (str): The column to sort the data by. Defaults to an empty string.
        columns (list): The columns to include in the table. Defaults to None.
        filters (list): The filters to apply to the data. Defaults to None.
        markdown (bool): Whether to format the table as markdown. Defaults to False.
        transpose (bool): Whether to transpose the table. Defaults to False.
        max_cols (int): The maximum number of columns to display. Defaults to 20.
        max_colwidth (int): The maximum width of each column. Defaults to 40.
        max_width (int): The maximum width of the table. Defaults to 100.
        tabbed (bool): Whether to format the table as tab-separated values. Defaults to False.
        comma (bool): Whether to format the table as comma-separated values. Defaults to False.
        piped (bool): Whether to format the table as piped values. Defaults to False.
        quiet (bool): Whether to suppress printing meta-messages. Defaults to False.
        print_sample (bool): Whether to print the sampled table. Defaults to True.

    Returns:
        pd.DataFrame: The sampled data table.
    """

    if transpose:
        max_cols = sample_size or max_cols
    elif columns:
        max_cols = len(columns)
    if not (tabbed or piped or markdown or comma):
        set_pd_display(max_colwidth=max_colwidth,
                       max_width=max_width,
                       max_cols=max_cols)

    # > markdown output formatting overrides meta-message quieting
    elif markdown:
        quiet = False

    data_sample = _get_data_sample(sample_size=sample_size, data_path=data_path, filters=filters,
                                   columns=columns, sort_by=sort_by, regex=regex,
                                   quiet=quiet, markdown=markdown)

    if print_sample:
        _print_table(data_sample=data_sample,
                     max_cols=max_cols, transpose=transpose, quiet=quiet,
                     markdown=markdown, tabbed=tabbed, comma=comma, piped=piped)

    return data_sample


def _get_data_sample(sample_size: int,
                     data_path: Path,
                     filters: list = None,
                     columns: list = None,
                     sort_by: str = '',
                     regex: bool = False,
                     quiet: bool = False,
                     markdown: bool = False):

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

    return data


def _read_data(read_path, quiet=False):

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

    length_info = (f'{n_sample_rows} random row{"s" if n_sample_rows != 1 else ""}'
                   if n_sample_rows < n_input_rows
                   else f'All ({n_sample_rows}) row(s)')
    if filter_applied:
        length_info += ' matching filter(s)'
    print(f'\n### {length_info} from `{file_name}`\n')


def _parse_filter(filter_str: str, f: pd.DataFrame, quiet: bool):
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
                 quiet=False):
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
            print('\n- *filtering rows...*')
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
            matches_filter = target_param.apply(_assess_value_for_target,
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
    return any(re.findall(target, value)) if regex else value == target


def _select_columns(data_selection: pd.DataFrame,
                    seek_cols: list,
                    quiet=False):
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
        if not quiet:
            print('\n- *selecting columns...*')
        selected_cols = []
        for col in seek_cols:
            if col not in data_selection.columns and not quiet:
                print(
                    f'  - Warning‼️ `{col}` not in columns. Selection ignored.')
            else:
                selected_cols.append(col)
        if selected_cols:
            data_selection = data_selection[selected_cols]
    return data_selection


def _print_table(data_sample: pd.DataFrame,
                 max_cols: int = 8,
                 transpose: bool = False,
                 markdown: bool = False,
                 tabbed: bool = False,
                 comma: bool = False,
                 piped: bool = False,
                 quiet: bool = False):
    if transpose and not quiet:
        print('_note: table transposed for display_\n')
        data_sample = data_sample.transpose()

    if piped or markdown or tabbed or comma:
        data_sample = data_sample.iloc[:, 0:max_cols]
        if comma:
            print(data_sample.to_csv(header=True))
        elif tabbed:
            print(data_sample.to_csv(header=True, sep='\t'))
        elif piped:
            print(data_sample.to_csv(header=True, sep='|'))
        else:
            print_md_table(data_sample)
    else:
        print('```log')
        print(data_sample)
        print('```')
