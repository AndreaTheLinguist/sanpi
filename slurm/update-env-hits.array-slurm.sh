#!/bin/bash 
#SBATCH -J "UpdateENVhits"
#SBATCH -o %x-%2a.%A.out      # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x-%2a.%A.err      # Name of stderr output log file (%j expands to jobID)
#SBATCH --array 0-34%12
#SBATCH -N 1                  # Total number of nodes requested
#SBATCH -c 3
#SBATCH --time 2:00:00       # Time limit (hh:mm:ss)
#SBATCH --mem 6G
#SBATCH --requeue
#SBATCH --get-user-env
#SBATCH --chdir="/share/compling/projects/sanpi/logs/update_env_hits"

echo 'running: `slurm/update-env-hits.array-slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %-I:%M%P') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo 

eval "$(conda shell.bash hook)"
conda activate sanpi

PAT=${1:-'RBdirect'}
PROG='/share/compling/projects/sanpi/script/update_env_hits.py'
DATA_DIR="/share/compling/data/sanpi/2_hit_tables"
PAT_DIR="${DATA_DIR}/${PAT}"

eval "$(conda shell.bash hook)"
conda activate sanpi

SEED=$((SLURM_ARRAY_TASK_ID))
echo "Array Index = ${SEED}"

# * news
## APW ##
if [ ${SEED} == 32 ]; then
    # echo "  Task ID ${SEED} assigned to 'Apw' dataset"
    CORPUS_PART="Apw"

## NYT ##
elif [ ${SEED} == 33 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt1' dataset"
    CORPUS_PART="Nyt1"
elif [ ${SEED} == 34 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt2' dataset"
    CORPUS_PART="Nyt2"
# * puddin
elif [ ${SEED} == 30 ]; then
    # echo "  Task ID ${SEED} assigned to 'test' dataset"
    CORPUS_PART="PccTe"
elif [ ${SEED} == 31 ]; then
    # echo "  Task ID ${SEED} assigned to 'val' dataset"
    CORPUS_PART="PccVa"
else
    SEEDL=${#SEED}
    if [ ${SEEDL} -lt 2 ]; then
        SEED="0${SEED}"
    fi
    # echo "  ${SEED} dataset"
    CORPUS_PART="Pcc${SEED}"
fi

echo "Processing..."
# usage: update_env_hits.py [-h] [-p CORPUS_PART] [-c CSV_PATH] [-x INDEX_PATH]
# options:
#   -h, --help            show this help message and exit
#   -p CORPUS_PART, --corpus_part CORPUS_PART
#                         corpus part tag to select both `--csv_path` and `--index_path`.
#                         (index will default to `alpha` version.) (default: None)
# ...
echo -e "\nCorpus Part #${SEED}: '${CORPUS_PART}'\n"
echo "python '${PROG}' -p '${CORPUS_PART}' -d '${PAT_DIR}'"

time python "${PROG}" -p "${CORPUS_PART}" -d "${PAT_DIR}"

exit

