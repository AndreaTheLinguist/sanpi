#!/bin/env bash
# makeTable.sh

echo "Arguments provided:" "$@"

if [ "$1" == "-h" ]; then
  echo "Script to run all scripts for single AdvAdj pattern and single corpus chunk."
  echo "Usage: `basename $0` [conlldir=path patternfile=path jsondir=path outputprefix=string]"
  echo "Note: script `basename $0` intended to be run from level above 'script/' directory. jsondir also expects form of <sentence data>.<pattern key>"
  exit 0
fi


# conll = "$1"
# pattern = "$2"
# jsondir = "$3"
# outputprefix = "$4"

echo "directory of connll files... $1"
echo "path to pattern file... $2"
echo "directory of grew corpus hits in json format... $3"
echo "string to prefix to final freq/<>_counts.csv table... $4"
echo

read -p "Are all arguments correct? y/n " -r -n 1

echo  
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

python3 ./script/grewSearchDir.py $1 $2 $3 && python3 ./script/FillJson.py -c $1 -r $3 && python3 script/tabulate.py -p $3 -o $4

