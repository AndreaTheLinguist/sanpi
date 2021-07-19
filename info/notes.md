# To Do and Notes

## start with

- [x] debug dataframe NaN calculated cells
- [ ] calculate divergence between simplest distinctions
  - [x]  ~~write script to process pandas.Series as probability distributions~~ uneccessary with `entropy()` (below)
  - [ ] read up on KL divergence more
  - [ ] positive || negative, "test" || positive/negative
  - [ ] coding cost, information theory KL divergence
  - [x] write/find KL divergence function
    --> __*bingo!*__ `scipy.stats.entropy(p, q, base=2)`
- [x] separate uncertain-polarity contexts from others for testing purposes
- [x] add sample files with minimum count threshold (=5?)
- [ ] update scripts on Kay
- [ ] calculate divergence between test contexts and known contexts
- [ ] write more test context patterns

## meeting notes

multinomial stats to augment actual occurence of data
should be large effect size

## Up next

- [ ] read *The Pile* corpus paper (in `zotero_files/`)
- [ ] revisit other distance/divergence metrics in `scipy`
- [ ] check out `scikit` as well
- [ ] plot some data using `matplotlib` or `pandas.plot`
- [ ] adapt `tabulateHits.py` to output subdirs
- [ ] adapt `generatePatFiles.py` to output subdirs
- [x] adapt `processTables.py` to expect subdirectories
- [ ] run less restrictive basic patterns on kay
- [ ] make jupyter notebook (or at least markdown file) for pipeline? e.g. how to run all the scripts with some sample data?
- [ ] determine contexts to run and discuss in syntax chapter: include locality constraints
- [ ] convert more contexts to grew-match pattern specifications
- [ ] patterns for NPIs in same contexts
- [ ] revisit corpus duplicates errors: bug in `cleanConlls.py`?
- [x] create bash script to run all python code? e.g. grewSearchDir -> fillJson --> tabulate --> future comparison script?
- [ ] run patterns
- [x] ~~write scipt to compare new simplified count csv's~~
- [x] ~~determine naming schema for contexts-- create all contexts/patterns before naming?~~
- [x] write script to pull patterns from `pat_notes.md` rather than from individual `.pat` files
- [x] add log output for all outputs skipped due to errors
- [x] ~~but also fix encoding/decoding errors!~~
- [x] add full time spent output to shell script
- [x] figure out how data works with Evert dissertation
- [x] repeated documents in conll files!!!
- [x] alter `tabulate.py` output
- [x] clean conllu files
- [x] edits to `tabulate.py` output:
  - [x] add field for combined `hit_id` (sent_id + adv_id)
  - [x] ~~add field for `pattern` filename?~~
    - [x] ~~remove extra whitespace characters from `sent_text`~~

## old

- [x] figure out R ucs toolkit and get plots of initial dataset
- [ ] clean up workspace on kay (only relevant files/folders)

- [x] revise output for make-tables to have lines like `<context> \t <adv, adj>` for each instance
  - [x] create new grew patterns to get right sets of json files: need positive context to be basic pattern with relevant trigger filtered out (use `without:` clause)
  - [x] need to update printing script to concatonate json pairs (with and without relevant trigger)
- [x] settle on initial set of contexts/searches
- [x] read German NPI papers that use scp
  - manual verification of NPIs still required
  - exact specification of known downward entailing operators
  - use ucs to get **t-score, log likelihood, chi-squared, poisson, and z-score**
  - some ling processing, but only percentage of neg contexts occurred in is releveant for this project (i.e. no translation data)
- [x] <http://www.collocations.de/UCS/tron-one-minute-guide.html>  try ucs tables
  - [x] get all pair-hits of ADV ADJ for pattern
  - [x] pipe `ADV \t ADJ \n` output to `ucs-make-tables -v`
- [x] look at corpus study stats paper file:///C:/Users/Andrea/Downloads/cantos-2018-lexical.pdf
- [x] fixing encoding error in tabulate for p1 outputs! (remember server `tabulate.py` has `print()` statement)

## tabled

- [ ] ucs needs annotation data for plots: get annotations
  - [ ] write script to add annotations to colloc tokens in json files
  - [ ] run script on with-/without-not data from kay
- [ ] run some simplified searches with bare adjective predicates, rather than adverbially modified cases (too much data??)
- [ ] ~~use simpleConllRead function to either output and read in or call from other scripts? want to use it for:~~
  - [ ] adding preceding and following sentences to the reorganized json files
  - [ ] filter out repeated/duplicated documents in conll files and either skip when processing or rewrite files? (making conll smaller would help with future searches, both in processing time and data accuracy)
- [ ] too many hits to just start annoating at random. Need to sort/filter in some way
  - sort by total collocate frequency (f2) or by association measure ranks?
  - should collocates only in one context be ignored?
  - should I only do first x for any mod pair in each context? would that create incomplete values for ucs/R table?
  - create new json files with hits for all of mod pair? <-- separate script to run on every json directory? and create index file to more easily and reliably pull up correct data for specfic mod pair
- [ ] determine how to format data to use with ucs
