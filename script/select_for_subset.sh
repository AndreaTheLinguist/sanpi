#!/bin/bash

#* INPUTS
TAG=${1:-"bigram"}
CONLL_DIR=${2:-"/share/compling/data/sanpi/corpora_shortcuts/testing/smallest20.conll"}
echo "Running ../sanpi/playground/select_for_subset.sh"
date
echo "*******************************"
#* built variables
SUBSET_DIR=${CONLL_DIR}/subset_${TAG}
if [[ ! -d $SUBSET_DIR ]]; then
    mkdir $SUBSET_DIR
fi

#// MISSING_STEM=missing_subset_${TAG}
#// COMPLETE_STEM=in_subset_${TAG}
MISSING_STEM=${SUBSET_DIR}/subset-${TAG}_missing
COMPLETE_STEM=${SUBSET_DIR}/subset-${TAG}_complete

# * look for subset files
for F in ${CONLL_DIR}/*conllu; do 
  
  if [[ $(du ${SUBSET_DIR}/*`basename ${F}`)  ]]; then
    echo "$(basename $F) $TAG subset already completed."

  else
    #> run subset job on $F
    F_NAME="$(basename $F)"
    STEM=${F_NAME%.conllu}
    echo -e "***************\nsbatch -J ${STEM/_eng_/}-$TAG -t01:00:00 /share/compling/projects/sanpi/grewpy_subset.slurm.sh $TAG $F"
    date +%F@%R
    sbatch -J ${STEM/_eng_/}-$TAG -t01:00:00 /share/compling/projects/sanpi/grewpy_subset.slurm.sh $TAG $F
    echo "***************"
  fi

done
sleep 5m

RECENT_MISSING="${MISSING_STEM}.$(date +%F_%H%M).txt"
RECENT_COMPLETE="${COMPLETE_STEM}.$(date +%F_%H%M).txt"
for F in ${CONLL_DIR}/*conllu; do 
  du -h --time ${CONLL_DIR}/subset_${TAG}/*$(basename ${F})\
    && basename $F >> $RECENT_COMPLETE\
    || basename $F >> $RECENT_MISSING
done

if [[ -x $(cat $RECENT_MISSING) ]]; then
  echo "Subsets complete!" 
  exit 
fi

echo "...jobs running..."
sleep 10m

RECENT_MISSING="${MISSING_STEM}.$(date +%F_%H%M).txt"
RECENT_COMPLETE="${COMPLETE_STEM}.$(date +%F_%H%M).txt"
for F in ${CONLL_DIR}/*conllu; do 
  du -h --time ${CONLL_DIR}/subset_${TAG}/*$(basename ${F})\
    && basename $F >> $RECENT_COMPLETE\
    || basename $F >> $RECENT_MISSING
done

if [[ -x $(cat $RECENT_MISSING) ]]; then
  echo "Subsets complete!" 
  exit 0
fi

echo "...jobs running..."
sleep 15m

RECENT_MISSING="${MISSING_STEM}.$(date +%F_%H%M).txt"
RECENT_COMPLETE="${COMPLETE_STEM}.$(date +%F_%H%M).txt"
for F in ${CONLL_DIR}/*conllu; do 
  du -h --time ${CONLL_DIR}/subset_${TAG}/*$(basename ${F})\
    && basename $F >> $RECENT_COMPLETE\
    || basename $F >> $RECENT_MISSING
done

if [[ -x $(cat $RECENT_MISSING) ]]; then
  echo "Subsets complete!" 
  exit 0
fi

echo "...jobs running..."
sleep 15m

RECENT_MISSING="${MISSING_STEM}.$(date +%F_%H%M).txt"
RECENT_COMPLETE="${COMPLETE_STEM}.$(date +%F_%H%M).txt"
for F in ${CONLL_DIR}/*conllu; do 
  du -h --time ${CONLL_DIR}/subset_${TAG}/*$(basename ${F})\
    && basename $F >> $RECENT_COMPLETE\
    || basename $F >> $RECENT_MISSING
done

if [[ -x $(cat $RECENT_MISSING) ]]; then
  echo "Subsets complete!" 
  exit 0
fi

echo "...jobs running..."
sleep 15m

RECENT_MISSING="${MISSING_STEM}.$(date +%F_%H%M).txt"
RECENT_COMPLETE="${COMPLETE_STEM}.$(date +%F_%H%M).txt"
for F in ${CONLL_DIR}/*conllu; do 
  du -h --time ${CONLL_DIR}/subset_${TAG}/*$(basename ${F})\
    && basename $F >> $RECENT_COMPLETE\
    || basename $F >> $RECENT_MISSING
done

if [[ -x $(cat $RECENT_MISSING) ]]; then
  echo "Subsets complete!" 
  exit 0
fi

echo "Time allotment is up! The following files are still missing subsets:"
cat $RECENT_MISSING

exit