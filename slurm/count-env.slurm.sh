#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=16G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 4:00:00
#SBATCH -J count_env
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/count_env/#//testing #!#HACK remove "testing"

# usage:    sbatch [slurm flags] count-neg.slurm.sh
echo 'running slurm script: /share/compling/projects/sanpi/slurm/count-env.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with $(nproc) cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

# TODO: update this to use `getopts` like `count_RBgrams.slurm.sh`: 
    # while getopts ":t:f:d:" opt; do
    #   case $opt in
    #     t) THRESH="${OPTARG/\%/}" ;;  # Store the threshold percentage
    #     f) N_FILES="${OPTARG%f}" ;;  # Store the number of corpus parts
    #     d) HIT_DATA_DIR="${OPTARG}" ;;  
    #     \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
    #     esac
    # done

SANPI_DATA="/share/compling/data/sanpi"

ENV_NAME=${2:-'RBdirect'}
#> to run on `DEMO` data, prefix argument string with "DEMO/"
REL_PARENT_DIR=${3:-"2_hit_tables"}
HIT_DATA_DIR="${SANPI_DATA}/${REL_PARENT_DIR}/${ENV_NAME}"
echo "processing ➡️ ${HIT_DATA_DIR//*data/..}"

POST_PROC_DIR="${HIT_DATA_DIR%2_hit_tables*}4_post-processed/RBXadj"
#> if no argument given, use most recent frequency index .txt file created in nearest 4_post-processed/RBXadj/ dir
FRQ_FILTER=${1:-"$(ls -t1 $POST_PROC_DIR/*index_frq*.txt  | head -1)"}
#> if number given instead of path, use value to locate relevant frequency index .txt file
if [[ ! (-f $FRQ_FILTER && -r $FRQ_FILTER) ]]; then
    FRQ_FILTER="$( (ls -t1 $POST_PROC_DIR/*index_frq*${FRQ_FILTER/./-}p*.txt || ls -t1 $POST_PROC_DIR/*index_frq*txt ) | head -1 )"
fi
echo -e "Selected frequency filter: \n  ${FRQ_FILTER}"

RESULTS="/share/compling/projects/sanpi/results"
if [[ "${REL_PARENT_DIR%%/*}" == "DEMO" ]]; then
    # HIT_DATA_DIR="${SANPI_DATA}/DEMO/${REL_HIT_DIR}"
    #> replace "results" with "DEMO/results"
    RESULTS="${RESULTS/results/DEMO/results}"
fi
echo -e "Selected output parent directory: \n ${RESULTS}"
mkdir -p $RESULTS


#? Can this can be changed to load from `3_dep_info/` instead?
HIT_DIR_ARG="-d ${HIT_DATA_DIR}"
OUT_DIR_ARG="-o ${RESULTS}/freq_out/${ENV_NAME}"
FRQ_IX_ARG="-b ${FRQ_FILTER}"

PY_MODULE="/share/compling/projects/sanpi/source/analyze/count_env.py"

echo -e "\ntime python ${PY_MODULE}\n    ${HIT_DIR_ARG}\n    ${OUT_DIR_ARG}\n    ${FRQ_IX_ARG}"
time python ${PY_MODULE} ${HIT_DIR_ARG} ${OUT_DIR_ARG} ${FRQ_IX_ARG} #>> >(tee -i -a ${LOG_FILE}) 2>&1
echo
echo "Closing shell script @ $(date)"
exit 