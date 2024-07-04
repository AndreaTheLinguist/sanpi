#!/bin/bash
TABLE_PATH=${1:-/share/compling/data/sanpi/debug/2_hit_tables/NEGmirror/debug_neg-mirror-R_hits.csv}
TABLE_DIR="$(dirname ${TABLE_PATH})"
echo "Input CSV: ${TABLE_PATH}"
INDEX_TXT_PATH=${TABLE_PATH/.csv/index.txt}
INDEX_TXT_PATH=${INDEX_TXT_PATH/hits/}
echo "Saving index as: ${INDEX_TXT_PATH}"

time cut -f1 -d, ${TABLE_PATH} | tail -n+2 > ${INDEX_TXT_PATH} \
&& echo "$(basename ${TABLE_PATH/.csv/}) index successfully retrieved."
ls -ho ${INDEX_TXT_PATH}
WCL="$(wc -l ${INDEX_TXT_PATH})"
echo "${WCL%% *} total ids in sanpi${TABLE_DIR##*sanpi}\
/$(basename -s _hits.csv ${TABLE_PATH}) dataset"
echo '...............................................................................................'
echo 

exit