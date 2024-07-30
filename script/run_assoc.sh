#!/bin/bash
# Runs a Python script for associating data with specified parameters and options. 
# The script generates logs and executes the association metric processing for different frequency thresholds.

# Args:
#     The script takes optional arguments for the target pattern, comparison type. 
set -o nounset
set -o pipefail
set -o errexit

eval "$(conda shell.bash hook)"
conda activate sanpi

SANPI='/share/compling/projects/sanpi'
FRQ_T="${SANPI}/results/freq_tsv"
FRQ_O="${SANPI}/results/freq_out"
MIN=0
COMPARE='polar' # use 'diff' to get complement of given `$PAT_DIR`
# echo $COMPARE # use 'diff' to get complement of given `$PAT_DIR`
while getopts ":dEs:t:A:C:N:P:m:" opt; do
  case $opt in
    d) COMPARE="diff" ;; # Set comparison type to diff
    E) DATASET="NEQ" ;; # Set dataset tag to "NEQ" instead of "ALL"
    # f) N_FILES="${OPTARG/f/}" ;;  # Store the number of corpus parts
    s) SUFF="${OPTARG}" ;; # Store the tsv suffix
    t) TSV_STEM="${OPTARG}" ;;  # Store the tsv stem [! minus "ALL_WORDS_"]
    A) A="${OPTARG}" ;;  # Store the all count path
    C) C="${OPTARG}" ;;  # Store the comparison counts path
    N) N="${OPTARG}" ;;  # Store the neg/target counts path
    P) PAT_DIR="${OPTARG}" ;;  # Store the `PAT_DIR` directory name in $FRQ_O
    m) MIN="${OPTARG}" ;; # Store joint frequency floor for visibility in AM tables
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
    esac
done

PAT_DIR="${PAT_DIR:-RBdirect}"
# echo PAT_DIR="${PAT_DIR}"
DATASET="${DATASET:-ALL}"
# echo DATASET=${DATASET}
PAT_SUFF=${PAT_DIR:(-6)}
# echo PAT_SUFF="${PAT_SUFF}"
TSV_STEM="${TSV_STEM:-AdvAdj_${DATASET}_*${PAT_SUFF}*}"
# echo TSV_STEM="${TSV_STEM}"
# find "${FRQ_T}" -name "${TSV_STEM}" -exec wc -l '{}' \;
SUFF="${SUFF:-final-freq.tsv}"
if [[ ${DATASET} == 'NEQ' ]]; then
    SUFF="${SUFF}"
fi

A=${A:-"${FRQ_T}/ANY${PAT_DIR/[A-Z]*[A-Z]/}/${TSV_STEM/\*${PAT_SUFF}/any-${PAT_SUFF}}*${SUFF}"}
A=$(ls ${A})


LOG_DIR="/share/compling/projects/sanpi/logs/associate"

if [[ ${PAT_DIR} == 'RBdirect' ]]; then
    N_NAME='negated'
    C_NAME='complement'
    N=${N:-"${FRQ_T}/${PAT_DIR}/${TSV_STEM/\*${PAT_SUFF}/${PAT_DIR}}${SUFF}"}
    N="${N/NEQ/ALL}"
    C=${C:-"${FRQ_T}/${PAT_DIR}/${TSV_STEM/\*${PAT_SUFF}/not-${PAT_DIR}}${SUFF}"}


# TODO adjust the remaining options to run *mirror data
elif [[ ${COMPARE} == 'polar' && ${PAT_SUFF} == 'mirror' &&  ! ${PAT_DIR} =~ 'ANY' ]]; then
    N_NAME='negmir'
    C_NAME='posmir'
    # PAT_DIR='mirror'
    N=${N:-"${FRQ_T}/${PAT_DIR}/${TSV_STEM/\*${PAT_SUFF}/NEG${PAT_DIR}}${SUFF}"}
    N="${N/NEQ/ALL}"
    # N=$(ls ${N})
    # # echo "N='${N}'"
    # du -h --time "${N}"
    # N=${N:-"${FRQ_O}/${PAT_DIR}/ucs_format/${TSV_STEM}.tsv"}
    C=${C:-"${FRQ_T}/${PAT_DIR}/${TSV_STEM/\*${PAT_SUFF}/POS${PAT_DIR}}${SUFF}"}
    # C=$(ls ${C})
    # # echo "C='${C}'"
    # du -h --time "${C}"
    # C=${C:-"${FRQ_O}/POSmirror/ucs_format/${TSV_STEM}.tsv"}
    # A=${A:-"${FRQ_O}/ANYmirror/ucs_format/${TSV_STEM}.tsv"}
    # A="${A/RBXadj/ANYmirror}"
    # SUFF=".MIRROR_polar${SUFF}"
# else 
#     N_NAME=${PAT_DIR::6}
#     N_NAME=${N_NAME,,}
#     C_NAME='complement'
#     N=${N:-"${FRQ_O}/${PAT_DIR}/ucs_format/${TSV_STEM}.tsv"}
#     C=${C:-"${FRQ_O}/${PAT_DIR}/complement/ucs_format/diff_all-${PAT_DIR}_${TSV_STEM}.tsv"}
#     SUFF=".MIRROR_${N_NAME::3}_diff${SUFF}"
#     LOG_DIR=${LOG_DIR}/mirror_eval
fi

function custom_du() {
    FILE=$1
    du -Lh --time --time-style='+%Y/%m/%d_%-I:%M%P' ${FILE}

}

N=$(ls ${N})
C=$(ls ${C})


# du -h --time "${A}"

SUFF="${SUFF/freq/${PAT_SUFF}}"
SUFF="${SUFF/final/${DATASET}}"

echo -e "↯ running '$(pwd)/${0}'\n$(date)" | tabulate -1 -s, -f heavy_outline
echo
echo ">> Parameters <<"
echo -e "frequency dir name, ${PAT_DIR}\nstem,${TSV_STEM}\nsuffix,${SUFF}\ncomparison type,${COMPARE}" \
| tabulate -f simple_grid -s ','

echo ">> Selected Inputs <<"
HEADER="Environment\tSize\tModified\tPath"
N_INFO="${N_NAME^^}\t$(custom_du ${N})"
N_INFO=${N_INFO/"$(dirname ${FRQ_T})"/'.'}
C_INFO="${C_NAME^^}\t$(custom_du ${C})"
C_INFO=${C_INFO/"$(dirname ${FRQ_T})"/'.'}
A_INFO="COMBINED\t$(custom_du ${A})"
A_INFO=${A_INFO/"$(dirname ${FRQ_T})"/'.'}
echo -e "${HEADER}\n${N_INFO}\n${C_INFO}\n${A_INFO}" | tabulate -f simple_grid -1

LOG_DIR=${LOG_DIR}/polar_${PAT_SUFF}
if [[ ! -d ${LOG_DIR} ]]; then mkdir "${LOG_DIR}"; fi
LOG_PREFIX="${LOG_DIR}/assoc-${DATASET}_${PAT_DIR}-${COMPARE}_"
DAY="$(date +%y%m%d)"
echo "logs ↣ '${LOG_PREFIX}*x.${DAY}*'" | tabulate -s , -1 -f rst

# for FRQ_FLOOR in 50 75 120; do
# for FRQ_FLOOR in 50 120 200 500 700 1000 2000; do
function execute_py_script() {
    TSV_STEM=${1}
    FRQ_FLOOR=${2}
    SANPI=${3}
    N=${4}
    C=${5}
    A=${6}
    N_NAME=${7}
    C_NAME=${8}
    SUFF=${9}
    
    echo "# "\`${TSV_STEM}\`" AM processing for ${FRQ_FLOOR}+ joint frequency"
    echo -e "\n started @ `date +%-I:%M%P` \n"
    echo '```shell'
    echo "time python ${SANPI}/script/polar_assoc.py \\"
    echo -e "  -v -m ${FRQ_FLOOR} \\ \n  --comp_label ${C_NAME} --compare_counts ${C} \\"
    echo -e "  --targ_label ${N_NAME} --target_counts ${N} \\ \n  \
        --all_counts ${A} \\ \n  --data_suffix ${SUFF}"
    echo '```'
    echo
    echo "*******************************************"
    echo
    # echo "time python ${SANPI}/script/polar_assoc.py -v -m ${FRQ_FLOOR} -C ${C_NAME} -c ${C} -N ${N_NAME} --target_counts ${N} --data_suffix ${SUFF} --all_counts ${A}"

    time python ${SANPI}/script/polar_assoc.py -v -m ${FRQ_FLOOR} -C ${C_NAME} -c ${C} -N ${N_NAME} --target_counts ${N} --data_suffix ${SUFF} --all_counts ${A}
    
}

if [[ ${MIN} != '0' ]]; then
    FRQ_FLOOR="${MIN}"
    LOG="${LOG_PREFIX}${FRQ_FLOOR}x.${DAY}-$(date +%H%M).log"

     echo "${FRQ_FLOOR}+ log: '${LOG}'" 
    ( execute_py_script $TSV_STEM $FRQ_FLOOR $SANPI ${N} ${C} ${A} ${N_NAME} ${C_NAME} ${SUFF} ) 1>${LOG} 2>&1

else 
    for FRQ_FLOOR in 2000 1000 500 300 100 50 25 5 3; do
        LOG="${LOG_PREFIX}${FRQ_FLOOR}x.${DAY}-$(date +%H%M).log"

        echo "${FRQ_FLOOR}+ log: '${LOG}'" 
        ( execute_py_script $TSV_STEM $FRQ_FLOOR $SANPI ${N} ${C} ${A} ${N_NAME} ${C_NAME} ${SUFF} ) 1>${LOG} 2>&1
    done
fi
#// echo "[[ 🛑 reached temp exit ]]"
#// exit #! # HACK temp
