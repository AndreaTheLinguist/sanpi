#!/usr/bin/env python3

import csv
import argparse
import re
import os
from collections import namedtuple
from pathlib import Path


def __main__():

    args = parse_args()
    mask_code = args.masked_element
    input_file = args.input_file_path
    fstem = input_file.stem

    output_dir = Path(input_file.parts[0] + '/masked/'
                      if not args.output_dir
                      else args.output_dir)

    output_filepath = output_dir / f'{fstem}_masked_{mask_code}.csv'

    try:
        os.mkdir(output_dir)

    except OSError:
        pass

    data = []

    if mask_code == 'both':

        with open(input_file, 'r') as f1:

            data = add_masks('predicate', csv.DictReader(f1), data)

        with open(input_file, 'r') as f2:

            data = add_masks('modifier', csv.DictReader(f2), data)

    else:

        with open(input_file, 'r') as f:

            data = add_masks(mask_code, csv.DictReader(f), data)

    with open(output_filepath, 'w') as out:

        data_writer = csv.writer(out)

        data_writer.writerow(
            ('sentences', 'mask_type', 'pred_pos', 'scale_type'))
        data_writer.writerows(data)


def add_masks(mask_type, data_reader, data):
    # input = str, sentence(s) with [MASK]
    # mask_type = str, modifier or predicate
    # pred_pos = str, predicate part of speech: adj, noun, verb
    # scale_type = str, absolute, relative, quantifier?
    # test_type = str, default (single sentece), mask first, mask second
    # negated_mask = bool, is MASK position under scope of negation?
    # str_before_mask = str, what precedes mask, e.g. 'not extremely happy. slightly'
    # str_after_mask = str, what follows mask, e.g. 'sad but not happy'
    # prev_vp = None if mask first, else (<>_n) (<>_m) <>_p of preceding sentence
    # next_vp = None if mask second, else (<>_n) (<>_m) <>_p of following sentence
    # mask_vp = str, (<>_n) _ <>_p or (<>_n) (<>_m) _
    # sent1_comp = bool, is sent1 a composite/conjoined sentence (has 'but')
    # sent2_comp = bool, is sent2 a composite/conjoined sentence (has 'but')
    data_tuple = namedtuple(
        'test_input',
        ['input', 'mask_type', 'pred_pos', 'scale_type', 'test_type',
         'negated_mask', 'str_before_mask', 'str_after_mask',
         'prev_vp', 'next_vp', 'mask_vp', 'sent1_comp', 'sent2_comp'])

    mask_str = '[MASK]'

    mask_tag_pattern = re.compile(r"_[pmn]")
    neg_tag = re.compile(r"_n")
    mod_tag = re.compile(r"_m")
    pred_tag = re.compile(r"_p")
    mask_pattern = re.compile(r"\w+_[pmn]")
    mask_sent_pattern = re.compile(r"[^\.]*[MASK][^\.]*\.")

    for entry in data_reader:

        recorded_sent = [d[0] for d in data]

        (sents, pos, sctype) = entry.values()

        new = sents.replace(' n\'t', 'n\'t')

        # should not happen, but just in case...
        if '_' not in new:
            continue

        sent1, sent2 = sents.split('.', 1)

        sent1neg = neg_tag.search(sent1)
        sent2neg = neg_tag.search(sent2)

        sent1modified = mod_tag.search(sent1)
        sent2modified = mod_tag.search(sent2)

        sent1comp = bool(re.search(r"but ", sent1))
        sent2comp = bool(re.search(r"but ", sent2))

        preds = re.findall(r"\w+_p", sents)

        mods = re.findall(r"\w+_m", sents)

        tags = mask_pattern.findall(new)

        if mask_type != 'predicate':

            new = new.replace('_p', '')

        if mask_type != 'modifier':

            new = new.replace('_m', '')

        tokens = preds if mask_type == 'predicate' else mods

        for i, token in enumerate(tokens):

            # first
            if i == 0:

                alt = new.replace(token, mask_str, 1)

            else:

                alt = new.replace(token, '', 1)
                alt = mask_tag_pattern.sub('', new, count=i)
                alt = alt.replace(token, mask_str, 1)

            alt = mask_tag_pattern.sub('', alt)
            alt_retagged = retag(alt, sents, mask_str)

            mask_sentence = mask_sent_pattern.findall(alt)[0]

            # sentences = [sent for sent in new.split('.')]
            # mask_sentence_list = list(filter(mask_str.search, sentences))
            # mask_sentence = mask_sentence_list[0].strip() + '.'
            alt_sents_split = alt.split('.', 1)

            test_type = ('mask first' if mask_str in alt_sents_split[0]
                         else 'mask second')

            neg_mask = ((test_type == 'mask first' and sent1neg)
                        or (test_type == 'mask second' and sent2neg))

            if alt not in recorded_sent:

                sent1comp = 'but ' in alt_sents_split[0]
                sent2comp = 'but ' in alt_sents_split[1]

                before, after = alt.split(mask_str)

                alt_retagged_s1, alt_retagged_s2 = alt_retagged.split('.', 1)

                first_vp = ' '.join([w for w
                                     in alt_retagged_s1.split(' ')
                                     if mask_pattern.search(w)
                                     or w in ('but', mask_str)])

                second_vp = ' '.join([w for w
                                      in alt_retagged_s2.split(' ')
                                      if mask_pattern.search(w)
                                      or w in ('but', mask_str)])

                if test_type == 'mask first':
                    prev_vp = None
                    next_vp = second_vp
                    mask_vp = first_vp

                elif test_type == 'mask second':
                    prev_vp = first_vp
                    next_vp = None
                    mask_vp = second_vp

                data.append(data_tuple(alt, mask_type,
                                       pos, sctype, test_type, neg_mask, before, after, prev_vp, next_vp, mask_vp, sent1comp, sent2comp))

            if mask_sentence not in recorded_sent:

                before, after = mask_sentence.split(mask_str)

                mask_retagged = mask_sent_pattern.findall(alt_retagged)

                vp = ' '.join([w for w
                               in mask_retagged.split(' ')
                               if mask_pattern.search(w)
                               or w in ('but', mask_str)])
                comp = 'but' in mask_sentence

                data.append(data_tuple(mask_sentence, mask_type, pos, sctype,
                                       'default', neg_mask, before, after, '', '', vp, comp, ''))

    return data


def retag(alt, sents, mask_str):

    alt_words_retagged = []
    zipped = zip(alt.split(' '), sents.split(' '))
    for word_pair in zipped:

        if word_pair[0] == word_pair[1]:
            w = word_pair[0]

        elif mask_str in word_pair[0]:
            w = word_pair[0]

        else:
            w = word_pair[1]

        alt_words_retagged.append(w)

    return ' '.join(alt_words_retagged)


def parse_args():

    parser = argparse.ArgumentParser(
        description='script to apply [MASK] over desired tokens. Takes in CSV file and outputs new file in masked/ directory in same same directory as the original file.')

    parser.add_argument('input_file_path', type=Path,
                        help='path of csv file containing tagged sentences to apply masks to')

    parser.add_argument('masked_element', type=str,
                        choices=['modifier', 'predicate', 'both'], help='choice of which item type to mask in each data point. Choices are: modifier, predicate, negation.')

    parser.add_argument('-o', '--output_dir', type=Path,
                        help='optional argument to specify different directory for output. Output directory will default to location of input file.')

    return parser.parse_args()


if __name__ == '__main__':

    __main__()
