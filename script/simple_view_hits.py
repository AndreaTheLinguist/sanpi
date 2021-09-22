"""saves a simplified version (select columns only) of the hits table 
    to a csv file with name '[label]_simplified.csv' to the parent directory of the original file. 

    Arguments are: [csv path], [name of pat version (for labeling)]
    """
import pandas as pd
from sys import argv
from pathlib import Path

# arguments are: [csv path], [name of pat version]
source = Path(argv[1])
label = argv[2]


def simplify(source, label):

    df = pd.read_csv(source)
    word_info = [c for c in df.columns
                 if c.endswith(('dep', 'word', 'deplabel'))]
    added_col = [c for c in df.columns
                 if c in ['sent_id', 'sent_text', 'window_text', 'colloc']]
    df = df[word_info + added_col]
    df = df.assign(pat_version=label).sort_values(
        ['sent_text', 'sent_id', 'colloc'])

    df = df[~df.duplicated(word_info.append('sent_text'))]

    pd.set_option('display.max_colwidth', 80)

    sample = df[['colloc', 'sent_text']].sample(min(5, len(df)))
    print(sample)

    outpath = source.parent.joinpath(f'{label}_simplified.csv')
    df.to_csv(outpath)
    print('...\n-> simplified viewing csv saved to', outpath)


simplify(source, label)
