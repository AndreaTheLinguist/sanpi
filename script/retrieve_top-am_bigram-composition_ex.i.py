# %%
from source.utils.am_notebooks import *
from sys import argv
from source.utils import HIT_TABLES_DIR
from source.utils.associate import TOP_AM_DIR, AM_DF_DIR

try:
    TAG = argv[1]
except IndexError:
    TAG = 'NEQ'

try:

    VERBOSE = argv[2] == '-v'
except IndexError:
    VERBOSE = False  # ! MAKE SURE THIS IS WHAT YOU WANT

# TAG = 'ALL'
K = 8
BK = max(K+2, 10)
BIGRAM_F_FLOOR = 50 if TAG == 'ALL' else 25

ADV_F_FLOOR = 5000

TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
TAG_TOP_STR = f'{TAG}-Top{K}'
TAG_TOP_DIR = TOP_AM_TAG_DIR / TAG_TOP_STR
DATE = timestamp_today()
FOCUS_ORIG = ['f', 'E11', 'unexpected_f',
              'am_p1_given2', 'am_p1_given2_simple',
              'am_p2_given1', 'am_p2_given1_simple',
              'conservative_log_ratio',
              'am_log_likelihood',
              'N', 'f1', 'f2', 'l1', 'l2']
FOCUS = adjust_am_names(FOCUS_ORIG)
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 80)


# %%
adv_am = seek_top_adv_am(date_str=DATE, adv_floor=ADV_F_FLOOR,
                         tag_top_str=TAG_TOP_STR, tag_top_dir=TAG_TOP_DIR)

# %% [markdown]
# > Loaded top adv AM table from
# > `/share/compling/projects/sanpi/results/top_AM/ALL/ALL-Top8/ALL-Top8_NEG-ADV_combined-5000.2024-08-05.csv`
#

# %%
NEG_HITS_PATH = HIT_TABLES_DIR / 'RBdirect'/'ALL-RBdirect_final.parq'
POS_HITS_PATH = HIT_TABLES_DIR / 'not-RBdirect' / \
    f'{TAG}_not-RBdirect_final.parq'

# %%
adv_list = adv_am.index.to_list()
print_iter(adv_list, header=f'## Top {K} Most Negative Adverbs', bullet='1.')

blind_am_iter = list(AM_DF_DIR.joinpath('adv_adj').rglob(
    f'AdvAdj_{TAG}*min{BIGRAM_F_FLOOR}x_extra.parq'))
if not blind_am_iter: 
    blind_am_iter = list(AM_DF_DIR.joinpath('adv_adj').rglob(
        f'AdvAdj_{TAG}*min50x_extra.parq'))
    
blam_dict = {blamp.parent.parent.name.strip(
    'ANY'): blamp for blamp in blind_am_iter}
# print(pd.Series(blam_dict)
#       .to_frame('path to "context-blind" AM scores')
#       .to_markdown(tablefmt='rounded_grid', maxcolwidths=[None, 72]))


# %% [markdown]
# ```log
# ╭────────┬──────────────────────────────────────────────────────────────────────────╮
# │        │ path to "context-blind" AM scores                                        │
# ├────────┼──────────────────────────────────────────────────────────────────────────┤
# │ mirror │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYmirror/extra/ │
# │        │ AdvAdj_ALL_any-mirror_final-freq_min50x_extra.parq                       │
# ├────────┼──────────────────────────────────────────────────────────────────────────┤
# │ direct │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYdirect/extra/ │
# │        │ AdvAdj_ALL_any-direct_final-freq_min50x_extra.parq                       │
# ╰────────┴──────────────────────────────────────────────────────────────────────────╯
# ```

# %%
def peek_am(peek_metric, blamin):
    peek = blamin.reset_index().groupby('l1').apply(
        lambda x: x.nlargest(1, peek_metric)
    ).reset_index(drop=True).set_index('key')
    print(
        f'\n_Bigrams with the highest `{peek_metric}` value for each adverb_\n')
    return peek.sort_values(peek_metric, ascending=False)


blind_priority_cols = METRIC_PRIORITY_DICT[f'{TAG}_blind']
blam_dfs = {}
for blam_kind, blam_path in blam_dict.items():
    print(
        f'\n### Loading `{blam_kind}` AM scores\n\n Path: `{blam_path.relative_to(AM_DF_DIR.parent)}`\n')
    blamin = pd.read_parquet(
        blam_path, engine='pyarrow',
        filters=[('l1', 'in', adv_list)],
        columns=FOCUS_DICT[TAG]['adv_adj'])
    blamin['dataset'] = blam_kind
    blamin = catify(adjust_am_names(blamin),
                    reverse=True)

    # for peek_metric in blind_priority_cols:
    #     nb_show_table(peek_am(peek_metric, blamin).filter(blind_priority_cols), n_dec=3)
    blamin.index = f'[_{blam_kind}_] ' + blamin.index
    blam_dfs[blam_kind] = blamin

print(f'\n * Loading hits for top adverbs in `{TAG}` selection...\n')
hits_df = load_hit_table(
    adv_set=set(adv_list),
    adv_floor=ADV_F_FLOOR, tag_top_dir=TAG_TOP_DIR,
    pos_hits=POS_HITS_PATH, neg_hits=NEG_HITS_PATH)


# %%
show_sample(hits_df
            .filter(['all_forms_lower', 'token_str']).sample(
                5).sort_values('all_forms_lower').apply(embolden,
                                                        bold_regex=r'\b((?:' + r'|'.join(adv_list) + r') \w+)\b'), format='pipe')

# %%
blam_df = pd.concat(blam_dfs.values()).sort_values(
    blind_priority_cols[0], ascending=False)

# %%

if VERBOSE:
    perspective_cols = blind_priority_cols + \
        ['dP1', 'dP2', 'f', 'f2', 'unexp_r']
    filter_blam = (blam_df.copy()
                   .filter(perspective_cols)
                   .round(2))
    perspectives = [perspective_cols[i:i+2] for i in range(0, 2)]
    perspectives.extend([['dP1', 'LRC'], ['dP2', 'LRC']])
    for ia, _adv in enumerate(adv_list[:8], start=1):
        print(f'### {ia}. Sampling _{_adv}_ context-blind bigram AMs\n')
        adv_blam = filter_blam.filter(like=f' {_adv}~', axis=0)

        for ip, col_list in enumerate(perspectives, start=1):
            print(
                f'#### {ia}.{ip}. _{_adv}_ Highest and Lowest `{col_list[0]}`\n\n(_tie-breaker: `{col_list[1]}`_)')
            x_blam = adv_blam.sort_values(col_list, ascending=False)
            nb_show_table(pd.concat([x_blam.head(3),
                                    x_blam.tail(3)]))
        print('\n---\n')

    perspect_blam = (blam_df
                     .filter(regex=r'|'.join(adv_list[:5]), axis=0)
                     .filter(perspective_cols + adjust_am_names(FOCUS_DICT[TAG]['adv_adj']))
                     .filter(regex=r'^[^laN]').iloc[:, :14]
                     .sort_values(blind_priority_cols, ascending=False))
    nb_show_table(pd.concat([perspect_blam.head(20), perspect_blam.tail(10)]))

print(timestamp_today())
for adverb in adv_am.index:
    sample_adv_bigrams(
        adverb, data_tag=TAG, verbose=True,
        amdf=blam_df, hits_df=hits_df,
        n_top_bigrams=BK, bigram_floor=BIGRAM_F_FLOOR)
