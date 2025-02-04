SPECIAL_ADV = {
    'ever', 'yet', 'anymore', 'any', 'anyway',
    'necessarily', 'still',
    'pretty', 'rather', 'somewhat', 'fairly', 'kinda',  # 'sorta',
    'insanely', 'absurdly', 'ridiculously', 'insanely',
    'marginally', 'moderately', 'minimally',
    # 'maximally',
    'perfectly', 'completely', 'totally', 'fully', 'especially',
    'absolutely', 'utterly', 'downright',  # 'positively',# 'hugely',
    'allegedly', 'supposedly',  # 'easily',
    # 'certifiably',
    'definitely', 'nearly',  # 'decreasingly','lowkey',
    'slightly', 'perfectly', 'almost', 'mostly', 'largely',  # 'very',
    # 'now', 'soon', 'previously',
    'remotely', 'that', 'exactly', 'precisely', 'quite'
}

EXACTLY_RELEVANT_ADJ = ['sure',
                        'forthcoming',
                        'uncommon',
                        'same',
                        'surprising',
                        'clear',
                        'conducive',
                        'thrilled',
                        'zero',
                        'comparable',
                        'friendly',
                        'easy',
                        'opposite',
                        'equivalent',
                        'unexpected',
                        'fair',
                        'reassuring',
                        'correct',
                        'right',
                        'famous',
                        'novel',
                        'equal',
                        'subtle',
                        'true',
                        'revolutionary',
                        'great',
                        'stellar',
                        'ideal',
                        'analogous',
                        'pleasant',
                        'straightforward',
                        'alike',
                        'happy',
                        'cheap',
                        'difficult',
                        'shocking',
                        'perpendicular',
                        'welcome',
                        'parallel',
                        'shy',
                        'impressive',
                        'new'
                        ]

TOP_NEG_ADV = {
    "ever",
    "longer",
    "particularly",
    "inherently",
    "especially",
    "necessarily",
    "that",
    "exactly",
    "immediately",
    "yet",
    "any",
    "remotely",
    "terribly",
    "only",
    "overly",
}
TOP_POS_ADV = {
    "maybe",
    "downright",
    "largely",
    "pretty",
    "plain",
    "rather",
    "somewhat",
    "otherwise",
    "increasingly",
    "relatively",
    "almost",
    "mostly",
    "seemingly",
    "fairly",
}

SAMPLE_ADJ = {
    'open': (
        'large', 'small',
        'big', 'little',
        'tall', 'short',
        'high', 'low',
        'rich', 'poor',
        'good', 'bad',
        'easy', 'difficult',
        'hard', 'soft',
    ),
    'lower_closed': (
        'bent', 'dirty', 'rough', 'dangerous'
    ),
    'upper_closed': (
        'straight', 'clean', 'smooth', 'safe'
    ),
    'totally_closed': (
        'transparent', 'opaque',
        'full', 'empty',
        'open', 'closed'
    ),
    'extreme': (
        'enormous', 'minuscule',
        'colossal', 'gorgeous',
        'hideous', 'idiotic',
        'fantastic'
    ),
    'nongradeable': (
        'existing', 'extinct',
        'missing',
        'alive',
        'dead',
        'pregnant',
        'locked',
        'geological'
    )
}

SAMPLE_ADV = {
    'comparative': (
        'more',
        'most',
        'less',
        'least',
        'as'
        # 'relatively',
    ),
    'sufficient': (
        'so',
        'too',
        'enough'
    ),
    'intense': (
        'very',
        'really',
        'quite',
        'extremely',
        'particularly'
    ),
    'min_threshold': (
        'slightly',
        'partially',
    ),
    'max_threshold': (
        'perfectly',
        'fully',
        'completely'
    ),
    'extreme': (
        'absolutely',
        'positively',
        'downright',
        'just'
    ),
}

ADV_OF_INTEREST = {
    'sufficient': {
        'so',
        'too',
        'enough'
    },

    'min_threshold': {
        'slightly',
        'partially',
    },

    'max_threshold': {
        'perfectly',
        'fully',
        'completely'
    },

    'moderate':    {
        'slightly',
        'partially',
        'minimally',
        'marginally',
        'weakly',
        'modestly',
        'moderately',
        'underwhelmingly',
        'acceptably',
        'adequately',
        'passingly',
        'passing',
        'satisfactorily',
        'reasonably',
        'tolerably',
        'dubiously',
        'supposedly',
    },

    'precise_intense': {
        'exactly',
        'precisely'
    },

    'compare': {
        'more',
        'less',
        'most',
        'least',
        'as',
        'comparatively'  # ? #TODO does this pelong here?
        # 'relatively'
    },

    'weak_intense':    {
        'very',
        'really',
        'real',
        'quite'
    },

    'meas_intense':    {
        'hugely',
        'largely',
        'greatly',
        'highly',
        'deeply',
        'steeply',
        'widely',
        'strongly',
        'immensely',
        'grossly',
        'increasingly',
        'purely',
        'tremendously',
        'monumentally'
    },

    'mod_intense': {
        'particularly',
        'especially',
        'entirely',
        'extremely',
        'super',
        'intensely'
    },

    'good_intense': {
        'amazingly',
        'heartily',
        'awesomely',
        'phenomenally',
        'impressively',
        'marvelously',
        'extraordinarily',
        'splendidly',
        'gloriously',
        'divinely',
        'sensationally',
        'wonderfully',
        'fabulously',
        'fantastically',
        'delectably',
        'deliciously'
    },

    'bad_intense': {
        'badly',
        'dismally',
        'disappointingly',
        'unfortunately'
    },

    'physical_intense': {
        'physically',
        'painfully',
        'viscerally',
        'sorely',
        'excruciatingly'
    },

    'epistemic': {
        # 'positively',
        'surely',
        'certainly',
        'actually',
        'definitely',
        'undoubtedly',
        'incontravertably',
        'undeniably',
        'indubitably',
        'doubtless',
        'certifiably',
        'veritably',
        'verifiably',
        'truly',
        'honestly',
        'genuinely'
    },

    'reporting': {
        'apparently',
        'seemingly',
        'reportedly',
        'ostensibly',
        'supposedly',
        'supposed',
        'allegedly',
        'tentatively',
        'potentially',
        'evidently',
        'perceived',
        'theoretically',
        'hypothetically'
    },

    'serious_intense': {
        'seriously',
        'sincerely',
        'severely',
        'earnestly',
        'hopelessly',
        'miserably',
        'desperately',
        'depressingly',
        'sadly',
        'profoundly',
        'strictly',
        'rigidly'
    },
    'time': {
        'eternally',
        'always',
        'infinitely',
        'forever',
        'already',
        'eventually',
        'now',
        'still',
        'soon',
        'previously',
        'formerly',
        'yet',
        'recently',
        'instantly'
    },
    'observable': {
        'obviously',
        'notably',
        'clearly',
        'visibly',
        'audibly',
        'blatantly',
        'flagrantly',
        'openly',
        'deliberately',
        'distinctly',
        'intentionally',
        'decidedly',
        'uniquely',
        'significantly',  # not sure this is where this goes
    },

    'fear_intense': {
        'horribly',
        'frightfully',
        'scarily',
        'creepily',
        'eerily',
        'spookily',
        'terribly',
        'dreadfully',
        'dangerously',
        'alarmingly',
        'suspiciously',
        'awfully',
        'fiercely',
        'competitively'
    },
    'consume_intense': {
        'insatiably',
        'voraciously',
        'greedily'
    },

    'curse_intense': {
        'fucking',
        'freaking',
        'damned',
        'bloody'
    },
    'taboo_intense': {
        'disgustingly',
        'grotesquely',
        'morbidly',
        'terminally',
        'fatally',
        'sickeningly',
        'maddeningly',
        'brutally',
        'violently',
        'belligerantly'
    },
    'round-up_intense': {
        'virtually',
        'practically',
        'essentially',
        'basically'
    },
    'absurd_intense': {
        'peculiarly',
        'strangely',
        'freakishly',
        'freakily',
        'weirdly',
        'oddly',
        'ridiculously',
        'bizarrely',
        'absurdly',
        'curiously'
    },

    'crazy_intense': {
        'crazy',
        'crazily',
        'insanely',
        'madly',
        'wildly'
    },

    'expectation_intense': {
        'incredibly',
        'unbelievably',
        'indescribably',
        'unfathomably',
        'impossibly',
        'inutterably',
        'unspeakably',
        'remarkably',
        'exceptionally',
        'unusually',
        'unexpectedly',
        'surprisingly',
        'considerably'
    },

    'unease_intense': {
        'disconcertingly',
        'troublingly',
        'worryingly',
        'disturbingly',
        'alarmingly'
    },

    'excess_intense': {
        'inordinately',
        'excessively',
        'overly',
        'overwhelmingly',
        'intolerably',
        'unacceptably'
    },

    'max_intense': {
        # 'utterly',
        'completely',
        'totally',
        'maximally',
        'perfectly',
        'entirely',
        'thoroughly'
    },

    # Morzycki's EDM
    'EDM_Morzycki': {
        'simply',
        'just',
        'positively',
        'absolutely',
        'downright',
        'outright',
        'flat-out',
        'full-on',
        'out-and-out',
        'straight-up',
        'balls-out'
    },

    # M-modifiers (Solt & Wilson 2021)
    'Mmod_SoltWilson': {
        'pretty',
        'fairly',
        'rather',
        'somewhat',
        'kinda',
        'sorta'
    },

    # NegPol Triggers
    'negative': {
        'scarcely',
        'barely',
        'hardly',
        'rarely',
        'no',
        'not',
        'never'
    },

    # minimal pairs?
    'positive': {
        'always',
        'some',
        'often',
        'frequently',
        'normally',
        'usually',
        'typically',
        'commonly'
    },

    # NPI or "rescuer"
    'NPS': {
        'yet',
        'ever',
        'exactly'
    },

    'PS_rescuer': {
        'even',
        'only',
        'enough',
        'too'
    },

    'PPS': {
        'pretty',
        'fairly',
        'rather',
        'somewhat',
        'kinda',
        'sorta',
        'utterly'  # ? include this?
    },
}

# ADV_OF_INTEREST.update({f'{k}_sample': set(v)
#                        for k, v in SAMPLE_ADV.items() if not k.startswith('compar')})

ADJ_BY_SCALE = {
    'NONGRADABLE': {'dead',
                    'alive',
                    'existing',
                    'extinct',
                    'pregnant',
                    # Kennedy 2007
                    'wooden',
                    'hand-made',
                    'geological',
                    'locked'
                    },

    'OPEN': {'big',
             'large',
             'small',
             'cheap',
             'deep',
             'shallow',
             'fat',
             'thin',
             'long',
             'short',
             'tall',
             'rich',
             'poor',
             'strong',
             'weak',
             'wide',
             'narrow',
             'loud',
             'quiet',
             'soft',
             'hard',
             'high',
             'low',
             # Kennedy 2007
             'expensive',
             'inexpensive',
             'energetic',
             'lethargic',
             'likely',
             'unlikely'
             },

    # lower closure ==> can be modified by "slightly"
    'LOWER_CLOSED': {'bent',
                     'bumpy',
                     'crooked',
                     'dangerous',
                     'dirty',
                     'impure',
                     'incomplete',
                     'wet',
                     'rough',
                     # kennedy 2007
                     'bent', 'bumpy', 'dirty', 'worried'
                     },

    # upper closure ==> can be modified by "perfectly"
    'UPPER_CLOSED': {'straight',
                     'smooth',
                     'safe',
                     'clean',
                     'pure',
                     'complete',
                     'dry',
                     'smooth',
                     # Kennedy 2007
                     'uncertain', 'dangerous', 'impure', 'inaccurate',
                     'straight', 'flat', 'clean', 'unworried'},

    'TOTALLY_CLOSED': {'open',
                       'closed',
                       'full',
                       'empty',
                       'opaque',
                       'transparent',
                       'exposed',
                       'hidden',
                       'covered'
                       'uncovered'}
}


UNCLASSIFIED_SCALAR_ADJ = {
    # Tessler & Franke 2019
    'affectionate', 'unaffectionate', 'cold', 'ambitious', 'unambitious', 'lazy', 'attractive', 'unattractive', 'ugly', 'educated', 'uneducated', 'ignorant', 'forgiving', 'unforgiving', 'resentful', 'friendly', 'unfriendly', 'mean', 'generous', 'ungenerous', 'stingy', 'happy', 'unhappy', 'sad', 'honest', 'dishonest', 'deceitful', 'intelligent', 'unintelligent', 'stupid', 'interesting', 'uninteresting', 'boring', 'kind', 'unkind', 'cruel', 'mature', 'immature', 'childish', 'patriotic', 'unpatriotic', 'traitorous', 'polite', 'impolite', 'rude', 'rational', 'irrational', 'crazy', 'reliable', 'unreliable', 'flaky', 'resourceful', 'unresourceful', 'wasteful', 'sincere', 'insincere', 'fake', 'tolerant', 'intolerant', 'bigoted',   'attractive', 'unattractive', 'beautiful', 'ugly', 'educated', 'uneducated', 'brave', 'cowardly', 'friendly', 'unfriendly', 'fat', 'skinny', 'happy', 'unhappy', 'hard-working', 'lazy', 'honest', 'dishonest', 'loud', 'quiet', 'intelligent', 'unintelligent', 'proud', 'humble', 'interesting', 'uninteresting', 'rich', 'poor', 'mature', 'immature', 'strong', 'weak', 'polite', 'impolite', 'tall', 'short', 'successful', 'unsuccessful',

    'wise', 'foolish',
    'awake', 'asleep'
    'intelligent', 'brilliant'

}

LEXICAL_EXTREME_ADJ = {
    # Morzycki 2012 p. 574
    'fantastic',
    'wonderful',
    'fabulous',
    'gorgeous',
    'resplendent',
    'magnificent',
    'glorious',
    'sumptuous',
    'spectacular',
    'outstanding',
    'tremendous',
    'huge',
    'gigantic',
    'ginormous',
    'mammoth',
    'colossal',
    'tremendous',
    'enormous',
    'monumental',
    'minuscule',
    'tiny',
    'microscopic',
    'minute',
    'grotesque',
    'delicious',
    'scrumptious',
    'idiotic',
    'inane',
    'destitute',
    'penniless',
    'terrified',
    'horrified',
    'obese',
    'phenomenal',
    'sensational',
    'marvelous',
    'superb',
    'unflappable',
    'amateurish',
    'excellent',
    'terrific',
    'monstrous',
    'extraordinary',
    'hideous',
}
CONTEXTUAL_EXTREME_ADJ = {
    # Morzycki 2012 p. 574
    'brilliant',
    'certain',
    'obvious',
    'dangerous',
    'reckless',
    'infuriating',
    'obscene',
    'offensive',
    'insulting',
    'ridiculous',
    'absurd',
    'evil',
    'contemptible',
    'stupid',
    'drunk',
    'dead',
    'ugly',
    'dumb',
    'rich',
    'loaded',
    'hopeless',
    'calm',
    'outrageous',
    'incompetent',
}


# From Kennedy 2007 p. 34
# (62) Open scales
#   a. ??perfectly/??slightly {tall, deep, expensive, likely}
#   b. ??perfectly/??slightly {short, shallow, inexpensive, unlikely}
# (63) Lower closed scales
#   a. ??perfectly/slightly {bent, bumpy, dirty, worried}
#   b. perfectly/??slightly {straight, flat, clean, unworried}
# (64) Upper closed scales
#   a. perfectly/??slightly {certain, safe, pure, accurate}
#   b. ??perfectly/slightly {uncertain, dangerous, impure, inaccurate}
# (65) Closed scales
#   a. perfectly/slightly {full, open, opaque}
#   b. perfectly/slightly {empty, closed, transparent}
