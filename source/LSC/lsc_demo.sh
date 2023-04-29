#!/bin/bash
LSC_TOP=/share/compling/projects/sanpi/source/LSC
DEMO_LOG=${LSC_TOP}/data/lsc_demo.$(date +%y-%m-%d_%H-%M).log
exec &> >(tee -a "$DEMO_LOG")
cd $LSC_TOP
echo "⁘ LSC demo ⁘"
date
make -f Makefile
DATA=${1:-"data/vo.txt"}
N_CLUST=${2:-"20"}
N_ITERS=${3:-"50"}
MOD_NAME="data/m-${N_CLUST}-${N_ITERS}"
echo -e "\n>> Train the model <<"
echo "src/lsc-train ${N_CLUST} ${N_ITERS} ${DATA} > ${MOD_NAME}"
src/lsc-train ${N_CLUST} ${N_ITERS} ${DATA} >${MOD_NAME}
echo -e "\n>> View the model <<"
echo "src/lsc-print -n 10 ${MOD_NAME} > ${MOD_NAME}.txt"
src/lsc-print -n 10 ${MOD_NAME} >${MOD_NAME}.txt
echo
head -4 ${MOD_NAME}.txt
head -27 ${MOD_NAME}.txt | tail -23 | column -ten
echo -e '...\n'
tail -24 ${MOD_NAME}.txt | column -ten
echo
echo ">> Evaluate the model <<"
MOD_TEST=${4:-"data/vo-test.txt"}
EVAL=${MOD_TEST%.*}_eval-$(basename ${MOD_NAME}).txt
echo "src/lsc-disambiguate ${MOD_NAME} ${MOD_TEST} > ${EVAL}"
src/lsc-disambiguate ${MOD_NAME} ${MOD_TEST} >${EVAL}
echo
echo '...'
tail ${EVAL} | head -6 | column -ten
echo
tail -4 ${EVAL} | column -ten -s:
