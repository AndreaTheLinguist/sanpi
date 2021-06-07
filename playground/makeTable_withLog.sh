#!/bin/env bash
# makeTable.sh


echo "Arguments provided:" "$@"

if [ "$1" == "-h" ]; then
  echo "Script to run all scripts for single AdvAdj pattern and single corpus chunk."
  echo "Usage: `basename $0` [conlldir=path patternfile=path jsondir=path outputprefix=string]"
  echo "Note: script `basename $0` intended to be run from level above 'script/' directory. jsondir also expects form of <sentence data>.<pattern key>"
  exit 0
fi


# conll dir (path) = "$1"
# pattern file (path) = "$2"
# jsondir dir name (str) = "$3"
# outputprefix (str) = "$4"

echo "directory of conllu files... $1"
echo "path to pattern file... $2"
echo "directory of grew corpus hits in json format... $3"
echo "string to prefix to final freq/<>_hits.csv table... $4"
echo

read -p "Are all arguments correct? y/n " -r -n 1

echo  
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

exec   > >(tee -ia make_$4.log)
exec  2> >(tee -ia make_$4.log >& 2)
exec 19> make_$4.log

export BASH_XTRACEFD="19"
set -x

python3 ./script/grewSearchDir.py $1 $2 $3 && python3 ./script/FillJson.py -c $1 -r $3 && python3 script/tabulate.py -t -p $3 -o $4

echo
date -ud "@$SECONDS" "+Total time to create hits/$4_hits.csv: %H:%M:%S"

