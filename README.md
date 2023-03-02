# SANPI 
**_Scalar Ambiguity of Negative Polarity Inferences_**

## Environment Set Up

1. Install [anaconda](https://docs.anaconda.com/anaconda/install/index.html) if not already installed.

2. From the `setup/` directory, run: 

        $ conda env create -f sanpi_env.yml

   Or from `sanpi/` directory, run: 

        $ conda env create -f setup/sanpi_env.yml

    _For development, use `setup/dev-sanpi_env.yml` instead_

3. To check for remaining required tools, run: 

        $ bash setup/condacheck.sh


## Project Overview

This is a project to collect collocation frequencies of adv-adj pairs, weak NPIs, and strong NPIs under a variety of contexts. 

The `script/` directory contains python code for running grew-match searches, process the hits (output as json files), and run statistical comparisons on the results. Match results can be found in csv tables in `hits/`. Use `bash script/viewHits.sh hits/[filename]` for a reader friendly view of the hits in the command line.

The `sample_data/` directory contains sample csv files of counts and simple statistics on current data (not finalized). Full tables for token information, frequency information of collocation by context, as well as some simple statistics can be located in the source directory as `pkl.gz` files.

The idea is that certain adv-adj pairs which are commonly used to create litotes will have similar distributions to strong NPIs, and perhaps have increased freqency in only a subset of contexts licensing weak NPIs. There is also a question whether certain kinds of adverbs will pattern even more strongly with certain context features than others, showing signs of semi-lexicalized usage.

Corpus frequency data is derived from grew-match searches run on dependency annotated corpora (currently the New York Times, and soon the Associated Press)

## Helpful Links

- [CoNLL-U viewer](https://urd2.let.rug.nl/~kleiweg/conllu/)
- `grew` documentation: 
  - [command line](https://grew.fr/usage/cli/)
  - [pattern syntax](https://grew.fr/doc/request/)
