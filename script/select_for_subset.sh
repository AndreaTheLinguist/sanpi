#!/usr/bin/bash

# set -o errexit
set -o pipefail
set -o nounset

#* define functions
function showDate() {
  date "+%a %-m/%-d/%y @ %-I:%M%#p"
}

function probeFileMatch() {
  TARGET=$1
  TARGET_DIR=$2
  du -h --time $TARGET_DIR/*$(basename $TARGET)
}

function submitJob() {
  F=$1
  TAG=$2
  SLURM_FLAGS=$3
  echo "+ $(basename $F)"

  #! wait if there are quite a few jobs already
  if [[ $(squeue | egrep -c "arh234") -gt 20 ]]; then

    for i in $(seq 5); do
      if [[ $(squeue | egrep -c "arh234") -gt 30 ]]; then
        if [[ $(squeue | egrep -c "arh234") -gt 50 ]]; then
          echo "  $(squeue | egrep -c arh234) jobs running currently. Waiting..."
          sleep 10m
        fi

        if [[ $(squeue | egrep -c "arh234") -gt 70 ]]; then
          echo "  $(squeue | egrep -c arh234) jobs running currently. Waiting..."
          sleep 10m
        fi

        if [[ $(squeue | egrep -c "arh234") -gt 50 ]]; then
          echo "  $(squeue | egrep -c arh234) jobs running currently. Waiting..."
          sleep 5m
        fi

        if [[ $(squeue | egrep -c "arh234") -gt 40 ]]; then
          echo "  $(squeue | egrep -c arh234) jobs running currently. Waiting..."
          sleep 2m
        fi
      fi
    done
  fi

  #* run subset job on $F
  F_NAME="$(basename $F)"
  STEM=${F_NAME%.conllu}
  J_NAME="-J ${STEM/_eng_/}-${TAG}"
  # echo '-------------------'
  echo -e "sbatch $J_NAME $SLURM_FLAGS /share/compling/projects/sanpi/grewpy_subset.slurm.sh $TAG $F"
  showDate
  sbatch $J_NAME $SLURM_FLAGS /share/compling/projects/sanpi/grewpy_subset.slurm.sh $TAG $F
  sleep 30

}

function ifQueueEmptyExit() {
  if [[ "$(squeue | egrep -c "arh234")" == "0" ]]; then
    echo -e "\n⋄ No jobs running. Quitting script."
    echo "⟪ script closed: $(showDate) ⟫"
    exit
  else
    echo -e "\n» $(showDate) «"
    echo "... $(squeue | egrep -c arh234) jobs running ..."
  fi
}

function inspectSubset() {
  SUBSET_DIR=$1
  TAG=${SUBSET_DIR##*subset_}
  CONLL_DIR=$(dirname $SUBSET_DIR)
  INFO_DIR=${SUBSET_DIR}/info
  #// MISSING_STEM=${INFO_DIR}/subset-${TAG}_missing
  #// COMPLETE_STEM=${INFO_DIR}/subset-${TAG}_complete
  RECENT_MISSING=${INFO_DIR}/subset-${TAG}_missing.$(date +%F_%H%M).txt
  RECENT_COMPLETE=${INFO_DIR}/subset-${TAG}_complete.$(date +%F_%H%M).txt

  #> if file path has already been written to, clear it.
  if [[ -f $RECENT_MISSING ]]; then
    rm $RECENT_MISSING
  fi
  if [[ -f $RECENT_COMPLETE ]]; then
    rm $RECENT_COMPLETE
  fi
  #> look for file correspondence
  for FILE in ${CONLL_DIR}/*conllu; do
    F_NAME="$(basename $FILE)"
    STEM=${F_NAME%.conllu}
    if [[ $(probeFileMatch $FILE $SUBSET_DIR) ]]; then
      echo " ✓ ${STEM}: $(probeFileMatch $FILE $SUBSET_DIR | cut -d '/' -f1)"
      echo $FILE >>$RECENT_COMPLETE
    else
      echo " ✕ ${STEM} not found"
      echo $FILE >>$RECENT_MISSING
    fi
  done

  #> check updated file lists
  if [[ ! -f $RECENT_MISSING ]]; then
    CONFIRM="✓ All conllu files accounted for in subset."
    echo "Corpus Dir: $(dirname $CONLL_DIR)/" >>$RECENT_MISSING
    echo "Slice: ../$(basename $CONLL_DIR)/" >>$RECENT_MISSING
    echo "Subset: ../$(basename $SUBSET_DIR)/" >>$RECENT_MISSING
    echo ' ⌁ ⌁ ⌁ ⌁ ⌁ ⌁ ⌁'
    echo $CONFIRM >>$RECENT_MISSING
    showDate >>$RECENT_MISSING
    echo "+ + full ../$(basename $CONLL_DIR)/ subset complete! + +"
    showDate

  fi
}

function checkCorpusStatus() {
  CORPUS_DIR=$1
  TAG=$2

  ifQueueEmptyExit

  CONFIRM="All conllu files accounted for in subset"

  for CONLL_DIR in ${CORPUS_DIR}/*conll; do
    SUBSET_DIR=${CONLL_DIR}/subset_${TAG}
    INFO_DIR=${SUBSET_DIR}/info

    MISSING_STEM=${INFO_DIR}/subset-${TAG}_missing
    COMPLETE_STEM=${INFO_DIR}/subset-${TAG}_complete

    MISSING_INDEX_GLOB="${MISSING_STEM}*"

    echo -e "\nChecking ../$(basename $CONLL_DIR)/$(basename $SUBSET_DIR)/ for previous processing..."
    #> check this subset's previous file index records
    # Note: This could fail either because no files match the glob,
    #       or because no lines match the grep. No need to distinguish.
    if [[ $(egrep accounted $MISSING_INDEX_GLOB) ]]; then
      echo " ✓ $(basename $(dirname $SUBSET_DIR)) processing previously completed."
      echo "   ⨧ To REPROCESS, move or rename directories or specific files."
    else
      inspectSubset $SUBSET_DIR
    fi

  done

}

#* INPUTS
CORPUS_DIR=${1:-'/share/compling/projects/sanpi/demo/data/corpora/testing'}
TAG=${2:-'bigram'}
SLURM_ARG=${3:-'--mem=15G --t1:00:00'}
LOG_DIR="/share/compling/projects/sanpi/logs/grewpy_subsets/`basename $CORPUS_DIR`"
mkdir -p $LOG_DIR
SLURM_FLAGS="$SLURM_ARG --chdir=$LOG_DIR"

echo "Starting $0"
date
echo '*******************************'
echo -e "Processing Corpus: ${CORPUS_DIR}/..."
echo "  + additional slurm options: $SLURM_FLAGS"

#* SELECT FILES AND SUBMIT JOBS
for CONLL_DIR in ${CORPUS_DIR}/*conll; do

  CONLL_HEADER=">> ../$(basename $CORPUS_DIR)/$(basename $CONLL_DIR)/"
  LINE="$(echo $CONLL_HEADER | tr -d '\n' | tr -c '[:alnum:]' '=' | tr '[:alnum:]' '=')"
  echo -e "\n$LINE\n$CONLL_HEADER\n$LINE"
  SUBSET_DIR=${CONLL_DIR}/subset_${TAG}
  INFO_DIR=${SUBSET_DIR}/info
  MISSING_INDEX_GLOB="${INFO_DIR}/subset-${TAG}_missing*"
  #> if there is no subset dir or it is empty, run everything.
  if [[ ! -d $SUBSET_DIR || ! $(ls $SUBSET_DIR/*) || ! "$(ls $SUBSET_DIR | egrep "conllu")" ]]; then
    echo "⊘  No evidence of prior processing found. All files will be submitted ⇫"
    if [[ ! "$(ls $SUBSET_DIR | egrep "conllu")" ]]; then
      echo "(subset directory exists and is not empty, but does not contain any '.conllu' files)"
    fi

    for FILE in ${CONLL_DIR}/*conllu; do
      echo '-------------------'
      submitJob $FILE $TAG $SLURM_FLAGS
    done

  #> check for any "missing" records indicating completion
  elif [[ $(egrep accounted $MISSING_INDEX_GLOB) ]]; then
    echo " ✓ $(basename $(dirname $SUBSET_DIR)) processing previously completed."
    echo "   ⨧ To REPROCESS, move or rename directories or specific files."

  #> if no info dir (unlikely) or no indication of completion in info files,
  #> check all parent .conllu files for corresponding file in subset dir
  else

    # * look for subset files
    for FILE in ${CONLL_DIR}/*conllu; do
      echo '-------------------'
      if [[ $(probeFileMatch $FILE $SUBSET_DIR) ]]; then
        echo "✓ $(basename $FILE) $TAG subset already completed."

      else
        submitJob $FILE $TAG $SLURM_FLAGS
      fi

    done

  fi
  sleep 3

done
echo '-------------------'

#* WAIT WHILE JOBS RUN.
#*---------------------

ifQueueEmptyExit
sleep 2m

checkCorpusStatus $CORPUS_DIR $TAG
sleep 7m
# at least 10 min in

checkCorpusStatus $CORPUS_DIR $TAG
sleep 10m
#at least 20 min in

checkCorpusStatus $CORPUS_DIR $TAG
sleep 10m
#at least 30 min in

checkCorpusStatus $CORPUS_DIR $TAG
sleep 10m
#at least 40 min in

checkCorpusStatus $CORPUS_DIR $TAG
sleep 10m
#at least 50 min in

checkCorpusStatus $CORPUS_DIR $TAG
sleep 10m
#at least 60 min in

echo
showDate
echo "Script has run for at least 1 hr; the following files are still missing subsets:"
checkCorpusStatus $CORPUS_DIR $TAG

echo
showDate
echo "Script Closed."
exit
