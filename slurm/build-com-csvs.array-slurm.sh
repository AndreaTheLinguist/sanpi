#!/bin/bash 
#SBATCH -J "Build-COM"
#SBATCH -o %x-%2a.%A.out      # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x-%2a.%A.err      # Name of stderr output log file (%j expands to jobID)
#SBATCH --array 0-34%12
#SBATCH -N 1                  # Total number of nodes requested
#SBATCH --time 4:00:00       # Time limit (hh:mm:ss)
#SBATCH --mem 10G
#SBATCH --requeue
#SBATCH --get-user-env
#SBATCH --chdir="/share/compling/projects/sanpi/logs/build_complement"

echo 'running: `slurm/build-com-csvs.array-slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %-I:%M%P') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo 

eval "$(conda shell.bash hook)"
conda activate sanpi

PROG='/share/compling/projects/sanpi/script/filter_csv_by_index.py'
DATA_DIR="/share/compling/data/sanpi/2_hit_tables"
RBX="${DATA_DIR}/RBXadj"
COM="${DATA_DIR}/not-RBdirect"



echo 'running: "slurm/drop-numerical_hack.slurm.sh"'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi


SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

# * news
## APW ##
if [ $SEED == 32 ]; then
    # echo "  Task ID ${SEED} assigned to 'Apw' dataset"
    CORPUS_PART="Apw"

## NYT ##
elif [ $SEED == 33 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt1' dataset"
    CORPUS_PART="Nyt1"
elif [ $SEED == 34 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt2' dataset"
    CORPUS_PART="Nyt2"
# * puddin
elif [ $SEED == 30 ]; then
    # echo "  Task ID ${SEED} assigned to 'test' dataset"
    CORPUS_PART="PccTe"
elif [ $SEED == 31 ]; then
    # echo "  Task ID ${SEED} assigned to 'val' dataset"
    CORPUS_PART="PccVa"
else
    SEEDL=${#SEED}
    if [ $SEEDL -lt 2 ]; then
        SEED="0${SEED}"
    fi
    # echo "  ${SEED} dataset"
    CORPUS_PART="Pcc${SEED}"
fi

echo "Processing..."


# usage: filter_csv_by_index.py [-h] [-c CSV_PATH] [-x INDEX_PATH]
# -c CSV_PATH, --csv_path CSV_PATH
#                 path to dataframe saved as csv 
#                 (default: "${RBX}/pre-cleaned/clean_bigram-${/.}_rb-bigram_hits.csv")
# -x INDEX_PATH, --index_path INDEX_PATH
#                 path to text file containing `bigram_id` filter; id strings only separated by new lines 
#                 (default: "${COM}/clean_bigram-${/.}_not-RBdirect_index.txt")

echo -e "\nPart ${SEED}: '${CORPUS_PART}'\n"
echo "python '${PROG}' \\"
echo "  --csv_path '${RBX}/pre-cleaned/clean_bigram-${CORPUS_PART}_rb-bigram_hits.csv' \\"
echo "  --index_path '${COM}/clean_bigram-${CORPUS_PART}_not-RBdirect_alpha-index.txt'"
exit
time python ${PROG} \
    --csv_path "${RBX}/pre-cleaned/clean_bigram-${CORPUS_PART}_rb-bigram_hits.csv" \
    --index_path "${COM}/clean_bigram-${CORPUS_PART}_not-RBdirect_alpha-index.txt"


exit

