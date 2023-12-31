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
# usage:    sbatch [slurm flags] count_RBgrams.slurm.sh '-f 3' '-t 0.001' '/share/compling/data/sanpi/debug/2_hit_tables/RBXadj'
SANPI_DATA="/share/compling/data/sanpi"

echo 'running slurm script: /share/compling/projects/sanpi/slurm/count_RBgrams.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

# DATA_DIR_NAME=${3:-'RBXadj'} #> i.e. category
# HIT_DIR="${SANPI_DATA}/2_hit_tables/$DATA_DIR_NAME" 
N_FILES=${1:-"-f $(ls -d1 ${HIT_DIR}/*pkl.gz | wc -l)"}
# THRESH=${2:-'0.01'}

# N_FILES=${1:-''}
THRESH=${2:-''}
HIT_DATA_DIR=${3:-"${SANPI_DATA}/2_hit_tables/RBXadj"}
DATA_DIR_NAME=$(basename ${HIT_DATA_DIR})
echo "processing ➡️ ${DATA_DIR_NAME}"
POST_PROC_DIR="${HIT_DATA_DIR%2_hit_tables*}4_post-processed/${DATA_DIR_NAME}"
PROG="/share/compling/projects/sanpi/source/analyze/count_bigrams.py -p ${POST_PROC_DIR} -o /share/compling/projects/sanpi/results/freq_out/${DATA_DIR_NAME}-$(basename $(pwd))" #! #HACK remove
# LOG_FILE="${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${N_FILES}f${THRESH//./-}p.log"
# LOG_FILE="${SLURM_JOB_NAME}_${SLURM_JOB_ID}_${N_FILES}f${THRESH//./-}p.$(date +%y-%m-%d_%H%M).log"
# echo 'time python $PROG -f $N_FILES -t $THRESH #>> >(tee -i -a ${LOG_FILE}) 2>&1'
# echo "time python $PROG -f $N_FILES -t $THRESH #>> >(tee -i -a ${LOG_FILE}) 2>&1"
# time python $PROG -f $N_FILES -t $THRESH #>> >(tee -i -a ${LOG_FILE}) 2>&1

echo 'time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR'
echo "time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR"
time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR #>> >(tee -i -a ${LOG_FILE}) 2>&1