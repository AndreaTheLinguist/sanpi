# To Do and Notes

## start with

- [ ] finalize `tabulateHits.py` changes to use `pandas.json_normalize()`
- [ ] update github
- [ ] update kay
- [ ] iron out template patterns
  - [ ] relay cases
  - [ ] direct cases
  - [ ] neg-raising/transparent cases
  - [ ] mitgated cases
  - [ ] specific problem cases: `without`, `few`
  - [ ] *known* positive cases?
  - [ ] unknown polarity/test cases, e.g.:
    - `if`
    - `before`
    - restriction of $\neg\exists$ quantification
    - restriction of $\forall$ quantification
    - questions
    - comparatives
    - `less than`




## meeting notes

- multinomial stats to augment actual occurence of data
- should be large effect size

## idea notes

+ How to organize patterns and data:

  - patterns specify polarity in context heading (of `pat_notes.md`)
  - to speed up data gathering, could:
    1. split each of the new polarity subdirectories into arbitrary chunks
    2. split subdirs into non-arbitrary chunks also specified in `pat_notes.md`
  - Option 1 would be simplest, though the split would have to be either predetermined (size) 
    or calculated based on number of patterns in subdir
  - Option 2 would be extra work on the front end, but would be more meaningful
    and then could also be used in processing and analysis

## Up next

- [ ] read *The Pile* corpus paper (in `zotero_files/`)
- [ ] revisit other distance/divergence metrics in `scipy`
- [ ] check out `scikit` as well
- [ ] plot some data using `matplotlib` or `pandas.plot`
- [X] adapt `tabulateHits.py` to output subdirs
- [X] adapt `generatePatFiles.py` to output subdirs
- [x] adapt `processTables.py` to expect subdirectories
- [ ] run less restrictive basic patterns on kay
- ~~[ ] make jupyter notebook (or at least markdown file) for pipeline? e.g. how to run all the scripts with some sample data?~~
- [ ] determine contexts to run and discuss in syntax chapter: include locality constraints
- [ ] convert more contexts to grew-match pattern specifications
- [ ] patterns for NPIs in same contexts
- ~~[ ] revisit corpus duplicates errors: bug in `cleanConlls.py`?~~
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
