#! /bin/bash

LSC_DIR=$(dirname $0)
N_K=${1:-'6'}
N_I=${2:-'80'}
# DATA=${3:-"${LSC_DIR}/data/RJ_top-200j75r_lsc-counts.15f.txt"}
DATA=${3:-"${LSC_DIR}/data/RJ_scale-diag_lsc-counts.15f.txt"}

MOD_DIR="${LSC_DIR}/models"
# echo $MOD_DIR
mkdir -p $MOD_DIR

MOD="${MOD_DIR}/$(basename ${DATA%_*})_m-${N_K}-${N_I}"
# echo $MOD
MOD_TXT="${MOD}.txt"
echo "frequency data: $DATA" 
du -h --time $DATA
echo "model output: ..${MOD#*source}"
echo
src/lsc-train $N_K $N_I $DATA > $MOD
echo
du -h --time $MOD
echo
src/lsc-print -n 10 ${MOD} > $MOD_TXT
du -h --time $MOD_TXT
head -4 $MOD_TXT
head -27 $MOD_TXT | tail -23 | column -ten
echo '...'
tail -24 $MOD_TXT | column -ten
# cat data/${MOD}.tsv


