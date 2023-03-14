#!/bin/bash
#SBATCH --mail-user=arh234@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH -J contig-puddin         # Job name
#SBATCH -o full-%x_%2a.%A.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e full-%x_%2a.%A.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH --array 0-34
#SBATCH -N 1                            # Total number of nodes requested
##SBATCH -n 12                            # Total number of cores requested
##SBATCH --mem-per-cpu=16G                     # Total amount of (real) memory requested (per node)
#SBATCH -n 1                            # Total number of cores requested
#SBATCH --mem=60G
#SBATCH --time 48:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/projects/sanpi/logs # to allow running `sbatch` cmd from anywhere and still put .out and .err in ../logs/ dir

# * Array Assignments * # 
# > puddin
# 0-29  ../puddin/Pcc[##].conll
#   OR
#   30  ../puddin/PccTe.conll
#   31  ../puddin/PccVa.conll
#
# > news
# ## APW ##
#   32  ../news/Apw.conll
#
# ## NYT ##
#   33  ../news/Nyt1.conll
#   34  ../news/Nyt2.conll
#
# > #HACK testing
#   35  ../sanpi/corpora_shortcuts/testing/small.conll
#   36  ../sanpi/corpora_shortcuts/testing/large.conll

set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo "slurm script: /share/compling/projects/sanpi/sanpi_slurm.sh"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate parallel-sanpi
echo "python interpreter path:"
which python

# pattern directory should be specified as directory name
PAT_DIR_NAME=${1:-"contig"}
echo "Pattern Type: \'${PAT_DIR_NAME##*/}\'"
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

echo "Job \'$SLURM_JOB_NAME\' - $SLURM_JOB_ID"
echo "  running on:"
echo "   - partition: $SLURM_JOB_PARTITION"
echo "   - node: $SLURM_JOB_NODELIST"
echo "   - 1 of $SLURM_ARRAY_TASK_COUNT"

SOURCE_DIR=/share/compling/projects/sanpi
PAT_DIR=${SOURCE_DIR}/Pat/${PAT_DIR_NAME}

SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

NEWS_DIR="$DATA_DIR/news"
PUDDIN_CORPUS="$DATA_DIR/puddin"

## * Assign Array Job Inputs * ##
# * news
## APW ##
if [ $SEED == 32 ]; then
    # echo "  Task ID ${SEED} assigned to 'Apw' dataset"
    SEED_CORPUS="${NEWS_DIR}/Apw.conll"

## NYT ##
elif [ $SEED == 33 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt1' dataset"
    SEED_CORPUS="${NEWS_DIR}/Nyt1.conll"
elif [ $SEED == 34 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt2' dataset"
    SEED_CORPUS="${NEWS_DIR}/Nyt2.conll"

# * #HACK test
elif [ $SEED == 35 ]; then
    SEED_CORPUS="${OUT_DIR}/corpora_shortcuts/testing/small.conll"

elif [ $SEED == 36 ]; then
    SEED_CORPUS="${OUT_DIR}/corpora_shortcuts/testing/large.conll"

elif [ $SEED == 37 ]; then
    SEED_CORPUS="${OUT_DIR}/corpora_shortcuts/testing/smallest20.conll"

elif [ $SEED == 38 ]; then
    SEED_CORPUS="${OUT_DIR}/corpora_shortcuts/testing/midrange10.conll"

# * puddin
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
    SEED_CORPUS="${PUDDIN_CORPUS}/Pcc${SEED}.conll"
fi

echo "Processing..."
echo "Corpus ${SEED}:  ${SEED_CORPUS}"
echo "Pattern Directory:  ${PAT_DIR}"

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
