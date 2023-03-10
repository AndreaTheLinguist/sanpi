#!/bin/bash
#SBATCH --mail-user=arh234@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH -J contig-puddin         # Job name
#SBATCH -o %x_%2a.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%2a.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH --array 0-31
#SBATCH -N 1                            # Total number of nodes requested
#SBATCH -n 1                            # Total number of cores requested
#SBATCH --mem=11G                     # Total amount of (real) memory requested (per node)
#SBATCH --time 12:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/projects/sanpi/logs # to allow running `sbatch` cmd from anywhere and still put .out and .err in ../logs/ dir

set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo "slurm script: /share/compling/projects/sanpi/sanpi_slurm.sh"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate parallel-sanpi
conda info | head -2 | tail -1

# pattern directory should be specified as directory name
PAT_DIR_NAME=${1:-"contig"}
echo "Pattern Type: ${PAT_DIR_NAME##*/}"
DATA_DIR=/share/compling/data
if [[ ! -d ${DATA_DIR} ]]; then
    DATA_DIR=/home/arh234/data
fi

OUT_DIR=${DATA_DIR}/sanpi
if [[ ! -d ${OUT_DIR} ]]; then
    echo "Creating output directory: ${OUT_DIR}"
    mkdir ${OUT_DIR}
else
    echo "Output will be saved to ${OUT_DIR}"
fi

LOGS_DIR="${OUT_DIR}/logs"
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

## * Assign Array Job Inputs * ##
# * news
#> APW
if [ $SEED == 32 ]; then
    # echo "  Task ID ${SEED} assigned to 'Apw' dataset"
    SEED_CORPUS="${DATA_DIR}/news/Apw.conll"
#> NYT
elif [ $SEED == 33 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt1' dataset"
    SEED_CORPUS="${DATA_DIR}/news/Nyt1.conll"
elif [ $SEED == 34 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt2' dataset"
    SEED_CORPUS="${DATA_DIR}/news/Nyt2.conll"

#* #HACK test
elif [ $SEED == 35 ]; then
    SEED_CORPUS="${OUT_DIR}/corpora_shortcuts/small_test"

elif [ $SEED == 36 ]; then
    SEED_CORPUS="${OUT_DIR}/corpora_shortcuts/large_test"


#* puddin
elif [ $SEED == 30 ]; then
    # echo "  Task ID ${SEED} assigned to 'test' dataset"
    SEED_CORPUS="${PUDDIN_CORPUS}/PccTe.conll"
elif [ $SEED == 31 ]; then
    # echo "  Task ID ${SEED} assigned to 'val' dataset"
    SEED_CORPUS="${PUDDIN_CORPUS}/PccVa.conll"
else
    SEEDL=${#SEED}
    if [ $SEEDL -lt 2 ]; then
        SEED="0${SEED}"
    fi
    # echo "  ${SEED} dataset"
    SEED_CORPUS ="${PUDDIN_CORPUS}/Pcc${SEED}.conll"
fi

echo "Processing..."
echo "Corpus ${SEED}:  ${SEED_CORPUS}"
echo "Pattern Type:  ${PAT_DIR}"

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
