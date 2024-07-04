#!/bin/bash

DATA_DIR='/share/compling/data/sanpi'
DEFAULT_INDEX="${DATA_DIR}/4_post-processed/RBXadj/bigram-index_clean.35f.txt"
DF_DIR_NAME=${1:-'RBXadj'}
INDEX_ARG=${2:-''}
INDEX_NAME=${2:-'bigram-index_clean.35f.txt'}

LOG_DIR="${DATA_DIR}/logs"
mkdir -p "${LOG_DIR}"
LOG_PATH="${LOG_DIR}/chunk-clean-ids_${DF_DIR_NAME}.`date +"%Y-%m-%d_%I%M%P"`.log"
echo -e "> log will be saved to: ${LOG_PATH}\n..."
exec 1>${LOG_PATH} 2>&1

echo "# Chunking ${DF_DIR_NAME} ``hit_id`` index *.txt by corpus part"

if [[ ${DF_DIR_NAME} != 'RBXadj' && -z ${INDEX_ARG} ]]; then
    INDEX_NAME="trigger_${INDEX_NAME}"
fi

INDEX_DIR="${DATA_DIR}/4_post-processed/${DF_DIR_NAME}"
INDEX_PATH="${INDEX_DIR}/${INDEX_NAME}"

if [[ ! -f ${INDEX_PATH} ]]; then
    echo "${INDEX_PATH} not found. Trying fallback 'trigger-index_clean.35f.txt'"
    INDEX_PATH="${INDEX_DIR}/trigger-index_clean.35f.txt"
fi

if [[ ! -f ${INDEX_PATH} ]]; then
    echo -e "Warning: index '${INDEX_PATH}' not found.\n+ Falling back to default: '${DEFAULT_INDEX}'"
    INDEX_PATH=${DEFAULT_INDEX}
fi

echo -e "\n+ Index file:"
INDEX_INFO=$(ls -ho "${INDEX_PATH}" | tabulate -f 'plain')
echo "  >${INDEX_INFO##*arh234}"

HIT_DF_DIR="${DATA_DIR}/2_hit_tables/${DF_DIR_NAME}"
SUFFIX='_hits.csv'
echo -e "\n## Sample of Target '*${SUFFIX}' Files"
echo -e '\n```log'
tree -h "${HIT_DF_DIR}" | egrep "${SUFFIX}" | head -5
echo '```'
echo

PARTS=$(basename -a -s "${SUFFIX}" $(ls "${HIT_DF_DIR}"/bigram*${SUFFIX}))
PAT_STEM="rb-bigram"
for PART in ${PARTS}; do
    PART_NAME="${PART/bigram-/}"

    PART_NAME="${PART_NAME%%_*}"
    OUT_PATH="${HIT_DF_DIR}/${PART_NAME}_${INDEX_NAME}"
    if [[ ! -f ${OUT_PATH} ]]; then
        echo -e "\n## Identifying *${PART_NAME}* ids\n"
        
        echo "+ csv filestem prefix: ${PART}"
        CORP="${PART_NAME::3}"
        SLICE="${PART_NAME:(3)}"
        KEY="${CORP,,}_eng_${SLICE,,}"
        echo "+ $(grep -c "${KEY}" "${INDEX_PATH}") total ids matching '${KEY}'"
        echo -e '\nSample:\n'
        echo '```shell'
        echo "$ grep -m 4 '${KEY}' '${INDEX_PATH}'"
        grep -m 4 "${KEY}" "${INDEX_PATH}"
        echo -e '```'

        echo -e "\n+ Saving ${PART_NAME} specific 'bigram_id' index as:\n  ${OUT_PATH}"
        
        grep "${KEY}" "${INDEX_PATH}" > "${OUT_PATH}"

    else
        echo "'${OUT_PATH}' already exists. Skipping."
    fi
done

echo "Finished at `date '+%h %-d, %Y @ %-I:%m%P'`"
exit