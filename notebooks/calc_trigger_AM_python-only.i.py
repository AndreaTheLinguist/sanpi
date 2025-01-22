# %% [markdown]
# # Calculating Trigger ~ `UNIT` frequencies and AMs directly from final parquets
# initiated: _January 16, 2025_
# > The previously authored notebook `calc_trigger_AM.*` relies on `UCS` command line tools,
# > which this attempt will not, thereby simplifying the pipeline and file outputs.
#
# Loading imports
from am_notebooks import *
from source.utils.LexicalCategories import SPECIAL_ADV
from association_measures import frequencies as amfq, measures as amms

L1 = 'trigger_lemma'
L2 = 'adv_form_lower'

HIT_DATA_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
NEG_SUPER_PARQ = HIT_DATA_DIR.joinpath('RBdirect/ALL-RBdirect_final.parq')
POS_SUPER_PARQ = HIT_DATA_DIR.joinpath(
    'not-RBdirect/ALL_not-RBdirect_final.parq')
NEG_MIRROR_PARQ = HIT_DATA_DIR.joinpath('NEGmirror/ALL-NEGmirror_final.parq')
POS_MIRROR_PARQ = HIT_DATA_DIR.joinpath('POSmirror/ALL-POSmirror_final.parq')


def rename_trigger_dep_info(df):
    if df.filter(['neg_head', 'mir_head', 'neg_deprel', 'mir_deprel']).empty:
        return df
    return df.assign(
        trigger_head=df.filter(
            ['neg_head', 'mir_head']).iloc[:, 0],
        trigger_deprel=df.filter(
            ['neg_deprel', 'mir_deprel']).iloc[:, 0],
    )


def fix_word_null(df):
    """Fix null values in adjective and adverb columns.

    This function replaces null values in 'adj_form_lower' and 'adv_form_lower'
    columns of a DataFrame with the string 'null'. 
    That is, these are cases where the string "null" 
    was improperly interpreted as '<NA>' rather than the literal word, "null".

    Args:
        df: Pandas DataFrame containing 'adj_form_lower' and 'adv_form_lower' columns.

    Returns:
        Pandas DataFrame with null values in specified columns replaced with 'null'.
    """

    return df.assign(adj_form_lower=df.adj_form_lower.fillna('null'),
                     adv_form_lower=df.adv_form_lower.fillna('null'),
                     trigger_lower=df.trigger_lower.fillna('null'))


def load_trigger_info(parq_paths):
    sources = []
    trig_node = 'neg'
    polarity = 'neg'
    for path in parq_paths:
        if 'POS' in path.stem:
            trig_node = 'mir'
            polarity = 'pos'
        _df = pd.read_parquet(
            path, engine='pyarrow',
            columns=pd.Series(
                [L1, L2] +
                ['trigger_lemma', 'trigger_lower', 'bigram_lower',
                 f'{trig_node}_head', f'{trig_node}_deprel',
                 'adv_form_lower', 'adj_form_lower']
            ).drop_duplicates().to_list())
        _df = rename_trigger_dep_info(_df)
        _df = _df.assign(polarity=polarity).convert_dtypes()
        sources.append(_df)
    trigger_df = pd.concat(sources) if len(sources) > 1 else sources[0]
    trigger_df = trigger_df.loc[:, ~
                                trigger_df.columns.str.startswith(('neg_', 'mir_'))]
    trigger_df = fix_word_null(trigger_df)
    if any(trigger_df.trigger_lemma.str.startswith('ain')):
        aint_triggered = trigger_df.trigger_lemma.isin(["ain't", "aint"])
        trigger_df.loc[aint_triggered, :] = trigger_df.loc[aint_triggered, :].assign(
            trigger_lemma='not')
    trigger_df.info()
    return trigger_df


# %%
df_super_neg = load_trigger_info([NEG_SUPER_PARQ])
df_super_neg.describe().T.iloc[:, 1:].convert_dtypes()
# save_latex_table(
#     sty=(df_super_neg.groupby('trigger_lemma').value_counts(
#         ['trigger_lower']).to_frame()
#         .style
#         .background_gradient(axis=0, cmap='YlGnBu')
#         .format(precision=1, thousands=',', escape='latex')),
#     caption=(r'Negative Trigger Lemma Composition: attested forms'),
#     label='trig-lemma-vs-form',
#     longtable=True,
#     latex_subdir='triggers',
#     latex_stem='super-neg-trigger_lemma-form_counts')

# %%
df_mirror = load_trigger_info([NEG_MIRROR_PARQ, POS_MIRROR_PARQ])
df_mirror.describe().T.iloc[:, 1:].convert_dtypes()
# %%
save_latex_table(
    sty=(df_mirror.groupby(['polarity', 'trigger_lemma']).value_counts(
        ['trigger_lower']).to_frame()
        .style
        .background_gradient(axis=0, cmap='purple_rain')
        .format(precision=0, thousands=',', escape='latex')),
    caption=(r'Mirror Subset Trigger Lemma Composition: attested forms'),
    label='trig-lemma-vs-form-subset',
    longtable=True,
    latex_subdir='triggers',
    latex_stem='mirror-trigger_lemma-form_counts')
# %%
df_mirror_neg = load_trigger_info([NEG_MIRROR_PARQ])
df_mirror_neg.describe().T.iloc[:, 1:].convert_dtypes()
# %%
save_latex_table(
    sty=(df_mirror_neg.groupby(['polarity', 'trigger_lemma']).value_counts(
        ['trigger_lower']).to_frame()
        .style
        .background_gradient(axis=0, cmap='purple_rain')
        .format(precision=0, thousands=',', escape='latex')),
    caption=(r'Negative Mirror Subset Trigger Lemma Composition: attested forms'),
    label='trig-lemma-vs-form-subset',
    longtable=True,
    latex_subdir='triggers',
    latex_stem='mirror-neg-trigger_lemma-form_counts')

# %%


def add_assoc_key(_df,
                  l1: str = L1,
                  l2: str = L2):  # sourcery skip: use-fstring-for-concatenation
    _df['key'] = _df[l1] + '~' + _df[l2]
    return _df.set_index('key')


def add_marginal_cols(_df, _fdf,
                      l1: str = L1,
                      l2: str = L2):
    _fdf['f1'] = _fdf[l1].map(_df.value_counts(l1))
    _fdf['f2'] = _fdf[l2].map(_df.value_counts(l2))
    return _fdf


def get_joint_f(_df,
                l1: str = L1,
                l2: str = L2):
    fdf = _df.value_counts([l1, l2]).to_frame('f').reset_index()
    fdf = add_assoc_key(fdf, l1=l1, l2=l2).assign(N=len(_df))
    return add_marginal_cols(_fdf=fdf, _df=_df, l1=l1, l2=l2)


def calc_trigger_assoc(trigger_info_df):
    freq_df = get_joint_f(trigger_info_df)
    freq_df = freq_df.rename(columns={L1: 'l1', L2: 'l2'})
    display(set_my_style(freq_df.nlargest(10, 'f')))

    freq_df = freq_df.join(
        amfq.expected_frequencies(
            freq_df, observed=True),
        rsuffix='_X')
    freq_df = freq_df.loc[:, ~freq_df.columns.str.endswith('_X')]
    # display(set_my_style(freq_df.nlargest(10, 'f')))

    _am_df = adjust_am_names(amms.score(
        freq_df, measures=['conservative_log_ratio', 'log_likelihood']))
    _am_df['dP1'] = freq_df.apply(deltaP, axis=1)
    _am_df['dP2'] = freq_df.apply(deltaP, given=1, axis=1)
    _am_df = extend_deltaP(_am_df, extensions=('mean', 'max'))
    _am_df = _am_df.assign(
        f=freq_df.f,
        f1=freq_df.f1,
        f2=freq_df.f2,
        l1=freq_df.l1,
        l2=freq_df.l2,
    )
    # display(set_my_style(_am_df.nlargest(10, 'LRC')))

    _am_df['unexp_f'] = freq_df['f'] - \
        _am_df['exp_f']
    _am_df['unexp_r'] = (
        _am_df['f'] / _am_df['unexp_f']).apply(lambda r: max(r, -1))
    # pprint(trigger_info_df.set_index(L1).polarity.to_dict())
    _am_df['polarity'] = _am_df.l1.map(
        trigger_info_df.set_index(L1).polarity.to_dict()).astype('category')
    display(_am_df.polarity.value_counts())
    display(set_my_style(_am_df.nlargest(10, 'LRC')))
    return _am_df


am_trig_adv_super = calc_trigger_assoc(df_super_neg)
# %%
am_trig_adv_mirror = calc_trigger_assoc(df_mirror)
# %%
am_trig_adv_negmir = calc_trigger_assoc(df_mirror_neg)
# %%


def limit_am_df(full_am_df):

    return full_am_df.filter(
        adjust_am_names(
            BASIC_FOCUS+DELTA_COLS
            + P2_COLS+FREQ_COLS +
            ['polarity'])).assign(
                polar_int=pd.to_numeric(
                    full_am_df.polarity.map({'neg': -1, 'pos': +1}),
                    downcast='integer'))


am_trig_adv = limit_am_df(am_trig_adv_super)
mir_am_trig_adv = limit_am_df(am_trig_adv_mirror)
negmir_am_trig_adv = limit_am_df(am_trig_adv_negmir)

for view, am_df in {'NEG Superset (-)': am_trig_adv, 'Mirror Subset (+/-)': mir_am_trig_adv,
                    'NEG Mirror Subset (-)': negmir_am_trig_adv}.items():
    caption = f'<b>{view}</b><br/>Trigger~Adverb Association<br/>Top LRC values'
    sty = (am_df.filter(regex=r'^[^lNe]')
           .nlargest(3000, 'f2')
           .nlargest(20, 'LRC')
           .sort_index(axis=1)
           .style
           .background_gradient('PuRd'))
    save_latex_table(sty, latex_stem=f"trig-adv_AM-topLRC_{view.strip('(-/+) ').replace(' ','_')}", 
                     latex_subdir='triggers', caption=caption, longtable=True, 
                     label=f"trig-adv-AMtop-{view.replace(' ','')[:6]}")
    display(set_my_style(sty))

# %% [markdown]
# NOTE: It appears not all tokens in the negative superset make it into the subset,
# even if the trigger lemma is included.
# This is illustrated by the difference in `f` shown above for `no~longer` 👆
# There are $768$ co-occurrences for _no_ and _longer_ in the negative superset,
# but only $764$ in the mirror subset.
# This is due to additional constraints applied to the subset:
# Since both positive and negative triggers were required,
# both positive and negative pattern matches excluded the presence of the opposing trigger type.
# The "missing" 4 tokens must have had a positive mirror trigger present in the preceding string?
#
# That may not be a sufficient explanation though, because sometimes there are _more_ tokens in the mirror subset than in the superset...

subset_conflict = mir_am_trig_adv.filter(
    am_trig_adv.index, axis=0).sort_index().loc[
        (am_trig_adv
         .filter(mir_am_trig_adv.index, axis=0)
         .sort_index().f)
    != (mir_am_trig_adv
        .filter(am_trig_adv.index, axis=0).sort_index().f)]

super_conflict = am_trig_adv.filter(
    mir_am_trig_adv.index, axis=0).sort_index().loc[
        (am_trig_adv
         .filter(mir_am_trig_adv.index, axis=0)
         .sort_index().f)
    != (mir_am_trig_adv
        .filter(am_trig_adv.index, axis=0).sort_index().f)]

conflict = (super_conflict
            .filter(['f', 'f1', 'f2', 'dP1', 'LRC', 'dP2'])
            ).join((subset_conflict.filter(
                ['f', 'f1', 'f2', 'dP1', 'LRC', 'dP2'])),
    rsuffix='_mir', lsuffix='_sup').sort_index(axis=1)
conflict['f_diff'] = (conflict.f_sup - conflict.f_mir)
conflict['f1_diff'] = (conflict.f1_sup - conflict.f1_mir)
# conflict['f2_diff'] = (conflict.f2_sup - conflict.f2_mir)
display(set_my_style(conflict.sort_values('f_diff'))
        .background_gradient('PRGn',
                             subset=conflict.filter(like='diff').columns))
# %%
am_trig_adv['l2_exactly'] = am_trig_adv.l2 == 'exactly'
am_trig_exactly = am_trig_adv.loc[am_trig_adv.l2_exactly].reset_index(
).set_index('l1')
am_trig_exactly['OTHERS_f'] = am_trig_exactly.f1 - am_trig_exactly.f
# %%
mir_am_trig_adv['l2_exactly'] = mir_am_trig_adv.l2 == 'exactly'
mir_am_trig_exactly = mir_am_trig_adv.loc[mir_am_trig_adv.l2_exactly].reset_index(
).set_index('l1')
mir_am_trig_exactly['OTHERS_f'] = mir_am_trig_exactly.f1 - \
    mir_am_trig_exactly.f
# %%
# set_my_style(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1'])
#              .sort_values('f1', ascending=False),
#              caption=('Trigger Frequencies<br/>'
#                       'with <i>exactly</i> vs. other adverbs')
#              ).bar(axis=0, cmap='purple_rain').relabel_index(
#     labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
#     axis=1)
# %%
# set_my_style(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1'])
#              .iloc[1:, :].sort_values('f1', ascending=False),
#              caption=('Trigger Frequencies <u>other than "<i>not</i>"</u><br/>'
#                       'with <i>exactly</i> vs. other adverbs')
#              ).bar(axis=0, cmap='purple_rain').relabel_index(
#     labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
#     axis=1)
# %%
for am_df in [am_trig_exactly, mir_am_trig_exactly]:
    display(save_html(set_my_style(
        (transform_counts(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1']))
         .sort_values('f1', ascending=False)),
        caption=('Square Root Transformed Trigger Frequencies<br/>'
                 'with <i>exactly</i> vs. other adverbs'),
        precision=1)
        .bar(axis=0, cmap='YlGnBu')
        .relabel_index(labels=['with <i>exactly</i>',
                               'with<u>out</u> <i>exactly</i>',
                               'Total'],
                       axis=1),
        subdir='triggers', stem='trigger-f_exactly-vs-others'))

    save_latex_table(
        (transform_counts(
            am_trig_exactly.filter(['f', 'OTHERS_f', 'f1']))
         .sort_values('f1', ascending=False)
         .style
         .background_gradient(axis=0, cmap='YlGnBu')
         .relabel_index(
            labels=['with <i>exactly</i>',
                    'with<u>out</u> <i>exactly</i>',
                    'Total'], axis=1)
         .format(precision=1, thousands=',', escape='latex')),
        caption=(r'Square Root Transformed Trigger Frequencies\\'
                 'with <i>exactly</i> vs. other adverbs'),
        label='trig-exactly-others',
        latex_path=WRITING_LINKS.joinpath(
            f'cluster/triggers/trigger_x_exactly-vs-others_freq.{timestamp_today()}.tex')
    )
# %%
# set_my_style(transform_counts(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1']))
#              .iloc[1:, :].sort_values('f1', ascending=False),
#              caption=('Square Root Transformed <u>Other</u> Trigger Frequencies<br/>'
#                       'with <i>exactly</i> vs. other adverbs')
#              ).background_gradient(axis=0, cmap='BuPu').relabel_index(
#     labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
#     axis=1)
# %%
# am_trig_adv[['l1','f','l2_exactly']].plot(kind='barh', subplots=True)
# %%
am_trig_exactly.filter(['f', 'OTHERS_f']).plot(
    kind='barh', logx=True, subplots=True)
am_trig_exactly.filter(['OTHERS_f']).plot(kind='box')
# %%
display(am_trig_exactly
        .sort_values('f', ascending=False))
style_crosstab(am_trig_exactly.reset_index(),
               ['l1'], ['l2'], 'f', aggfunc='sum')
# %%
# df_super_pos = pd.read_parquet(POS_SUPER_PARQ, columns=[
#                              'adv_form_lower', 'adj_form_lower']).assign()
# df_super = pd.concat([df_super_neg, df_super_pos])

save_latex_table(
    format_zeros(
        am_trig_exactly
        .reset_index()
        .rename(
            columns={'l1': 'trigger lemma', 'l2': 'adverb'})
        .set_index(['trigger lemma', 'adverb'])
        .filter(['LRC', 'dP1', 'dP2', 'G2'])
        .stack().unstack(['adverb', -1])
        .sort_values(('exactly', 'LRC'), ascending=False)
        .style
        .format(precision=2, thousands=',', escape='latex')
        .background_gradient('RdBu_r')
    ),
    label='trigger-exactly-AM',
    caption='Negative Trigger$\sim$<i>Exactly</i> Association',
    latex_path=WRITING_LINKS.joinpath(
        f'cluster/triggers/trigger-exactly_AM-rbdirect.{timestamp_today()}.tex')

)
# %% [markdown]
# ## Just *exactly*, but more info
exactly_df = pd.read_parquet(
    NEG_SUPER_PARQ,
    columns=['bigram_id', 'hit_id', 'all_forms_lower',
             'trigger_lemma', 'trigger_lower', 'bigram_lower',
             'adv_form_lower', 'adj_form_lower', 'adj_lemma',
             'neg_head', 'neg_deprel', 'category', 'pattern'],
    # filters=[('adv_form_lower', 'in', SPECIAL_ADV)]
    filters=[('adv_form_lower', '==', 'exactly')]
)
exactly_df = rename_trigger_dep_info(exactly_df)
exactly_df.describe()

# exactly_trig_f = get_joint_f(exactly_df,l2='bigram_lower').reset_index()
exactly_df['f'] = exactly_df.all_forms_lower.map(
    exactly_df.value_counts(
        'all_forms_lower').astype('int64').to_dict())
exactly_df['f1'] = exactly_df.trigger_lemma.map(
    exactly_df.value_counts(
        'trigger_lemma').astype('int64').to_dict())
display(set_my_style(exactly_df.filter(
    like='f').drop_duplicates().nlargest(10, 'f')))

display(style_crosstab(exactly_df, ['trigger_lemma'],
                       ['adv_form_lower', 'neg_head'],
                       'f', aggfunc='sum',
                       axis=None,
                       group=False,
                       cmap='purple_rain'))

# %% [markdown]
# The `am_notebooks.style_crosstab()` method applies table-wide formatting via `am_notebooks.set_my_style()`
# that does not convert to latex properly.
#
# To get around this, return the crosstabulated table using `return_cross_df=True`,
# and apply the `background_gradient` directly.
#
# Remember that `background_gradient` applies to individual columns by default:
# use `axis=None` to apply same gradient to whole table.

f_ct_df = style_crosstab(
    exactly_df, ['trigger_lemma'],
    ['adv_form_lower', 'neg_head'],
    'f', aggfunc='sum',
    return_cross_df=True
).fillna(0).convert_dtypes()

sty = (f_ct_df.style
       .background_gradient(
           #    cmap='YlGnBu',
           axis=None, vmax=25000)
       .format(precision=0, thousands=','))


# %% [markdown]
# If running on the cluster, set latex_path explicitly. Else, just pass subdir and stem
#
# `latex_path=SANPI_HOME.joinpath(f'info/writing_links/cluster/trigger-x-exactly_freq.{timestamp_today()}.tex')`

latex_path = SANPI_HOME.joinpath(
    f'info/writing_links/cluster/trigger_x_exactly-head_freq.{timestamp_today()}.tex')
save_latex_table(
    sty, latex_path=latex_path,
    label='trig-exactly-head-f',
    caption=('Superset Negative Trigger Co-Occurences with <i>Exactly</i> Bigrams,'
             r'\\Grouped by head of trigger dependency'))

# %%
exactly_df = exactly_df.join(
    transform_counts(exactly_df.filter(['f', 'f1', 'f2'])),
    rsuffix='_sqrt')
display(style_crosstab(exactly_df, ['trigger_lemma'],
                       ['adv_form_lower', 'neg_head'],
                       'f_sqrt',
                       aggfunc='sum',
                       axis=None,
                       group=False,
                       cmap='RdPu'))

# %%
# (style_crosstab(df,
#                 ['bigram_lower'],
#                 ['trigger_lemma'],
#                 'f',
#                 aggfunc='sum',
#                 return_cross_df=True)
#  .fillna(0).style.background_gradient('RdPu'))
# %%
amfq.observed_frequencies(df, N=N)
