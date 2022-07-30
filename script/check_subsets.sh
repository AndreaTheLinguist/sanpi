#!/bin/bash
#check_subsets.sh

SUBSET_TAG=${1:-exactly}
PUDDIN_DIR=/share/compling/data/puddin
DATA_DIR=${2:-${PUDDIN_DIR}}
echo -e "Searching ${DATA_DIR} for \`${SUBSET_TAG}\` subset .conllu files"

INFO_DIR=${DATA_DIR}/info/${SUBSET_TAG}_subset
mkdir -p ${INFO_DIR}


function move_prev() {
    # arg = filepath to existing info
    if [[ -f ${1} ]]; then

        PREV_INFO="$(dirname ${1})/prev"
        mkdir -p ${PREV_INFO}

        UPDATE="$PREV_INFO/prev_$( basename ${1} )"
        mv ${1} ${UPDATE}
        sync $( dirname ${1} )
        echo -e "previous output moved to\n  >  ..${UPDATE##*puddin}"
    fi
}
export -f move_prev

function check_conll_dir() {
    # arg 1 = conll dir
    # arg 2 = subset tag
    # arg 3 = info (output) dir
    CONLL_DIR=$1
    DATA_DIR=$( dirname ${CONLL_DIR} )
    SUBSET_TAG=$2
    INFO_DIR=$3
    SUBSET_META=$4
    echo -e "\n=== $( basename ${CONLL_DIR} ) ===\n$( date +"%D @ %R" )"

    OUT_LABEL="$( basename ${CONLL_DIR%.*})_${SUBSET_TAG}"
    CONLL_WITHOUT_SUBSET=${INFO_DIR}/${OUT_LABEL}-subset-missing.txt
    SUBSET_FILES=${INFO_DIR}/${OUT_LABEL}-paths.txt
    
    move_prev ${CONLL_WITHOUT_SUBSET}
    move_prev ${SUBSET_FILES}

    if [[ `find ${CONLL_DIR} -type d -name "subset*"` ]]; then
        echo "= Checking files..."
        for FILE in ${CONLL_DIR}/*.conllu ; do 
            #) look for subset file
            #) > if found, append *subset* path to confirmed list
            #) > else, append *original* path to missing list
            find ${CONLL_DIR} -maxdepth 2 | egrep "$( basename ${FILE%.conllu} ).*${SUBSET_TAG}.*conllu" >> ${SUBSET_FILES} || echo ${FILE} >> ${CONLL_WITHOUT_SUBSET} 
        done
    fi
    #) add info to meta csv output
    echo "${CONLL_DIR},${SUBSET_TAG},$(date '+%F'),$(date '+%X'),${CONLL_WITHOUT_SUBSET},${SUBSET_FILES}" >> ${SUBSET_META}

    echo -e "Files without corresponding subset files saved to: \n  >  ..${CONLL_WITHOUT_SUBSET##${DATA_DIR}}\nCurrent subset file paths saved to:\n  >  ..${SUBSET_FILES##${DATA_DIR}}"
}
export -f check_conll_dir

#) initialize header row for meta check csv output
SUBSET_META=${INFO_DIR}/${SUBSET_TAG}_check-meta-info.csv
echo "CONLL_DIR,SUBSET_TAG,DATE,TIME,CONLL_WITHOUT_SUBSET_PATH,SUBSET_FILES_PATH" > ${SUBSET_META}

#) >>> run all conll dirs in parallel
#)      set number of jobs to number of available cpus (i.e. slurm `-n` flag)
parallel -j$( nproc ) --keep-order "check_conll_dir {} ${SUBSET_TAG} ${INFO_DIR} ${SUBSET_META}" ::: $(find ${DATA_DIR} -maxdepth 1 -type d -name "*.conll" | sort )

SUBSET_TOTALS=${INFO_DIR}/${SUBSET_TAG}_total-missing-files.tsv
move_prev ${SUBSET_TOTALS}
# if [[ -e ${SUBSET_TOTALS} ]]; then rm ${SUBSET_TOTALS}; fi

echo -e "\n---------------------------------\nMissing subset files per data set\n---------------------------------"
#) grep all the paths in the "missing" output files, 
#)      select only the name and number > to file
# (find ${INFO_DIR}  -maxdepth 1 -print0 -name "${SUBSET_TAG}*missing.txt" | wc -l --files0-from=- | column -t ) >> >(tee -i -a $SUBSET_TOTALS) 2>&1
(egrep -c "conllu" ${INFO_DIR}/*${SUBSET_TAG}*missing.txt  | cut -d/ -f 8 | column -t -s: | sort ) >> >(tee -i -a $SUBSET_TOTALS) 2>&1

#) send all the original conllu paths without subset files to a single text file;
#)      one absolute path per line

ALL_FILE=${INFO_DIR}/ALLpaths_missing-subset.txt
move_prev $ALL_FILE
egrep -h "conllu" ${INFO_DIR}/*${SUBSET_TAG}*missing.txt > $ALL_FILE
