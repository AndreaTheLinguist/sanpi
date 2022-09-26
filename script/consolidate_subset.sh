#!/bin/bash
# ${0}

eval "$(conda shell.bash hook)"
conda activate parallel-sanpi

TAG=${1:-entirely}
if [[ -z ${TAG} ]]; then
    echo -e "[!!] ERROR: No tag string given!\n > Tag string needed to:\n   (a) identify subset files\n   (b) label new output grouping subdirectory linking to specified subset files\n ** Tag string must be unique to the desired subset. **"
    echo "consolidation unsuccessful ( >_<)"
    exit 1
fi
echo "Creating grouping directory for: \"${TAG}\""

SUBDIR=/share/compling/data/puddin/${TAG}_subset
echo "Changing to grouping directory to create soft links: ${SUBDIR}"
if [[ ! -d ${SUBDIR} ]]; then
    mkdir ${SUBDIR}
fi

cd ${SUBDIR}
SUBSET_FILE_PAT=/share/compling/data/puddin/*.conll/*subset*/*${TAG}*.conllu
echo "Search Pattern: ${SUBSET_FILE_PAT}"
# save _output_ to variable
SUBSET_FILES=$(ls -S1 ${SUBSET_FILE_PAT})
NUM_FOUND=$(echo $SUBSET_FILES | wc -w)

echo "____________________ + ${NUM_FOUND} matching subset files found + ________________________"
ls -1 $SUBSET_FILES | head -5
echo ...
ls -1 $SUBSET_FILES | tail -4

# parallel echo {/} \; echo "ln -s {} ./" ::: $SUBSET_FILES | tail -5

if [[ "$(ls | wc -l)" != ${NUM_FOUND} ]]; then
    echo -e "[!] WARNING:\n    Not all subset files were successfully linked!"
    echo "consolidation unsuccessful ( >_<)"
    exit 1
fi
exit
