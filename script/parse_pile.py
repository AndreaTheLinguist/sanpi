# -*- coding: utf-8 -*-
import argparse
import sys
import time
import zlib
from collections import namedtuple
from datetime import datetime
from json import loads as jsloads
from pathlib import Path
from pprint import pprint

import jsonlines
import pandas as pd
import stanza

# from bs4 import BeautifulSoup
from unidecode import unidecode

from pile_regex_imports import *

doc2conll_text = stanza.utils.conll.CoNLL.doc2conll_text

global_output_limit = 10000
pd.set_option('display.max_colwidth', 80)
global_char_replacement = '<__?UNK__>'
global_subset_abbr_dict = {'Gutenberg (PG-19)': 'PG19',
                           'Books3': 'Bks3',
                           'BookCorpus2': 'BkC2',
                           'Pile-CC': 'Pcc',
                           'OpenWebText2': 'OWT2'}
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
    input_files = args.input_files
    df_files = []
    js_files = get_rawfile_list(args)

    if js_files:
        subcorpora_list = args.corpus_selection
        print('\nraw jsonlines files will be processed for the following subcorpora: ')
        pprint(subcorpora_list)
        print('')

    if input_files:
        df_files = [p.resolve()
                    for p in input_files
                    if p.name.endswith('pkl') or p.stem.endswith('pkl')]
    # won't have both jsonl and pkl.gz files in the same directory
    elif not js_files and args.search_dir:
        print(f'seeking all `.df.pkl` files in {args.search_dir}')
        df_files = [p.resolve() for p in args.search_dir.glob('*pkl.gz')]
    print('Dataframes to be processed:')
    pprint(df_files)

    if df_files:
        presliced_files = [f for f in df_files
                           if 'slices' in (f.parent.name, f.parent.parent.name)]
        fulldf_files = [f for f in df_files if f not in presliced_files]

        for df, data_source_label in process_pickledf(fulldf_files):
            slice_df(df, data_source_label)

        for slice_path in presliced_files:
            print('processing dataframe slice',
                  slice_path.relative_to(Path.cwd()))

            if slice_path.parent.name != 'tmp' or slice_path.parent.parent.joinpath(slice_path.name).is_file():
                print('This slice has already been fully processed. Skipping.\n'
                      '   (To *reprocess*, delete file from `slices/`')
                continue

            process_slice(pd.read_pickle(slice_path))

    if js_files:
        for df, data_source_label in process_raw_jsonlines(js_files, subcorpora_list):
            slice_df(df, data_source_label)


def parse_arg_inputs():

    parser = argparse.ArgumentParser(
        description='script to convert scrambled pile data from raw jsonlines format '
        'into dependency parsed conllu files.'
        'Required packages: stanza, unidecode, and pandas')

    parser.add_argument(
        '-i', '--input_file',
        type=Path, action='append', dest='input_files',
        help='path(s) for input file(s). Can be `.jsonl` or `.pkl(.gz).` '
        'If not specified, script will seek all applicable files '
        'the scope of the calling directory or directory specified with -s flag.')

    parser.add_argument(
        '-s', '--search_dir',
        type=Path, default=Path.cwd(),
        help='Path to search for `jsonl` files. Only relevant if no input files are specified. '
        'Defaults to calling directory.')

    parser.add_argument(
        '-n', '--pile_set_name',
        default=['Pile-CC'],
        type=str, action='append', dest='corpus_selection',
        help=('option to select alternate pile set(s). Default selection: "Pile-CC".'
              ' Flag can be reused: '
              'All flagged paths will be appended to selection list'))

    # parser.add_argument(
    #     '-f', '--jsonl_file_path',
    #     type=Path, action='append', dest='jsonl_files',
    #     help=('OLD: flag to point to raw pile jsonlines file path to parse. Flag can be reused: '
    #           'All flagged paths will be appended to file list. If no file or dataframe '
    #           '(below) flags are included, '
    #           'all .jsonl data files will be run.'))

    # parser.add_argument(
    #     '-d', '--dataframe',
    #     type=Path, action='append', dest='df_files',
    #     help=('OLD: If a pickle/.pkl(.gz) of the processed dataframe already exists from a previous run '
    #           '(saved in `[cwd]/pile_tables/`), use this '
    #           'option to specify its path and skip the first step of the script. This flag can be reused: '
    #           'all specified paths will be appended to `df_files`. *NOTE*: -f and -d flags can be run together,'
    #           'so make sure they are not redundant!'))

    return parser.parse_args()


def get_rawfile_list(args):
    inputs = args.input_files
    search_dir = args.search_dir
    print('+ raw files selected to process:')
    jsonl_list = []

    if inputs:
        jsonl_list = [i.resolve()
                      for i in inputs if i.name.endswith('jsonl')]
    # if args.jsonl_files:
    #     files_list = [f.resolve() for f in args.jsonl_files]
    # # only do a glob search of directory if no pkl files given
    # elif not args.df_files:
    #     files_list = list(Path.cwd().glob('**/*jsonl'))
    #     # note: can't print files_iter here bc it's a generator obj
    elif search_dir.is_dir():
        print('seeking all `.jsonl` files in', search_dir)
        jsonl_list = list(search_dir.glob('**/*jsonl'))

    else:
        sys.exit(
            'Error: No input files or valid search directory specified. See --help for more info.')

    if jsonl_list:
        pprint(jsonl_list)
    else:
        print('[no raw data files to be processed]')
    return jsonl_list


def process_pickledf(dfiles):

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
        print('finalized dataframe?')

        if dfpath.parent.name in ('tmp', 'raw'):
            print(f'  no -> Cleaning {dfpath.name}...')
            tmpdfpath = (get_dfpkl_outpath(dfpath.stem, is_tmp=True)
                         if dfpath.parent.name == 'raw'
                         else dfpath)
            df = clean_df(df, tmpdfpath)
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


def clean_df(orig_df, tmp_save_path):

    print('\nCleaning text in dataframe...')
    if any(orig_df.text_id.str.startswith(('PiCC', 'Pcc'))):

        orig_df = orig_df.assign(
            text_id=orig_df.text_id.str.replace('PiCC', 'pcc')
            .str.lower().astype('category'))

    if 'text' not in orig_df.columns:
        orig_df = orig_df.assign(text=orig_df.raw)

    # moved this here from preprocessing method because translating encoding belongs in cleanup
    # doing it before `pull_exclusions()` because texts with errors will be excluded
    print('  translating encoding...')
    unidecode_t0 = time.perf_counter()
    df = orig_df.assign(
        text=orig_df.text.apply(
            lambda t: unidecode(t, errors='replace',
                                replace_str=global_char_replacement))
    )
    unidecode_t1 = time.perf_counter()
    print(
        f'  ~ {round(unidecode_t1 - unidecode_t0, 2)}  sec elapsed')

    # removing urls before pulling exclusions so that "variable" and "id" patterns
    #   will not throw out texts simply due to urls that would have been removed
    print('  removing URLs...')
    t0 = time.perf_counter()
    df = df.assign(text=df.text.apply(
        lambda t: bracket_url.sub(r'\1', t)))
    df = df.assign(text=df.text.apply(lambda t: likely_url.sub(r' ', t)))
    t1 = time.perf_counter()
    print(f'  ~ {round(t1 - t0, 2)}  sec elapsed')

    df.to_pickle(tmp_save_path)
    print(f'dataframe saved to {tmp_save_path.relative_to(Path.cwd())}')

    print('+ Excluding messy data...')
    excl_save_path = get_dfpkl_outpath(tmp_save_path.stem, is_excl=True)
    df, excl_df = pull_exclusions(orig_df, excl_save_path)

    df.to_pickle(tmp_save_path)

    df = df.assign(text=df.text.astype('string'),
                   raw=df.raw.astype('string'))

    # Andrea Hummel on Feb 11, 2022 at 7:14 PM
    # This was an attempt at fixing exclusions, if the offenses were minor. However,
    # this is not consistent with the new approach of excluding texts that "*might* be
    # problems" because they might cause **problems**. I.e. the point of pulling
    # anything that might be messy or hard to parse text is so that those can be
    # safely ignored for now while the *easier* stuff gets processed. Any fixing needs
    # to be tabled, perhaps indefinitely.
    #
    # Keeping the `recheck` parameter and code in `pull_exclusions()` for now, but it
    # will not be reached ever (i.e. is not called as a recheck)
    #
    # if not excl_df.empty:
    #     clean_excl = excl_df.assign(
    #         text=excl_df.text.apply(lambda t: bracket_url.sub(r'\1', t)))
    #     clean_excl = clean_excl.assign(
    #         text=clean_excl.text.apply(lambda t: likely_url.sub('', t)))
    #     clean_excl = clean_excl.assign(
    #         text=clean_excl.text.apply(
    #             lambda t: punc_only.sub(r'\1\2\3\4\5\6\7\n\n', t)))
    #     restore_to_df, still_excl_df = pull_exclusions(
    #         clean_excl, excl_save_path, recheck=True)
    #     # if any previous exclusions were not caught after cleaning attempts
    #     # restore them to the main dataframe,
    #     # and overwrite the saved exclusions file with only those remaining
    #     if not restore_to_df.empty:
    #         df.loc[restore_to_df.index.to_list(), :] = restore_to_df
    #         still_excl_df.to_pickle(excl_save_path)

    # clean up internet syntax quirks
    print('+ Cleaning up text...\n   - punctuation delineated text breaks')
    df = df.assign(text=df.text.apply(
        lambda t: punc_only.sub(r'\1\2\3\4\5\6\7\n\n', t)))

    # print('   - @ and # tagging...')
    # df = df.assign(text=df.text.apply(
    #     lambda t: re.sub(r'\@\w+(\s)', r' \<\@tag \1\>', t)))
    # df = df.assign(text=df.text.apply(
    #     lambda t: re.sub(r'\#(\w+\s)', r' \<\#tag \1\>', t)))
    print('   - title abbreviations at line breaks...')
    df = df.assign(
        text=df.text.apply(lambda t: end_of_line_abbr.sub(r'\1\2\5\6 \3\4', t)))

    text_diff = ~df.text.isin(df.raw)
    if any(text_diff):
        changedf = df.loc[text_diff, :]
        print(f'{len(changedf)} of {len(df)} texts modified')

    df.loc[:, ['text', 'raw']] = df[['text', 'raw']].astype('string')
    return df


def pull_exclusions(df: pd.DataFrame,
                    excl_save_path: Path,
                    recheck: bool = False):

    print('  pulling excluded formats...')
    excl_df = pd.DataFrame()
    loaded_from_file = False
    found_exclusions = False
    prev_excl_count = 0
    if excl_save_path.is_file() and not recheck:
        loaded_from_file = True
        prev_excl = pd.read_pickle(excl_save_path)
        if 'raw' not in prev_excl.columns:
            excl_df = prev_excl.assign(raw=prev_excl.text,
                                       excl_type=None)
        else:
            excl_df = prev_excl.assign(excl_type=None)

        df = df.loc[~df.text_id.isin(excl_df.text_id)]
        prev_excl_count = len(excl_df)
        print(f'  -> {prev_excl_count} previously '
              'identified exclusions loaded from file')
    else:
        print('[No previous exclusion assessment found.]')

    # uninterpretable/unknown characters (could not be decoded)
    print('  looking for uninterpretable characters...')
    t0 = time.perf_counter()
    cannot_interpret = df.text.str.contains(global_char_replacement)
    if any(cannot_interpret):
        found_exclusions = True
        unkchardf = df.loc[cannot_interpret, :].assign(excl_type='?unk')
        print(f'   +{len(unkchardf)} exclusions')
        excl_df = pd.concat([excl_df, unkchardf])
        df = df.loc[~cannot_interpret, :]
    t1 = time.perf_counter()
    print(f'= ?unk char excl ~~ {round(t1-t0, 2)} seconds')

    # wikitext
    t0 = time.perf_counter()
    df, wiki_df = exclude_wikitexts(df)
    if not wiki_df.empty:
        found_exclusions = True
        wiki_df = wiki_df.assign(excl_type='wiki')
        excl_df = pd.concat([excl_df, wiki_df])
    t1 = time.perf_counter()
    print(f'= wiki excl ~~ {round(t1-t0, 2)} seconds')

    # html source code
    t0 = time.perf_counter()
    df, html_df = exclude_html(df)
    if not html_df.empty:
        found_exclusions = True
        html_df = html_df.assign(excl_type='html')
        excl_df = pd.concat([excl_df, html_df])
    t1 = time.perf_counter()
    print(f'= html excl ~~ {round(t1-t0, 2)} seconds')

    # flag texts that contain technical seeming strings and exclude for now
    print('  looking for other messy text...')
    # likely_source_code = df.text.apply(
    #     lambda t: bool(len(variable_regex.findall(t)) > 15
    #                    or possible_code.search(t)))

    # has_embedded_ids = df.text.apply(
    #     lambda t: bool(len(likely_idtag.findall(t)) > 5))

    # likely_hard_parsing = likely_source_code | has_embedded_ids

    df, excl_df, found_exclusions = exclude_regex(
        df, excl_df, found_exclusions)

    # is_json = df.text.apply(lambda t: bool(json_pat.search(t)))
    # if any(is_json):
    #     found_exclusions = True
    #     new_excl = df.loc[is_json, :]
    #     new_excl = new_excl.assign(excl_type='json')
    #     print(f'   +{len(new_excl)} exclusions')
    #     excl_df = pd.concat([excl_df, new_excl])
    #     df = df.loc[~df.text_id.isin(excl_df.text_id), :]

    # currently unreachable (no calls of function as recheck)
    if recheck:
        if not found_exclusions:
            print('all previously flagged exclusions have been fixed by simple cleanup')
        elif len(excl_df) < len(df):
            print('some excluded texts have been fixed by simple cleanup')
        else:
            print('all prev exclusions remain')

    else:
        # only save if (new) texts were marked as exclusions
        if found_exclusions:
            excl_df.to_pickle(excl_save_path)
            print(f'  = {len(excl_df)} exclusions '
                  f'({len(excl_df) - prev_excl_count} new) saved to '
                  f'{excl_save_path.relative_to(Path.cwd())}')

        elif loaded_from_file:
            print('  = No additional exclusions found.')

        else:
            excl_df.to_pickle(excl_save_path)
            print('  = No exclusions found.')
        # if len(excl_df) > 0:
        #     print(f'e.g.:\n', excl_df.sample(1).text.iloc[0][:800])

    return df, excl_df


def exclude_regex(df, excl_df, found_excl):

    pattern_type_dict = {
        'json': json_regex,
        'code': code_regex,
        '_wrd': underscore_regex,
        'a0wrd': mixed_letter_digit_regex,
    }

    for excl_type_str, excl_regex in pattern_type_dict.items():
        t0 = time.perf_counter()
        excl_boolean = df.text.apply(lambda t: bool(excl_regex.search(t)))
        if any(excl_boolean):
            found_excl = True
            new_excl = df.loc[excl_boolean, :]
            new_excl = new_excl.assign(excl_type=excl_type_str)
            print(f'   +{len(new_excl)} {excl_type_str} exclusions')
            excl_df = pd.concat([excl_df, new_excl])
            df = df.loc[~df.text_id.isin(excl_df.text_id), :]
        t1 = time.perf_counter()
        print(f'= {excl_type_str} filtering ~~ {round(t1-t0, 2)} seconds')

    return df, excl_df, found_excl


def exclude_wikitexts(df):
    print('  looking for wikitext/wikimedia formatting...')
    wikidf = pd.DataFrame()

    is_wiki = df.text.apply(lambda t: bool(defwiki.search(t)))
    if any(is_wiki):
        wikidf = pd.concat([wikidf, df.loc[is_wiki, :]])
        df = df.loc[~is_wiki, :]

    maybe_wiki = (df.text.apply(lambda t: bool(wikipat.search(t))))
    if any(maybe_wiki):
        wikidf = pd.concat([wikidf, df.loc[maybe_wiki, :]])
        df = df.loc[~maybe_wiki, :]

    print(f'   +{len(wikidf)} exclusions')
    return df, wikidf


def exclude_html(df):
    print('  looking for any html...')
    html_df = pd.DataFrame()
    is_html = df.text.apply(
        lambda t: bool(
            likely_html.search(t)
            # BeautifulSoup(t, "html.parser").find()
        ))

    if any(is_html):

        html_df = df.loc[is_html, :]
        df = df.loc[~is_html, :]

        # html_text = htmldf.text.apply(
        #     lambda t:
        #     BeautifulSoup(t, "html.parser").get_text()).astype('string')
        # htmldf = htmldf.assign(text=html_text)
        # if any(htmldf.text.isna()):
        #     htmldf.loc[htmldf.text.isna(), 'text']

        # df.loc[is_html, ['raw', 'text']] = (htmldf.loc[:, ['raw', 'text']]
        #                                     .astype('string'))
        # df.to_pickle(tmp_save_path)

    print(f'   +{len(html_df)} exclusions')
    return df, html_df


def slice_df(full_df, data_source_label):

    for subcorpus_code, df in full_df.groupby('pile_set_code'):
        subcorpus_name = df.pile_set_name.iat[0]
        print(f'Partitioning data in {subcorpus_name} subset')

        # Andrea Hummel on Feb 11, 2022 at 9:13 PM
        # Currently, `excl_df` is not passed into this method. Instead of
        # getting it via a redundant call to `pull_exclusions()`
        # (that happens in `clean_df()` now) it is loaded from where it
        # was saved either in the previous call, or in a previous run
        # of the script.
        # If for some reason the exclusions file cannot be found, run again.
        #    (but save with different name so as to not overwrite original.)
        excl_save_path = get_dfpkl_outpath(data_source_label,
                                           subcorpus_name, is_excl=True)

        if excl_save_path.is_file():
            excl_df = pd.read_pickle(excl_save_path)
        else:
            backup_path = excl_save_path.with_name(excl_save_path.name
                                                   .split('.', 1)[0]+'-slicing.pkl.gz')
            if backup_path.is_file():
                excl_df = pd.read_pickle(backup_path)
            else:
                print('Warning: previous exclusions file could not be found. '
                      'Reassessing data...')
                df, excl_df = pull_exclusions(df, backup_path)

            print('Excluded data alternate:',
                  backup_path.relative_to(Path.cwd()))

        print(f'{len(df)} total texts to parse')

        remaining_df = df.sort_values('text_id')
        slices = []
        # e.g. if limit were 1000:
        # slice off 1000 rows at a time until total is 2400 or less
        while len(remaining_df) > int(2.4*global_output_limit):

            dfslice = remaining_df.iloc[:global_output_limit, :].reset_index()
            remaining_df = remaining_df.iloc[global_output_limit:, :]
            slices.append(dfslice)
        # if 2400 split remaining: 2 slices of 1200
        # if 1202, split remaining: 2 slices of 610
        # if remaining df is 1200 rows or less:
        #   keep as is (no more slicing)
        if len(remaining_df) > 1.2*global_output_limit:

            half_remaining = int(len(remaining_df)/2)

            dfslice_penult = remaining_df.iloc[:half_remaining, :]
            slices.append(dfslice_penult)

            remaining_df = remaining_df.iloc[half_remaining:, :]

        # this must be outdented to catch smaller dataframes
        slices.append(remaining_df)
        slices_total_str = str(len(slices))
        # Andrea Hummel on Feb 3, 2022 at 4:45 PM
        # Note that this first save of the dataframe slices is *after* `pull_exclusions()`
        # is called, so to get the full set of texts covered in the full dataframe, need
        # to look at the union of the slices _and_ the corresponding exclusions dataframe.
        for i, sdf in enumerate(slices):
            # starting at i = 0 meant the first slice wasn't
            # getting saved bc if slice_num was evaluating as False
            slice_num = i+1
            slice_zfilled = str(slice_num).zfill(len(str(len(slices))))
            sdf = create_ids(sdf, zfilled_slice_num=slice_zfilled)
            print(f'slice {slice_num}: ({len(sdf)} texts)\n  {sdf.text_id.iloc[0]}'
                  f'\n  ...\n  {sdf.text_id.iloc[-1]}')
            outpath = get_dfpkl_outpath(
                data_source_label, subcorpus_code,
                slice_num=slice_num, is_tmp=True)
            sdf.to_pickle(outpath)

        # this needs to be its own loop so that all the slices can be saved
        # before any of them are processed
        # (which takes a long time and has a high likelihood of crashing)
        for sdf in slices:
            process_slice(sdf, slices_total_str)


def process_slice(dfslice: pd.DataFrame, slices_total_str: str = '?'):
    id_prototype = dfslice.text_id.iloc[0]
    subset_label, __, data_source_label, slice_id, __ = id_prototype.split('_')
    slice_number, __ = slice_id.split('.')
    subset_label = subset_label.capitalize()

    excl_path = get_dfpkl_outpath(
        data_source_label, subset_label, is_excl=True)
    excl_df = pd.read_pickle(excl_path)

    out_path = get_conllu_outpath(
        f'{data_source_label}-{slice_number}',
        subset_label)

    excl_df = stanza_parse(dfslice, out_path, excl_df,
                           slice_number, slices_total_str)

    # save version of dataframe for all texts actually processed
    actual_slice = dfslice[~dfslice.isin(excl_df)]
    actual_slice.to_pickle(
        get_dfpkl_outpath(data_source_label, subset_label,
                          slice_num=slice_number))

    # save exclusions df

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
    text_info = namedtuple('Text', ['raw', 'pile_set_name'])

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
        print('  building dataframe from `jsonlines` generator object...')
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
    df = df.drop_duplicates(subset='raw').reset_index(drop=True)

    df = df.assign(pile_set_name=df.pile_set_name.astype('category'))

    # Create codes for data subsets
    # (code dict is now a global variable)
    codes = (global_subset_abbr_dict[n] for n in df.pile_set_name)
    df = df.assign(pile_set_code=pd.Categorical(codes))
    # save tmp df
    df.to_pickle(rawdfpath)

    print('  adding subset codes & text IDs...')
    codedf = create_ids(df, data_source_label=data_source_label)

    df = codedf[['text_id', 'raw', 'pile_set_name', 'pile_set_code']]
    df = df.assign(text_id=df.text_id.astype('string'),
                   pile_set_code=df.pile_set_code.astype('category'))

    df.to_pickle(rawdfpath)
    print(f'raw dataframe saved to {rawdfpath.relative_to(Path.cwd())}')

    df = clean_df(df, tmpdfpath)

    # print('\ndataframe info:')
    # print(df.info())
    # print('...')
    # raw column will no longer be saved to finalized dataframe output
    # dataframes in `raw/` will have only `raw`
    # dataframes in `tmp/` will have both `raw` and `text`
    # dataframes in the parent dir, `pile_tables` will have only `text`
    df.pop('raw')
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
    is_prefixed = bool(stem.count('_')) or stem.startswith('pile_')
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

    if subcorpus_label in [v for v in global_subset_abbr_dict.values()]:
        subcorpus_label = [k
                           for k, v in global_subset_abbr_dict.items()
                           if v == subcorpus_label][0]

    elif not subcorpus_label:
        print('WARNING: subcorpus label not provided for output path. '
              'Default "Pile-CC" inserted.')
        subcorpus_label = 'Pile-CC'

    return df_output_dir.joinpath(
        f'{stem}_{subcorpus_label}_{data_type}.pkl.gz')


def create_ids(df: pd.DataFrame, data_source_label: str = None, zfilled_slice_num: str = None):
    # Create text ids from raw file name, pile subset code, and dataframe index.
    codedf = pd.DataFrame()
    codes_t0 = time.perf_counter()
    fullix = bool(data_source_label)
    sliceix = bool(zfilled_slice_num)
    for code in df.pile_set_code.unique():
        subdf = df.loc[df.pile_set_code == code, :].reset_index()
        code = code.lower()
        prefix = ''

        if fullix:
            prefix = f'{code}_{data_source_label}_'
        elif sliceix:
            subdf = subdf.assign(orig_text_id=subdf.text_id)
            __, file_label, __ = subdf.orig_text_id.iloc[0].split(
                '_')
            prefix = f'{code}_eng_{file_label}_{zfilled_slice_num}.'
            # then add... '{slice_ix.zfill}-{jsonl_ix}

        # start at 1 instead of 0
        idnums = subdf.index + 1
        zfill_len = len(str(df.index.max()))
        idnums = idnums.astype('string').str.zfill(zfill_len)

        subdf = subdf.assign(id_stem=prefix + idnums)
        if sliceix:
            subdf = subdf.assign(
                text_id=(subdf.id_stem + '_x'
                         + subdf.text_id.str.rsplit('_', 1).str.get(1)))
        else:
            subdf = subdf.assign(text_id=subdf.id_stem)

        subdf.pop('id_stem')
        codedf = pd.concat([codedf, subdf])
    codes_t1 = time.perf_counter()
    print(f'  ~ {round(codes_t1 - codes_t0, 3)}  sec elapsed')

    return codedf

### parsing functions ###


def stanza_parse(df, output_path, excl_df, filenum, total: str):
    # TODO : change POS to XPOS; remove extra features?

    slice_total = len(df)
    print(
        f'Starting output {filenum} of {total}: {slice_total} texts in current slice')
    # open output file for conll formatted data
    print(f'  parsed data will be written to {output_path}')
    with output_path.open(mode='w') as conlloutput:
        # for each text in the pile subset...
        successes = 0
        for position_in_slice, ix in enumerate(df.index):
            # `position_in_slice` should only be used for ordinal/counting
            parse_t0 = time.perf_counter()
            row_df = df.loc[[ix], :]

            text_id = row_df.text_id.squeeze()
            print(f'  {position_in_slice+1} of {slice_total} '
                  f'in slice {filenum} (of {total}): {text_id}')

            textstr = row_df.text.squeeze()

            # the text can be parsed with jsloads, it's in json format,
            # which we do not want (and which will break stanza)
            try:
                __ = jsloads(textstr)
            except ValueError:
                pass
            else:
                print(f'    in json format. Added to exclusions.')
                excl_df = pd.concat([excl_df, row_df])

            # create doc (with parsing)
            try:
                doc = nlp(textstr)
            except RuntimeError:
                excl_df = pd.concat([excl_df, row_df])
                print('WARNING! Excluding unparsable text. (runtime error, '
                      'reason unknown). Added to exclusions.')

            else:
                process_sentences(row_df, conlloutput, doc)
                successes += 1

            parse_t1 = time.perf_counter()
            print(f'       ~ {round(parse_t1 - parse_t0, 1)}  seconds')

    print(f'Finished writing parses to {output_path}')
    print(datetime.now().ctime())
    print(f'= {successes} of {len(df)} texts successfully parsed.')

    return excl_df


def process_sentences(row_df, conlloutput, doc):

    print('    - processing sentences...')
    text_id = row_df.text_id.squeeze()

    # check for line breaks in sentence text string
    doc = confirm_parse(doc)
    sent_zfill = len(str(len(doc.sentences)))
    # add comments to sentences (info pulled from dataframe)
    for enumi, sentence in enumerate(doc.sentences):
        enumi += 1
        # ignore s.id--these will be off if sentences with line breaks were broken up above
        if enumi == 1:
            # "newdoc id" will be the text_id from the pile subset
            sentence.add_comment(f'# newdoc id = {text_id}')

        # "sent_id" will be doc/text id with _[sentence number] appended
        # TODO : change this to `enumi + 1` for consistency with other conllu files

        sent_id = f'{text_id}_{str(enumi).zfill(sent_zfill)}'
        sentence.add_comment(f'# sent_id = {sent_id}')
        print('     ', sent_id)

        # remove line breaks and duplicated white space characters with single space
        text = remove_breaks(sentence.text)
        # this adds the full text string to the output file
        sentence.add_comment(f'# text = {text}')

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
    subset = global_subset_abbr_dict.get(subset, subset)
    out_fname = f'{subset.lower()}_eng_{slice_name}.conllu'
    out_dir = Path.cwd().joinpath(f'{subset}.conll')

    if not out_dir.is_dir():
        out_dir.mkdir()

    return out_dir.joinpath(out_fname)


if __name__ == '__main__':
    main()
