#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=8G
#SBATCH --cpus-per-task=3
##SBATCH --partition=compling
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 1:00:00
#SBATCH -J BUG-pipe
#SBATCH --chdir=/share/compling/data/sanpi/debug/logs

echo 'running slurm script: /share/compling/projects/sanpi/playground/slurm_pipeline_debug.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
DEBUG_DIR="/share/compling/data/sanpi/debug"
BUG_CORP="${DEBUG_DIR}/bigram_debug/bigram-apw"

PAT_ARG="/share/compling/projects/sanpi/Pat/advadj"
PROG="/share/compling/projects/sanpi/run_pipeline.py"
echo "time python ${PROG} -R -c ${BUG_CORP} -p ${PAT_ARG} -g ${DEBUG_DIR}/1_json_grew-matches"
time python ${PROG} -R -c ${BUG_CORP} -p ${PAT_ARG} -g ${DEBUG_DIR}/1_json_grew-matches
