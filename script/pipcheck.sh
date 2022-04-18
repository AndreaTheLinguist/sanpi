#!/bin/bash
# pipcheck.sh

echo "Checking for requirements..."

if [[ $(echo "`which python3 -m pyconll`" ) == "" ]]
then 
  echo "pyconll package not found:"
  echo "conda install pyconll -c pyconll"
  pip3 install pyconll
  echo " "
else
  echo "pyconll located in $(echo "`which python3 -m pyconll`")"
fi

if [[ $(echo "`which python3 -m pandas`" ) == "" ]]
then
  echo "pandas package not found:"
  echo "pip3 install pandas"
  pip3 install pandas
else
  echo "pandas located in $(echo "`which python3 -m pandas`")"
fi


if [[ $(echo "`which grew`" ) == "" ]]
then
  echo "grew not found. Installing:"

  if [[ $(echo "`which opam`" ) == "" ]]
  then
    # using apt-get requires root
    # echo "apt-get install opam"
    # apt-get install opam
    # curl shell install should not require root
    echo "bash -c \"sh <(curl -fsSL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)\""
    bash -c "sh <(curl -fsSL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)"
  fi

  echo "opam init"
  opam init

  echo "eval opam env"
  eval opam env

  if [[ $(echo "`ocamlc -v | cut -d " " -f 5 | head -1`") < 4.1 ]]
  then
    echo "opam switch create 4.13.1"
    opam switch create 4.13.1
    echo "eval $(opam env --switch=4.13.1)"
    eval $(opam env --switch=4.13.1) 
  fi

  echo "opam remote add grew \"http://opam.grew.fr\""
  opam remote add grew "http://opam.grew.fr"
  opam repository add grew --all-switches --set-default
  echo "opam install grew grewpy"
  opam install grew grewpy
fi

if [[ $(echo "`grew version | cut -d " " -f 2 | head -1`") < 1.7 ]]
then
  echo "grew version is out of date. Upgrading..."
  echo "opam update"
  opam update
  echo "opam upgrade"
  opam upgrade
  echo "pip3 install grew --upgrade"
  pip3 install grew --upgrade
fi

echo "$(echo "`grew version | tail -1`"), located in $(echo "`which grew`")"
echo "\`\`\`"