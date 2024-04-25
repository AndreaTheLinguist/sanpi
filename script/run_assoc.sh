#!/bin/bash
"""
Runs a Python script for associating data with specified parameters and options. 
The script generates logs and executes the association metric processing for different frequency thresholds.

Args:
    The script takes optional arguments for the target pattern, comparison type. 
"""
SANPI='/share/compling/projects/sanpi'
FRQ="${SANPI}/results/freq_out"
TARGET_PAT=${1:-'RBdirect'} # directory name in $FRQ
COMPARE=${2:-'polar'} # use 'diff' to get complement of given `$TARGET_PAT`

S='.35f-868c.tsv'
A="${FRQ}/RBXadj/ucs_format/all_adj-x-adv_frq-thr0-001p.35f=868+.tsv"

if [[ ${TARGET_PAT} == 'RBdirect' ]]; then
    N_NAME='negated'
    C_NAME='complement'
    N="${FRQ}/${TARGET_PAT}/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv"
    C="${FRQ}/${TARGET_PAT}/complement/ucs_format/diff_all-${TARGET_PAT}_adj-x-adv_frq-thr0-001p.35f=868+.tsv"
elif [[ ${COMPARE} == 'polar' ]]; then
    N_NAME='negmir'
    C_NAME='posmir'
    TARGET_PAT='NEGmirror'
    N="${FRQ}/${TARGET_PAT}/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv"
    C="${FRQ}/POSmirror/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv"
    A="${FRQ}/ANYmirror/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv"
    S=".MIRROR_${COMPARE}${S}"
else 
    N_NAME=${TARGET_PAT::6}
    N_NAME=${N_NAME,,}
    C_NAME='complement'
    N="${FRQ}/${TARGET_PAT}/ucs_format/ALL-WORDS_adj-x-adv_thr0-001p.35f.tsv"
    C="${FRQ}/${TARGET_PAT}/complement/ucs_format/diff_all-${TARGET_PAT}_adj-x-adv_frq-thr0-001p.35f=868+.tsv"
    S=".MIRROR_${N_NAME::3}_${COMPARE}${S}"
fi

date
LOG_DIR="/share/compling/projects/sanpi/logs/associate"
if [[ ! -d $LOG_DIR ]]; then mkdir $LOG_DIR; fi
LOG_PREFIX="${LOG_DIR}/assoc_${TARGET_PAT}-${COMPARE}_"
echo "logs ⇰  ${LOG_PREFIX}*"

for F in 50 100 800 2000; do
    LOG="${LOG_PREFIX}${F}x-verbose.$(date +%Y%m%d_%H%M).out"
    exec 1>${LOG} 2>${LOG/out/err}
    date +"@ %I:%m%P"
    echo "time python ${SANPI}/script/polar_assoc.py \\"
    echo "  -v -m ${F} \\ \n  -C ${C_NAME} -c ${C} \\"
    echo -e "  -N ${N_NAME} -n ${N} \\ \n  --all_counts ${A} \\ \n  --data_suffix ${S}"
    echo "..........................................."
    echo
    time python ${SANPI}/script/polar_assoc.py -v -m ${F} -C ${C_NAME} -c ${C} -N ${N_NAME} -n ${N} --data_suffix ${S} --all_counts ${A}
    
done