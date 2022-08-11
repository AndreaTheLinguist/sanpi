#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J subset-exactly                 # Job name
#SBATCH -o %x-%2a_%A.out              # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x-%2a_%A.err              # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1                       # Total number of nodes requested
#SBATCH --ntasks=1                      # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --cpus-per-task=4               # number of cpus per task
#SBATCH --ntasks-per-socket=1
#SBATCH --mem-per-cpu=10G               # Total amount of (real) memory requested (per node)
#SBATCH --time 2:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --array 0-31
#SBATCH --chdir=/share/compling/data/sanpi/logs/subsets      # change working directory to this before execution

# set -o errexit
if [[ -n "${SLURM_JOB_ID}" ]]; then
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
fi

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
# echo "Active Environment:"
# echo "$(conda env list)"
# echo ""

#> set pat file path. Default to `exactly-JJ.pat`
PAT=${1:-${SOURCE_DIR}/Pat/filter/exactly-JJ.pat}

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

if [[ -n "${SLURM_JOB_ID}" ]]; then
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
  fi
  
else
  SEED=00
fi

echo "Processing ${SEED} dataset"
SEED_CORPUS_DIR=${DATA_DIR}/puddin/Pcc${SEED}.conll
MISSING_LIST=$( dirname ${SEED_CORPUS_DIR} )/info/exactly_subset/ALLpaths_missing-subset.txt

##> running the code
if [[ -d $SEED_CORPUS_DIR ]]; then
  # run script and send both stdout and stderr to log file
  echo "> ${SEED_CORPUS_DIR}"
  date "+%F %X"

  if [[ `which parallel` ]]; then

    #// #! `-maxdepth 1` required to exclude previously made subset .conllu files
    #// INPUTS_CMD="find ${SEED_CORPUS_DIR} -maxdepth 1 -type f -name \"*.conllu\" )
    #// # echo $FILTER_DIR"

    #// #> if filter dir path was given
    #// if [[ -n "${FILTER_DIR}" ]]; then
      #> locate the "...missing.txt" for the given SEED
      #//# ! must include `-maxdepth 1` to exclude files in `../prev/`
      # FILE_LIST_PATH=`find $( dirname ${SEED_CORPUS_DIR} )/**/*${FILTER_DIR}* -maxdepth 1 -type f -name "*${SEED}*missing.txt"`
      # FILE_LIST_PATH=$( find $( dirname ${SEED_CORPUS_DIR} )/**/*${FILTER_DIR}* -maxdepth 1 -type f -name "*${SEED}*missing.txt" )
    #   if [[ -f ${FILE_LIST_PATH} ]]; then
    #     INPUTS_CMD="cat ${FILE_LIST_PATH}"
    #   else
    #     echo -e "All conllu files in ${SEED_CORPUS_DIR##${DATA_DIR}} have corresponding subset files.\n> Exiting script."
    #     exit 0
    #   fi
      
    # fi
    
    # echo -e "Files to be processed\n*********************\n${INPUTS}"
    if [[ -f ${MISSING_LIST} ]]; then
      echo "Files in need of processing:"
      egrep Pcc${SEED}.conll ${MISSING_LIST} || echo "[NONE]"
      (egrep Pcc${SEED}.conll ${MISSING_LIST} | parallel --group -j0 "echo -e '\n{#} ({%}) {/}'; echo 'time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}'; time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}") || exit 1
      # (egrep Pcc${SEED}.conll ${MISSING_LIST} | parallel --group -j0 "echo -e '\n{#} ({%}) {/}'; time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}") || exit 1

      
      # egrep ${MISSING_LIST} | sort | parallel --keep-order --dryrun --jobs +0 --eta 'echo "------>>> {/} <<<------"; time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL})'
      # exit 0
    else
      echo "Filter list not found. Running entire directory."

      (find ${SEED_CORPUS_DIR} -maxdepth 1 -type f -name \"*.conllu\" | sort | parallel --keep-order -j0 --eta time ${BASE_PYTHON_CMD} -c {} $PAT_CALL) || exit 1

      wait
    fi

  else
    echo "<!> parallel utility not found! "
    find ${SEED_CORPUS_DIR} -maxdepth 1 -type f -name *.conllu -exec bash -c "echo \"\" ; echo \"_______________________\" ; echo \">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}" \; #>> >(tee -i -a $LOG_FILE) 2>&1
  fi

else
    echo "SEED value ${SEED} does not point to existing directory. Skipping."
    exit 1

fi

date "+%F %X %Z"
echo "Job closed."
exit 0

