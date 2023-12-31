#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=20G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 5:00:00
#SBATCH -J LSC
#SBATCH --chdir=/share/compling/projects/sanpi/logs

echo 'running slurm script: /share/compling/projects/sanpi/slurm/lsc_35JxR.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

SANPI_DIR="/share/compling/projects/sanpi"
PY_PROG="/share/compling/projects/sanpi/source/LSC/src/format_counts.py"
SH_PROG="/share/compling/projects/sanpi/source/LSC/mk_RJ-mod.sh"

FRQ_GRP=${1:-'JxR-frq'}
N_FILES=${2:-'35'}
N_ITER=${3:-'100'}
N_CLUST=${4:-''}

DATA="${SANPI_DIR}/results/freq_out/${FRQ_GRP}_thresh5.${N_FILES}f.csv"
LSC_DATA="${SANPI_DIR}/source/LSC/data/${FRQ_GRP}_thresh5-${N_FILES}f.tsv"

LOG_STEM="${SLURM_JOB_NAME}_${FRQ_GRP}.${SLURM_JOB_ID}"

echo "time python $PY_PROG $DATA"
time python $PY_PROG $DATA >> >(tee -i -a ${LOG_STEM}.format.log) 2>&1


echo "time bash ${SH_PROG} ${LSC_DATA} ${N_ITER} ${N_CLUST}"
time bash ${SH_PROG} ${LSC_DATA} ${N_ITER} ${N_CLUST} >> >(tee -i -a ${LOG_STEM}.train.log) 2>&1