# %%
import pandas as pd
from pathlib import Path
import json
from pprint import pprint

# > RUN `puddin`
# _DATA_DIR=Path('/share/compling/data/puddin')

# > RUN `news`
_DATA_DIR = Path('/share/compling/data/news')

input_paths = tuple(_DATA_DIR.glob('*conll/info/*counts.json'))

FILE_CAP = 0
# %%
count_dfs_dict = {}
conllu_id_list = []
read_paths = input_paths[:FILE_CAP] if FILE_CAP > 0 else input_paths
for json_path in read_paths:

    # if already added, skip.
    # 🪲 not sure where the path duplication is coming from... perhaps the different softlinked directories?
    conllu_id = json_path.name.split('.', 1)[0]
    if conllu_id in conllu_id_list:
        print('warning! duplicate entry for', conllu_id)
        continue
    conllu_id_list.append(conllu_id)

    with json_path.open(mode='r') as count_json:
        cj = json.load(count_json)
    totals = pd.Series(cj.pop('total')).to_frame().rename(
        columns={0: conllu_id}).transpose()
    # print(totals.to_markdown())
    if 'total' in count_dfs_dict.keys():
        count_dfs_dict['total'] = count_dfs_dict['total'] + [totals]
    else:
        count_dfs_dict['total'] = [totals]

    for node_name in cj.keys():
        cj0 = cj[node_name]
        for descriptor in cj0.keys():
            table_name = f'{node_name}{descriptor}'.replace('by', '')
            count_df = pd.DataFrame.from_dict(cj0[descriptor]).rename(
                index={'total': conllu_id}).loc[[conllu_id], :]
            if table_name not in count_dfs_dict.keys():
                count_dfs_dict[table_name] = [count_df]
            else:
                count_dfs_dict[table_name] = count_dfs_dict[table_name] + [count_df]


# %%
combined_counts = {}
for label, frames in count_dfs_dict.items():
    # print(f'\nCounts: *{label}*')

    combined = pd.concat(frames).fillna(0).convert_dtypes()
    combined.loc['ALL_FILES', :] = combined.sum()
    combined_counts[label] = combined.round(0).astype('int')
    # print(combined_counts[label].convert_dtypes())

all_counts = {k: df.loc['ALL_FILES', :].to_dict()
              for k, df in combined_counts.items()}
all_counts['FILE_CAP'] = FILE_CAP

out_file = _DATA_DIR.joinpath(f'info/full_total_counts.json')
if FILE_CAP > 0:
    out_file = out_file.with_suffix(f'.sample{FILE_CAP}.json')

if not out_file.parent.is_dir():
    out_file.parent.mkdir(parents=True)
out_file.write_text(json.dumps(all_counts, indent=4), encoding='utf8')
