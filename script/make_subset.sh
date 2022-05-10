#!/bin/bash
# make_subset.sh
# glue script to run 'create_match_conllu.py' 
#   a little more neatly for more than 1 conllu file at a time
# echo "Input:" "$@"

if [[ $1 == "-h" ]]; then

  echo "shell script to create subsets matching pattern file (only) for all conllu files specified by path (dir or file*)."
  echo "  -> should be run from toplevel of sanpi project ('../sanpi/')"
  echo "  * intended for directory containing .conllu files, but won't crash for direct path to .conllu file"
  echo "  !! CONLLU_PATH must end with '/' to be parsed as directory"
  echo ""
  echo "Usage: (sanpi\$) bash script/$(basename $0) [CONLLU_PATH=path PATTERN_FILE=path]"
  echo "  If arguments are not given, python script (create_match_conllu.py) defaults to:"
  echo "    CONLLU = ~/data/devel/quicktest.conll/nyt_eng_199912.conllu"
  echo "    PATTERN = Pat/advadj/all-RB-JJs.pat"
  echo "       (will crash with pattern default if not run from dir containing 'Pat/')"
  
  exit 0
fi
  
echo "Creating match subset conllu files..."
# conllu file/dir (path) = "$1"
# pattern file  (path) = "$2"

# echo "number of arguments = $#"
echo "conllu:   $1"
echo "pattern:  $2"

# read -p "Are all arguments correct? y/n " -r -n 1

# echo  
# if [[ ! $REPLY =~ ^[Yy]$ ]]
# then
#   [[ $0 = $BASH_SOURCE ]] && exit 1 || return 1 
#   # handle exits from shell or function but don't exit interactive shell
# fi

BASE_PYTHON_CMD="python /home/$(whoami)/projects/sanpi/script/create_match_conllu.py"
# echo $BASE_PYTHON_CMD
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate sanpi

LOG_DIR="logs"
if [[ ! -d $LOG_DIR ]]; then
  mkdir $LOG_DIR
fi

if [[ $# -eq 0 ]]; then
  exec >> "${LOG_DIR}/subset_defaults.log" 2>&1
  date
  echo $BASE_PYTHON_CMD
  time $BASE_PYTHON_CMD
  exit 0
else
  CONLLU=$1
  LOG_SUFFIX=${CONLLU##*/}
  if [[ -z ${LOG_SUFFIX} ]]; then
    NOSLASH=${CONLLU%/}
    LOG_SUFFIX=${NOSLASH##*/}

    echo $LOG_SUFFIX
  fi
  LOG_FILE="${LOG_DIR}/subset_${LOG_SUFFIX}.log"
  exec >> ${LOG_FILE} 2>&1
fi

date
PAT_CALL=""
if [[ $# -gt 1 ]]; then
  PAT=$2
  if [[ -f ${PAT} && ${PAT##*.} == "pat" ]]; then
      PAT_CALL="-p ${PAT}"
  else
    echo "Invalid pattern file supplied. Must be existing '.pat' file."
    exit 1  
  fi
fi

    
if [[ -f ${CONLLU} ]]; then
  echo "time ${BASE_PYTHON_CMD} -c ${CONLLU} ${PAT_CALL}"
  time ${BASE_PYTHON_CMD} -c ${CONLLU} ${PAT_CALL}

elif [[ -d "${CONLLU}" ]]; then

  if [[ `which parallel` ]]; then
    # find ${CONLLU} -type f -name *.conllu -print0 | parallel -0 bash -c "echo \"\" ; echo \"_______________________\" ; echo \">>> {}\" " #&& time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}" \;
    # find ${CONLLU} -type f -name *.conllu | parallel "echo \"------>>> {} <<<------\" && echo \"time ${BASE_PYTHON_CMD} -c {}\" && echo \"\" && \"time ${BASE_PYTHON_CMD} -c {}\" && echo \"\""
    find ${CONLLU} -type f -name *.conllu | parallel "echo \"\" ; echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL ; echo \" ~ completed @ $(date) \"; echo \"\" "

  else
    echo "find ${CONLLU} -name *.conllu -exec bash -c \"echo \\\"\\\" ; echo \\\"_______________________\\\" ; echo \\\">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}\" \;"
    find ${CONLLU} -type f -name *.conllu -exec bash-c "echo \"\" ; echo \"_______________________\" ; echo \">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}" \;
  fi

fi
echo "========================================"
echo "Finished at $(date)"
echo "========================================"
echo ""
