#!/bin/bash

#SBATCH -J fix-eof-blanks        # Job name
#SBATCH -o %x_%j.out                # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%j.err                # Name of stderr output log file (%j expands to jobID)
#SBATCH -N 1                            # Total number of nodes requested
#SBATCH --mem=7G                     # Total amount of (real) memory requested (per node)
#SBATCH --time 2:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/projects/sanpi/logs # to allow running `sbatch` cmd from anywhere and still put .out and .err in ../logs/ dir


set -o errexit
echo ">>=======================================<<"
echo "JOB ID: ${SLURM_ARRAY_JOB_ID}"
echo "started @ $(date) from $(pwd)"
echo "slurm script: /share/compling/projects/sanpi/script/adjust_eof_blanks.slurm.sh"
echo ""
# activate conda environment
eval "$(conda shell.bash hook)"
conda activate sanpi
conda info | head -2 | tail -1

time python /share/compling/projects/sanpi/script/adjust_conllu_blanklines.py $1