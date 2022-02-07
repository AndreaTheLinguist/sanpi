# -*- coding: utf-8 -*-
import argparse
# from itertools import groupby as itgrby
# from more_itertools import pairwise, grouper
from json import loads as jsloads
# import re
import time
from collections import namedtuple
from pathlib import Path
from pprint import pprint
import zlib
from bs4 import BeautifulSoup
# from mediawiki_dump.tokenizer import clean as mwclean
# from numpy import empty
import wikitextparser as wtp
import jsonlines
import pandas as pd
import stanza
from unidecode import unidecode
from datetime import date, datetime

from pile_regex_imports import *

doc2conll_text = stanza.utils.conll.CoNLL.doc2conll_text

output_limit = 10000
pd.set_option('display.max_colwidth', 80)

# initiate language model for dependency parsing (load just once)
# Note:
#   standfordNLP does not have multi-word token (mwt) expansion
#   for English, so `mwt` processor is not required for dependency parsing
#   (https://github.com/stanfordnlp/stanza/issues/297#issuecomment-627673245)
try:
    print('Loading dependency parsing pipeline...')
    nlp = stanza.Pipeline(
        lang='en',
        processors='tokenize,pos,lemma,depparse')
except stanza.pipeline.core.ResourcesFileNotFoundError:
    print('Language model not found. Downloading...')
    stanza.download('en')
    print('Loading dependency parsing pipeline...\n')
    nlp = stanza.Pipeline(
        lang='en',
        processors='tokenize,pos,lemma,depparse')


def main():
    print('started:', datetime.now().ctime())
    args = parse_arg_inputs()

    dfiles = [d.resolve()
              for d in args.df_files] if args.df_files else []

    rfiles = get_rawfile_list(args)
    if rfiles:
        subcorpora_list = args.corpus_selection
        print('\nraw jsonlines files will be processed for the following subcorpora: ')
        pprint(subcorpora_list)
        print('')

    if dfiles:
        for df, data_source_label in process_pickledf(dfiles):
            slice_df(df, data_source_label)
        # df_data_gen = process_pickledf(dfiles)

    if rfiles:
        for df, data_source_label in process_raw_jsonlines(rfiles, subcorpora_list):
            slice_df(df, data_source_label)
        # jl_data_gen = process_raw_jsonlines(rfiles, subcorpora_list)

    # for df, data_source_label in df_data_gen + jl_data_gen:
    #     slice_df(df, data_source_label)


def parse_arg_inputs():

    parser = argparse.ArgumentParser(
        description='script to convert scrambled pile data from raw jsonlines format '
        'into dependency parsed conllu files.'
        'Required packages: stanza, unidecode, and pandas')

    parser.add_argument(
        '-s', '--pile_set_name',
        default=['Pile-CC'],
        type=str, action='append', dest='corpus_selection',
        help=('option to select alternate pile set(s). Default selection: "Pile-CC".'
              ' Flag can be reused: '
              'All flagged paths will be appended to selection list'))

    parser.add_argument(
        '-f', '--jsonl_file_path',
        type=Path, action='append', dest='jsonl_files',
        help=('flag to point to raw pile jsonlines file path to parse. Flag can be reused: '
              'All flagged paths will be appended to file list. If no file or dataframe '
              '(below) flags are included, '
              'all .jsonl data files will be run.'))

    parser.add_argument(
        '-d', '--dataframe',
        type=Path, action='append', dest='df_files',
        help=('If a pickle/.pkl(.gz) of the processed dataframe already exists from a previous run '
              '(saved in `[cwd]/pile_tables/`), use this '
              'option to specify its path and skip the first step of the script. This flag can be reused: '
              'all specified paths will be appended to `df_files`. *NOTE*: -f and -d flags can be run together,'
              'so make sure they are not redundant!'))

    return parser.parse_args()


def get_rawfile_list(args):
    print('+ raw files selected to process:')
    files_list = []
    if args.jsonl_files:
        files_list = [f.resolve() for f in args.jsonl_files]
    # only do a glob search of directory if no pkl files given
    elif not args.df_files:
        files_list = list(Path.cwd().glob('**/*jsonl'))
        # note: can't print files_iter here bc it's a generator obj

    else:
        print('[no raw data files to be processed]')

    pprint(files_list)
    return files_list


def process_pickledf(dfiles):
    print('Preprocessed dataframes to parse into conllu files:\n')
    pprint(dfiles)

    for dfpath in dfiles:
        dfpath = dfpath.resolve()
        try:
            pathstr = dfpath.relative_to(Path.cwd())
        except:
            pathstr = dfpath

        print(f'\n---\n\n## Finishing processing {pathstr}'
              '\n-> Loading dataframe from compressed pickle...')

        loadstart = time.perf_counter()
        try:
            df = pd.read_pickle(dfpath)
        except zlib.error:
            print('Error: File cannot be decompressed (zlib). Skipping.')
            continue
        
        # previously saved df filestems
        else:
            loadcomplete = time.perf_counter()
            print('    [dataframe loaded in', round(
                loadcomplete - loadstart, 2), 'seconds]')

        #   = pile_[original jsonl file/data source file stem]_...
        # so index 1 gives the data_source_label when split by _
        data_source_label = dfpath.stem.split('_')[1]

        # run clean up on any dataframes in `tmp/` or `raw/`
        print('precleaned dataframe?')
        if 'raw' not in df.columns or dfpath.parent.name in ('tmp', 'raw'):
            print(f'  no -> Cleaning {dfpath}...')
            tmp_df_path = (dfpath if dfpath.parent.stem == 'tmp'
                           else get_dfpkl_outpath(dfpath.stem, is_tmp=True))
            df = clean_df(df, tmp_df_path)
            df.to_pickle(get_dfpkl_outpath(dfpath.stem))

        else:
            print('  yes')

        yield df, data_source_label


def process_raw_jsonlines(rfiles, subcorpora_list):
    for rawfile_path in rfiles:
        print(f'\n---\n\nPreprocessing {rawfile_path}...')

        df = preprocess_pile_texts(rawfile_path, subcorpora_list)

        data_source_label = rawfile_path.stem

        yield df, data_source_label


def clean_df(df, tmp_save_path):

    print('\nCleaning text in dataframe...')
    if any(df.text_id.str.startswith(('PiCC', 'pcc_eng'))):

        df = df.assign(
            text_id=df.text_id.str.replace('PiCC', 'pcc_eng').astype('category'))

    if 'raw' not in df.columns:
        df = df.assign(raw=df.text)

    df = df.assign(text=df.text.astype('string'),
                   raw=df.raw.astype('string'))

    df = clean_wikitexts(df)

    df.to_pickle(tmp_save_path)

    print('  looking for any html...')
    is_html = df.text.apply(
        lambda t: (bool(BeautifulSoup(t, "html.parser").find())))

    if any(is_html):
        print(f'  converting {len(df.loc[is_html, :])} html to text...')

        htmldf = df.loc[is_html, :]

        html_text = htmldf.text.apply(
            lambda t:
            BeautifulSoup(t, "html.parser").get_text()).astype('string')
        htmldf = htmldf.assign(text=html_text)
        if any(htmldf.text.isna()):
            htmldf.loc[htmldf.text.isna(), 'text']

        # exdf = htmldf.sample(min(2, len(htmldf)))
        # print('  examples:\n')
        # for rix in exdf.index:
        #     print('    text:')
        #     print(exdf.at[rix, 'text'])
        #     print('    from raw html:')
        #     print(exdf.at[rix, 'raw'])
        #     print('...')

        df.loc[is_html, ['raw', 'text']] = (htmldf.loc[:, ['raw', 'text']]
                                            .astype('string'))
        df.to_pickle(tmp_save_path)

    else: 
        print('    [none found]')
    df.to_pickle(tmp_save_path)

    print('  cleaning up text...\n   - urls...')
    # clean up web markers
    df = df.assign(text=df.text.apply(
        lambda t: likely_url.sub(r' [url] ', t)))
    # print('   - @ and # tagging...')
    # df = df.assign(text=df.text.apply(
    #     lambda t: re.sub(r'\@\w+(\s)', r' \<\@tag \1\>', t)))
    # df = df.assign(text=df.text.apply(
    #     lambda t: re.sub(r'\#(\w+\s)', r' \<\#tag \1\>', t)))
    print('   - title abbreviations at line breaks...')
    df = df.assign(
        text=df.text.apply(lambda t: end_of_line_abbr.sub(r'\1\2\5\6 \3\4', t)))
    print('   - punctuation delineated text breaks')
    df = df.assign(
        text=df.text.apply(
            lambda t: punc_only.sub(r'\1\2\3\4\5\6\7\n\n', t)))

    precleaned = ~df.text.isin(df.raw)
    if any(precleaned):
        changedf = df.loc[precleaned, :]
        print(f'{len(changedf)} of {len(df)} texts modified')

        # exdf = changedf.sample(min(2, len(changedf)))
        # print('  examples:\n')
        # for rix in exdf.index:
        #     print('    new text:')
        #     print(df.at[rix, 'text'])
        #     print('    from raw:')
        #     print(df.at[rix, 'raw'])

    df.loc[:, ['text', 'raw']] = df[['text', 'raw']].astype('string')
    return df


def clean_wikitexts(df):
    print('  looking for wikitext/wikimedia formatting...')
    wikidf = None    
    
    is_wiki = df.text.apply(lambda t: bool(defwiki.search(t)))
    if any(is_wiki):
        wikidf = df.loc[is_wiki, :]
        print(
            f'  extracting text from {len(wikidf)} known wikitext formatting...')
        wikidf = wikidf.assign(
            text=wikidf.text.apply(lambda t: wtp.parse(t).plain_text()).astype('string'))
        df.loc[is_wiki, :] = wikidf

    maybe_wiki = (df.text.apply(lambda t: bool(wikipat.search(t))))
    if any(maybe_wiki):
        wikidf = df.loc[maybe_wiki, :]
        print(f'  cleaning {len(wikidf)} possibly wikitext formatted texts...')
        cleaned_text = wikidf.text.apply(lambda t: _reformat_wiki(t))
        wikidf = wikidf.assign(text=cleaned_text.astype('string'))
        df.loc[maybe_wiki, :] = wikidf

    if wikidf is None:
        print('    [none found]')
    return df


def _reformat_wiki(t):

    # add vertical space between bullet points
    t = wt0.sub('\n\n', t)
    t = wt1.sub(r'\1\2', t)
    t = wt2.sub(r'\1', t)
    t = wt3.sub(r' (\3)', t)
    t = wt4.sub('\n\n', t)
    # remove links, internal or url
    t = wt5.sub(r'\1', t)
    t = wt6.sub(r'\1', t)
    t = wt7.sub(r'\1\1\2 \3\4\4', t)
    t = wt8.sub('', t)
    t = wt9.sub(r'\2', t)
    t = wt10.sub(r'\1', t)
    t = wt11.sub(r'\2', t)
    t = wt12.sub('\n\n\n', t)

    return t


def slice_df(full_df, data_source_label):

    for subcorpus_label, df in full_df.groupby('pile_set_code'):

        excl_save_path = get_dfpkl_outpath(
            data_source_label, subcorpus_label, is_excl=True)
        remaining_df, excl_df = pull_exclusions(df, excl_save_path)

        total = len(remaining_df)
        print(f'{total} total texts to parse')

        remaining_df = remaining_df.sort_values('text_id')
        slices = []
        # e.g. if limit were 1000:
        # slice off 1000 rows at a time until total is 2400 or less
        while len(remaining_df) > int(2.4*output_limit):

            dfslice = remaining_df.iloc[:output_limit, :].reset_index()
            remaining_df = remaining_df.iloc[output_limit:, :]
            slices.append(dfslice)
        # if 2400 split remaining: 2 slices of 1200
        # if 1202, split remaining: 2 slices of 610
        # if remaining df is 1200 rows or less:
        #   keep as is (no more slicing)
        if len(remaining_df) > 1.2*output_limit:

            half_remaining = int(len(remaining_df)/2)

            dfslice_penult = remaining_df.iloc[:half_remaining, :]
            slices.append(dfslice_penult)

            remaining_df = remaining_df.iloc[half_remaining:, :]

        # this must be outdented to catch smaller dataframes
        slices.append(remaining_df)

        for i, sdf in enumerate(slices):
            # starting at i = 0 meant the first slice wasn't
            # getting saved bc if slice_num was evaluating as False
            outpath = get_dfpkl_outpath(
                data_source_label, subcorpus_label,
                slice_num=i+1, is_tmp=True)
            sdf.to_pickle(outpath)

        process_slices(
            slices, total,  data_source_label, subcorpus_label, excl_df)


def pull_exclusions(df: pd.DataFrame, excl_save_path: Path):
    print('  pulling excluded formats...')
    excl_df = pd.DataFrame()
    if excl_save_path.is_file:
        excl_df = pd.read_pickle(excl_save_path)

        df = df.loc[~df.text_id.isin(excl_df.text_id)]
        print(f'  -> {len(excl_df)} previously identified exclusions removed')

    # this assumes exclusion search run previously would have been identical
    else:
        # flag texts that contain technical seeming strings and exclude for now
        technical = df.text.apply(lambda t:
                                  bool(len(variable_regex.findall(t)) > 15
                                       or possible_code.search(t)))

        is_json = df.text.apply(lambda t: bool(json_pat.search(t)))

        if any(technical) or any(is_json):
            excl_df = pd.concat([excl_df,
                                df.loc[technical | is_json, :]])
            df = df.loc[~df.text_id.isin(excl_df.text_id), :]

            excl_df.to_pickle(excl_save_path)
            print(f'  -> {len(excl_df)} exclusions saved '
                f'to {excl_save_path.relative_to(Path.cwd())}]')
            
    # if len(excl_df) > 0:
    #     print(f'e.g.:\n', excl_df.sample(1).text.iloc[0][:800])

    return df, excl_df


def process_slices(slices: list,
                   total: int,
                   data_source_label: str,
                   subset_label: str,
                   excl_df: pd.DataFrame):

    for i, dfslice in enumerate(slices):
        slice_number = i + 1
        out_path = get_conllu_outpath(
            f'{data_source_label}-{slice_number}',
            subset_label)

        excl_df = stanza_parse(dfslice, out_path, excl_df,
                               slice_number, total)

        # save version of dataframe for all texts actually processed
        actual_slice = dfslice[~dfslice.isin(excl_df)]
        actual_slice.to_pickle(
            get_dfpkl_outpath(data_source_label, subset_label,
                              slice_num=slice_number))

    # save exclusions df
    excl_path = get_dfpkl_outpath(
        data_source_label, subset_label, is_excl=True)
    excl_df.to_pickle(excl_path)


### raw processing functions ###
def preprocess_pile_texts(raw_file_path: Path, subcorpora_list: list):

    # pile_data_path = Path('test.jsonl')
    data_source_label = raw_file_path.stem
    # path to save final version of df
    df_output_path = get_dfpkl_outpath(data_source_label,
                                       '-'.join(subcorpora_list))
    # get temporary version of path for unfinished df files
    tmpdfpath = get_dfpkl_outpath(df_output_path.stem, is_tmp=True)
    # raw path set for just this method: dataframes at any stage of pre-processing
    rawdfdir = tmpdfpath.parent.parent.joinpath('raw')
    if not rawdfdir.is_dir():
        rawdfdir.mkdir()
    rawdfpath = rawdfdir.joinpath(tmpdfpath.name)

    # define namedtuple to simplify dataframe creation from json object
    text_info = namedtuple('Text', ['text', 'pile_set_name'])

    # Load the (sample) jsonlines formatted (`.jsonl`) file using `jsonlines`.
    # Create a generator object which directly filters out texts from unwanted data sets.
    # Use pandas to create a flattened dataframe from the generator.
    print('  creating `jsonlines` generator for corpus selection...')
    read_t0 = time.perf_counter()
    with raw_file_path.open(encoding='utf-8-sig', mode='r') as jlf:
        jlines = jsonlines.Reader(jlf).iter()
        texts = (text_info(d['text'], d['meta']['pile_set_name'])
                 for d in jlines if d['meta']['pile_set_name'] in subcorpora_list)
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

    df = df.assign(pile_set_name=df.pile_set_name.astype('category'))

    df.to_pickle(rawdfpath)

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
                        'Pile-CC': 'Pcc',
                        'OpenWebText2': 'OWT2'}
    codes = (subset_abbr_dict[n] for n in df.pile_set_name)
    df = df.assign(pile_set_code=pd.Categorical(codes))
    # save tmp df

    df.to_pickle(rawdfpath)

    print('  adding subset codes & text IDs...')
    # Create text ids from raw file name, pile subset code, and dataframe index.
    codedf = pd.DataFrame()
    codes_t0 = time.perf_counter()
    for code in df.pile_set_code.unique():
        subdf = df.loc[df.pile_set_code == code, :].reset_index()
        prefs = code + '_' + data_source_label + '_'
        idnums = subdf.index.astype('string')
        width = len(str(df.index.max()))
        idnums = idnums.str.zfill(width)
        subdf = subdf.assign(text_id=prefs + idnums)

        codedf = pd.concat([codedf, subdf])
    codes_t1 = time.perf_counter()
    print(f'  ~ {round(codes_t1 - codes_t0, 3)}  sec elapsed')

    df = codedf[['text_id', 'text', 'pile_set_name', 'pile_set_code']]
    df = df.assign(text_id=df.text_id.astype('string'),
                   pile_set_code=df.pile_set_code.astype('category'))

    df.to_pickle(rawdfpath)

    df = clean_df(df, tmpdfpath)

    print('\ndataframe info:')
    print(df.info())
    print('...')

    print('Finished preprocessing: dataframe saved to', df_output_path)
    df.to_pickle(df_output_path)

    return df


def get_dfpkl_outpath(stem: str,
                      subcorpus_label='',
                      slice_num: int = None,
                      is_tmp: bool = False,
                      is_excl: bool = False):
    '''
    return path object for dataframes to be saved as `.pkl.gz`:
    file name template = `pile_[jsonl stem]_[subcorpus]_{df, excl}.pkl.gz`
    * If input is bare or only prefixed (`pile_[jsonl stem]`), 
        `corpus_selection` must be provided
    * all full dataframe file names/stems have 3 underscores
    Directories are as follows:
        - for pre-processing saves,
            `pile_tables/raw/`
        - for unfinalized saves, 
            `pile_tables/tmp/`
        - for df slices unfiltered for exclusions,
            `pile_tables/slices/tmp/`
        - for df slices with exclusions removed, 
            `pile_tables/slices/`
        - for exclusions dataframe, 
            `pile_exclusions/`
    '''

    data_type = 'excl' if is_excl else 'df'

    # to remove any '.pkl' strings still included with [path].stem attributes
    if '.' in set(stem):
        stem = stem.split('.', 1)[0]

    is_bare = False if '_' in stem else True
    is_prefixed = stem.startswith('pile_')
    is_full = stem.count('_') == 3 and is_prefixed

    df_output_dir = (Path.cwd().joinpath('pile_exclusions') if is_excl
                     else Path.cwd().joinpath('pile_tables'))

    # just the jsonl stem, e.g. "00", "val", etc.
    if is_bare:
        # process orig name parts and prefix 'pile_'
        subcorpus_label = ("-".join(subcorpus_label).replace(" ", "")
                           if isinstance(subcorpus_label, list)
                           else subcorpus_label)
        stem = f'pile_{stem}'

    # entire stem of previously created pkl output path;
    # e.g. "pile_00_Pile-CC_df" (".pkl" removed above)
    elif is_full:
        # '.pkl' will not have been included in ext but removed above
        # data_type not inherited from stem in this case because
        #   exclusions input stem might include df if stem Path attribute
        stem, subcorpus_label = stem.rsplit('_', 2)[:2]

    # if not bare and not full, use `stem` and `subcorpus_label` as is;
    # e.g. "pile_00", "pile_val", etc.

    # If path is for dataframe slice
    # Note: need to test for None because `if slice_num` is False when 0
    # This precedes the tmp clause so that tmp slices
    #   are in `slices/tmp/` instead of `tmp/slices/`
    if slice_num is not None:
        df_output_dir = df_output_dir.joinpath('slices')
        stem += f'-{slice_num}'

    # if tmp save (in case of script crash)
    if is_tmp:
        df_output_dir = df_output_dir.joinpath('tmp')

    if not df_output_dir.is_dir():
        df_output_dir.mkdir(parents=True)

    if not subcorpus_label:
        print('WARNING: subcorpus label not provided for output path. Default "Pile-CC" inserted.')
        subcorpus_label = 'Pile-CC'
    return df_output_dir.joinpath(
        f'{stem}_{subcorpus_label}_{data_type}.pkl.gz')


### parsing functions ###
def stanza_parse(df, output_path, excl_df, filenum, total):
    # TODO : change POS to XPOS; remove extra features?

    slice_total = len(df)
    print(f'Starting output {filenum}: {slice_total} of {total} texts')
    # open output file for conll formatted data
    print(f'  parsed data will be written to {output_path}')
    with output_path.open(mode='w') as conlloutput:
        # for each text in the pile subset...
        count = 0
        for doc_num, ix in enumerate(df.index):
            parse_t0 = time.perf_counter()

            text_id = df.at[ix, "text_id"]
            print(f'  {doc_num+1} of {slice_total} '
                  f'in slice {filenum} ({total} total): {text_id}')

            # the text can be parsed with jsloads, it's in json format,
            # which we do not want (and which will break stanza)
            try:
                __ = jsloads(df.text[ix])
            except ValueError:
                pass
            else:
                print(f'    in json format. Added to exclusions.')
                excl_df.append(df.loc[ix, :])

            # create doc (with parsing)
            try:
                doc = nlp(df.text[ix])
            except RuntimeError:
                excl_df.append(df.loc[ix, :])
                print('WARNING! Excluding unparsable text. (runtime error, '
                      'reason unknown). Added to exclusions.')

            else:
                process_sentences(df, conlloutput, ix, doc)
                count += 1

            parse_t1 = time.perf_counter()
            print(f'       ~ {round(parse_t1 - parse_t0, 1)}  seconds')

    print(f'Finished writing parses to {output_path}')
    print(datetime.now().ctime())
    print(f'= {count} of {len(df)} texts successfully parsed.')

    return excl_df


def process_sentences(df, conlloutput, ix, doc):
    # check for line breaks in sentence text string
    print('    - processing sentences...')
    doc = confirm_parse(doc)

    # add comments to sentences (info pulled from dataframe)
    for enumi, s in enumerate(doc.sentences):

        text_id = df.at[ix, 'text_id']
        # text = re.sub(r'\n+|\s{2,}', ' ', s.text)
        # ignore s.id--these will be off if sentences with line breaks were broken up above
        if enumi == 0:
            # "newdoc id" will be the text_id from the pile subset
            s.add_comment(f'# newdoc id = {text_id}')

        # "sent_id" will be doc/text id with _[sentence number] appended
        s.add_comment(f'# sent_id = {text_id}_{enumi}')

        # remove line breaks and duplicated white space characters with single space
        text = remove_breaks(s.text)
        # this adds the full text string to the output file
        s.add_comment(f'# text = {text}')

        # write conll formatted string of doc to output file
    conlloutput.write(doc2conll_text(doc))


def confirm_parse(doc):

    for s in doc.sentences:
        text = s.text.strip()
        # if sentence has line breaks...
        if len(text.split('\n')) > 1:
            # print('\n===> Line breaks found: attempting remediation...')
            ix = doc.sentences.index(s)
            doc.sentences = try_redoc(ix, doc.sentences)
            # print('------------')
    return doc


def remove_breaks(textstr):
    """takes in a sentence string and returns the string with
        new lines and duplicated whitespace characters replaced by ' '. """

    cleantext = solonew_or_dupwhite.sub(r' ', textstr.strip())
    cleantext = extra_newlines.sub('\n\n', cleantext)
    return cleantext


def try_redoc(ix, sent_list):
    """takes in a single sentence string, either reformatted or
        the original text but as a single unit, and attempts to parse it.
        If the model generates a different parse than the existing,
        that will be returned. Otherwise the original is kept.

        Args:
            ix (int): index of original sentence object in existing sentences list
            sent_list (list): existing list of sentence objects

        Returns:
            sent_list (list): list of sentence objects;
            input list with new sentences inserted if any parse changes,
            otherwise with cleaned text replacing original sentence text.
        """

    text = sent_list[ix].text.strip()

    # NOTE: previously, the regex was stronger and caught any case of sentence end punc before \n
    # OR any case of capitals/sentence "starts" after \n.
    # However, this splits up proper nouns that happen to land at a \n into different sentences,
    # so it's weaker now and requires *both*.
    # This is motivated by the fact that better edited sources
    # will have both, and it is better to preserve clean edited materials
    # than trash them in a likely futile attempt to salvage messy data
    # (and messy in wildly varying ways, too) e.g.:
    # not split:
    # [no punctuation]
    # If ImmoNatie would be an object, it would be..An Iphone
    # If ImmoNatie would be a car, it would be..A Mini
    # ---
    # No more jokes about French
    # No more jokes about women
    # CHICKENS ONLY
    # [no approved "start" char]
    # ...
    # 3 star - getting closer but need revisions or a different take on your design
    # 4 star - design is being considered
    # 5 star - made the final cut!
    # [to preserve]:
    # ...shock loss for second seed Tommy
    # Robredo.
    # ---
    # ... the first one will be Duke Nukem
    # Trilogy.
    # ---
    # The latest Batman movie... drove overall
    # Hollywood box office weekend sales of the top 12 titles... .
    # ---
    # Thanks,
    # Meyrav Levine.
    # ---
    # ...opposed the idea as the start of reform process promoted by
    # King Abdullah that they fear will liberalize the stringent system.
    # split:
    # A motion was made by Joseph Marsh and seconded by Jason Forbes to adjourn at 4:44 p.m.
    # Jamison called for a voice vote on that motion and all members voted yes.
    # :\n is treated as a sentence break, whereas midline : is not; e.g.
    # Sentences:
    #   (0) EDIT:
    #   (1) Freedreno is up, performance is on par with existing...
    # Sentences:
    #   (0) NOTE: Apply a light coat of Premium Long Life Grease XG-1-C ...
    if linebreak_is_sent.search(text):
        # print('multiple sentences found:')
        print(f'    original sentence {ix} split into:')
        plausible_sep_text = linebreak_is_sent.sub(r'\1\3\n\n\2\4', text)
        plausible_sep_text = remove_breaks(plausible_sep_text)
        new_sentences = nlp(plausible_sep_text).sentences
        for s in new_sentences:
            print(f'    + {s.text}')
    else:
        # print('    Line breaks removed from sentence text:')
        new_sentences = nlp(remove_breaks(text)).sentences
        # print(f'      {new_sentences[0].text}')

    return sent_list[:ix] + new_sentences + sent_list[ix+1:]


def get_conllu_outpath(slice_name, subset):
    '''returns path for final conllu output files'''

    out_fname = f'{subset.lower()}_eng_{slice_name}.conllu'
    out_dir = Path.cwd().joinpath(f'{subset}.conll')

    if not out_dir.is_dir():
        out_dir.mkdir()

    return out_dir.joinpath(out_fname)


if __name__ == '__main__':
    main()
