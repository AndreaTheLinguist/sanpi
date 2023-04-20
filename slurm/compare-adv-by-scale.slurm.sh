#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=10G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 1:00:00
#SBATCH -J scale-compare
#SBATCH --chdir=/share/compling/projects/sanpi/notebooks/scale_comparison/logs

echo 'running slurm script: /share/compling/projects/sanpi/slurm/compare-adv-by-scale.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

N_FILES=${1:-''}
PROG="/share/compling/projects/sanpi/notebooks/scale_comparison/compare-adv-by-scale.py"

echo 'time python $PROG $N_FILES'
echo "time python $PROG $N_FILES"
time python $PROG $N_FILES
