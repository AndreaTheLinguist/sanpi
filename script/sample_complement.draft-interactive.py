# coding=utf-8
from pathlib import Path

import pandas as pd

from source.utils.general import POST_PROC_DIR, confirm_dir

# %%
RBXadj_min7_pkl = POST_PROC_DIR.joinpath('RBXadj').glob('*MIN-7*pkl.gz')[0] #FIXME
RBdirect_min7_index = POST_PROC_DIR.joinpath('RBdirect').glob('*MIN-7*index*.txt')[0] #FIXME
neg_ids = {neg_id.strip() for neg_id in RBdirect_min7_index.read_text().splitlines()}
MIN7 = pd.read_pickle(RBXadj_min7_pkl) 
# compute complement
MIN7_not_neg = MIN7.loc[~MIN7.hit_id.isin(neg_ids), :]
# set complement paths
complement_dir = RBdirect_min7_index.parent.joinpath('complement')
confirm_dir(complement_dir)
complement_pkl= complement_dir.joinpath(f'ALL_not-neg_{RBXadj_min7_pkl.name}')
# save full complement
MIN7_not_neg.to_pickle(complement_pkl)
# pull complement sample
N = len(neg_ids)
not_neg_sample = MIN7_not_neg.sample(N)
# save complement sample
not_neg_sample.to_pickle(complement_pkl.with_name(complement_pkl.name.replace('ALL',f'SAMPLE{N}')))