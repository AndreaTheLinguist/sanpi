# %%
import re
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, RESULT_DIR, corners
from source.utils.associate import POLAR_DIR, TOP_AM_DIR, adjust_am_names
from source.utils.sample import sample_pickle

ADV = 'exactly'
pd.set_option('float_format', '{:,.2f}'.format)
HIT_EX_COLS = ['WITH::^[bt].*lower', 'WITH::text', 'token_str']
LOAD_COLS = ['f',
             'conservative_log_ratio',
             'am_p1_given2',
             'am_p1_given2_simple',
             'am_p2_given1',
             'am_p2_given1_simple',
             'am_log_likelihood',
             'N', 'f1', 'f2',
             'E11', 'unexpected_f',
             'mutual_information', 'am_odds_ratio_disc', 't_score',
             'l1', 'l2',
             'adj', 'adj_total']
FOCUS = ['f',
         'conservative_log_ratio',
         'am_p1_given2',
         'am_p1_given2_simple',
         #  'am_p2_given1',
         #  'am_p2_given1_simple',
         'am_log_likelihood',
         #  'N', 'f1',
         #  'mutual_information', 'am_odds_ratio_disc', 't_score',
         'f2', 'E11', 'unexpected_f',
         'l1', 'l2', 'adj', 'adj_total']
abbr_FOCUS = adjust_am_names(FOCUS)


def update_index(df, pat_name: str = None):
    neg_env_name = df.filter(like='NEG', axis=0).l1[0]
    # > will be either `NEGATED` or `NEGMIR`
    #   both are shortened to just `NEG` for the keys in their separate dataframes
    # > replace to avoid ambiguity in `key` values when combined
    #! some filtering relies on 'NEG', so have to keep that prefix
    index_update = pat_name or (
        'NEGmir' if neg_env_name.endswith('MIR') else 'NEGany')
    df.index = df.index.str.replace('NEG', index_update)
    return df


def set_col_widths(df):
    cols = df.copy().reset_index().columns
    width_dict = (
        {c: None for c in cols}
        | {c: 22 for c in cols[cols.str.contains('_id')]}
        | {c: 35 for c in cols[cols.str.contains('text')]}
        | {c: 30 for c in cols[cols.str.contains('forms')]}
        | {c: 55 for c in cols[cols.str.contains('_str')]})
    return list(width_dict.values())


def embolden(strings: pd.Series,
             bold_regex: str = None,
             mono: bool = True) -> pd.Series:
    bold_regex = re.compile(bold_regex, flags=re.I) if bold_regex else REGNOT
    if mono:
        return strings.apply(lambda x: bold_regex.sub(r' __`\1`__ ', x))
    else:
        return strings.apply(lambda x: bold_regex.sub(r' __\1__ ', x))


def show_sample(df: pd.DataFrame,
                format: str = 'grid',
                n_dec: int = 0,
                limit_cols: bool = True,
                assoc: bool = False):
    _df = df.copy().convert_dtypes()
    if limit_cols and format != 'pipe' and not assoc:
        print(_df.to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=',',
            maxcolwidths=set_col_widths(_df),
            tablefmt=format
        ))
    else:
        if assoc:
            if not bool(n_dec):
                n_dec = 2
            _df = adjust_am_names(_df)

        print(_df.to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=',',
            tablefmt=format
        ))


# %%
top_neg_adv = pd.read_csv(TOP_AM_DIR.joinpath(
    f'neg_bigram_examples/{ADV}/{ADV}_10mostNEG-bigrams_AMscores_2024-05-22.csv')).set_index('key')
top_neg_adv

# %%
top_all_adv = pd.read_csv(TOP_AM_DIR.joinpath(
    f'any_bigram_examples/{ADV}/{ADV}_top11-bigrams_AMscores_2024-05-18.csv')).set_index('key')
top_all_adv

# %%


def load_polar_am(l2: str = 'bigram',
                  freq_floor: int = 100,
                  l2_filter: str = None,
                  mirror_floor: int = None) -> dict:

    def file_glob(floor: int | str):
        return f"polarized*35f-7c_min{floor}x_extra.pkl.gz"
    mirror = mirror_floor or round(freq_floor//2, -1)
    print(f'+ set_diff frequency floor set to: {freq_floor}')
    print(f'+ mirror frequency floor set to: {mirror}')
    print(f'+ `l2` filter set to: "{l2_filter}"\n')
    amdf_dict = {}
    for d in POLAR_DIR.glob(f'*/{l2}/extra'):
        pat_name = d.parent.parent.name
        print(f"+ Loading `{pat_name}`")
        floor = mirror if pat_name.endswith('mirror') else freq_floor
        try:
            pkl_path = tuple(d.glob(file_glob(floor)))[0]
        except IndexError:
            print(
                f'  * initial attempt (floor={floor}) failed. Trying again...')
            floor = round(floor + 50, -2)
            try:
                pkl_path = tuple(d.glob(file_glob(floor)))[0]
            except IndexError:
                print(
                    f'  * second attempt (floor={floor}) failed. Trying again...')
                floor = 50
                try:
                    pkl_path = tuple(d.glob(file_glob(floor)))[0]
                except IndexError:
                    print(
                        f'  * third attempt (floor={floor}) failed. Trying again...')
                    floor = '0'
                    pkl_path = tuple(d.glob(file_glob(f'*{floor}')))[0]
        print(f'  + selected path:\n    `{pkl_path.relative_to(POLAR_DIR)}`')
        amdf = pd.read_pickle(pkl_path)
        if 'key' in amdf.columns:
            amdf = amdf.set_index('key')
        if l2_filter:
            amdf = amdf.filter(like=l2_filter, axis=0)
        # if mirror < 50:
        #     amdf = amdf.loc[amdf.f2 > 25,:]
        if l2 != 'bigram':
            amdf = amdf.loc[amdf.f2 > 50, :]
        else:
            amdf = amdf.loc[amdf.f2 > 10, :]
        amdf_dict[pat_name] = update_index(
            adjust_am_names(amdf.filter(LOAD_COLS))).sort_values('dP1', ascending=False)
    return amdf_dict


# %%
polar_am_dict = {}
for key in ['adv', 'adj', 'bigram']:
    print('\n=================================')
    print(f'\n## Retrieving `{key}` AM tables\n')
    if key == 'adj':
        polar_am_dict[key] = load_polar_am(
            l2=key,
            freq_floor=50,
            mirror_floor=10)
    else:
        polar_am_dict[key] = load_polar_am(
            l2=key,
            freq_floor=50,
            mirror_floor=10 if key == 'bigram' else 50,
            l2_filter=ADV)

    for p, df in polar_am_dict[key].items():
        print(f'\n`{p}` {key.upper()}\n')
        show_sample(df.filter(abbr_FOCUS).head(5), assoc=True, format='pipe')

# %%
env_adv = pd.concat(polar_am_dict['adv'].values())
env_adv

# %%
env_adv_bigram = pd.concat(polar_am_dict['bigram'].values())
env_adv_bigram
# %%
show_sample(env_adv_bigram.filter(like='NEG', axis=0).sample(
    20).filter(abbr_FOCUS[:-4]), format='outline', assoc=True, n_dec=1)
# %%
env_adv_adj = pd.concat(polar_am_dict['adj'].values()).filter(
    regex='~'+'|~'.join(env_adv_bigram.adj.unique()),
    axis=0)
env_adv_adj

# %%


def interpret_polar_lrc(df: pd.DataFrame) -> pd.DataFrame:
    if "LRC" not in df.columns:
        df = adjust_am_names(df)
    df = df.assign(data='any',
                   polarity=df.l1.apply(
                       lambda env: 'Neg' if env.startswith('NEG') else 'Pos'),
                   signif=df.LRC.abs() > 1,
                   attract=df.LRC.round() > 0)
    df = df.assign(prone=df.signif & df.attract,
                   repel=df.signif & ~df.attract)
    df.loc[df.prone, 'outcome'] = df.loc[df.prone, 'polarity'] + 'Prone'
    df.loc[df.repel, 'outcome'] = df.loc[df.repel, 'polarity'] + 'Repel'
    df.loc[~df.signif, 'outcome'] = df.loc[~df.signif, 'polarity'] + 'Neutral'
    min_N = df.N.min()
    df.loc[df.N == min_N, 'data'] = df.loc[df.N ==
                                           min_N, 'data'].str.replace('any', 'mir')

    return df


i_env_adv = interpret_polar_lrc(env_adv)
i_env_adv

# %%
i_env_adv_bigram = interpret_polar_lrc(env_adv_bigram)
i_env_adv_bigram.groupby('polarity').value_counts(['data', 'prone', 'repel'])
# %%
i_env_adv_bigram.groupby('data').value_counts(['outcome'])
# %%
i_env_adv_adj = interpret_polar_lrc(env_adv_adj)
i_env_adv_adj.groupby(['signif', 'data']).value_counts(['outcome'])
# %%
# i_env_adv_adj.value_counts(['l2','outcome']).to_frame('signif_count').reset_index().sort_values(['signif_count','outcome'], ascending=False).groupby('signif_count').value_counts(['outcome'])
i_env_adv_adj.loc[i_env_adv_adj.signif, :].value_counts(['l2', 'outcome']).to_frame('votes').reset_index().sort_values(
    ['votes', 'outcome'], ascending=False).head(30)


# %% [markdown]
# ## _exactly sure_: full comparison
#
# 1. environment:
#    - env~adv(exactly)
#    - env~adj(sure)
#    - env~bigram(exactly_sure)
# 4. composition: adv(exactly)~adj(sure)\
#    restricted by evaluation space
#    - ALL
#    - NEG
#    - POS/COM
#

def view_results(i_am_df):
    return i_am_df.copy()[['outcome', 'LRC', 'dP1', 'dP1_simple', 'G2', 'f', 'f1', 'f2']]

# %%[markdown]
# ### env~*exactly*


results = [i_env_adv]
view_results(i_env_adv)

# %%[markdown]
# ### env~*sure*
results.append(i_env_adv_adj.filter(regex=r'sure$', axis=0))
view_results(i_env_adv_adj.filter(regex=r'sure$', axis=0))

# %%[markdown]
# ### env~*exactly_sure*

results.append(i_env_adv_bigram.filter(regex=r'sure$', axis=0))
view_results(i_env_adv_bigram.filter(regex=r'sure$', axis=0))


# %%[markdown]
# ### All 3 environment assessments combined and sorted by descending $\Delta P(\texttt{env}|\texttt{lex})$
view_results(pd.concat(results)).sort_values('dP1', ascending=False)
# %%[markdown]
# ### Composition Affinities: *exactly*~*sure*
#
# Load bigram composition association tables for different datasets

any_mir = pd.read_pickle(RESULT_DIR.joinpath('assoc_df/adv_adj/ANYmirror/extra/AdvAdj_frq-thrMIN-7.35f_min100x_extra.pkl.gz')
                         ).filter(LOAD_COLS).assign(data='mir', polarity='any')
neg_mir = pd.read_pickle(RESULT_DIR.joinpath('assoc_df/adv_adj/NEGmirror/extra/AdvAdj_frq-thrMIN-7.35f_min100x_extra.pkl.gz')
                         ).filter(LOAD_COLS).assign(data='mir', polarity='neg')
pos_mir = pd.read_pickle(RESULT_DIR.joinpath('assoc_df/adv_adj/POSmirror/extra/AdvAdj_frq-thrMIN-7.35f_min100x_extra.pkl.gz')
                         ).filter(LOAD_COLS).assign(data='mir', polarity='pos')
any_any = pd.read_pickle(RESULT_DIR.joinpath('assoc_df/adv_adj/RBXadj/extra/AdvAdj_frq-thrMIN-7.35f_min100x_extra.pkl.gz')
                         ).filter(LOAD_COLS).assign(data='any', polarity='any')
neg_any = pd.read_pickle(RESULT_DIR.joinpath('assoc_df/adv_adj/RBdirect/extra/AdvAdj_frq-thrMIN-7.35f_min100x_extra.pkl.gz')
                         ).filter(LOAD_COLS).assign(data='any', polarity='neg')
raw_comp_dfs = (any_any, any_mir, neg_any, neg_mir, pos_mir)

# %%[markdown]
# ### Compile Bigram Composition Affinities:
# _ALL Top Adjectives_ ➡️ "context-blind" or most negatively associated

assoc_adj = list(set(top_neg_adv.adj.to_list() + top_all_adv.l2.to_list()))
comp_affin = adjust_am_names(
    pd.concat([d.loc[(d.l2.isin(assoc_adj)) & (d.l1 == ADV), :]
               .reset_index()
               for d in raw_comp_dfs], ignore_index=True
              ))
# %%
comp_affin.LRC.round().reset_index().groupby('data').value_counts(['polarity', 'LRC']).reset_index(
).sort_values(['data', 'polarity', 'LRC'], ascending=False)
# %%

adjust_am_names(
    pd.concat([d.filter(like='exactly~sure', axis=0).reset_index().set_index(['key', 'polarity', 'data'])
               for d in raw_comp_dfs]))
# %%[markdown]
# ### Composition Affinities: *exactly*~*alike*
adjust_am_names(
    pd.concat([d.filter(like='exactly~alike', axis=0).reset_index().set_index(['key', 'polarity', 'data']) for d in raw_comp_dfs]))
# %%[markdown]
# ### Composition Affinities: *exactly*~*zero*
adjust_am_names(
    pd.concat([d.filter(like='exactly~zero', axis=0).reset_index().set_index(['key', 'polarity', 'data']) for d in raw_comp_dfs]))
# %%[markdown]
# ### Composition Affinities: *exactly*~*surprising*
adjust_am_names(
    pd.concat([d.filter(like='exactly~surprising', axis=0).reset_index().set_index(['key', 'polarity', 'data']) for d in raw_comp_dfs]))
# %%[markdown]
# ### Composition Affinities: *exactly*~*subtle*
adjust_am_names(
    pd.concat([d.filter(like='exactly~subtle', axis=0).reset_index().set_index(['key', 'polarity', 'data']) for d in raw_comp_dfs]))

comp_affin.dP1.round(1).reset_index().groupby(
    'data').value_counts(['polarity', 'dP1'])
# %%
comp_affin.dP2.round(1).reset_index().groupby(
    'data').value_counts(['polarity', 'dP2'])

# %%
comp_affin.xs(('exactly~sure'))
# %%
round(comp_affin.xs(('exactly~sure')).dP1.mean(), 3)

# %%


def pivot_metric(amdf,
                 metric='LRC',
                 func='mean',
                 index='key',
                 columns=['polarity']
                 ):
    piv_df = amdf.reset_index().pivot_table(
        index=index, aggfunc=func, values=metric, columns=columns
    )
    piv_df = piv_df.dropna().assign(
        diff=(piv_df[['any']].squeeze() - piv_df[['neg']].squeeze())
    ).sort_values('diff', ascending=False)
    piv_df.columns = piv_df.columns + f'_{metric}'
    return piv_df


# %%
pivot_metric(comp_affin.reset_index().set_index(
    ['data', 'polarity', 'key']).xs('any'))
# %%
superset = comp_affin.reset_index().set_index(
    ['data', 'polarity', 'key']).xs('any')
pivot_metric(superset)
# %%
pivot_metric(superset, 'dP1')
# %%
pivot_metric(superset, 'dP2')

# %%
pivot_metric(superset, 'G2')

# %%
pivot_metric(superset, 'MI')

# %%
pivot_metric(superset, metric='t')

# %%
