#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=16G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 3:00:00
#SBATCH -J correlate
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs

# usage:    sbatch [slurm flags] count_bigrams.slurm.sh [N_FILES] [THRESH]
echo 'running slurm script: /share/compling/projects/sanpi/slurm/correlate.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
SANPI_DIR="/share/compling/projects/sanpi"
THRESH=${1:-'8777'}
N_FILES=${2:-'35'}
INPUT="${SANPI_DIR}/results/freq_out/all-frq_thresh${THRESH}.${N_FILES}f.csv"

if [[ -f ${INPUT} ]]; then

    if [[ -s ${INPUT} ]]; then

        PROG="/share/compling/projects/sanpi/source/analyze/correlate_lemmas.py"
        LOG_FILE="${SLURM_JOB_NAME}_${THRESH}.${SLURM_JOB_ID}.log"
        echo 'time python $PROG ${INPUT}'
        echo "time python $PROG ${INPUT}"
        time python $PROG ${INPUT} >> >(tee -i -a ${LOG_FILE}) 2>&1
    else
        echo "${INPUT} is empty."
        exit 1
    fi
else
    echo "${INPUT} not found."
    exit 1
fi
