#!/bin/bash
# condacheck.sh
ENV=${1:-sanpi}
SETUP_DIR=${0%/*}
if [[ -f ${SETUP_DIR} ]]; then
  SETUP_DIR="$(pwd)"
fi
echo "Checking ${ENV} env for requirements"
LOG_PATH=${SETUP_DIR}/${ENV}_check.log
echo -e "> log will be saved to: ${LOG_PATH}\n..."
exec 1>${LOG_PATH} 2>&1
echo "Checking ${ENV} env for requirements..."
echo "Started at $(date)"

# TODO : see if this is actually relevant for off-cluster
#! must create `sanpi` env from yml file first
# activate conda environment
eval "$(conda shell.bash hook)"
echo "conda activate ${ENV} || cat ${SETUP_DIR}/${ENV}_env.yml && conda env create -f ${SETUP_DIR}/${ENV}_env.yml "
conda activate ${ENV} || cat ${SETUP_DIR}/${ENV}_env.yml && conda env create -f ${SETUP_DIR}/${ENV}_env.yml
conda info | head -3 | tail -2

ACTIVE_PATH="$(conda info | head -3 | tail -1 | cut -d ':' -f 2 | tr -d '[:space:]')"

echo -e "\nChecking channel list..."
(conda info | egrep conda-forge) || conda config --append channels conda-forge
(conda info | egrep pyconll) || conda config --append channels pyconll
conda config --set pip_interop_enabled true

which cc || sudo apt-get install build-essential

pypackages=('pyconll' 'pandas' 'scipy' 'more-itertools' 'bubblewrap')

for p in "${pypackages[@]}"; do
  echo -e "\n> ${p}"
  #// pip3 show ${p} || conda install ${p}
  echo "pip3 show ${p} || (ls ${ACTIVE_PATH}/*/*${p}* && conda list ${p}) || conda install -y ${p}"
  pip3 show ${p} || (ls ${ACTIVE_PATH}/*/*${p}* && conda list ${p}) || conda install -y ${p}
done

shpackages=('opam' 'wget' 'm4' 'unzip' 'curl')
for p in "${shpackages[@]}"; do
  echo -e "\n> ${p}"
  which ${p} || conda install -y ${p}
done

#// # BUBBLE="$(conda list bubblewrap)"
#// if [[ $(ls ${ACTIVE_PATH}/**/*bubblewrap*) ]]; then
#//   conda list bubblewrap
#// else
#//   echo "conda install bubblewrap"
#//   conda install bubblewrap
#// fi

echo -e "\n### opam installs ###"
if [[ ! `which grew` ]]; then
  echo "installing grew..."

  if [[ ! $(echo "`opam --version`") =~ 2.* ]]; then
    echo "opam version obsolete"
    conda update -y opam=2.*
  fi

  echo "opam -y init"
  opam -y init

  echo 'eval $(opam env --switch=4.14.0) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0)'
  eval $(opam env --switch=4.14.0) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0)

  # if [[ "`ocamlc -v | cut -d " " -f 5 | head -1`" -le 4.1 ]]; then
  #   echo "opam switch create 4.14.0 4.14.0" 
  #   opam switch create 4.14.0 4.14.0
  #   echo "eval $(opam env --switch=4.14.0)"
  #   eval $(opam env --switch=4.14.0) 
  # fi

  echo "opam remote add grew \"http://opam.grew.fr\""
  opam -y remote add grew "http://opam.grew.fr"
  opam -y repository add grew --all-switches --set-default
  echo "opam install grew grewpy"
  opam -y install grew grewpy
  echo "pip3 install grew"
  pip3 install grew

elif [[ $(echo "`grew version | cut -d ' ' -f 2 | head -1`") != "1.10.0" ]]; then
  echo "grew installation is out of date. Upgrading..."
  echo "updating prerequisites..."
  echo "sudo apt-get update && sudo apt-get upgrade"
  sudo apt-get update && sudo apt-get upgrade || echo -e "\nInsufficient permissions to update prerequisites. In case of error, contact admin."

  if [[ ! $(echo "`opam --version`") =~ 2.* ]]; then
    echo "opam installation is out of date. updating..."
    conda update -y opam=2.*
  fi

  echo -e "\nopam -y init"
  opam -y init

  echo -e '\neval $(opam env --switch=4.14.0) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0)'
  eval $(opam env --switch=4.14.0) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0)


  echo "opam -y update"  
  opam -y update
  echo -e "\nopam -y upgrade"
  opam -y upgrade
  echo -e "\npip3 install grew --upgrade"
  pip3 install grew --upgrade
  
fi

echo "$(echo "`grew version | tail -1`"), located in $(echo "`which grew`")"

Finished at $(date)