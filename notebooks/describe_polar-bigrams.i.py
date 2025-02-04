# %%
from pathlib import Path
from sys import exit as sys_exit
from math import sqrt
import pandas as pd

from am_notebooks import *
from source.utils import HIT_TABLES_DIR, SANPI_HOME, timestamp_today
from source.utils.dataframes import NEG_REGEX, REGNOT
from source.utils.LexicalCategories import SPECIAL_ADV, EXACTLY_RELEVANT_ADJ

import matplotlib as mpl
mpl.pyplot.rcParams['font.family'] = 'serif'
mpl.pyplot.style.use('seaborn-v0_8-paper')

RECOUNT_NEG = False
# %%


def set_outpath(dir_name, unit_name):
    return SANPI_HOME.joinpath(
        f'results/freq_out/{dir_name}/{unit_name}-counts_{dir_name}.{timestamp_today()}.csv')


def count_and_describe(values, name: str, dir_name: str = 'RBdirect'):
    counts = values.value_counts()
    outpath = set_outpath(dir_name, name)
    # x_neg.adv_form_lower.value_counts()
    counts.to_csv(outpath)
    print(f'💾 Saved {outpath.relative_to(SANPI_HOME)}')
    freq_stats = counts.to_frame(
        f'{name}_counts').describe().T.assign(
            unique=values.nunique()).round(4).convert_dtypes()
    # print(freq_stats.to_markdown(floatfmt=',.2f', intfmt=','))
    freq_stats.to_csv(outpath.with_name(
        outpath.name.replace('counts', 'freq-stats')))
    return counts, freq_stats


def seek_prior_counting(dir_name: str,
                        polarity: str) -> dict[pd.DataFrame]:
    adv_out = set_outpath(dir_name, f'{polarity[:3]}_adverb')
    adj_out = set_outpath(dir_name, f'{polarity[:3]}_adject')
    big_out = set_outpath(dir_name, f'{polarity[:3]}_bigram')
    outpath_dict = {'adv': adv_out, 'adj': adj_out, 'bigram': big_out}
    existing = {u: tuple(o.parent.glob(f'{Path(o.stem).stem}*csv'))
                for u, o in outpath_dict.items()}

    counts_dict = {}
    if all(existing.values()):
        for unit, path_tup in existing.items():
            col = f'{unit}_form_lower'.replace('bigram_form', 'bigram')
            loaded_counts = pd.read_csv(
                path_tup[0], engine='c', low_memory=True,
                index_col=col,
                dtype={col: 'string', 'count': 'int'})
            print(f'Reading {unit.upper()} Counts from {path_tup[0]}')
            # ! Needed to deal with how pandas.read_csv treats the string "null"
            loaded_counts.index = loaded_counts.index.fillna('null')
            counts_dict[unit] = loaded_counts
    # neg_adj_counts = pd.read_csv(
    #     neg_adj_out, engine='c', low_memory=True, index_col='adj_form_lower')
    # neg_big_counts = pd.read_csv(
    #     neg_big_out, engine='c', low_memory=True, index_col='bigram_lower')
    return counts_dict


def count_hits(redo_neg=False):

    neg_ids = HIT_TABLES_DIR.joinpath('RBdirect/ALL_RBdirect_final-index.txt'
                                      ).read_text(encoding='utf8').splitlines()
    pos_ids = HIT_TABLES_DIR.joinpath('not-RBdirect/ALL_not-RBdirect_final-index.txt'
                                      ).read_text(encoding='utf8').splitlines()
    x_neg = pd.read_parquet(
        '/share/compling/data/sanpi/info/ALL_final-hits_basic.24-08-03.parq/category=RBdirect',
        engine='pyarrow',
        filters=[('hit_id', 'in', neg_ids)]
    )
    if 'hit_id' in x_neg.columns:
        x_neg = x_neg.set_index('hit_id')
    x_neg = x_neg.join(x_neg.all_forms_lower.str.extract(
        r'^(?P<trigger_lower>[^_]+)_(?P<adv_form_lower>[^_]+)_(?P<adj_form_lower>[^_]+)$')).convert_dtypes()
    adv_counts, neg_adv_stats = count_and_describe(
        x_neg.adv_form_lower, 'neg_adverb', 'RBdirect')
    adj_counts, neg_adj_stats = count_and_describe(
        x_neg.adj_form_lower, 'neg_adject', 'RBdirect')
    bigram_counts, neg_bigram_stats = count_and_describe(
        x_neg.bigram_lower, 'neg_bigram', 'RBdirect')

    trigger_counts, trigger_stats = count_and_describe(
        x_neg.trigger_lemma, 'trigger_lemma')
    trigger_form_counts, trigger_form_stats = count_and_describe(
        x_neg.trigger_lower, 'trigger_lower')

    print(pd.concat([neg_adv_stats, neg_adj_stats, neg_bigram_stats, trigger_stats,
                     trigger_form_stats]).convert_dtypes().to_markdown(floatfmt=',.2f', intfmt=','))
    if redo_neg:
        return
    # // x_neg = x_neg.join(x_neg.bigram_lower.str.extract(r'^(?P<adv_form_lower>[^_]+)_(?P<adj_form_lower>[^_]+)$')
    # //                    ).assign(polarity='neg').convert_dtypes()

    # // x_pos = catify(pd.read_parquet('',
    # //                                engine='pyarrow',
    # //                                columns=['adv_form_lower', 'adj_form_lower', 'hit_id']).set_index('hit_id').assign(polarity='pos'),
    # //                reverse=True)

    # // x_pos['bigram_lower'] = x_pos.adv_form_lower + '_' + x_pos.adj_form_lower
    pos_chunks = (
        pd.read_parquet(chunk,
                        engine='pyarrow',
                        columns=['bigram_lower', 'adv_form_lower',
                                 'adj_form_lower', 'token_str'])
        for chunk in Path(
            '/share/compling/data/sanpi/2_hit_tables/not-RBdirect/ALL_not-RBdirect_final.parq'
        ).rglob('group*.parquet'))
    x_pos = pd.concat(pos_chunks)

    pos_adv_counts, pos_adv_stats = count_and_describe(
        x_pos.adv_form_lower, 'pos_adverb', 'not-RBdirect')
    pos_adj_counts, pos_adj_stats = count_and_describe(
        x_pos.adj_form_lower, 'pos_adject', 'not-RBdirect')
    pos_bigram_counts, pos_bigram_stats = count_and_describe(
        x_pos.bigram_lower, 'pos_bigram', 'not-RBdirect')
    print(pd.concat([pos_adv_stats, pos_adj_stats, pos_bigram_stats,
                     ]).convert_dtypes().to_markdown(floatfmt=',.2f', intfmt=','))

    all_adv_counts, all_adv_stats = count_and_describe(
        pd.concat((x.adv_form_lower for x in [x_pos, x_neg])),
        'all_adverb', 'ANYdirect')
    all_adj_counts, all_adj_stats = count_and_describe(
        pd.concat((x.adj_form_lower for x in [x_pos, x_neg])),
        'all_adject', 'ANYdirect')
    all_bigram_counts, all_bigram_stats = count_and_describe(
        pd.concat((x.bigram_lower for x in [x_pos, x_neg])),
        'all_bigram', 'ANYdirect')

    print(pd.concat([all_adv_stats, all_adj_stats, all_bigram_stats,
                     ]).convert_dtypes().to_markdown(floatfmt=',.2f', intfmt=','))
    print(
        f'{pd.concat((x.token_str for x in [x_pos, x_neg])).nunique():,} unique sentences in Polar Bigrams')


def combine_polarities(pos_counts, neg_counts, unit):
    pos_unit = pos_counts[unit]
    neg_unit = neg_counts[unit]
    unit_name = pos_unit.index.name
    all_unit = (
        pd.Series(pos_unit.index.tolist()+neg_unit.index.tolist()
                  ).drop_duplicates().to_frame(unit_name).set_index(unit_name)
        .join(pos_unit.rename(columns={'count': 'PosTokens'}))
        .join(neg_unit.rename(columns={'count': 'NegTokens'}))
        .fillna(0)
    )
    all_unit['AllTokens'] = (all_unit.PosTokens + all_unit.NegTokens)
    all_unit = all_unit.astype('int').sort_values('AllTokens', ascending=False)[
        ['AllTokens', 'PosTokens', 'NegTokens']]
    all_unit['%Neg'] = ((all_unit.NegTokens / all_unit.AllTokens)
                         * 100).astype('float64').round(3)
    all_unit['%Pos'] = ((all_unit.PosTokens / all_unit.AllTokens)
                         * 100).astype('float64').round(3)
    return all_unit


if RECOUNT_NEG:
    count_hits(redo_neg=True)

neg_counts = seek_prior_counting('RBdirect', 'neg')
pos_counts = seek_prior_counting('not-RBdirect', 'pos')

if not bool(neg_counts) and bool(pos_counts):
    count_hits()
    neg_counts = seek_prior_counting('RBdirect', 'neg')
    pos_counts = seek_prior_counting('not-RBdirect', 'pos')

all_adv = combine_polarities(pos_counts, neg_counts, 'adv')
print(f'> {len(all_adv):,} unique adverbs')
all_adv.filter(['null'], axis=0)
# %%
all_adj = combine_polarities(pos_counts, neg_counts, 'adj')
print(f'> {len(all_adj):,} unique adjectives')
all_adj.filter(['null'], axis=0)
# %%
all_bigram = combine_polarities(pos_counts, neg_counts, 'bigram')
all_bigram.index = all_bigram.index.str.replace('_', ' ')
# %%


def plot_totals(_unit_counts=all_adj, unit_name='adjective', size=(5, 3), pad_inches=0.1):
    _N = _unit_counts.AllTokens.sum()
    unique_vals = len(_unit_counts)

    unit_name = unit_name.lower()
    cmap = 'petrol_wine_r' if unit_name.startswith('adj') else (
        'purple_rain_r' if unit_name.startswith('adv') else 'petrol_wine')

    _unit_totals = _unit_counts.sort_values(
        ['AllTokens']
    ).reset_index().filter(like='All')
    _fig = _unit_totals.cumsum().plot(
        figsize=size, cmap=cmap,
        title=f'Cumulative Sum of Tokens by {unit_name}\nin ALL+ Superset\nN={_N:,}'.title(
        ), ylabel='cumulative sum of tokens',
        xlabel=f'sequential order of unique {unit_name}s\n({unique_vals:,} unique)',
        legend=False
    )
    plt.savefig(RESULT_DIR.joinpath(f'freq_out/images/{unit_name[:(3 if unit_name.lower().startswith("a") else 4)]}-cumsum_ALL-PBR_{timestamp_today()}.png'),
                dpi=300, bbox_inches='tight', pad_inches=pad_inches)

    _fig = _unit_totals.plot(
        kind='line', cmap=cmap, legend=False, figsize=size,
        xlabel=f'sequential order of unique {unit_name}s\n({unique_vals:,} unique)',
        ylabel='observed tokens', logy=False,
        title=f'Increasing {unit_name} Marginal Frequencies\nin ALL+ Superset\nN={_N:,}'.title()
    )
    plt.savefig(RESULT_DIR.joinpath(f'freq_out/images/{unit_name[:(3 if unit_name.lower().startswith("a") else 4)]}-sequential-f-raw_ALL-PBR_{timestamp_today()}.png'),
                dpi=300, bbox_inches='tight', pad_inches=pad_inches)

    _fig = _unit_totals.plot(
        kind='line', cmap=cmap, legend=False, figsize=size,
        xlabel=f'sequential order of unique {unit_name}s\n({unique_vals:,} unique)',
        ylabel='observed tokens (log)', logy=True,
        title=f'Increasing {unit_name} Marginal Frequencies\nin ALL+ Superset\n(log transformed) N={_N:,}'.title())
    plt.savefig(RESULT_DIR.joinpath(f'freq_out/images/{unit_name[:(3 if unit_name.lower().startswith("a") else 4)]}-sequential-f-log_ALL-PBR_{timestamp_today()}.png'),
                dpi=300, bbox_inches='tight', pad_inches=pad_inches)

    _fig = _unit_totals.plot(
        kind='hist', cmap=cmap, legend=False, figsize=size,
        xlabel=f'unique {unit_name}s\n({unique_vals:,} unique)',
        ylabel='observed tokens (log)', logy=True,
        title=f'Distribution of {unit_name} Marginal Frequencies\nin ALL+ Superset\n(log transformed) N={_N:,}'.title())
    plt.savefig(RESULT_DIR.joinpath(f'freq_out/images/{unit_name[:(3 if unit_name.lower().startswith("a") else 4)]}-hist-log_ALL-PBR_{timestamp_today()}.png'),
                dpi=300, bbox_inches='tight', pad_inches=pad_inches)

    _fig = _unit_totals.plot(
        kind='hist', cmap=cmap, legend=False, figsize=size,
        xlabel=f'unique {unit_name}s\n({unique_vals:,} unique)',
        ylabel='observed tokens', logy=False,
        title=f'Distribution of {unit_name} Marginal Frequencies\nin ALL+ Superset\nN={_N:,}'.title())
    plt.savefig(RESULT_DIR.joinpath(f'freq_out/images/{unit_name[:(3 if unit_name.lower().startswith("a") else 4)]}-hist_ALL-PBR_{timestamp_today()}.png'),
                dpi=300, bbox_inches='tight', pad_inches=pad_inches)

# plot_totals(all_adj, 'adjective')
# plot_totals(all_adv, 'adverb')
# plot_totals(all_bigram, 'bigram')


# %%
K = 20
bigram_min = 100
all_bigram_common = all_bigram.loc[
    (all_bigram.AllTokens >= bigram_min)
    & ~(all_bigram.index.str.startswith(("not", "no ", "never", "n't"))), :]
save_latex_table(
    format_zeros(all_bigram_common
                 .nlargest(K, ['%Neg', 'AllTokens']).convert_dtypes()
                 .style.background_gradient('PuBu')),
    verbose=True,
    caption=f'Top {K} Bigrams with Highest <u>Negative Polarity</u> Percentage ({bigram_min:,}+ tokens)' +
    '<i>Note: Negative trigger bigrams excluded</i>',
    latex_subdir='PBR_summary/negative',
    latex_stem=f'top{K}-bigram-NegPercent_{bigram_min}+',
    label='tab:top-bigram-NegPercent')
# nb_show_table(
#     all_bigram_common.nlargest(10, ['%Neg', 'AllTokens']).convert_dtypes(),
#     title=f'##### Top 10 Bigrams with Highest *Negative* Percentage ({bigram_min:,}+ tokens)^[Negative trigger bigrams excluded]')
save_latex_table(
    format_zeros(all_bigram_common
                 .nlargest(K, ['%Pos', 'AllTokens']).convert_dtypes()
                 .style.background_gradient('BuPu')),
    verbose=True,
    caption=f'Top {K} Bigrams with Highest <u>Positive Polarity</u> Percentage ({bigram_min:,}+ tokens)',
    latex_subdir='PBR_summary/positive',
    latex_stem=f'top-bigram-PosPercent_{bigram_min}+',
    label=f'top-bigram-PosPercent')
# nb_show_table(
#     all_bigram_common.nlargest(10, ['%Pos', 'AllTokens']).convert_dtypes(),
#     title=f'##### Top 10 Bigrams with Highest *Positive* Percentage ({bigram_min:,}+ tokens)')

# %%
adv_min = 500
all_adv_common = all_adv.loc[
    (all_adv.AllTokens >= adv_min)
    & ~(all_adv.index.str.startswith(
        ("not", "never", "n't")))
    & (all_adv.index != 'no'), :]
# all_adv_common
# nb_show_table(all_adv_common.nlargest(10, ['%Neg', 'AllTokens']).convert_dtypes(),
#               title=f'##### Top 10 Adverbs with Highest *Negative* Percentage ({adv_min:,}+ tokens)')
# nb_show_table(all_adv_common.nlargest(10, ['%Pos', 'AllTokens']).convert_dtypes(),
#               title=f'##### Top 10 Adverbs with Highest *Positive* Percentage ({adv_min:,}+ tokens)')

save_latex_table(
    format_zeros(all_adv_common
                 .nlargest(K, ['%Neg', 'AllTokens']).convert_dtypes()
                 .style.background_gradient('GnBu')),
    verbose=True,
    caption=f'Top {K} Adverbs with Highest <u>Negative Polarity</u> Percentage ({adv_min:,}+ tokens)',
    latex_subdir='PBR_summary/negative',
    latex_stem=f'top{K}-adv-NegPercent_{adv_min}+',
    label=f'top-adv-NegPercent')
save_latex_table(
    format_zeros(all_adv_common
                 .nlargest(K, ['%Pos', 'AllTokens']).convert_dtypes()
                 .style.background_gradient('BuGn')),
    verbose=True,
    caption=f'Top {K} Adverbs with Highest <u>Positive Polarity</u> Percentage ({adv_min:,}+ tokens)',
    latex_subdir='PBR_summary/positive',
    latex_stem=f'top{K}-adv-PosPercent_{adv_min}+',
    label=f'top-adv-PosPercent')

# %%
adj_min = 250
all_adj_common = all_adj.loc[all_adj.AllTokens >= adj_min, :]
# nb_show_table(all_adj_common.nlargest(K, ['%Neg', 'AllTokens']).convert_dtypes(),
#               title=f'##### Top {K} Adjectives with Highest *Negative* Percentage ({adj_min:,}+ tokens)')
# nb_show_table(all_adj_common.nlargest(K, ['%Pos', 'AllTokens']).convert_dtypes(),
#               title=f'##### Top {K} Adjectives with Highest *Positive* Percentage ({adj_min:,}+ tokens)')
save_latex_table(
    format_zeros(all_adj_common
                 .nlargest(K, ['%Neg', 'AllTokens']).convert_dtypes()
                 .style.background_gradient('PuRd')),
    verbose=True,
    caption=f'Top {K} Adjectives with Highest <u>Negative Polarity</u> Percentage ({adj_min:,}+ tokens)',
    latex_subdir='PBR_summary/negative',
    latex_stem=f'top{K}-adj-NegPercent_{adj_min}+',
    label='tab:top-adj-NegPercent')
save_latex_table(
    format_zeros(all_adj_common
                 .nlargest(K, ['%Pos', 'AllTokens']).convert_dtypes()
                 .style.background_gradient('RdPu')),
    verbose=True,
    caption=f'Top {K} Adjectives with Highest <u>Positive Polarity</u> Percentage ({adj_min:,}+ tokens)',
    latex_subdir='PBR_summary/positive',
    latex_stem=f'top{K}-adj-PosPercent_{adj_min}+',
    label='tab:top-adj-PosPercent')


# %%
def _split_bigrams(bigram_counts: pd.DataFrame, strict: bool = False, floor: int = 1):
    _bigram_counts = bigram_counts.copy()
    if strict:
        floor = floor if floor > 1 else 5
    if floor > 1:
        _bigram_counts = _bigram_counts.loc[_bigram_counts.AllTokens >= floor, :]
    return _bigram_counts.index.str.extract(r'^(?P<adv>\S+) (?P<adj>\S+)$')


# %%
bigram_split_any = _split_bigrams(all_bigram)
trivial_bigram_unique_adx = bigram_split_any.nunique()
# %%
bigram_split_5 = _split_bigrams(all_bigram, strict=True)
# bigram_split_5 = all_bigram.loc[all_bigram.AllTokens >= 5, :].index.str.extract(
#     r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$')
bigram_unique_adx_5 = bigram_split_5.nunique()
# %%
bigram_split_2 = _split_bigrams(all_bigram, floor=2)
bigram_unique_adx_2 = bigram_split_2.nunique()
bigram_split_3 = _split_bigrams(all_bigram, floor=3)
bigram_unique_adx_3 = bigram_split_3.nunique()
bigram_split_4 = _split_bigrams(all_bigram, floor=4)
bigram_unique_adx_4 = bigram_split_4.nunique()

# %%
save_latex_table(trivial_bigram_unique_adx.to_frame('trivial').assign(
    strict2=bigram_unique_adx_2,
    strict3=bigram_unique_adx_3,
    strict4=bigram_unique_adx_4,
    strict5=bigram_unique_adx_5,
).style.text_gradient('deep_waters', axis=1),
    verbose=True,
    caption='Unique Values by Minimum Frequency Floor',
    label='tab:pbr-adx-unique-by-f-floor',
    latex_path=TEX_ASSETS.joinpath('tables/PBR_summary/versatility/uniqueADx_by_f-thresh'))
# %%
_fig = (trivial_bigram_unique_adx.to_frame('trivial')
              .assign(strict2=bigram_unique_adx_2,
                      strict3=bigram_unique_adx_3,
                      strict4=bigram_unique_adx_4,
                      strict5=bigram_unique_adx_5,
                      )
        ).plot(kind='bar', cmap='lisa_frank', logy=True, ylabel='# Unique Values (log)',
               title='Unique Values By Bigram Frequency Floor', width=0.65)
plt.xticks(rotation=0)
plt.savefig(RESULT_DIR.joinpath(f'freq_out/images/nunique-ADx-by-freq-floor_ALL-PBR_{timestamp_today()}.png'),
            dpi=300, bbox_inches='tight', pad_inches=0.1)
# %%


def count_unique_partners(split_bigrams: pd.DataFrame,
                          unit: str,
                          nunique_df: int,
                          strict: bool = False):
    swap_adx = {'adv': 'adj', 'adj': 'adv'}
    kind_tag = "strict" if strict else "trivial"
    vers = split_bigrams.value_counts(unit).to_frame(
        f'{kind_tag}_{unit}_versatility')
    print(nunique_df[swap_adx[unit]])
    vers[f'{kind_tag}_%of_{swap_adx[unit]}_forms'
         ] = (vers.squeeze()
              / nunique_df[swap_adx[unit]]) * 100
    return vers  # .assign(unit=unit)[['unit'] + vers.columns.to_list()]


# %%  [markdown]
# ### *Trivial* Versatility
trivial_vers_adv = count_unique_partners(
    bigram_split_any, 'adv',  trivial_bigram_unique_adx)
print(trivial_vers_adv.head().to_markdown(
    tablefmt='simple_outline', floatfmt='.2f', intfmt=','))

trivial_vers_adj = count_unique_partners(
    bigram_split_any, 'adj',  trivial_bigram_unique_adx)
print(trivial_vers_adj.head().to_markdown(
    tablefmt='simple_outline', floatfmt='.2f', intfmt=','))

save_latex_table(pd.concat((trivial_vers_adv.describe().T,
                            trivial_vers_adj.describe().T)).convert_dtypes().style,
                 latex_subdir='PBR_summary/versatility', latex_stem='trivial_vers_adv',
                 label='tab:trivial-vers-adv', verbose=True)

# %% [markdown]
# ### *Strict* Versatility
strict_vers_adv = count_unique_partners(
    bigram_split_5, 'adv',
    nunique_df=trivial_bigram_unique_adx,
    strict=True)
print(strict_vers_adv.head().to_markdown(
    tablefmt='simple_outline', floatfmt='.2f', intfmt=','))

strict_vers_adj = count_unique_partners(
    bigram_split_5, 'adj',
    nunique_df=trivial_bigram_unique_adx,
    strict=True)
print(strict_vers_adj.head().to_markdown(
    tablefmt='simple_outline', floatfmt='.2f', intfmt=','))

nb_show_table(pd.concat((strict_vers_adv.describe().T,
              strict_vers_adj.describe().T)).convert_dtypes())
save_latex_table(pd.concat((strict_vers_adv.describe().T,
                            strict_vers_adv.describe().T)).convert_dtypes().style,
                 latex_subdir='PBR_summary/versatility', latex_stem='strict_vers_adv',
                 label='tab:strict-vers-adv')
# %%
strict_vers_adv.sort_index().join(all_adv.sort_index().filter(['AllTokens'])  # .apply(sqrt).to_frame('AllTokens_sqrt')
                                  ).plot(kind='scatter', loglog=True, x='strict_adv_versatility', y='AllTokens',
                                         title='ADV: Marginal Frequency (sqrt) by Strict Versatility')

# %%
combined_vers_stats = pd.concat(
    (d.describe().T
     for d in [strict_vers_adv,
               trivial_vers_adv,
               strict_vers_adj,
               trivial_vers_adj]
     )
).round(1).convert_dtypes()
save_latex_table(combined_vers_stats.filter(like='vers', axis=0).T.convert_dtypes().style,
                 latex_subdir='PBR_summary/versatility', latex_stem='combined-vers-stats_values')
save_latex_table(combined_vers_stats.filter(like='%', axis=0).T.convert_dtypes().style,
                 latex_subdir='PBR_summary/versatility', latex_stem='combined-vers-stats_percents')

# %%
vers_out_dir = RESULT_DIR/'versatility'
confirm_dir(vers_out_dir)
# %%
adv_vers = strict_vers_adv.join(trivial_vers_adv).fillna(
    0).convert_dtypes().join(all_adv.filter(like='All'))
adv_vers.to_csv(vers_out_dir / 'adverb_versatility.csv')
nb_show_table(adv_vers.nlargest(30, strict_vers_adv.columns[0])
              )
save_latex_table(adv_vers.nlargest(30, strict_vers_adv.columns[0])
                 .style.background_gradient('BuPu'),
                 latex_stem='most-vers-adv',
                 label='tab:most-vers-adv',
                 latex_subdir='PRB_summary/versatility')
save_latex_table(adv_vers.filter(SPECIAL_ADV, axis=0).sort_values('strict_%of_adj_forms', ascending=False)
                 .style.background_gradient('BuPu'),
                 latex_stem='adv-of-interest-vers',
                 label='tab:adv-of-interest-vers',
                 latex_subdir='PRB_summary/versatility')
# %%
adj_vers = strict_vers_adj.join(trivial_vers_adj).fillna(
    0).convert_dtypes().join(all_adj.filter(like='All'))
adv_vers.to_csv(vers_out_dir / 'adjective_versatility.csv')
nb_show_table(adj_vers.nlargest(10, strict_vers_adj.columns[0])
              )
save_latex_table(adj_vers.nlargest(30, strict_vers_adj.columns[0])
                 .style.background_gradient('BuGn'),
                 latex_stem='most-vers-adj', label='tab:most-vers-adj', latex_subdir='PRB_summary/versatility')
# %%


def show_most_versatile(all_pairs, substantial_pairs, k=10):

    most_versatile = substantial_pairs.copy().head(k)
    at_all = all_pairs.filter(most_versatile.index, axis=0).squeeze()
    most_versatile.loc[:, 'diff'] = at_all - most_versatile.squeeze()
    most_versatile.loc[:, 'at_all'] = at_all
    nb_show_table(most_versatile.reset_index())
    return most_versatile

#! #BUG--undefined variables
# versatile_adj = show_most_versatile(unique_adv_per_adj, unique_adv_per_adj_5)
# versatile_adj_20 = show_most_versatile(
#     unique_adv_per_adj, unique_adv_per_adj_5, 20)
# # %%
# versatile_adv = show_most_versatile(unique_adj_per_adv, unique_adj_per_adv_5)
# versatile_adv_20 = show_most_versatile(
#     unique_adj_per_adv, unique_adj_per_adv_5, 20)


# %%
TARGET_ADV = tuple(pd.Series([
    #   top superALL Negatively associated
    'necessarily', 'that', 'exactly', 'any', 'remotely', 'longer', 'ever',
    'immediately', 'yet', 'particularly', 'terribly',
    #   top superNEQ Positively associated
    'increasingly', 'relatively', 'almost', 'mostly', 'seemingly', 'fairly', 'pretty',
    'largely', 'rather', 'sometimes', 'also', 'now', 'probably', 'somewhat', 'potentially',

    'utterly', 'definitely', 'marginally', 'approximately', 'nearly',
    'albeit', 'quite', 'downright', 'absolutely',
    'kinda', 'sorta', 'entirely', 'especially', 'before',
    'only', 'just', 'extremely', 'slightly', 'precisely', 'accurately',

] + ['as', 'so', 'more', 'too', 'very', 'really',
     'always',  'completely', 'even', 'overly', 'less', 'most', 'all', 'totally', 'much',
     'actually', 'super', 'fully', 'merely',
     'also', 'often', 'still',
     'truly', 'highly', 'equally'] + (
    all_adv.loc[(all_adv.AllTokens > 500) & ~(all_adv.index.str.contains(
        NEG_REGEX)), :].nlargest(10, '%Neg').index.to_list()
    + all_adv[all_adv.AllTokens > 500].nlargest(10, '%Pos').index.to_list())
    + sorted(SPECIAL_ADV)
).drop_duplicates().to_list())
all_adv.filter(TARGET_ADV, axis=0)
# %%
format_zeros(all_bigram[~all_bigram.index.str.startswith(("n't", 'not', 'never'))].filter(regex=r''.join(
    [f'|{a} ' for a in TARGET_ADV]), axis=0).nlargest(15, ['%Neg', 'NegTokens']).style.background_gradient('PuBu'))

# %%
all_bigram.filter(regex=r''.join(
    [f'| {a}' for a in EXACTLY_RELEVANT_ADJ]), axis=0).nlargest(15, '%Neg')

# %%
all_bigram.filter(regex=r''.join(
    [f'|{a} ' for a in TARGET_ADV]), axis=0).nlargest(15, ['%Pos', 'PosTokens'])

# %%
save_latex_table(format_zeros(pd.concat((all_bigram.filter(regex=r''.join(
    [f'|{a} ' for a in TARGET_ADV]), axis=0).nlargest(15, '%Pos'),
    all_bigram[~all_bigram.index.str.startswith(("n't", 'not', 'never'))].filter(regex=r''.join(
        [f'|{a} ' for a in TARGET_ADV]), axis=0).nlargest(15, '%Neg'))).style.background_gradient('YlGnBu')),
    latex_subdir='PBR_summary', verbose=True,
    latex_stem='top-relative-freq-combined', label='tab:top-relative-freq-combined'
)

# %%
#! #BUG the structures aren't what are expected and it's not obvious to me what it's looking for
def show_most_versatile_by_pole(adx, _neg_counts, _pos_counts, k=15):

    target_adv_versatility = pd.DataFrame(index=TARGET_ADV)
    most_vers_dict = {}
    top_adv_either = []
    for pole, polar_counts in [('Neg', _neg_counts), ('Pos', _pos_counts)]:
        pol_bigram_counts = polar_counts['bigram']
        pol_bigrams_5 = pol_bigram_counts.copy()[
            pol_bigram_counts.squeeze() >= 5]
        pol_bigrams_5.info()
        print(pol_bigrams_5.head())
        # neg_adv_unique_partners_5 = count_unique_partners(pol_bigrams_5, 'adv')
        # neg_adj_unique_partners_5 = count_unique_partners(pol_bigrams_5, 'adj')
        if adx == 'adv':
            try:  # HACK
                target_adv_versatility = target_adv_versatility.join(
                    count_unique_partners(pol_bigrams_5, adx,
                                          trivial_bigram_unique_adx
                                          )
                    .to_frame(f"{pole}Vers")
                    .filter(TARGET_ADV, axis=0))
            except KeyError:
                pass
        _most_vers = show_most_versatile(
            all_pairs=count_unique_partners(pol_bigram_counts, adx,
                                            trivial_bigram_unique_adx
                                            ).to_frame(
                f'{pole}{adx.upper()}_with_most_unique'),
            substantial_pairs=count_unique_partners(pol_bigrams_5, adx,
                                                    trivial_bigram_unique_adx
                                                    ).to_frame(
                f'{pole}{adx.upper()}_with_most_unique_5+'),
            k=k)
        top_adv_either.extend(_most_vers.index.to_list())
        most_vers_dict[pole] = _most_vers
    pos_vers = most_vers_dict['Pos']
    neg_vers = most_vers_dict['Neg']
    if adx == 'adv' and not target_adv_versatility.empty:
        # nb_show_table(target_adv_versatility)
        return target_adv_versatility.fillna(0), pos_vers, neg_vers
    return pos_vers, neg_vers


# %%
target_adv_vers, pos_adv_vers, neg_adv_vers = show_most_versatile_by_pole(
    'adv', neg_counts, pos_counts, k=30)
# %%
target_adv_vers = target_adv_vers.assign(
    NegVersOdds=target_adv_vers.NegVers / target_adv_vers.PosVers,
    PosMinusNegVers=target_adv_vers.PosVers - target_adv_vers.NegVers
).sort_values('NegVersOdds', ascending=False)
nb_show_table(target_adv_vers, n_dec=4)
# %%
target_adv_vers = (
    target_adv_vers
    .join(bigram_split_5.value_counts('adv')[target_adv_vers.index].squeeze().to_frame('AllVers'))
    .join(all_adv.filter(target_adv_vers.index, axis=0)))
target_adv_info = target_adv_vers.assign(
    NegVersPercent=target_adv_vers.NegVers / target_adv_vers.AllVers * 100
)[['NegVers', 'PosVers', 'AllVers',
   'NegVersOdds', 'PosMinusNegVers', 'NegVersRatio',
   'AllTokens', 'PosTokens', 'NegTokens', '%Neg', '%Pos']]
nb_show_table(
    target_adv_info,
    n_dec=1)
# %%
show_most_versatile_by_pole('adj', neg_counts, pos_counts)

# %%
immediately_bigrams = all_bigram.filter(like='immediately', axis=0)
immediately_margin = all_adv.loc['immediately', :].squeeze()
immediately_bigrams = immediately_bigrams.T.assign(
    immediately_MARGIN=immediately_margin).T
immediately_bigrams['%All_immediately'] = immediately_bigrams.AllTokens / \
    immediately_margin['AllTokens'] * 100
immediately_bigrams['%Neg_immediately'] = immediately_bigrams.NegTokens / \
    immediately_margin['NegTokens'] * 100
immediately_bigrams['%Pos_immediately'] = immediately_bigrams.PosTokens / \
    immediately_margin['PosTokens'] * 100
nb_show_table(immediately_bigrams.nlargest(10, '%Neg_immediately'))
# %%
nb_show_table(immediately_bigrams.nlargest(10, '%Neg'))


# # %%
# # super_adgrams['bigram_lower'] = (super_adgrams.adv_form_lower.astype('string') + '_' + super_adgrams.adj_form_lower).astype('string')
# print(f'{super_adgrams.bigram_lower.nunique():,} unique bigram types (case-normalized forms)---attested combinations of',
#       f'{super_adgrams.adv_form_lower.nunique():,} adverb types and',
#       f'{super_adgrams.adj_form_lower.nunique():,} adjective types.')

# nb_show_table(super_adgrams.bigram_lower.value_counts().nlargest(
#     10).to_frame().reset_index())

# # %% [markdown]
# # _How many unique sentences?_

# # %%
# super_adgrams['sent_id'] = super_adgrams.index.str.split(':').str.get(0)

# # %%
# print(f'There are {super_adgrams.sent_id.nunique():,} unique sentences in PBR')
# nb_show_table(super_adgrams.describe().T.convert_dtypes())

# %%
