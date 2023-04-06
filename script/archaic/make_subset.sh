#!/bin/bash
# make_subset.sh
# glue script to run 'make_subset_conllus.py'
#   a little more neatly for more than 1 conllu file at a time
# echo "Input:" "$@"
ARG1=${1:--h} # if no arguments given, assume help is desired.
#> "%\/" removes any final "/"
CONLL_DIR=${1%\/}
#> Set source dir variable
THIS_SCRIPT_DIR="$(dirname $0)"
# echo "This script is in ${THIS_SCRIPT_DIR}"
CURR_SOURCE_DIR="${THIS_SCRIPT_DIR%%script*}"
SOURCE_DIR=${CURR_SOURCE_DIR:-/share/compling/projects/sanpi}
# echo "source directory: ${SOURCE_DIR}"
DEFAULT_PAT="${SOURCE_DIR}/Pat/advadj/all-RB-JJs.pat"
PAT=${2:-$DEFAULT_PAT}

if [[ ${ARG1} == "-h" ]]; then
  echo -e "$0 Help:\n" \
    "shell script to create subset files of sentences matching \n" \
    "  a specific pattern plus the preceding and following sentence \n" \
    "  for all conllu files in given directory.\n" \
    "\n" \
    "Usage:\n" \
    " \$ bash $(basename $0) CONLL_DIR_PATH [PATTERN_FILE_PATH]\n" \
    "  If pattern file path not given, processing defaults to:\n" \
    "    PATTERN = ${DEFAULT_PAT}\n"
  exit 0
fi

# * activate conda environment
eval "$(conda shell.bash hook)"
conda activate parallel-sanpi

echo "Creating match subset conllu files..."

BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/make_subset_conllus.py"
echo "base command is: ${BASE_PYTHON_CMD}"

if [[ ! -f ${PAT} ]]; then
  echo "ERROR: Pattern file ${PAT} cannot be found."
  exit 1
fi
if [[ ${PAT:(-4)} != ".pat" ]]; then
  echo "Invalid pattern file supplied. Should have suffix '.pat'"
  exit 1
fi

echo "pat: ${PAT}"
PAT_CALL="-p ${PAT}"
PAT_NAME="$(basename ${PAT})"
CONLL_NAME="$(basename ${CONLL_DIR})"

#> Set logging variables
LOG_SUFFIX="${CONLL_NAME%.conll}"

if [[ -z ${LOG_SUFFIX} ]]; then
  LOG_SUFFIX="subset$(date '+%F_%X')"
  echo ${LOG_SUFFIX}
fi

LOG_STEM="subset_${LOG_SUFFIX}_${PAT_NAME%.pat}"
echo ${LOG_STEM}

LOG_DIR="${SOURCE_DIR}/logs"
if [[ ! -d ${LOG_DIR} ]]; then
  mkdir -p ${LOG_DIR}
fi

LOG_PATH="${LOG_DIR}/${LOG_STEM}.log"
echo "log will be saved to: ${LOG_PATH}"

#* send rest of stdout and stderr to log!
exec >>${LOG_PATH} 2>&1
echo -e "\n[ creating subset @ $(date '+%F %X') ]"
if [[ -d "${CONLL_DIR}" ]]; then

  if [[ $(which parallel) ]]; then
    echo "conll directory given >> using parallel..."
    echo "------------------------------------------"
    ls ${CONLL_DIR}/*.conllu | head -5
    echo "..."
    ls ${CONLL_DIR}/*.conllu | tail -4
    FILE_LIST=$(ls ${CONLL_DIR}/*.conllu | head -8)
    # parallel \( echo \; echo "------\>\>\> {/} \<\<\<------"\;\
    # date "+%F\ %X" \; echo \; echo "time $BASE_PYTHON_CMD -c {} $PAT_CALL"\;\
    # echo "..."\; echo \)\
    # && time $BASE_PYTHON_CMD -c {} $PAT_CALL

    parallel --halt soon,fail=20 --jobs=+0\
    echo "\[ {#} \| {%} \]: {/.}" \; date "+%F\ %X"\;\
    time $BASE_PYTHON_CMD $PAT_CALL -c {} ::: $FILE_LIST

    wait
    sleep 2

  else
    # echo 'find ${CONLL_DIR} -name *.conllu -exec bash -c echo -e "\n\n------>>> {} <<<------\n"\
    #   "$(date)\ntime $BASE_PYTHON_CMD -c {} $PAT_CALL\n...\n'
    find ${CONLL_DIR} -type f -name *.conllu -exec bash -c \
    "echo -e \"\n\n------>>> {} <<<------\n$(date)\ntime "\
    "${BASE_PYTHON_CMD} -c {} ${PAT_CALL}\n...\n\""\
    "&& time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL};"
  fi

else
  echo "ERROR: conll directory ${CONLL_DIR} not found."
  exit 1

fi
echo "========================================"
echo "Finished at $(date)"
echo "========================================"
echo ""
exit
