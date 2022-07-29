#!/bin/bash
#SBATCH -N1 
#SBATCH -n6
#SBATCH --mem-per-cpu=10G 
#SBATCH --partition=compling
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 1:30:00
#SBATCH -J pool-test
#SBATCH --chdir=/share/compling/projects/sanpi/demo/logs

echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with:"
echo "  - ${SLURM_NTASKS} cores"
echo "  - ${SLURM_MEM_PER_CPU} mem/cpu"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
DEMO_DIR=/share/compling/projects/sanpi/demo
CORP=${1:-PccX9.conll}
PAT=${2:-advadj/all-RB-JJs.pat}
python ${DEMO_DIR}/source/gather/grew_search.py ${DEMO_DIR}/data/corpora/puddin/${CORP} ${DEMO_DIR}/Pat/${PAT} ${DEMO_DIR}/data/1_json_grew-matches