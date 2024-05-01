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

TOP_UCS_DIR="/share/compling/projects/sanpi/results/ucs"
DATA_PATH=${1:-"${TOP_UCS_DIR}/polarized-adv_min50x.ds.gz"}
# if [[ -f "${ARG1}" ]]; then
# DATA_PATH="${ARG1}"
# else
#     DATA_PATH="${TOP_UCS_DIR}/polarized-bigram_min${ARG1}x.ds.gz"
# fi

SUBDIR_NAME=$(basename $(dirname ${DATA_PATH}))
# UCS_DIR=${TOP_UCS_DIR}/${SUBDIR_NAME}
UCS_DIR=$(dirname ${DATA_PATH})
# mkdir -p ${UCS_DIR}

DATA_SET=$(basename ${DATA_PATH/./-})
DATA_SET=${DATA_SET%%.*}

#* initialize logging
LOG_DIR="/share/compling/projects/sanpi/logs/associate/ucs"
LOG_FILE_NAME="ucs_${DATA_SET}"
if [[ ! -d ${LOG_DIR} ]]; then
    mkdir -p ${LOG_DIR}
fi
LOG_PATH=${LOG_DIR}/${LOG_FILE_NAME}.$(date +"%Y-%m-%d_%H%M").log
echo -e "> log will be saved to: ${LOG_PATH}\n..."
exec 1>${LOG_PATH} 2>&1
TMP_DIR=${UCS_DIR}/tmp
mkdir -p ${TMP_DIR}
TMP=${TMP_DIR}/tmp_$(date +"%Y%m%d-%H%M%S").${DATA_SET}

echo "# Manipulating ${DATA_SET} ucs table"
echo "path to this script: $0"
date
echo "(TMP: ${TMP})"

#* check path for ucs install
if [[ ! $(ucsdoc ucs-print | head) ]]; then
    echo "ucs installation not found"
    exit 1
fi

#* Get overview of starting data
echo "## Initial Contingency Info"

ucs-info -l -s -v ${DATA_PATH}
echo -e '========================================\n'
echo "ucs-sort -v ${DATA_PATH} BY f- f1- f2- | ucs-print -v -i | head -12"
ucs-sort -v ${DATA_PATH} BY f- f1- f2- | ucs-print -v -i | head -12
echo -e '::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n'
#* Declare association metrics
SCORES_PATH=${DATA_PATH/.ds./.scores.}

#> set built-in association measures to use. More information for the measures can be found with `ucsdoc ucsam`, `ucs-list-am`, or at http://www.collocations.de/AM/index.html
# INIT_SCORES=${3:-$(echo am.{log.likelihood,log.likelihood.pv,log.likelihood.tt,log.likelihood.tt.pv,Poisson.pv,odds.ratio,odds.ratio.disc,Dice,t.score,t.score.pv,multinomial.likelihood.pv,binomial.pv,binomial.likelihood.pv})}
# ! #BUG some issue with the installation versions of UCS and R is preventing the .pv and MI.conf scores
# INIT_SCORES=${3:-$(echo am.{log.likelihood,log.likelihood.tt,odds.ratio,odds.ratio.disc,Dice,t.score})}
# INIT_SCORES=${3:-$(echo am.{log.likelihood,log.likelihood.tt,odds.ratio.disc,Dice,t.score})}
# INIT_SCORES=${3:-$(echo am.{log.likelihood,MI,odds.ratio.disc,Jaccard,gmean,relative.risk,t.score,chi.squared.corr})}
#*  MARK:ADD
INIT_SCORES=${3:-$(echo am.{log.likelihood,odds.ratio.disc})}
echo -e "## built-in association metrics (all symmetric) to be added:${INIT_SCORES//am./"\n+ am."}"
# PJ="am.p.joint := (%O11% / %N%)"
DELTA_P1="am.p1.given2 := (%O11% / %C1%) - (%O12% / %C2%)"
DELTA_P2="am.p2.given1 := (%O11% / %R1%) - (%O21% / %R2%)"
P1="am.p1.given2.simple := (%O11% / %C1%)"
P2="am.p2.given1.simple := (%O11% / %R1%)"
# P1_MARG_ADJUST="am.p1.given2.margin := (%O11% / %C1%) - (%R1% / %N%)"
# P2_MARG_ADJUST="am.p2.given1.margin := (%O11% / %R1%) - (%C1% / %N%)"
#// EXPECT_DIFF="am.expect.diff := (%O11% - %E11%)"

USER_SCORES="${DELTA_P1} ${DELTA_P2} ${P1} ${P2}" # ${P1_MARG_ADJUST} ${P2_MARG_ADJUST}" #${EXPECT_DIFF}"
echo -e "\n## derived association metrics to be added:\n(adjusted conditional probabilities)${USER_SCORES//'am.'/'\n+ am.'}\n"
SCORES_STR="${INIT_SCORES} ${USER_SCORES}"
N_SCORES_REQ=$(echo -e "${SCORES_STR//'am.'/'\nam.'}" | egrep -c 'am\.')

#* add association metric columns
#[ ] below could be a single dysjunctive `if` statement, but I'm not going to mess with it now since it's working
echo "Table with Scores: ${SCORES_PATH}"
#> if scores-modified table not found
if [[ ! -f ${SCORES_PATH} ]]; then
    #> add additional columns to table for computation
    add_extra_fvar ${DATA_PATH} ${TMP}
    echo -e "\n> adding association metric scores:"
    # echo 'ucs-add -v -x htest ${INIT_SCORES} "${DELTA_P1}" "${DELTA_P2}" "${P1}" "${P2}" "${P1_MARG_ADJUST}" "${P2_MARG_ADJUST}" TO ${TMP} INTO ${SCORES_PATH}'
    # echo "ucs-add -v -x htest ${INIT_SCORES} \"${DELTA_P1}\" \"${DELTA_P2}\" \"${P1}\" \"${P2}\" \"${P1_MARG_ADJUST}\" \"${P2_MARG_ADJUST}\" TO ${TMP} INTO ${SCORES_PATH}"
    # ucs-add -v -x htest ${INIT_SCORES} "${DELTA_P1}" "${DELTA_P2}" "${P1}" "${P2}" "${P1_MARG_ADJUST}" "${P2_MARG_ADJUST}" TO ${TMP} INTO ${SCORES_PATH}
    echo 'ucs-add -v -x ALL ${INIT_SCORES} "${DELTA_P1}" "${DELTA_P2}" "${P1}" "${P2}" TO ${TMP} INTO ${SCORES_PATH}'
    echo "ucs-add -v -x ALL ${INIT_SCORES} \"${DELTA_P1}\" \"${DELTA_P2}\" \"${P1}\" \"${P2}\" TO ${TMP} INTO ${SCORES_PATH}"
    ucs-add -v -x ALL ${INIT_SCORES} "${DELTA_P1}" "${DELTA_P2}" "${P1}" "${P2}" TO ${TMP} INTO ${SCORES_PATH}

else
    SCORES_N="$(ucs-info -l ${SCORES_PATH} | egrep -c 'am\.')"

    #> or if found scores-modified table does not have the same number of metrics as current set
    if [[ "${SCORES_N}" != "${N_SCORES_REQ}" ]]; then
        echo "${SCORES_N} metric columns found in existing scores table."
        echo "${N_SCORES_REQ} metrics in current request"
        #> add additional columns to table for computation
        add_extra_fvar ${DATA_PATH} ${TMP}
        echo -e "\n> adding association metric scores..."
        echo "ucs-add -v ${INIT_SCORES} '${DELTA_P1}' '${DELTA_P2}' TO ${TMP} INTO ${SCORES_PATH}"
        ucs-add -v ${INIT_SCORES} "${DELTA_P1}" "${DELTA_P2}" TO ${TMP} INTO ${SCORES_PATH}

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
#! #BUG The odds.ratio measure appears to be broken for the "polarized-bigrams" dataset
#// SORT=${2:-'r.odds.ratio r.log.likelihood'}
SORT=${2:-'r.p1.given2 r.odds.ratio.disc r.log.likelihood '}
# SORT=${2:-'r.Dice r.log.likelihood'}
# SORT=${2:-'r.p1.given2 r.log.likelihood'}
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
TOP_N=500
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
