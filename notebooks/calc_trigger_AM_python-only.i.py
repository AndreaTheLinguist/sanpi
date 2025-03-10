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
pd.set_option('display.max_colwidth', 15)
pd.set_option('display.max_columns', 6)
pd.set_option('display.width', 120)
HIT_DATA_DIR = Path('/share/compling/data/sanpi/2_hit_tables')
NEG_SUPER_PARQ = HIT_DATA_DIR.joinpath('RBdirect/ALL-RBdirect_final.parq')
POS_SUPER_PARQ = HIT_DATA_DIR.joinpath(
    'not-RBdirect/ALL_not-RBdirect_final.parq')
NEG_MIRROR_PARQ = HIT_DATA_DIR.joinpath('NEGmirror/ALL-NEGmirror_final.parq')
POS_MIRROR_PARQ = HIT_DATA_DIR.joinpath('POSmirror/ALL-POSmirror_final.parq')
print(timestamp_today())


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
            columns=(pd.Series(
                [L1, L2] +
                ['trigger_lemma', 'trigger_lower', 'bigram_lower',
                 f'{trig_node}_head', f'{trig_node}_deprel',
                 'adv_form_lower', 'adj_form_lower', 'bigram_id']
            ).drop_duplicates().to_list()))
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
print(df_super_neg.describe().T.iloc[:, 1:].convert_dtypes())
# %%


def display_trigger_totals(_df, dataset='superset',
                           polar='negative',
                           cross='lower',
                           cmap='YlGnBu'):
    x = f'trigger_{cross}'
    cross_count_label = f"{x} total".replace('_', ' ')
    total_name = 'lemma total'
    _df[total_name] = _df.trigger_lemma.map(_df.trigger_lemma.value_counts())
    indexers = ['polarity', 'rigger_lemma', total_name] if _df.polarity.nunique() > 1 else [
        'trigger_lemma', total_name]
    for_sty = _df.groupby(indexers).value_counts(
        [x,]).to_frame(cross_count_label)
    if cross == 'head':
        if _df[x].nunique() > 2:
            _df[x] = _df[x].map(
                {'ADJ': 'BIGRAM', 'MIR': 'TRIGGER', 'NEG': 'TRIGGER'})
        cross_name = 'dependency head'
        for_sty = for_sty.unstack().fillna(0).droplevel(
            0, axis=1).reset_index(level=total_name).sort_index(axis=1)
        # head_totals = _df.value_counts(x).to_frame(cross_count_label).T
        print(_df.value_counts(x)
              .to_frame(cross_count_label).T
              .style.background_gradient(cmap, axis=1)
              .to_latex(siunitx=True, convert_css=True).replace('_', ' '))
        for_sty = (
            for_sty  # .assign(Total=q.sum(axis=1))
            .sort_values(total_name, ascending=False)
            .convert_dtypes())
    else:
        cross_name = 'lowercase form'
        for_sty = (
            for_sty.reset_index(level=total_name)
            .sort_values([total_name, cross_count_label], ascending=False)
            # .reset_index(level=x)
            # .filter([total_name, x, cross_count_label])
            .filter([total_name, cross_count_label])
        )
    for_sty['lemma % N'] = (for_sty[total_name] / for_sty[total_name].sum()) * 100
    _sty = (for_sty.sort_index(axis=1).style
            .background_gradient(
                axis=0, cmap=cmap))
    # nb_display(_sty)
    tex_table = save_latex_table(
        sty=_sty, 
        longtable=cross=='lower',
        caption=(
            f'{dataset} {polar} Trigger Lemma Frequencies by {cross_name}'.title()),
        label=f'trig-lemma-{cross}-{dataset[:3]}-{polar[:3]}',
        verbose=True,
        latex_subdir='ch2/triggers',
        latex_stem=f'trigger_lemma-{cross}_counts_{dataset[:3]}-{polar[:3]}')


display_trigger_totals(df_super_neg)
# %%
display_trigger_totals(df_super_neg, cross='head', cmap='YlOrRd')
#%%

N_dict = {'super':  71961373,
          'mirror':  1680633}
def describe_triggers(_df):
    lemma_counts = _df.value_counts('trigger_lemma')
    form_counts = _df.value_counts('trigger_lower')
    trig_stats = lemma_counts.describe().to_frame('lemma').join(
        form_counts.describe().to_frame('lowercase form')
    ).convert_dtypes()
    trig_stats.columns.name = 'Trigger'
    trig_stats = trig_stats.rename(index={'count': 'unique'})
    trig_stats.loc['CV%'] = [(v.std()/v.mean()) * 100
                             for v in (lemma_counts, form_counts)]
    return trig_stats  # .iloc[1:, :]


# nb_display(describe_triggers(df_super_neg))
save_latex_table(
    describe_triggers(df_super_neg), default_SI=7.0,
    caption='Descriptive Statistics for Negative Superset Trigger Frequencies', 
    latex_subdir= 'ch2/freq/neg-super/', position='ht', verbose=True,
    latex_stem='neg-super-trigger-freq-descrip')

# %% [markdown]
#  Mirror Overall
# %%
# df_mirror = load_trigger_info([NEG_MIRROR_PARQ, POS_MIRROR_PARQ])
# df_mirror.describe().T.iloc[:, 1:].convert_dtypes()

# save_latex_table(
#     sty=(df_mirror.groupby(['polarity', 'trigger_lemma']).value_counts(
#         ['trigger_lower']).to_frame()
#         .style
#         .background_gradient(axis=0, cmap='purple_rain')
#         .format(precision=0, thousands=',', escape='latex')),
#     caption=(r'Mirror Subset Trigger Lemma Composition: attested forms'),
#     label='trig-lemma-vs-form-subset',
#     longtable=True,
#     latex_subdir='triggers',
#     latex_stem='mirror-trigger_lemma-form_counts')
# %%
df_mirror_neg = load_trigger_info([NEG_MIRROR_PARQ])
df_mirror_neg.describe().T.iloc[:, 1:].convert_dtypes()

# save_latex_table(
#     sty=(df_mirror_neg.groupby(['polarity', 'trigger_lemma']).value_counts(
#         ['trigger_lower']).to_frame()
#         .style
#         .background_gradient(axis=0, cmap='purple_rain')
#         .format(precision=0, thousands=',', escape='latex')),
#     caption=(r'Negative Mirror Subset Trigger Lemma Composition: attested forms'),
#     label='negmir-trig-lemma-vs-form',
#     longtable=True,
#     latex_subdir='triggers',
#     latex_stem='mirror-neg-trigger_lemma-form_counts')
# %%

save_latex_table(
    describe_triggers(df_mirror_neg), default_SI=6.0,
    caption='Descriptive Statistics for Negative Mirror Subset Trigger Frequencies', 
    latex_subdir= 'ch2/freq/neg-mirror/', position='ht', verbose=True,
    latex_stem='neg-mirror-trigger-freq-descrip')

display_trigger_totals(df_mirror_neg, dataset='mirror')
display_trigger_totals(df_mirror_neg, dataset='mirror', cross='head', cmap='YlOrRd')
# %%
df_mirror_pos = load_trigger_info([POS_MIRROR_PARQ])
df_mirror_pos.describe().T.iloc[:, 1:].convert_dtypes()

#%%
save_latex_table(
    describe_triggers(df_mirror_pos), default_SI=6.0,
    caption='Descriptive Statistics for Positive Mirror Subset Trigger Frequencies', 
    latex_subdir= 'ch2/freq/pos-mirror/', position='ht', verbose=True,
    latex_stem='pos-mirror-trigger-freq-descrip')

display_trigger_totals(df_mirror_pos, dataset='mirror', polar='positive', cmap='PuBu')
display_trigger_totals(df_mirror_pos, dataset='mirror', polar='positive',  cross='head', cmap='PuBuGn')

# save_latex_table(
#     sty=(df_mirror_pos.groupby(['polarity', 'trigger_lemma']).value_counts(
#         ['trigger_lower']).to_frame()
#         .style
#         .background_gradient(axis=0, cmap='purple_rain')
#         .format(precision=0, thousands=',', escape='latex')),
#     caption=(r'Negative Mirror Subset Trigger Lemma Composition: attested forms'),
#     label='posmir-trig-lemma-vs-form',
#     longtable=True,
#     latex_subdir='triggers',
#     latex_stem='mirror-pos-trigger_lemma-form_counts')

# %%
bare_cols = [
    'polarity', L1, L2,
    'trigger_lemma', 'adv_form_lower',
    'adj_form_lower', 'trigger_head',
    'trigger_lower', 'bigram_id'
]
all_trigger_info = pd.concat(
    [df_super_neg.filter(bare_cols),
     df_mirror.filter(bare_cols)]
).drop_duplicates('bigram_id').drop(columns=['bigram_id'])

all_trigger_info
# %%
for tdf, pol, dat in [
    (df_mirror, 'any polarity', 'mirror subset'),
    (df_mirror_neg, 'negative', 'mirror subset'),
    (df_mirror_pos, 'positive', 'mirror subset'),
    (all_trigger_info, 'any polarity', 'any triggered data')
]:
    display_trigger_totals(tdf, polar=pol, dataset=dat, cross='head')
    display_trigger_totals(tdf, polar=pol, dataset=dat)

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
am_trig_adv_posmir = calc_trigger_assoc(df_mirror_pos)
# %%
am_trig_adv_ALL = calc_trigger_assoc(all_trigger_info)
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
posmir_am_trig_adv = limit_am_df(am_trig_adv_posmir)
ALL_am_trig_adv = limit_am_df(am_trig_adv_ALL)

for view, am_df in {'NEG Superset (-)': am_trig_adv,
                    'Mirror Subset (+/-)': mir_am_trig_adv,
                    'Any Triggered (+/-)': ALL_am_trig_adv,
                    'NEG Mirror Subset (-)': negmir_am_trig_adv,
                    'POS Mirror Subset (-)': posmir_am_trig_adv,
                    }.items():
    caption = f'<b>{view}</b><br/>Trigger~Adverb Association<br/>Top LRC values'
    sty = (am_df.filter(regex=r'^[^lNe]')
           .nlargest(3000, 'f2')
           .nlargest(2000, 'f')
           .nlargest(20, 'LRC')
           .sort_index(axis=1)
           .style
           .background_gradient('PuRd'))
    save_latex_table(sty, latex_stem=f"trig-adv_AM-topLRC_{view.strip('(-/+) ').replace(' ','_')}",
                     latex_subdir='triggers', caption=caption, longtable=True,
                     label=f"trig-adv-AMtop-{view.replace(' ','')[:6]}")
    # display(set_my_style(sty))

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
# That may not be a sufficient explanation though,
# because sometimes there are _more_ tokens in the mirror subset than in the superset...
#
# ---
#
# 💡 Oh! I think the discrepancies are due to duplicate and "double-dipping" removal.
# Since different triggers were permitted, the collected bigrams and sentences will be different.
# A broader array of "other" triggers will appear for NEGmirror data,
# because any "nearer" _not_ triggers were not collected to create conflict.
# This might entail errors in trigger assignment accuracy, but it does explain how the frequencies deviate.

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


def exactly_only(_df):
    _df['l2_exactly'] = _df.l2 == 'exactly'
    exactly_df = _df.loc[_df.l2_exactly].reset_index().set_index('l1')
    exactly_df['OTHERS_f'] = exactly_df.f1 - exactly_df.f
    return exactly_df


am_trig_exactly = exactly_only(am_trig_adv)
mir_am_trig_exactly = exactly_only(am_trig_adv_mirror)
ALL_trig_exactly = exactly_only(am_trig_adv_ALL)
# set_my_style(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1'])
#              .sort_values('f1', ascending=False),
#              caption=('Trigger Frequencies<br/>'
#                       'with <i>exactly</i> vs. other adverbs')
#              ).bar(axis=0, cmap='purple_rain').relabel_index(
#     labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
#     axis=1)
# set_my_style(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1'])
#              .iloc[1:, :].sort_values('f1', ascending=False),
#              caption=('Trigger Frequencies <u>other than "<i>not</i>"</u><br/>'
#                       'with <i>exactly</i> vs. other adverbs')
#              ).bar(axis=0, cmap='purple_rain').relabel_index(
#     labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
#     axis=1)
# %%
for name, am_df in [('neg-super', am_trig_exactly),
                    ('any-mirror', mir_am_trig_exactly),
                    ('any-trigger', ALL_trig_exactly)]:
    display(save_html(set_my_style(
        (transform_counts(am_df.filter(['f', 'OTHERS_f', 'f1']))
         .sort_values('f1', ascending=False)),
        caption=('Square Root Transformed Trigger Frequencies<br/>'
                 'with <i>exactly</i> vs. other adverbs'),
        precision=1)
        .bar(axis=0, cmap='YlGnBu')
        .relabel_index(labels=['with <i>exactly</i>',
                               'with<u>out</u> <i>exactly</i>',
                               'Total'],
                       axis=1),
        subdir='triggers', stem=f'{name}-trigger-f_exactly-vs-others_bar'))

    save_latex_table(
        (transform_counts(
            am_df.filter(['f', 'OTHERS_f', 'f1']))
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
            f'cluster/triggers/{name}-trigger_x_exactly-vs-others_freq.{timestamp_today()}.tex')
    )

    save_latex_table(
        format_zeros(
            am_df
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
        caption=f'{name}: Trigger$\sim$<i>Exactly</i> Association',
        latex_path=WRITING_LINKS.joinpath(
            f'cluster/triggers/{name}-trigger-exactly_AM.{timestamp_today()}.tex')

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
    format_zeros(sty), latex_path=latex_path,
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
