#!/bin/bash
# condacheck.sh

echo "Checking for requirements..."

# TODO : see if this is actually relevant for off-cluster
#! must create `sanpi` env from yml file first
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate sanpi
conda config --append channels conda-forge
conda config --append channels pyconll
conda config --set pip_interop_enabled true

which cc || sudo apt-get install build-essential

pypackages=('pyconll' 'pandas' 'scipy' 'more-itertools')

for p in "${pypackages[@]}"; do
  echo "> ${p}"
  pip show ${p} || conda install ${p}
  echo ""
done

echo "# opam installs"
if [[ ! `which grew` ]]
then
  echo "installing grew..."

  shpackages=('opam' 'wget' 'm4' 'unzip' 'curl' 'bubblewrap')
  for p in "${shpackages[@]}"; do
    echo "> ${p}"
    which ${p} || conda install ${p}
    echo ""
  done


  if [[ ! `which bubblewrap` ]]; then
    conda install bubblewrap
  fi

  if [[ ! $(echo "`opam --version`") =~ 2.* ]]
  then
    echo "opam version obsolete"
    conda update opam=2.*
  fi

  echo "opam init"
  opam init

  echo "opam switch create 4.14.1 4.14.1"
  opam switch create 4.14.1 4.14.1
  echo "eval $(opam env --switch=4.14.1)"
  eval $(opam env --switch=4.14.1) 

  # if [[ "`ocamlc -v | cut -d " " -f 5 | head -1`" -le 4.1 ]]; then
  #   echo "opam switch create 4.13.1 4.13.1" 
  #   opam switch create 4.13.1 4.13.1
  #   echo "eval $(opam env --switch=4.13.1)"
  #   eval $(opam env --switch=4.13.1) 
  # fi

  echo "opam remote add grew \"http://opam.grew.fr\""
  opam remote add grew "http://opam.grew.fr"
  opam repository add grew --all-switches --set-default
  echo "opam install grew grewpy"
  opam install grew grewpy
  pip install grew

 if [[ $(echo "`grew version | cut -d " " -f 2 | head -1`") != "1.10.0" ]]; then
  echo "grew installation is out of date. Upgrading..."
  echo "updating prerequisites..."
  echo "apt-get update && apt-get upgrade"
  (apt-get update && apt-get upgrade ) || echo "Insufficient permissions to update prerequisites. In case of error, contact admin."

  if [[ ! $(echo "`opam --version`") =~ 2.* ]]
  then
    echo "opam installation is out of date. Updating."
    conda update opam=2.*
  fi

  echo "opam init"
  opam init

  echo "opam switch create 4.14.1 4.14.1"
  opam switch create 4.14.1 4.14.1
  echo "eval $(opam env --switch=4.14.1)"
  eval $(opam env --switch=4.14.1) 

  echo "opam update"  
  opam update
  echo "opam upgrade"
  opam upgrade
  echo "pip3 install grew --upgrade"
  pip install grew --upgrade
  
fi

echo "making sure python module is installed"
pip3 install grew

echo "$(echo "`grew version | tail -1`"), located in $(echo "`which grew`")"