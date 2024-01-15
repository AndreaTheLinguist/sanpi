#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=40G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 4:00:00
#SBATCH -J count_env
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/count_env/#//testing #!#HACK remove "testing"

# usage:    sbatch [slurm flags] count-neg.slurm.sh
echo 'running slurm script: /share/compling/projects/sanpi/slurm/count-env.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

SANPI_DATA="/share/compling/data/sanpi"
DATA=${1:-'RBdirect'}
# ${foo:+val} -> 	val if $foo is set (and not null)
FRQ_FILT_IX=${2:+"-b $2"}
PARENT_DIR=${3:-"2_hit_tables"}
echo "Selected frequency filter indexer: ${FRQ_FILT_IX}"

#? Can this can be changed to load from `3_dep_info/` instead?
HIT_DIR="-d ${SANPI_DATA}/${PARENT_DIR}/${DATA}"
OUT_DIR="-o /share/compling/projects/sanpi/results/freq_out/${DATA}"
#HACK: this would be better as an argument, but 🤷‍♀️
# BIGRAM_FIlTER="${SANPI_DATA}/4_post-processed/RBXadj/bigram-IDs_thr0-1p.10f.txt"


PY_MODULE="/share/compling/projects/sanpi/source/analyze/count_env.py"
# LOG_FILE="${SLURM_JOB_NAME}.${SLURM_JOB_ID}~$(date +%y-%m-%d_%H%M).log"
LOG_FILE="${SLURM_JOB_NAME}.${SLURM_JOB_ID}.log"
# echo 'time python ${PY_MODULE}'
echo -e "\ntime python ${PY_MODULE} \\ \n    ${HIT_DIR} \\ \n    ${OUT_DIR} \\ \n    ${FRQ_FILT_IX}"
#// time python ${PY_MODULE} -b ${BIGRAM_FILTER} >> >(tee -i -a ${LOG_FILE}) 2>&1
time python ${PY_MODULE} ${HIT_DIR} ${OUT_DIR} ${FRQ_FILT_IX} #>> >(tee -i -a ${LOG_FILE}) 2>&1