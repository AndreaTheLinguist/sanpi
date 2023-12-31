#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=16G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 3:00:00
#SBATCH -J count_bigrams
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/

# usage:    sbatch [slurm flags] count_bigrams.slurm.sh [N_FILES] [THRESH] [HIT_TABLE_DIR]
# usage:    sbatch [slurm flags] count_bigrams.slurm.sh '-f 3' '-t 0.0005' '-d /share/compling/data/sanpi/debug/2_hit_tables/RBXadj'
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
HIT_DATA_DIR=${3:-''}
PROG="/share/compling/projects/sanpi/source/analyze/count_bigrams.py"
LOG_FILE="${SLURM_JOB_NAME}.${SLURM_JOB_ID}.log"
echo 'time python $PROG $N_FILES $THRESH $HIT_DATA_DIR'
echo "time python $PROG $N_FILES $THRESH $HIT_DATA_DIR"
time python $PROG $N_FILES $THRESH $HIT_DATA_DIR >> >(tee -i -a ${LOG_FILE}) 2>&1
