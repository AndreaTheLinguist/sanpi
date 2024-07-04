#!/bin/bash 
#SBATCH -N1
#SBATCH --mem=10G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 8:00:00
#SBATCH -J "pre-clean-parts"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs"

echo 'running additional cleaning/processing for corpus parts: `slurm/com-process_by-part.slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
LOG_FILE=${SLURM_JOB_NAME}.JID${SLURM_JOB_ID}_$(date +%y-%m-%d_%H%M).log
echo "time python "/share/compling/projects/sanpi/script/get_pre-cleaned_subtables.py" >> >(tee -i -a ${LOG_FILE}) 2>&1"
time python "/share/compling/projects/sanpi/script/get_pre-cleaned_subtables.py" >> >(tee -i -a ${LOG_FILE}) 2>&1
echo "Finished."
date
exit

