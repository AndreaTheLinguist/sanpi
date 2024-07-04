#!/bin/bash 
#SBATCH -N1
#SBATCH --cpus-per-task 7
#SBATCH --mem-per-cpu 8G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 6:00:00
#SBATCH -J "BuildComCsvs"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs"

echo 'running: `slurm/build-com-csvs.slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %-I:%M%P') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo 

eval "$(conda shell.bash hook)"
conda activate parallel-sanpi

PROG='/share/compling/projects/sanpi/script/filter_csv_by_index.py'
DATA_DIR="/share/compling/data/sanpi/2_hit_tables"
RBX="${DATA_DIR}/RBXadj"
COM="${DATA_DIR}/not-RBdirect"
PARTS="$(find "${RBX}" -type f -name '*_bigram-index_clean.35f.txt')"; 

# usage: filter_csv_by_index.py [-h] [-c CSV_PATH] [-x INDEX_PATH]
# -c CSV_PATH, --csv_path CSV_PATH
#                 path to dataframe saved as csv 
#                 (default: "${RBX}/pre-cleaned/clean_bigram-${/.}_rb-bigram_hits.csv")
# -x INDEX_PATH, --index_path INDEX_PATH
#                 path to text file containing `bigram_id` filter; id strings only separated by new lines 
#                 (default: "${COM}/clean_bigram-${/.}_not-RBdirect_index.txt")

CMD_PRE="python '${PROG}' --csv_path '${RBX}/pre-cleaned/clean_bigram-"
CMD_MID="_rb-bigram_hits.csv' --index_path '${COM}/clean_bigram-"
CMD_SUF="_not-RBdirect_index.txt'"
parallel -k "echo -e '\nPart #{#}: {/.}\n\
    \n$CMD_PRE{/.}$CMD_MID{/.}$CMD_SUF' \
    && $CMD_PRE{/.}$CMD_MID{/.}$CMD_SUF" \
::: ${PARTS//_bigram-index_clean.35f.txt/}

exit

