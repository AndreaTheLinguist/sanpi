## Installation
I installed grew on kay using opam.  This seems to be a personal installation, this is the philosophy for opam.
However it is set to `a+x`.  

```
which grew
/home/mr249/.opam/4.10.0/bin/grew
-rwxrwxr-x 1 mr249 pug-mr249 5623136 Jun 24 10:16 /home/mr249/.opam/4.10.0/bin/grew
```

Grew is described at [grew.fr/match_doc](http://grew.fr/match_doc/).

## Patterns
`/projects/sem/snpi/grew` is a working directory. `be_adj_adv_not.pat` is a basic pattern.

```
pattern {
  V [lemma="be"];
  NOT [lemma="not"];
  R [upos="ADV"];
  A [upos="ADJ"];
  e1: A -[cop]-> V;
  e2: A -[advmod]-> R;
  e3: A -[advmod]-> NOT;
}
```

It can be run as follows.

```
make be_adj_adv_not.json
grew grep -pattern be_adj_adv_not.pat -i en_pud-ud-test.conllu > be_adj_adv_not.json
```

The result looks like this.

```
[
  {
    "sent_id": "n05008012",
    "matching": {
      "nodes": { "V": "6", "R": "8", "NOT": "7", "A": "9" },
      "edges": {
        "e3": { "source": "9", "label": "advmod", "target": "7" },
        "e2": { "source": "9", "label": "advmod", "target": "8" },
        "e1": { "source": "9", "label": "cop", "target": "6" }
      }
    }
  },
  {
    "sent_id": "n05002015",
    "matching": {
      "nodes": { "V": "8", "R": "4", "NOT": "7", "A": "9" },
      "edges": {
        "e3": { "source": "9", "label": "advmod", "target": "7" },
        "e2": { "source": "9", "label": "advmod", "target": "4" },
        "e1": { "source": "9", "label": "cop", "target": "8" }
      }
    }
  },
...

```

## Fillers and context sentence
The search result does not show the text, or the fillers for the
nodes. These can be recovered from the conllu file
`en_pud-ud-test.conllu`.  Spot checks indicate that the hits are
correct.  *We need software that reads `be_adj_adv_not.json` and
`en_pud-ud-test.conllu`, and fills in values in the json like this.*

```
  {
    "sent_id": "n05008012",
    "text": "As a result, Trump isn't very worried about the Latin American vote at a national level."
    "matching": {
      "nodes": { "V": "6", "R": "8", "NOT": "7", "A": "9" },
      "fillers": { "V": "is", "R": "very", "NOT": "n't", "A": "worried" },
      "edges": {
        "e3": { "source": "9", "label": "advmod", "target": "7" },
        "e2": { "source": "9", "label": "advmod", "target": "8" },
        "e1": { "source": "9", "label": "cop", "target": "6" }
      }
    }
  },

```

## NYT corpora
The NYT corpora need to be trainsformed into the `conll` format,
including the text and sentence ID.  This should be done on Woods,
with an xml awk program similar to the one used to create the cwb
corpora.

