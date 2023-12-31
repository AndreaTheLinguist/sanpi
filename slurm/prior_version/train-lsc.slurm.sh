#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=40G
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#SBATCH --time 6:00:00
#SBATCH -J LSC
#SBATCH --chdir=/share/compling/projects/sanpi/logs
set -o errexit

#> set default parameter values
#// TRAIN_ONLY='false'
FRQ_THR='500'
DATA_GRP='all-frq'
N_FILES='35'
N_ITER='50'
N_CLUST='10'

print_usage() {
    echo "Usage:"
    echo -e "$(basename $0)\t[-t freq_threshold(#_tokens_per_lemma)]\n\t\t\t[-g freq_lemma_group]"
    echo -e "\t\t\t[-f #_corpus_parts_in_freq_data(#_files)]\n\t\t\t[-i #_lsc_iterations]"
    echo -e "\t\t\t[-k #_lsc_clusters]\n\t\t\t[-h]"
    exit 1
}

# process argument flags
while getopts 'f:g:n:i:k:h' flag; do
    case "${flag}" in
    t) FRQ_THR="${OPTARG:-'350'}" ;;
    g) DATA_GRP="${OPTARG:-'all-frq'}" ;;
    h) print_usage ;;
    i) N_ITER="${OPTARG:-'50'}" ;;
    k) N_CLUST="${OPTARG:-'10'}" ;;
    f) N_FILES="${OPTARG:-'35'}" ;;
    #// T) TRAIN_ONLY='true' ;;
    esac
done

echo 'running slurm script: /share/compling/projects/sanpi/slurm/train-lsc.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID:-none}"
echo "JOB NAME: ${SLURM_JOB_NAME:-none}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST:-$(hostname)} with $(nproc) cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi

SANPI_DIR="/share/compling/projects/sanpi"
LSC_DIR="${SANPI_DIR}/source/LSC"
PY_FORMAT="${LSC_DIR}/src/format_counts.py"
SH_PROG="${LSC_DIR}/mk_RJ-mod.sh"
PY_VIEW="${LSC_DIR}/view_model.py"

FRQ_TABLE_FNAME="${DATA_GRP}_thresh${FRQ_THR}.${N_FILES}f.csv"
FRQ_TABLE="${SANPI_DIR}/results/freq_out/${FRQ_TABLE_FNAME}"
echo -e "PARAMETERS:\n  - $FRQ_THR token/lemma threshold\n  - $N_ITER LSC iterations\n  - $N_CLUST LSC clusters\n  - input frequency table: ..${FRQ_TABLE#${SANPI_DIR}}"

if [[ $FRQ_THR -gt 5 ]]; then
    LSC_DATA="${SANPI_DIR}/source/LSC/data/${DATA_GRP}_thresh${FRQ_THR}-${N_FILES}f.tsv"
else
    LSC_DATA="${SANPI_DIR}/source/LSC/data/${DATA_GRP}_thresh5-${N_FILES}f.tsv"
fi
echo "lsc formated counts file: $LSC_DATA"

LOG_STEM="${SLURM_JOB_NAME:-no-job}_${DATA_GRP}_thresh${FRQ_THR}.${SLURM_JOB_ID:-xx}"
echo "log identifier: $LOG_STEM"

if [[ ! -f $LSC_DATA ]]; then
    echo "time python $PY_FORMAT -i $FRQ_TABLE -f $FRQ_THR"
    time python $PY_FORMAT -i $FRQ_TABLE -f $FRQ_THR >> >(tee -i -a ${LOG_STEM}.format.log) 2>&1
fi

echo "time bash ${SH_PROG} ${LSC_DATA} ${N_ITER} ${N_CLUST}"
time bash ${SH_PROG} ${LSC_DATA} ${N_ITER} ${N_CLUST} >> >(tee -i -a ${LOG_STEM}.train.log) 2>&1
