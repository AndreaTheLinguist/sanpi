#!/bin/bash

TABLES_DIR='/share/compling/data/sanpi/2_hit_tables'
PAT_CAT=${2:-'RBdirect'}
UPDATED_DIR="${TABLES_DIR}/${PAT_CAT}/cleaned"
mkdir -p ${UPDATED_DIR}
CORPUS_PART=${1:-'PccTe'}
ALL_PRECLEAN_IDS="${TABLES_DIR}/RBXadj/cleaned/clean_${CORPUS_PART}_rb-bigram_index.txt"
EXISTING_PAT_IDS="${TABLES_DIR}/${PAT_CAT}/${CORPUS_PART}_trigger_bigram-index_clean.35f.txt"
BASELINE_NAME="$(basename ${ALL_PRECLEAN_IDS})"
UPDATED_PATH="${UPDATED_DIR}/${BASELINE_NAME/rb-bigram/${PAT_CAT}}"
echo $UPDATED_PATH

echo -e "\n## Collecting '${CORPUS_PART}' IDs in pre-cleaned baseline AND '${PAT_CAT}'\n\
--> The (newly) cleaned ${PAT_CAT} hits:\n"
echo -e "🫧\tCleaned ID set:\t\t${ALL_PRECLEAN_IDS}"
echo -e "📇\tExisting ID set:\t${EXISTING_PAT_IDS}"
echo -e "💾\tSave new ID set as:\t${UPDATED_PATH}\n"

# SORT_CLEAN="${ALL_PRECLEAN_IDS/.txt/.sort.txt}"
# sort "${ALL_PRECLEAN_IDS}" > "${SORT_CLEAN}"
SORT_PAT="${EXISTING_PAT_IDS/.txt/.sort.txt}"
sort "${EXISTING_PAT_IDS}" >"${SORT_PAT}"

(
  echo -e "clean\t${PAT_CAT}.\tSHARED"
  comm -123 --total --check-order <(sort "${ALL_PRECLEAN_IDS}") "${SORT_PAT}" | cut -f-3
) | tabulate --format fancy_grid -1
echo
if [[ ! -s ${UPDATED_PATH} ]]; then
  echo "\$ comm -12 --check-order <(sort '${ALL_PRECLEAN_IDS}') '${SORT_PAT}' > '${UPDATED_PATH}'"
  comm -12 --check-order <(sort "${ALL_PRECLEAN_IDS}") "${SORT_PAT}" >"${UPDATED_PATH}"
else
  echo "> IDs previously collected. ✓ My work is done."
fi

SANPI_DATA=$(dirname ${TABLES_DIR})
echo "+ $(ls -ho ${UPDATED_PATH} | tabulate -f 'tsv' | cut -f4- | tabulate -f 'plain')"
WCL="$(wc -l ${UPDATED_PATH})"
declare -i WCL
echo -e "+ ${WCL%% *} total *cleaned* '${PAT_CAT}' hits in '${CORPUS_PART}'."

echo "Finished @ $(date)"
exit
