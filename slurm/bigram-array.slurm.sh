#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J bigram-search      # Job name
#SBATCH -o %x-%2a.%A.out      # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x-%2a.%A.err      # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH --array 0-34%12
#SBATCH -N 1                  # Total number of nodes requested
#SBATCH -n 1                  # Total number of cores requested
#//#SBATCH --mem=60G
#//#SBATCH --cpus-per-task=10
#//#SBATCH --mem-per-cpu=5G    # Total amount of (real) memory requested (per node)
#SBATCH --time 35:00:00       # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs 
    # this ^^ allows running `sbatch` cmd from anywhere and still put .out and .err in ../logs/ dir

# * Array Assignments * # 
# > puddin
# 0-29  ../sanpi/subsets/bigram_puddin/bigram-Pcc[##]
#   OR
#   30  ../sanpi/subsets/bigram_puddin/bigram-PccTe
#   31  ../sanpi/subsets/bigram_puddin/bigram-PccVa
#
# > news
# ## APW ##
#   32  ../sanpi/subsets/bigram_news/bigram-Apw
#
# ## NYT ##
#   33  ../sanpi/subsets/bigram_news/bigram-Nyt1
#   34  ../sanpi/subsets/bigram_news/bigram-Nyt2
#
# > demo
#   35 ../sanpi/subsets/bigram_demo/bigram-DEMO-Apw
#   36 ../sanpi/subsets/bigram_demo/bigram-DEMO-Nyt
#   37 ../sanpi/subsets/bigram_demo/bigram-DEMO-Pcc
#
# > testing
#   38  ../sanpi/debug/bigram_debug/bigram-apw
#   39  ../sanpi/debug/bigram_debug/bigram-nyt
#   40  ../sanpi/debug/bigram_debug/bigram-pcc

set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo "slurm script: /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate parallel-sanpi
echo "python interpreter path:"
which python

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

echo "Job \'$SLURM_JOB_NAME\' - $SLURM_JOB_ID"
echo "  running on:"
echo "   - partition: $SLURM_JOB_PARTITION"
echo "   - node: $SLURM_JOB_NODELIST"
echo "   - 1 of $SLURM_ARRAY_TASK_COUNT"

SOURCE_DIR=/share/compling/projects/sanpi
PAT_DIR=${SOURCE_DIR}/Pat/${PAT_DIR_NAME}

SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

## * Assign Array Job Inputs * ##
SUBSETS_DIR=${OUT_DIR}/subsets
# * news
## APW ##
if [ $SEED == 32 ]; then
    # echo "  Task ID ${SEED} assigned to 'Apw' dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_news/bigram-Apw"

## NYT ##
elif [ $SEED == 33 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt1' dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_news/bigram-Nyt1"
elif [ $SEED == 34 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt2' dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_news/bigram-Nyt2"

#* demo of bigram subset
elif [ $SEED == 35 ]; then
    echo "  Task ID ${SEED} assigned to 'Apw' demo sample dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_demo/bigram-DEMO-Apw"
elif [ $SEED == 36 ]; then
    echo "  Task ID ${SEED} assigned to 'Nyt' demo sample dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_demo/bigram-DEMO-Nyt"
elif [ $SEED == 37 ]; then
    echo "  Task ID ${SEED} assigned to 'Pcc' demo sample dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_demo/bigram-DEMO-Pcc"


#HACK debug assignments
#* test
elif [ $SEED == 38 ]; then
    SEED_CORPUS="${OUT_DIR}/debug/bigram_debug/bigram-apw"

elif [ $SEED == 39 ]; then
    SEED_CORPUS="${OUT_DIR}/debug/bigram_debug/bigram-nyt"

elif [ $SEED == 40 ]; then
    SEED_CORPUS="${OUT_DIR}/debug/bigram_debug/bigram-pcc"

# * puddin
elif [ $SEED == 30 ]; then
    # echo "  Task ID ${SEED} assigned to 'test' dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_puddin/bigram-PccTe"
elif [ $SEED == 31 ]; then
    # echo "  Task ID ${SEED} assigned to 'val' dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_puddin/bigram-PccVa"
else
    SEEDL=${#SEED}
    if [ $SEEDL -lt 2 ]; then
        SEED="0${SEED}"
    fi
    # echo "  ${SEED} dataset"
    SEED_CORPUS="${SUBSETS_DIR}/bigram_puddin/bigram-Pcc${SEED}"
fi

# (no longer needed)
#// SEED_CORPUS="${SEED_CORPUS}/subset_bigram"
echo "Processing..."
echo "Corpus ${SEED}:  ${SEED_CORPUS}"
echo "Pattern Directory:  ${PAT_DIR}"

if [[ -d $SEED_CORPUS && -d ${PAT_DIR} ]]; then
    # run script and send both stdout and stderr to log file
    # DATE="$(date -I)"
    # job name itself has date now ✓
    LOG_FILE="${LOGS_DIR}/${SLURM_JOB_NAME}-${SEED}.log"
    echo "Combined log will be appended to ${LOG_FILE}"
    
    if [[ "$( basename $(dirname ${SEED_CORPUS}))" == 'bigram_demo' ]]; then
        OUT_DIR="${OUT_DIR}/DEMO"
        mkdir -p $OUT_DIR
    fi

    echo "time python ${SOURCE_DIR}/run_pipeline.py -c ${SEED_CORPUS} -p ${PAT_DIR}"
    echo "  -g ${OUT_DIR}/1_json_grew-matches >> >(tee -i -a ${LOG_FILE}) 2>&1"
    time python ${SOURCE_DIR}/run_pipeline.py -c $SEED_CORPUS -p $PAT_DIR \
        -g ${OUT_DIR}/1_json_grew-matches >> >(tee -i -a $LOG_FILE) 2>&1

    if [[ $PAT_DIR_NAME != "RBXadj" ]]; then
        echo -e "\n>> Run condensation and remove any bigram double dipping <<"
        CORPUS_NAME="$(basename $SEED_CORPUS)"
        echo "time python ${SOURCE_DIR}/source/gather/stop_double_dipping.py -c $CORPUS_NAME -p $PAT_DIR_NAME"
        echo "  --verbose --data_dir $OUT_DIR >> >(tee -i -a "${LOGS_DIR}/condense_${CORPUS_NAME}-${PAT_DIR_NAME}.$(date +%Y-%m-%d).log") 2>&1"
        time python ${SOURCE_DIR}/source/gather/stop_double_dipping.py -c $CORPUS_NAME -p $PAT_DIR_NAME --verbose \
            --data_dir $OUT_DIR >> >(tee -i -a "${LOGS_DIR}/condense_${CORPUS_NAME}-${PAT_DIR_NAME}.$(date +%Y-%m-%d).log") 2>&1
    fi
else
    echo "SEED value ${SEED} does not point to existing directories. Skipping."

fi
echo "Finished @ $(date)"
