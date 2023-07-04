#! /bin/bash
set -o errexit
set -o nounset
# usage: bash mk_RJ-mod.sh path/to/lsc/formatted/counts/file.tsv [NUMBER_OF_ITERATIONS NUMBER_OF_CLUSTERS]
LSC_DIR=$(dirname $0)
DATA=${1:-"${LSC_DIR#/source*}/results/freq_out/JxR-frq_thresh5.35f.csv"}
N_I=${2:-'80'}
N_K=${3:-''}
# DATA=${3:-"${LSC_DIR}/data/RJ_top-200j75r_lsc-counts.15f.txt"}
echo "frequency data: $DATA"
du -h --time $DATA

function train_model() {
    N_K=$1
    N_I=$2
    DATA=$3
    LSC_DIR=$4

    MOD_DIR="${LSC_DIR}/models"
    # echo $MOD_DIR
    mkdir -p $MOD_DIR

    MOD="${MOD_DIR}/$(basename ${DATA%.*})_m-${N_K}-${N_I}"
    MOD_TXT="${MOD}.txt"
    echo "model output: ..${MOD#*source}"
    echo
    echo "${LSC_DIR}/src/lsc-train $N_K $N_I $DATA > $MOD"
    ${LSC_DIR}/src/lsc-train $N_K $N_I $DATA > $MOD

    echo
    echo "${LSC_DIR}/src/lsc-print -n 20 ${MOD} > $MOD_TXT"
    ${LSC_DIR}/src/lsc-print -n 10 ${MOD} > $MOD_TXT
    # du -h --time $MOD_TXT
    # head -4 $MOD_TXT
    # head -27 $MOD_TXT | tail -23 | column -ten
    # echo '...'
    # tail -24 $MOD_TXT | column -ten
    # cat data/${MOD}.tsv
}

if [[ -z $N_K ]]; then

    for K in {2..24..2}; do
        echo "for $K clusters..."
        if [[ -z $N_I ]]; then
            for I in {50..150..20}; do
                echo "for $I iterations..."
                echo "train_model $K $I $DATA $LSC_DIR"
                train_model $K $I $DATA $LSC_DIR
            done
        else
            echo "train_model $K $N_I $DATA $LSC_DIR"
            train_model $K $N_I $DATA $LSC_DIR
        fi
    done

else
    echo "train_model $N_K $N_I $DATA $LSC_DIR"
    train_model $N_K $N_I $DATA $LSC_DIR
fi
