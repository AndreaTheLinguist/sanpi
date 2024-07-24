#!/bin/bash
echo -e "Concatenating Frequency TSVs\n> running '${0}'"
SANPI_DATA="/share/compling/data/sanpi"
DATA_DIR=''
while getopts ":d:sC:N:p:" opt; do
	case $opt in
	d) DATA_DIR="${OPTARG}" ;; # Set data dir
	s) TAG_C="NEQ" ;;          # Set data tag to "NEQ" (sample)
	C) TSV_C="${OPTARG}" ;;    # Store the comparison counts path
	N) TSV_N="${OPTARG}" ;;    # Store the neg/target counts path
	p) PAT_KEY="${OPTARG}" ;;  # Store the pattern key--subdirectory for env tsvs and shared element of path to `ucs_format/`
	\?)
		echo "Invalid option -$OPTARG" >&2
		exit 1
		;;
	esac
done

PAT_KEY=${PAT_KEY:-'RBdirect'}
TAG_C=${TAG_C:-'ALL'}

if [[ ${DATA_DIR} == 'DEMO' ]]; then
	DATA_DIR="${SANPI_DATA}/DEMO"
else
	DATA_DIR="${DATA_DIR:-$SANPI_DATA}"
fi
echo "Data --> '${DATA_DIR}'"

TSV_DIR="${DATA_DIR}/5_freq_tsv"
echo "Top Frequency TSV dir: '${TSV_DIR}'"
ENV_TSVS="${TSV_DIR}/${PAT_KEY}"
mkdir -p "${ENV_TSVS}"
echo "Pattern specific dir: '${ENV_TSVS}'"

for T in $(find ${DATA_DIR}/2_hit_tables/*${PAT_KEY}/ucs_format -name '*ALL*tsv'); do
	ln -srv -t "${ENV_TSVS}" "${T}" 2>/dev/null
done


# > link most recent NEQ sample;
EXISTING_SYML=$(find ${ENV_TSVS} -type l -name '*NEQ*tsv')
if [[ -f ${EXISTING_SYML} ]]; then
	NEQ_PATHS=$(find -L ${SANPI_DATA}/2_hit_tables/*${PAT_KEY}/ucs_format -newer ${EXISTING_SYML} -name '*NEQ*.tsv')
else
	NEQ_PATHS=$(find -L ${SANPI_DATA}/2_hit_tables/*${PAT_KEY}/ucs_format -name '*NEQ*.tsv')
fi

if [[ -n "${NEQ_PATHS}" ]]; then
	unset -v LATEST
	for FILE in ${NEQ_PATHS}; do
		[[ ${FILE} -nt ${LATEST} ]] && LATEST=${FILE}
	done

	# #! must include `--force` or `-b` or `--backup=t/numbered` to replace previous link
	ln -srv --backup=numbered \
		${LATEST} \
		"${ENV_TSVS}/$(basename ${LATEST/.[0-9]*[0-9]./.})"
	#^ removing timestamp
	#^ 		for direct ~ "AdvAdj_NEQ_not-RBdirect_final-freq.tsv"
	#^ 		for mirror ~ "AdvAdj_NEQ_POSmirror_final-freq.tsv"
else
	echo -e "Most Recent NEQ sample already linked.\n✓ No update required." | tabulate -sep,
fi 

#> #HACK rename env tsvs: "-final-freq" --> "_final-freq"
for X in ${ENV_TSVS}/*-final-freq*tsv; do
	mv -v "${X}" "${X/-final-freq/_final-freq}"
done

tree -lhD --prune -I *~* "${TSV_DIR}"

if [[ $(ls ${ENV_TSVS}/*tsv) ]]; then
	echo ''
	(
		echo 'frequency *.tsv, *source* last modified'
		for f in ${ENV_TSVS}/*tsv; do echo "$(basename ${f}),$(date -r ${f})"; done
	) | tabulate -f fancy_grid -s',' -1
fi

TSV_C=${TSV_C:-"${ENV_TSVS}/AdvAdj_${TAG_C}_not-${PAT_KEY}_final-freq.tsv"}
TSV_N=${TSV_N:-"${ENV_TSVS}/AdvAdj_ALL_${PAT_KEY}_final-freq.tsv"}

if [[ "${PAT_KEY}" == "mirror" ]]; then
	TSV_C="${ENV_TSVS}/AdvAdj_${TAG_C}_POS${PAT_KEY}_final-freq.tsv"
	echo $TSV_C 
	TSV_N="${ENV_TSVS}/AdvAdj_ALL_NEG${PAT_KEY}_final-freq.tsv"
	echo $TSV_N

fi
echo "Input Paths:"
echo "1. Complement:"
STEM_C="$(basename -s '.tsv' ${TSV_C})"
echo "   $(tree -hDlf -P *${STEM_C}* -I *~* --prune --noreport ${ENV_TSVS} | tail -1)"
echo "   $(wc -l ${TSV_C} | tabulate -f tsv | cut -f1) total unique attested"

echo "2. Negated:"
STEM_N="$(basename -s '.tsv' ${TSV_N})"
echo "   $(tree -hDlf -P *${STEM_N}* -I *~* --prune --noreport ${ENV_TSVS} | tail -1)"
echo "   $(wc -l ${TSV_N} | tabulate -f tsv | cut -f1) total unique attested"
# echo " $(ls -ho ${TSV_N})"

#>>>>>>>>>>>>>>>> ARG 1 >>>>>>>>>>>>>>>>>>>>>>>>

echo -e "\n## COM ##"

echo "  filestem:          '${STEM_C}'"

CROSS_C=${STEM_C%%_*}
echo "  compared features: '${CROSS_C}'"

INFO_C=${STEM_C%?final*}
PREFIX_C=${INFO_C%_*}
TAG_C=${TAG_C:-"${PREFIX_C/*_/}"}
echo "  sample tag:        '${TAG_C}'"

ENV_C=$(basename -s "_final-freq" "${STEM_C/*${TAG_C}_/}")
echo "  environment:       '${ENV_C}'"
#>>>>>>>>>>>>>>>> ARG 2 >>>>>>>>>>>>>>>>>>>>>>>>

echo -e "\n## NEG ##"
echo "  filestem:          '${STEM_N}'"

CROSS_N=${STEM_N%%_*}
echo "  compared features: '${CROSS_N}'"

INFO_N="${STEM_N%?final-freq*}"
PREFIX_N="${INFO_N%_*}"
TAG_N=${PREFIX_N/*_/}
echo "  sample tag:        '${TAG_N}'"

ENV_N=$(basename -s "_final-freq" "${STEM_N/*${TAG_N}_/}")
echo "  environment:       '${ENV_N}'"

# >>>>>>>>> set output >>>>>>>>>>>>>>>
ENV_SUFF=${ENV_N//[A-Z]/}
ANY_TSVS="${TSV_DIR}/ANY${ENV_SUFF,,}"
# echo "${ANY_TSVS}"
mkdir -p "${ANY_TSVS}"
OUT_TSV="${ANY_TSVS}/${PREFIX_C}_any-${ENV_SUFF}_final-freq.tsv"
echo -e "\n------------------------\n"
echo "Combined Output: ${OUT_TSV}"

echo "cat '${TSV_C}' > '${OUT_TSV}'"
cat "${TSV_C}" >"${OUT_TSV}"

echo "cat '${TSV_N}' >> '${OUT_TSV}'"
cat "${TSV_N}" >>"${OUT_TSV}"
echo
echo "$(wc -l ${OUT_TSV} | tabulate -f tsv | cut -f1) lines in combined tsv"
tree -hDl --du --prune -I *~* ${TSV_DIR}

echo "Finished concatenating tsv files"
date
# exit #// ! HACK TEMP <---- REMOVE
