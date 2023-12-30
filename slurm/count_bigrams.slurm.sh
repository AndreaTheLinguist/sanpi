#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=16G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 3:00:00
#SBATCH -J count_bigrams
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs

# usage:    sbatch [slurm flags] count_bigrams.slurm.sh [N_FILES] [THRESH]
echo 'running slurm script: /share/compling/projects/sanpi/slurm/count_bigrams.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

# TODO I think the argument structure has changed for python script. Update below?
N_FILES=${1:-''}
THRESH=${2:-''}
PROG="/share/compling/projects/sanpi/source/analyze/count_bigrams.py"
LOG_FILE="${SLURM_JOB_NAME}.${SLURM_JOB_ID}.log"
echo 'time python $PROG -f $N_FILES -t $THRESH'
echo "time python $PROG -f $N_FILES -t $THRESH"
time python $PROG -f $N_FILES -t $THRESH >> >(tee -i -a ${LOG_FILE}) 2>&1
