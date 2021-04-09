#!/usr/bin/env python3

from collections import namedtuple

people_subjects = [
    'she',
    'he',
]

thing_subjects = [
    'that',
    'it'
]

subjects = {"people": people_subjects, 'things': thing_subjects}

neg = tuple(n+'_n'
            for n in (
                ' not',
                # 'n\'t'
            ))

modifiers = {
    'closed_max': tuple(
        m+'_m' for m in ('completely',
                         'totally',
                         'absolutely',
                         'entirely')),
    'open_max': tuple(
        m+'_m' for m in ('extremely',
                         'ridiculously',
                         'incredibly',
                         'terribly')),
    'closed_min': tuple(
        m+'_m' for m in ('slightly',
                         'partially')),
    'open_min': tuple(
        m+'_m' for m in ('kinda',
                         'sorta',
                         'somewhat'))
}

person = 'person'
thing = 'thing'
either = 'either'

###  base adjective info  ###
rel_adj = [
    # end1, end2, entity type
    ('happy', 'sad', person),
    ('tall', 'short', either),
    ('expensive', 'inexpensive', thing),
    ('big', 'small', either),
    ('strong', 'weak', either),
    ('fast', 'slow', either),
    ('smart', 'dumb', either),
    ('brilliant', 'idiotic', either),
    ('interesting', 'boring', either),
    ('rich', 'poor', person),
    ('beautiful', 'ugly', either),
    ('old', 'young', either),
    ('kind', 'cruel', either),
    ('polite', 'rude', either),
    ('deep', 'shallow', either),
    ('likely', 'unlikely', thing),
    ('energetic', 'lethargic', person),
    ('tight', 'loose', thing),
    ('hot', 'cold', either)
]

# may be some complications with these because different scale points may have different modifier restrictions.
# these also will not be litotes in the unmodified cases

abs_adj = [
    # end1, end2, entity type, closed1, closed2
    ('wet', 'dry', thing, True, True),
    ('full', 'empty', thing, True, True),
    ('opaque', 'transparent', thing, True, True),
    ('open', 'closed', thing, True, True),

    ('straight', 'bent', thing, True, False),
    ('pure', 'diluted', thing, True, False),
    ('honest', 'deceitful', person, True, False),
    ('smooth', 'bumpy', thing, True, False),
    ('clean', 'dirty', either, True, False),
    ('certain', 'uncertain', either, True, False),
    ('safe', 'dangerous', either, True, False),
    ('accurate', 'inaccurate', either, True, False),

]

# these are simpler than absolute gradables in the sense that they never create litotes
nongrad_adj = [
    # pred1, pred2, entity type
    ('locked', 'unlocked', thing),
    ('dead', 'alive', person),
    ('married', 'unmarried', person),
    ('organic', 'inorganic', thing),
    ('known', 'unknown', either),
    ('present', 'absent', either),
]


###  base verb info  ###
verb_info_tup = namedtuple('verb_info', [
                           'end1', 'end2', "subject_type", 'object_type', 'past1', 'past2', 'obj', 'subj', 'closed1', 'closed2'])

rel_verb = [
    # end1, end2, subject type, object type, past1, past2, object
    verb_info_tup('love', 'hate', person, either,
                  'loved', 'hated', 'the dish', None, None, None),
    verb_info_tup('like', 'dislike', person, either, 'liked',
                  'disliked', 'the candidate', None, None, None),
    verb_info_tup('rise', 'fall', thing, None, 'rose',
                  'fell', None, None, None, None),
    verb_info_tup('warm up', 'cool down', either, None,
                  'warmed up', 'cooled down', None, None, None, None)
]

abs_verb = [
    # end1, end2, subject type, object type, past1, past2, object, closed1, closed2
    verb_info_tup('open', 'close', person, thing, 'opened',
                  'closed', 'the window', None, True, True),
    verb_info_tup('bend', 'straighten', person, thing, 'bent',
                  'straightened', 'the rod', None, False, True)
]

nongrad_verb = [
    # end1, end2, subject type, object type, past1, past2, object, subject
    verb_info_tup('pass', 'fail', person, thing, 'passed',
                  'failed', 'the exam', 'the students', None, None),
    verb_info_tup('accept', 'reject', person, thing, 'accepted',
                  'rejected', 'the application', 'the judges', None, None),
    verb_info_tup('buy', 'sell', person, thing, 'bought', 'sold',
                  'the package', 'the companies', None, None),
    # maybe not a person? conglomerate
    verb_info_tup('join', 'leave', person, thing, 'joined',
                  'left', 'the association', 'the residents', None, None)
]

# should this be extended to be ADJ + NOUN ? happy person, tall man
rel_noun = [
    ('hero', 'villian', person, 'count'),
    # is this more absolute? middle gound may not exist for all people in all cases
    ('optimist', 'pessimist', person, 'count')
]

abs_noun = [
    ('safety', 'danger', thing, 'mass', True, False),
    ('certainty', 'uncertainty', thing, 'mass', True, False)
]

# do these need to be in pairs? if there is no relevant scale?
nongrad_noun = [
    ('boat', 'airplane', thing, 'count'),
    ('teacher', 'student', person, 'count'),
    ('buyer', 'seller', person, 'count'),
    ('christian', 'atheist', person, 'count')
]


def set_deg_specs(word_info, sctype, pos):

    # process adj
    if pos == 'adj':

        word_list = set_adj_specs(word_info, sctype)

    # process verb
    elif pos == 'verb':

        word_list = set_verb_specs(word_info, sctype)

    # process noun
    else:

        word_list = set_noun_specs(word_info, sctype)

    return tuple(word_list)


def set_adj_specs(word_info, sctype):

    word_list = []
    adj_tup = namedtuple('adj_specs',
                         ['end1', 'end2', 'subj_type', 'relative', 'vague', 'closed1', 'closed2'])

    for w in word_info:

        if sctype == 'nongrad':

            rel = vague = False
            closed1 = closed2 = True

        else:

            vague = True

            if sctype == 'relative':

                rel = True
                closed1 = closed2 = False

            elif sctype == 'absolute':

                rel = False
                closed1 = w[3]
                closed2 = w[4]

        word_list.append(
            adj_tup(w[0]+'_p', w[1]+'_p', w[2], rel, vague, closed1, closed2))

    return word_list


def set_verb_specs(word_info, sctype):

    word_list = []
    verb_tup = namedtuple('verb_specs',
                          ['end1', 'end2', 'past1', 'past2', 'subject', 'object', 'subj_type', 'obj_type', 'closed1', 'closed2', 'relative', 'vague'])

    for w in word_info:

        if sctype == 'nongrad':

            rel = vague = False
            closed1 = closed2 = True

        elif sctype == 'relative':

            rel = vague = True
            closed1 = closed2 = False

        elif sctype == 'absolute':

            rel = False
            vague = True
            closed1 = w.closed1
            closed2 = w.closed2

        word_list.append(
            verb_tup(w.end1+'_p', w.end2+'_p', w.past1+'_p', w.past2+'_p',
                     w.subj, w.obj, w.subject_type, w.object_type,
                     closed1, closed2, rel, vague))

    return word_list


def set_noun_specs(word_info, sctype):
    word_list = []

    noun_tup = namedtuple('noun_specs', [
                          'end1', 'end2', 'subj_type', 'measure', 'relative', 'vague', 'closed1', 'closed2'])

    for n in word_info:

        if sctype == 'nongrad':

            rel = vague = False
            closed1 = closed2 = True

        elif sctype == 'relative':

            rel = vague = True
            closed1 = closed2 = False

        elif sctype == 'absolute':

            rel = False
            vague = True
            closed1 = n[4]
            closed2 = n[5]

        word_list.append(
            noun_tup(n[0]+'_p', n[1]+'_p', n[2], n[3], rel, vague, closed1, closed2))

    return word_list


# rel_adj_maxmod = [
#     'extremely',
#     # 'ridiculously'
# ]
# rel_noun_maxmod = [
#     'completely',
#     # 'necessarily'
# ]
# rel_verb_maxmod = [
#     # 'completely',
#     'extremely'
# ]

# rel_adj_minmod = [
#     'slightly',
#     # 'sort of'
# ]

# rel_noun_minmod = [
#     # 'slightly',
#     'sort of'
# ]

# rel_verb_minmod = [
#     # 'sort of',
#     'kinda'
# ]


# abs_adj_maxmod = [
#     # 'completely',
#     'entirely'
# ]

# abs_adj_minmod = [
#     # 'slightly',
#     'sort of'
# ]


nongrad_verbs = []

# initialize empty dict to store predicate specifications
pred_specs = {}

pred_specs['adj_rel'] = set_deg_specs(rel_adj, 'relative', 'adj')
pred_specs['adj_abs'] = set_deg_specs(abs_adj, 'absolute', 'adj')
pred_specs['adj_non'] = set_deg_specs(nongrad_adj, 'nongrad', 'adj')

pred_specs['verb_rel'] = set_deg_specs(rel_verb, 'relative', 'verb')
pred_specs['verb_abs'] = set_deg_specs(abs_verb, 'absolute', 'verb')
pred_specs['verb_non'] = set_deg_specs(nongrad_verb, 'nongrad', 'verb')

pred_specs['noun_rel'] = set_deg_specs(rel_noun, 'relative', 'noun')
pred_specs['noun_abs'] = set_deg_specs(abs_noun, 'absolute', 'noun')
pred_specs['noun_non'] = set_deg_specs(nongrad_noun, 'nongrad', 'noun')
