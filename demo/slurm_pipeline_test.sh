#!/bin/bash
#SBATCH -N1
#SBATCH -n4
#SBATCH --mem-per-cpu=10G
#SBATCH --partition=compling
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 1:00:00
#SBATCH -J pipe-test
#SBATCH --chdir=/share/compling/projects/sanpi/demo/logs

# bash script to start batch slurm job to run **demo/** grew_search with cluster resources
# usage:
#     sbatch [slurm flags addtions/overrides] slurm_pipeline_test.sh \
#         [path of corpus dir relative to ..sanpi/demo/data/corpora/] \
#         [path of pattern dir relative to ..sanpi/demo/Pat/ (= name of dir containing .pat files)] \
#   *Note: includes -R flag automatically (files will be overwritten)

echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with:"
echo "  - ${SLURM_NTASKS} cores"
echo "  - ${SLURM_MEM_PER_CPU} mem/cpu"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate dev-sanpi
DEMO_DIR="/share/compling/projects/sanpi/demo"

CORP_IN=${1:-"puddin/PccX5.conll"}
CORP_ARG="${DEMO_DIR}/data/corpora/${CORP_IN}"

PAT_IN=${2:-"contig"}
PAT_ARG="${DEMO_DIR}/Pat/${PAT_IN}"

echo "time python ${DEMO_DIR}/run_pipeline.py -R -c ${CORP_ARG} -p ${PAT_ARG} -g ${DEMO_DIR}/data/1_json_grew-matches"
time python ${DEMO_DIR}/run_pipeline.py -R -c ${CORP_ARG} -p ${PAT_ARG} -g ${DEMO_DIR}/data/1_json_grew-matches
