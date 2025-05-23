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


def _main():
    # * Set input arguments
    conllu_path, pat_path, subset_name = _parse_args()
    print(f'# Creating `{subset_name}` subset of `{conllu_path.name}`:',
          f'all sentences matching `{pat_path.name}`')

    # * Get corpus object from `conllu_path`
    file_size = fileSize(conllu_path, sizeUnit.MB)
    print(f'Loading corpus from `{conllu_path}` ({file_size} MB)...')
    proc_t0 = pd.Timestamp.now()
    co = corpus_from_path(conllu_path)
    proc_t1 = pd.Timestamp.now()
    time_str = get_time_str(proc_t0, proc_t1)
    print(f'\nTime to load corpus: {time_str}')

    # * Describing the corpus (`co`)
    print('## Loaded (full-size) corpus info')
    counts_df = describe_corpus(conllu_path, co)

    # * `ADV ADJ` bigrams/collocations
    print(f'## Assessing `{conllu_path.name}` for',
          f'`{Path(*pat_path.resolve().parts[-3:])}`')

    # > create output directory and shared stem for output files
    subset_dir = conllu_path.parent.joinpath(f'subset_{subset_name}')
    if not subset_dir.is_dir():
        subset_dir.mkdir()
    out_stem = f"{(subset_name).upper()}.{conllu_path.stem}"
    print(f'stem for output files: `{out_stem}`')

    # > get request from pattern file
    req = Request(grewpize_pat_path(pat_path))
    print('\n```')
    pprint_pat(req)
    print('```\n')

    # > count hits for pattern and describe
    show_req_counts(co, req, conllu_path, subset_name)

    # * Get Matchings
    print('\n## Collecting pattern matchings...')
    proc_t0 = pd.Timestamp.now()
    match_by_sent = co.search(req, flat="matchings")
    proc_t1 = pd.Timestamp.now()
    print(f'+ Time to create matchings: `{get_time_str(proc_t0, proc_t1)}`')

    # * Collect context info
    print('\n## Compiling Context Info...')
    proc_t0 = pd.Timestamp.now()
    context_info = build_context(co, match_by_sent.keys(), conllu_path)
    proc_t1 = pd.Timestamp.now()
    time_str = get_time_str(proc_t0, proc_t1)
    print(f'+ Time to build context dataframe: {time_str}')

    subset_sent_total = len(match_by_sent)
    print('+ Subset Size:\n',
          f'  + number of sentences: {subset_sent_total}\n',
          f'  + {round(subset_sent_total / counts_df.at["total", "sentences"]*100, 1)}%',
          'of input sentences')

    # *Save `context_info` dataframe as .psv
    context_path = subset_dir.joinpath(
        f'{out_stem}.context.psv')
    _t0 = pd.Timestamp.now()
    context_info.to_csv(context_path, sep='|')
    _t1 = pd.Timestamp.now()
    time_str = get_time_str(_t0, _t1)

    print(f'\n✓  context info for `{subset_name}` subset of',
          f'`{conllu_path.name}` saved as:\n',
          f'> `{context_path.relative_to(conllu_path.parent)}`')
    print('+ Time to save context info as file:',  time_str)

    # *Create subset conllu and save to file
    print('\n## Creating subset conllu file...')
    sub_conllu_path = subset_dir.joinpath(f'{out_stem}.conllu')

    proc_t0 = pd.Timestamp.now()
    create_subset_conllu(match_by_sent,
                         sub_conllu_path)
    proc_t1 = pd.Timestamp.now()
    time_str = get_time_str(proc_t0, proc_t1)

    print(f'\n✓  `{subset_name}` subset of `{conllu_path.name}` saved as:\n'
          f'  > `{sub_conllu_path.resolve().relative_to(conllu_path.parent)}`')
    print(f'+ Total time to create conllu output: `{time_str}`')


def show_req_counts(corpus: Corpus,
                    req: Request,
                    conllu_path: Path,
                    subset_name: str) -> None:

    total_hits = corpus.count(req)
    print(f"total `{subset_name}` matches in {conllu_path.name}: {total_hits}")

    # > counts by adverb lemma
    print(f"\n### `{subset_name}` matches in",
          f"`{conllu_path.name}` with clustering")
    print(f"\n`{subset_name}` matches by ADV lemma: Top 10\n")
    print(table_counts_by(corpus, req, ["ADV.lemma"], total_hits).nlargest(
        10, 'total').to_markdown())

    # > counts by bigram/collocation
    print(f"\nTop 5 `{subset_name}` matches in `{conllu_path.name}`\n")
    print(table_counts_by(corpus, req, ["ADV.lemma", "ADJ.lemma"],
                          total_hits).nlargest(5, 'total').to_markdown())


def create_subset_conllu(
        match_by_sent: dict,
        sub_conllu_path: Path) -> None:

    _t0s = pd.Timestamp.now()
    conllu_output = '\n'.join(
        s[0].graph.to_conll()
        for s
        in match_by_sent.values())
    _t1s = pd.Timestamp.now()
    time_str = get_time_str(_t0s, _t1s)
    print(f'+ Time to create conllu string: `{time_str}`')

    # print(f'\n### First sentence in `{sub_conllu_path.name}`',
    #       ('> ```{conllu}\n'
    #        + conllu_output.split('\n\n', 1)[0] + '\n```'
    #        ).replace('\n', '\n> '),
    #       sep='\n')

    _t0w = pd.Timestamp.now()
    sub_conllu_path.write_text(conllu_output, encoding='utf8')
    _t1w = pd.Timestamp.now()
    time_str = get_time_str(_t0w, _t1w)
    print(f'+ Time to save `{sub_conllu_path.name}`: `{time_str}`')


def build_context(corpus: Corpus,
                  sent_ids,
                  conllu_path: Path) -> pd.DataFrame:
    sent_ids = pd.Series(sent_ids).unique()
    context_info = pd.concat(pd.DataFrame(parse_sent(sid, corpus))
                             for sid in sent_ids)

    context_info = context_info.assign(
        conllu_id=conllu_path.stem).set_index('sent_id')

    context_info = context_info[['conllu_id', 'doc_id', 'sent_int',
                                 'prev_id', 'next_id', 'prev_text', 'sent_text', 'next_text']]
    return context_info


def parse_sent(sent_id: str, corpus: Corpus) -> _META_TUP:

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


def corpus_from_path(path):
    return Corpus(str(path))


def grewpize_pat_path(pat_path) -> Request:
    pat_text = pat_path.read_text(encoding='utf8')
    return Request(
        ''.join(line.strip()
                for line in pat_text
                .split('{', 1)[1].split('}', 1)[0]
                .strip().splitlines()))


def pprint_pat(request):
    print(str(request).replace(';', ';\n\t '))


def table_counts_by(corpus: Corpus, request: Request, cluster: list, total_hits):

    if len(cluster) == 1:
        df = pd.Series(corpus.count(request, cluster)).to_frame().rename(
            columns={0: 'total'})
    else:
        df = (pd.json_normalize(corpus.count(request, cluster), sep='_')
              .transpose().rename(columns={0: 'total'}))

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
    # Converts the file unit
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


def describe_corpus(conllu_path, co):
    file_size = fileSize(conllu_path, sizeUnit.MB)
    counts_df = pd.DataFrame(
        index=['total'],
        columns=['file_size', 'sentences', 'tokens', 'ADV', 'ADJ', 'NEG'])
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

        print(f"\nTotal {name} in `{conllu_path.name}` by exact POS:\n")
        print(table_counts_by(co, req, ["X.xpos"],
              total_count).to_markdown(), '\n')

        print(f"\nTop 10 {name} lemma in `{conllu_path.name}`\n")
        print(table_counts_by(co, req, ["X.lemma"], total_count).nlargest(
            10, 'total').to_markdown(), '\n')

    print(f"### `{conllu_path.name}` overview\n")
    print(counts_df.transpose().to_markdown())
    print('\n*******************************************\n')
    return counts_df


def get_time_str(start: pd.Timestamp,
                 finish: pd.Timestamp) -> str:
    t_comp = (finish - start).components
    time_str = (
        ":".join(str(c).zfill(2)
                 for c
                 in (t_comp.hours, t_comp.minutes, t_comp.seconds))
        + f'.{round(t_comp.microseconds, 1)}')

    return time_str


if __name__ == '__main__':
    _t0 = pd.Timestamp.now()
    _main()
    _t1 = pd.Timestamp.now()
    time_str = get_time_str(_t0, _t1)
    print(
        f'\n## Subset creation complete!✨ \nTotal time elapsed: **`{time_str}`**')
