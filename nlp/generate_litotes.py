#!/usr/bin/env python3

import itertools
import time

from collections import namedtuple
from pprint import pprint

from wordbank import subjects, neg, modifiers, pred_specs


def __main__():

    scaleTup = namedtuple(
        'scaleTup', ['pos', 'sctype', 'end_1', 'end_2', 'maxim', 'minim'])

    nonGradTup = namedtuple(
        'nongradTup', ['pred', 'pos', 'sub', 'obj', 'past'])

    # relative scales
    rel_adj_scales = [
        scaleTup('adj', 'rel', p[0], p[1],
                 rel_adj_maxmod, rel_adj_minmod)
        for p in rel_adj]

    rel_noun_scales = [
        scaleTup('noun', 'rel', p[0], p[1],
                 rel_noun_maxmod, rel_noun_minmod)
        for p in rel_noun]

    rel_verb_scales = [
        scaleTup('verb', 'rel', p[0], p[1],
                 rel_verb_maxmod, rel_verb_minmod)
        for p in rel_verb]

    # absolute scales
    abs_adj_scales = [
        scaleTup('adj', 'abs', p[0], p[1],
                 abs_adj_maxmod, abs_adj_minmod)
        for p in abs_adj]

    # 'pred', 'pos', 'sub', 'obj', 'past'
    nongrad_tuples = [nonGradTup(p, 'adj', '', '', '') for p in nongrad_adj]

    nongrad_verbs1 = [nonGradTup(
        v, 'verb', 'the students', 'the exam', v+'ed') for v in ['pass', 'fail']]

    nongrad_verbs2 = [nonGradTup(
        v, 'verb', 'the judges', 'the application', v+'ed') for v in ['accept', 'reject']]

    nongrad_tuples = nongrad_tuples + nongrad_verbs1 + nongrad_verbs2

    adj_scale_list = rel_adj_scales + abs_adj_scales

    # generator obj yields tuples of form (sentence, POS, scale type)
    adj_data_generator = generate_data(subjects, adj_scale_list, neg)

    noun_data_generator = generate_data(people_subjects, rel_noun_scales, neg)

    verb_data_generator = generate_data(people_subjects, rel_verb_scales, neg)

    quant_data_generator = generate_quant(neg, nongrad_tuples)

    data_generator = itertools.chain(
        adj_data_generator, noun_data_generator,
        verb_data_generator, quant_data_generator)

    with open('/home/andrea/litotes/nlp/generated.csv', 'w') as out:

        out.write('sentences, pos, scale_type\n')

        for d in data_generator:
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


def generate_data(subjects, scales_list, neg_types):

    for sub in subjects:

        for scale in scales_list:

            for n in neg_types:

                for sent in generate_sentence(scale, sub, n):

                    yield (sent, scale.pos, scale.sctype)


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


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round((absFinish - absStart)/60, 2)} minutes')
