#!/bin/bash
# checkRequirements.sh

echo "Checking for requirements..."
echo "\`\`\`"
if [[ $(echo "`which python3 -m pyconll`" ) == "" ]]
then 
  echo "pyconll package not found:"
  echo "pip3 install pyconll"
  pip3 install pyconll
  echo " "
fi
echo "pyconll located in $(echo "`which python3 -m pyconll`")"

if [[ $(echo "`which python3 -m pandas`" ) == "" ]]
then
  echo "pandas package not found:"
  echo "pip3 install pandas"
  pip3 install pandas
fi
echo "pandas located in $(echo "`which python3 -m pandas`")"

if [[ $(echo "`which grew`" ) == "" ]]
then
  echo "grew not found. Installing:"

  if [[ $(echo "`which opam`" ) == "" ]]
  then
    echo "apt-get install opam"
    # apt-get install opam
    echo "apt-get install wget m4 unzip librsvg2-bin curl bubblewrap"
    # apt-get install wget m4 unzip librsvg2-bin curl bubblewrap
    echo "opam init"
    # opam init
    echo "eval opam env"
    # eval opam env
  fi

  if [[ $(echo "`ocamlc -v | cut -d " " -f 5 | head -1`") < 4.1 ]]
  then
    echo "opam switch create 4.13.1"
    # opam switch create 4.13.1
    echo "eval $(opam env --switch=4.13.1)"
    # eval $(opam env --switch=4.13.1) 
  fi

  echo "opam remote add grew \"http://opam.grew.fr\""
  # opam remote add grew "http://opam.grew.fr"
  # opam repository add grew --all-switches --set-default
  echo "opam install grew grewpy"
  # opam install grew grewpy
fi

if [[ $(echo "`grew version | cut -d " " -f 2 | head -1`") < 1.7 ]]
then
  echo "grew version is out of date. Upgrading..."
  echo "opam update"
  # opam update
  echo "opam upgrade"
  # opam upgrade
  echo "pip3 install grew --upgrade"
  # pip3 install grew --upgrade
fi

echo "$(echo "`grew version | tail -1`"), located in $(echo "`which grew`")"
echo "\`\`\`"