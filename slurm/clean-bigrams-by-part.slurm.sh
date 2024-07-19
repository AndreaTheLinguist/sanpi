#!/bin/bash 
#SBATCH -N1
#SBATCH --mem-per-cpu=1G
#SBATCH --cpus-per-task 5
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 8:00:00
#SBATCH -J "clean-parts"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs/bigram_cleaning"

# ! do not use this with slurm
#// set -o errexit 
# set -o nounset
# set -o pipefail

echo 'running additional cleaning/processing for corpus parts: `slurm/com-process_by-part.slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
LOG_FILE=${SLURM_JOB_NAME}_$(date +%y-%m-%d_%I%M%p).${SLURM_JOB_ID}.log
echo "time python "/share/compling/projects/sanpi/script/clean_bigrams_by_part.py" >> >(tee -i -a ${LOG_FILE}) 2>&1"
time python "/share/compling/projects/sanpi/script/clean_bigrams_by_part.py" >> >(tee -i -a ${LOG_FILE}) 2>&1
echo "Finished."
date

exit

