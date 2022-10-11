#!/bin/bash
#SBATCH --mail-user=arh234@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH -J subset                 # Job name
#SBATCH -o %x_%j.out              # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%j.err              # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1                       # Total number of nodes requested
#SBATCH --ntasks=1                      # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --cpus-per-task=10              # number of cpus per task
#//#SBATCH --ntasks-per-socket=1
#SBATCH --mem-per-cpu=10G               # Total amount of (real) memory requested (per node)
#SBATCH --time 48:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/data/sanpi/logs/subsets    # change cwd before execution
#SBATCH --requeue

# """
#   usage:
#     $0 {string} {file} {directory} [-q]

#   Note: this will run the check_subset.sh script directly,
#           so it doesn't need to be run beforehand.

#   Input arguments:

#     1 -> SUBSET_TAG
#       some unique portion of the pattern file *stem*, not the parent dir.
#         This does not have to be the whole thing, but it needs to be something
#         that will correctly identify the associated files. e.g.:
#           'exactly' for Pat/filter/exactly-JJ.pat,
#           'RB-JJ' for Pat/advadj/all-RB-JJs.pat, etc.
#       This will be used for the check_subset.sh output in info/ and then
#       in turn pick out the right file listing the paths to be searched.

#     2 -> PATTERN_PATH
#       the path to the file to create the subset for.
#         This should be the absolute path, since cwd will be set to
#         'data/sanpi/logs/subsets' by slurm

#     3 -> DATA_PATH
#       the path to directory containing original corpus file directories
#         This should be the absolute path, since cwd will be set to
#         'data/sanpi/logs/subsets' by slurm

#     4: QUIET_FLAG
#       include literally anything as a third argument and the output of
#       the subcall of 'check_subset.sh' will be sent to null
#   """

set -o errexit
#! cannot use $0 to get the script name because it's actually run by slurm
#   i.e. would return 'script: /var/spool/slurmd/job781775/slurm_script'
echo "script: projects/sanpi/filter_subset_slurm.sh"
if [[ -n "${SLURM_JOB_ID}" ]]; then
  echo ">>=======================================<<"
  echo "JOB ID: ${SLURM_JOB_ID}"
  echo "JOB NAME: ${SLURM_JOB_NAME}"
  echo "started @ $(date) from $(pwd)"
  echo ""
  echo "running on ${SLURM_JOB_NODELIST} with:"
  echo "  - ${SLURM_NTASKS} tasks"
  echo "  - ${SLURM_CPUS_PER_TASK} cpus/task"
  # echo "  - ${SLURM_CPUS_ON_NODE} cpus per node"
  # echo "  - ${SLURM_JOB_NUM_NODES} nodes"
  # echo "  - ${SLURM_NTASKS_PER_CORE} tasks/core"
  # echo "  - ${SLURM_NTASKS_PER_NODE} tasks/node"
  echo "  - ${SLURM_MEM_PER_CPU} mem/cpu"
fi

DATA_DIR=${3:-"/share/compling/data/puddin"}
INFO_DIR="${DATA_DIR}/info"
mkdir -p ${INFO_DIR}
SOURCE_DIR="/share/compling/projects/sanpi"
# activate conda environment
eval "$(conda shell.bash hook)"

conda activate parallel-sanpi

SUBSET_TAG=${1:-${exactly}}
QUIET_FLAG=${4:-""}

if [[ -n "${QUIET_FLAG}" ]]; then
  SILENCER= &>/dev/null
else
  SILENCER=""
fi

${SOURCE_DIR}/script/check_subset.sh ${SUBSET_TAG} ${DATA_DIR} $SILENCER

#> set pat file AND FILTER FILE LIST paths. Default to `exactly-JJ.pat`
MISSING_LIST_PATH="${INFO_DIR}/${SUBSET_TAG}_subset/ALLpaths_missing-subset.txt"
# sanpi/Pat/advadj/all-RB-JJs.pat
PAT=${2:-${SOURCE_DIR}/Pat/filter/exactly-JJ.pat}
BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/make_subset_conllus.py"

# e.g. PAT_CALL="-p /share/compling/projects/sanpi/Pat/filter/exactly-JJ.pat"
if [[ -f ${PAT} && ${PAT##*.} == "pat" ]]; then
  PAT_CALL="-p ${PAT}"

elif
  [[ $(find ${SOURCE_DIR} -path "*Pat*${PAT}*" | wc -l)=="1" ]]
then
  PAT_CALL="-p $(find ${SOURCE_DIR} -path \"*Pat*${PAT}*\")"
else
  echo "Invalid pattern file supplied. Must be existing '.pat' file."
  exit 1
fi

if [[ -f ${MISSING_LIST_PATH} ]]; then
  if [[ $(egrep -v "conllu" ${MISSING_LIST_PATH}) ]]; then
    date "+%F %X %Z"
    echo "Job finished successfully."
    exit 0
  fi
  echo -e "\n>>> Gather subsets for files listed in ${MISSING_LIST_PATH}...\n"
  echo "Subset pattern: ${PAT}"
  # search string "conllu/n" yields total = 0 ㄟ( ▔, ▔ )ㄏ
  echo "Files in need of processing: $(egrep -c "conllu" ${MISSING_LIST_PATH}) total"
  echo -e "$(head -4 ${MISSING_LIST_PATH})\n...\n$(tail -4 ${MISSING_LIST_PATH})"
  BATCH_COUNT=1
  while [[ -n "$(head ${MISSING_LIST_PATH})" ]]; do
    NAME1="$(basename $(head -1 ${MISSING_LIST_PATH}))"
    NAME250="$(basename $(head -250 ${MISSING_LIST_PATH} | tail -1))"
    echo -e "\n--- batch ${NAME1%.conllu} through ${NAME250%.conllu} ---"

    parallel --halt soon,fail=15 --jobs=+0 echo "\[ {#} \| {%}\ ]: {/.}"\; time $BASE_PYTHON_CMD $PAT_CALL -c {} ::: $(head -200 $MISSING_LIST_PATH)

    wait
    sleep 2
    sync ${DATA_DIR}

    ${SOURCE_DIR}/script/check_subset.sh ${SUBSET_TAG} ${DATA_DIR} ${SILENCER}

  done

else
  echo "File list not found. Terminating."
  date "+%F %X %Z"
  echo "Job closed without success."
  exit 1
fi
# wait

# ${SOURCE_DIR}/script/check_subset.sh &>/dev/null

# if [[ $( egrep -c ".conllu\n" ${MISSING_LIST_PATH} ) -ne 0 ]]; then
#   echo "Files *still* in need of processing: $(egrep "conllu\n" ${MISSING_LIST_PATH}) total"
#   echo -e "$(head -3 ${MISSING_LIST_PATH})\n...\n$(tail -3 ${MISSING_LIST_PATH})"

#   while [[ -n "$(head ${MISSING_LIST_PATH})" ]]; do
#     parallel --jobs=+0 echo "+>> ({#}) {\}"\; time ${BASE_PYTHON_CMD} ${PAT_CALL} -c {} ::: head -250 ${MISSING_LIST_PATH}
#   done
# fi

date "+%F %X %Z"
echo "Job closed."
