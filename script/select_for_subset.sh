#!/usr/bin/bash

set -o pipefail
set -o nounset

#* define functions
function showDate() {
  date "+%a %-m/%-d/%y @ %-I:%M%#p"
}


function submitJob() {
  F=$1
  TAG=$2
  SLURM_FLAGS=$3

  #! wait if there are quite a few jobs already
  if [[ $(squeue | egrep -c "arh234") -gt 33 ]]; then
    echo "... $(squeue | egrep -c arh234) jobs running @ $(date +%R)..."
    for i in $(seq 5); do
      if [[ $(squeue | egrep -c "arh234") -gt 35 ]]; then
        echo "$(squeue | egrep -c arh234) jobs running ↠ sleep 30"
        sleep 30
      elif [[ $(squeue | egrep -c "arh234") -gt 40 ]]; then
        echo "$(squeue | egrep -c arh234) jobs running ↠ sleep 1m"
        sleep 1m
      elif [[ $(squeue | egrep -c "arh234") -gt 50 ]]; then
        echo "$(squeue | egrep -c arh234) jobs running ↠ sleep 3m"
        sleep 3m
      elif [[ $(squeue | egrep -c "arh234") -gt 60 ]]; then
        echo "$(squeue | egrep -c arh234) jobs running ↠ sleep 5m"
        sleep 5m
      fi
    done
    echo "... $(squeue | egrep -c arh234) jobs running @ $(date +%R)..."
  else
    echo "... $(squeue | egrep -c arh234) jobs running @ $(date +%R)..."
  fi

  #* run subset job on $F
  F_NAME="$(basename $F)"
  echo "▶ $F_NAME"
  STEM=${F_NAME%.conllu}
  J_NAME="-J ${STEM/_eng_/}-${TAG}_$(date +%y%m%d-%H%M)"
  echo -e "sbatch $J_NAME $SLURM_FLAGS /share/compling/projects/sanpi/grewpy_subset.slurm.sh $TAG $F"
  showDate
  sbatch $J_NAME $SLURM_FLAGS /share/compling/projects/sanpi/grewpy_subset.slurm.sh $TAG $F

  echo "sleep 3"
  sleep 3

}

function ifQueueEmptyExit() {
  if [[ "$(squeue | egrep -c arh234)" == "0" ]]; then
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
  TAG=${2:-"${SUBSET_DIR##*subset_}"}
  CONLL_DIR=${SUBSET_DIR%/*}
  CONLL_NAME=$(basename ${CONLL_DIR})
  echo -e "\n## ..${CONLL_DIR#*compling}/"
  CORPUS_DIR=${CONLL_DIR%/*}
  TOP_INFO_DIR=${CONLL_DIR}/info
  mkdir -p $TOP_INFO_DIR
  SUB_INFO_DIR=${SUBSET_DIR}/info
  mkdir -p $SUB_INFO_DIR

  RECENT_MISSING=${SUB_INFO_DIR}/subset-${TAG}_missing.$(date +%F_%H%M).txt
  RECENT_COMPLETE=${SUB_INFO_DIR}/subset-${TAG}_complete.$(date +%F_%H%M).txt
  RECENT_INDEX=${SUB_INFO_DIR}/subset-${TAG}_path-index.$(date +%F_%H%M).csv
  echo "STEM, INPUT_CONLLU, INPUT_COUNTS, SUBSET_CONLLU, SUBSET_CONTEXT, SUBSET_COUNTS" >$RECENT_INDEX
  #> if file path has already been written to, clear it.
  if [[ -f $RECENT_MISSING ]]; then
    rm $RECENT_MISSING
  fi
  if [[ -f $RECENT_COMPLETE ]]; then
    rm $RECENT_COMPLETE
  fi

  #> look for file correspondences
  for IN_CONLLU in ${CONLL_DIR}/*conllu; do
    NAME="${IN_CONLLU##*/}"
    STEM=${NAME%.conllu}
    IN_COUNTS=''
    SUB_COUNTS=''
    SUB_CONLLU=''
    SUB_COUNTS=''
    SUB_CONTEXT=''
    #> check for partial processing:
    #>> subset .conllu
    if [[ $(find $SUBSET_DIR -name "*${NAME}") ]]; then
      SUB_CONLLU=$(find $SUBSET_DIR -name "*${NAME}")
    fi

    #>> subset context.psv
    if [[ $(find $SUBSET_DIR -name "*${STEM}.context*") ]]; then
      SUB_CONTEXT=$(find $SUBSET_DIR -name "*${STEM}.context*")
    fi

    #>> subset counts.json
    if [[ $(find $SUB_INFO_DIR -name "*${STEM}.counts*") ]]; then
      SUB_COUNTS=$(find $SUB_INFO_DIR -name "*${STEM}.counts*")
    fi

    #>> input counts
    if [[ $(find $TOP_INFO_DIR -name "${STEM}.counts*") ]]; then
      IN_COUNTS=$(find $TOP_INFO_DIR -name "${STEM}.counts*")
    fi

    #> look for subset counts (least likely to exist)
    if [[ -n $IN_COUNTS && -n $SUB_COUNTS && -n $SUB_CONLLU && -n $SUB_CONTEXT ]]; then

      #* append input conllu name to "complete" index
      echo " ✓ ${STEM} found"
      echo $IN_CONLLU >>$RECENT_COMPLETE

    #> if not there, mark as missing and queue IN_CONLLU for job submission
    else
      echo " ✕ ${STEM} missing"
      echo $IN_CONLLU >>$RECENT_MISSING
    fi

    echo "$STEM, $IN_CONLLU, $IN_COUNTS, $SUB_CONLLU, $SUB_CONTEXT, $SUB_COUNTS" >>$RECENT_INDEX
    # echo -e "$STEM\n  - $IN_CONLLU\n  - $IN_COUNTS\n  - $SUB_CONLLU\n  - $SUB_CONTEXT\n  - $SUB_COUNTS"

  done
  #> check updated file lists
  if [[ ! -f $RECENT_MISSING ]]; then
    CONFIRM="✓ All original files accounted for in subset."
    echo "Corpus Dir: ${CORPUS_DIR}/" >>$RECENT_MISSING
    echo "Slice: ../${CONLL_NAME}/" >>$RECENT_MISSING
    echo "Subset: ../$(basename $SUBSET_DIR)/" >>$RECENT_MISSING
    echo '⌁  ⌁  ⌁  ⌁  ⌁  ⌁  ⌁'
    echo $CONFIRM >>$RECENT_MISSING
    showDate >>$RECENT_MISSING
    echo "+ + full ../$(basename $(dirname $CONLL_DIR))/${CONLL_NAME}/ subset complete! + +"
    showDate
  fi

  echo '-------------------------'
  echo "TOTALS"
  echo "    finished:  $(egrep -c conllu $RECENT_COMPLETE)"
  echo "  unfinished:  $(egrep -c conllu $RECENT_MISSING)"
  echo "    (partial:  $(egrep -c 'counts.*, ?$' $RECENT_INDEX))"
  echo
  du -ch --time ${SUBSET_DIR}/*conllu | column -t -n
  echo -e "\n↦ full subset processing paths index saved as:\n   $RECENT_INDEX"
  echo '*************************'
}

function checkCorpusStatus() {
  CORPUS_DIR=$1
  TAG=$2

  echo -e "\nChecking ..${CORPUS_DIR#*compling}/ processing..."
  for CONLL_DIR in ${CORPUS_DIR}/*conll; do
    SUBSET_DIR=${CONLL_DIR}/subset_${TAG}
    INFO_DIR=${SUBSET_DIR}/info

    MISSING_STEM=${INFO_DIR}/subset-${TAG}_missing
    COMPLETE_STEM=${INFO_DIR}/subset-${TAG}_complete

    MISSING_INDEX_GLOB="${MISSING_STEM}*"

    #> check this subset's previous file index records
    # Note: This could fail either because no files match the glob,
    #       or because no lines match the grep. No need to distinguish.
    if [[ $(egrep accounted $MISSING_INDEX_GLOB) ]]; then
      echo "⁂ $(basename $(dirname $SUBSET_DIR)) processing previously completed."
      echo "   ⨧ To REPROCESS, move or rename directories or specific files."

    else
      inspectSubset $SUBSET_DIR

    fi
  done
}

echo "Running $0"
date
echo '*******************************'

#* INPUTS
CORPUS_DIR=${1:-'/share/compling/data/sanpi/corpora_shortcuts/debug'}
LOG_DIR="/share/compling/projects/sanpi/logs/grewpy_subsets/$(basename $CORPUS_DIR)"
TAG=${2:-'bigram'}
CHECK=${3:-''}
SLURM_ARG=${3:-'--requeue --nice --mem=20G -t1:00:00'}
SLURM_FLAGS="$SLURM_ARG --chdir=$LOG_DIR"
echo -e "Processing Corpus: ${CORPUS_DIR}/..."
echo "+ additional slurm options:"
echo "  $SLURM_FLAGS"
mkdir -p $LOG_DIR

echo "Checking status of $TAG subset"
echo "  for ../${CORPUS_DIR}/ ..."
echo "($(squeue | egrep -c arh234) jobs currently running)"
checkCorpusStatus $CORPUS_DIR $TAG $CHECK

#> if explicit check only, exit
if [[ $CHECK == "--status_check" ]]; then
  echo "Status check complete. Closing script."
  showDate
  exit 0
fi

#* SELECT FILES AND SUBMIT JOBS
for CONLL_DIR in ${CORPUS_DIR}/*conll; do
  CONLL_NAME=$(basename $CONLL_DIR)
  CONLL_HEADER=">> ../$(basename $CORPUS_DIR)/${CONLL_NAME}/"
  LINE="$(echo $CONLL_HEADER | tr -d '\n' | tr -c '[:alnum:]' '=' | tr '[:alnum:]' '=')"
  echo -e "\n$LINE\n$CONLL_HEADER\n$LINE"
  SUBSET_DIR=${CONLL_DIR}/subset_${TAG}
  INFO_DIR=${SUBSET_DIR}/info
  MISSING_INDEX_GLOB="${INFO_DIR}/subset-${TAG}_missing*"

  IN_CONLLU_COUNT=$(ls ${CONLL_DIR} | egrep -c 'conllu')
  SUB_CONLLU_COUNT=$(ls ${SUBSET_DIR} | egrep -c 'conllu')
  echo "$IN_CONLLU_COUNT conllu files in ../$CONLL_NAME/"
  echo "$SUB_CONLLU_COUNT conllu files in ..${SUBSET_DIR#$CORPUS_DIR}/"

  #> check for existing "missing" records
  CURRENT_MISSING="$(ls -t1 ${MISSING_INDEX_GLOB} | head -1 || echo)"
  if [[ -f $CURRENT_MISSING ]]; then
    echo "Missing file record located:"
    echo " ..${CURRENT_MISSING#$CORPUS_DIR}"

  #! if `CONLL_DIR` has reached this point without a status check,
  #  some dirs in `CORPUS_DIR` have had status check performed,
  #  but this one has not for some reason (or the records were wiped)
  else
    #> inspect `CONLL_DIR` individually
    inspectSubset $SUBSET_DIR
    CURRENT_MISSING="$(ls -t1 ${MISSING_INDEX_GLOB})"
  fi

  #> if there is no subset dir or it is empty, run everything.
  if [[ ! -d $SUBSET_DIR || ! "$(ls $SUBSET_DIR | egrep "conllu")" ]]; then
    echo "⊘  No evidence of prior processing found. All files will be submitted ⇫"
    if [[ ! "$(ls $SUBSET_DIR | egrep "conllu")" ]]; then
      echo "  (subset directory exists and is not empty, but does not contain any '.conllu' files)"
    fi

    for FILE in ${CONLL_DIR}/*conllu; do
      echo '-------------------'
      submitJob $FILE $TAG "$SLURM_FLAGS"
    done

  #> if already marked as complete, move to next conll dir
  elif [[ $(egrep 'accounted' $CURRENT_MISSING) ]]; then

    #! make `CONLL_DIR` and `SUBSET_DIR` have same # of .conllu files
    if [[ $IN_CONLLU_COUNT == $SUB_CONLLU_COUNT ]]; then
      echo "✓ $CONLL_NAME processing previously completed."
      echo "  ⨧ To REPROCESS, move or rename directories or specific files."

    else
      echo "Error: $CONLL_NAME marked as complete, but '.conll' file counts don't match."
      echo "$IN_CONLLU_COUNT conllu files in ../$CONLL_NAME/"
      echo "$SUB_CONLLU_COUNT conllu files in ../${SUBSET_DIR#$CORPUS_DIR}/"
      exit 1

    fi

  #> some files exist, but processing is not complete
  else

    # * look for subset files
    for FILE in ${CONLL_DIR}/*conllu; do
      FNAME=$(basename $FILE)
      STEM=${FNAME%.conllu}
      echo '-------------------'
      if [[ $(egrep $STEM $CURRENT_MISSING) ]]; then
        echo "✕ $FNAME $TAG subset unfinished."
        submitJob $FILE $TAG "$SLURM_FLAGS"

      else
        echo "✓ $FNAME $TAG subset already created."
      fi
    done

  fi
  echo "sleep 5"
  sleep 5

done

echo -e "\n≣≣≣≣≣≣≣≣ ▶▶  Jobs submitted for all files in ..${CORPUS_DIR#*compling}/  ▶▶ ≣≣≣≣≣≣≣≣ \n"

#* WAIT WHILE JOBS RUN.
#*---------------------

echo "sleep 10"
sleep 10

checkCorpusStatus $CORPUS_DIR $TAG
ifQueueEmptyExit
sleep 15m
echo "sleep 1"
sleep 1

#at least 15 min
checkCorpusStatus $CORPUS_DIR $TAG
ifQueueEmptyExit
sleep 15m
echo "sleep 1"
sleep 1

#at least 30 min after last job submitted
echo
showDate
echo "30 minutes since last job submitted. Current Status:"
echo "($(squeue | egrep -c arh234) jobs still running)"
checkCorpusStatus $CORPUS_DIR $TAG

echo
showDate
echo "Script Closed."
exit 0
