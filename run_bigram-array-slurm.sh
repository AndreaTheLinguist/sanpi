#!/bin/bash

# shell script to submit array slurm jobs to run pipeline on full corpora directories. Calls 'sbatch /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh'.
#
#  1 of the following can be passed to specify pattern directories to run (directories in ./Pat/) If none is given, '--neg' will be used.
#
#      --all_pat
#          all main patterns:
#              'PATS=("contig" "scoped" "raised" "advadj")'
#
#      --neg
#          all main negated patterns:
#              'PATS=("contig" "scoped" "raised")'
#
#      --noncontig
#          main negated patterns excluding 'contig':
#              'PATS=("scoped" "raised")'
#
#      [directory name]
#          any (single) directory name in "./Pat/"

# example: bash /share/compling/projects/sanpi/run_bigram-array-slurm.sh multi contig --array=35-36
# EVERYTHING: bash /share/compling/projects/sanpi/run_bigram-array-slurm.sh multi --all_pat

CPUS=10
CPU_MEM=5G

echo "Running /share/compling/projects/sanpi/run_bigram-array-slurm.sh"
date
LOG_DIR=/share/compling/projects/sanpi/logs/bigram-pipeline_`date "+%y-%m-%d"`
mkdir -p $LOG_DIR
MODE=$1
PAT_FLAG=${2:-"--neg"}
echo "PAT_FLAG: $PAT_FLAG"
ARRAY=${3:-""}
echo "ARRAY: $ARRAY"

if [[ $(which grew && grew version) ]]; then
    date
    echo 'grew module found'
    if [[ $PAT_FLAG == '--all_pat' ]]; then
        PATS=("contig" "scoped" "raised" "advadj")

    elif [[ $PAT_FLAG == '--neg' ]]; then
        PATS=("contig" "scoped" "raised")

    elif [[ $PAT_FLAG == '--noncontig' ]]; then
        PATS=("scoped" "raised")

    elif [[ -d "/share/compling/projects/sanpi/Pat/$PAT_FLAG" ]]; then
        PATS=("$PAT_FLAG")

    else
        PATS=("contig")
        ARRAY=$PAT_FLAG
        echo "(update) ARRAY = $ARRAY"

    fi

    echo -e "\nPatterns to submit jobs for: ${PATS[@]}"
    for PAT in "${PATS[@]}"; do

        echo -e "\n# $PAT"
        JOB_NAME="-J bigram-${PAT}_$(date +%y-%m-%d_%H%M)"
        if [[ $MODE == 'multi' ]]; then
            # echo 'sbatch ${JOB_NAME} $ARRAY ./bigram-array.slurm.sh $PAT'
            echo "sbatch ${JOB_NAME} $ARRAY --cpus-per-task ${CPUS} --mem-per-cpu=${CPU_MEM} --chdir=$LOG_DIR bigram-array.slurm.sh $PAT"
            sbatch ${JOB_NAME} $ARRAY --cpus-per-task ${CPUS} --mem-per-cpu=${CPU_MEM} --chdir=$LOG_DIR /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh $PAT

        elif [[ $MODE == 'solo' ]]; then
            # echo 'sbatch ${JOB_NAME} $ARRAY ./bigram-array.slurm.sh $PAT'
            echo "sbatch ${JOB_NAME} $ARRAY -n 1 --mem=15G --chdir=$LOG_DIR bigram-array.slurm.sh $PAT"
            sbatch ${JOB_NAME} $ARRAY -n 1 --mem=15G --chdir=$LOG_DIR  /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh $PAT
        else
            echo -e  "No valid cpu mode given. First argument should be one of the following strings:\n+ 'solo' for 1 core/cpu\n~or~\n+ 'multi' for multiple cores/cpus"
        fi

    done
else
    echo -e 'grew installation not found. Check conda environment.\n** If running in screen, make sure calling env has access to grew as well.'
fi
