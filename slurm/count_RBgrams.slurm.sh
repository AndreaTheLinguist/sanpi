#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=50G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 12:00:00
#SBATCH -J count_RBgrams
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/count_RBgrams

# usage:    sbatch [slurm flags] count_RBgrams.slurm.sh [N_FILES] [THRESH] [DATA_DIR_NAME]
echo 'running slurm script: /share/compling/projects/sanpi/slurm/count_RBgrams.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

SANPI_DATA="/share/compling/data/sanpi"
#> i.e. category
DATA_DIR_NAME=${3:-'RBXadj'} 

HIT_DIR="${SANPI_DATA}/2_hit_tables/$DATA_DIR_NAME" 
N_FILES=${1:-$(ls -d1 ${HIT_DIR}/*pkl.gz | wc -l)}
THRESH=${2:-'0.01'}
PROG="/share/compling/projects/sanpi/source/analyze/count_bigrams.py -d ${HIT_DIR} -p ${SANPI_DATA}/4_post-processed/${DATA_DIR_NAME} -o /share/compling/projects/sanpi/results/freq_out/${DATA_DIR_NAME}"
LOG_FILE="${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${N_FILES}f${THRESH//./-}p.log"
# LOG_FILE="${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${N_FILES}f${THRESH//./-}p.$(date +%y-%m-%d_%H%M).log"
echo 'time python $PROG -f $N_FILES -t $THRESH #>> >(tee -i -a ${LOG_FILE}) 2>&1'
echo "time python $PROG -f $N_FILES -t $THRESH #>> >(tee -i -a ${LOG_FILE}) 2>&1"
time python $PROG -f $N_FILES -t $THRESH #>> >(tee -i -a ${LOG_FILE}) 2>&1