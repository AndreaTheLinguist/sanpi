#!/bin/bash

#SBATCH -J Alpha     # Job name
#SBATCH -o %x-%2a.%A.out      # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x-%2a.%A.err      # Name of stderr output log file (%j expands to jobID)
#SBATCH --array 0-34%12
#SBATCH -N 1                  # Total number of nodes requested
#SBATCH -n 1                  # Total number of cores requested
#SBATCH --time 4:00:00       # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --mem=5G
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/alpha-filter
echo 'running: "slurm/alpha-filter.array-slurm.sh"'
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
    SEED_CORPUS="Apw"

## NYT ##
elif [ $SEED == 33 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt1' dataset"
    SEED_CORPUS="Nyt1"
elif [ $SEED == 34 ]; then
    # echo "  Task ID ${SEED} assigned to 'Nyt2' dataset"
    SEED_CORPUS="Nyt2"
# * puddin
elif [ $SEED == 30 ]; then
    # echo "  Task ID ${SEED} assigned to 'test' dataset"
    SEED_CORPUS="PccTe"
elif [ $SEED == 31 ]; then
    # echo "  Task ID ${SEED} assigned to 'val' dataset"
    SEED_CORPUS="PccVa"
else
    SEEDL=${#SEED}
    if [ $SEEDL -lt 2 ]; then
        SEED="0${SEED}"
    fi
    # echo "  ${SEED} dataset"
    SEED_CORPUS="Pcc${SEED}"
fi

echo "Processing..."
echo "Corpus ${SEED}:  ${SEED_CORPUS}"
PY_SCRIPT='/share/compling/projects/sanpi/script/apply_alpha-filter.py'
echo "time python ${PY_SCRIPT} -p '${SEED_CORPUS}'"
time python ${PY_SCRIPT} -p "${SEED_CORPUS}"