#!/bin/bash
#SBATCH -N1
#//#SBATCH -n5
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
##SBATCH --partition=compling
#SBATCH -o %x_%j.demo.out
#SBATCH -e %x_%j.demo.err
#SBATCH --time 1:00:00
#SBATCH -J demo-pipe
#SBATCH --chdir=/share/compling/projects/sanpi/demo/logs/pipeline

# bash script to start batch slurm job to run **demo/** grew_search with cluster resources
# usage:
#     sbatch [slurm flags addtions/overrides] slurm_pipeline_test.sh \
#         [path of pattern dir #! relative to ..sanpi/demo/Pat/ (= name of dir containing .pat files)] \
#          ^ RBdirect
#         [path of corpus dir #! relative to ..sanpi/demo/data/corpora/] \
#          ^ subsets/bigrams/bigram_smallest
# *   defaults to: `run_pipeline.py -c ../demo/data/corpora/subsets/bigrams/bigram_smallest -p ../demo/Pat/RBdirect`

echo 'running slurm script: `../sanpi/demo/slurm_pipeline_test.sh`'
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
DEMO_DIR="/share/compling/projects/sanpi/demo"

PAT_IN=${1:-"RBdirect"}
PAT_ARG="${DEMO_DIR}/Pat/${PAT_IN}"

CORP_IN=${2:-"subsets/bigrams/bigram_smallest"}
CORP_ARG="${DEMO_DIR}/data/corpora/${CORP_IN}"

echo "time python ${DEMO_DIR}/run_pipeline.py -c ${CORP_ARG} -p ${PAT_ARG} -g ${DEMO_DIR}/data/1_json_grew-matches"
time python ${DEMO_DIR}/run_pipeline.py -c ${CORP_ARG} -p ${PAT_ARG} -g ${DEMO_DIR}/data/1_json_grew-matches
