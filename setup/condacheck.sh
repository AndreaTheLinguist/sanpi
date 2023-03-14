#!/bin/bash
# condacheck.sh
VERSION="1.11.0"
ENV=${1:-"sanpi"}
echo "Checking ${ENV} env for requirements:"
OPTION=${2:-""}
SETUP_DIR="${0%/*}"
if [[ ! -d ${SETUP_DIR} ]]; then
  SETUP_DIR="$(pwd)"
fi
LOG_DIR="${SETUP_DIR}/env-check_logs"
if [[ ! -d $LOG_DIR ]]; then
  mkdir $LOG_DIR
fi
LOG_PATH="${LOG_DIR}/${ENV}_`date +'%Y-%m-%d_%R'`.log"
echo -e "> log will be saved to: ${LOG_PATH}\n..."
exec 1>${LOG_PATH} 2>&1
echo "Checking ${ENV} env for requirements..."
echo "Started at $(date)"

# TODO : see if this is actually relevant for off-cluster
#! must create `sanpi` env from yml file first
# activate conda environment
eval "$(conda shell.bash hook)"
echo "conda activate ${ENV}" 
conda activate ${ENV} || echo -e "${ENV} env does not exist! Create by running\n $ conda env create -f ${SETUP_DIR}/${ENV}_env.yml "
conda info | head -3 | tail -2

ACTIVE_PATH=$(conda info | head -3 | tail -1 | cut -d ":" -f 2 | tr -d "[:space:]")

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

#! 'librsvg2-bin' is supposedly required, but cannot get it through conda
#   however, it seems to be for generating svg images
#   "librsvg2-bin - command-line utility to convert SVG files"
#? maybe needed but wasn't specificed in grew docs...: 'libcairo2-dev'
shpackages=('opam' 'wget' 'm4' 'unzip' 'curl' 'pkg-config')

if [[ $ENV == "parallel-sanpi" ]]; then
  shpackages=("${shpackages[@]}" "parallel")
  echo "${shpackages[@]}"
fi

for p in "${shpackages[@]}"; do
  echo -e "\n> ${p}"
  ( which ${p} || conda install -y ${p} ) || echo "⚠️ failed to install $p"
done

#// # BUBBLE="$(conda list bubblewrap)"
#// if [[ $(ls ${ACTIVE_PATH}/**/*bubblewrap*) ]]; then
#//   conda list bubblewrap
#// else
#//   echo "conda install bubblewrap"
#//   conda install bubblewrap
#// fi

echo -e "\n### checking opam installs ###"
if [[ -z "`which grew`" || $OPTION == '--force' ]]; then
  echo "installing grew..."

  #*install or upgrade opam (conda)
  opam --version || conda install -y opam=2.*
  if [[ ! $(echo "`opam --version`") =~ 2.* ]]; then
    echo "opam version obsolete"
    conda update -y opam=2.*
  fi

  echo "opam -y init"
  opam -y init

  # echo 'eval $(opam env --switch=4.14.0) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0)'
  echo 'eval $(opam env --switch=4.14.0 --set-switch) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0 --set-switch)'
  eval $(opam env --switch=4.14.0 --set-switch) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0 --set-switch)

  # if [[ "`ocamlc -v | cut -d " " -f 5 | head -1`" -le 4.1 ]]; then
  #   echo "opam switch create 4.14.0 4.14.0" 
  #   opam switch create 4.14.0 4.14.0
  #   echo "eval $(opam env --switch=4.14.0)"
  #   eval $(opam env --switch=4.14.0) 
  # fi
  opam repository set-url default https://opam.ocaml.org
  opam -y update && opam -y upgrade

  #* install grew (opam)
  echo -e "\nopam remote add grew \"http://opam.grew.fr\""
  opam -y remote add grew "http://opam.grew.fr"
  opam -y repository add grew --all-switches --set-default

  echo -e "\nopam -y install grew"
  opam -y install grew
  eval $(opam env)
  eval $(opam env)
  grew version || opam -y install grew

  #* install grewpy_backend (opam)
  echo -e "\nopam -y update && opam -y install grewpy_backend"
  opam -y update && opam -y install grewpy_backend
  eval $(opam env)
  
  #* install grewpy (pip)
  echo -e "\npip3 install grewpy"
  pip3 install grewpy --upgrade

elif [[ `grew version | tail -1 | cut -d ' ' -f 2` != "${VERSION}" ]]; then
# elif [[ $(echo "`grew version | cut -d ' ' -f 2 | head -1`") != "${VERSION}" ]]; then
  echo "grew installation is out of date. Upgrading..."
  echo "updating prerequisites..."
  echo "sudo apt-get update && sudo apt-get upgrade"
  ( sudo apt-get update && sudo apt-get upgrade ) || echo -e "\nInsufficient permissions to update prerequisites. In case of error, contact admin."

  if [[ ! $(echo "`opam --version`") =~ 2.* ]]; then
    echo "opam installation is out of date. updating..."
    conda update -y opam=2.*
  fi

  echo -e "\nopam -y init"
  opam -y init

  # echo -e '\neval $(opam env --switch=4.14.0) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0)'
  echo 'eval $(opam env --switch=4.14.0 --set-switch) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0 --set-switch)'
  eval $(opam env --switch=4.14.0 --set-switch) || opam switch create 4.14.0 4.14.0 && eval $(opam env --switch=4.14.0 --set-switch)
  
  #* update opam package list
  opam repository set-url default https://opam.ocaml.org
  echo "opam -y update && opam -y upgrade"  
  opam -y update && opam -y upgrade

  #* upgrade grew (opam)
  echo -e "\nopam -y upgrade grew"
  # TODO: don't think this is reached every time it should be
  opam -y upgrade grew
  eval $(opam env)

  #* upgrade grewpy_backend (opam)
  echo -e "\nopam -y install grewpy_backend"
  opam -y install grewpy_backend || opam -y upgrade grewpy_backend
  eval $(opam env)

  #* upgrade grewpy (pip3)
  echo -e "\npip3 install grewpy --upgrade"
  pip3 install grewpy --upgrade
  
fi

echo -e '\ngrewpy_backend version should be >= 0.1.3'
if [[ -z "`opam list | grep grewpy`" ]]; then
  opam -y install grewpy_backend
  eval $(opam env)
else
  echo "opam list | grep grewpy"
  opam list | grep grewpy
fi

echo -e '\ngrewpy should be >= 0.1.2'
echo "pip3 show grewpy"
pip3 show grewpy || pip3 install grewpy


echo "`grew version | tail -1`, located in `which grew`"

echo "Finished at $(date)"