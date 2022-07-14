#!/bin/bash
#SBATCH --mail-user=arh234@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH -J subsetAdvAdj                 # Job name
#SBATCH -o %x-%2a_%A.out              # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x-%2a_%A.err              # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1                       # Total number of nodes requested
#SBATCH --ntasks=2                      # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --cpus-per-task=8               # number of cpus per task
#SBATCH --ntasks-per-socket=1
#SBATCH --mem-per-cpu=10G               # Total amount of (real) memory requested (per node)
#SBATCH --time 2:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --array 0-31
#SBATCH --chdir=/share/compling/data/sanpi/logs/subsets      # change working directory to this before execution

# set -o errexit

echo ">>=======================================<<"
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date) from $(pwd)"
echo ""
echo "running on ${SLURM_NODEID} with:"
echo "  - ${SLURM_CPUS_PER_TASK} cpus/task"
echo "  - ${SLURM_CPUS_ON_NODE} cpus per node"
echo "  - ${SLURM_JOB_NUM_NODES} nodes"
echo "  - ${SLURM_NTASKS} tasks"
# echo "  - ${SLURM_NTASKS_PER_CORE} tasks/core"
# echo "  - ${SLURM_NTASKS_PER_NODE} tasks/node"
echo "  - ${SLURM_MEM_PER_CPU} mem/cpu"


DATA_DIR=/share/compling/data
if [[ ! -d ${DATA_DIR} ]]; then
    DATA_DIR=/home/$(whoami)/data
fi

SOURCE_DIR=/share/compling/projects/sanpi
# activate conda environment
eval "$(conda shell.bash hook)"
# if [[ -z "$(find /home/$(whoami)/.conda/envs -name parallel-sanpi -type d)" ]]; then
#   echo "could not find parallel env"
#   # conda create -f ${SOURCE_DIR}/setup/parallel-sanpi_env.yml
# fi
conda activate parallel-sanpi
echo "Active Environment:"
echo "$(conda env list)"
echo ""

echo "Creating match subset conllu files..."
#! do not need conllu input arg with array

# // echo "conllu:   $1"
#! so pattern input is first
echo "pattern:  $1"

BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/create_match_conllu.py"

LOGS_DIR=${SOURCE_DIR}/logs
if [[ ! -d ${LOGS_DIR} ]]; then
  mkdir ${LOGS_DIR}
fi
LOG_SUBDIR=${LOGS_DIR}/${SLURM_JOB_NAME}
if [[ ! -d ${LOG_SUBDIR} ]]; then
  mkdir ${LOG_SUBDIR}
fi

# ! irrelevant code with job array
#// if [[ $# -eq 0 ]]; then
#//   # exec >> "${LOG_DIR}/subset_defaults.log" 2>&1
#//   date
#//   echo $BASE_PYTHON_CMD
#//   time $BASE_PYTHON_CMD
#//   exit 0
#// else
#//   CONLLU=$1
#//   # LOG_SUFFIX=${CONLLU##*/}
#//   # if [[ -z ${LOG_SUFFIX} ]]; then
#//   #   NOSLASH=${CONLLU%/}
#//   #   LOG_SUFFIX=${NOSLASH##*/}

#//   # fi
 
#//   # LOG_FILE="${LOG_DIR}/subset_${LOG_SUFFIX}.log"
#//   # exec >> ${LOG_FILE} 2>&1
#// fi

# if pattern file path is supplied
date
PAT_CALL="-p /share/compling/projects/sanpi/Pat/filter/exactly-JJ.pat"
# if [[ $# -gt 1 ]]; then
#   PAT=$2
#   if [[ -f ${PAT} && ${PAT##*.} == "pat" ]]; then
#       PAT_CALL="-p ${PAT}"
#   else
#     echo "Invalid pattern file supplied. Must be existing '.pat' file."
#     exit 1  
#   fi
# fi

#! irrelevant code with job array
#// if [[ -f ${CONLLU} ]]; then
#//   echo "time ${BASE_PYTHON_CMD} -c ${CONLLU} ${PAT_CALL}"
#//   time ${BASE_PYTHON_CMD} -c ${CONLLU} ${PAT_CALL}

## seed code copied from slurm snippet
SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

if [ $SEED == 30 ]; then
  echo "  Task ID ${SEED} assigned to 'test' dataset"
  SEED="Te"
elif [ $SEED == 31 ]; then
  echo "  Task ID ${SEED} assigned to 'val' dataset"
  SEED="Va"
else
  SEEDL=${#SEED}
  if [ $SEEDL -lt 2 ]; then
    SEED="0${SEED}"
  fi
  echo "  ${SEED} dataset"
fi


SEED_CORPUS_DIR=${DATA_DIR}/puddin/Pcc${SEED}.conll

### running the code

if [[ -d $SEED_CORPUS_DIR ]]; then
  # run script and send both stdout and stderr to log file
  DATE="$(date -I)"

  LOG_FILE=${LOG_SUBDIR}/${SEED}_${DATE}.log
  echo "Combined log will be appended to ${LOG_FILE}"
 
  # for FILE in $SEED_CORPUS_DIR/*.conllu; do
  #   # echo "srun time ${BASE_PYTHON_CMD} -c $FILE $PAT_CALL >> >(tee -i -a $LOG_FILE) 2>&1"
  #   # srun time ${BASE_PYTHON_CMD} -c $FILE $PAT_CALL >> >(tee -i -a $LOG_FILE) 2>&1
  # done


  if [[ `which parallel` ]]; then
    echo "find ${SEED_CORPUS_DIR} -type f -name *.conllu | parallel srun \"echo \"\" ; echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL; echo \"\" \" >> >(tee -i -a $LOG_FILE) 2>&1"
    find ${SEED_CORPUS_DIR} -type f -name *.conllu | parallel "srun --mem=8G echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL"; echo \"\"  >> >(tee -i -a $LOG_FILE) 2>&1

  else
    echo "srun find ${SEED_CORPUS_DIR} -name *.conllu -exec bash -c \"echo \\\"\\\" ; echo \\\"_______________________\\\" ; echo \\\">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}\" \;"
    find ${SEED_CORPUS_DIR} -type f -name *.conllu -exec bash -c "echo \"\" ; echo \"_______________________\" ; echo \">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}" \; >> >(tee -i -a $LOG_FILE) 2>&1
  fi

else
    echo "SEED value ${SEED} does not point to existing directory. Skipping."

fi
echo "========================================"
echo "Job closed at $(date)"
echo "========================================"
echo ""
