#!/bin/bash 
#SBATCH -N1
#SBATCH --cpus-per-task 10
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 2:00:00
#SBATCH -J "UpdateNEGix"
#SBATCH --requeue
#SBATCH --chdir="/share/compling/projects/sanpi/logs/collect_ids"

echo 'running slurm script: `slurm/collect-neg-ids.slurm.sh`'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} (${SLURM_JOB_PARTITION} partition) with ${SLURM_MEM_PER_NODE} memory on ${SLURM_CPUS_ON_NODE} cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
echo 

eval "$(conda shell.bash hook)"
conda activate parallel-sanpi

PROG='/share/compling/projects/sanpi/script/collect_updatedNeg_ids.sh'
PARTS="$(find /share/compling/data/sanpi/2_hit_tables/RBdirect -type f -name '*_trigger_bigram-index_clean.35f.txt')"; 
parallel -k "echo -e '\nPart #{#}: {/.}'; echo 'bash ${PROG} {/.}' \
    && bash ${PROG} {/.}" ::: ${PARTS//_trigger_bigram-index_clean.35f.txt/}

exit

