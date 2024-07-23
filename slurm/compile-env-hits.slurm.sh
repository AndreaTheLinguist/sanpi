#!/bin/bash 
#SBATCH -N1
#SBATCH --mem=40G
#SBATCH --cpus-per-task 4
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 1:00:00
#SBATCH -J "ENVcompile"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs/update_env_hits"

echo 'running: `/share/compling/projects/sanpi/slurm/compile-env-hits.slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %-I:%M%P') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo 

eval "$(conda shell.bash hook)"
conda activate sanpi

LOG_FILE=${SLURM_JOB_NAME}.${SLURM_JOB_ID}_$(date +%y%m%d_%I%p).log.md
DATA_ARG=${1:-''}
if [[ -n $DATA_ARG ]]; then
    DATA_ARG="-d ${DATA_ARG} "
fi

PROG='/share/compling/projects/sanpi/script/compile_env_from_parts.py'

echo "time python '${PROG}' ${DATA_ARG} >> >(tee -i -a ${LOG_FILE})"
time ( python ${PROG} ${DATA_ARG} || echo "⚠️ python script failed." && exit 1 )  >> >(tee -i -a ${LOG_FILE}) 
echo -e '\n=======================\n'
echo -e "Finished.\n"
date
exit

