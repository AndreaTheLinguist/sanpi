# %% [markdown]
# # Context-Blind AMs calculated within polar partitions
# > Additions as of: February **25**, 2025 & February **27**, 2025
from am_notebooks import *
from source.utils.associate import AM_DF_DIR
from source.utils.dataframes import enhance_descrip
from source.utils.LexicalCategories import \
    EXACTLY_RELEVANT_ADJ as ERA


# print(__name__)
try:
    print(Path(__file__).relative_to(SANPI_HOME), (icf().f_lineno), sep=':')
except NameError:
    print('notebooks/polar-partition-blindAM.py')

LEX = 'exactly'
pd.set_option("display.float_format", '{:,.2f}'.format)

BLIND_PRIORITY = METRIC_PRIORITY_DICT['ALL_blind']
# %%
# // %% [markdown]
# Columns present in context-blind extended AM tables
# i.e. `results/assoc_df/adv_adj/ANYdirect/extra/AdvAdj_*_final-freq_min*x_extra.parq`
# *will vary slightly depending on what `ALPHA` was set as when created, but for everything besides the extra LRC columns, should be*:
# ```python
# ['key', 'l1', 'l2', 'f', 'E11',
# 'am_log_likelihood', 'am_odds_ratio_disc', 'am_p1_given2', 'am_p2_given1',
# 'am_p1_given2_simple', 'am_p2_given1_simple', 'f1', 'f2', 'N',
# 'Fyy(O11)', 'Fyn(O12)', 'Fny(O21)', 'Fnn(O22)',
# 'Fy_(R1)', 'Fn_(R2)', 'F_y(C1)', 'F_n(C2)',
# 'E12', 'E21', 'E22', 't_score', 'dice', 'mutual_information',
# 'deltaP_min', 'deltaP_max', 'deltaP_abs_max', 'deltaP_mean',
# 'unexpected_f', 'unexpected_ratio', 'conservative_log_ratio',
# 'conservative_log_ratio_001', 'conservative_log_ratio_01', 'conservative_log_ratio_05',
# 'conservative_log_ratio_nc', 'conservative_log_ratio_dv',
# 'f_sqrt', 'f1_sqrt', 'f2_sqrt', 'first_char']
# ```

# // %% [markdown]
# snippet of existing table in chapter 3 markdown draft
#
# | $exactly\sim\texttt{adj}$ within $\textbf{Negative }E$ |     f |  LRC | deltaP_mean |        G2 |  dP1 |   P1 |  dP2 |   P2 | adj_total | expected_f | unexpected_f (f - expected_f) | unexpected_ratio (unexpected_f/f) |
# |:-------------------------------------------------------|------:|-----:|------------:|----------:|-----:|-----:|-----:|-----:|----------:|-----------:|------------------------------:|----------------------------------:|
# | exactly~**stellar**                                    |   170 | 4.19 |        0.14 |    770.46 | 0.28 | 0.30 | 0.00 | 0.00 |       574 |       7.92 |                        162.08 |                              0.95 |
# | exactly~**cheap**                                      |   691 | 3.56 |        0.09 |  2,324.37 | 0.16 | 0.17 | 0.01 | 0.02 |     4,040 |      55.77 |                        635.23 |                              0.92 |
# | exactly~**ideal**                                      |   417 | 3.50 |        0.09 |  1,421.26 | 0.16 | 0.18 | 0.01 | 0.01 |     2,379 |      32.84 |                        384.16 |                              0.92 |
# | exactly~**alike**                                      |   133 | 3.30 |        0.09 |    476.98 | 0.18 | 0.19 | 0.00 | 0.00 |       694 |       9.58 |                        123.42 |                              0.93 |
# %%
raw_columns = ['f', 'conservative_log_ratio', 'deltaP_mean', 'am_log_likelihood',
               'am_p1_given2', 'am_p1_given2_simple', 'am_p2_given1', 'am_p2_given1_simple',
               'f1',  # > added---not in markdown table
               'f2',  # renamed  in markdown table 'adj_total',
               'E11', 'unexpected_f', 'unexpected_ratio',
               'l2'  # > added---having adj separate is useful for frequency filtering
               ]
md_columns = adjust_am_names(raw_columns)
# %% [markdown]
# ## *Overall* Bigram Composition
# + `adv~adj` AMs based on entirety of `ANYdirect` hits, combination of `RBdirect` + `not-RBdirect`
# + _overall_ bigram subtotal $\geq 10$
full_blind = adjust_am_names(
    pd.read_parquet(
        AM_DF_DIR.joinpath(
            'adv_adj/ANYdirect/extra/AdvAdj_ALL_any-direct_final-freq_min10x_extra.parq'),
        filters=[('l1', '==', LEX)], engine='pyarrow',
        columns=raw_columns
    )).assign(polarity='ANY').convert_dtypes()
# nb_display(full_blind.nlargest(10, 'LRC').filter(
#     BLIND_PRIORITY + INVESTIGATE_COLUMN_LIST))
print(f'{full_blind.l2.nunique()} unique adjectives (where {LEX}~ADJ f >= 10)')
# %% [markdown]
# >Filter for bigram subtotal, adjectives where $f \geq \mathtt{ANY\_F\_MIN}$
ANY_F_MIN = 40
adj_fmin = full_blind.l2.astype('string')[full_blind.f >= ANY_F_MIN].to_list()

print(f'{len(adj_fmin):,} {LEX} bigrams where f >= {ANY_F_MIN}')

# # %% [markdown]
# # > loading frequencies from polar bigram AM table
# # Columns in `../results/assoc_df/polar/RBdirect/bigram/extra/*`:
# # ```csv
# # key,l1,l2,f,E11,am_log_likelihood,am_odds_ratio_disc,am_p1_given2,am_p2_given1,am_p1_given2_simple,am_p2_given1_simple,
# # f1,f2,N,Fyy(O11),Fyn(O12),Fny(O21),Fnn(O22),Fy_(R1),Fn_(R2),F_y(C1),F_n(C2),E12,E21,E22,t_score,dice,mutual_information,
# # deltaP_min,deltaP_max,deltaP_abs_max,deltaP_mean,unexpected_f,unexpected_ratio,
# # conservative_log_ratio,conservative_log_ratio_001,conservative_log_ratio_01,conservative_log_ratio_05,conservative_log_ratio_nc,conservative_log_ratio_dv,
# # f_sqrt,f1_sqrt,f2_sqrt,adv,adj,adv_total,adj_total
# # ```
# #%%
# ```python
# all_polar_bigram_freq = assign_polarity(adjust_am_names(
#     pd.read_parquet(
#         AM_DF_DIR.joinpath('polar/RBdirect/bigram/extra/polarized-bigram_ALL-direct_min1x_extra.parq'),
#         engine='pyarrow', #filters=[('adv', '==', LEX)],
#         columns=['l1','l2','f','f1','f2','N','adv','adj','adv_total','adj_total'])
#     ))
# all_polar_bigram_freq.head()
# #%%
# FULL_N = all_polar_bigram_freq.N.unique()[0]
# FULL_N
# #%%
# ENV_MARGINS = all_polar_bigram_freq[['f1','polarity']].drop_duplicates().rename(columns={'f1':'total'}).set_index(['polarity']).T.assign(any=FULL_N).T.convert_dtypes()
# # ENV_MARGINS.loc['any', 'total'] = FULL_N
# nb_display(ENV_MARGINS)
# #%%
# reconfig_all_freq = all_polar_bigram_freq.copy().rename(
#     columns={'f':'polar_bigram_f', 'f1':'polar_margin', 'f2':'bigram_margin','N':'absolute_N'})
# reconfig_all_freq
# #%%
# style_crosstab(reconfig_all_freq.loc[reconfig_all_freq.adj.isin(adj_fmin[:20])],
#                ['adj','adj_total'],
#                ['polarity','polar_margin'],
#                'polar_bigram_f', 'sum')
# #%%
# lex_polar_bigram_freq = all_polar_bigram_freq.set_index(['adv','polarity','l2','adj']).xs(LEX).filter(['f','f1','f2','adv_total','adj_total'])
# lex_polar_bigram_freq
# #%%
# lex_polar_bigram_freq.unstack(['polarity']).stack(0).unstack()
# ```

# %% [markdown]
# ## *Negative* Bigram Composition
# + __`adv~adj` AMs based only on `RBdirect` hits__
# + _negative polarity_ bigram subtotal $\geq 10$
lex_neg_compos = adjust_am_names(
    pd.read_parquet
    (AM_DF_DIR.joinpath(
        'adv_adj/RBdirect/extra/AdvAdj_ALL_RBdirect_final-freq_min10x_extra.parq'),
     filters=[('l1', '==', LEX)], engine='pyarrow',
     columns=raw_columns
     )
).assign(polarity='(-)').convert_dtypes()
# ).filter(BLIND_PRIORITY + INVESTIGATE_COLUMN_LIST).assign(polarity='(-)').convert_dtypes()
# lex_neg_compos.nlargest(5, 'f')

# #//%% [markdown]
# ### top LRC for internal composition of __negative__ bigrams
# ```py
# nb_display(lex_neg_compos.nlargest(10, 'LRC'))
# print(f'{lex_neg_compos.l2.nunique()} unique adjectives (where NEGATED {LEX}~ADJ f >= 10)')
# ```
# %%
# #//%% [markdown]
# ### top LRC of __negative__ bigrams where _overall_/_any polarity_ $f < \mathtt{ANY\_F\_MIN}$
# ```py
# nb_display(lex_neg_compos.loc[~lex_neg_compos.l2.isin(
#     adj_fmin)].nlargest(10, 'LRC'))
# caption = ('Top LRC of \\textbf{Negative} bigrams where \\textit{overall/any polarity} $f < \\mathtt{ANY\\_F\\_MIN}$\\\\'
#            f'{lex_neg_compos.loc[~lex_neg_compos.l2.isin(adj_fmin)].l2.nunique()} unique adjectives'
#            'where NEGATED \\textit{'
#            + LEX
#            + '}$\sim$\\cmtt{ADJ} $f \geq 10$\\\\'
#            + 'AND overall \\textit{'
#            + LEX
#            + '}$\\sim$\\cmtt{ADJ} ' +
#            f'$f\\geq {ANY_F_MIN}$')
# ```

# %% [markdown]
# ## *Positive* Bigram Composition
# + __`adv~adj` AMs based only on `not-RBdirect` hits__
# + _positive polarity_ bigram subtotal $\geq 10$
lex_com_compos = adjust_am_names(
    pd.read_parquet(
        AM_DF_DIR.joinpath(
            'adv_adj/not-RBdirect/extra/AdvAdj_ALL_not-RBdirect_final-freq_min10x_extra.parq'),
        filters=[('l1', '==', LEX)], engine='pyarrow',
        columns=raw_columns
    )).assign(polarity='(+)').convert_dtypes()
# )).filter(BLIND_PRIORITY + INVESTIGATE_COLUMN_LIST).assign(polarity='(+)').convert_dtypes()
# lex_com_compos.nlargest(5, 'f')
# %%
# #//%% [markdown]
# ### top LRC of __positive__ bigrams where _overall_/_any polarity_ $f < \mathtt{ANY\_F\_MIN}$
# ```py
# nb_display(lex_com_compos.loc[~lex_com_compos.l2.isin(
#     adj_fmin)].nlargest(10, 'LRC'))
# print(f'{lex_com_compos.loc[~lex_com_compos.l2.isin(adj_fmin)].l2.nunique()} unique adjectives '
#       f'where NON-NEGATED {LEX}~ADJ f >= 10)\n'
#       f'AND overall {LEX}~ADJ f < {ANY_F_MIN}')
# ```
# %% [markdown]
# ## **Save Polar Tables**


def save_polar_blind(polarity: str, lex_polar_blind_amdf: pd.DataFrame, k: int = 25,  _adj_fmin=adj_fmin):

    _fmin_blind_polar = (lex_polar_blind_amdf.loc[lex_polar_blind_amdf.l2.isin(_adj_fmin)]
                         #  .reset_index().set_index(['key', 'polarity']).stack().unstack(['polarity',-1])
                         )
    n_polar_adj_above_fmin = _fmin_blind_polar['l2'].nunique()

    # top_neg_blind = fmin_neg_blind.nlargest(50, 'LRC')
    _fmin_blind_polar.columns.name = f'{polarity} Bigram Composition'
    _fmin_blind_polar = _fmin_blind_polar.reset_index().set_index('l2')
    _fmin_blind_polar

    caption = ('Top LRC for \\textbf{'
               + polarity
               + '} bigrams where \\textit{overall/any polarity} '
               + f'$f \\geq {ANY_F_MIN}$\\\\'
               f'{n_polar_adj_above_fmin:,} unique adjectives '
               'where \\underline{'+polarity
               + '} \\textit{'
               + LEX
               + '}$\\sim$\\cmtt{ADJ} $f \\geq 10$\\\\'
               + 'AND \\overall{overall} \\textit{'
               + LEX
               + '}$\\sim$\\cmtt{ADJ} ' +
               f'$f\\geq {ANY_F_MIN}$')
    _sty = _fmin_blind_polar.nlargest(k, ['LRC', 'unexp_f']).select_dtypes(
        include='number').style.background_gradient('PuBuGn')
    save_latex_table(_sty, caption=caption, latex_subdir='exactly/blind-AM-by-polarity',
                     latex_stem=f'{polarity[:3].lower()}-exactly-blind-top{k}-lrc',
                     longtable=True, position='ht', default_SI=5.1, verbose=True, neg_color='Violet!80')


# save_polar_blind('Negative', lex_neg_compos)
# save_polar_blind('Positive', lex_com_compos )
# %%
lex_polar_compose = pd.concat(
    [pol_compose.assign(polar_key=pol_compose.index + '=' + pol_compose.polarity.str.upper(),
                        bigram=pol_compose.index.str.replace('~', '_'))
     .set_index('bigram').reset_index().set_index('polar_key')
     for pol_compose in (lex_com_compos, lex_neg_compos)]
)

# enhance_descrip(lex_polar_compose.select_dtypes(include='number'))


def front_cols(lex_df, front: list = ['polarity', 'bigram'] + BLIND_PRIORITY):
    # print(f'origin: {__file__}[{__name__}].{icf().f_code.co_name}:{icf().f_lineno}')
    # call = ist()[0]
    # print(str(call.frame))
    return lex_df.filter(front).join(lex_df.drop(columns=lex_df.filter(front).columns))


lex_polar_compose = front_cols(lex_polar_compose)
# nb_display(lex_polar_compose.sample(5).iloc[:, :5])
# %%
# for _adj in ({'sure', 'opposite', 'conducive',
#              'right', 'fair', 'equal', 'parallel',
#              'true', 'cheap', 'identical', 'alike', 'shy', 'new', 'clear', 'happy',
#              'ideal', 'zero', 'enough', 'halfway'
#              }.union(ERA)
#             ):
#     try:
#         show_example_l2(eval_sig(pd.concat([full_blind, lex_polar_compose])), example_l2=_adj,
#                         columns=['LRC', 'deltaP_mean',
#                                  'deltaP_abs_max', 'tpm_unexp_f', 'unexp_r'],
#                         transpose=True, cmap='PuBuGn',
#                         adv=LEX,
#                         index_order=['l1', 'l2', 'direction',
#                                      'polarity',
#                                      'f1', 'f2', 'f'],
#                         latex=True,
#                         latex_advsubdir='blind-AM-by-polarity/l2juxtex',
#                         call_from=':'.join([str(Path(__file__).relative_to(SANPI_HOME)),str(icf().f_lineno)])
#                         )
#     except KeyError:
#         continue
# %%
# %% [markdown]
# ### ANY polarity
# i.e. what is already discussed previously in chapter 3
nb_display(
    front_cols(full_blind.loc[full_blind.f > 50].nlargest(30, BLIND_PRIORITY),
               front=['polarity'] + BLIND_PRIORITY + ['f']))

# nb_show_table(
#     front_cols(full_blind.loc[full_blind.f > 50].nlargest(30, BLIND_PRIORITY),
#                front=['polarity'] + BLIND_PRIORITY + ['f']),
#     outpath=cobble_dated_path(
#         f'adv~adj_ANY-{LEX}_top30lrc-over50x',
#         Path(f'/share/compling/projects/sanpi/writing_assets.link/{LEX}'),
#         suffix='.md')
#     )

# %% [markdown]
# ### Negative Only
nb_display(front_cols(lex_neg_compos, ['polarity'] + BLIND_PRIORITY + ['f']
                      ).loc[lex_neg_compos.f > 50].nlargest(30, BLIND_PRIORITY))
# nb_show_table(front_cols(lex_neg_compose, ['polarity'] + BLIND_PRIORITY + ['f']
#                       ).loc[lex_neg_compose.f > 50].nlargest(30, BLIND_PRIORITY),
#            outpath=cobble_dated_path(f'adv~adj_NEG-{LEX}_top30lrc-over50x',
#                                      Path(
#                                          f'/share/compling/projects/sanpi/writing_assets.link/{LEX}'),
#                                      suffix='.md'))


# %% [markdown]
# ### Positive Only
nb_display(front_cols(lex_com_compos, ['polarity'] + BLIND_PRIORITY + ['f']
                      ).loc[lex_com_compos.f > 50].nlargest(30, BLIND_PRIORITY))
# nb_show_table(front_cols(lex_com_compose, ['polarity'] + BLIND_PRIORITY + ['f']
#                       ).loc[lex_com_compose.f > 50].nlargest(30, BLIND_PRIORITY),
#            outpath=cobble_dated_path(f'adv~adj_POS-{LEX}_top30lrc-over50x',
#                                      Path(
#                                          f'/share/compling/projects/sanpi/writing_assets.link/{LEX}'),
#                                      suffix='.md'))

# %%


def top_k_lrc_blind_each(polar_compos_df, k=20):
    return pd.concat(pam.nlargest(k, 'LRC')
                     for pol, pam in polar_compos_df.groupby('polarity'))


PROB = ['dP1', 'P1'] + adjust_am_names(P2_COLS + DELTA_COLS)
_lrc_blind_each = top_k_lrc_blind_each(lex_polar_compose, k=100).sort_values(
    'LRC', ascending=False)
_lrc_blind_each.set_index(['polarity', 'bigram']).unstack('polarity')
# %%
top_k_lrc_blind_each(lex_polar_compose, k=40).sort_values(
    'LRC', ascending=False)


# %%
# full30 = full_blind.assign(bigram=full_blind.l1.astype('string')+'_'+ full_blind.l2.astype('string')
#                           ).nlargest(30, 'LRC').set_index('bigram').LRC.to_frame('LRC_full')
full30_f_over_min = full_blind.loc[full_blind.l2.isin(adj_fmin)].nlargest(
    30, 'LRC').LRC.to_frame('LRC_full')


neg30_f_over_min = lex_neg_compos.loc[lex_neg_compos.l2.isin(adj_fmin)].nlargest(
    30, 'LRC').LRC.to_frame('LRC_neg')

pos30_f_over_min = lex_com_compos.loc[lex_com_compos.l2.isin(adj_fmin)].nlargest(
    30, 'LRC').LRC.to_frame('LRC_pos')

full_join = full30_f_over_min.join(neg30_f_over_min).join(pos30_f_over_min)
nb_display(full_join.style.set_caption(
    '<u>Any/Either</u> Polarity Top Blind <i>exactly</i> AM (ALL+ Superset)'))

neg_join = neg30_f_over_min.join(full30_f_over_min).join(pos30_f_over_min)
nb_display(neg_join.style.set_caption(
    '<u>Negative</u> Polarity Top Blind <i>exactly</i> AM (ALL+ Superset)'))

pos_join = pos30_f_over_min.join(full30_f_over_min).join(neg30_f_over_min)
nb_display(pos_join.style.set_caption(
    '<u>Positive</u> Polarity Top Blind <i>exactly</i> AM (ALL+ Superset)'))
# %%
nb_display(format_zeros(
    (pd.concat([full_join, neg_join, pos_join])
     .drop_duplicates()[['LRC_neg', 'LRC_full', 'LRC_pos']]
     .sort_values(['LRC_full', 'LRC_neg'], ascending=False)
     # .fillna(0).convert_dtypes()
     .style.background_gradient('PuBuGn', axis=None)),
    grey_out=True
))

# %%
pol_order = ['(-)', 'ANY', '(+)']
juxta_blind_lrc = pd.concat([bdf[bdf.l2.isin(adj_fmin)].set_index(['l2', 'polarity']).filter(['LRC'])
                             for bdf in (lex_neg_compos, lex_com_compos, full_blind)
                             ]).unstack().droplevel(0, axis=1).filter(pol_order)
juxta_blind_lrc.columns.name = 'Polar LRC'
top_juxta_merge = pd.concat(
    [juxta_blind_lrc.nlargest(
        15, [p, ('(-)' if p == 'ANY'
             else 'ANY')]) for p in pol_order]
).drop_duplicates().sort_values('ANY', ascending=False)

save_latex_table(
    top_juxta_merge.style.background_gradient('PuBuGn', axis=None),
    latex_subdir='exactly/blind-AM-by-polarity',
    caption="``Blind'' LRC for <i>Exactly *</i> Across Polarity Partions",
    latex_stem='juxta-exactly-LRC-top15ea',
    neg_color="Mulberry", verbose=True,
    call_comment=f"% {':'.join([str(Path(__file__).relative_to(SANPI_HOME)),str(icf().f_lineno)])}"
)
# %% [markdown]
# ## Calculate LRC for combinations where $f<10$
# ### Load Frequency TSVs
all_pos_f = pd.read_csv(
    SANPI_HOME.joinpath(
        'results/freq_tsv/RBdirect/AdvAdj_ALL_not-RBdirect_final-freq.tsv'),
    sep='\t', names=['f', 'l1', 'l2'], engine='pyarrow', keep_default_na=False
).convert_dtypes()
all_neg_f = pd.read_csv(
    SANPI_HOME.joinpath(
        'results/freq_tsv/RBdirect/AdvAdj_ALL_RBdirect_final-freq.tsv'),
    sep='\t', names=['f', 'l1', 'l2'], engine='pyarrow', keep_default_na=False
).convert_dtypes()
# %%
# all_pos_f.info(memory_usage='deep')
# all_pos_f.memory_usage('deep')

# #%%
# l1_union = set(all_pos_f.l1.unique()).union(set(all_neg_f.l1.unique()))
# l2_union = set(all_pos_f.l2).union(all_neg_f.l2)
# #%%
# all_pos_f['l1'] = pd.Categorical(all_pos_f.l1, categories=l1_union)
# all_pos_f['l2'] = pd.Categorical(all_pos_f.l2, categories=l2_union)
# #%%
# all_pos_f.info(memory_usage='deep')
# all_pos_f.memory_usage('deep')
# #%%
# all_neg_f['l1'] = pd.Categorical(all_neg_f.l1, categories=l1_union)
# all_neg_f['l2'] = pd.Categorical(all_neg_f.l2, categories=l2_union)
# #%%
# all_neg_f.info(memory_usage='deep')
# all_neg_f.memory_usage('deep')

adj_top = top_juxta_merge.index.to_list()
# %%


def fill_missing_lrc(l2_selection, all_f_df):
    top_fsig = pd.DataFrame(index=l2_selection,
                            columns=['f', 'f1', 'f2', 'N'])
    top_fsig.update(all_f_df.loc[(all_f_df.l2.isin(l2_selection))
                                 & (all_f_df.l1 == LEX), ['f', 'l2']].set_index('l2'))
    top_fsig['f'] = top_fsig.f.fillna(0)
    top_fsig['f2'] = all_f_df[['f', 'l2']].groupby(
        'l2').sum().filter(l2_selection, axis=0)
    top_fsig = top_fsig.assign(N=all_f_df.f.sum(),
                               f1=all_f_df.loc[all_f_df.l1 == LEX, 'f'].sum())
    print(top_fsig.head(8).to_markdown(floatfmt=',.2f', tablefmt='plain'))
    # nb_display(top_fsig)
    return am_ms.conservative_log_ratio(am_fq.expected_frequencies(top_fsig, observed=True).astype('int64'))


all_pos_lrc = fill_missing_lrc(sorted(set(adj_top+ERA)), all_pos_f).to_frame('POS')
# %%
all_neg_lrc = fill_missing_lrc(sorted(set(adj_top+ERA)), all_neg_f).to_frame('NEG')
top_juxta_filled = pd.concat(
    [all_neg_lrc.T, 
     (full_blind.set_index('l2')[['LRC']]
      .rename(columns={'LRC':'ANY'})
      .T.filter(adj_top+ERA)), 
     all_pos_lrc.T]).T.sort_values(['ANY','NEG','POS'], ascending=False)
# %%
save_latex_table(
    top_juxta_filled.style.background_gradient('PuBuGn', axis=None),
    latex_subdir='exactly/blind-AM-by-polarity',
    caption="``Blind'' LRC for <i>Exactly *</i> Across Polarity Partions",
    latex_stem='juxta-exactly-LRC-top15ea-nafill-PLUSexactly-relevant',
    neg_color="Mulberry", verbose=True,
    call_comment=f"% {':'.join([str(Path(__file__).relative_to(SANPI_HOME)),str(icf().f_lineno)])}"
)
# top_f_fill = full_blind.loc[
#     full_blind.l2.isin(top_juxta_merge.index), ['f','l2']].set_index('l2').join(
#         all_pos_f.set_index('l1').xs(LEX).set_index('l2').filter(top_juxta_merge.index,axis=0),
#         lsuffix='_any', rsuffix='_pos')
# top_f_fill = top_f_fill.join(
#         all_neg_f.set_index('l1').xs(LEX).set_index('l2').add_suffix('_neg').filter(top_juxta_merge.index,axis=0))
# top_f_fill = top_f_fill.fillna(0)
# top_f_fill
# %% [markdown]
# ### 💡 "blind" LRC for `polarity~alike` within the "*exactly* corpus"
am_ms.conservative_log_ratio(
    am_fq.expected_frequencies(
        pd.DataFrame(columns='f,f1,f2,N'.split(','),
                     index=['POS~alike', 'NEG~alike'],
                     data=[[643, 12296, 776, 56109],
                           [133, 43813, 776, 56109]]),
        observed=True))


def get_lrc_from_fsig(fsig_df):
    return am_ms.conservative_log_ratio(
        am_fq.expected_frequencies(fsig_df,
                                   observed=True))


# %% [markdown]
# > Current LRC for ALL+ Super Negated `exactly_alike` is $1.39$
# %%
all_exactly_f = pd.pivot_table(pd.concat(
    (all_neg_f.loc[all_neg_f.l1 == LEX, :].assign(l1='neg'),
     all_pos_f.loc[all_pos_f.l1 == LEX, :].assign(l1='pos')),
    ignore_index=True),
    index='l2', columns='l1', fill_value=0
).stack().astype('int64').reset_index()
all_exactly_f.columns.name = LEX
all_exactly_f
# %%
all_exactly_fsig = pd.DataFrame(
    columns=['l1', 'l2', 'f', 'f1', 'f2', 'N'], index=all_exactly_f.index)
all_exactly_fsig.update(all_exactly_f)
# %%
f1_dict = all_exactly_fsig[['f', 'l1']].groupby('l1').sum().squeeze().to_dict()
f2_dict = all_exactly_fsig[['f', 'l2']].groupby('l2').sum().squeeze().to_dict()
all_exactly_fsig['f1'] = all_exactly_fsig.l1.map(f1_dict)
all_exactly_fsig['f2'] = all_exactly_fsig.l2.map(f2_dict)
all_exactly_fsig = all_exactly_fsig.assign(N=all_exactly_f.f.sum())
all_exactly_fsig

# %%
exactly_split_lrc = get_lrc_from_fsig(all_exactly_fsig.set_index(
    ['l2', 'l1']).astype('int64')).to_frame('LRC').unstack()
exactly_split_lrc.columns.name = 'exactly LRC'
exactly_split_lrc = exactly_split_lrc.droplevel(0, axis=1)
nb_display(exactly_split_lrc.nlargest(
    15, 'neg').style.background_gradient('BrBG', axis=None))
# %%
save_latex_table(top_juxta_filled.join(
    exactly_split_lrc.add_suffix('_exactly_subset').filter(
        top_juxta_filled.index, axis=0)
).style.background_gradient('lilac_rose', axis=None),
    latex_subdir='exactly/blind-AM-by-polarity',
    caption="``Blind'' LRC for <i>Exactly *</i> Across Polarity Partions <b>PLUS ``<i>exactly</i> corpus'' calculated LRC",
    latex_stem='juxta-exactly-LRC-top15ea-ERA-PLUS-exactly-corp-calc',
    neg_color="Orange", verbose=True,
    call_comment=f"% {':'.join([str(Path(__file__).relative_to(SANPI_HOME)),str(icf().f_lineno)])}")

# %% [markdown]
# ## Unrestricted, Polar_exactly~ADJ
# For each comparison space (i.e. frequency perspective and polarity approximation combination) there are the following "windows" or "facets" for examination for any given "triple".
# Using `(neg, exactly, alike)` as an example:
#
# ### A. within full `N`
#
# *already calculated/discussed*
# 1. ✔️<font color=SpringGreen>neg~exactly</font>
# 2. ✔️<font color=SpringGreen>neg~alike</font>
# 3. ✔️<font color=SpringGreen>neg~exactly_alike</font>
# 4. ✔️<font color=SpringGreen>exactly~alike</font>
#
# *not explored*
#
# 5. ❓ <font color=Orange>neg_exactly~alike</font>
# 6. ~~neg_alike~exactly~~
#
# ### B. within a proper subset `N`; i.e. examination area restricted to...
#
# 1. <u>just *exactly*</u> -- meaning `N` = *exactly* marginal frequency from above cases
#    - [ ] ⏳**<font color=violet>neg~alike</font>** ➡️ calculated last night (Feb 1. See note [calculate blind LRC for ENV~ADJ for only "exactly" hits](https://ticktick.com/webapp/#p/ece24b5f8b263a75a9da014b/tasks/67c14fe37b5edd00000003ce))
#               *but not discussed!*
# 2. <u>just **neg**</u> -- i.e. `N` = **neg** marginal frequency from above
#    - [ ] ⏳<font color=DodgerBlue>**exactly~alike**</font> ➡️ calculated in same notebook as above note: *`notebooks/polar-partition-blindAM.py`*
#             *discussion initiated, but not complete*
# 3. ~~just *alike* -- `N` = *alike* marginal frequency~~\
#    ~~**neg~exactly**~~ :  don't think restricting by adjective is well-motivated for examination of an adverb, but would be more relevant if the object of inquiry were an adjective/set of adjectives instead
# ---
# So,
# + A1-A4 are already examined ✔️ (full N: `polar~exactly`, `polar~adj`, `polar~bigram=exactly_adj`, blind `exactly~adj`)
# + ⏳ B1 and B2 have been calculated but not really examined closely or discussed fully:
#     + (polar N: `exactly~adj` & *exactly* N: `polar~adj`)
# + A6 and B3 seem less relevant given a focus on the <u>adverb</u> *exactly*
#     + (full N: `polar_adj~exactly` & ADJ N: `polar~exactly`)
# + A5 (full N: `ENV_exactly~ADJ`) could be relevant, but I'm not certain it will be any more informative than the others.
#     + ❔ How does A5 differ from B1?
#             + A5: **full N**: `polar_exactly~alike`
#             + B1: ***exactly* N**: `neg~alike`
#         + <u>`f` would be the same</u>: `neg & exactly & ADJ` is constant (for the comparison space)
#         + <u>`f1`  would be the same</u>
#             + A5 `f1` is the `f` from A1 (env~adv)-- out of all tokens, how many are negated & have *exactly*
#             + B1 `f1` is the same number: out of the *exactly* tokens, how many are negated.
#         + <font color=Tomato>`f2` would differ</font>
#             + A5 `f2` is the `f` from A2 (env~adj)--out of all tokens, how many have *alike*
#             + B1 `f2` is the `f` from A4 (blind): out of the *exactly* tokens, how many have *alike*?
#         + <font color=Tomato>`N` would differ</font>
#             + A5 `N` = **total** total
#             + B1 `N` = *exactly* total

# %%
polar_adv_fsig = pd.concat([
    all_neg_f.assign(l1='NEG_' + all_neg_f.l1, adv=all_neg_f.l1),
    all_pos_f.assign(l1='POS_' + all_pos_f.l1, adv=all_pos_f.l1)
])
# %%
_f1_mapper = polar_adv_fsig[['f', 'l1']].groupby('l1').sum().squeeze()
polar_adv_fsig['f1'] = polar_adv_fsig.l1.map(_f1_mapper)
_f2_mapper = polar_adv_fsig[['f', 'l2']].groupby('l2').sum().squeeze()
polar_adv_fsig['f2'] = polar_adv_fsig.l2.map(_f2_mapper)
polar_adv_fsig = polar_adv_fsig.assign(N=polar_adv_fsig.f.sum()).convert_dtypes()
polar_adv_fsig
# %%
polar_lex_fsig = pd.DataFrame(columns=['f', 'f1', 'f2', 'N'])
polar_lex_fsig['f'] = pd.pivot_table(
    polar_adv_fsig.reset_index().set_index(['adv', 'index']).xs(LEX),
    values='f', index='l1', columns='l2', fill_value=0).stack().astype('int64')
polar_lex_fsig = polar_lex_fsig.reset_index().assign(
    N=polar_adv_fsig.N.iloc[0])
polar_lex_fsig['f1'] = polar_lex_fsig.l1.map(_f1_mapper)
polar_lex_fsig['f2'] = polar_lex_fsig.l2.map(_f2_mapper)
polar_lex_fsig.sort_values(['f2','l2'], ascending=False)
#%%
polar_lex_fsig = polar_lex_fsig.set_index(['l1', 'l2'])
polar_lex_fsig['LRC'] = get_lrc_from_fsig(polar_lex_fsig.select_dtypes(include='number').astype('int64'))
# %%
nb_display(polar_lex_fsig.nlargest(15, 'LRC').style.background_gradient(axis=None, subset='LRC'))

rotate = polar_lex_fsig.loc[polar_lex_fsig.f2>=200].reset_index().set_index(
    ['N', 'l1', 'f1','l2', 'f2']).unstack(['N','l1','f1'])
nb_display(rotate.nlargest(15, rotate.filter(like='NEG_').columns)
           .style
           .background_gradient(axis=None, subset='LRC')
           .background_gradient('purple_rain', axis=None, subset='f')
           )

# %%
nb_display(rotate.reset_index(level='f2').filter(adj_top+ERA, axis=0)
           .style
           .background_gradient(axis=None, subset='LRC')
           .background_gradient('purple_rain', axis=None, subset='f'))
rotate_trim = rotate.filter(like='LRC').droplevel(0, axis=1).droplevel(('N','f1'),axis=1).droplevel('f2', axis=0)
# %%
save_latex_table(
    (top_juxta_filled
     .join(
    rotate_trim.add_suffix('PolarL1').filter(
        top_juxta_filled.index, axis=0))
     .join(
    exactly_split_lrc.add_suffix('_exactly_subset').filter(
        top_juxta_filled.index, axis=0))
    .style.background_gradient('lilac_rose', axis=None)),
    latex_subdir='exactly/blind-AM-by-polarity',
    caption="``Blind'' LRC for <i>Exactly *</i> Across Polarity Partions <b>PLUS ``<i>exactly</i> corpus'' calculated LRC",
    latex_stem='juxta-exactly-LRC-top15ea-ERA-PLUS-exactly-corp-calc-PLUS-polarExactlyL1',
    neg_color="Orange", verbose=True,
    call_comment=f"% {':'.join([str(Path(__file__).relative_to(SANPI_HOME)),str(icf().f_lineno)])}")
# %%
