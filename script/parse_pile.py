# -*- coding: utf-8 -*-
import argparse
from json import loads as jsloads
import time
from collections import namedtuple
from pathlib import Path
from pprint import pprint

import jsonlines
import pandas as pd
import stanza
from unidecode import unidecode
from datetime import date, datetime

doc2conll_text = stanza.utils.conll.CoNLL.doc2conll_text
pd.set_option('display.max_colwidth', 80)


def main():
    print('started:', datetime.now().ctime())
    args = parse_arg_inputs()
    corpus_selection = args.corpus_selection
    print('\nfiles to parse:')
    if args.file_list:
        files = args.file_list
        pprint(files)
    else:
        files = Path.cwd().glob('**/*jsonl')
        print(list(Path.cwd().glob('**/*jsonl')))

    print('\nselected pile set(s): ')
    pprint(corpus_selection)
    print('')

    # initiate language model for dependency parsing (load just once)
    # Note:
    #   standfordNLP does not have multi-word token (mwt) expansion
    #   for English, so `mwt` processor is not required for dependency parsing
    #   (https://github.com/stanfordnlp/stanza/issues/297#issuecomment-627673245)

    try:
        print('Loading dependency parsing pipeline...')
        nlp = stanza.Pipeline(
            lang='en',
            processors='tokenize,pos,lemma,depparse',
            # logging_level='WARN'
        )

    except stanza.pipeline.core.ResourcesFileNotFoundError:
        print('Language model not found. Downloading...')
        stanza.download('en')
        print('Loading dependency parsing pipeline...\n')
        nlp = stanza.Pipeline(
            lang='en',
            processors='tokenize,mwt,pos,lemma,depparse',
            # logging_level='WARN'
        )

    for data_file_path in files:
        print(f'\n---\n\nPreprocessing {data_file_path}...')
        df = preprocess_pile_texts(data_file_path, corpus_selection)
        df_output_dir = Path.cwd().joinpath('pile_tables')
        if not df_output_dir.is_dir():
            df_output_dir.mkdir()
        df_output_path = df_output_dir.joinpath(
            f'pile_{data_file_path.stem}_'
            f'{"-".join(corpus_selection).replace(" ","")}'
            '_table.pkl.gz')
        print('Finished preprocessing: dataframe saved to', df_output_path)
        df.to_pickle(df_output_path)

        for subset in corpus_selection:
            print(f'\nParsing {subset} data...')
            subset_df = df[df.pile_set_name == subset]

            out_fname = f'{subset_df.pile_set_code.iat[0]}_{data_file_path.stem}.conllu'
            out_dir = Path.cwd().joinpath(f'{subset}.conll')
            if not out_dir.is_dir():
                out_dir.mkdir()

            out_path = out_dir.joinpath(out_fname)

            stanza_parse(subset_df, nlp, out_path)


def parse_arg_inputs():

    parser = argparse.ArgumentParser(
        description='script to convert scrambled pile data from raw jsonlines format '
        'into dependency parsed conllu files.'
        'Required packages: stanza, unidecode, and pandas')

    parser.add_argument('-s', '--pile_set_name',
                        default=['Pile-CC'],
                        type=str,
                        action='append',
                        dest='corpus_selection',
                        help=('option to select alternate pile set(s). Default selection: "Pile-CC"'
                              'Flag can be reused: '
                              'All flagged paths will be appended to selection list'))

    parser.add_argument('-f', '--jsonl_file_path', type=Path, action='append', dest='file_list',
                        help=('flag to point to raw pile jsonlines file path to parse. Flag can be reused: '
                              'All flagged paths will be appended to file list.'))

    return parser.parse_args()


def preprocess_pile_texts(pile_data_path, selectCorp):
    # pile_data_path = Path('test.jsonl')
    datastem = pile_data_path.stem
    # define namedtuple to simplify dataframe creation from json object
    text_info = namedtuple('Text', ['text', 'pile_set_name'])

    # Load the (sample) jsonlines formatted (`.jsonl`) file using `jsonlines`.
    # Create a generator object which directly filters out texts from unwanted data sets.
    # Use pandas to create a flattened dataframe from the generator.
    print('  creating `jsonlines` generator for corpus selection...')
    read_t0 = time.perf_counter()
    with pile_data_path.open(encoding='utf-8-sig', mode='r') as jlf:
        jlines = jsonlines.Reader(jlf).iter()
        texts = (text_info(d['text'], d['meta']['pile_set_name'])
                 for d in jlines if d['meta']['pile_set_name'] in selectCorp)
        read_t1 = time.perf_counter()
        print(
            f'  ~ {round(read_t1 - read_t0, 4)}  sec elapsed')
        print('  building dataframe from from `jsonlines` generator object...')
        # This has to be done before the file is closed:
        #   Since we're using a generator to speed things up, the data is not fully
        #   loaded into the workspace until it's put into the dataframe.
        toDf_t0 = time.perf_counter()
        df = pd.DataFrame(
            texts, columns=text_info._fields, dtype='string')
        toDF_t1 = time.perf_counter()
        print(
            f'  ~ {round(toDF_t1 - toDf_t0, 3)}  sec elapsed')

    # Clean it up a bit, and remove duplicate text items
    df = df.drop_duplicates(subset='text').reset_index(drop=True)

    # temp sampling for debugging
    # df = df.sample(50)

    df = df.assign(
        pile_set_name=df.pile_set_name.astype('category'))

    print('  translating encoding...')
    unidecode_t0 = time.perf_counter()
    df = df.assign(text=df.text.apply(unidecode))
    unidecode_t1 = time.perf_counter()
    print(
        f'  ~ {round(unidecode_t1 - unidecode_t0, 2)}  sec elapsed')
    # Create codes for data subsets
    subset_abbr_dict = {'Gutenberg (PG-19)': 'PG19',
                        'Books3': 'Bks3',
                        'BookCorpus2': 'BkC2',
                        'Pile-CC': 'PiCC',
                        'OpenWebText2': 'OWT2'}
    codes = (subset_abbr_dict[n] for n in df.pile_set_name)
    df = df.assign(pile_set_code=pd.Categorical(codes))

    print('  adding subset codes & text IDs...')
    # Create text ids from raw file name, pile subset code, and dataframe index.
    codedf = pd.DataFrame()
    codes_t0 = time.perf_counter()
    for code in df.pile_set_code.unique():
        subdf = df.loc[df.pile_set_code == code, :].reset_index()
        prefs = code + '_' + datastem + '_'
        idnums = subdf.index.astype('string')
        width = len(str(df.index.max()))
        idnums = idnums.str.zfill(width)
        subdf = subdf.assign(text_id=prefs + idnums)

        codedf = pd.concat([codedf, subdf])
    codes_t1 = time.perf_counter()
    print(
        f'  ~ {round(codes_t1 - codes_t0, 3)}  sec elapsed')

    df = codedf[['text_id', 'text', 'pile_set_name', 'pile_set_code']]
    df = df.assign(text_id=df.text_id.astype('string'),
                   pile_set_code=df.pile_set_code.astype('category'))
    print('\nSnippet of dataframe:')
    print(df.head())
    print('...')
    return df


def stanza_parse(df, nlp, output_path):
    # TODO : change POS to XPOS; remove extra features?

    # open output file for conll formatted data
    print(f'  parsed data will be written to {output_path}')
    with open(output_path, mode='w', encoding='utf8') as conlloutput:
        # for each text in the pile subset...
        total = len(df)
        print(f'  {total} texts to parse')
        count = 0
        for ix in df.index:
            parse_t0 = time.perf_counter()
            text = df.text[ix]
            print(f'  {ix+1} of {total}: {df.at[ix, "text_id"]}')

            # create doc (with parsing)
            try:
                j = jsloads(text)
            except ValueError:
                pass
            else:
                print('WARNING! Skipping invalid text format: json')
                continue

            try:
                doc = nlp(text)
            except RuntimeError:
                print('WARNING! Skipping unparsable text. (reason unknown)')
            else:
                process_doc(df, conlloutput, ix, doc)
                count += 1
            parse_t1 = time.perf_counter()
            print(
                f'        {round(parse_t1 - parse_t0, 2)}  sec elapsed')

    print(f'Finished writing parses to {output_path}')
    print(f'= {count} of {len(df)} texts successfully parsed.')
    print(datetime.now().ctime())


def process_doc(df, conlloutput, ix, doc):
    # add comments to sentences (info pulled from dataframe)
    for s in doc.sentences:
        text_id = df.at[ix, 'text_id']

        if s.id == 0:
            # "newdoc id" will be the text_id from the pile subset
            s.add_comment(f'# newdoc id = {text_id}')

            # TODO : fix numbering of tokens (or see if necessary to start at 1)
            # "sent_id" will be doc/text id with _[sentence number] appended
        s.add_comment(f'# sent_id = {text_id}_{s.id}')

        # this adds the full text string to the output file
        s.add_comment(f'# text = {s.text}')

        # write conll formatted string of doc to output file
    conlloutput.write(doc2conll_text(doc))


if __name__ == '__main__':
    main()
