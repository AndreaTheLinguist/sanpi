#!/bin/bash
#SBATCH --mail-user=arh234@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH -J subset         # Job name
#SBATCH -o logs/%x_%j.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e logs/%x_%j.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH -N 3                            # Total number of nodes requested
#SBATCH -n 3                            # Total number of cores requested
#SBATCH -c 10                           # number of cpus per task
#SBATCH --mem-per-cpu=20G                     # Total amount of (real) memory requested (per node)
#SBATCH --time 4:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
# # SBATCH --array 0-31

# set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo ""
echo "running with ${SLURM_CPUS_PER_TASK}"


DATA_DIR=/share/compling/data
if [[ ! -d $DATA_DIR ]]; then
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
echo "conllu:   $1"
echo "pattern:  $2"

BASE_PYTHON_CMD="python ${SOURCE_DIR}/script/create_match_conllu.py"

LOG_DIR="${DATA_DIR}/sanpi/logs"
if [[ ! -d $LOG_DIR ]]; then
  mkdir $LOG_DIR
fi

if [[ $# -eq 0 ]]; then
  # exec >> "${LOG_DIR}/subset_defaults.log" 2>&1
  date
  echo $BASE_PYTHON_CMD
  time $BASE_PYTHON_CMD
  exit 0
else
  CONLLU=$1
  # LOG_SUFFIX=${CONLLU##*/}
  # if [[ -z ${LOG_SUFFIX} ]]; then
  #   NOSLASH=${CONLLU%/}
  #   LOG_SUFFIX=${NOSLASH##*/}

  # fi
  
  # LOG_FILE="${LOG_DIR}/subset_${LOG_SUFFIX}.log"
  # exec >> ${LOG_FILE} 2>&1
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
    find ${CONLLU} -type f -name *.conllu | parallel "echo \"\" ; echo \"------>>> {} <<<------\" ; date ; echo \"time ${BASE_PYTHON_CMD} -c {} $PAT_CALL\" && echo \"...\"; echo \"\"; time ${BASE_PYTHON_CMD} -c {} $PAT_CALL && echo \" ~ completed @ $(date) \"; echo \"\" "

  else
    echo "find ${CONLLU} -name *.conllu -exec bash -c \"echo \\\"\\\" ; echo \\\"_______________________\\\" ; echo \\\">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}\" \;"
    find ${CONLLU} -type f -name *.conllu -exec bash -c "echo \"\" ; echo \"_______________________\" ; echo \">>> {}\" && time ${BASE_PYTHON_CMD} -c {} ${PAT_CALL}" \;
  fi

fi
echo "========================================"
echo "Finished at $(date)"
echo "========================================"
echo ""
