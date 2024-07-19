#!/bin/bash

TABLES_DIR='/share/compling/data/sanpi/2_hit_tables'
PAT_CAT=${2:-'RBdirect'}
REMAINDER_CAT="not-${PAT_CAT}"
CORPUS_PART=${1:-'PccTe'}

ALL_PRECLEAN_IDS="${TABLES_DIR}/RBXadj/cleaned/clean_${CORPUS_PART}_rb-bigram_index.txt"
BASELINE_NAME="$(basename ${ALL_PRECLEAN_IDS})"
PAT_IDS_TO_REMOVE="${TABLES_DIR}/${PAT_CAT}/${CORPUS_PART}_trigger_bigram-index_clean.35f.txt"
REMAINDER_PATH="${TABLES_DIR}/${REMAINDER_CAT}/${BASELINE_NAME/rb-bigram/${REMAINDER_CAT}}"
mkdir -p $(dirname ${REMAINDER_PATH})
echo -e "\n## Collecting \`${CORPUS_PART}\` IDs *only* in the (newly) cleaned \`RBXadj\` index\n\
   i.e. The (newly) cleaned 'RBXadj' IDs **not** in the '${PAT_CAT}' hits\n"
echo -e "🫧\tCleaned ID set:\t\t${ALL_PRECLEAN_IDS}"
echo -e "🗑️\tIDs to REMOVE:\t\t${PAT_IDS_TO_REMOVE}"
echo -e "💾\tSave new ID set as:\t${REMAINDER_PATH}\n"

(
  echo -e "CLEAN\t${PAT_CAT}.\tshared"
  comm -123 --total --check-order <(sort "${ALL_PRECLEAN_IDS}") <(sort "${PAT_IDS_TO_REMOVE}") | cut -f-3
) | tabulate --format fancy_grid -1
echo

if [[ ! -s ${REMAINDER_PATH} ]]; then
  echo "$ comm -23 --check-order <(sort '${ALL_PRECLEAN_IDS}') <(sort '${PAT_IDS_TO_REMOVE}') > '${REMAINDER_PATH}'"
  comm -23 --check-order <(sort "${ALL_PRECLEAN_IDS}") <(sort "${PAT_IDS_TO_REMOVE}") >"${REMAINDER_PATH}"
else
  echo "> IDs previously collected. ✓ My work is done."
fi

SANPI_DATA=$(dirname ${TABLES_DIR})
echo -e "\n+ $(ls -ho ${REMAINDER_PATH} | tabulate -f 'tsv' | cut -f4- | tabulate -f 'plain')"
WCL="$(wc -l ${REMAINDER_PATH})"
declare -i WCL
echo -e "+ ${WCL%% *} total *cleaned* '${CORPUS_PART}' hits (ids) NOT in ${PAT_CAT} hits."
