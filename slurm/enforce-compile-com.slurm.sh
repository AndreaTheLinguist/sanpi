#!/bin/bash 
#SBATCH -N1
#SBATCH --mem=40G
#SBATCH --cpus-per-task 4
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 6:00:00
#SBATCH -J "COM_ConcatEnforced"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs/build_complement"

echo '> running "not negated" enforcement and compiling: "slurm/enforce-compile-com.slurm.sh"'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
LOG_FILE=${SLURM_JOB_NAME}.j${SLURM_JOB_ID}_$(date +%y%m-%d_%I%p).log.md
DATA_ARG=${1:-''}
if [[ -n $DATA_ARG ]]; then
    DATA_ARG="-d ${DATA_ARG} "
fi

echo "time python '/share/compling/projects/sanpi/script/compile_com_from_parts.py' ${DATA_ARG} >> >(tee -i -a ${LOG_FILE})"
time ( python /share/compling/projects/sanpi/script/compile_com_from_parts.py ${DATA_ARG} || exit 1 )  >> >(tee -i -a ${LOG_FILE}) 
echo -e '\n=======================\n'
echo -e "Finished.\n"
date
exit

