import argparse
import json
import sys
import time
from collections import namedtuple
from pathlib import Path

import pyconll

_dep_tuple = namedtuple('dependency', ['source', 'target', 'relation'])
_tok_tuple = namedtuple('token', ['lemma', 'ix', 'xpos', 'deprel', 'head'])


def fill_json(conllu_dir: Path,
              raw_dir: Path,
              rewrite: bool = False,
              output_dir: Path = None):

    dir_start = time.perf_counter()
    paired_paths, output_dir = _check_dirs(raw_dir, conllu_dir, output_dir)

    # TODO : make this parallel??
    for data_stem, paths_pair in paired_paths.items():
        file_start = time.perf_counter()
        json_fpath = paths_pair.raw_json
        filled_json_path = json_fpath.with_name(json_fpath.name.replace('.raw', ''))
        if not rewrite and filled_json_path.exists():
            print(
                f'-> {data_stem} data was previously processed: Skipping.\n     Output in {filled_json_path}')
            continue

        print(f'-> Processing {data_stem}...')
        # conllu_fpath = conllu_dir.joinpath(f'{data_stem}.conllu')
        # json_fpath = list(raw_dir.rglob(f'*{data_stem}*.raw*'))[0]
        # json_fpath = raw_dir.joinpath(f'{pref}.raw.json')
        # load json object
        # note that ordering of sentence ids in json file are reverse of conllu
        hits_json = _load_hits_json(json_fpath)

        if not hits_json:
            print('! -> Skipping. (file is empty)')
            continue
        # > connect (possible) context ids with hit ids
        context_sent_ids = _include_context(hits_json)
        hits_by_id = {}
        for hit_dict in hits_json:
            sent_id = hit_dict['sent_id']
            context_dict = {}
            context_dict['prev_id'] = context_sent_ids[sent_id].prev_id
            context_dict['prev_sent'] = ''
            context_dict['next_id'] = context_sent_ids[sent_id].next_id
            context_dict['next_sent'] = ''
            hit_dict['context'] = context_dict
            #TODO: fix this non-unique identifier bug
            #! Using this as the dict key is the source of the empty hits later on: if 2
            #!   matches have the same `ADV` and `ADJ` nodes, but different `NEG` nodes, only 1
            #!   is processed. That is, the second hit overwrites the first in the dictionary.
            node_id_dict = hit_dict['matching']['nodes']
            # > add hit id
            # >   format: [sentence id]-[ADV node id]-[ADJ node id]
            #       (where `sentence id` = [doc_id]_[sentence index])
            hit_id = f"{sent_id}:{node_id_dict['NEG']}-{node_id_dict['ADV']}-{node_id_dict['ADJ']}"
            # > add additional top layer to json to order by hit id, rather than int index
            hits_by_id[hit_id] = hit_dict
            hit_dict['hit_id'] = hit_id


        hits_by_id, json_entry_count, conll_count = _add_conll_info(
            hits_by_id, paths_pair.conllu, context_sent_ids)

        finish = time.perf_counter()

        print(f'    + {json_entry_count} hit results filled from {conll_count} total original '
              f'sentences in {round(finish - file_start, 2)} seconds')

        _write_new(filled_json_path, hits_json)

    print('Finished processing all corresponding json and conll files.')
    absFinish = time.perf_counter()
    print(
        f'\nTime elapsed: {round((absFinish - dir_start)/60, 2)} minutes\n'
        '====================================\n')


def _add_conll_info(hits_by_id: dict, conllu_fpath: Path, ids_dict: dict):

    # TODO add info on what the "trigger" word is, and words directly preceding adv?

    sent_with_hit = tuple(ids_dict.keys())
    # > flatten context tuple into flat tuple and concatonate with hit ids
    # > convert to set to remove duplicate ids
    id_set = set(sent_with_hit + sum(ids_dict.values(), ()))

    # prev_ids = {v.prev_id: k for k, v in ids_dict.items()}
    # next_ids = {v.next_id: k for k, v in ids_dict.items()}
    # // create dictionary mapping sentence id to text for possible context sentences
    # // context_sent_dict = {i.id: i.text
    # //                      for i in pyconll.load.iter_from_file(conllfile)
    # //                      if i.id in set(prev_ids + next_ids)}

    # > create full hit generator object from conllu file
    conll_gen = (sent for sent in pyconll.load.iter_from_file(conllu_fpath)
                 if sent.id in id_set)
    # conll_gen = (c for c in pyconll.load.iter_from_file(conllu_fpath)
    #              if c.id in sent_with_hit)
    # > initialize json entry count
    json_entry_count = 0
    json_loops = 0
    # > initialize conllu entry count
    conll_count = 0

    hit_start = time.perf_counter()
    # > add info from conllu to json
    for conllu in conll_gen:

        current_id = conllu.id
        sent_text = conllu.text

        id_to_ix = conllu._ids_to_indexes
        tok_dicts = conllu._tokens
        # > list and for loop required to ensure all hit info will be
        # > filled in the case of a single sentence having more than 1
        # > search hit
        relevant_hit_ids_iter = (
            hit_id for hit_id in hits_by_id.keys()
            if current_id in (hits_by_id[hit_id]['sent_id'],
                              hits_by_id[hit_id]['context']['prev_id'],
                              hits_by_id[hit_id]['context']['next_id']))

        for hit_id in relevant_hit_ids_iter:

            hit_dict = hits_by_id[hit_id]

            if current_id == hit_dict['sent_id']:
                raw_match_info = hit_dict.pop('matching')
                hit_dict['text'] = sent_text
                hit_dict['token_str'] = ' '.join(t.form for t in tok_dicts)
                hit_dict['lemma_str'] = ' '.join(t.lemma for t in tok_dicts)

                _update_tokens(conllu, tok_dicts, id_to_ix,
                               hit_dict, raw_match_info)

                hit_dict['deps'] = _get_deps(raw_match_info['edges'],
                                             tok_dicts, id_to_ix)
                json_entry_count += 1
            elif current_id == hit_dict['context']['prev_id']:
                hit_dict['context']['prev_sent'] = sent_text

            elif current_id == hit_dict['context']['next_id']:
                hit_dict['context']['next_sent'] = sent_text
            json_loops += 1
        conll_count += 1

    hit_end = time.perf_counter()
    print(f'Total time to fill {conllu_fpath.stem} hits json:'
          f' {round((hit_end-hit_start)/60,1)} min')
    print(f'= {json_loops} json loops\n'
          f'= {conll_count} conllu sentence objects')

    return hits_by_id, json_entry_count, conll_count


# def _fill_context(hits: dict, ids_dict: dict, conllu_fpath: Path):

    # for context_type in ('prev', 'next'):
    #     id_key = f'{context_type}_id'
    #     text_key = f'{context_type}_text'
    #     # prev
    #     if context_type == 'prev':
    #         context_sent_ids = {v.prev_id: k for k, v in ids_dict.items()}
    #     # next
    #     else:
    #         context_sent_ids = {v.next_id: k for k, v in ids_dict.items()}

    #     context_gen = (c for c in pyconll.load.iter_from_file(conllu_fpath)
    #                    if c.id in context_sent_ids.keys())

    #     for context_sent in context_gen:
    #         sent_id = context_sent.id
    #         sent_text = context_sent.text

    #         corresponding_hit_ids = [hit_id for hit_id in hits.keys()
    #                                  if hits[hit_id][id_key] == sent_id]

    #         for hit_id in corresponding_hit_ids:
    #             hits[hit_id][text_key] = sent_text

    # return hits


def _include_context(hits):

    context = namedtuple('context', ['prev_id', 'next_id'])
    parts_tuple = namedtuple('hit_id', ['doc_id', 'sent_ix'])

    hit_ids = list(set(h['sent_id'] for h in hits))
    hit_ids.sort()
    id_parts_dict = {id_str: parts_tuple._make(
        id_str.rsplit('_', 1)) for id_str in hit_ids}

    # // prev_ids = [f'{pair[0]}_{int(pair[1])-1}' for pair in id_parts]
    # // next_ids = [f'{pair[0]}_{int(pair[1])+1}' for pair in id_parts]
    #! because sentence index value may be zfilled, the constucted ids
    #! must also be zfilled to successfully locate the context sentence
    context_dict = {}
    for hit_id, parts_tuple in id_parts_dict.items():
        ix_str = parts_tuple.sent_ix
        zlen = len(ix_str)
        prev_sent_ix = str(int(ix_str)-1).zfill(zlen)
        next_sent_ix = str(int(ix_str)+1).zfill(zlen)
        context_dict[hit_id] = context(f'{parts_tuple.doc_id}_{prev_sent_ix}',
                                       f'{parts_tuple.doc_id}_{next_sent_ix}')
    return context_dict
    # // return hit_ids, prev_ids, next_ids


#// def _get_context_id(sid, position: int):

    #// if '_' in sid:
    #//     parts = sid.rsplit('_', 1)
    #//     cix = f'{parts[0]}_{int(parts[1]) + position}'
    #//
    #// else:
    #//     cix = ''
    #//
    #// return cix


def _update_tokens(info, tok_dict_list, id_to_ix, hit, raw_match_info):
    nodes = raw_match_info['nodes']

    tok_lemmas = tok_forms = {}

    for k, v in nodes.items():
        try:
            token = tok_dict_list[info._ids_to_indexes[v]]
        except KeyError:
            token = tok_dict_list[int(v) - 1]

        tok_lemmas[k] = token.lemma
        tok_forms[k] = token.form

    hit['lemmas'] = tok_lemmas
    hit['forms'] = tok_forms

    for node, id in nodes.items():
        nodes[node] = _get_ix(id_to_ix, id)
    hit['index'] = nodes


def _load_hits_json(raw_json_file):

    hits = None

    # note that ordering of sentence ids in json file are reverse of conllu
    with open(raw_json_file, 'r') as j:

        try:
            hits = json.load(j)

        except json.decoder.JSONDecodeError:
            pass

        else:

            if len(hits) < 1:
                hits = None

    return hits


def _write_new(out_path: Path, hits):

    with open(out_path, 'w') as o:
        print(f'   -> Writing output file {Path(*out_path._parts[-4:])}...')
        json.dump(hits, o, indent=2)


def _check_dirs(raw: Path, conllu: Path, output: Path = None):

    # raw = args.raw_dir
    # conllu = args.conllu_dir

    if not (raw.is_dir() and conllu.is_dir()):

        sys.exit(
            'Error: specified conll directory and json directory do not exist'
            ' in the base directory.')
        
    if raw.stem != conllu.stem:
        sys.exit(
            'Error: specified conll directory and json directory do not match.')

    if len(list(raw.iterdir())) > 0:
        paired_paths_dict = _getDataPairs(raw, conllu)

        if not paired_paths_dict:
            sys.exit('Error: No corresponding .json and .conllu files found.')

    else:
        sys.exit('Error: specified data directory is empty')

    output_dir = output if output else raw

    if not output_dir.exists():
        output_dir.mkdir()

    return paired_paths_dict, output_dir


def _get_deps(edges, tok_dicts, id_to_ix):
    deps = {}
    for edge, parts in edges.items():

        source_tok = _process_edge(parts['source'], tok_dicts, id_to_ix)
        target_tok = _process_edge(parts['target'], tok_dicts, id_to_ix)

        label = parts['label']
        ## TODO: change to `isinstance()`
        if type(label) == dict:
            label = label.get('1', '_')

        deps[edge] = _dep_tuple(source_tok._asdict(),
                                target_tok._asdict(),
                                label)._asdict()

    return deps


def _process_edge(id, tok_dicts, id_to_ix):
    ix = _get_ix(id_to_ix, id)
    tok = tok_dicts[ix]
    head = tok_dicts[_get_ix(id_to_ix, tok.head)].lemma

    tokt = _tok_tuple(tok.lemma, ix, tok.xpos, tok.deprel, head)
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

    parser.add_argument('-R', '--rewriteFiles', action='store_true',
                        help='Option to rewrite previously processed json files. '
                        'If not included, processed files will be skipped.')
    # Obsolete Arguments
    # // parser.add_argument('-w', '--rewriteFiles',
    # //                     choices=['yes', 'no', 'check'],
    # //                     default='yes',
    # //                     help='Indicate whether to skip file pairs which '
    # //                     'already have a corresponding filled (already '
    # //                     'processed) json file. Options are: '
    # //                          '\'no\' = rewrite none; '
    # //                          '\'yes\' = rewrite all; '
    # //                          '\'check\' = check for each case, which requires '
    # //                          'user input. The default is to rewrite all '
    # //                          'previously created output files (i.e. \'yes\').')
    # //
    # // parser.add_argument('-t', '--tokenFillerType',
    # //                     choices=['lemma', 'form'],
    # //                     default='lemma',
    # //                     help='set type for fillers. options are lemma or form. '
    # //                     'Lemma is used by default.')

    return parser.parse_args()


def _getDataPairs(json_dir, conllu_dir):
    '''function to return list of file prefixes which have both conllu and raw json files '''
    paths_tuple = namedtuple('data_paths', ['raw_json', 'conllu'])

    raw_jsons = {j.name.replace('.raw.json', ''): j for j in json_dir.rglob(
        f'*.raw.json')}
    conllus = {c.stem: c for c in conllu_dir.glob('*.conllu')}
    paired_stems = list(set(raw_jsons.keys()).intersection(conllus.keys()))
    paired_stems.sort()
    path_pairs = {stem: paths_tuple(
        raw_jsons[stem], conllus[stem]) for stem in paired_stems}
    return path_pairs


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
    fill_json(*_parseArgs())
