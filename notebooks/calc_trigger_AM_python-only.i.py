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
df_super_neg = pd.read_parquet(
    NEG_SUPER_PARQ, engine='pyarrow',
    columns=pd.Series(
        [L1, L2] +
        ['trigger_lemma', 'trigger_lower',
         'neg_head', 'neg_deprel',
         'adv_form_lower', 'adj_form_lower']
    ).drop_duplicates().to_list())
df_super_neg.info()

# %%


def rename_trigger_dep_info(df):
    if df.filter(['neg_head', 'mir_head', 'neg_deprel', 'mir_deprel']).empty:
        return df
    return df.assign(
        trigger_head=df.filter(
            ['neg_head', 'mir_head']).iloc[:, 0],
        trigger_deprel=df.filter(
            ['neg_deprel', 'mir_deprel']).iloc[:, 0],
    )
#
# df_super_neg = rename_trigger_dep_info(df_super_neg)
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

# %%


def calc_trigger_assoc(_df):
    freq_df = get_joint_f(_df).rename(columns={L1: 'l1', L2: 'l2'})
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
    display(set_my_style(_am_df.nlargest(10, 'LRC')))
    return _am_df


am_trig_adv_extra = calc_trigger_assoc(df_super_neg)
# %%
am_trig_adv = am_trig_adv_extra.filter(
    adjust_am_names(
        BASIC_FOCUS+DELTA_COLS
        + P2_COLS+FREQ_COLS)
)

display(set_my_style(am_trig_adv.nlargest(3000, 'f2').nlargest(10, 'LRC')))
# %%
am_trig_adv['l2_exactly'] = am_trig_adv.l2 == 'exactly'
am_trig_exactly = am_trig_adv.loc[am_trig_adv.l2_exactly].reset_index(
).set_index('l1')
am_trig_exactly['OTHERS_f'] = am_trig_exactly.f1 - am_trig_exactly.f
# %%
set_my_style(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1'])
             .sort_values('f1', ascending=False),
             caption=('Trigger Frequencies<br/>'
                      'with <i>exactly</i> vs. other adverbs')
             ).bar(axis=0, cmap='purple_rain').relabel_index(
    labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
    axis=1)
# %%
set_my_style(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1'])
             .iloc[1:, :].sort_values('f1', ascending=False),
             caption=('Trigger Frequencies <u>other than "<i>not</i>"</u><br/>'
                      'with <i>exactly</i> vs. other adverbs')
             ).bar(axis=0, cmap='purple_rain').relabel_index(
    labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
    axis=1)
# %%
save_html(set_my_style(
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
 subdir='triggers', stem='trigger-f_exactly-vs-others')
# %%
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
        f'cluster/trigger_x_exactly-vs-others_freq.{timestamp_today()}.tex')
)
# %%
set_my_style(transform_counts(am_trig_exactly.filter(['f', 'OTHERS_f', 'f1']))
             .iloc[1:, :].sort_values('f1', ascending=False),
             caption=('Square Root Transformed <u>Other</u> Trigger Frequencies<br/>'
                      'with <i>exactly</i> vs. other adverbs')
             ).background_gradient(axis=0, cmap='BuPu').relabel_index(
    labels=['with <i>exactly</i>', 'with<u>out</u> <i>exactly</i>', 'Total'],
    axis=1)
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

(am_trig_exactly.reset_index().rename(
    columns={'l1':'trigger lemma', 'l2':'adverb'}
    ).set_index(['trigger lemma', 'adverb']
                ).filter(['LRC', 'dP1', 'dP2', 'G2', 'unexp_r']).stack().unstack(['adverb', -1])
).style.format(precision=2, thousands=',', escape='latex').background_gradient()
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
