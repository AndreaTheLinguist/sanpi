#!/bin/bash
echo -e "Concatenating Frequency TSVs\n> running '${0}'"
SANPI_DATA="/share/compling/data/sanpi"
DATA_DIR=''
while getopts ":d:s:C:N:" opt; do
	case $opt in
	d) DATA_DIR="${OPTARG}" ;; # Set data dir
	s) TAG_C="${OPTARG}" ;;    # Store the tsv tag
	C) TSV_C="${OPTARG}" ;;    # Store the comparison counts path
	N) TSV_N="${OPTARG}" ;;    # Store the neg/target counts path
	\?)
		echo "Invalid option -$OPTARG" >&2
		exit 1
		;;
	esac
done

TAG_C=${TAG_C:-'ALL'}

if [[ ${DATA_DIR} == 'DEMO' ]]; then
	DATA_DIR="${SANPI_DATA}/DEMO"
else
	DATA_DIR="${DATA_DIR:-$SANPI_DATA}"
fi
echo "Data --> '${DATA_DIR}'"

TSV_DIR="${DATA_DIR}/5_freq_tsv"
echo "Frequency TSV dir: '${TSV_DIR}'"
mkdir -p "${TSV_DIR}"

for T in ${DATA_DIR}/2_hit_tables/*RBdirect/ucs_format/*freq.tsv; do
	# echo "ln -srvf -t '${TSV_DIR}' '${T}'"
	ln -srv -t "${TSV_DIR}" "${T}" 2>/dev/null
done

# > link most recent NEQ sample; 
#! must include `--force` to replace previous link
# echo -e "ln -srv --force  \\
#   '$(ls -t ${DATA_DIR}/2_hit_tables/not-RBdirect/ucs_format/*NEQ*.tsv | head -1)' \\
#   '${TSV_DIR}/AdvAdj_NEQ_not-RBdirect-final-freq.tsv'"
ln -srv --force \
	"$(ls -t ${DATA_DIR}/2_hit_tables/not-RBdirect/ucs_format/*NEQ*.tsv | head -1)" \
	"${TSV_DIR}/AdvAdj_NEQ_not-RBdirect-final-freq.tsv"
tree -lhD "${TSV_DIR}"

if [[ $(ls ${TSV_DIR}/*tsv) ]]; then
	echo ''
	(
		echo 'frequency *.tsv, *source* last modified'
		for f in ${TSV_DIR}/*tsv; do echo "$(basename ${f}),$(date -r ${f})"; done
	) | tabulate -f fancy_grid -s',' -1
fi

TSV_C=${TSV_C:-${TSV_DIR}/AdvAdj_${TAG_C}_not-RBdirect-final-freq.tsv}
TSV_N=${TSV_N:-"${TSV_DIR}/AdvAdj_ALL_RBdirect-final-freq.tsv"}

echo "Input Paths:"
echo "1. Complement:"
STEM_C=$(basename "${TSV_C%.tsv}")
echo "   $(tree -hDlf -P "${STEM_C}*" ${TSV_DIR} | tail -n+2 | head -1)"
echo "   $(wc -l ${TSV_C} | tabulate -f tsv | cut -f1) total unique attested"

echo "2. Negated:"
STEM_N=$(basename "${TSV_N%.tsv}")
echo "   $(tree -hDlf -P "${STEM_N}*" ${TSV_DIR} | tail -n+2 | head -1)"
echo "   $(wc -l ${TSV_N} | tabulate -f tsv | cut -f1) total unique attested"
# echo "     $(ls -ho ${TSV_N})"

#>>>>>>>>>>>>>>>> ARG 1 >>>>>>>>>>>>>>>>>>>>>>>>

echo -e "\n## COM ##"

echo "  filestem:          '${STEM_C}'"

CROSS_C=${STEM_C%%_*}
echo "  compared features: '${CROSS_C}'"

PREFIX_C=${STEM_C%_*}
TAG_C=${TAG_C:-"${PREFIX_C/*_/}"}
echo "  sample tag:        '${TAG_C}'"

ENV_C=$(basename -s "-final-freq" "${STEM_C/*${TAG_C}_/}")
echo "  environment:       '${ENV_C}'"

#>>>>>>>>>>>>>>>> ARG 2 >>>>>>>>>>>>>>>>>>>>>>>>

echo -e "\n## NEG ##"

echo "  filestem:          '${STEM_N}'"

CROSS_N=${STEM_N%%_*}
echo "  compared features: '${CROSS_N}'"

PREFIX_N=${STEM_N%_*}
TAG_N=${PREFIX_N/*_/}
echo "  sample tag:        '${TAG_N}'"

ENV_N=$(basename -s "-final-freq" "${STEM_N/*${TAG_N}_/}")
echo "  environment:       '${ENV_N}'"
# // echo "test completed.";  exit

# >>>>>>>>> set output >>>>>>>>>>>>>>>
OUT_TSV="${TSV_DIR}/${PREFIX_C}_any-${ENV_N//[A-Z]/}_final-freq.tsv"

echo -e "\n------------------------\n"
echo "Combined Output: ${OUT_TSV}"
echo "cat '${TSV_C}' > '${OUT_TSV}'"
cat "${TSV_C}" >"${OUT_TSV}"

echo "cat '${TSV_N}' >> '${OUT_TSV}'"
cat "${TSV_N}" >>"${OUT_TSV}"
tree -hDl ${TSV_DIR}
echo "$(wc -l ${OUT_TSV} | tabulate -f tsv | cut -f1) lines in combined tsv"

echo "Finished concatenating tsv files"
date
