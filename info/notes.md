# Up next: 

- [ ] determine contexts to run and discuss in syntax chapter: include locality constraints
- [ ] convert contexts to grew-match pattern specifications
- [ ] patterns for NPIs in same contexts
- [x] create bash script to run all python code? e.g. grewSearchDir -> fillJson --> tabulate --> future comparison script? 
- [ ] run patterns
- [ ] write scipt to compare new simplified count csv's
- [ ] determine naming schema for contexts-- create all contexts/patterns before naming?
- [ ] figure out how data works with Evert dissertation


# start with:
- [ ] figure out R ucs toolkit and get plots of initial dataset
- [ ] determine how to format data to use with ucs
- [ ] revise output for make-tables to have lines like `<context> \t <adv, adj>` for each instance
    - [ ] create new grew patterns to get right sets of json files: need positive context to be basic pattern with relevant trigger filtered out (use `without:` clause)
    - [ ] need to update printing script to concatonate json pairs (with and without relevant trigger)
- [ ] settle on initial set of contexts/searches
- [x] read German NPI papers that use scp
    - manual verification of NPIs still required
    - exact specification of known downward entailing operators 
    - use ucs to get **t-score, log likelihood, chi-squared, poisson, and z-score**
    - some ling processing, but only percentage of neg contexts occurred in is releveant for this project (i.e. no translation data)
- [x] http://www.collocations.de/UCS/tron-one-minute-guide.html  try ucs tables
    - [x] get all pair-hits of ADV ADJ for pattern 
    - [x] pipe `ADV \t ADJ \n` output to `ucs-make-tables -v`
- [x] look at corpus study stats paper file:///C:/Users/Andrea/Downloads/cantos-2018-lexical.pdf
- [x] fixing encoding error in tabulate for p1 outputs! (remember server tabulate.py has print() statement)