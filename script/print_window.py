"""This script searches the given corpus directory for the given 
    string. Medial words may be replaced with "_" as a wildcard, 
    but the first and last word in the string must be defined. 
    
    Console output includes matching words, their pos, and dependency 
    relations, as well a "window" of the given token. The window size
    can be controlled via optional arguments. 

    Arguments: 
        [corpus directory] [search string] ([number of preceding words] [number of following words])

    Returns:
        standard output only (but can be saved to file using > command)
    """

from sys import argv
from pathlib import Path
import pyconll

# args: corpus file path to look in, string to look for, (words before, words after)
corpusPath = Path(argv[1])
sought = argv[2]

try:
    words_before = int(argv[3])
except IndexError:
    words_before = 5

try:
    words_after = int(argv[4])
except IndexError:
    words_after = 5

print('')


def get_window(s):

    tokens = s._tokens
    words = [t.form for t in tokens]
    targets = sought.split(' ')
    beg_targ = targets[0]
    end_targ = targets[-1]
    defined = [t for t in targets if t != '_']
    indices = [words.index(x) for x in defined if x in words]
    if (not indices
            or max(indices) - min(indices) != len(targets) - 1):
        return

    # if words.count(beg_targ) == 1 and words.count(end_targ) == 1:
    #     center_1 = words.index(beg_targ)
    #     center_2 = words.index(end_targ)

    # else:
    center_1 = center_2 = None
    for i, w in enumerate(words):
        projected_end = i + len(targets) - 1
        if w == beg_targ and words[projected_end] == end_targ:
            center_1 = i
            center_2 = projected_end
            break

    if not (center_1 and center_2):
        return

    info_list = []
    heads = []

    for center_ix in range(center_1, center_2+1):

        center_token = tokens[center_ix]
        if set('`~!#$%^&*()=,./;<>:"[]\'}{').intersection(center_token.lemma):
            return

        try:
            head_ix = s._ids_to_indexes[center_token.head]

        except KeyError:

            if not int(center_token.head):
                head_ix = 0
                head_form = '_'
                head_pos = 'n/a'

            else:
                print('head could not be found')
                return

        else:
            head = tokens[head_ix]
            head_form = head.form
            head_pos = head.xpos

        info_str = (f'"{center_token.form}" {center_token.xpos}\t'
                    f'-[{center_token.deprel}]->\t"{head_form}" {head_pos}')

        info_list.append(info_str)
        heads.append(head_ix)

    start_ix = min(min(heads), center_1 - words_before)
    end_ix = max(max(heads), center_2 + words_after + 1)

    if min(heads) < start_ix:
        start_ix = min(heads)

    if end_ix < max(heads):
        end_ix = max(heads) + 1

    window = (' '.join(words[start_ix:center_1])
              + ' _ '
              + ' '.join(words[center_1:center_2+1])
              + ' _ '
              + ' '.join(words[center_2+1:end_ix]))
    if not window.endswith('.'):
        window = f'{window}...'

    if len(targets) > 1 and len(set(heads)) == 1:
        info_list.append(f'+ targets have same head: {head_form}')
    info = '\n'.join(info_list)

    return f'{info}\n...{window}'


def process_file(corpus):

    for sentence in pyconll.iter_from_file(corpus):
        window_str = get_window(sentence)
        if not window_str:
            continue
        print(window_str)
        print(f'   >> {sentence.id}')
        print('')


for corpus in corpusPath.iterdir():
    print(f'searching {corpus}...')
    process_file(corpus._str)
