# coding=utf-8
import argparse
from pathlib import Path


# pd.set_option('display.max_colwidth', 40)
# pd.set_option('display.max_columns', 20)
# pd.set_option('display.width', 200)
try:
    from utils import sample_pickle
except ModuleNotFoundError:
    from source.utils import sample_pickle


def _main():
    # [-N SAMPLE_SIZE] [-s SORT_BY] [-c COLUMNS] [-f FILTERS] [-m] [-t] [-C MAX_COLS] [-w MAX_COLWIDTH] [-W MAX_WIDTH] pickle

    args = _parse_args()

    sample_pickle(
        data_path=args.path,
        sample_size=args.sample_size,
        sort_by=args.sort_by,
        columns=args.columns,
        filters=args.filters,
        markdown=args.markdown,
        transpose=args.transpose,
        max_cols=args.max_cols,
        max_colwidth=args.max_colwidth,
        max_width=args.max_width,
        tabbed=args.tabbed,
        comma=args.comma,
        piped=args.piped,
        quiet=args.quiet)


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
    parser.add_argument(
        '-p', '--path',
        type=Path,
        default=Path(
            '/share/compling/data/sanpi/4_post-processed/RBdirect/neg-bigrams_thr0-001p.10f.pkl.gz'),
        help=('path to dataframe to sample')
    )

    parser.add_argument(
        '-N', '--sample_size',
        type=int, default=20,
        help=('number of rows to include in sample. '
              'To disable sampling (show entire '
              'table--use with caution! ⚠️), use `-N 0`')
    )

    parser.add_argument(
        '-s', '--sort_by',
        type=str, default=None,
        help=('name of column to sort sample by; '
              "needn't be selected for printout. "
              '*note* this will be _ascending_ (A-Z or increasing numerical values)')
    )

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
        '-T', '--tabbed',
        action='store_true',
        default=False,
        help=('option to print tab-delimited format')
    )
    parser.add_argument(
        '-P', '--piped',
        action='store_true',
        default=False,
        help=('option to print pipe-delimited (|) format')
    )
    parser.add_argument(
        '-C', '--comma',
        action='store_true',
        default=False,
        help=('option to print in csv format')
    )

    parser.add_argument(
        '-t', '--transpose',
        action='store_true',
        default=False,
        help=('option to transpose the output (swap axes) for clearer viewing')
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help=('option to suppress meta-messages printed to stdout. '
              '(Can be used with `-T/--tabbed` or `-P/--piped` or `-C/--comma` '
              'to write sample to file or use with `column -T [-s,/-s\\|]`)')
    )

    parser.add_argument(
        '-x', '--max_cols',
        type=int, default=20,
        help=('max number of columns to include in sample; overriden by '
              '--column flags if given (or --sample_size if --transpose specified)')
    )

    parser.add_argument(
        '-w', '--max_colwidth',
        type=int, default=40,
        help=('max width (in pixels?) of each column in sample display; '
              '*currently does not apply to markdown formatted displays, '
              'which include full values for every included cell.')
    )

    parser.add_argument(
        '-W', '--max_width',
        type=int, default=180,
        help=('max width of the entire display; '
              '*currently does not apply to markdown formatted displays, '
              'which will be the sum of the widest cell in every included columm')
    )



    return parser.parse_args()


if __name__ == '__main__':
    _main()
