#!/bin/bash
#SBATCH --mail-user=arh234@cornell.edu
#SBATCH --mail-type=ALL
#SBATCH -J contig-puddin         # Job name
#SBATCH -o %x_%2a.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%2a.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH --open-mode=append
#SBATCH -N 1                            # Total number of nodes requested
#SBATCH -n 1                            # Total number of cores requested
#SBATCH --mem=11G                     # Total amount of (real) memory requested (per node)
#SBATCH --time 12:00:00                  # Time limit (hh:mm:ss)
# #SBATCH --partition=gpu                 # Request partition for resource allocation
#SBATCH --get-user-env
# #SBATCH --gres=gpu:1                    # Specify a list of generic consumable resources (per node)
#SBATCH --array 0-31

set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate sanpi
echo "Active Environment:"
echo "$(conda env list)"
echo ""

PAT=${SLURM_JOB_NAME:0:6}
echo "Pattern set: ${PAT}"
DATA_DIR=/share/compling/data
if [[ ! -d $DATA_DIR ]]; then
    DATA_DIR=/home/arh234/data
fi

OUT_DIR=${DATA_DIR}/sanpi
if [[ ! -d $OUT_DIR ]]; then
    echo "Creating output directory: ${OUT_DIR}"
    mkdir $OUT_DIR
else
    echo "Output will be saved to ${OUT_DIR}"
fi

LOGS_DIR=${OUT_DIR}/logs
if [ ! -d "$LOGS_DIR" ]; then
    mkdir $LOGS_DIR
fi

echo "Job $SLURM_JOB_NAME - $SLURM_JOB_ID"
echo "  running on:"
echo "   - partition: $SLURM_JOB_PARTITION"
echo "   - node: $SLURM_JOB_NODELIST"
echo "   - 1 of $SLURM_ARRAY_TASK_COUNT"

SOURCE_DIR=/home/arh234/projects/sanpi
PAT_DIR=${SOURCE_DIR}/Pat/${PAT}

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


SEED_CORPUS=${DATA_DIR}/puddin/Pcc${SEED}.conll
# echo "  ${SEED_CORPUS}"
# echo "  ${PAT_DIR}"

if [[ -d $SEED_CORPUS && -d $PAT_DIR ]]; then
    # run script and send both stdout and stderr to log file
    DATE="$(date -I)"
    LOG_FILE=${LOGS_DIR}/${SLURM_JOB_NAME}${SEED}_${DATE}.log
    echo "Combined log will be appended to ${LOG_FILE}"
 
    echo "time python ${SOURCE_DIR}/run_pipeline.py -c ${SEED_CORPUS} -p ${PAT_DIR}"
    time python ${SOURCE_DIR}/run_pipeline.py -c ${SEED_CORPUS} -p ${PAT_DIR} >> >(tee -i -a $LOG_FILE) 2>&1

else
    echo "SEED values ${SEED} do not point to existing directories. Skipping."

fi
echo "Finished @ $(date)"