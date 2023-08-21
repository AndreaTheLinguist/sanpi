#!/bin/bash
# set -o errexit
set -o nounset
set -o pipefail

function add_extra_fvar() {
    local in_path=$1
    local out_path=$2
    echo -e "\n> adding detailed contingency table variables:"
    echo "ucs-add 'E11' 'O%' 'C%' 'R%' TO ${DATA_PATH} INTO ${TMP}"
    ucs-add 'E11' 'O%' 'C%' 'R%' TO ${DATA_PATH} INTO ${TMP}
}

LOG_DIR=logs
UCS_DIR="/share/compling/projects/sanpi/results/ucs_tables"
ARG1=${1:-8777}
if [[ -f "${ARG1}" ]]; then
    DATA_PATH="${ARG1}"
else
    DATA_PATH="${UCS_DIR}/all-frq_thresh${ARG1}.35f-min3x.ds.gz"
fi

DATA_SET=$(basename ${DATA_PATH/./-})
DATA_SET=${DATA_SET%%.*}

#* initialize logging
LOG_DIR="/share/compling/projects/sanpi/logs/ucs"
LOG_FILE_NAME="ucs_${DATA_SET}"
if [[ ! -d ${LOG_DIR} ]]; then
    mkdir -p ${LOG_DIR}
fi
LOG_PATH=${LOG_DIR}/${LOG_FILE_NAME}.$(date +"%Y-%m-%d_%R").log
echo -e "> log will be saved to: ${LOG_PATH}\n..."
exec 1>${LOG_PATH} 2>&1

echo "# Manipulating ${DATA_SET} ucs table"
echo "path to this script: $0"
date

#* check path for ucs install
if [[ ! $(ucsdoc ucs-print | head) ]]; then
    echo "ucs installation not found"
    exit 1
fi

#* Get overview of starting data
echo "## Initial Contingency Info"
TMP=${UCS_DIR}/tmp-ucs.ds.gz
ucs-info -l -s -v ${DATA_PATH}
echo -e '========================================\n'
echo "ucs-sort -v ${DATA_PATH} BY f- f1- | ucs-print -v -i | head -12"
ucs-sort -v ${DATA_PATH} BY f- f1- | ucs-print -v -i | head -12
echo -e '::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n'
#* Declare association metrics
SCORES_PATH=${DATA_PATH/.ds./.scores.}
INIT_SCORES=${3:-$(echo am.{log.likelihood,Poisson.Stirling,odds.ratio,Dice})}
echo -e "## built-in _symmetric_ association metrics to be added:${INIT_SCORES//am./"\n+ am."}"

PEX_DEF="am.dPEX := (%O11% / %C1%) - (%O12% / %C2%)"
PXE_DEF="am.dPXE := (%O11% / %R1%) - (%O21% / %R2%)"
USER_SCORES="${PEX_DEF} ${PXE_DEF}"
echo -e "\n## derived *assymetric* association metrics to be added:\n(adjusted conditional probabilities)${USER_SCORES//'am.'/'\n+ am.'}\n"
SCORES="${INIT_SCORES} ${USER_SCORES}"
N_SCORES_REQ=$(echo -e "${SCORES//'am.'/'\nam.'}" | egrep -c 'am\.')

#* add association metric columns
#FIXME below could be a single dysjunctive `if` statement, but I'm not going to mess with it now since it's working
echo "Table with Scores: ${SCORES_PATH}"
#> if scores-modified table not found
if [[ ! -f ${SCORES_PATH} ]]; then
    #> add additional columns to table for computation
    add_extra_fvar ${DATA_PATH} ${TMP}
    echo -e "\n> adding association metric scores:"
    echo "ucs-add -v ${INIT_SCORES} '${PEX_DEF}' '${PXE_DEF}' TO ${TMP} INTO ${SCORES_PATH}"
    ucs-add -v ${INIT_SCORES} "${PEX_DEF}" "${PXE_DEF}" TO ${TMP} INTO ${SCORES_PATH}
else
    SCORES_N="$(ucs-info -l ${SCORES_PATH} | egrep -c 'am\.')"

    #> or if found scores-modified table does not have the same number of metrics as current set
    if [[ "${SCORES_N}" != "${N_SCORES_REQ}" ]]; then
        echo "${SCORES_N} metric columns found in existing scores table."
        echo "${N_SCORES_REQ} metrics in current request"
        #> add additional columns to table for computation
        add_extra_fvar ${DATA_PATH} ${TMP}
        echo -e "\n> adding association metric scores..."
        echo "ucs-add -v ${INIT_SCORES} '${PEX_DEF}' '${PXE_DEF}' TO ${TMP} INTO ${SCORES_PATH}"
        ucs-add -v ${INIT_SCORES} "${PEX_DEF}" "${PXE_DEF}" TO ${TMP} INTO ${SCORES_PATH}
    else
        echo -e "↻ Prior computation of metrics will be used.\n"
    fi
fi

#* add ranks for all association metrics (any `'am.%'`)
RANKS_PATH=${DATA_PATH/.ds./.ranks.}
echo "Table with Ranks: ${RANKS_PATH}"
if [[ ! -f ${RANKS_PATH} ]]; then
    echo -e "\n> converting 'am.%' columns to ranks..."
    ucs-add -v 'r.%' TO ${SCORES_PATH} INTO ${RANKS_PATH}
else
    RANK_N="$(ucs-info -l ${RANKS_PATH} | egrep -c 'r\.')"
    if [[ "${RANK_N}" != "${N_SCORES_REQ}" ]]; then
        echo "${RANK_N} metric rank columns found in existing ranks table."
        echo "${N_SCORES_REQ} metrics in current request"
        echo -e "\n> converting 'am.%' columns to ranks..."
        ucs-add -v 'r.%' TO ${SCORES_PATH} INTO ${RANKS_PATH}
    else
        echo -e "↻ Prior computation of ranks will be used.\n"
    fi
fi

#* sort table rows
SORT_PATH=${DATA_PATH/.ds./.rsort.}
echo "Sorted Table: ${SORT_PATH}"
SORT=${2:-'r.odds.ratio r.log.likelihood'}
if [[ ! -f ${SORT_PATH} ]]; then

    echo -e "\n> sorting data table by: ${SORT//' '/' then '}"
    ucs-sort -v ${RANKS_PATH} BY ${SORT} INTO ${SORT_PATH}

else
    SORT_N="$(ucs-info -l ${SORT_PATH} | egrep -c 'am\.')"

    if [[ "${SORT_N}" != "${N_SCORES_REQ}" ]]; then
        echo "${SORT_N}  metric columns found in existing sorted table."
        echo "${N_SCORES_REQ} metrics in current request"
        echo -e "\n> sorting data table by: ${SORT//' '/' then '}"
        ucs-sort -v ${RANKS_PATH} BY ${SORT} INTO ${SORT_PATH}
    else
        echo -e "↻ Prior sorting output will be used.\n"
    fi
fi

#* create text samples of table
VIEW_DIR="${UCS_DIR}/readable"
if [[ ! -d ${VIEW_DIR} ]]; then
    mkdir -p $VIEW_DIR
fi
VIEW_PATH=${VIEW_DIR}/`basename $SORT_PATH`
VIEW_PATH=${VIEW_PATH/.gz/-view.txt}
# ucs-print -v -o ${VIEW_PATH} 'l1' 'l2' 'f' 'E11' 'r.%' 'am.%' 'f1' 'f2' 'N' FROM ${SORT_PATH}
# ucs-print -i ${VIEW_PATH} | head -30
ucs-info -l -v ${SORT_PATH}
TOP_N=200
TOP_N_PATH=${VIEW_PATH/.txt/"_top${TOP_N}.txt"}
ucs-print -v -p ${TOP_N} -d 2 'l1' 'l2' 'f' 'E11' 'r.%' 'am.%' 'f1' 'f2' 'N' FROM ${SORT_PATH} | head -$((TOP_N + 2)) >${TOP_N_PATH}
head -30 $TOP_N_PATH
echo
ucs-print -v -o ${VIEW_PATH} \
    'l1' 'l2' 'f' 'E11' 'r.%' 'am.%' 'f1' 'f2' 'N' FROM ${SORT_PATH}
ucs-print -v -o ${VIEW_PATH/.txt/_r-only.txt} \
    'l1' 'l2' 'f' 'E11' 'r.%' 'f1' 'f2' 'N' FROM ${SORT_PATH}
ucs-print -v -o ${VIEW_PATH/.txt/_am-only.txt} \
    'l1' 'l2' 'f' 'E11' 'am.%' 'f1' 'f2' 'N' FROM ${SORT_PATH}
echo "Script finished at $(date)"
