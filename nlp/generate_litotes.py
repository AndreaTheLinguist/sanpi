#!/usr/bin/env python3

import itertools
import time

from collections import namedtuple
from itertools import chain, product
from pprint import pprint

from wordbank import subjects, neg, modifiers, pred_specs


def __main__():

    # scaleTup = namedtuple(
    #     'scaleTup', ['pos', 'sctype', 'end_1', 'end_2', 'maxim', 'minim'])

    # nonGradTup = namedtuple(
    #     'nongradTup', ['pred', 'pos', 'sub', 'obj', 'past'])

    # # relative scales
    # rel_adj_scales = [
    #     scaleTup('adj', 'rel', p[0], p[1],
    #              rel_adj_maxmod, rel_adj_minmod)
    #     for p in rel_adj]

    # rel_noun_scales = [
    #     scaleTup('noun', 'rel', p[0], p[1],
    #              rel_noun_maxmod, rel_noun_minmod)
    #     for p in rel_noun]

    # rel_verb_scales = [
    #     scaleTup('verb', 'rel', p[0], p[1],
    #              rel_verb_maxmod, rel_verb_minmod)
    #     for p in rel_verb]

    # # absolute scales
    # abs_adj_scales = [
    #     scaleTup('adj', 'abs', p[0], p[1],
    #              abs_adj_maxmod, abs_adj_minmod)
    #     for p in abs_adj]

    # # 'pred', 'pos', 'sub', 'obj', 'past'
    # nongrad_tuples = [nonGradTup(p, 'adj', '', '', '') for p in nongrad_adj]

    # nongrad_verbs1 = [nonGradTup(
    #     v, 'verb', 'the students', 'the exam', v+'ed') for v in ['pass', 'fail']]

    # nongrad_verbs2 = [nonGradTup(
    #     v, 'verb', 'the judges', 'the application', v+'ed') for v in ['accept', 'reject']]

    # nongrad_tuples = nongrad_tuples + nongrad_verbs1 + nongrad_verbs2

    # adj_scale_list = rel_adj_scales + abs_adj_scales

    nongrad_dict = dict(
        filter(lambda item: '_non' in item[0], pred_specs.items()))

    grad_dict = dict(
        filter(lambda item: '_non' not in item[0], pred_specs.items()))

    adj_dict = dict(filter(lambda item: 'adj' in item[0], grad_dict.items()))

    pred_data_gen = generate_pred_data(subjects,
                                       adj_dict,  # grad_dict,
                                       modifiers, neg)

    # quant_data_gen = generate_quant(neg, nongrad_dict)

    # data_generator = chain(pred_data_gen, quant_data_gen)

    with open('/home/andrea/litotes/nlp/generated.csv', 'w') as out:

        out.write('sentences, pos, scale_type\n')

        for d in pred_data_gen:
            # for d in data_generator:
            out.write(f'{d[0]}, {d[1]}, {d[2]}\n')

        print(d)


def generate_quant(neg, nongrad_tuples):

    for sent in generate_quant_sent(neg, nongrad_tuples):

        yield (sent, 'det', 'quant')


def generate_quant_sent(neg, predTuples):

    for predTup in predTuples:

        if predTup.pos == 'adj':

            nongrad_adj = predTup.pred
            some_sent = f'Some were {nongrad_adj}.'
            none_sent = f'None were {nongrad_adj}.'

            # yield f'Not all of {pl_sub} were {nongrad_adj}.'
            yield f'Not all of them were {nongrad_adj}. {some_sent}'
            yield f'Not all of them were {nongrad_adj}. {none_sent}'

            for n in neg:
                # yield f'All of {pl_sub} were{n} {nongrad_adj}.'
                # yield f'{pl_sub.capitalize()} were{n} all {nongrad_adj}.'
                yield f'All of them were{n} {nongrad_adj}. {some_sent}'
                yield f'They were{n} all {nongrad_adj}. {some_sent}'

                yield f'All of them were{n} {nongrad_adj}. {none_sent}'
                yield f'They were{n} all {nongrad_adj}. {none_sent}'

        elif predTup.pos == 'verb':

            s_obj = predTup.obj
            pl_obj = s_obj+'s'

            inf_verb = predTup.pred
            past_verb = predTup.past

            some_did = f'Some of them  {past_verb} {s_obj}.'
            none_did = f'None of them  {past_verb} {s_obj}.'

            # yield f'Not all of {pl_sub} {past_verb} {s_obj}.'
            not_all = f'Not all of them {past_verb} {s_obj}.'
            yield f'{not_all} {some_did}'
            yield f'{not_all} {none_did}'
            yield f'{some_did} {not_all}'
            yield f'{none_did} {not_all}'

            for n in neg:

                all_didnt = f'All of them did{n} {inf_verb} {s_obj}.'
                didnt_all = f'They did{n} all {inf_verb} {s_obj}.'

                for s in [all_didnt, didnt_all]:

                    yield f'{s} {some_did}'
                    yield f'{s} {none_did}'
                    yield f'{some_did} {s}'
                    yield f'{none_did} {s}'

                for sub in ['She', 'He']:

                    # yield f'All of {pl_sub} did{n} {inf_verb} {s_obj}.'
                    # yield f'{pl_sub.capitalize()} did{n} all {inf_verb} {s_obj}.'
                    # yield f'{s_sub.capitalize()} did{n} {inf_verb} all of {pl_obj}.'
                    some_sent = f'{sub} {past_verb} some of {pl_obj}.'
                    none_sent = f'{sub} {past_verb} none of {pl_obj}.'
                    didnt_verb_all = f'{sub} did{n} {inf_verb} all of {pl_obj}.'

                    yield f'{didnt_verb_all} {some_sent}'
                    yield f'{didnt_verb_all} {none_sent}'
                    yield f'{some_sent} {didnt_verb_all}'
                    yield f'{none_sent} {didnt_verb_all}'


def generate_pred_data(subjects, specs_dict, modifiers, neg_forms):

    for category in specs_dict.keys():

        pos, sctype = category.split('_')

        if pos == 'adj':

            sent_gen = generate_adj_sentences(
                specs_dict[category], subjects, modifiers, neg_forms)

        elif pos == 'verb':

            sent_gen = generate_verb_sentences(
                specs_dict[category], subjects, modifiers, neg_forms)

        elif pos == 'noun':

            sent_gen = generate_verb_sentences(
                specs_dict[category], subjects, modifiers, neg_forms)

        for sent in sent_gen:

            yield (sent, pos, sctype)


def generate_sentence(scale, sub, neg):

    min_mods = [f' {w}' for w in scale.minim]
    max_mods = [f' {w}' for w in scale.maxim]
    no_mod = ['']

    for order in [(scale.end_1, scale.end_2),
                  (scale.end_2, scale.end_1)
                  ]:

        for neg_mod in max_mods + no_mod:

            for pos_mod in min_mods + max_mods + no_mod:

                # neg - pos, pos - neg
                # John wasn't (extremely) happy. John was (slightly, extremely) sad
                if scale.pos == 'adj':

                    n_sent = f'{sub} was{neg}{neg_mod} {order[0]}.'
                    p_sent = f'{sub} was{pos_mod} {order[1]}.'

                # taking adv-DP approach, rather than det-AdjP
                # John wasn't (totally) a villain. John was (somewhat of) a hero.
                # NOT: wasn't a total villain, etc.
                elif scale.pos == 'noun':

                    n_sent = f'{sub} was{neg}{neg_mod} a {order[0]}.'
                    p_sent = f'{sub} was{pos_mod} a {order[1]}'

                # John didn't (completely) love it. John (kind of) hated it.
                # todo: will need to include past tense conjugation info
                elif scale.pos == 'verb':

                    n_sent = f'{sub} did{neg}{neg_mod} {order[0]} it.'
                    p_sent = f'{sub} {pos_mod} {order[1]}d it.'

                yield f'{n_sent.capitalize()} {p_sent.capitalize()}'
                yield f'{p_sent.capitalize()} {n_sent.capitalize()}'

            # neg - neg
            for neg_mod2 in max_mods + no_mod:

                # e.g. John wasn't (extremely) happy. John wasn't (extremely) sad.
                if scale.pos == 'adj':

                    n1_sent = f'{sub} was{neg}{neg_mod} {order[0]}.'
                    n2_sent = f'{sub} was{neg}{neg_mod2} {order[1]}.'

                # e.g. John wasn't a (complete) hero. John wasn't a (complete) villian.
                # or??
                # John wasn't totally a hero. John wasn't totally a villian.
                elif scale.pos == 'noun':

                    n1_sent = f'{sub} was{neg}{neg_mod} a {order[0]}.'
                    n2_sent = f'{sub} was{neg}{neg_mod2} a {order[1]}.'

                # John didn't (completely) love it. John didn't (completely) hate it.
                elif scale.pos == 'verb':

                    n1_sent = f'{sub} did{neg}{neg_mod} {order[0]} it.'
                    n2_sent = f'{sub} did{neg}{neg_mod2} {order[0]} it.'

                yield f'{n1_sent.capitalize()} {n2_sent.capitalize()}'

        # intense clafification
        for max_mod in max_mods:

            for min_mod in min_mods:

                # John wasn't extremely happy. John was slightly happy.
                if scale.pos == 'adj':

                    neg_max_sent = f'{sub} was{neg}{max_mod} {order[0]}.'
                    pos_min_sent = f'{sub} was{min_mod} {order[0]}.'

                    pos_precise_span = f'{sub} was{min_mod} {order[0]}.'
                    neg_maxbase = f'{sub} was{neg}{max_mod} {order[0]}'
                    neg_contrary = f'{sub} was{neg} {order[1]}'

                # John wasn't completely a hero. John was sort of a hero.
                elif scale.pos == 'noun':

                    neg_max_sent = f'{sub} was{neg}{max_mod} a {order[0]}.'
                    pos_min_sent = f'{sub} was{min_mod} a {order[0]}.'

                    pos_precise_span = f'{sub} was{min_mod} a {order[0]}.'
                    neg_maxbase = f'{sub} was{neg}{max_mod} a {order[0]}'
                    neg_contrary = f'{sub} was{neg} a {order[1]}'

                # John didn't totlly love it. John sort of loved it.
                elif scale.pos == 'verb':

                    neg_max_sent = f'{sub} did{neg}{max_mod} {order[0]} it.'
                    pos_min_sent = f'{sub} {min_mod} {order[0]}d it.'

                    pos_precise_span = f'{sub} {min_mod} {order[0]} it.'
                    neg_maxbase = f'{sub} did{neg}{max_mod} {order[0]} it.'
                    neg_contrary = f'{sub} did{neg} {order[1]} it.'

                yield f'{neg_max_sent.capitalize()} {pos_min_sent.capitalize()}'
                yield f'{pos_min_sent.capitalize()} {neg_max_sent.capitalize()}'

                neg_conj_1 = f'{neg_maxbase} but {neg_contrary} either.'
                neg_conj_2 = f'{neg_contrary} but {neg_maxbase} either.'

                yield f'{pos_precise_span.capitalize()} {neg_conj_1.capitalize()}'
                yield f'{pos_precise_span.capitalize()} {neg_conj_2.capitalize()}'
                yield f'{neg_conj_1.capitalize()} {pos_precise_span.capitalize()}'
                yield f'{neg_conj_2.capitalize()} {pos_precise_span.capitalize()}'


def generate_adj_sentences(specs, pro_dict, modifiers, neg):

    for scale in specs:

        end1 = scale.end1
        end2 = scale.end2

        pos_contexts = [f'{p} was'
                        for p in get_pronouns(scale.subj_type, pro_dict)]

        neg_contexts = [''.join(c) for c in product(pos_contexts, neg)]

        # get_mod() returns relevant modifiers for scale type
        minim1, minim2, maxim1, maxim2 = get_mod(scale, modifiers)

        min_pred1 = [' '.join((adv, end1)) for adv in minim1]
        max_pred1 = [' '.join((adv, end1)) for adv in maxim1]

        min_pred2 = [' '.join((adv, end2)) for adv in minim2]
        max_pred2 = [' '.join((adv, end2)) for adv in maxim2]

        pred_template = namedtuple(
            'pred_forms', ['name', 'min_phrases', 'max_phrases', 'pos_phrases', 'neg_phrases'])

        # in order to do both scale directions
        for x in range(2):

            if x == 0:

                A = pred_template([end1], min_pred1, max_pred1,
                                  min_pred1 + max_pred1,
                                  max_pred1 + [end1])

                B = pred_template([end2], min_pred2, max_pred2,
                                  min_pred2 + max_pred2,
                                  max_pred2 + [end2])

            else:

                # switch assignment
                B = pred_template([end1], min_pred1, max_pred1,
                                  min_pred1 + max_pred1,
                                  max_pred1 + [end1])

                A = pred_template([end2], min_pred2, max_pred2,
                                  min_pred2 + max_pred2,
                                  max_pred2 + [end2])

            # neg - pos, pos - neg
            # John wasn't (extremely) happy. John was (slightly, extremely) sad
            n_sents = [' '.join(pairing)
                       for pairing in product(neg_contexts, A.neg_phrases)]

            p_sents = [' '.join(pairing)
                       for pairing in product(pos_contexts, B.pos_phrases)]

            for sent_pair in sent_pairs_gen(n_sents, p_sents):

                yield sent_pair

            # was:
            # n_sent = f'{sub} was{neg}{neg_mod} {order[0]}.'
            # p_sent = f'{sub} was{pos_mod} {order[1]}.'
            #
            # yield f'{n_sent.capitalize()} {p_sent.capitalize()}'
            # yield f'{p_sent.capitalize()} {n_sent.capitalize()}'

            # neg - neg
            # John wasn't (extremely) happy. John wasn't (extremely) sad.
            n1_sents = [' '.join(pairing)
                        for pairing in product(neg_contexts, A.neg_phrases)]

            n2_sents = [' '.join(pairing)
                        for pairing in product(neg_contexts, B.neg_phrases)]

            for sent_pair in sent_pairs_gen(n1_sents, n2_sents, flip=False):

                yield sent_pair

            # was:
            # n1_sent = f'{sub} was{neg}{neg_mod} {order[0]}.'
            # n2_sent = f'{sub} was{neg}{neg_mod2} {order[1]}.'

            # not-max base, mitigated base
            # John wasn't extremely happy. John was slightly happy.
            neg_max_sents = [
                ' '.join(pairing)
                for pairing in product(neg_contexts, A.max_phrases)]

            pos_min_sents = [
                ' '.join(pairing)
                for pairing in product(pos_contexts, A.min_phrases)]

            for sent_pair in sent_pairs_gen(neg_max_sents, pos_min_sents):

                yield sent_pair

            # was:
            # neg_max_sent = f'{sub} was{neg}{max_mod} {order[0]}.'
            # pos_min_sent = f'{sub} was{min_mod} {order[0]}.'

            # precise span conjunctions
            # She was slightly happy.
            # She wasn't extremely happy, but she wasn't sad either.
            pos_precise_spans = [
                ' '.join(pairing)
                for pairing in product(pos_contexts, A.min_phrases)]

            neg_maxbases = [
                ' '.join(pairing)
                for pairing in product(neg_contexts, A.max_phrases)]

            neg_contraries = [' '.join(pairing)
                              for pairing in product(neg_contexts, B.name)]

            max_cont_neithers = [
                ' but '.join(pairing) + ' either'
                for pairing in product(neg_maxbases, neg_contraries)]

            cont_max_neithers = [
                ' but '.join(pairing) + ' either'
                for pairing in product(neg_contraries, neg_maxbases)]

            for sent_pair in sent_pairs_gen(
                    pos_precise_spans,
                    max_cont_neithers + cont_max_neithers):

                yield sent_pair

            # was:
            # pos_precise_span = f'{sub} was{min_mod} {order[0]}.'
            # neg_maxbase = f'{sub} was{neg}{max_mod} {order[0]}'
            # neg_contrary = f'{sub} was{neg} {order[1]}'

            # neg_conj_1 = f'{neg_maxbase} but {neg_contrary} either.'
            # neg_conj_2 = f'{neg_contrary} but {neg_maxbase} either.'

        # yield f'{n1_sent.capitalize()} {n2_sent.capitalize()}'

        # yield f'{neg_max_sent.capitalize()} {pos_min_sent.capitalize()}'
        # yield f'{pos_min_sent.capitalize()} {neg_max_sent.capitalize()}'

        # yield f'{pos_precise_span.capitalize()} {neg_conj_1.capitalize()}'
        # yield f'{pos_precise_span.capitalize()} {neg_conj_2.capitalize()}'

        # yield f'{neg_conj_1.capitalize()} {pos_precise_span.capitalize()}'
        # yield f'{neg_conj_2.capitalize()} {pos_precise_span.capitalize()}'


def get_pronouns(s_type, subjects):

    if s_type == 'person':

        s_pronouns = subjects['people']

    elif s_type == 'thing':

        s_pronouns = subjects['things']

    elif s_type == 'either':

        s_pronouns = subjects['people'] + subjects['things']

    return s_pronouns


def get_mod(scale, modifiers):

    minim1 = minim2 = modifiers['open_min']
    maxim1 = maxim2 = modifiers['open_max']

    if scale.closed1:

        minim1 += modifiers['closed_min']
        maxim1 += modifiers['closed_max']

    if scale.closed2:

        minim2 += modifiers['closed_min']
        maxim2 += modifiers['closed_max']

    return minim1, minim2, maxim1, maxim2


def sent_pairs_gen(sentlist1, sentlist2, flip=True):

    sentlist1 = [s.capitalize()+'.' for s in sentlist1]

    sentlist2 = [s.capitalize()+'.' for s in sentlist2]

    sentlist_orders = [(sentlist1, sentlist2)]

    if flip:

        sentlist_orders.append((sentlist2, sentlist1))

    for order in sentlist_orders:

        for sent_pair in product(*order):

            yield ' '.join(sent_pair)


def generate_verb_sentences(specs, subjects, modifiers, n):

    yield []


def generate_noun_sentences(specs, subjects, modifiers, n):

    yield []


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round((absFinish - absStart)/60, 2)} minutes')
