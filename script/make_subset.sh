#!/bin/bash
# make_subset.sh
# glue script to run 'make_subset_conllus.py' 
#   a little more neatly for more than 1 conllu file at a time
# echo "Input:" "$@"

if [[ $1 == "-h" ]]; then

  echo "shell script to create subsets matching pattern file (only) for all conllu files specified by path (dir or file*)."
  echo "  -> should be run from toplevel of sanpi project ('../sanpi/')"
  echo "  * intended for directory containing .conllu files, but won't crash for direct path to .conllu file"
  echo "  !! CONLLU_PATH must end with '/' to be parsed as directory"
  echo ""
  echo "Usage: (sanpi\$) bash script/$(basename $0) [CONLLU_PATH=path PATTERN_FILE=path]"
  echo "  If arguments are not given, python script (make_subset_conllus.py) defaults to:"
  echo "    CONLLU = ~/data/devel/quicktest.conll/nyt_eng_199912.conllu"
  echo "    PATTERN = Pat/advadj/all-RB-JJs.pat"
  echo "       (will crash with pattern default if not run from dir containing 'Pat/')"
  
  exit 0
fi
set -o errexit
# * activate conda environment
eval "$(conda shell.bash hook)"
# if [[ -z "$(find /home/$(whoami)/.conda/envs -name parallel-sanpi -type d)" ]]; then
#   echo "could not find parallel env"
#   # conda create -f ${SOURCE_DIR}/setup/parallel-sanpi_env.yml
# fi
conda activate parallel-sanpi

echo "Creating match subset conllu files..."
# conllu file/dir (path) = first arg
# pattern file  (path) = second arg

# echo "number of arguments = $#"
echo "conllu supplied:   $1"
echo "pattern supplied:  $2"

# read -p "Are all arguments correct? y/n " -r -n 1

# echo  
# if [[ ! $REPLY =~ ^[Yy]$ ]]
# then
#   [[ $0 = $BASH_SOURCE ]] && exit 1 || return 1 
#   # handle exits from shell or function but don't exit interactive shell
# fi
SOURCE_DIR=/share/compling/projects/sanpi
if [[ ! -d ${SOURCE_DIR} ]]; then
    SOURCE_DIR=/home/$(whoami)/projects/sanpi
fi
BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/make_subset_conllus.py"
echo "base command is: ${BASE_PYTHON_CMD}"


LOG_DIR=${SOURCE_DIR}/logs
if [[ ! -d $LOG_DIR ]]; then
  mkdir $LOG_DIR
fi

date
PAT_CALL=""
LOG_FILE_NAME="subset_defaults.log"
if [[ $# -eq 0 ]]; then

  date
  echo $BASE_PYTHON_CMD
  time $BASE_PYTHON_CMD
  exit 0
else
  CONLLU=$1
  LOG_SUFFIX=${CONLLU##*/}
  if [[ -z ${LOG_SUFFIX} ]]; then
    LOG_SUFFIX=${CONLLU%/}
    echo $LOG_SUFFIX
  fi

  LOG_FILE_NAME="subset_${LOG_SUFFIX%.conllu}"
  # exec >> ${LOG_FILE} 2>&1

  if [[ $# -gt 1 ]]; then
    PAT=$2
    if [[ -f ${PAT} && ${PAT##*.} == "pat" ]]; then
        PAT_CALL="-p ${PAT}"
        PAT_NAME=${PAT##*/}
        LOG_FILE_NAME=${PAT_NAME%.pat}-${LOG_FILE_NAME}
    else
      echo "Invalid pattern file supplied. Must be existing '.pat' file."
      exit 1  
    fi
  fi
fi
LOG_FILE="${LOG_DIR}/${LOG_FILE_NAME%.conll}.log"
echo "log file: ${LOG_FILE}"

    
if [[ -f ${CONLLU} ]]; then
  echo "time ${BASE_PYTHON_CMD} -c ${CONLLU} ${PAT_CALL}"
  time ${BASE_PYTHON_CMD} -c ${CONLLU} ${PAT_CALL}

elif [[ -d "${CONLLU}" ]]; then

  if [[ `which parallel` ]]; then
    echo "conll directory given >> using parallel..."
    echo "------------------------------------------"
    echo 'find ${CONLLU} -type f -name *.conllu | parallel "echo \"\" ; echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL ; echo \"\" " >> >(tee -i -a $LOG_FILE) 2>&1'
    echo "===>>"
    echo "find ${CONLLU} -type f -name *.conllu | parallel \"echo \"\" ; echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL ; echo \"\" \" >> >(tee -i -a $LOG_FILE) 2>&1"
    find ${CONLLU} -type f -name *.conllu | parallel "echo \"\" ; echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL ; echo \"\" " >> >(tee -i -a $LOG_FILE) 2>&1

  else
    echo "find ${CONLLU} -name *.conllu -exec bash -c \"echo \\\"\\\" ; echo \\\"_______________________\\\" ; echo \\\">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}\" \;"
    find ${CONLLU} -type f -name *.conllu -exec bash -c "echo \"\" ; echo \"_______________________\" ; echo \">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}" \;
  fi

fi
echo "========================================"
echo "Finished at $(date)"
echo "========================================"
echo ""
