#!/bin/bash
# makeTable.sh

echo "Arguments provided:" "$@"

if [[ $1 == "-h" ]]; then
  echo "Script to run all scripts for a single pattern (terminal) directory on single corpus chunk. Pattern directory must contain .pat files. Should be located in Pat/ and named according to the corresponding 'Pat/specs_....md' file's title (top level heading, not filename, though these may be equivalent). This script can be run simultaneously on different pattern directories."
  echo " "
  echo "Usage: $(basename $0) [conlldir=path patternsdir=path (logdir=path)]"
  echo " "
  echo " -> If logdir is included, logs will be saved as [logdir]/[context_group].log. If 'default' is given, following will be used: info/logs/" 
  echo " -> Otherwise, no log file of console output will be saved."
  
  exit 0
fi
  
# conll/corpus dir (path) = "$1"
# pattern file dir (path) = "$2"
# log option = "$3"

echo "directory of conllu files... $1"
echo "directory of pattern files... $2"
# echo "path to logs directory... $3"
echo "optional log output:"
if [[ $3 ]]
then

  if [[ $3 == "default" ]]
  then
    logdir=$(echo "info/logs")
  else
    logdir=$(echo "$3")
  fi

  echo "  + logs will be saved in... $logdir/"
else 
  echo "  - No log directory given -> terminal output log will NOT be saved."
fi

read -p "Are all arguments correct? y/n " -r -n 1

echo  
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  [[ $0 = $BASH_SOURCE ]] && exit 1 || return 1 
  # handle exits from shell or function but don't exit interactive shell
fi

# assign relevant transparent variable for arg input
corpusdir=$(echo $1)
corpus=$(echo "$(basename $corpusdir)" | cut -f 1 -d '.')
patdir=$(echo "$2")
contextgrp=$(echo "$(basename $patdir)")

if [[ $logdir ]]
then   

  if [[ ! -d $logdir ]]
  then 
    mkdir $logdir
  fi
  
  corplogdir=$(echo $logdir/$corpus)

  if [[ ! -d $corplogdir ]]
  then
    mkdir $corplogdir
  fi
  
  logfile=$(echo "$corplogdir/$contextgrp.md")
  >$logfile
  echo "- Log will be saved as $logfile"
  exec >  >(tee -ia $logfile)
  exec 2> >(tee -ia $logfile >&2)

  echo >&2

fi

echo "# Running \`$(dirname $0)/$(basename $0)\`"

# echo "_Checking for required packages..._"
# echo "\`\`\`"
# if [[ $(echo "`which pyconll`" ) == "" ]]
# then 
#   echo "pyconll package not found:"
#   echo "pip3 install pyconll"
#   pip3 install pyconll
#   echo " "
# fi

# if [[ $(echo "`which pandas`" ) == "" ]]
# then
#   echo "pandas package not found:"
#   echo "pip3 install pandas"
#   pip3 install pandas
# fi
# echo "\`\`\`"

echo "## >> Searching \`$corpusdir\` for \`$contextgrp\` patterns"
echo " "
echo "- started by: \`$(whoami)\`"
echo "- run from: \`$(pwd)\`"
echo "- timestamp: \`$(date)\`"
echo " "

if [[ ! -d data ]]
then
  mkdir data
fi

if [[ ! -d hits ]]
then
  mkdir hits
fi

patfiles=$(echo "$patdir*")
patgrp_datadir=$(echo "data/$contextgrp")
hitsdir=$(echo "hits/$contextgrp")
skipgrew=$(echo false )

if [[ ! -d $patgrp_datadir ]]
then
  mkdir $patgrp_datadir
else
  
  relevant=$(echo ` find $patgrp_datadir -type d -name "*$corpus*" `)
  if [[ $relevant ]]
  then
  
    echo "\`\`\`"
    echo "Output directory $patgrp_datadir already exists and contains these relevant files:"
    find $relevant -type f
    echo " "

    echo "* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n)."
    echo " "

    read -p  "--> Run grew search on $corpus again and overwrite any corresponding files? y/n " -r -n 1

    echo  
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
      skipgrew=$(echo true )
      echo "= New $corpus corpus searches will NOT be run. Current files in $patgrp_datadir will be used."
    else
      skipgrew=$(echo false )
      echo "= Corpus $corpus will be searched again. Corresponding files in $patgrp_datadir will be overwritten."
    fi

  fi
fi

echo "\`\`\`"

for pat in $patfiles
do
  
  context=$(echo "$(basename $pat)" | cut -f 1 -d '.')
  echo "## Starting context: \`$context\`"
  echo "- time stamp: \`$(date)\`"

  jsondir=$(echo "$patgrp_datadir/$corpus.$context")
  hitslabel=$(echo "$corpus""_""$context")
  echo "- data directory: \`$jsondir\`"
  echo "- hits table: \`$hitsdir/$hitslabel\`"
  echo "\`\`\`{js}"
  echo "$(cat $pat)"  
  echo "\`\`\`" " "

  echo "\`\`\`" " "

  if [[ $skipgrew == true ]]
  then 

    python3 ./script/FillJson.py -c $corpusdir -r $jsondir && python3 script/tabulateHits.py -p $jsondir -o $hitslabel

  else
    
    python3 ./script/grewSearchDir.py $corpusdir $pat $jsondir && python3 ./script/FillJson.py -c $corpusdir -r $jsondir && python3 script/tabulateHits.py -p $jsondir -o $hitslabel

  fi

  echo "\`\`\`" " "

done 

echo " "
echo "## Finished at: \`$(date)\`"
echo "  + All raw data in \`$jsondir/...\`"
echo "  + All hit tabulations in \`$hitsdir/...\`"
echo 
date -ud "@$SECONDS" "+  + Total time to populate $hitsdir: %H:%M:%S"


