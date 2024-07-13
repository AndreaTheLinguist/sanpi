#!/bin/bash 
#SBATCH -N1
#SBATCH --cpus-per-task 2
#SBATCH --mem-per-cpu 10G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 6:00:00
#SBATCH -J "UpdatePatCsvs"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs/update_env_hits"

echo 'running: `slurm/update-pat-csvs.slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %-I:%M%P') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo 

eval "$(conda shell.bash hook)"
conda activate parallel-sanpi

PROG='/share/compling/projects/sanpi/script/update_env_hits.py'
DATA_DIR="/share/compling/data/sanpi/2_hit_tables"
NEG="${DATA_DIR}/RBdirect"

# usage: filter_csv_by_index.py [-h] [-c CSV_PATH] [-x INDEX_PATH]
# -c CSV_PATH, --csv_path CSV_PATH
#                 path to dataframe saved as csv 
#                 (default: "${RBX}/pre-cleaned/clean_bigram-${/.}_rb-bigram_hits.csv")
# -x INDEX_PATH, --index_path INDEX_PATH
#                 path to text file containing `bigram_id` filter; id strings only separated by new lines 
#                 (default: "${COM}/clean_bigram-${/.}_not-RBdirect_index.txt")
PART=${1:-'PccTe'}
echo
echo "Updating '${PART}' tables"
echo
INDEX_PATH=$(find ${NEG}/pre-cleaned -name "*${PART}*index*alpha*REclean*txt")
CMD_PRE="python ${PROG} --index_path ${INDEX_PATH} --csv_path"

echo "Index: ${INDEX_PATH}"
echo "Original CSV files:"
find ${NEG} -name "*${PART}*hits.csv.bz2"
FILES=$(find ${NEG} -name "*${PART}*hits.csv.bz2")

time ( parallel -k "echo 'File:'; ls -oh {}; echo; $CMD_PRE {}" ::: ${FILES} )

exit

