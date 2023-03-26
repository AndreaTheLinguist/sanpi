# %%
"""new script to create corpora subsets using newly released version of GREW python module, `grewpy`.
   Branched from `demo/create_grewpy_subset.interactive.py` (was just `demo/create_grewpy_subset.py`)"""
import argparse
import enum
import os
from collections import namedtuple
from pathlib import Path
import json
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

    # > create output directory and shared stem for output files
    subset_dir = conllu_path.parent.joinpath(f'subset_{subset_name}')
    if not subset_dir.is_dir():
        subset_dir.mkdir()
    out_stem = f"{(subset_name).upper()}.{conllu_path.stem}"

    print(f'stem for output files: `{out_stem}`')
    # * Describing the corpus (`co`)
    print('## Loaded (full-size) corpus info')
    # counts_df = describe_corpus(conllu_path, co)
    counts_df = describe_corpus_json(conllu_path, co)

    # * `ADV ADJ` bigrams/collocations
    print(f'## Assessing `{conllu_path.name}` for',
          f'`{Path(*pat_path.resolve().parts[-3:])}`')

    # > get request from pattern file
    req = Request(grewpize_pat_path(pat_path))
    print('\n```')
    pprint_pat(req)
    print('```\n')

    # > count hits for pattern and describe
    show_req_counts(co, req, conllu_path, subset_name)

    # * Collect context info
    print('\n## Compiling Context Info...')
    proc_t0 = pd.Timestamp.now()
    context_info = build_context(co, req, conllu_path)
    proc_t1 = pd.Timestamp.now()
    time_str = get_time_str(proc_t0, proc_t1)
    print(f'+ Time to build context dataframe: {time_str}')

    subset_sent_total = len(context_info)
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
    create_subset_conllu(co, context_info.index,
                         sub_conllu_path)
    proc_t1 = pd.Timestamp.now()
    time_str = get_time_str(proc_t0, proc_t1)

    print(f'\n✓  `{subset_name}` subset of `{conllu_path.name}` saved as:\n'
          f'  > `{sub_conllu_path.resolve().relative_to(conllu_path.parent)}`')
    print(f'+ Total time to create new conllu output: `{time_str}`\n\n'
          '*******************************************\n')
    
    print(f'## Subset Counts: {sub_conllu_path.name}')
    totals = pd.DataFrame()
    totals['input'] = counts_df.squeeze()
    totals['subset']= describe_corpus_json(sub_conllu_path, 
                             corpus_from_path(sub_conllu_path)).squeeze()
    totals['change'] = totals.subset - totals.input
    totals = totals.astype('int')
    totals['%_of_input'] = (totals.subset / totals.input * 100).round(1)
    print(f'\n## Corpus Size Comparison: `{conllu_path.stem}` ⇢  `{out_stem}`\n')
    print(totals.to_markdown(floatfmt=',.0f'))
   

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
        10, 'total').to_markdown(floatfmt=',.0f'))

    # > counts by bigram/collocation
    print(f"\nTop 5 `{subset_name}` matches in `{conllu_path.name}`\n")
    print(table_counts_by(corpus, req, ["ADV.lemma", "ADJ.lemma"],
                          total_hits).nlargest(5, 'total').to_markdown(floatfmt=',.0f'))


def create_subset_conllu(
        corpus: Corpus, sent_ids,
        sub_conllu_path: Path) -> None:

    _t0s = pd.Timestamp.now()
    conllu_output = '\n'.join(
        corpus.get(x).to_conll()
        for x
        in sent_ids)
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
    #   dur_round((_t1w - _t0w).seconds))


def build_context(corpus: Corpus,
                  req: Request,
                  conllu_path: Path) -> pd.DataFrame:
    sent_ids = pd.Series(match['sent_id']
                         for match in corpus.search(req)).unique()
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
    #? # LATER: `total_hits` could be calculated by getting sum of counts column?
    if len(cluster) == 1:
        df = pd.Series(corpus.count(request, cluster)
                       ).to_frame().rename(
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


def describe_corpus_json(conllu_path: Path,
                         corpus: Corpus):
    _t0 = pd.Timestamp.now()
    file_size = fileSize(conllu_path, sizeUnit.MB, decimals=2)
    counts_df = pd.DataFrame(
        index=['total'],
        columns=['file_MB', 'sentences', 'tokens'])
    counts_df['file_MB'] = file_size
    counts_df['sentences'] = int(len(corpus))
    counts_df['tokens'] = int(sum(len(sent) for sent in corpus))
    
    json_dict = dict.fromkeys(['total', 'ADV', 'ADJ', 'NEG', 'NR'])
    for name, spec in (
        ('ADV', 'xpos=re"RB.*"'),
        ('ADJ', 'xpos=re"JJ.*"'),
        ('NEG', ('lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|'
                 '"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"')),
        ('NR', ('lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"'
                '|"imagine"|"likely"|"probable"|"appear"|"look"|"intend"'
                '|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"'
                '|"desirable"|"should"|"ought"|"better"|"most"|"usually"'))):
        req = Request(f'X[{spec}]')
        total_count = corpus.count(req)
        counts_df[f'{name}_tokens'] = total_count
        
        node_counts={}
        
        xpos_df = table_counts_by(corpus, req, ["X.xpos"], total_count)
        node_counts['by_xpos'] = xpos_df.to_dict(orient='index')
        counts_df[f'{name}_xpos']=len(xpos_df)
        print(f"\nTotal {name} in `{conllu_path.name}` by exact POS:\n")
        print(xpos_df.to_markdown(floatfmt=',.0f'), '\n')

        lemma_df = table_counts_by(corpus, req, ["X.lemma"], total_count)
        node_counts['by_lemma'] = lemma_df.to_dict(orient='index')
        counts_df[f'{name}_lemmas']=len(lemma_df)
        print(f"\nTop 10 {name} lemmas in `{conllu_path.name}`\n")
        print(lemma_df.nlargest(10, 'total').to_markdown(floatfmt=',.0f'), '\n')
        
        form_df = table_counts_by(corpus, req, ["X.form"], total_count)
        node_counts['by_form'] = form_df.to_dict(orient='index')
        counts_df[f'{name}_forms']=len(form_df)
        print(f"\nTop 10 {name} forms in `{conllu_path.name}`\n")
        print(form_df.nlargest(10, 'total').to_markdown(floatfmt=',.0f'), '\n')
        
        json_dict[name] = node_counts
        

    json_dict.update(counts_df.to_dict(orient="index"))
    
    info_dir=conllu_path.with_name('info')
    if not info_dir.is_dir():
        info_dir.mkdir()
        
    json_path=info_dir.joinpath(f'{conllu_path.stem}.counts.json')
    json_path.write_text(json.dumps(json_dict, indent=4), encoding='utf8')
    
    print(f"\n### `{conllu_path.name}` overview\n")
    print(counts_df.transpose().to_markdown(floatfmt=',.0f'))
    print(f'\n+ Counts info saved to: `../{json_path.relative_to(conllu_path.parent.parent)}`')
    
    _t1 = pd.Timestamp.now()
    time_str = get_time_str(_t0, _t1)
    print(f'+ Time to gather counts: `{time_str}`\n\n'
          '*******************************************\n')
    return counts_df


# def describe_corpus(conllu_path, co):
#     file_size = fileSize(conllu_path, sizeUnit.MB, decimals=2)
#     counts_df = pd.DataFrame(
#         index=['total'],
#         columns=['file_MB', 'sentences', 'tokens', 'ADV', 'ADJ', 'NEG', 'NR'])
#     counts_df['file_MB'] = file_size
#     counts_df['sentences'] = len(co)
#     counts_df['tokens'] = sum(len(sent) for sent in co)

#     for name, spec in (
#         ('ADV', 'xpos=re"RB.*"'),
#         ('ADJ', 'xpos=re"JJ.*"'),
#         ('NEG', ('lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|'
#                  '"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"')),
#         ('NR', ('lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"'
#                 '|"imagine"|"likely"|"probable"|"appear"|"look"|"intend"'
#                 '|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"'
#                 '|"desirable"|"should"|"ought"|"better"|"most"|"usually"'))):
#         req = Request(f'X[{spec}]')
#         total_count = co.count(req)
#         counts_df[name] = total_count

#         print(f"\nTotal {name} in `{conllu_path.name}` by exact POS:\n")
#         print(table_counts_by(co, req, ["X.xpos"],
#               total_count).to_markdown(floatfmt=',.0f'), '\n')

#         print(f"\nTop 10 {name} lemma in `{conllu_path.name}`\n")
#         print(table_counts_by(co, req, ["X.lemma"], total_count).nlargest(
#             10, 'total').to_markdown(floatfmt=',.0f'), '\n')

#     print(f"### `{conllu_path.name}` overview\n")
#     print(counts_df.transpose().to_markdown(floatfmt=',.0f'))
#     print('\n*******************************************\n')
#     return counts_df


def get_time_str(start: pd.Timestamp,
                 finish: pd.Timestamp) -> str:
    t_comp = (finish - start).components
    time_str = (
        ":".join(str(c).zfill(2)
                 for c
                 in (t_comp.hours, t_comp.minutes, t_comp.seconds))
        + f'.{str(t_comp.microseconds).zfill(3)}')

    return time_str


if __name__ == '__main__':
    _t0 = pd.Timestamp.now()
    _main()
    _t1 = pd.Timestamp.now()
    time_str = get_time_str(_t0, _t1)
    print(f'\n## Subset creation complete!✨ \n'
          f'Total time elapsed: **`{time_str}`**')
