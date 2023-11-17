#!/bin/bash
#SBATCH -N1
#//#SBATCH -n5
#SBATCH --cpus-per-task=15
#SBATCH --mem-per-cpu=5G
#//#SBATCH --partition=compling
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 3:00:00
#SBATCH -J deps-3h_adj-RBdirect
#SBATCH --chdir=/share/compling/projects/sanpi/logs/collect-deps

# bash script to start batch slurm job to run `source/collect_deps.py` with cluster resources
# usage:
#     sbatch [slurm flags addtions/overrides] slurm_collect-deps.sh 

echo 'running slurm script: `../sanpi/slurm/collect-deps.slurm.sh`'
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
SANPI_DIR="/share/compling/projects/sanpi"
DATA_DIR="/share/compling/data/sanpi"
LOGS_DIR="/share/compling/projects/sanpi/logs/collect-deps"

LOG_FILE="${LOGS_DIR}/${SLURM_JOB_NAME}_$(date +%y-%m-%d).${SLURM_JOB_ID}.log"
# echo -e "time python ${SANPI_DIR}/source/collect_deps.py \ \n\t--input_dir ${DATA_DIR}/2_hit_tables \ \n\t--glob_expr RBdirect/\*hits.pkl.gz \ \n\t--output_dir ${DATA_DIR}/3_dep_info \ \n\t--verbose >> >(tee -i -a ${LOG_FILE}) 2>&1"
# time python ${SANPI_DIR}/source/collect_deps.py --input_dir ${DATA_DIR}/2_hit_tables --glob_expr RBdirect/\*adj\*hits.pkl.gz --output_dir ${DATA_DIR}/3_dep_info --verbose >> >(tee -i -a ${LOG_FILE}) 2>&1
echo -e "time python ${SANPI_DIR}/source/collect_deps.py \ \n\t--input_dir ${DATA_DIR}/2_hit_tables \ \n\t--glob_expr RBdirect/\*hits.pkl.gz \ \n\t--output_dir ${DATA_DIR}/3_dep_info \ \n\t--verbose >> >(tee -i -a ${LOG_FILE})"
time python ${SANPI_DIR}/source/collect_deps.py --input_dir ${DATA_DIR}/2_hit_tables --glob_expr RBdirect/\*adj\*hits.pkl.gz --output_dir ${DATA_DIR}/3_dep_info --verbose >> >(tee -i -a ${LOG_FILE})
