import pyconll
from collections import namedtuple

# temp for devel/debug
import sys


def simpleReadConllu(file):

    # save generator object for iterating over conllu file
    conlluReader = pyconll.load.iter_from_file(file)

    # define named tuples for documents and sentences
    doc_form = namedtuple('document', ['id', 'sentences'])
    sent_form = namedtuple('sentence', ['id', 'text', 'doc_id', 'line_number'])

    basic_info = []
    sent_list = []
    for entry in conlluReader:

        sent_id = entry.id
        doc_id, index_in_doc = sent_id.rsplit('_', 1)

        sentence = sent_form(sent_id, entry.text, doc_id, index_in_doc)

        # if sentence list is nonempty and doc id is new
        # save previous doc's sent_list to basic_info list as named tuple
        # then restart sentence list
        if bool(sent_list) and doc_id != sent_list[-1].doc_id:

            # check all sentences in current sent_list are all same doc
            if len(set([s.doc_id for s in sent_list])) != 1:

                print('Warning!!! No unique document in grouping.')

            prev_doc = sent_list[0].doc_id

            # save prev doc's sentences
            basic_info.append(doc_form(prev_doc, sent_list))
            print(f'{prev_doc} processing complete...')

            # clear list before adding new sentence
            sent_list = []

        sent_list.append(sentence)

    # save final doc to basic_info
    final_doc = sent_list[0].doc_id
    basic_info.append(doc_form(final_doc, sent_list))
    print(f'{final_doc} processing complete...')
    print('\nProcessing Complete.')

    # list of namedtuples containing another list of named tuples
    return basic_info


# for debugging
simpleReadConllu(sys.argv[1])
