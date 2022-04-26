import argparse
import json
import sys
import time
from collections import namedtuple
from pathlib import Path

import pyconll

deptup = namedtuple('dependency', ['source', 'target', 'relation'])
toktup = namedtuple('token', ['lemma', 'ix', 'xpos', 'deprel', 'head'])


def fill_json():
    absStart = time.perf_counter()
    args = _parseArgs()

    prefixes, outputDir = _check_dirs(args)

    jsonDirPath = args.raw_dir
    conllDirPath = args.conllu_dir
    rewrite = args.rewriteFiles

    print(
        f'```\n### Running `FillJson.py` script on json files in '
        f'`{jsonDirPath.name}` from conll files in `{conllDirPath.name}`...\n'
        f'```')

    for pref in prefixes:

        startTime = time.perf_counter()

        jsonfiles = jsonDirPath.glob(f'{pref}*')
        # //if rewrite != 'yes' and _skipFiles(pref, jsonDirPath, rewrite):
        if any('.raw' not in j.suffixes for j in jsonfiles):
            print(
                f'-> {pref} data was previously processed. Skipping.')
            continue

        print(f'-> Processing {pref}...')
        conllfile = conllDirPath.joinpath(f'{pref}.conllu')
        jsonfile = jsonDirPath.joinpath(f'{pref}.raw.json')
        # load json object
        # note that ordering of sentence ids in json file are reverse of conllu
        hits = _load_hits_json(jsonfile)

        if not hits:
            print('! -> Skipping. (file is empty)')
            continue

        hits, json_entry_count, conll_count = _add_conll_info(hits, conllfile)

        finishTime = time.perf_counter()

        print(f'    + {json_entry_count} hit results filled from {conll_count} total original '
              f'sentences in {round(finishTime - startTime, 2)} seconds')

        _write_new(outputDir, pref, hits)

    print('Finished processing all corresponding json and conll files.')
    absFinish = time.perf_counter()
    print(
        f'\nTime elapsed: {round((absFinish - absStart)/60, 2)} minutes\n'
        '====================================\n')


def _add_conll_info(hits, conllfile):

    # TODO add info on what the "trigger" word is, and words directly preceding adv?

    # connect (possible) context ids with hit ids
    hit_ids, prev_ids, next_ids = _include_context(hits)

    # create dictionary mapping sentence id to text for possible context sentences
    # context_sent_dict = {i.id: i.text
    #                      for i in pyconll.load.iter_from_file(conllfile)
    #                      if i.id in set(prev_ids + next_ids)}

    # create full hit generator object from conllu file
    conll_gen = (sent for sent in pyconll.load.iter_from_file(conllfile)
                 if sent.id in set(hit_ids + prev_ids + next_ids))

    # initialize json entry count
    json_entry_count = 0

    # initialize conllu entry count
    conll_count = 0

    prev_sent = ''
    sent_id = ''
    sent_text = ''

    # add info from conllu to json
    for hit_conll in conll_gen:

        prev_sent = ''
        prev_id = sent_id
        prev_text = sent_text

        sent_id = hit_conll.id
        sent_text = hit_conll.text

        if sent_id == _get_context_id(prev_id, 1) and prev_id in hit_ids:

            # hitIndexList should always be defined if previous sentence was a hit
            for hitIndex in hitIndexList:
                hits[hitIndex]['next_sent'] = sent_text

        if sent_id in hit_ids:

            if prev_id == _get_context_id(sent_id, -1):
                prev_sent = prev_text

            id_to_ix = hit_conll._ids_to_indexes
            tokdictlist = hit_conll._tokens
            # list and for loop required to ensure all hit info will be
            # filled in the case of a single sentence having more than 1
            # search hit
            hitIndexList = [ix for ix, hit_id in enumerate(hit_ids)
                            if hit_id == sent_id]

            for hitIndex in hitIndexList:

                hit = hits[hitIndex]

                hit['prev_sent'] = prev_sent

                raw_match_info = hit.pop('matching')
                hit['text'] = sent_text
                hit['token_str'] = ' '.join(t.form for t in tokdictlist)
                hit['lemma_str'] = ' '.join(t.lemma for t in tokdictlist)

                _update_tokens(hit_conll, tokdictlist, id_to_ix,
                               hit, raw_match_info)

                hit['deps'] = _get_deps(raw_match_info['edges'],
                                        tokdictlist, id_to_ix)

                json_entry_count += 1

        conll_count += 1

    return hits, json_entry_count, conll_count


def _include_context(hits):

    # context = namedtuple('context', ['prev_id', 'next_id'])

    hit_ids = [h['sent_id'] for h in hits]
    id_parts = [id_str.rsplit('_', 1) for id_str in hit_ids]

    prev_ids = [f'{pair[0]}_{int(pair[1])-1}' for pair in id_parts]
    next_ids = [f'{pair[0]}_{int(pair[1])+1}' for pair in id_parts]

    return hit_ids, prev_ids, next_ids


def _get_context_id(sid, position: int):

    if '_' in sid:
        parts = sid.rsplit('_', 1)
        cix = f'{parts[0]}_{int(parts[1]) + position}'

    else:
        cix = ''

    return cix


def _update_tokens(info, tokdictlist, id_to_ix, hit, raw_match_info):
    nodes = raw_match_info['nodes']

    tok_lemmas = tok_forms = {}

    for k, v in nodes.items():
        try:
            token = tokdictlist[info._ids_to_indexes[v]]
        except KeyError:
            token = tokdictlist[int(v) - 1]

        tok_lemmas[k] = token.lemma
        tok_forms[k] = token.form

    hit['lemmas'] = tok_lemmas
    hit['forms'] = tok_forms

    for node, id in nodes.items():
        nodes[node] = _get_ix(id_to_ix, id)
    hit['index'] = nodes


def _load_hits_json(jsonfile):

    hits = None

    # note that ordering of sentence ids in json file are reverse of conllu
    with open(jsonfile, 'r') as j:

        try:
            hits = json.load(j)

        except json.decoder.JSONDecodeError:
            pass

        else:

            if len(hits) < 1:
                hits = None

    return hits


def _write_new(outputDir, pref, hits):

    with open(outputDir / f'{pref}.json', 'w') as o:
        print('   -> Writing output file...')
        json.dump(hits, o, indent=2)


def _check_dirs(args):

    jsonDirPath = args.raw_dir
    conllDirPath = args.conllu_dir

    if not (jsonDirPath.is_dir() and conllDirPath.is_dir()):

        sys.exit(
            'Error: specified conll directory and json directory do not exist'
            ' in the base directory.')

    if len(list(jsonDirPath.iterdir())) > 0:
        prefixes = _getValidPrefixes(jsonDirPath, conllDirPath)

        if not prefixes:
            sys.exit('Error: No corresponding .json and .conllu files found.')

    else:
        sys.exit('Error: specified data directory is empty')

    outputDir = args.output_dir if args.output_dir else jsonDirPath

    if not outputDir.exists():
        outputDir.mkdir()

    return prefixes, outputDir


def _get_deps(edges, tokdictlist, id_to_ix):
    deps = {}
    for edge, parts in edges.items():

        source_tok = _process_edge(parts['source'], tokdictlist, id_to_ix)
        target_tok = _process_edge(parts['target'], tokdictlist, id_to_ix)

        label = parts['label']
        if type(label) == dict:
            label = label.get('1', '_')

        deps[edge] = deptup(source_tok._asdict(),
                            target_tok._asdict(),
                            label)._asdict()

    return deps


def _process_edge(id, tokdicts, id_to_ix):
    ix = _get_ix(id_to_ix, id)
    tok = tokdicts[ix]
    head = tokdicts[_get_ix(id_to_ix, tok.head)].lemma

    tokt = toktup(tok.lemma, ix, tok.xpos, tok.deprel, head)
    return tokt


def _get_ix(id_to_ix, id):
    try:
        ix = id_to_ix[id]
    except KeyError:
        ix = int(id) - 1
    return ix


def _parseArgs():
    parser = argparse.ArgumentParser(
        description=(
            'This is a script to loop over all \'.raw.json\' (grew-match '
            'result) files in a given directory and output new json files with '
            'info filled in from the corresponding .conllu (corpus info) files'))

    parser.add_argument('conllu_dir', type=Path,
                        help='path to directory containing sentences .conllu '
                        'files. e.g. Nyt1.conll')

    parser.add_argument('raw_dir', type=Path,
                        help='path to directory containing unprocessed/raw '
                        '.json search result files to be processed of '
                        'form \'<sentenceSetID>.raw.json\'. e.g. Nyt1.if')

    parser.add_argument('-o', '--output_dir', type=Path, default=None,
                        help='path to directory to write filled output json '
                        'files to. If not specified, the raw_dir path will'
                        ' be used (output/filled json files lose the '
                             '\'.raw\' in the filename.)')

    parser.add_argument('-w', '--rewriteFiles',
                        choices=['yes', 'no', 'check'],
                        default='yes',
                        help='Indicate whether to skip file pairs which '
                        'already have a corresponding filled (already '
                        'processed) json file. Options are: '
                             '\'no\' = rewrite none; '
                             '\'yes\' = rewrite all; '
                             '\'check\' = check for each case, which requires '
                             'user input. The default is to rewrite all '
                             'previously created output files (i.e. \'yes\').')

    parser.add_argument('-t', '--tokenFillerType',
                        choices=['lemma', 'form'],
                        default='lemma',
                        help='set type for fillers. options are lemma or form. '
                        'Lemma is used by default.')

    return parser.parse_args()


def _getValidPrefixes(jsonDir, conllDir):
    '''function to return list of file prefixes which have both conll and raw
        json files '''

    rawJsonSet = set(j.with_suffix('').stem for j in jsonDir.iterdir()
                     if '.raw' in j.suffixes)
    conlluSet = set(c.stem for c in conllDir.iterdir()
                    if c.suffix == '.conllu')

    return rawJsonSet.intersection(conlluSet)


def _skipFiles(prefix, directory, rewrite):
    if directory.joinpath(f'{prefix}.json').exists():
        if rewrite == 'no':
            return True
        while rewrite == 'check':
            skipResponse = input(f'Filled json for prefix {prefix} already '
                                 f'exists in directory {directory}. Do you '
                                 f'want to skip this file pair? y/n ')
            if skipResponse.lower() == 'y':
                return True
            if skipResponse.lower() == 'n':
                return False
    return False


if __name__ == '__main__':

    fill_json()
