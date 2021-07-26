#!/usr/bin/env python3

import itertools
import time

from collections import namedtuple
from itertools import chain, product
from pprint import pprint

from wordbank import modifiers, neg, pred_specs, subjects

pred_template = namedtuple(
    'pred_forms', ['neg_name', 'pos_min_phrases', 'neg_max_phrases',
                   'pos_phrases', 'neg_phrases'])


def __main__():

    nongrad_dict = dict(
        filter(lambda item: '_non' in item[0], pred_specs.items()))

    grad_dict = dict(
        filter(lambda item: '_non' not in item[0], pred_specs.items()))

    adj_dict = dict(filter(lambda item: 'adj' in item[0], grad_dict.items()))

    pred_data_gen = generate_pred_data(
        adj_dict
        # grad_dict,
    )

    quant_data_gen = generate_quant(nongrad_dict)

    # data_generator = chain(pred_data_gen, quant_data_gen)

    with open('/home/andrea/litotes/nlp/generated.csv', 'w') as out:

        out.write('sentences,pos, scale_type\n')

        for d in pred_data_gen:
            # for d in quant_data_gen:
            # for d in data_generator:
            out.write(f'{d[0]},{d[1]},{d[2]}\n')

        print(d)


def generate_quant(nongrad_dict):

    for sent in generate_quant_data(nongrad_dict):

        yield (sent, 'det', 'quant')


def generate_quant_data(specs_dict):

    for category in specs_dict.keys():

        pos, __ = category.split('_')

        if pos == 'adj':

            for pred_info in specs_dict[category]:

                yield from generate_quant_adj(pred_info)

        # elif predTup.pos == 'verb':

        #     s_obj = predTup.obj
        #     pl_obj = s_obj+'s'

        #     inf_verb = predTup.pred
        #     past_verb = predTup.past

        #     some_did = f'Some of them  {past_verb} {s_obj}.'
        #     none_did = f'None of them  {past_verb} {s_obj}.'

        #     # yield f'Not all of {pl_sub} {past_verb} {s_obj}.'
        #     not_all = f'Not all of them {past_verb} {s_obj}.'
        #     yield f'{not_all} {some_did}'
        #     yield f'{not_all} {none_did}'
        #     yield f'{some_did} {not_all}'
        #     yield f'{none_did} {not_all}'

        #     for n in neg:

        #         all_didnt = f'All of them did{n} {inf_verb} {s_obj}.'
        #         didnt_all = f'They did{n} all {inf_verb} {s_obj}.'

        #         for s in [all_didnt, didnt_all]:

        #             yield f'{s} {some_did}'
        #             yield f'{s} {none_did}'
        #             yield f'{some_did} {s}'
        #             yield f'{none_did} {s}'

        #         for sub in ['She', 'He']:

        #             # yield f'All of {pl_sub} did{n} {inf_verb} {s_obj}.'
        #             # yield f'{pl_sub.capitalize()} did{n} all {inf_verb} {s_obj}.'
        #             # yield f'{s_sub.capitalize()} did{n} {inf_verb} all of {pl_obj}.'
        #             some_sent = f'{sub} {past_verb} some of {pl_obj}.'
        #             none_sent = f'{sub} {past_verb} none of {pl_obj}.'
        #             didnt_verb_all = f'{sub} did{n} {inf_verb} all of {pl_obj}.'

        #             yield f'{didnt_verb_all} {some_sent}'
        #             yield f'{didnt_verb_all} {none_sent}'
        #             yield f'{some_sent} {didnt_verb_all}'
        #             yield f'{none_sent} {didnt_verb_all}'


def generate_quant_adj(pred_info):

    adj_a = pred_info.end1
    adj_b = pred_info.end2
    adj_pair = (adj_a, adj_b)

    pos_exist_sents = [f'some of them were {adj}'
                       for adj in adj_pair]

    neg_exist_sents = [f'none of them were {adj}'
                       for adj in adj_pair]

    exist_sents = pos_exist_sents + neg_exist_sents

    not_all_sents = [f'not all of them were {adj}'
                     for adj in adj_pair]

    # note: product() requires iterables, even for singletons
    all_not_parts = product(('all of them were',), neg, adj_pair)
    all_not_sents = [' '.join(parts) for parts in all_not_parts]

    were_n_all_parts = product(('they were',), neg, ('all',), adj_pair)
    were_n_all_sents = [' '.join(parts) for parts in were_n_all_parts]

    neg_univ_sents = not_all_sents + all_not_sents + were_n_all_sents

    for sent_pair in sent_pairs_gen(neg_univ_sents, exist_sents, flip=False):

        # print(sent_pair)
        yield sent_pair


def generate_pred_data(specs_dict):

    for category in specs_dict.keys():

        pos, sctype = category.split('_')

        specs = specs_dict[category]

        if pos == 'adj':

            sent_gen = generate_adj_sentences(
                specs)

        elif pos == 'verb':

            sent_gen = generate_verb_sentences(
                specs)

        elif pos == 'noun':

            sent_gen = generate_noun_sentences(
                specs)

        for sent in sent_gen:

            yield (sent, pos, sctype)


def generate_adj_sentences(specs):

    for scale in specs:

        end1 = scale.end1
        end2 = scale.end2

        # get_mod() returns relevant modifiers for scale type
        minim1, minim2, maxim1, maxim2 = get_mod(scale)

        # just use adv for adjectives
        min_pred1 = [' '.join((m.adv, end1)) for m in minim1]
        max_pred1 = [' '.join((m.adv, end1)) for m in maxim1]

        min_pred2 = [' '.join((m.adv, end2)) for m in minim2]
        max_pred2 = [' '.join((m.adv, end2)) for m in maxim2]

        for sub in get_pronouns(scale.subj_type):

            pos_context = f'{sub} was'

            neg_contexts = [f'{pos_context} {n}' for n in neg]

        # in order to do both scale directions
        for x in range(2):

            if x == 0:

                A = pred_template([end1], min_pred1, max_pred1,
                                  min_pred1 + max_pred1 + [end1],
                                  max_pred1 + [end1])

                B = pred_template([end2], min_pred2, max_pred2,
                                  min_pred2 + max_pred2 + [end2],
                                  max_pred2 + [end2])

            else:

                # switch assignment
                B = pred_template([end1], min_pred1, max_pred1,
                                  min_pred1 + max_pred1 + [end1],
                                  max_pred1 + [end1])

                A = pred_template([end2], min_pred2, max_pred2,
                                  min_pred2 + max_pred2 + [end2],
                                  max_pred2 + [end2])

            yield from gen_basic(A, B, neg_contexts, pos_context)
            yield from gen_2negated(A, B, neg_contexts)
            yield from gen_mitigated_contrary(A, neg_contexts, pos_context)
            yield from gen_precise_spans(A, B, neg_contexts, pos_context)


def generate_verb_sentences(specs):

    # generate sentences like:
    # She loved it. She didn't love it.
    # She absolutely loved it. She did not absolutely love it.

    for scale in specs:

        verb_tense = namedtuple('verb_forms', ['past', 'inf'])
        verb_a = verb_tense(scale.past1, scale.end1)
        verb_b = verb_tense(scale.past2, scale.end2)

        subs = get_pronouns(scale.subj_type)
        if scale.subject:
            subs.append(scale.subject)

        objs = get_pronouns(scale.obj_type)
        if scale.object:
            objs.append(scale.object)

        min_a, min_b, max_a, max_b = get_mod(scale)

        # pull out just the adv for verbs
        min_a = [m.adv for m in min_a]
        min_b = [m.adv for m in min_b]
        max_a = [m.adv for m in max_a]
        max_b = [m.adv for m in max_b]

        # loved it
        bare_pos_a = [f'{verb_a.past} {o}' for o in objs]
        bare_pos_b = [f'{verb_b.past} {o}' for o in objs]

        # love it
        bare_neg_a = [f'{verb_a.inf} {o}' for o in objs]
        bare_neg_b = [f'{verb_b.inf} {o}' for o in objs]

        # absolutely loved it
        pos_min_a = [' '.join(p)
                     for p in product(min_a, bare_pos_a)]
        pos_max_a = [' '.join(p)
                     for p in product(max_a, bare_pos_a)]

        pos_min_b = [' '.join(p)
                     for p in product(min_b, bare_pos_b)]
        pos_max_b = [' '.join(p)
                     for p in product(max_b, bare_pos_b)]

        # absolutely love it
        # note: negated minimizers are ungrammatical = no neg_min_a/b
        neg_max_a = [' '.join(p)
                     for p in product(max_a, bare_neg_a)]

        neg_max_b = [' '.join(p)
                     for p in product(max_b, bare_neg_b)]

        for s in subs:

            pos_contexts = s
            # "she did n't", "she did not"
            neg_contexts = [f'{s} did {n}' for n in neg]

            # in order to do both scale directions
            for x in range(2):

                if x == 0:

                    A = pred_template(bare_neg_a,
                                      pos_min_a, neg_max_a,
                                      bare_pos_a + pos_min_a + pos_max_a,
                                      bare_neg_a + neg_max_a)

                    B = pred_template(bare_neg_b,
                                      pos_min_b, neg_max_b,
                                      bare_pos_b + pos_min_b + pos_max_b,
                                      bare_neg_b + neg_max_b)

                else:

                    # switch assignment
                    B = pred_template(bare_neg_a,
                                      pos_min_a, neg_max_a,
                                      bare_pos_a + pos_min_a + pos_max_a,
                                      bare_neg_a + neg_max_a)

                    A = pred_template(bare_neg_b,
                                      pos_min_b, neg_max_b,
                                      bare_pos_b + pos_min_b + pos_max_b,
                                      bare_neg_b + neg_max_b)

        yield from gen_basic(A, B, neg_contexts, pos_contexts)
        yield from gen_2negated(A, B, neg_contexts)
        yield from gen_mitigated_contrary(A, neg_contexts, pos_contexts)
        yield from gen_precise_spans(A, B, neg_contexts, pos_contexts)


def generate_noun_sentences(specs):

    for scale in specs:

        bases, min_phrases, max_phrases = get_noun_phrases(scale)

        sub_list = get_pronouns(scale.subj_type)
        for s in sub_list:

            pos_context = f'{s} was'
            neg_contexts = [f'{pos_context} {n}' for n in neg]

            for cycle in range(2):

                if cycle == 0:

                    A = pred_template(
                        [bases[0]],
                        min_phrases[0], max_phrases[0],
                        min_phrases[0] + max_phrases[0] + [bases[0]],
                        max_phrases[0] + [bases[0]]
                    )

                    B = pred_template(
                        [bases[1]],
                        min_phrases[1], max_phrases[1],
                        min_phrases[1] + max_phrases[1] + [bases[1]],
                        max_phrases[1] + [bases[1]]
                    )

                else:

                    # switch assignment
                    B = pred_template(
                        [bases[0]],
                        min_phrases[0], max_phrases[0],
                        min_phrases[0] + max_phrases[0] + [bases[0]],
                        max_phrases[0] + [bases[0]]
                    )

                    A = pred_template(
                        [bases[1]],
                        min_phrases[1], max_phrases[1],
                        min_phrases[1] + max_phrases[1] + [bases[1]],
                        max_phrases[1] + [bases[1]]
                    )

            yield from gen_basic(A, B, neg_contexts, pos_context)
            yield from gen_2negated(A, B, neg_contexts)
            yield from gen_mitigated_contrary(A, neg_contexts, pos_context)
            yield from gen_precise_spans(A, B, neg_contexts, pos_context)


def get_noun_phrases(scale):

    noun_1 = scale.end1
    noun_2 = scale.end2

    min_1, min_2, max_1, max_2 = get_mod(scale)

    min_1_adj_nouns = [f'{m.adj} {noun_1}' for m in min_1]
    max_1_adj_nouns = [f'{m.adj} {noun_1}' for m in max_1]

    min_2_adj_nouns = [f'{m.adj} {noun_2}' for m in min_2]
    max_2_adj_nouns = [f'{m.adj} {noun_2}' for m in max_2]

    if scale.measure == 'count':

        article_1 = 'an' if noun_1[0] in 'aeiou' else 'a'
        article_2 = 'an' if noun_2[0] in 'aeiou' else 'a'

        np_1 = f'{article_1} {noun_1}'
        np_2 = f'{article_2} {noun_2}'

        # completely a hero
        min_1_aps = [f'{m.adv} {np_1}' for m in min_1]
        max_1_aps = [f'{m.adv} {np_1}' for m in max_1]

        min_2_aps = [f'{m.adv} {np_2}' for m in min_2]
        max_2_aps = [f'{m.adv} {np_2}' for m in max_2]

        art_an = 'an'
        art_a = 'a'
        vowels = 'aeiou'

        # a complete hero, an absolute villian
        min_1_nps = [f'{art_an if a_n[0] in vowels else art_a} {a_n}'
                     for a_n in min_1_adj_nouns]
        max_1_nps = [f'{art_an if a_n[0] in vowels else art_a} {a_n}'
                     for a_n in max_1_adj_nouns]

        min_2_nps = [f'{art_an if a_n[0] in vowels else art_a} {a_n}'
                     for a_n in min_2_adj_nouns]
        max_2_nps = [f'{art_an if a_n[0] in vowels else art_a} {a_n}'
                     for a_n in max_2_adj_nouns]

        min_1_phrases = min_1_aps + min_1_nps
        max_1_phrases = max_1_aps + max_1_nps

        min_2_phrases = min_2_aps + min_2_nps
        max_2_phrases = max_2_aps + max_2_nps

    # (complete) safety
    else:

        np_1 = noun_1
        np_2 = noun_2

        min_1_phrases = min_1_adj_nouns
        max_1_phrases = max_1_adj_nouns

        min_2_phrases = min_2_adj_nouns
        max_2_phrases = max_2_adj_nouns

    return ((np_1, np_2),
            (min_1_phrases, min_2_phrases),
            (max_1_phrases, max_2_phrases))


def get_pronouns(entity_type):

    pronouns = []

    if not entity_type:
        return ['']

    if entity_type == 'person':

        pronouns += subjects['people']

    elif entity_type == 'thing':

        pronouns += subjects['things']

    elif entity_type == 'either':

        pronouns += subjects['people']
        pronouns += subjects['things']

    return pronouns


def get_mod(scale):

    closed_max = modifiers['closed_max']
    closed_min = modifiers['closed_min']

    open_max = modifiers['open_max']
    open_min = modifiers['open_min']

    if scale.pos == 'adj':

        minim1 = minim2 = open_min
        maxim1 = maxim2 = open_max

        if scale.closed1:

            minim1 += closed_min
            maxim1 += closed_max

        if scale.closed2:

            minim2 += closed_min
            maxim2 += closed_max

    else:

        minim1 = minim2 = open_min

        # relative verbs and nouns do not seem to work with open_max
        # e.g. ?John was extremely a hero. ?He was an extreme hero.
        #      ?He extremely loved the dish.
        # but they do work with closed_max
        # e.g. John was completely a hero. He was a total hero.
        #      He completely loved the dish.
        if scale.relative:

            maxim1 = maxim2 = closed_max

        else:

            maxim1 = maxim2 = open_max

            if scale.closed1:

                minim1 += closed_min
                maxim1 += closed_max

            if scale.closed2:

                minim2 += closed_min
                maxim2 += closed_max

    return minim1, minim2, maxim1, maxim2


def gen_basic(A, B, neg_contexts, pos_context):

    # neg - pos, pos - neg
    # John wasn't (extremely) happy. John was (slightly, extremely) sad
    n_sents = [' '.join(pairing)
               for pairing in product(neg_contexts, A.neg_phrases)]

    p_sents = [f'{pos_context} {pred}' for pred in B.pos_phrases]

    for sent_pair in sent_pairs_gen(n_sents, p_sents):

        yield sent_pair

    # was:
    # n_sent = f'{sub} was{neg}{neg_mod} {order[0]}.'
    # p_sent = f'{sub} was{pos_mod} {order[1]}.'
    #
    # yield f'{n_sent.capitalize()} {p_sent.capitalize()}'
    # yield f'{p_sent.capitalize()} {n_sent.capitalize()}'


def gen_2negated(A, B, neg_contexts):

    # neg - neg
    # John wasn't (extremely) happy. John wasn't (extremely) sad.
    n1_sents = [' '.join(pairing)
                for pairing in product(neg_contexts, A.neg_phrases)]

    n2_sents = [' '.join(pairing)
                for pairing in product(neg_contexts, B.neg_phrases)]

    for sent_pair in sent_pairs_gen(n1_sents, n2_sents, flip=False):

        yield sent_pair


def gen_precise_spans(A, B, neg_contexts, pos_context):

    # precise span conjunctions
    # She was slightly happy.
    # She wasn't extremely happy, but she wasn't sad either.
    pos_precise_spans = [f'{pos_context} {pred}'
                         for pred in A.pos_min_phrases]

    neg_maxbases = [
        ' '.join(pairing)
        for pairing in product(neg_contexts, A.neg_max_phrases)]

    neg_contraries = [' '.join(pairing)
                      for pairing in product(neg_contexts, B.neg_name)]

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

    # yield f'{pos_precise_span.capitalize()} {neg_conj_1.capitalize()}'
    # yield f'{pos_precise_span.capitalize()} {neg_conj_2.capitalize()}'

    # yield f'{neg_conj_1.capitalize()} {pos_precise_span.capitalize()}'
    # yield f'{neg_conj_2.capitalize()} {pos_precise_span.capitalize()}'


def gen_mitigated_contrary(A, neg_contexts, pos_context):

    # not-max base, mitigated base
    # John wasn't extremely happy. John was slightly happy.
    neg_max_sents = [
        ' '.join(pairing)
        for pairing in product(neg_contexts, A.neg_max_phrases)]

    pos_min_sents = [f'{pos_context} {pred}' for pred in A.pos_min_phrases]

    for sent_pair in sent_pairs_gen(neg_max_sents, pos_min_sents):

        yield sent_pair

    # was:
    # neg_max_sent = f'{sub} was{neg}{max_mod} {order[0]}.'
    # pos_min_sent = f'{sub} was{min_mod} {order[0]}.'

    # yield f'{neg_max_sent.capitalize()} {pos_min_sent.capitalize()}'
    # yield f'{pos_min_sent.capitalize()} {neg_max_sent.capitalize()}'


def sent_pairs_gen(sentlist1, sentlist2, flip=True):

    # final touches on sentences
    sentlist1 = [s.capitalize()+'.' for s in sentlist1]

    sentlist2 = [s.capitalize()+'.' for s in sentlist2]

    sentlist_orders = [(sentlist1, sentlist2)]

    # for everything but the negative-negative sentence pairs
    if flip:

        sentlist_orders.append((sentlist2, sentlist1))

    for order in sentlist_orders:

        for sent_pair in product(*order):

            yield ' '.join(sent_pair)


if __name__ == '__main__':

    absStart = time.perf_counter()
    __main__()
    absFinish = time.perf_counter()
    print(f'Total time: {round((absFinish - absStart)/60, 2)} minutes')
