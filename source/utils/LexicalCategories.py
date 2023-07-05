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
        'alive', 'dead',
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
        'relatively',
        'as'
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

PPI_ADVERBS = [
    'pretty',
    'fairly',
    'rather',
    'somewhat',
    'kinda',
    'sorta'
]

ADV_OF_INTEREST = [
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

    'exactly',
    'precisely',

    'more',
    'less',
    'most',
    'least',

    'very',
    'really',
    'quite',

    'hugely',
    'largely',
    'greatly',
    'highly',
    'deeply',
    'widely',
    'strongly',
    'super',

    'particularly',
    'especially',
    'entirely',
    'extremely',
    'notably',

    'amazingly',
    'heartily',
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
    'deliciously',

    'positively',
    'surely',
    'certainly',
    'actually',
    'definitely',
    'undoubtedly',
    'certifiably',
    'veritably',
    'verifiably',
    'truly',
    'honestly',
    'genuinely',

    'seriously',
    'sincerely',
    'earnestly',
    'hopelessly',

    'obviously',
    'clearly',
    'blatantly',
    'openly',

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
    'fucking',

    'disgustingly',
    'morbidly',
    'fatally',
    'miserably',
    'maddeningly',
    'violently',

    'peculiarly',
    'strangely',
    'freakishly',
    'weirdly',
    'oddly',
    'ridiculously',
    'bizarrely',
    'absurdly',

    'crazy',
    'crazily',
    'insanely',
    'madly',
    'incredibly',
    'unbelievably',
    'impossibly',

    'disconcertingly',
    'troublingly',
    'worryingly',
    'disturbingly',

    'inordinately',
    'excessively',
    'overly',
    'overwhelmingly',
    'intolerably',
    'unacceptably',

    'utterly',
    'completely',
    'totally',
    'maximally',
    'perfectly',

    # Morzycki's EDM
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
    'balls-out',

    # M-modifiers (Solt & Wilson 2021)
    'pretty',
    'fairly',
    'rather',
    'somewhat',
    'kinda',
    'sorta',

    # NegPol Triggers
    'scarcely',
    'barely',
    'hardly',
    'rarely',
    # 'no',
    'not',
    'never',

    # minimal pairs?
    'always',
    'some',
    'often',
    'frequently',
    'normally',
    'usually',
    'typically',
    'commonly',

    # NPI or "rescuer"
    'yet',
    'even',
    'only',
    'enough',
    'too',
]


ADJ_BY_SCALE = {
    'NONGRADABLE': {'dead',
                    'alive',
                    'existing',
                    'extinct',
                    'pregnant'
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
             'low'
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
