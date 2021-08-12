'''
    This script loads a dataframe of all non-overlapping collocation tokens.
    All tokens that matched more than a single *informative* context
    (e.g. not basic, unrestricted pattern matches) are excluded from these data.

    This script outputs various "samples" of data for quick illustration, as
    well as various frequency table dataframes (pickled and compressed)
    generated via `pandas.crosstab`:
        1. all contexts, raw counts
        2. all contexts, what proportion of colloc each context accounts for
        3. all contexts, what proportion of context each colloc accounts for
        4. text cases (contexts with uncertain polarity), raw counts
        5. counts and various normalized metrics for 2 defined polarity context
            groups: positive and negative
'''

import time

from pathlib import Path
from pprint import pprint

import pandas as pd
from scipy.stats import zscore

# TODO: create argument input structure: file names, load previously created
#  data, verbose, exclusion threshold, etc.

# create output directory if it doesn't exist
sample_dir = Path.cwd() / 'data_samples'
if not (sample_dir.exists() and sample_dir.is_dir()):
    sample_dir.mkdir()


def __main__():

    # load nonoverlapping hits dataframe
    compiled = pd.read_pickle("compiled_hits.pkl.gz")
    hits = compiled.loc[:, ['colloc', 'context', 'context_word',
                            'context_type', 'context_group', 'adv', 'adj', 'polarity']]

    # print summary infomation on frequencies
    polarity_descrip = hits.groupby("polarity").describe()
    print(polarity_descrip)
    polarity_descrip.to_csv("no-overlap_polarity_summary.csv")

    # TODO fix this hack once data has been fully gathered
    test_contexts = (
        hits[hits.context_word.isin(
            ('every', 'everyone', 'everyone' 'if', 'never'))].context
        .append(hits[hits.polarity == 'unknown'].context)
        .unique())

    pos_hits = hits[hits.polarity == 'positive']
    neg_hits = hits[hits.polarity == 'negative']
    neg_hits = neg_hits[~neg_hits.context.isin(test_contexts)]
    test_hits = hits[hits.context.isin(test_contexts)]

    # write sample files to sample_dir and returns frequency table dataframe(s)
    pos_colloc_counts = basic_freq_table(pos_hits, 'positive')
    neg_colloc_counts = basic_freq_table(neg_hits, 'negative')
    test_colloc_counts = basic_freq_table(test_hits, 'test')
    # collocs_by_context = basic_freq_table(hits)
    # collocs_by_context = pd.read_pickle(
    #     "individual-contexts_freq-table.pkl.gz")

    collocs_by_context = (pos_colloc_counts.join(neg_colloc_counts)
                          .join(test_colloc_counts)).fillna(0).apply(pd.to_numeric, downcast='unsigned')
    collocs_by_context.to_pickle('all-contexts_freq-table.pkl.gz')
    pprint(collocs_by_context.describe().sort_values("max", axis=1, ascending=False).round(3))
    print("")

    prop_of_colloc, prop_of_context = get_proportions(hits)

    context_zscores, colloc_zscores = calc_zscores(collocs_by_context)

    # get sum of counts across polarity categories
    negative_counts = pos_colloc_counts.sum(axis=1)
    positive_counts = neg_colloc_counts.sum(axis=1)

    # default threshold of 3 will be used
    compare_2_count_series(positive_counts, negative_counts,
                           'positive', 'negative')

    # also create dataframe/samples with no min threshold of occurences
    compare_2_count_series(positive_counts, negative_counts,
                           'positive', 'negative', threshold=0)


    test_colloc_counts.to_pickle("test-contexts_freq-table.pkl.gz")
    test_colloc_counts.sample(n=500).sort_values("colloc").to_csv(
        sample_dir / 'test-contexts-freq_500rows.csv')


def basic_freq_table(data: pd.DataFrame, name:str):

    # get frequency table
    collocs_by_context = pd.crosstab(
        data.colloc, data.context).apply(pd.to_numeric, downcast="unsigned")

    # write full frequency table to file (compressed pickle format)
    collocs_by_context.to_pickle(f"{name}-contexts_freq-table.pkl.gz")
    # write sample csv for easy illustration
    collocs_by_context.sample(n=300).sort_index().to_csv(
        sample_dir / f'{name}_freq_300rows.csv')

    # +1 smoothing
    # counts_plus_one = collocs_by_context.add(1)
    # counts_plus_one.sample(n=500).sort_index().to_csv(
    #     sample_dir / 'freq_plus-one_500rows.csv')

    return collocs_by_context


def get_proportions(data: pd.DataFrame):

    # shows what proportion of the colloc falls in each context
    proportion_of_colloc = pd.crosstab(
        data.colloc, data.context,
        margins=True, margins_name='all_collocs', normalize='index'
    ).round(3).apply(pd.to_numeric, downcast="float")

    # make sample
    colloc_prop_sample = proportion_of_colloc.sample(
        n=500).append(proportion_of_colloc.loc["all_collocs", :])

    colloc_prop_sample = (
        colloc_prop_sample.sort_index()
        .sort_values("all_collocs", axis=1, ascending=False))

    # write sample file
    colloc_prop_sample.to_csv(
        sample_dir / "colloc-proportion_500plusTotalRow.csv")

    # shows what proportion of the context falls in each colloc
    proportion_of_context = pd.crosstab(
        data.colloc, data.context,
        margins=True, margins_name='all_contexts', normalize='columns'
    ).round(3).apply(pd.to_numeric, downcast="float")

    # make sample
    context_prop_sample = (
        proportion_of_context.sample(n=500)
        .sort_index()
        .sort_values("all_contexts", ascending=False))

    # write sample file
    context_prop_sample.to_csv(
        sample_dir / "contextProportion_500rows.csv")

    return proportion_of_colloc, proportion_of_context


def calc_zscores(freq_df: pd.DataFrame):

    column_z = freq_df.apply(zscore, raw=True
                             ).round(4).apply(pd.to_numeric, downcast="float")

    row_z = freq_df.apply(zscore, axis=1, result_type="expand", raw=True
                          ).round(4).apply(pd.to_numeric, downcast="float")

    column_z.sample(500).to_csv(sample_dir / "contextZscores_500rows.csv")
    row_z.sample(500).to_csv(sample_dir / "collocZscores_500rows.csv")

    return column_z, row_z


def compare_2_count_series(counts1: pd.Series, counts2: pd.Series,
                           name1='positive', name2='negative',
                           threshold=3, precision=5):

    fileprefix = f'{name1}-{name2}'

    # raw counts seed dataframe
    counts_raw = pd.DataFrame(
        {f'{name1}_raw': counts1,
         f'{name2}_raw': counts2}).fillna(0).apply(pd.to_numeric, downcast="unsigned")

    # add "total" column (cannot add row due to category type limitations)
    counts_raw.loc[:, 'total_raw'] = counts_raw.sum(axis=1)

    # filter out low frequency collocations
    # (default: at least 3 total ocurrences)
    orig_num_colloc = len(counts_raw)
    counts_raw = counts_raw[counts_raw.total_raw >= threshold].apply(
        pd.to_numeric, downcast='unsigned')
    rawtotal = counts_raw.total_raw
    filtered_num_colloc = len(counts_raw)
    print(
        f'Minimum combined token threshold of {threshold} applied --> {orig_num_colloc - filtered_num_colloc} rare collocations removed. {filtered_num_colloc} unique collocation pairs remain.')

    z_counts = counts_raw.apply(zscore)
    z_counts.columns = z_counts.columns.str.replace('raw', 'z')

    # calculate simple ratios of hits per context out of total hits
    # (for each collocation)
    ratios = counts_raw.iloc[:, :2].apply(lambda x: x / rawtotal)
    ratios.fillna(0, inplace=True)
    ratios.columns = ratios.columns.str.replace('raw', 'ratio')

    simplified = counts_raw.join(z_counts).join(ratios)

    baseline_freq_ratios = counts_raw.iloc[:, :2].sum()/rawtotal.sum()

    simplified.loc[:, f"{name1}_skew"] = (
        ratios.iloc[:, 0] / baseline_freq_ratios[0])
    simplified.loc[:, f"{name2}_skew"] = (
        ratios.iloc[:, 1] / baseline_freq_ratios[1])

    is_continuous = simplified.columns.str.endswith(('z', 'ratio', 'skew'))
    simplified.loc[:, is_continuous] = simplified.loc[
        :, is_continuous].round(precision).apply(pd.to_numeric, downcast='float')

    simplified = simplified.sort_values(
        ["negative_skew", "total_z", "negative_z"],
        ascending=[False]*3)

    pprint(simplified.head(10))

    # +1 smoothing counts dataframe
    counts_plus1 = simplified.iloc[:, :2].add(1)
    counts_plus1.columns = counts_plus1.columns.str.replace("raw", "plus1")

    # combined raw, z-scored, and +1 smoothed counts dataframe
    simplified = simplified.join(counts_plus1)

    simplified.to_pickle(f'{fileprefix}_thresh{threshold}_freq-table.pkl.gz')
    simplified.iloc[:500, :].to_csv(
        sample_dir / f'{fileprefix}_thresh{threshold}_top500neg.csv')
    simplified.sort_values(
        by="positive_skew", ascending=False).iloc[:500, :].to_csv(
            sample_dir / f'{fileprefix}_thresh{threshold}_top500pos.csv')

    simplified.sort_values("total_raw", ascending=False).iloc[:500, :].to_csv(
        sample_dir / f'{fileprefix}_thresh{threshold}_500-most-common.csv')

    pprint(simplified.round(3))


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Time elapsed: {round(absFinish - absStart, 3)} seconds')
