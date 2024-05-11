#!/bin/bash
# Runs a Python script for associating data with specified parameters and options. 
# The script generates logs and executes the association metric processing for different frequency thresholds.

# Args:
#     The script takes optional arguments for the target pattern, comparison type. 


SANPI='/share/compling/projects/sanpi'
FRQ="${SANPI}/results/freq_out"

COMPARE='polar' # use 'diff' to get complement of given `$PAT_DIR`
while getopts ":df:s:t:A:C:N:P:" opt; do
  case $opt in
    d) COMPARE="diff" ;; # Set comparison type to diff
    f) N_FILES="${OPTARG/f/}" ;;  # Store the number of corpus parts
    s) SUFF="${OPTARG}" ;; # Store the tsv suffix
    t) TSV_STEM="${OPTARG}" ;;  # Store the tsv stem [! minus "ALL_WORDS_"]
    A) A="${OPTARG}" ;;  # Store the all count path
    C) C="${OPTARG}" ;;  # Store the comparison counts path
    N) N="${OPTARG}" ;;  # Store the neg/target counts path
    P) PAT_DIR="${OPTARG}" ;;  # Store the `PAT_DIR` directory name in $FRQ
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
    esac
done
PAT_DIR="${PAT_DIR:-RBdirect}"
N_FILES="${N_FILES:-35}f"
TSV_STEM="${TSV_STEM:-AdvAdj_frq-thrMIN-7}"

SUFF="${SUFF:-${N_FILES}-${TSV_STEM##*thr}c.tsv}"
SUFF=".${SUFF/MIN-/}"

TSV_STEM="${TSV_STEM}.${N_FILES}"

A=${A:-"${FRQ}/RBXadj/ucs_format/${TSV_STEM}.tsv"}
echo -e "pattern data dir, ${PAT_DIR}\nstem,${TSV_STEM}\nsuffix,${SUFF}\nall_counts,${A}\ncomparison type,${COMPARE}" \
| tabulate -f grid -s ','

if [[ ! $(ls ${A}) ]]; then
    exit
fi

if [[ ${PAT_DIR} == 'RBdirect' ]]; then
    N_NAME='negated'
    C_NAME='complement'
    N=${N:-"${FRQ}/${PAT_DIR}/ucs_format/${TSV_STEM}.tsv"}
    C=${C:-"${FRQ}/${PAT_DIR}/complement/ucs_format/diff_all-${PAT_DIR}_${TSV_STEM}.tsv"}
elif [[ ${COMPARE} == 'polar' &&  ! ${PAT_DIR} =~ 'ANY' ]]; then
    N_NAME='negmir'
    C_NAME='posmir'
    PAT_DIR='NEGmirror'
    N=${N:-"${FRQ}/${PAT_DIR}/ucs_format/${TSV_STEM}.tsv"}
    C=${C:-"${FRQ}/POSmirror/ucs_format/${TSV_STEM}.tsv"}
    A=${A:-"${FRQ}/ANYmirror/ucs_format/${TSV_STEM}.tsv"}
    A="${A/RBXadj/ANYmirror}"
    SUFF=".MIRROR_polar${SUFF}"
else 
    N_NAME=${PAT_DIR::6}
    N_NAME=${N_NAME,,}
    C_NAME='complement'
    N=${N:-"${FRQ}/${PAT_DIR}/ucs_format/${TSV_STEM}.tsv"}
    C=${C:-"${FRQ}/${PAT_DIR}/complement/ucs_format/diff_all-${PAT_DIR}_${TSV_STEM}.tsv"}
    SUFF=".MIRROR_${N_NAME::3}_diff${SUFF}"
fi

date
LOG_DIR="/share/compling/projects/sanpi/logs/associate"
if [[ ! -d $LOG_DIR ]]; then mkdir $LOG_DIR; fi
LOG_PREFIX="${LOG_DIR}/assoc_${PAT_DIR}-${COMPARE}_"
echo "logs ⇰  ${LOG_PREFIX}*x-verbose.$(date +%Y%m)*"

# for FRQ_FLOOR in 50 100 200 1500 3000 6000; do
for FRQ_FLOOR in 6000 3000; do #! #HACK revert to full set of thresholds
    OUT="${LOG_PREFIX}${FRQ_FLOOR}x-verbose.$(date +%Y%m%d_%H%M).out"
    ERR="${OUT/out/err}"
    echo -e "exec 1>${OUT/${SANPI}\//} \\ \n     2>${ERR/${SANPI}\//}"
    exec 1>${OUT} 2>${ERR}
    echo "@ `date +%I:%M%P`"
    echo "time python ${SANPI}/script/polar_assoc.py \\"
    echo -e "  -v -m ${FRQ_FLOOR} \\ \n  --comp_label ${C_NAME} --compare_counts ${C} \\"
    echo -e "  --targ_label ${N_NAME} --target_counts ${N} \\ \n  --all_counts ${A} \\ \n  --data_suffix ${SUFF}"
    echo "..........................................."
    echo
    time python ${SANPI}/script/polar_assoc.py -v -m ${FRQ_FLOOR} -C ${C_NAME} -c ${C} -N ${N_NAME} --target_counts ${N} --data_suffix ${SUFF} --all_counts ${A}
    
done