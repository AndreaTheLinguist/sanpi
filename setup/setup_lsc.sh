#!/bin/bash
set -o errexit
LOG=/share/compling/projects/sanpi/setup/lsc_init.$(date +%y-%m-%d_%H%M).log
exec &> >(tee -a "$LOG")
echo "Setting up LSC clustering program..."
date
echo "( output will be saved as ${LOG})"

URL="https://www.cis.lmu.de/~schmid/tools/LSC/data/LSC.tar.gz"
LSC_DEST=${1:-"/share/compling/projects/sanpi/LSC"}
mkdir -p $(dirname $LSC_DEST)

# echo "du -h LSC.tar.gz || wget ${URL}"
du -h LSC.tar.gz || wget ${URL}

# echo "du -h LSC.tar || gzip -dkv LSC.tar.gz"
du -h LSC.tar || gzip -dkv LSC.tar.gz

# echo "du -h $LSC_DEST || ( tar -x -f LSC.tar && mv LSC ${LSC_DEST} )"
du -hc $LSC_DEST || (tar -x -f LSC.tar && mv LSC ${LSC_DEST})

# echo "cd $(dirname $LSC_DEST)"
cd $(dirname $LSC_DEST)
pwd
echo "tree -h $(basename $LSC_DEST)"
tree -h $(basename $LSC_DEST)

# echo "cd ${LSC_DEST}/src"
cd ${LSC_DEST}/src

# echo "make -f Makefile"
make -f Makefile

# echo "cd .."
cd ..
echo
echo '>> README <<'
cat data/README

DEMO_SH="${LSC_DEST}/lsc_demo.sh"
echo -e "\nCreating $DEMO_SH:"
echo '#!/bin/bash' >$DEMO_SH
chmod 777 $DEMO_SH
echo -e "LSC_TOP=${LSC_DEST}" >>$DEMO_SH
echo -e 'DEMO_LOG=${LSC_TOP}/data/lsc_demo.$(date +%y-%m-%d_%H-%M).log\nexec &> >(tee -a "$DEMO_LOG")' >>$DEMO_SH
echo -e 'cd $LSC_TOP\necho "⁘ LSC demo ⁘"\ndate' >>$DEMO_SH
echo "make -f Makefile" >>$DEMO_SH
echo -e 'DATA=${1:-"data/vo.txt"}\nN_CLUST=${2:-"20"}\nN_ITERS=${3:-"50"}\nMOD_NAME="data/m-${N_CLUST}-${N_ITERS}"' >>$DEMO_SH
echo 'echo -e "\n>> Train the model <<"' >>$DEMO_SH
echo 'echo "src/lsc-train ${N_CLUST} ${N_ITERS} ${DATA} > ${MOD_NAME}"' >>$DEMO_SH
echo 'src/lsc-train ${N_CLUST} ${N_ITERS} ${DATA} > ${MOD_NAME}' >>$DEMO_SH

echo 'echo -e "\n>> View the model <<"' >>$DEMO_SH
echo 'echo "src/lsc-print -n 10 ${MOD_NAME} > ${MOD_NAME}.txt"' >>$DEMO_SH
echo 'src/lsc-print -n 10 ${MOD_NAME} > ${MOD_NAME}.txt' >>$DEMO_SH
echo 'echo; head -4 ${MOD_NAME}.txt; head -27 ${MOD_NAME}.txt | tail -23 | column -ten' >>$DEMO_SH
echo "echo -e '...\n'" >>$DEMO_SH
echo 'tail -24 ${MOD_NAME}.txt | column -ten' >>$DEMO_SH

echo -e 'echo\necho ">> Evaluate the model <<"\nMOD_TEST=${4:-"data/vo-test.txt"}\nEVAL=${MOD_TEST%.*}_eval-$(basename ${MOD_NAME}).txt' >>$DEMO_SH
echo 'echo "src/lsc-disambiguate ${MOD_NAME} ${MOD_TEST} > ${EVAL}"' >>$DEMO_SH
echo 'src/lsc-disambiguate ${MOD_NAME} ${MOD_TEST}> ${EVAL}' >>$DEMO_SH
echo "echo; echo '...'" >>$DEMO_SH
echo -e 'tail ${EVAL} | head -6 | column -ten\necho\ntail -4 ${EVAL} | column -ten -s:' >>$DEMO_SH
echo "bash $DEMO_SH"
bash $DEMO_SH
echo 
echo 'LSC set up complete.'
date
