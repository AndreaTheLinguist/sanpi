#!/bin/env bash
# makeTable.sh


echo "Arguments provided:" "$@"

if [ "$1" == "-h" ]; then
  echo "Script to run all scripts for pattern directory and single corpus chunk."
  echo "Usage: `basename $0` [conlldir=path patternsdir=path (--log)]"
  echo "if --log is included, script creates a log file of the form make_[context].log"
  
  exit 0
fi
  
# conll dir (path) = "$1"
# pattern file dir (path) = "$2"
# log option = "$5"

echo "directory of conllu files... $1"
echo "path to pattern dir... $2"
echo

read -p "Are all arguments correct? y/n " -r -n 1

echo  
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

corpus=$(echo "$1" | cut -f 1 -d '.' | cut -f 1 -d '/')
echo "Corpus segment: $corpus"

patterns=$(echo "$2*")
# echo $patterns
for pat in $patterns
do
  
  context=$(echo "$pat" | cut -f 1 -d '.' | cut -f 3 -d '/')
  jsondir=$(echo "data/$corpus.$context")
  hitslabel=$(echo $corpus"_"$context)

  if [ "$3" == "--log" ]; then   
    exec   > >(tee -ia make_$context.log)
    exec  2> >(tee -ia make_$context.log >& 2)
    exec 19> make_$context.log
    export BASH_XTRACEFD="19"
    set -x
    echo "Log will be saved to make_$context.log"
  fi

  echo "Pattern file path: $pat"
  echo "Context: $context"
  echo "json output dir: $jsondir"
  echo "hits file prefix: $hitslabel"

  python3 ./script/grewSearchDir.py $1 $pat $jsondir && python3 ./script/FillJson.py -c $1 -r $jsondir && python3 script/tabulateHits.py -t -p $jsondir -o $hitslabel
done 

echo
date -ud "@$SECONDS" "+Total time to create hits/$4_hits.csv: %H:%M:%S"

