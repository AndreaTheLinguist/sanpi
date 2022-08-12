#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J redo-subset                 # Job name
#SBATCH -o %x_%j.out              # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%j.err              # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1                       # Total number of nodes requested
#SBATCH --ntasks=1                      # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --cpus-per-task=8              # number of cpus per task
##SBATCH --ntasks-per-socket=1
#SBATCH --mem-per-cpu=10G               # Total amount of (real) memory requested (per node)
#SBATCH --time 24:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/data/sanpi/logs/subsets      # change working directory to this before execution

  # """
  # this will run the check_subset.sh script directly. The arguments are: 
  #   1: SUBSET_TAG
  #     some unique portion of the pattern file *stem*, not the parent dir. This does not have to be the whole thing, but it needs to be something that will correctly identify the associated files. e.g.:
  #       'exactly' for Pat/filter/exactly-JJ.pat, 
  #       'RB-JJ' for Pat/advadj/all-RB-JJs.pat, etc.
  #     This will be used for the check_subset.sh output in info/ and then in turn pick out the right file listing the paths to be searched.
  #   2: PATTERN_PATH
  #     the path to the file to create the subset for. This should be the absolute path, since cwd will be set to 'data/sanpi/logs/subsets' by slurm
  #   3: QUIET_FLAG
  #     include literally anything as a third argument and the output of the subcall of 'check_subset.sh' will be sent to null
  # """

set -o errexit
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

DATA_DIR=/share/compling/data
if [[ ! -d ${DATA_DIR} ]]; then
    DATA_DIR=/home/$(whoami)/data
fi

SOURCE_DIR=/share/compling/projects/sanpi
# activate conda environment
eval "$(conda shell.bash hook)"

conda activate parallel-sanpi

SUBSET_TAG=${1:-${exactly}}
QUIET_FLAG=${3:-""}

if [[ -n "${QUIET_FLAG}" ]]; then
  SILENCER="&>/dev/null"
else
  SILENCER=""
fi

${SOURCE_DIR}/script/check_subset.sh ${SUBSET_TAG} $SILENCER

echo -e "\n>>> Gather still missing subsets...\n"
#> set pat file AND FILTER FILE LIST paths. Default to `exactly-JJ.pat`
MISSING_LIST=${DATA_DIR}/puddin/info/${SUBSET_TAG}_subset/ALLpaths_missing-subset.txt
# sanpi/Pat/advadj/all-RB-JJs.pat
PAT=${2:-${SOURCE_DIR}/Pat/filter/exactly-JJ.pat}

echo $MISSING_LIST
echo $PAT

# example usage: 
#   sbatch [SLURM FLAGS] array_subset_slurm.sh (filter/)exactly-JJ(.pat) (info/)exactly_subset
BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/make_subset_conllus.py"

# e.g. PAT_CALL="-p /share/compling/projects/sanpi/Pat/filter/exactly-JJ.pat"
if [[ -f ${PAT} && ${PAT##*.} == "pat" ]]; then
    PAT_CALL="-p ${PAT}"
    echo "Subset pattern: ${PAT##${SOURCE_DIR}}"

elif [[ $( find ${SOURCE_DIR} -path "*Pat*${PAT}*" | wc -l )=="1" ]]; then
    PAT_CALL="-p $( find ${SOURCE_DIR} -path "*Pat*${PAT}*" )"
else
  echo "Invalid pattern file supplied. Must be existing '.pat' file."
  exit 1
fi
# echo ${PAT_CALL}

if [[ -f ${MISSING_LIST} ]]; then
  # search string "conllu/n" yields total = 0 ㄟ( ▔, ▔ )ㄏ
  echo "Files in need of processing: $(egrep -c "conllu" ${MISSING_LIST}) total"
  echo -e "$(head -4 ${MISSING_LIST})\n...\n$(tail -4 ${MISSING_LIST})"

  while [[ -n "$(head ${MISSING_LIST})" ]]; do
    parallel --halt soon,fail=20 --jobs=+0 echo "\[ {#} \| {%}\ ]: {/.}"\; time ${BASE_PYTHON_CMD} ${PAT_CALL} -c {} ::: $( head -250 ${MISSING_LIST})
    wait
    sleep 2
    sync /share/compling/data/puddin
    ${SOURCE_DIR}/script/check_subset.sh ${SUBSET_TAG} ${SILENCER}
    echo -e "\n--- new batch ---"
  done

else
  echo "Filter list not found. Running entire directory."
  exit 1
fi
# wait

# ${SOURCE_DIR}/script/check_subset.sh &>/dev/null

# if [[ $( egrep -c ".conllu\n" ${MISSING_LIST} ) -ne 0 ]]; then
#   echo "Files *still* in need of processing: $(egrep "conllu\n" ${MISSING_LIST}) total"
#   echo -e "$(head -3 ${MISSING_LIST})\n...\n$(tail -3 ${MISSING_LIST})"

#   while [[ -n "$(head ${MISSING_LIST})" ]]; do
#     parallel --jobs=+0 echo "+>> ({#}) {\}"\; time ${BASE_PYTHON_CMD} ${PAT_CALL} -c {} ::: head -250 ${MISSING_LIST}
#   done
# fi

date "+%F %X %Z"
echo "Job closed."
exit 0

