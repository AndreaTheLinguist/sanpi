#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J analyze-deps         # Job name
#SBATCH -o %x_%2a.%j.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%2a.%j.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH -N 1                            # Total number of nodes requested
#SBATCH -n 4                            # Total number of cores requested
#SBATCH --mem-per-cpu=20G                     # Total amount of (real) memory requested (per node)
#SBATCH --time 12:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --array 0-1
#SBATCH --chdir=/share/compling/projects/sanpi/logs # to allow running `sbatch` cmd from anywhere and still put .out and .err in ../logs/ dir

#!WARNING: specifying `mem-per-cpu` may fail on larger input sets in crosstabulation step, since it is not parallel

set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo "slurm script: /share/compling/projects/sanpi/analyze-deps_exactly.slurm.sh"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate parallel-sanpi
conda info | head -2 | tail -1

# DATA_DIR=/share/compling/data
# if [[ ! -d ${DATA_DIR} ]]; then
#     DATA_DIR=/home/arh234/data
# fi

echo "Job $SLURM_JOB_NAME - $SLURM_JOB_ID"
echo "  running on:"
echo "   - partition: $SLURM_JOB_PARTITION"
echo "   - node: $SLURM_JOB_NODELIST"
echo "   - 1 of $SLURM_ARRAY_TASK_COUNT"

SANPI_DIR=/share/compling/projects/sanpi

LOGS_DIR="${SANPI_DIR}/logs"
if [[ ! -d "${LOGS_DIR}" ]]; then
    mkdir ${LOGS_DIR}
fi
SOURCE_DIR="${SANPI_DIR}/source"

SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

if [ $SEED == 0 ]; then
    echo "  Task ID ${SEED} assigned to 'exactly_puddin'"
    SEED="exactly_puddin"
elif [ $SEED == 1 ]; then
    echo "  Task ID ${SEED} assigned to 'exactly_news'"
    SEED="exactly_news"
elif [ $SEED == 2 ]; then
    echo "  Task ID ${SEED} assigned to 'exactly_nyt'"
    SEED="exactly_nyt"
elif [ $SEED == 3 ]; then
    echo "  Task ID ${SEED} assigned to 'exactly_apw'"
    SEED="exactly_apw"
else 
    echo "  Task ID ${SEED} assigned to 'exactly_test'"
    SEED="exactly_test"
fi

echo "Processing..."
echo "  ${SEED}"

# run script and send both stdout and stderr to log file
DATE="$(date -I)"
LOG_FILE=${LOGS_DIR}/${SLURM_JOB_NAME}-${SEED}_${DATE}.log
echo "Combined log will be appended to ${LOG_FILE}"

echo -e "time python ${SOURCE_DIR}/analyze_deps.py -g ${SEED}*hits.pkl.gz -n exactly-${SEED} -v >> >(tee -i -a ${LOG_FILE}) 2>&1"
time python ${SOURCE_DIR}/analyze_deps.py -g ${SEED}*hits.pkl.gz -n exactly-${SEED} -v >> >(tee -i -a ${LOG_FILE}) 2>&1


echo "Dep analysis by corpus finished @ $(date)"
