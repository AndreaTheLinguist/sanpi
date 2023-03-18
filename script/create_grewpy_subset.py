# %%
"""new script to create corpora subsets using newly released version of GREW python module, `grewpy`.
   Branched from `demo/create_grewpy_subset.interactive.py` (was just `demo/create_grewpy_subset.py`)"""
import argparse
import enum
import os
from collections import namedtuple
from pathlib import Path

import pandas as pd
from grewpy import Corpus, Request
from grewpy.grew import GrewError as GrewError

# sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib
os.system("eval $(opam env)")

# *Define functions
_META_TUP = namedtuple(
    'meta_info',
    ['sent_id', 'doc_id', 'sent_int', 'sent_text', 'prev_id', 'prev_text', 'next_id', 'next_text'])

def _parse_args():

    parser = argparse.ArgumentParser(
        description=(''),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    
    parser.add_argument(
        'conllu_path',
        type=Path,
        help=('path to `.conllu` file to get subset of')
        )
    
    parser.add_argument(
        '-p', '--pat_path',
        type=Path, default='/share/compling/projects/sanpi/Pat/advadj/all-RB-JJs.pat',
        help=('path to `.pat` file for pattern to match')
    )
    
    parser.add_argument(
        '-n', '--subset_name', 
        type=str, default=None,
        help=('optional string to use as output file label for subset. '
              'If none given, `pat_path` filestem will be used. '
              'Output path template: [conllu_path parent]/subset_[label]/[label]:[conllu_path stem].{context.psv, conllu}')
    )

    args = parser.parse_args()
    return args.conllu_path, args.pat_path, args.subset_name


def dur_round(time_dur: float):
    """take float of seconds and converts to minutes if 60+, then rounds to 1 decimal if 2+ digits

    Args:
        dur (float): seconds value

    Returns:
        str: value converted and rounded with unit label of 's','m', or 'h'
    """
    unit = "s"

    if time_dur >= 60:
        time_dur = time_dur / 60
        unit = "m"

        if time_dur >= 60:
            time_dur = time_dur / 60
            unit = "h"

    if time_dur < 10:
        dur_str = f"{round(time_dur, 2):.2f}{unit}"
    else:
        dur_str = f"{round(time_dur, 1):.1f}{unit}"

    return dur_str


def corpus_from_path(path):
    return Corpus(str(path))


def grewpize_pat_path(pat_path) -> Request:
    pat_text = pat_path.read_text(encoding='utf8')
    return Request(
        ''.join(line.strip()
                for line in pat_text
                .split('{', 1)[1].split('}', 1)[0]
                .strip().splitlines()))


def parse_sent(sent_id, corpus):
    doc_id, ordinal_str = sent_id.rsplit('_', 1)
    ordinal_int = int(ordinal_str)

    row = (sent_id, doc_id, ordinal_int, corpus.get(sent_id).meta['text'])
    for context_ix in (ordinal_int + i for i in (-1, 1)):
        c_text = ''
        c_id = ''
        # > conllu doc sentence numbering starts at 1
        if context_ix > 0:
            c_id = f'{doc_id}_{context_ix}'
            try:
                c_obj = corpus.get(c_id)
            except GrewError:
                c_id = ''
            else:
                c_text = c_obj.meta['text']
        row += (c_id, c_text)

    yield _META_TUP._make(row)


def pprint_pat(request):
    print(str(request).replace(';', ';\n\t '))


def table_counts_by(corpus: Corpus, request: Request, cluster: list, total_hits):
    
    if len(cluster) == 1: 
        df = pd.Series(corpus.count(request, cluster)).to_frame().rename(
            columns={0: 'total'})
    else: 
        df = pd.json_normalize(corpus.count(request, cluster), sep='_').transpose().rename(columns={0: 'total'})
    
    df = df.assign(percent=(df.total / total_hits * 100).round(1))
    df = df.sort_values('total', ascending=False)

    return df


# > Program to Get file size in human-readable units like KB, MB, GB, TB
class sizeUnit(enum.Enum):
    # class to store the various units
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def unitConvertor(sizeInBytes, unit):
    # Cinverts the file unit
    if unit == sizeUnit.KB:
        return sizeInBytes/1024
    elif unit == sizeUnit.MB:
        return sizeInBytes/(1024*1024)
    elif unit == sizeUnit.GB:
        return sizeInBytes/(1024*1024*1024)
    else:
        return sizeInBytes


def fileSize(filePath, size_type, decimals=1):
    """File size in KB, MB and GB"""
    size = os.path.getsize(filePath)
    return round(unitConvertor(size, size_type), decimals)

#%%
def _main():
    # * Set input arguments
    conllu_path, pat_path, subset_name = _parse_args()
    print(f'# Creating `{subset_name}` subset of {conllu_path.name}: all sentences matching {pat_path.name}')
    
    # * Get corpus object from `conllu_path`
    file_size = fileSize(conllu_path, sizeUnit.MB)
    print(f'Loading corpus from `{conllu_path}` ({file_size} MB)...')
    proc_t0 = pd.Timestamp.now()
    co = corpus_from_path(conllu_path)
    proc_t1 = pd.Timestamp.now()
    print(f'\nTime to load corpus: {dur_round((proc_t1 - proc_t0).seconds)}')


    # * Describing the corpus (`co`)
    print('## Loaded (full-size) corpus info')
    counts_df = describe_corpus(conllu_path, co)
    
    # * `ADV ADJ` bigrams/collocations
    print(f'## Assessing {conllu_path.name} for {Path(*pat_path.resolve().parts[-3:])}')
    
    # > get request from pattern file
    req = Request(grewpize_pat_path(pat_path))
    print('\n```')
    pprint_pat(req)
    print('```\n')

    # > count hits for pattern and describe
    total_hits = co.count(req)
    print(f"total `ADV ADJ` bigrams in {conllu_path.name}: {total_hits}")

    # > counts by adverb lemma
    print(f"\n### {subset_name} matches in {conllu_path.name} with clustering")
    print(f"\n{subset_name} matches by ADV lemma: Top 10\n")
    print(table_counts_by(co, req, ["ADV.lemma"], total_hits).nlargest(
        10, 'total').to_markdown())

    # > counts by bigram/collocation
    print(f"\nTop 5 `ADV ADJ` bigrams in {conllu_path.name} {subset_name} matches\n")
    print(table_counts_by(co, req, ["ADV.lemma", "ADJ.lemma"],
                     total_hits).nlargest(5, 'total').to_markdown())

    # * Collect context info
    print('\n## Compiling Context Info...')
    context_info = pd.concat(pd.DataFrame(parse_sent(
        match['sent_id'], co)) for match in co.search(req))
    context_info = context_info.assign(
        conllu_id=conllu_path.stem).set_index('sent_id')

    context_info = context_info[['conllu_id', 'doc_id', 'sent_int',
                                 'prev_id', 'next_id', 'prev_text', 'sent_text', 'next_text']]
    print(f'*Total sentences in subset: **{len(context_info)}**\n                           ',
          round(len(context_info)/counts_df.at["total", "sentences"]*100, 1), 
          '% of input sentences')
    # *Save `context_info` dataframe as .psv
    subset_dir = conllu_path.parent.joinpath(f'subset_{subset_name}')
    if not subset_dir.is_dir():
        subset_dir.mkdir()

    context_path = subset_dir.joinpath(
        f'{subset_name}:{conllu_path.stem}.context.psv')
    context_info.to_csv(context_path, sep='|')
    print(f'✓  context info for {subset_name} subset of {conllu_path.name} saved as:\n'
          f'     {context_path}')

    # *Create subset conllu and save to file

    print('\n## Creating subset conllu file...')

    subset_path = subset_dir.joinpath(f'{subset_name}:{conllu_path.name}')
    subset_path.write_text('\n'.join(co.get(id).to_conll()
                        for id in context_info.index), encoding='utf8')

    print(f'✓  {subset_name} subset of {conllu_path.name} saved as:\n'
        f'     {subset_path}')

def describe_corpus(conllu_path, co):
    file_size = fileSize(conllu_path, sizeUnit.MB)
    counts_df = pd.DataFrame(index=['total'], columns=[
        'file_size', 'sentences', 'tokens', 'ADV', 'ADJ', 'NEG'])
    counts_df['file_size'] = f'{file_size} MB'
    counts_df['sentences'] = len(co)
    counts_df['tokens'] = sum(len(sent) for sent in co)

    for name, spec in (
        ('ADV', 'xpos=re"RB.*"'),
        ('ADJ', 'xpos=re"JJ.*"'),
         # TODO: add neg raising lemma node
         #  ('N-R', ()),
        ('NEG', ('lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|'
                 '"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"'))):
        req = Request(f'X[{spec}]')
        total_count = co.count(req)
        counts_df[name] = total_count

        print(f"\nTotal {name} in {conllu_path.name} by exact POS:\n")
        print(table_counts_by(co, req, ["X.xpos"], total_count).to_markdown(), '\n')

        print(f"\nTop 10 {name} lemma in {conllu_path.name}\n")
        print(table_counts_by(co, req, ["X.lemma"], total_count).nlargest(
            10, 'total').to_markdown(), '\n')

    print(f"### {conllu_path.name} overview\n")
    print(counts_df.transpose().to_markdown())
    print('\n*******************************************\n')
    return counts_df


if __name__ == '__main__':
    proc_t0 = pd.Timestamp.now()
    _main()
    proc_t1 = pd.Timestamp.now()
    print(f'\nTime to create subset: {dur_round((proc_t1 - proc_t0).seconds)}')

