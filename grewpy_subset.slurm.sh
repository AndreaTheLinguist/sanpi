#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J sanpi-subset         # Job name
#SBATCH -o %x.%j.out            # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x.%j.err            # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1               # Total number of nodes requested
#SBATCH --ntasks=1              # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --mem=15G               # Total amount of (real) memory requested (per node)
#SBATCH --time 1:00:00          # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/projects/sanpi/logs/grewpy_subsets     # change working directory to this before execution

eval "$(conda shell.bash hook)"
conda activate sanpi

if [[ -n "${SLURM_JOB_ID}" ]]; then
    echo "JOB ID: $SLURM_JOB_ID"
    echo "JOB NAME: $SLURM_JOB_NAME"
    echo "started @ $(date '+%F %X') from $(pwd)"
    echo "script: /share/compling/projects/sanpi/grewpy_subset.slurm.sh"
    echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
    echo "running on $SLURM_JOB_NODELIST with:"
    echo "  - $SLURM_NTASKS cores"
    echo "  - $SLURM_MEM_PER_CPU mem/cpu"
    echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
fi

PAT=${3:-""}
if [[ -n $PAT ]]; then
    PAT="-p $PAT"
fi

echo "time python /share/compling/projects/sanpi/script/create_grewpy_subset.py -n $1 $PAT $2 > ${SLURM_JOB_NAME}.${SLURM_JOB_ID}.md"
time python /share/compling/projects/sanpi/script/create_grewpy_subset.py -n $1 $PAT $2 > ${SLURM_JOB_NAME}.${SLURM_JOB_ID}.md

echo "$SLURM_JOB_NAME finished @ $(date '+%F %X')"
