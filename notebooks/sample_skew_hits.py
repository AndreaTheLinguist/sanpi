# %%
#
from utils import sample_pickle
import pandas as pd
from pathlib import Path
_SANPI_DIR = Path('/share/compling/projects/sanpi')

skew_path = _SANPI_DIR.joinpath('results/ucs_tables/dataframes/polarized-bigram_MIRROR.35f-868thresh_min15x.SKEW_extra.csv')

if not skew_path.is_file(): 
    raise FileNotFoundError
# %%
sk = (pd.read_csv(skew_path) if skew_path.suffix == '.csv' 
      else pd.read_pickle(skew_path))

sk.head(3)
# %%

print('Minimum adjusted conditional probability of polarity environment:', round(sk.am_p1_given2.abs().min(), 3))
sk.head().key
# %%
parts = sk.key.str.split('-', expand=True).loc[:, :1].rename(columns={0:'pol', 1:'bigram'})
parts


#%%
data_paths = parts.pol.apply(lambda p: Path(f'/share/compling/data/sanpi/4_post-processed/{p}mirror/'))
data_paths
    # sample_pickle(data_path=Path('/share/compling/data/sanpi/4_post-processed/{pol}mirror/'))





# %%
