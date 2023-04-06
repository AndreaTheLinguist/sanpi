#!/bin/env bash
# removeRawJson.sh

echo "Removing .raw.json files from $1"
echo
echo "Files to be removed: "

find $1 -name "*.raw.json" -type f

echo 
echo "Files which will be kept:"

find $1 ! -name '*.raw.json' -type f

echo
read -p "Continue with removal? y/n " -n 1 -r

echo  
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

find $1 -name "*.raw.json" -type f -delete

echo "Files deleted."