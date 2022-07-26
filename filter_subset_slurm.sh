#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J redo-subset-exactly                 # Job name
#SBATCH -o %x_%j.out              # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%j.err              # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1                       # Total number of nodes requested
#SBATCH --ntasks=1                      # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --cpus-per-task=8               # number of cpus per task
#SBATCH --ntasks-per-socket=1
#SBATCH --mem-per-cpu=20G               # Total amount of (real) memory requested (per node)
#SBATCH --time 10:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/data/sanpi/logs/subsets      # change working directory to this before execution

# set -o errexit
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
${SOURCE_DIR}/script/check_subsets.sh 

echo -e "\n>>> Gather still missing subsets...\n"
#: set pat file AND FILTER FILE LIST paths. Default to `exactly-JJ.pat`
MISSING_LIST=${DATA_DIR}/puddin/info/exactly_subset/ALLpaths_missing-subset.txt
PAT=${2:-${SOURCE_DIR}/Pat/filter/exactly-JJ.pat}
# example usage: 
#   sbatch [SLURM FLAGS] array_subset_slurm.sh (filter/)exactly-JJ(.pat) (info/)exactly_subset
BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/create_match_conllu.py"

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
  echo "Files in need of processing: $(egrep "conllu\n" ${MISSING_LIST}) total"
  echo -e "$(head -3 ${MISSING_LIST})\n...\n$(tail -3 ${MISSING_LIST})"
  cat ${MISSING_LIST} | parallel --pipe -N 50 --round-robin --jobs=${SLURM_CPUS_ON_NODE} parallel --group --jobs=${SLURM_CPUS_ON_NODE} "time ${BASE_PYTHON_CMD} ${PAT_CALL} -c {}"
  # cat ${MISSING_LIST} | parallel --pipe -N 50 --round-robin -j50 parallel --dryrun --jobs=${SLURM_CPUS_ON_NODE} "echo -e '\n{#} ({%}) {/}\ntime ${BASE_PYTHON_CMD} ${PAT_CALL} -c'; time ${BASE_PYTHON_CMD} ${PAT_CALL} -c"

else
  echo "Filter list not found. Running entire directory."
  exit 1
fi
wait

${SOURCE_DIR}/script/check_subsets.sh

if [[ $( egrep -c ".conllu\n" ${MISSING_LIST} ) -ne 0 ]]; then
  echo "Files *still* in need of processing: $(egrep "conllu\n" ${MISSING_LIST}) total"
  echo -e "$(head -5 ${MISSING_LIST})\n...\n$(tail -5 ${MISSING_LIST})"

  cat ${MISSING_LIST} | parallel --pipe -N 50 --round-robin --jobs=${SLURM_CPUS_ON_NODE} parallel --group --jobs=${SLURM_CPUS_ON_NODE} "time ${BASE_PYTHON_CMD} ${PAT_CALL} -c {}"
fi

date "+%F %X %Z"
echo "Job closed."
exit 0

