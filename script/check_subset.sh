#!/bin/bash
#check_subset.sh

#   usage:
#     check_subset.sh {string} {directory} [-q]
#   Input arguments:

#     1 -> SUBSET_TAG
#       some unique portion of the pattern file *stem*, not the parent dir.
#         This does not have to be the whole thing, but it needs to be something
#         that will correctly identify the associated files. e.g.:
#           'entirely' for Pat/filter/entirely-JJ.pat,
#           'RB-JJ' for Pat/advadj/all-RB-JJs.pat, etc.
#       This will be used for the check_subset.sh output in info/ and then
#       in turn pick out the right file listing the paths to be searched.

#     2 -> PATTERN_PATH
#       the path to the file to create the subset for.
#         This should be the absolute path, since cwd will be set to
#         'data/sanpi/logs/subsets' by slurm

#     3 -> DATA_PATH
#       the path to directory containing original corpus file directories
#         This should be the absolute path, since cwd will be set to
#         'data/sanpi/logs/subsets' by slurm
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

        UPDATE="${PREV_INFO}/prev_$(basename ${1})"
        mv ${1} ${UPDATE}
        sync $(dirname ${1})
        echo -e "previous output moved to\n  >  ..${UPDATE##*info}"
    fi
}
export -f move_prev

function check_conll_dir() {
    # arg 1 = conll dir
    # arg 2 = subset tag
    # arg 3 = info (output) dir
    CONLL_DIR=$1
    #? does this overwrite global??
    DATA_DIR=$(dirname ${CONLL_DIR})
    SUBSET_TAG=$2
    OUT_DIR=$3
    SUBSET_META=$4
    echo -e "\n=== $(basename ${CONLL_DIR}) ===\n$(date +"%D @ %R")"
    OUT_LABEL="$(basename ${CONLL_DIR%.*})_${SUBSET_TAG}"
    CONLL_WITHOUT_SUBSET=${OUT_DIR}/${OUT_LABEL}-subset-missing.txt
    SUBSET_FILES=${OUT_DIR}/${OUT_LABEL}-paths.txt
    #// echo -e "DEBUG INFO (66):\nCONLL_DIR = ${CONLL_DIR}\nOUT_LABEL = ${OUT_LABEL}\nOUT_DIR = ${OUT_DIR}\nCONLL_WITHOUT_SUBSET = ${CONLL_WITHOUT_SUBSET}\nSUBSET_FILES = ${SUBSET_FILES}"

    move_prev ${CONLL_WITHOUT_SUBSET}
    move_prev ${SUBSET_FILES}
    #! There is a bug here where conllus that have no matches for a pattern are always flagged as "missing", so the slurm script for creating the subsets goes into an infinite loop rechecking the same matchless files over and over and over until the job gets cancelled.
    if [[ $(find ${CONLL_DIR} -type d -name "subset*") ]]; then
        echo "= Checking files..."
        for FILE in ${CONLL_DIR}/*.conllu; do
            #> look for subset file
            #> > if found, append *subset* path to confirmed list
            #> > else, append *original* path to missing list
            find ${CONLL_DIR} -maxdepth 2 | egrep "$(basename ${FILE%.conllu}).*${SUBSET_TAG}.*conllu" >>${SUBSET_FILES} || echo ${FILE} >>${CONLL_WITHOUT_SUBSET}
        done
    #! if subset code has *never* been run previously, put all paths in "without" list
    else
        for FILE in ${CONLL_DIR}/*.conllu; do
            echo ${FILE} >>${CONLL_WITHOUT_SUBSET}
        done
    fi
    #> add info to meta csv output
    echo "${CONLL_DIR},${SUBSET_TAG},$(date '+%F'),$(date '+%X'),${CONLL_WITHOUT_SUBSET},${SUBSET_FILES}" >>${SUBSET_META}

    echo -e "Files without corresponding subset files saved to: \n  >  ..${CONLL_WITHOUT_SUBSET##${DATA_DIR}}\nCurrent subset file paths saved to:\n  >  ..${SUBSET_FILES##${DATA_DIR}}"
}
export -f check_conll_dir

#> initialize header row for meta check csv output
SUBSET_META=${INFO_DIR}/${SUBSET_TAG}_check-meta-info.csv
echo "CONLL_DIR,SUBSET_TAG,DATE,TIME,CONLL_WITHOUT_SUBSET_PATH,SUBSET_FILES_PATH" >${SUBSET_META}

#> >>> run all conll dirs in parallel
#>      set number of jobs to number of available cpus (i.e. slurm `-n` flag)
# echo "parallel -j$(nproc) --keep-order "check_conll_dir {} ${SUBSET_TAG} ${INFO_DIR} ${SUBSET_META}" ::: $(find ${DATA_DIR} -maxdepth 1 -type d -name "*.conll" | sort)"
parallel -j$(nproc) --keep-order "check_conll_dir {} ${SUBSET_TAG} ${INFO_DIR} ${SUBSET_META}" ::: $(find ${DATA_DIR} -maxdepth 1 -type d -name "*.conll" | sort)

SUBSET_TOTALS=${INFO_DIR}/${SUBSET_TAG}_total-missing-files.tsv
move_prev ${SUBSET_TOTALS}

ALL_FILE=${INFO_DIR}/ALLpaths_missing-subset.txt
move_prev ${ALL_FILE}

if [[ $(egrep -s "conll" ${INFO_DIR}/*missing.txt) ]]; then
    echo -e "\n---------------------------------\nMissing subset files per data set\n---------------------------------"
    #> grep all the paths in the "missing" output files,
    #>      select only the name and number > to file
    # (find ${INFO_DIR}  -maxdepth 1 -print0 -name "${SUBSET_TAG}*missing.txt" | wc -l --files0-from=- | column -t ) >> >(tee -i -a $SUBSET_TOTALS) 2>&1

    #! was:
    # (egrep -c "conllu" ${INFO_DIR}/*${SUBSET_TAG}*missing.txt | cut -d/ -f 8 | column -t -s: | sort) >> >(tee -i -a $SUBSET_TOTALS) 2>&1
    #! changing to $INFO_DIR may have made $SUBSET_TAG redundant and therefor erroneous
    #^ try w/o $SUBSET_TAG:
    #! need -H to print filepath if only 1 is found (but default behavior for multiple files)
    # echo "(egrep -c -H "conllu" ${INFO_DIR}/*missing.txt | cut -d/ -f 8 | column -t -s: | sort) >> >(tee -i -a $SUBSET_TOTALS) 2>&1"
    (egrep -c -H "conllu" ${INFO_DIR}/*missing.txt | cut -d/ -f 8 | column -t -s: | sort) >> >(tee -i -a $SUBSET_TOTALS) 2>&1

    #> send all the original conllu paths without subset files to a single text file;
    #>      one absolute path per line
    #! was:
    # egrep -h "conllu" ${INFO_DIR}/*${SUBSET_TAG}*missing.txt >${ALL_FILE}
    #! changing to $INFO_DIR may have made $SUBSET_TAG redundant and therefor erroneous
    #^ try w/o $SUBSET_TAG:

    egrep -h "conllu" ${INFO_DIR}/*missing.txt >${ALL_FILE}

elif [[ -d "${INFO_DIR}/prev" ]]; then
    echo -e "\n--------------\n>>> \"${SUBSET_TAG}\" subset for ${DATA_DIR}/ is complete. <<<"
    echo "None" >${ALL_FILE}
else
    echo "!! Warning! No previous output, but no missing subsets found. !!"
fi
