#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

#* check path for ucs install
if [[ ! $(ucsdoc ucs-print | head) ]]; then
    echo "ucs installation not found"
    exit 1
fi

echo "running $0" 
date "+%D %r"
TABLES_DIR=${1:-'/share/compling/projects/sanpi/results/ucs_tables'}

echo "transforming *ds.gz ucs tables found in ${TABLES_DIR}"

for TABLE in ${TABLES_DIR}/*ds.gz; do
    echo "time /share/compling/projects/sanpi/script/transform_ucs.sh $TABLE"
    time /share/compling/projects/sanpi/script/transform_ucs.sh $TABLE

done

# #! #XXX Not sure this is going to work exactly right--has not been tested
# ls ${TABLES_DIR}/*ds.gz | parallel "echo {} && time /share/compling/projects/sanpi/script/transform_ucs.sh {}"

exit
# REGEX="'%${MATCH_VAR}% =~ /^${WORD}$/'"
# SAVE_DIR="$(dirname ${TABLE})/filter_${MATCH_VAR}"
# SAVE_DIR=${SAVE_DIR/l1/adv}
# SAVE_DIR=${SAVE_DIR/l2/adj}
# mkdir -p ${SAVE_DIR}
# # echo ${SAVE_DIR}
# FNAME=$(basename ${TABLE})
# SAVE_AS=${SAVE_DIR}/${FNAME/x.ds/x_${WORD}.ds}

# # echo `ucs-select --count FROM ${TABLE} WHERE ${REGEX}`
# # ucs-select --count FROM ${TABLE} WHERE ${REGEX}
# # exec bash -c "ucs-select --count FROM ${TABLE}  WHERE ${REGEX}" 

# echo ${SAVE_AS}
# # echo "ucs-select FROM ${TABLE} WHERE ${REGEX} INTO ${SAVE_AS}"
# # exec bash -c "ucs-select FROM ${TABLE} WHERE ${REGEX} INTO ${SAVE_AS}"
