from sys import argv

import stanza

_DOC2CONLL_TEXT = stanza.utils.conll.CoNLL.doc2conll_text

def _parse_sent():
    """
    Parses a sentence using the stanza NLP pipeline and prints the CoNLL-U formatted output.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Examples:
        >>> _parse_sent()
        Loading dependency parsing pipeline...
        This is a sentence.
        1   This    this    DET DT  Number=Sing|PronType=Dem    2   det _   _
        2   is  be  AUX VBZ Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin 0   root    _   _
        3   a   a   DET DT  Definite=Ind|PronType=Art    4   det _   _
        4   sentence    sentence    NOUN    NN  Number=Sing _   2   nsubj   _   _
        5   .   .   PUNCT   .   _   2   punct   _   _

    """
    NLP = get_nlp_pipeline()

    # [ ] update to use `argparse` module
    sentence = argv[1]

    # [ ] update to parse multiple sentences with single model load
        #^ as `while` loop with stdin input
        #^ or from text file of sentences
        #^ or just as `list` of strings instead of single string input
    doc = NLP(sentence)
    conllu = _DOC2CONLL_TEXT(doc)
    
    # [ ] update to write to file (path designated by argument)
    print(conllu[:-1])

def get_nlp_pipeline():
    """
    Returns a stanza NLP pipeline for English.

    Args:
        None

    Returns:
        NLP (stanza.Pipeline): The stanza NLP pipeline.

    Raises:
        stanza.pipeline.core.ResourcesFileNotFoundError: If the language model is not found.

    Examples:
        >>> get_nlp_pipeline()
        <stanza.pipeline.core.Pipeline object at 0x7f9e3e7e6a90>

    """
    try:
        NLP = stanza.Pipeline(
            lang='en',
            processors='tokenize,pos,lemma,depparse')
    except stanza.pipeline.core.ResourcesFileNotFoundError:
        stanza.download('en')
        NLP = stanza.Pipeline(
            lang='en',
            processors='tokenize,pos,lemma,depparse')
    return NLP

if __name__ == '__main__':
    _parse_sent()