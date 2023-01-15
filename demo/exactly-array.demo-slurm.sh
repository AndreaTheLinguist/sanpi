#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J exactly-demo         # Job name
#SBATCH -o %x_%2a.%j.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%2a.%j.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH -N 1                            # Total number of nodes requested
#SBATCH -n 4                            # Total number of cores requested
#SBATCH --mem-per-cpu=10G                     # Total amount of (real) memory requested (per node)
#SBATCH --time 10:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --array 0-1
#SBATCH --chdir=/share/compling/projects/sanpi/demo/logs

set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo "slurm script: /home/arh234/projects/sanpi/demo/exactly-array.demo-slurm.sh"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate sanpi
conda info | head -2 | tail -1

#! pattern directory arg should be specified as directory name
PAT_DIR_NAME=$1
echo "Pattern Type: ${PAT_DIR_NAME##*/}"
DEMO_DIR=/share/compling/projects/sanpi/demo
OUT_DIR=${DEMO_DIR}/data
if [[ ! -d ${OUT_DIR} ]]; then
    echo "Creating output directory: ${OUT_DIR}"
    mkdir ${OUT_DIR}
else
    echo "Output will be saved to ${OUT_DIR}"
fi

LOGS_DIR="${DEMO_DIR}/logs"
if [[ ! -d "${LOGS_DIR}" ]]; then
    mkdir ${LOGS_DIR}
fi

echo "Job $SLURM_JOB_NAME - $SLURM_JOB_ID"
echo "  running on:"
echo "   - partition: $SLURM_JOB_PARTITION"
echo "   - node: $SLURM_JOB_NODELIST"
echo "   - 1 of $SLURM_ARRAY_TASK_COUNT"

SOURCE_DIR=/share/compling/projects/sanpi
PAT_DIR=${SOURCE_DIR}/Pat/${PAT_DIR_NAME}

SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

if [ $SEED == 0 ]; then
    echo "  Task ID ${SEED} assigned to 'demo: exactly_puddin-val'"
    SEED="exactly_puddin-val"
else 
    echo "  Task ID ${SEED} assigned to 'demo: exactly_test'"
    SEED="exactly_test"
fi

SEED_CORPUS=${OUT_DIR}/corpora/subsets/${SEED}
echo "Processing..."
echo "  ${SEED_CORPUS}"
echo "  ${PAT_DIR}"

if [[ -d $SEED_CORPUS && -d ${PAT_DIR} ]]; then
    # run script and send both stdout and stderr to log file
    DATE="$(date -I)"
    LOG_FILE=${LOGS_DIR}/${SLURM_JOB_NAME}-${SEED}_${DATE}.log
    echo "Combined log will be appended to ${LOG_FILE}"

    echo -e "time python ${SOURCE_DIR}/run_pipeline.py -c ${SEED_CORPUS} -p ${PAT_DIR}\n-g ${OUT_DIR}/1_json_grew-matches >> >(tee -i -a ${LOG_FILE}) 2>&1"
    time python ${SOURCE_DIR}/run_pipeline.py -c ${SEED_CORPUS} -p ${PAT_DIR} -g ${OUT_DIR}/1_json_grew-matches >> >(tee -i -a ${LOG_FILE}) 2>&1

else
    echo "SEED value ${SEED} does not point to existing directories. Skipping."

fi
echo "Finished @ $(date)"
