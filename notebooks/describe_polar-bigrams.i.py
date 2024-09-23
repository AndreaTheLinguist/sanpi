# %%
from pathlib import Path
from sys import exit as sys_exit
from math import sqrt
import pandas as pd

from am_notebooks import nb_show_table
from source.utils import SANPI_HOME, timestamp_today
from source.utils.dataframes import NEG_REGEX, REGNOT

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
            # ! Needed to deal with how pandas.read_csv treats the string "null"
            loaded_counts.index = loaded_counts.index.fillna('null')
            counts_dict[unit] = loaded_counts
    # neg_adj_counts = pd.read_csv(
    #     neg_adj_out, engine='c', low_memory=True, index_col='adj_form_lower')
    # neg_big_counts = pd.read_csv(
    #     neg_big_out, engine='c', low_memory=True, index_col='bigram_lower')
    return counts_dict


def count_hits(redo_neg=False):

    neg_ids = Path('/share/compling/data/sanpi/2_hit_tables/RBdirect/ALL_RBdirect_final-index.txt'
                   ).read_text().splitlines()
    pos_ids = Path('/share/compling/data/sanpi/2_hit_tables/not-RBdirect/ALL_not-RBdirect_final-index.txt'
                   ).read_text().splitlines()
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
        .join(pos_unit.rename(columns={'count': 'Pos_tokens'}))
        .join(neg_unit.rename(columns={'count': 'Neg_tokens'}))
        .fillna(0)
    )
    all_unit['All_tokens'] = (all_unit.Pos_tokens + all_unit.Neg_tokens)
    all_unit = all_unit.astype('int').sort_values('All_tokens', ascending=False)[
        ['All_tokens', 'Pos_tokens', 'Neg_tokens']]
    all_unit['%_Neg'] = ((all_unit.Neg_tokens / all_unit.All_tokens)
                         * 100).astype('float64').round(3)
    all_unit['%_Pos'] = ((all_unit.Pos_tokens / all_unit.All_tokens)
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

# %%
bigram_min = 100
all_bigram_common = all_bigram.loc[
    (all_bigram.All_tokens >= bigram_min)
    & ~(all_bigram.index.str.startswith(("not", "no_", "never", "n't"))), :]
nb_show_table(
    all_bigram_common.nlargest(10, ['%_Neg', 'All_tokens']).convert_dtypes(),
    title=f'##### Top 10 Bigrams with Highest *Negative* Percentage ({bigram_min:,}+ tokens)^[Negative trigger bigrams excluded]')
nb_show_table(
    all_bigram_common.nlargest(10, ['%_Pos', 'All_tokens']).convert_dtypes(),
    title=f'##### Top 10 Bigrams with Highest *Positive* Percentage ({bigram_min:,}+ tokens)')

# %%
adv_min = 1000
all_adv_common = all_adv.loc[(all_adv.All_tokens >= adv_min), :]
all_adv_common
nb_show_table(all_adv_common.nlargest(10, ['%_Neg', 'All_tokens']).convert_dtypes(),
              title=f'##### Top 10 Adverbs with Highest *Negative* Percentage ({adv_min:,}+ tokens)')
nb_show_table(all_adv_common.nlargest(10, ['%_Pos', 'All_tokens']).convert_dtypes(),
              title=f'##### Top 10 Adverbs with Highest *Positive* Percentage ({adv_min:,}+ tokens)')

# %%
adj_min = 200
all_adj_common = all_adj.loc[all_adj.All_tokens >= adj_min, :]
nb_show_table(all_adj_common.nlargest(10, ['%_Neg', 'All_tokens']).convert_dtypes(),
              title=f'##### Top 10 Adjectives with Highest *Negative* Percentage ({adj_min:,}+ tokens)')
nb_show_table(all_adj_common.nlargest(10, ['%_Pos', 'All_tokens']).convert_dtypes(),
              title=f'##### Top 10 Adjectives with Highest *Positive* Percentage ({adj_min:,}+ tokens)')


# %%
def _split_bigrams(bigram_counts: pd.DataFrame, strict: bool = False, floor: int = 1):
    _bigram_counts = bigram_counts.copy()
    if strict:
        floor = floor if floor > 1 else 5
    if floor > 1:
        _bigram_counts = _bigram_counts.loc[_bigram_counts.All_tokens >= floor, :]
    return _bigram_counts.index.str.extract(r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$')


# %%
bigram_split_any = _split_bigrams(all_bigram)
trivial_bigram_unique_adx = bigram_split_any.nunique()
# %%
bigram_split_5 = _split_bigrams(all_bigram, strict=True)
# bigram_split_5 = all_bigram.loc[all_bigram.All_tokens >= 5, :].index.str.extract(
#     r'^(?P<adv>[^_]+)_(?P<adj>[^_]+)$')
bigram_unique_adx_5 = bigram_split_5.nunique()
# %%
bigram_split_2 = _split_bigrams(all_bigram, floor=2)
bigram_unique_adx_2 = bigram_split_2.nunique()
bigram_split_3 = _split_bigrams(all_bigram, floor=3)
bigram_unique_adx_3 = bigram_split_3.nunique()
nb_show_table(trivial_bigram_unique_adx.to_frame('trivial')
              .assign(strict2=bigram_unique_adx_2,
                      strict3=bigram_unique_adx_3,
                      strict5=bigram_unique_adx_5,
                      ))

# %%
def count_unique_partners(split_bigrams: pd.DataFrame,
                          unit: str,
                          nunique_df: int,
                          strict: bool = False):
    swap_adx = {'adv': 'adj', 'adj': 'adv'}
    kind_tag = "strict" if strict else "trivial"
    vers = split_bigrams.value_counts(unit).to_frame(
        f'{kind_tag}_{unit}_versatility')
    vers[f'{kind_tag}_%of_{swap_adx[unit]}_forms'
         ] = (vers.squeeze()
              / nunique_df[swap_adx[unit]]) * 100
    return vers#.assign(unit=unit)[['unit'] + vers.columns.to_list()]


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

nb_show_table(pd.concat((trivial_vers_adv.describe().T,
              trivial_vers_adj.describe().T)).convert_dtypes())

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
# %%
strict_vers_adv.join(all_adv.All_tokens.apply(sqrt).to_frame('All_tokens_sqrt')).plot(kind='scatter', x='strict_adv_versatility', y='All_tokens_sqrt', title='ADV: Marginal Frequency (sqrt) by Strict Versatility')

# %%
combined_vers_stats = pd.concat(
    (d.describe().T 
     for d in [strict_vers_adv,
               trivial_vers_adv,
              strict_vers_adj, 
              trivial_vers_adj]
     )
    ).round(1).convert_dtypes()
nb_show_table(combined_vers_stats.filter(like='vers', axis=0))
nb_show_table(combined_vers_stats.filter(like='%', axis=0))

# %%
adv_vers = strict_vers_adv.join(trivial_vers_adv).fillna(0).convert_dtypes().join(all_adv.filter(like='All'))
nb_show_table(adv_vers.nlargest(30, strict_vers_adv.columns[0])
      )
# %%
adj_vers = strict_vers_adj.join(trivial_vers_adj).fillna(0).convert_dtypes().join(all_adj.filter(like='All'))
nb_show_table(adj_vers.nlargest(10, strict_vers_adj.columns[0])
      )
# %%


def show_most_versatile(all_pairs, substantial_pairs, k=10):

    most_versatile = substantial_pairs.copy().head(k)
    at_all = all_pairs.filter(most_versatile.index, axis=0).squeeze()
    most_versatile.loc[:, 'diff'] = at_all - most_versatile.squeeze()
    most_versatile.loc[:, 'at_all'] = at_all
    nb_show_table(most_versatile.reset_index())
    return most_versatile


versatile_adj = show_most_versatile(unique_adv_per_adj, unique_adv_per_adj_5)
versatile_adj_20 = show_most_versatile(
    unique_adv_per_adj, unique_adv_per_adj_5, 20)
# %%
versatile_adv = show_most_versatile(unique_adj_per_adv, unique_adj_per_adv_5)
versatile_adv_20 = show_most_versatile(
    unique_adj_per_adv, unique_adj_per_adv_5, 20)

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
    all_adv.loc[(all_adv.All_tokens > 500) & ~(all_adv.index.str.contains(
        NEG_REGEX)), :].nlargest(10, '%_Neg').index.to_list()
    + all_adv[all_adv.All_tokens > 500].nlargest(10, '%_Pos').index.to_list())
).drop_duplicates().to_list())
all_adv.filter(TARGET_ADV, axis=0)
# %%
all_bigram.filter(regex=r''.join(
    [f'|{a}_' for a in TARGET_ADV]), axis=0).nlargest(15, '%_Neg')

# %%
all_bigram.filter(regex=r''.join(
    [f'|{a}_' for a in TARGET_ADV]), axis=0).nlargest(15, '%_Pos')

# %%


def show_most_versatile_by_pole(adx, neg_counts, pos_counts, k=15):

    target_adv_versatility = pd.DataFrame(index=TARGET_ADV)
    most_vers_dict = {}
    top_adv_either = []
    for pole, polar_counts in [('Neg', neg_counts), ('Pos', pos_counts)]:
        pol_bigram_counts = polar_counts['bigram']
        pol_bigrams_5 = pol_bigram_counts.copy()[
            pol_bigram_counts.squeeze() >= 5]
        # neg_adv_unique_partners_5 = count_unique_partners(pol_bigrams_5, 'adv')
        # neg_adj_unique_partners_5 = count_unique_partners(pol_bigrams_5, 'adj')
        if adx == 'adv':
            target_adv_versatility = target_adv_versatility.join(
                count_unique_partners(pol_bigrams_5, adx)
                .to_frame(f"{pole}Vers")
                .filter(TARGET_ADV, axis=0))

        _most_vers = show_most_versatile(
            all_pairs=count_unique_partners(pol_bigram_counts, adx).to_frame(
                f'{pole}{adx.upper()}_with_most_unique'),
            substantial_pairs=count_unique_partners(pol_bigrams_5, adx).to_frame(
                f'{pole}{adx.upper()}_with_most_unique_5+'),
            k=k)
        top_adv_either.extend(_most_vers.index.to_list())
        most_vers_dict[pole] = _most_vers
    pos_vers = most_vers_dict['Pos']
    neg_vers = most_vers_dict['Neg']
    if adx == 'adv':
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
   'All_tokens', 'Pos_tokens', 'Neg_tokens', '%_Neg', '%_Pos']]
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
immediately_bigrams['%_All_immediately'] = immediately_bigrams.All_tokens / \
    immediately_margin['All_tokens'] * 100
immediately_bigrams['%_Neg_immediately'] = immediately_bigrams.Neg_tokens / \
    immediately_margin['Neg_tokens'] * 100
immediately_bigrams['%_Pos_immediately'] = immediately_bigrams.Pos_tokens / \
    immediately_margin['Pos_tokens'] * 100
nb_show_table(immediately_bigrams.nlargest(10, '%_Neg_immediately'))
# %%
nb_show_table(immediately_bigrams.nlargest(10, '%_Neg'))


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
